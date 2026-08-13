from __future__ import annotations

import time

from app.services.agent_grounding.context_overview import (
    CONTEXT_OVERVIEW_INTENTS,
    build_context_overview,
    render_context_overview_answer,
)
from app.services.agent_grounding.contracts import (
    GroundingDecision,
    GroundingIntent,
    GroundingResult,
    GroundingRoute,
    GroundingScope,
    ResolutionQuality,
    SectionTextLoader,
)
from app.services.agent_grounding.intent_router import classify_intent
from app.services.agent_grounding.query_normalizer import normalize_query
from app.services.agent_grounding.response_renderer import render_metadata_answer
from app.services.agent_grounding.section_context_builder import build_section_context, descendant_section_ids
from app.services.agent_grounding.section_reference_parser import parse_section_reference
from app.services.agent_grounding.section_resolver import resolve_metadata_book, resolve_section
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer


class GroundingRouter:
    def __init__(
        self,
        scope: GroundingScope,
        section_text_loader: SectionTextLoader,
        *,
        section_context_max_chars: int,
        context_overview_enabled: bool = False,
        context_overview_max_visible_documents: int = 6,
    ) -> None:
        self.scope = scope
        self.section_text_loader = section_text_loader
        self.section_context_max_chars = section_context_max_chars
        self.context_overview_enabled = context_overview_enabled
        self.context_overview_max_visible_documents = max(1, context_overview_max_visible_documents)

    async def resolve(
        self,
        query: str,
        *,
        input_mode: AgentInputMode = AgentInputMode.TEXT,
        tracer: AgentTurnTracer | None = None,
    ) -> GroundingResult:
        started = time.perf_counter()
        normalized = normalize_query(query)

        # 1. Gọi bộ phân loại ý định ngữ nghĩa bất đồng bộ
        intent = await classify_intent(normalized)
        reference = parse_section_reference(normalized)

        # 2. Luật chặn (Guard Rule): Nếu phân loại là mục lục/tóm tắt chương nhưng không có đề mục cụ thể
        # thì tự động hạ cấp xuống BOOK_SEMANTIC_QUESTION để tránh lỗi định tuyến
        if intent in (GroundingIntent.BOOK_SECTION_SUMMARY, GroundingIntent.BOOK_SECTION_CONTENT):
            if not reference.has_target:
                intent = GroundingIntent.BOOK_SEMANTIC_QUESTION

        result = None
        if intent == GroundingIntent.BOOK_SEMANTIC_QUESTION:
            result = GroundingResult(
                GroundingDecision(
                    GroundingIntent.BOOK_SEMANTIC_QUESTION,
                    GroundingRoute.BOOK_RAG,
                    ResolutionQuality.NOT_FOUND,
                    "semantic_rag_fallback",
                )
            )
        elif intent == GroundingIntent.CLARIFICATION_REQUIRED:
            result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
        elif intent == GroundingIntent.EXTERNAL_CURRENT_INFO or intent in CONTEXT_OVERVIEW_INTENTS:
            result = self._resolve_context_or_external_intent(intent)
        elif intent in (GroundingIntent.BOOK_SECTION_SUMMARY, GroundingIntent.BOOK_SECTION_CONTENT):
            result = await self._resolve_section_intent(normalized, reference, intent)
        else:
            # Các nhóm Metadata
            result = self._resolve_metadata(normalized, intent)

        # Fallback phòng thủ cuối cùng
        if result is None:
            result = GroundingResult(
                GroundingDecision(
                    GroundingIntent.BOOK_SEMANTIC_QUESTION,
                    GroundingRoute.BOOK_RAG,
                    ResolutionQuality.NOT_FOUND,
                    "semantic_rag_fallback",
                )
            )

        if tracer is not None:
            self._record_trace(tracer, input_mode, result, int((time.perf_counter() - started) * 1000))
        return result

    def _resolve_metadata(self, query, intent: GroundingIntent) -> GroundingResult:
        resolution = resolve_metadata_book(self.scope, query)
        if resolution.book is None:
            return self._clarification(resolution.reason_code, resolution.clarification or "Bạn muốn hỏi sách nào?")
        decision = GroundingDecision(
            intent,
            GroundingRoute.BOOK_METADATA,
            resolution.quality,
            resolution.reason_code,
            resolved_book_ids=(resolution.book.id,),
        )
        return GroundingResult(decision, deterministic_answer=render_metadata_answer(resolution.book, intent))

    def _resolve_context_overview(self, intent: GroundingIntent) -> GroundingResult:
        overview = build_context_overview(
            self.scope,
            max_visible_documents=self.context_overview_max_visible_documents,
        )
        decision = GroundingDecision(
            intent,
            GroundingRoute.CONTEXT_OVERVIEW,
            ResolutionQuality.EXACT,
            "context_scope_metadata",
            resolved_book_ids=tuple(book.id for book in overview.books),
        )
        return GroundingResult(
            decision,
            deterministic_answer=render_context_overview_answer(overview, intent),
        )

    def _resolve_context_or_external_intent(self, intent: GroundingIntent) -> GroundingResult | None:
        if intent == GroundingIntent.EXTERNAL_CURRENT_INFO:
            return GroundingResult(
                GroundingDecision(
                    GroundingIntent.EXTERNAL_CURRENT_INFO,
                    GroundingRoute.WEB_POLICY,
                    ResolutionQuality.EXACT,
                    "clear_external_current_info",
                )
            )
        if self.context_overview_enabled:
            return self._resolve_context_overview(intent)
        return None

    async def _resolve_section_intent(self, query, reference, intent: GroundingIntent) -> GroundingResult | None:
        result = await self._resolve_section(query, reference, intent)
        if result.decision.route != GroundingRoute.CLARIFICATION:
            return result

        is_explicit = reference.explicit_path is not None or reference.explicit_ordinal is not None
        return result if is_explicit else None

    async def _resolve_section(self, query, reference, intent: GroundingIntent) -> GroundingResult:
        resolution = resolve_section(self.scope, query, reference)
        if resolution.book is None or resolution.section is None:
            return self._clarification(resolution.reason_code, resolution.clarification or "Bạn muốn hỏi đề mục nào?")

        section_ids = descendant_section_ids(self.scope, resolution.section.id)
        rows = await self.section_text_loader(resolution.book.id, section_ids)
        context = build_section_context(
            resolution.book,
            resolution.section,
            rows,
            max_chars=self.section_context_max_chars,
        )
        decision = GroundingDecision(
            intent,
            GroundingRoute.BOOK_SECTION,
            resolution.quality,
            resolution.reason_code,
            resolved_book_ids=(resolution.book.id,),
            resolved_section_ids=context.section_ids or (resolution.section.id,),
        )
        if not context.has_content:
            answer = f'Tôi đã tìm thấy mục "{resolution.section.title}", nhưng nội dung mục này chưa được trích xuất.'
            return GroundingResult(decision, deterministic_answer=answer)
        return GroundingResult(decision, section_context=context.text, section_context_truncated=context.truncated)

    @staticmethod
    def _clarification(reason_code: str, clarification: str) -> GroundingResult:
        return GroundingResult(
            GroundingDecision(
                GroundingIntent.CLARIFICATION_REQUIRED,
                GroundingRoute.CLARIFICATION,
                ResolutionQuality.AMBIGUOUS,
                reason_code,
                clarification=clarification,
            )
        )

    @staticmethod
    def _record_trace(tracer: AgentTurnTracer, input_mode: AgentInputMode, result: GroundingResult, elapsed_ms: int) -> None:
        decision = result.decision
        tracer.record_grounding_decision(
            input_mode,
            intent=decision.intent.value,
            route=decision.route.value,
            reason_code=decision.reason_code,
            resolved_book_ids=[str(value) for value in decision.resolved_book_ids],
            resolved_section_ids=[str(value) for value in decision.resolved_section_ids],
        )
        tracer.record_latency(input_mode, "grounding_total", elapsed_ms)
        source_by_route = {
            GroundingRoute.CONTEXT_OVERVIEW: AgentAnswerSource.CONTEXT_METADATA,
            GroundingRoute.BOOK_METADATA: AgentAnswerSource.BOOK_METADATA,
            GroundingRoute.BOOK_SECTION: AgentAnswerSource.BOOK_SECTION,
            GroundingRoute.CLARIFICATION: AgentAnswerSource.CLARIFICATION,
            GroundingRoute.WEB_POLICY: AgentAnswerSource.POLICY,
        }
        source = source_by_route.get(decision.route)
        if source is not None:
            tracer.record_answer_source(input_mode, source)
