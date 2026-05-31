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

MessageSaver = Callable[[str, bool], None]
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

    async def publish_transcript(self, role: TranscriptRole, text: str) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized or not self._room.isconnected():
            return

        payload = {
            "v": 1,
            "type": "transcript",
            "role": role,
            "text": normalized,
            "id": str(uuid.uuid4()),
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

        await asyncio.to_thread(self._save_message_sync, normalized, True)
        await self.publish_transcript("user", normalized)
        return True

    async def save_and_publish_assistant(self, text: str) -> bool:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return False

        await asyncio.to_thread(self._save_message_sync, normalized, False)
        await self.publish_transcript("assistant", normalized)
        return True

    async def load_recent_history(self, limit: int) -> list[ChatMessage]:
        return await asyncio.to_thread(self._load_history_sync, limit)

    def _save_message_to_db(self, text: str, is_user: bool) -> None:
        if not self._thread_id:
            return
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
        except Exception as exc:
            log.info(f"Lỗi khi lưu message: {exc}")

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

