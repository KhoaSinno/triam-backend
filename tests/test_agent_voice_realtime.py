import asyncio
import json
import sys
import wave
from pathlib import Path

import aiohttp
from livekit import rtc

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
MOCK_BOOK_ID = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"
TITLE_CONTEXT = "voice realtime test"
VOICE_WAV = Path("tests/fixtures/voice_question.wav")


async def setup_session() -> tuple[str, str]:
    async with aiohttp.ClientSession() as http:
        async with http.post(f"{BASE_URL}/study-contexts", json={"title": TITLE_CONTEXT}) as r:
            r.raise_for_status()
            context_id = (await r.json())["id"]

        async with http.post(
            f"{BASE_URL}/study-contexts/{context_id}/documents",
            json={"book_id": MOCK_BOOK_ID},
        ) as r:
            r.raise_for_status()

        async with http.post(
            f"{BASE_URL}/study-contexts/{context_id}/threads",
            json={"title": TITLE_CONTEXT},
        ) as r:
            r.raise_for_status()
            thread_id = (await r.json())["id"]

        async with http.get(f"{BASE_URL}/live-token/thread/{thread_id}") as r:
            r.raise_for_status()
            token = (await r.json())["token"]

    return thread_id, token


async def check_db(thread_id: str) -> list[dict]:
    async with aiohttp.ClientSession() as http:
        async with http.get(f"{BASE_URL}/threads/{thread_id}/messages") as r:
            r.raise_for_status()
            return await r.json()


async def publish_wav_as_mic(room: rtc.Room, wav_path: Path) -> None:
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        total_frames = wav.getnframes()

        if sample_width != 2:
            raise RuntimeError(f"WAV must be 16-bit PCM, got sample width={sample_width}")

        print(
            f"   🎙️ Publish WAV as mic: {wav_path} "
            f"({sample_rate} Hz, {channels} ch, {total_frames / sample_rate:.2f}s)"
        )

        source = rtc.AudioSource(sample_rate, channels)
        track = rtc.LocalAudioTrack.create_audio_track("voice-question", source)
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        await room.local_participant.publish_track(track, options)

        chunk_frames = max(1, sample_rate // 50)  # 20 ms
        while True:
            pcm = wav.readframes(chunk_frames)
            if not pcm:
                break
            samples_per_channel = len(pcm) // (sample_width * channels)
            frame = rtc.AudioFrame(
                pcm,
                sample_rate,
                channels,
                samples_per_channel,
            )
            await source.capture_frame(frame)

    await source.wait_for_playout()
    await asyncio.sleep(1.0)


async def main() -> None:
    print("=" * 60)
    print("   TEST: Realtime Voice via LiveKit audio track")
    print("=" * 60)

    if not VOICE_WAV.exists():
        raise FileNotFoundError(f"Missing WAV fixture: {VOICE_WAV}")

    thread_id, token = await setup_session()
    print(f"   ✅ Thread ID: {thread_id}")

    room = rtc.Room()
    greeting_received = asyncio.Event()
    user_voice_transcript_received = asyncio.Event()
    assistant_transcript_received = asyncio.Event()
    assistant_chat_received = asyncio.Event()

    transcripts: list[dict] = []
    chats: list[str] = []

    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket):
        try:
            text = packet.data.decode("utf-8")
        except Exception:
            return

        sender = packet.participant.identity if packet.participant else "unknown"

        if packet.topic == "lk.chat" and packet.participant and "agent" in sender.lower():
            if not greeting_received.is_set():
                print(f"   👋 Greeting: {text}")
                greeting_received.set()
            else:
                print(f"   💬 Assistant lk.chat: {text}")
                chats.append(text)
                assistant_chat_received.set()
            return

        if packet.topic != "lk.transcript":
            return

        try:
            payload = json.loads(text)
        except Exception:
            print(f"   ⚠️ Non-JSON transcript: {text[:160]}")
            return

        if not isinstance(payload, dict) or payload.get("type") != "transcript":
            return

        role = str(payload.get("role", ""))
        body = str(payload.get("text", ""))
        if not body:
            return

        transcripts.append(payload)
        print(f"   📝 Transcript {role}: {body}")

        if role == "user":
            user_voice_transcript_received.set()
        elif role == "assistant" and greeting_received.is_set():
            assistant_transcript_received.set()

    print("   🔌 Connect LiveKit...")
    await room.connect(LIVEKIT_URL, token)

    try:
        await asyncio.wait_for(greeting_received.wait(), timeout=60)
    except asyncio.TimeoutError:
        await room.disconnect()
        raise RuntimeError("Timeout waiting for agent greeting")

    await publish_wav_as_mic(room, VOICE_WAV)

    try:
        await asyncio.wait_for(user_voice_transcript_received.wait(), timeout=45)
    except asyncio.TimeoutError:
        print("   ❌ Timeout waiting for user voice transcript")

    try:
        await asyncio.wait_for(assistant_transcript_received.wait(), timeout=60)
    except asyncio.TimeoutError:
        print("   ❌ Timeout waiting for assistant transcript")

    try:
        await asyncio.wait_for(assistant_chat_received.wait(), timeout=15)
    except asyncio.TimeoutError:
        print("   ⚠️ No assistant lk.chat payload after voice")

    await room.disconnect()
    await asyncio.sleep(2.0)

    messages = await check_db(thread_id)
    print(f"\n   🗄️ DB messages: {len(messages)}")
    for item in messages:
        role = "USER " if item.get("is_user") else "AGENT"
        text = str(item.get("text", ""))
        print(f"      {role}: {text[:140]}")

    ok_user = any(x.get("role") == "user" for x in transcripts)
    ok_assistant = any(x.get("role") == "assistant" for x in transcripts)
    ok_db_voice = len(messages) >= 2

    print("\n--- RESULT ---")
    print(f"user voice transcript received: {ok_user}")
    print(f"assistant transcript received: {ok_assistant}")
    print(f"DB has messages: {ok_db_voice}")

    if not (ok_user and ok_assistant and ok_db_voice):
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise
    except Exception as exc:
        print(f"Lỗi: {exc}")
        sys.exit(1)
