from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from app.core.logger import log
from app.services.agent_grounding import GroundingResult, GroundingRoute, GroundingRouter
from app.services.agent_grounding.response_renderer import format_grounding_tool_result
from app.services.agent_observability import AgentAnswerSource, AgentTurnTracer
from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyRequest, AgentPolicyResult
from app.services.agent_policy.renderers import build_rag_text_context, build_section_text_context
from app.services.voice_agent.contracts import VoiceRagResult
from app.services.voice_agent.rag_context import format_rag_context, search_voice_book_context

SearchBookContext = Callable[..., Awaitable[VoiceRagResult]]


class SharedAgentPolicy:
    """Session-scoped policy for text and voice book-grounded decisions.

    This object intentionally holds session-specific state references such as
    tracer and document_ids, so it must never be created as a process-global
    singleton.
    """

    def __init__(
        self,
        *,
        document_ids: list[str],
        grounding_router: GroundingRouter | None,
        tracer: AgentTurnTracer,
        search_book_context: SearchBookContext = search_voice_book_context,
    ) -> None:
        self.document_ids = document_ids
        self.grounding_router = grounding_router
        self.tracer = tracer
        self.search_book_context = search_book_context

    async def resolve(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        started = time.perf_counter()
        try:
            result = await self._resolve(request)
            return result
        finally:
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            resolved = locals().get("result")
            if isinstance(resolved, AgentPolicyResult):
                log.info(
                    "Agent shared policy resolved | "
                    f"mode={request.input_mode.value} | "
                    f"action={resolved.action.value} | "
                    f"source={resolved.answer_source.value} | "
                    f"reason={resolved.reason_code} | "
                    f"books={len(resolved.resolved_book_ids)} | "
                    f"sections={len(resolved.resolved_section_ids)} | "
                    f"retrieval_count={resolved.retrieval_result_count} | "
                    f"latency_ms={elapsed_ms}"
                )

    async def _resolve(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        if self.grounding_router is not None:
            grounding_result = await self.grounding_router.resolve(
                request.query,
                input_mode=request.input_mode,
                tracer=self.tracer,
            )
            if grounding_result.decision.route != GroundingRoute.BOOK_RAG:
                return self._from_grounding_result(grounding_result, request)

        return await self._resolve_rag(request)

    def _from_grounding_result(
        self,
        grounding_result: GroundingResult,
        request: AgentPolicyRequest,
    ) -> AgentPolicyResult:
        decision = grounding_result.decision
        resolved_book_ids = tuple(str(value) for value in decision.resolved_book_ids)
        resolved_section_ids = tuple(str(value) for value in decision.resolved_section_ids)
        tool_marker = format_grounding_tool_result(grounding_result)

        if decision.route == GroundingRoute.BOOK_METADATA:
            return AgentPolicyResult(
                action=AgentPolicyAction.DIRECT_ANSWER,
                answer_source=AgentAnswerSource.BOOK_METADATA,
                reason_code=decision.reason_code,
                user_message=grounding_result.deterministic_answer,
                tool_marker=tool_marker,
                resolved_book_ids=resolved_book_ids,
            )

        if decision.route == GroundingRoute.CLARIFICATION:
            return AgentPolicyResult(
                action=AgentPolicyAction.ASK_CLARIFICATION,
                answer_source=AgentAnswerSource.CLARIFICATION,
                reason_code=decision.reason_code,
                message_key="ask_clarification",
                message_params={"clarification": decision.clarification or "Bạn vui lòng nói rõ câu hỏi."},
                tool_marker=tool_marker,
            )

        if decision.route == GroundingRoute.BOOK_SECTION:
            if grounding_result.section_context:
                return AgentPolicyResult(
                    action=AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT,
                    answer_source=AgentAnswerSource.BOOK_SECTION,
                    reason_code=decision.reason_code,
                    tool_marker=tool_marker,
                    llm_system_context=build_section_text_context(grounding_result.section_context),
                    resolved_book_ids=resolved_book_ids,
                    resolved_section_ids=resolved_section_ids,
                )
            return AgentPolicyResult(
                action=AgentPolicyAction.DIRECT_ANSWER,
                answer_source=AgentAnswerSource.BOOK_SECTION,
                reason_code=decision.reason_code,
                message_key="section_unavailable",
                message_params={"message": grounding_result.deterministic_answer or "Nội dung section chưa được trích xuất."},
                user_message=grounding_result.deterministic_answer,
                tool_marker=tool_marker,
                resolved_book_ids=resolved_book_ids,
                resolved_section_ids=resolved_section_ids,
            )

        if decision.route == GroundingRoute.WEB_POLICY:
            if request.allow_web_permission:
                return AgentPolicyResult(
                    action=AgentPolicyAction.ASK_WEB_PERMISSION,
                    answer_source=AgentAnswerSource.POLICY,
                    reason_code=decision.reason_code,
                    tool_marker=tool_marker,
                    resolved_book_ids=resolved_book_ids,
                )
            return self._web_disabled(decision.reason_code)

        return self._error("unsupported_grounding_route")

    async def _resolve_rag(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        try:
            rag_result = await self.search_book_context(
                request.query,
                request.document_ids,
                tracer=self.tracer,
                input_mode=request.input_mode,
            )
        except Exception as exc:
            self.tracer.record_error(request.input_mode, "book_rag_search_error")
            log.warning(
                "Shared policy RAG search failed | "
                f"mode={request.input_mode.value} | "
                f"document_count={len(request.document_ids)} | "
                f"error_type={type(exc).__name__}"
            )
            return self._error("book_rag_search_error")

        if rag_result.found:
            self.tracer.record_answer_source(request.input_mode, AgentAnswerSource.BOOK_RAG)
            tool_marker = format_rag_context(rag_result)
            return AgentPolicyResult(
                action=AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT,
                answer_source=AgentAnswerSource.BOOK_RAG,
                reason_code="rag_context_found",
                tool_marker=tool_marker,
                llm_system_context=build_rag_text_context(tool_marker),
                retrieval_chunk_ids=_chunk_ids(rag_result),
                retrieval_result_count=len(rag_result.chunks),
            )

        if request.allow_web_permission:
            self.tracer.record_answer_source(request.input_mode, AgentAnswerSource.POLICY)
            return AgentPolicyResult(
                action=AgentPolicyAction.ASK_WEB_PERMISSION,
                answer_source=AgentAnswerSource.POLICY,
                reason_code="rag_context_not_found",
                message_key="book_context_not_found",
                tool_marker=format_rag_context(rag_result),
            )

        return self._web_disabled("rag_context_not_found")

    @staticmethod
    def _web_disabled(reason_code: str) -> AgentPolicyResult:
        return AgentPolicyResult(
            action=AgentPolicyAction.WEB_DISABLED,
            answer_source=AgentAnswerSource.POLICY,
            reason_code=reason_code,
            message_key="web_disabled",
        )

    @staticmethod
    def _error(reason_code: str) -> AgentPolicyResult:
        return AgentPolicyResult(
            action=AgentPolicyAction.ERROR,
            answer_source=AgentAnswerSource.ERROR,
            reason_code=reason_code,
            message_key="book_context_error",
        )


def _chunk_ids(result: VoiceRagResult) -> tuple[str, ...]:
    values: list[str] = []
    for item in result.chunks:
        chunk_id = item.get("id")
        if chunk_id is not None:
            values.append(str(chunk_id))
    return tuple(dict.fromkeys(values))
