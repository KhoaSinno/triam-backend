import json
import uuid

import pytest

from app.services.voice_agent.contracts import LK_TRANSCRIPT_TOPIC
from app.services.voice_agent.transcript_store import VoiceTranscriptStore


class FakeLocalParticipant:
    def __init__(self) -> None:
        self.published: list[tuple[bytes | str, bool, str]] = []

    async def publish_data(self, payload, reliable: bool, topic: str) -> None:
        self.published.append((payload, reliable, topic))


class FakeRoom:
    def __init__(self) -> None:
        self.local_participant = FakeLocalParticipant()

    def isconnected(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_user_transcript_is_deduped_inside_window():
    room = FakeRoom()
    saved: list[tuple[str, bool]] = []
    store = VoiceTranscriptStore(
        room=room,
        thread_id=uuid.uuid4(),
        dedupe_window_seconds=3,
        save_message_sync=lambda text, is_user: saved.append((text, is_user)),
    )

    first = await store.save_and_publish_user("  Xin   chào  ")
    second = await store.save_and_publish_user("Xin chào")

    assert first is True
    assert second is False
    assert saved == [("Xin chào", True)]
    assert len(room.local_participant.published) == 1

    payload, reliable, topic = room.local_participant.published[0]
    data = json.loads(payload.decode("utf-8"))
    assert reliable is True
    assert topic == LK_TRANSCRIPT_TOPIC
    assert data["type"] == "transcript"
    assert data["role"] == "user"
    assert data["text"] == "Xin chào"


@pytest.mark.asyncio
async def test_assistant_transcript_is_saved_and_published():
    room = FakeRoom()
    saved: list[tuple[str, bool]] = []
    store = VoiceTranscriptStore(
        room=room,
        thread_id=uuid.uuid4(),
        dedupe_window_seconds=3,
        save_message_sync=lambda text, is_user: saved.append((text, is_user)),
    )

    ok = await store.save_and_publish_assistant("  Chào bạn  ")

    assert ok is True
    assert saved == [("Chào bạn", False)]
    payload, _, topic = room.local_participant.published[0]
    data = json.loads(payload.decode("utf-8"))
    assert topic == LK_TRANSCRIPT_TOPIC
    assert data["role"] == "assistant"
    assert data["text"] == "Chào bạn"

