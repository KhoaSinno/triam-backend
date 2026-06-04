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

        trace.transcript_final_seen = True
        trace.transcript_char_count = max(0, char_count)
        trace.detected_language = language
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

    def record_latency(self, input_mode: AgentInputMode, stage: str, elapsed_ms: int) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.stage_latency_ms[stage] = max(0, elapsed_ms)

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
            "resolved_book_ids": trace.resolved_book_ids,
            "resolved_section_ids": trace.resolved_section_ids,
            "retrieval_method": trace.retrieval_method,
            "retrieval_result_count": trace.retrieval_result_count,
            "retrieval_chunk_ids": trace.retrieval_chunk_ids,
            "retrieval_learning_unit_ids": trace.retrieval_learning_unit_ids,
            "retrieval_section_ids": trace.retrieval_section_ids,
            "retrieval_scores": trace.retrieval_scores,
            "tool_names": trace.tool_names,
            "answer_source": trace.answer_source.value,
            "assistant_char_count": trace.assistant_char_count,
            "stage_latency_ms": trace.stage_latency_ms,
            "error_code": trace.error_code,
            "correlation_quality": trace.correlation_quality,
        }
