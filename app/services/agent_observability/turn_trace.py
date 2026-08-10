from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from app.core.logger import log
from app.services.agent_observability.contracts import AgentAnswerSource, AgentInputMode, AgentTurnTrace

TraceEmitter = Callable[[str, dict[str, Any]], None]


def _default_emitter(event: str, payload: dict[str, Any]) -> None:
    log.info(f"AGENT_TRACE {event} | {json.dumps(payload, ensure_ascii=True, sort_keys=True)}")


def _string_values(items: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for item in items:
        value = item.get(key)
        if value is not None:
            values.append(str(value))
    return list(dict.fromkeys(values))


class AgentTurnTracer:
    """Session-scoped, best-effort trace collector that never stores raw content."""

    def __init__(
        self,
        *,
        enabled: bool,
        thread_id: str | None,
        room_name: str | None,
        score_precision: int = 4,
        late_transcript_window_seconds: float = 15.0,
        emitter: TraceEmitter | None = None,
    ) -> None:
        self.enabled = enabled
        self.thread_id = thread_id
        self.room_name = room_name
        self.score_precision = max(0, score_precision)
        self.late_transcript_window_seconds = max(0.0, late_transcript_window_seconds)
        self._emitter = emitter or _default_emitter
        self._active: dict[AgentInputMode, AgentTurnTrace] = {}
        self._last_completed: dict[AgentInputMode, AgentTurnTrace] = {}

    def begin_turn(self, input_mode: AgentInputMode) -> str | None:
        if not self.enabled:
            return None

        if input_mode in self._active:
            self.complete_turn(input_mode, error_code="superseded_by_new_turn")

        trace = AgentTurnTrace(
            trace_id=str(uuid.uuid4()),
            thread_id=self.thread_id,
            room_name=self.room_name,
            input_mode=input_mode,
            started_at=datetime.now(timezone.utc),
            started_monotonic=time.monotonic(),
        )
        self._active[input_mode] = trace
        self._emit_safe("turn_started", self._summary(trace))
        return trace.trace_id

    def ensure_turn(self, input_mode: AgentInputMode) -> str | None:
        trace = self._active.get(input_mode)
        if trace:
            return trace.trace_id
        return self.begin_turn(input_mode)

    def has_active_turn(self, input_mode: AgentInputMode) -> bool:
        return input_mode in self._active

    def has_final_transcript(self, input_mode: AgentInputMode) -> bool:
        """Return whether the active turn has a non-empty final user transcript."""
        trace = self._active.get(input_mode)
        return bool(trace and trace.transcript_final_seen and trace.transcript_char_count > 0)

    def record_transcript(
        self,
        input_mode: AgentInputMode,
        *,
        char_count: int,
        language: str | None = None,
        final: bool = True,
    ) -> None:
        if not self.enabled or not final:
            return

        trace = self._active.get(input_mode)
        late_update = False
        if trace is None:
            candidate = self._last_completed.get(input_mode)
            if candidate and not candidate.transcript_final_seen and candidate.completed_monotonic is not None:
                late_update = time.monotonic() - candidate.completed_monotonic <= self.late_transcript_window_seconds
                if late_update:
                    trace = candidate

        if trace is None:
            self.ensure_turn(input_mode)
            trace = self._active.get(input_mode)
        if trace is None:
            return

        now_monotonic = time.monotonic()
        trace.transcript_final_seen = True
        trace.transcript_char_count = max(0, char_count)
        trace.detected_language = language
        trace.transcript_final_monotonic = now_monotonic
        if trace.book_tool_started_monotonic is not None and trace.asr_final_status_at_book_tool == "final_missing":
            trace.book_tool_before_asr_final_ms = max(
                0,
                int((now_monotonic - trace.book_tool_started_monotonic) * 1000),
            )
        if late_update:
            trace.correlation_quality = "late_transcript_last_completed_turn"
            self._emit_safe("late_transcript", self._summary(trace))

    def record_tool(self, input_mode: AgentInputMode, tool_name: str) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None and tool_name not in trace.tool_names:
            trace.tool_names.append(tool_name)

    def record_retrieval(
        self,
        input_mode: AgentInputMode,
        payload: Any,
        *,
        elapsed_ms: int,
        method: str = "vector",
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return

        items = [item for item in payload if isinstance(item, dict)] if isinstance(payload, list) else []
        trace.retrieval_method = method
        trace.retrieval_result_count = len(items)
        trace.rag_candidate_count = len(items)
        trace.retrieval_chunk_ids = _string_values(items, "id")
        trace.retrieval_learning_unit_ids = _string_values(items, "learning_unit_id")
        trace.retrieval_section_ids = _string_values(items, "section_id")
        trace.retrieval_scores = [
            round(float(item["similarity"]), self.score_precision)
            for item in items
            if isinstance(item.get("similarity"), int | float)
        ]
        trace.stage_latency_ms["retrieval"] = max(0, elapsed_ms)
        self._emit_safe("retrieval_completed", self._summary(trace))

    def record_rag_context(
        self,
        input_mode: AgentInputMode,
        *,
        selected_count: int,
        content_char_count: int,
        budget_mode: str,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.rag_context_selected_count = max(0, selected_count)
        trace.rag_context_char_count = max(0, content_char_count)
        trace.rag_context_budget_mode = budget_mode
        self._emit_safe("rag_context_formatted", self._summary(trace))

    def record_book_grounding_tool_started(self, input_mode: AgentInputMode) -> None:
        """Record ASR-final timing at the first user-facing book-search boundary."""
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        now_monotonic = time.monotonic()
        trace.book_tool_started_monotonic = now_monotonic
        if trace.transcript_final_seen and trace.transcript_final_monotonic is not None:
            trace.asr_final_status_at_book_tool = "final_seen"
            trace.asr_final_before_book_tool_ms = max(
                0,
                int((now_monotonic - trace.transcript_final_monotonic) * 1000),
            )
        else:
            trace.asr_final_status_at_book_tool = "final_missing"
        self._emit_safe("book_grounding_tool_started", self._summary(trace))

    def record_grounding_decision(
        self,
        input_mode: AgentInputMode,
        *,
        intent: str,
        route: str,
        reason_code: str,
        resolved_book_ids: list[str],
        resolved_section_ids: list[str],
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.detected_intent = intent
        trace.grounding_route = route
        trace.grounding_reason_code = reason_code
        trace.resolved_book_ids = list(dict.fromkeys(resolved_book_ids))
        trace.resolved_section_ids = list(dict.fromkeys(resolved_section_ids))
        self._emit_safe("grounding_resolved", self._summary(trace))

    def record_latency(self, input_mode: AgentInputMode, stage: str, elapsed_ms: int) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.stage_latency_ms[stage] = max(0, elapsed_ms)

    def record_query_guard(
        self,
        input_mode: AgentInputMode,
        *,
        reason_code: str,
        guard_mode: str,
        overlap_ratio: float | None = None,
        important_overlap_ratio: float | None = None,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.query_guard_reason_code = reason_code
        trace.query_guard_mode = guard_mode
        trace.query_guard_overlap_ratio = (
            round(overlap_ratio, self.score_precision) if overlap_ratio is not None else None
        )
        trace.query_guard_important_overlap_ratio = (
            round(important_overlap_ratio, self.score_precision)
            if important_overlap_ratio is not None
            else None
        )

    def record_answer_source(self, input_mode: AgentInputMode, source: AgentAnswerSource) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.answer_source = source

    def record_assistant(self, input_mode: AgentInputMode, *, char_count: int) -> None:
        trace = self._active.get(input_mode)
        if trace is not None:
            trace.assistant_char_count = max(0, char_count)

    def record_error(self, input_mode: AgentInputMode, error_code: str) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.error_code = error_code
            trace.answer_source = AgentAnswerSource.ERROR

    def record_tool_reply_watchdog_scheduled(
        self,
        input_mode: AgentInputMode,
        *,
        tool_name: str,
        grace_ms: int,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_scheduled = True
        if tool_name not in trace.tool_reply_watchdog_tool_names:
            trace.tool_reply_watchdog_tool_names.append(tool_name)
        trace.stage_latency_ms["tool_reply_watchdog_grace"] = grace_ms
        self._emit_safe("watchdog_scheduled", self._summary(trace))

    def record_tool_reply_watchdog_fired(
        self,
        input_mode: AgentInputMode,
        *,
        tool_name: str,
        elapsed_ms: int | None,
        reason: str,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_fired = True
        trace.tool_reply_watchdog_reason = reason
        trace.forced_reply_reason = reason
        if elapsed_ms is not None:
            trace.tool_result_to_speech_ms = elapsed_ms
        self._emit_safe("watchdog_fired", self._summary(trace))

    def record_tool_reply_watchdog_bypassed(
        self,
        input_mode: AgentInputMode,
        *,
        reason: str,
        tool_name: str,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_fired = False
        trace.tool_reply_watchdog_reason = reason
        self._emit_safe("watchdog_bypassed", self._summary(trace))

    def record_tool_reply_watchdog_cancelled(
        self,
        input_mode: AgentInputMode,
        *,
        reason: str,
    ) -> None:
        trace = self._active.get(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_reason = f"cancelled_{reason}"
        self._emit_safe("watchdog_cancelled", self._summary(trace))

    def record_tool_reply_speech_created(
        self,
        input_mode: AgentInputMode,
        *,
        source: str | None = None,
        elapsed_ms: int | None = None,
    ) -> None:
        trace = self._active.get(input_mode)
        if trace is None:
            return
        if elapsed_ms is not None:
            trace.tool_result_to_speech_ms = elapsed_ms
        self._emit_safe("speech_created", self._summary(trace))

    def complete_turn(self, input_mode: AgentInputMode, *, error_code: str | None = None) -> dict[str, Any] | None:
        if not self.enabled:
            return None

        trace = self._active.pop(input_mode, None)
        if trace is None:
            return None

        trace.completed_at = datetime.now(timezone.utc)
        trace.completed_monotonic = time.monotonic()
        trace.stage_latency_ms["turn_total"] = max(0, int((trace.completed_monotonic - trace.started_monotonic) * 1000))
        if error_code:
            trace.error_code = error_code
        self._last_completed[input_mode] = trace
        summary = self._summary(trace)
        self._emit_safe("turn_completed", summary)
        return summary

    def _get_or_begin(self, input_mode: AgentInputMode) -> AgentTurnTrace | None:
        if not self.enabled:
            return None
        if input_mode not in self._active:
            self.begin_turn(input_mode)
        return self._active.get(input_mode)

    def _emit_safe(self, event: str, payload: dict[str, Any]) -> None:
        try:
            self._emitter(event, payload)
        except Exception as exc:
            log.warning(f"Agent trace emit failed | event={event} | error_type={type(exc).__name__}")

    @staticmethod
    def _summary(trace: AgentTurnTrace) -> dict[str, Any]:
        return {
            "trace_id": trace.trace_id,
            "thread_id": trace.thread_id,
            "room_name": trace.room_name,
            "input_mode": trace.input_mode.value,
            "started_at": trace.started_at.isoformat(),
            "completed_at": trace.completed_at.isoformat() if trace.completed_at else None,
            "transcript_final_seen": trace.transcript_final_seen,
            "transcript_char_count": trace.transcript_char_count,
            "detected_language": trace.detected_language,
            "detected_intent": trace.detected_intent,
            "grounding_route": trace.grounding_route,
            "grounding_reason_code": trace.grounding_reason_code,
            "resolved_book_ids": trace.resolved_book_ids,
            "resolved_section_ids": trace.resolved_section_ids,
            "retrieval_method": trace.retrieval_method,
            "retrieval_result_count": trace.retrieval_result_count,
            "retrieval_chunk_ids": trace.retrieval_chunk_ids,
            "retrieval_learning_unit_ids": trace.retrieval_learning_unit_ids,
            "retrieval_section_ids": trace.retrieval_section_ids,
            "retrieval_scores": trace.retrieval_scores,
            "rag_candidate_count": trace.rag_candidate_count,
            "rag_context_selected_count": trace.rag_context_selected_count,
            "rag_context_char_count": trace.rag_context_char_count,
            "rag_context_budget_mode": trace.rag_context_budget_mode,
            "asr_final_status_at_book_tool": trace.asr_final_status_at_book_tool,
            "asr_final_before_book_tool_ms": trace.asr_final_before_book_tool_ms,
            "book_tool_before_asr_final_ms": trace.book_tool_before_asr_final_ms,
            "tool_names": trace.tool_names,
            "query_guard_reason_code": trace.query_guard_reason_code,
            "query_guard_mode": trace.query_guard_mode,
            "query_guard_overlap_ratio": trace.query_guard_overlap_ratio,
            "query_guard_important_overlap_ratio": trace.query_guard_important_overlap_ratio,
            "answer_source": trace.answer_source.value,
            "assistant_char_count": trace.assistant_char_count,
            "stage_latency_ms": trace.stage_latency_ms,
            "error_code": trace.error_code,
            "tool_reply_watchdog_scheduled": trace.tool_reply_watchdog_scheduled,
            "tool_reply_watchdog_fired": trace.tool_reply_watchdog_fired,
            "tool_reply_watchdog_tool_names": trace.tool_reply_watchdog_tool_names,
            "tool_reply_watchdog_reason": trace.tool_reply_watchdog_reason,
            "tool_result_to_speech_ms": trace.tool_result_to_speech_ms,
            "forced_reply_reason": trace.forced_reply_reason,
            "correlation_quality": trace.correlation_quality,
        }
