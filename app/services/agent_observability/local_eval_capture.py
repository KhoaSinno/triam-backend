"""Opt-in local capture of completed agent turns for manual evaluation.

The ordinary agent trace intentionally excludes user text and source content. This
module is a separate artifact writer for an explicitly enabled local test run.
"""

from __future__ import annotations

import json
import re
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.logger import log


def _safe_run_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return normalized.strip(".-") or datetime.now(timezone.utc).strftime("voice-%Y%m%d-%H%M%S")


class LocalEvaluationCapture:
    """Best-effort per-turn writer used only by a deliberately enabled local run."""

    def __init__(
        self,
        *,
        enabled: bool,
        run_id: str,
        root_dir: str,
        thread_id: str | None,
        room_name: str | None,
    ) -> None:
        self.enabled = enabled
        self.run_id = _safe_run_id(run_id)
        self.thread_id = thread_id
        self.room_name = room_name
        self._lock = threading.Lock()
        self._turns: dict[str, dict[str, Any]] = {}
        self.run_dir = Path(root_dir) / self.run_id
        self.turns_dir = self.run_dir / "turns"
        if self.enabled:
            try:
                self.turns_dir.mkdir(parents=True, exist_ok=True)
                self._write_json(
                    self.run_dir / "run.json",
                    {
                        "schema_version": 1,
                        "run_id": self.run_id,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "thread_id": self.thread_id,
                        "room_name": self.room_name,
                        "purpose": "local_manual_evaluation_only",
                    },
                )
                log.info(f"Local evaluation capture enabled | run_id={self.run_id} | dir={self.run_dir}")
            except Exception as exc:
                self.enabled = False
                log.warning(f"Local evaluation capture disabled after setup failure | error_type={type(exc).__name__}")

    def emit_trace(self, event: str, payload: dict[str, Any]) -> None:
        """Preserve normal safe tracing and attach its metadata to the local artifact."""
        log.info(f"AGENT_TRACE {event} | {json.dumps(payload, ensure_ascii=True, sort_keys=True)}")
        if not self.enabled:
            return
        trace_id = str(payload.get("trace_id") or "")
        if not trace_id:
            return
        try:
            with self._lock:
                turn = self._turn(trace_id)
                turn["trace"] = payload.copy()
                turn["trace_event"] = event
                self._flush(trace_id)
        except Exception as exc:
            log.warning(f"Local evaluation trace capture failed | event={event} | error_type={type(exc).__name__}")

    def record_user_text(self, *, trace_id: str | None, text: str, source: str, language: str | None = None) -> None:
        self._record_text(trace_id, "user", text, source=source, language=language)

    def record_assistant_text(self, *, trace_id: str | None, text: str) -> None:
        self._record_text(trace_id, "assistant", text, source="committed_assistant")

    def record_rendered_rag_context(self, *, trace_id: str | None, query: str, context_text: str) -> None:
        if not self.enabled or not trace_id or not context_text:
            return
        try:
            with self._lock:
                turn = self._turn(trace_id)
                turn["retrieved_context"] = {
                    "query_sent_to_retrieval": query,
                    "rendered_context": context_text,
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                }
                self._flush(trace_id)
        except Exception as exc:
            log.warning(f"Local evaluation context capture failed | error_type={type(exc).__name__}")

    def _record_text(self, trace_id: str | None, role: str, text: str, *, source: str, language: str | None = None) -> None:
        if not self.enabled or not trace_id or not text:
            return
        try:
            with self._lock:
                turn = self._turn(trace_id)
                turn[role] = {
                    "text": text,
                    "source": source,
                    "language": language,
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                }
                self._flush(trace_id)
        except Exception as exc:
            log.warning(f"Local evaluation text capture failed | role={role} | error_type={type(exc).__name__}")

    def _turn(self, trace_id: str) -> dict[str, Any]:
        return self._turns.setdefault(
            trace_id,
            {
                "schema_version": 1,
                "run_id": self.run_id,
                "trace_id": trace_id,
                "thread_id": self.thread_id,
                "room_name": self.room_name,
                "evaluation_status": "unreviewed",
                "case_id": None,
            },
        )

    def _flush(self, trace_id: str) -> None:
        self._write_json(self.turns_dir / f"{trace_id}.json", self._turns[trace_id])

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        temporary_path = path.with_suffix(f"{path.suffix}.{uuid.uuid4().hex}.tmp")
        temporary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary_path.replace(path)
