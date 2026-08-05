from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.services.voice_agent.contracts import VoiceContextResolution


@dataclass(frozen=True)
class ActiveVoiceContext:
    context_id: uuid.UUID | None
    thread_id: uuid.UUID | None
    document_ids: tuple[str, ...]
    version: int
    context_title: str | None = None
    thread_title: str | None = None

    @classmethod
    def from_resolution(cls, value: VoiceContextResolution, *, version: int = 1) -> "ActiveVoiceContext":
        return cls(
            context_id=value.context_id,
            thread_id=value.thread_id,
            document_ids=value.document_ids,
            version=version,
            context_title=value.context_title,
            thread_title=value.thread_title,
        )


class ActiveVoiceContextState:
    """Small in-memory source of truth for one LiveKit job's active scope."""

    def __init__(self, initial: ActiveVoiceContext) -> None:
        self._current = initial

    @property
    def current(self) -> ActiveVoiceContext:
        return self._current

    def replace(self, value: VoiceContextResolution) -> ActiveVoiceContext:
        self._current = ActiveVoiceContext.from_resolution(
            value,
            version=self._current.version + 1,
        )
        return self._current
