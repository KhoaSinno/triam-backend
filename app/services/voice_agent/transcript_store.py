import asyncio
import json
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, cast

from sqlmodel import Session, select

from app.core.logger import log
from app.models.db_models import ChatMessage
from app.services.voice_agent.contracts import LK_TRANSCRIPT_TOPIC, TranscriptRole

MessageSaver = Callable[[str, bool], uuid.UUID | None]
HistoryLoader = Callable[[int], list[ChatMessage]]


def normalize_transcript_text(text: str) -> str:
    return " ".join((text or "").split())


class VoiceTranscriptStore:
    def __init__(
        self,
        *,
        room: Any,
        thread_id: uuid.UUID | None,
        dedupe_window_seconds: int,
        save_message_sync: MessageSaver | None = None,
        load_history_sync: HistoryLoader | None = None,
        db_engine: Any = None,
    ) -> None:
        self._room = room
        self._thread_id = thread_id
        self._seen_user_texts: dict[str, datetime] = {}
        self._dedupe_window_seconds = max(dedupe_window_seconds, 1)
        self._save_message_sync = save_message_sync or self._save_message_to_db
        self._load_history_sync = load_history_sync or self._load_history_from_db
        self._engine = db_engine

    def _get_engine(self) -> Any:
        if self._engine is None:
            from sqlalchemy.pool import NullPool
            from sqlmodel import create_engine

            from app.core.config import settings
            self._engine = create_engine(
                settings.DATABASE_URL,
                echo=False,
                poolclass=NullPool,
            )
        return self._engine

    async def publish_transcript(
        self,
        role: TranscriptRole,
        text: str,
        *,
        message_id: uuid.UUID | None = None,
    ) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized or not self._room.isconnected():
            return

        transcript_id = message_id or uuid.uuid4()
        payload = {
            "v": 1,
            "type": "transcript",
            "role": role,
            "text": normalized,
            "id": str(transcript_id),
            "message_id": str(message_id) if message_id else None,
            "thread_id": str(self._thread_id) if self._thread_id else None,
            "source": "livekit",
            "status": "committed",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        try:
            await self._room.local_participant.publish_data(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                reliable=True,
                topic=LK_TRANSCRIPT_TOPIC,
            )
        except Exception as exc:
            log.info(f"Transcript publish failed: {exc}")

    async def save_and_publish_user(self, text: str) -> bool:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return False

        now = datetime.now(timezone.utc)
        last_seen = self._seen_user_texts.get(normalized)
        if last_seen and (now - last_seen).total_seconds() < self._dedupe_window_seconds:
            return False
        self._seen_user_texts[normalized] = now

        message_id = await self._save_message_for_transcript(normalized, True)
        await self.publish_transcript("user", normalized, message_id=message_id)
        return True

    async def save_and_publish_assistant(self, text: str) -> bool:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return False

        message_id = await self._save_message_for_transcript(normalized, False)
        await self.publish_transcript("assistant", normalized, message_id=message_id)
        return True

    async def load_recent_history(self, limit: int) -> list[ChatMessage]:
        return await asyncio.to_thread(self._load_history_sync, limit)

    async def _save_message_for_transcript(self, text: str, is_user: bool) -> uuid.UUID | None:
        try:
            return await asyncio.to_thread(self._save_message_sync, text, is_user)
        except Exception as exc:
            self._log_transcript_save_failure(text=text, is_user=is_user, exc=exc)
            return None

    def _save_message_to_db(self, text: str, is_user: bool) -> uuid.UUID | None:
        if not self._thread_id:
            return None
        try:
            with Session(self._get_engine()) as db:
                new_msg = ChatMessage(
                    thread_id=self._thread_id,
                    is_user=is_user,
                    text=text,
                    source="livekit",
                    timestamp=datetime.now(timezone.utc),
                )
                db.add(new_msg)
                db.commit()
                db.refresh(new_msg)
                return new_msg.id
        except Exception as exc:
            self._log_transcript_save_failure(text=text, is_user=is_user, exc=exc)
            return None

    def _log_transcript_save_failure(self, *, text: str, is_user: bool, exc: Exception) -> None:
        role = "user" if is_user else "assistant"
        log.info(
            "Transcript DB save failed | "
            f"thread_id={self._thread_id} | role={role} | "
            f"text_len={len(text)} | error_type={type(exc).__name__}"
        )

    def _load_history_from_db(self, limit: int) -> list[ChatMessage]:
        if not self._thread_id:
            return []
        with Session(self._get_engine()) as db:
            messages = db.exec(
                select(ChatMessage)
                .where(ChatMessage.thread_id == self._thread_id)
                .order_by(cast(Any, ChatMessage.timestamp).desc())
                .limit(limit)
            ).all()
            return list(reversed(messages))

