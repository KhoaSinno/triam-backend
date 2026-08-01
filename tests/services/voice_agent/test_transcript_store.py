import json
import uuid

import pytest

from app.services.voice_agent import transcript_store
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


def decode_payload(room: FakeRoom, index: int = 0) -> dict:
    payload, _, _ = room.local_participant.published[index]
    return json.loads(payload.decode("utf-8"))


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
    assert len(room.local_participant.published) == 2

    payload, reliable, topic = room.local_participant.published[0]
    data = json.loads(payload.decode("utf-8"))
    assert reliable is True
    assert topic == LK_TRANSCRIPT_TOPIC
    assert data["type"] == "transcript"
    assert data["role"] == "user"
    assert data["text"] == "Xin chào"
    assert data["message_id"] is None
    assert data["source"] == "livekit"
    assert data["status"] == "pending"

    committed = decode_payload(room, 1)
    assert committed["id"] == data["id"]
    assert committed["status"] == "committed"


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
    assert data["status"] == "pending"
    assert decode_payload(room, 1)["status"] == "committed"


@pytest.mark.asyncio
async def test_user_transcript_uses_db_message_id_when_saver_returns_id():
    room = FakeRoom()
    thread_id = uuid.uuid4()
    message_id = uuid.uuid4()
    store = VoiceTranscriptStore(
        room=room,
        thread_id=thread_id,
        dedupe_window_seconds=3,
        save_message_sync=lambda _text, _is_user: message_id,
    )

    ok = await store.save_and_publish_user("Tác giả là ai?")

    assert ok is True
    pending = decode_payload(room, 0)
    data = decode_payload(room, 1)
    assert data["v"] == 1
    assert data["type"] == "transcript"
    assert data["role"] == "user"
    assert data["text"] == "Tác giả là ai?"
    assert pending["status"] == "pending"
    assert data["id"] == pending["id"]
    assert data["message_id"] == str(message_id)
    assert data["thread_id"] == str(thread_id)
    assert data["source"] == "livekit"
    assert data["status"] == "committed"
    assert data["ts"]


@pytest.mark.asyncio
async def test_assistant_transcript_uses_db_message_id_when_saver_returns_id():
    room = FakeRoom()
    thread_id = uuid.uuid4()
    message_id = uuid.uuid4()
    store = VoiceTranscriptStore(
        room=room,
        thread_id=thread_id,
        dedupe_window_seconds=3,
        save_message_sync=lambda _text, _is_user: message_id,
    )

    ok = await store.save_and_publish_assistant("John Steinbeck là tác giả.")

    assert ok is True
    pending = decode_payload(room, 0)
    data = decode_payload(room, 1)
    assert data["role"] == "assistant"
    assert pending["status"] == "pending"
    assert data["id"] == pending["id"]
    assert data["message_id"] == str(message_id)
    assert data["thread_id"] == str(thread_id)


@pytest.mark.asyncio
async def test_transcript_still_publishes_with_transient_id_when_saver_returns_none():
    room = FakeRoom()
    thread_id = uuid.uuid4()
    store = VoiceTranscriptStore(
        room=room,
        thread_id=thread_id,
        dedupe_window_seconds=3,
        save_message_sync=lambda _text, _is_user: None,
    )

    ok = await store.save_and_publish_assistant("Không có dữ liệu.")

    assert ok is True
    pending = decode_payload(room, 0)
    data = decode_payload(room, 1)
    assert pending["status"] == "pending"
    assert data["status"] == "committed"
    assert uuid.UUID(data["id"])
    assert data["id"] == pending["id"]
    assert data["message_id"] is None
    assert data["thread_id"] == str(thread_id)


@pytest.mark.asyncio
async def test_transcript_still_publishes_when_saver_raises_without_logging_raw_text(monkeypatch):
    room = FakeRoom()
    thread_id = uuid.uuid4()
    raw_text = "Nội dung nhạy cảm không được log đầy đủ"
    logs: list[str] = []

    def broken_saver(_text: str, _is_user: bool) -> uuid.UUID | None:
        raise RuntimeError("database timeout")

    monkeypatch.setattr(transcript_store.log, "info", lambda message: logs.append(message))
    store = VoiceTranscriptStore(
        room=room,
        thread_id=thread_id,
        dedupe_window_seconds=3,
        save_message_sync=broken_saver,
    )

    ok = await store.save_and_publish_user(raw_text)

    assert ok is True
    pending = decode_payload(room, 0)
    data = decode_payload(room, 1)
    assert pending["status"] == "pending"
    assert data["status"] == "committed"
    assert uuid.UUID(data["id"])
    assert data["id"] == pending["id"]
    assert data["message_id"] is None
    assert data["text"] == raw_text
    assert logs
    assert "Transcript DB save failed" in logs[0]
    assert f"thread_id={thread_id}" in logs[0]
    assert "role=user" in logs[0]
    assert f"text_len={len(raw_text)}" in logs[0]
    assert "RuntimeError" in logs[0]
    assert raw_text not in logs[0]

