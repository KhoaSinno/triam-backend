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


class VoiceTurnState:
    def __init__(self, *, clock=time.monotonic) -> None:
        self._clock = clock
        self._final_transcript: VoiceTranscriptSnapshot | None = None
        self._committed_user_text: VoiceTranscriptSnapshot | None = None

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
