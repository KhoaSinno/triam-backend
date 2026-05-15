import asyncio
import json
import sys
from pathlib import Path

import aiohttp
from livekit import rtc

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"

# NOTE: Use a real book id available in your DB if needed.
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"
TITLE_CONTEXT = "realtime transcript test"
TEST_QUESTION = "Cho tôi 1 câu trả lời ngắn gọn về nội dung sách."

WORKER_LOG_PATH = Path("worker.log")


def _safe_tail_text(path: Path, max_chars: int = 8000) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if len(data) <= max_chars:
        return data
    return data[-max_chars:]


async def main() -> None:
    print("=" * 60)
    print("   TEST: Realtime GPT transcript publish (lk.transcript)")
    print("=" * 60)

    async with aiohttp.ClientSession() as session:
        print("\n[1/4] 📦 Create Study Context...")
        async with session.post(f"{BASE_URL}/study-contexts", json={"title": TITLE_CONTEXT}) as r:
            if r.status != 200:
                print(f"❌ Create context failed: {r.status} {await r.text()}")
                return
            ctx = await r.json()
            context_id = ctx["id"]
            print(f"   ✅ Context ID: {context_id}")

        print(f"\n[2/4] 📚 Attach book {MOCK_BOOK_ID}...")
        async with session.post(
            f"{BASE_URL}/study-contexts/{context_id}/documents",
            json={"book_id": MOCK_BOOK_ID},
        ) as r:
            if r.status != 200:
                print(f"   ⚠️ Warning: attach book failed (may not exist): {r.status} {await r.text()}")
            else:
                print("   ✅ Book attached")

        print("\n[3/4] 💬 Create thread & get LiveKit token...")
        async with session.post(
            f"{BASE_URL}/study-contexts/{context_id}/threads",
            json={"title": "realtime transcript thread"},
        ) as r:
            if r.status != 200:
                print(f"❌ Create thread failed: {r.status} {await r.text()}")
                return
            thread = await r.json()
            thread_id = thread["id"]
            print(f"   ✅ Thread ID: {thread_id}")

        async with session.get(f"{BASE_URL}/live-token/thread/{thread_id}") as r:
            if r.status != 200:
                print(f"❌ Get live token failed: {r.status} {await r.text()}")
                return
            token_data = await r.json()
            token = token_data["token"]
            print("   ✅ LiveKit token OK")

    print(
        "\n[4/4] 🔌 Connect LiveKit, send question, validate lk.chat + lk.transcript...")

    room = rtc.Room()

    greeting_received = asyncio.Event()
    answer_received = asyncio.Event()
    assistant_transcript_received = asyncio.Event()
    user_transcript_received = asyncio.Event()

    latest_chat: list[str] = []
    latest_transcripts: list[dict] = []

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        try:
            data = packet.data.decode("utf-8")
        except Exception:
            return

        sender = packet.participant.identity if packet.participant else "unknown"

        if packet.topic == "lk.chat":
            if packet.participant and "agent" in sender.lower():
                if not greeting_received.is_set():
                    print(f"\n   👋 Greeting (lk.chat) from {sender}: {data}")
                    greeting_received.set()
                else:
                    print(f"\n   💬 Answer (lk.chat) from {sender}: {data}")
                    latest_chat.append(data)
                    answer_received.set()

        if packet.topic == "lk.transcript":
            # Expected JSON payload
            try:
                obj = json.loads(data)
            except Exception:
                print(f"\n   ⚠️ Non-JSON lk.transcript payload: {data[:200]}")
                return

            if not isinstance(obj, dict):
                return

            latest_transcripts.append(obj)
            role = str(obj.get("role", ""))
            text = str(obj.get("text", ""))
            if role == "user" and text:
                print(f"\n   📝 Transcript (user): {text}")
                user_transcript_received.set()
            if role == "assistant" and text:
                print(f"\n   📝 Transcript (assistant): {text}")
                assistant_transcript_received.set()

    await room.connect(LIVEKIT_URL, token)

    print("   ⏳ Wait for greeting...")
    try:
        await asyncio.wait_for(greeting_received.wait(), timeout=60)
    except asyncio.TimeoutError:
        print("❌ Timeout waiting for greeting")
        await room.disconnect()
        return

    print(f"   📤 Send question to lk.chat: {TEST_QUESTION}")
    await room.local_participant.publish_data(
        TEST_QUESTION.encode("utf-8"),
        reliable=True,
        topic="lk.chat",
    )

    try:
        await asyncio.wait_for(answer_received.wait(), timeout=60)
    except asyncio.TimeoutError:
        print("⚠️ Timeout waiting for answer on lk.chat")

    try:
        await asyncio.wait_for(user_transcript_received.wait(), timeout=30)
    except asyncio.TimeoutError:
        print("⚠️ Timeout waiting for user lk.transcript")

    try:
        await asyncio.wait_for(assistant_transcript_received.wait(), timeout=60)
    except asyncio.TimeoutError:
        print("⚠️ Timeout waiting for assistant lk.transcript")

    await room.disconnect()

    # Post-checks
    ok_chat = len(latest_chat) > 0
    ok_transcript = any(
        isinstance(x, dict)
        and x.get("type") == "transcript"
        and x.get("role") == "assistant"
        and isinstance(x.get("text"), str)
        and x.get("text")
        for x in latest_transcripts
    )

    ok_transcript_user = any(
        isinstance(x, dict)
        and x.get("type") == "transcript"
        and x.get("role") == "user"
        and isinstance(x.get("text"), str)
        and x.get("text")
        for x in latest_transcripts
    )

    print("\n--- RESULT ---")
    print(f"lk.chat answer received: {ok_chat}")
    print(f"lk.transcript assistant JSON received: {ok_transcript}")
    print(f"lk.transcript user JSON received: {ok_transcript_user}")

    if WORKER_LOG_PATH.exists():
        tail = _safe_tail_text(WORKER_LOG_PATH)
        interesting = [
            line
            for line in tail.splitlines()
            if "Starting realtime session with model" in line
            or "Realtime model not available" in line
            or "trying fallback" in line
            or "Transcript publish failed" in line
        ]
        if interesting:
            print("\n--- worker.log (tail highlights) ---")
            for line in interesting[-30:]:
                print(line)

    if not ok_chat or not ok_transcript or not ok_transcript_user:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except SystemExit as e:
        raise
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)
