from __future__ import annotations

import time

from app.services.agent_grounding.contracts import (
    GroundingDecision,
    GroundingIntent,
    GroundingResult,
    GroundingRoute,
    GroundingScope,
    ResolutionQuality,
    SectionTextLoader,
)
from app.services.agent_grounding.intent_router import detect_metadata_intent, detect_section_intent
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
    ) -> None:
        self.scope = scope
        self.section_text_loader = section_text_loader
        self.section_context_max_chars = section_context_max_chars

    async def resolve(
        self,
        query: str,
        *,
        input_mode: AgentInputMode = AgentInputMode.TEXT,
        tracer: AgentTurnTracer | None = None,
    ) -> GroundingResult:
        started = time.perf_counter()
        normalized = normalize_query(query)

        metadata_intent = detect_metadata_intent(normalized)
        if metadata_intent is not None:
            result = self._resolve_metadata(normalized, metadata_intent)
        else:
            reference = parse_section_reference(normalized)
            section_intent = detect_section_intent(normalized, reference)

            result = None
            if section_intent == GroundingIntent.CLARIFICATION_REQUIRED:
                result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
            elif section_intent is not None:
                result = await self._resolve_section(normalized, reference, section_intent)
                if result.decision.route == GroundingRoute.CLARIFICATION:
                    is_explicit = reference.explicit_path is not None or reference.explicit_ordinal is not None
                    if not is_explicit:
                        result = None

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
            GroundingRoute.BOOK_METADATA: AgentAnswerSource.BOOK_METADATA,
            GroundingRoute.BOOK_SECTION: AgentAnswerSource.BOOK_SECTION,
            GroundingRoute.CLARIFICATION: AgentAnswerSource.CLARIFICATION,
            GroundingRoute.WEB_POLICY: AgentAnswerSource.POLICY,
        }
        source = source_by_route.get(decision.route)
        if source is not None:
            tracer.record_answer_source(input_mode, source)
