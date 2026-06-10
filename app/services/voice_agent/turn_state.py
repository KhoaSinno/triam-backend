from __future__ import annotations

import time
from dataclasses import dataclass

from app.services.voice_agent.transcript_store import normalize_transcript_text


@dataclass(frozen=True)
class VoiceTranscriptSnapshot:
    text: str
    created_monotonic: float
    language: str | None = None
    source: str = "final_transcript"


@dataclass(frozen=True)
class PendingVoiceClarification:
    prompt_text: str
    candidate_query: str | None
    reason_code: str
    created_monotonic: float
    source: str = "query_guard"


class VoiceTurnState:
    def __init__(self, *, clock=time.monotonic) -> None:
        self._clock = clock
        self._final_transcript: VoiceTranscriptSnapshot | None = None
        self._committed_user_text: VoiceTranscriptSnapshot | None = None
        self._pending_clarification: PendingVoiceClarification | None = None

    def record_final_transcript(self, text: str, language: str | None = None) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return
        self._final_transcript = VoiceTranscriptSnapshot(
            text=normalized,
            created_monotonic=self._clock(),
            language=language,
            source="final_transcript",
        )

    def record_committed_user_text(self, text: str, language: str | None = None) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return
        self._committed_user_text = VoiceTranscriptSnapshot(
            text=normalized,
            created_monotonic=self._clock(),
            language=language,
            source="committed_user_item",
        )

    def recent_transcript(self, ttl_seconds: float) -> VoiceTranscriptSnapshot | None:
        candidates = [item for item in (self._committed_user_text, self._final_transcript) if item is not None]
        if not candidates:
            return None
        newest = max(candidates, key=lambda item: item.created_monotonic)
        if self._clock() - newest.created_monotonic > max(0.0, ttl_seconds):
            return None
        return newest

    def set_pending_clarification(
        self,
        *,
        prompt_text: str,
        reason_code: str,
        candidate_query: str | None = None,
        source: str = "query_guard",
    ) -> None:
        normalized_prompt = normalize_transcript_text(prompt_text)
        normalized_query = normalize_transcript_text(candidate_query or "")
        if not normalized_prompt:
            return
        self._pending_clarification = PendingVoiceClarification(
            prompt_text=normalized_prompt,
            candidate_query=normalized_query or None,
            reason_code=reason_code,
            created_monotonic=self._clock(),
            source=source,
        )

    def recent_pending_clarification(self, ttl_seconds: float) -> PendingVoiceClarification | None:
        pending = self._pending_clarification
        if pending is None:
            return None
        if self._clock() - pending.created_monotonic > max(0.0, ttl_seconds):
            self._pending_clarification = None
            return None
        return pending

    def clear_pending_clarification(self) -> None:
        self._pending_clarification = None
