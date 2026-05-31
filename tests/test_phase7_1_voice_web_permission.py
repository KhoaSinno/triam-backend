"""
Manual integration test for Phase 7.1 voice web-search permission.

Flow:
1. Connect to an existing thread through the local FastAPI live-token API.
2. Enable web search through lk.control.
3. Ask an out-of-book/current-info question through lk.chat.
4. Wait for the assistant to ask web-search permission.
5. Publish tests/fixtures/yub-làm-đi.wav as microphone input.
6. Verify user voice transcript and assistant reply arrive, then check DB delta.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import wave
from pathlib import Path
from typing import Any

import aiohttp
from livekit import rtc

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
THREAD_ID = "07be00b9-c6da-4801-8ba2-7558205b92b2"
VOICE_WAV = Path("tests/fixtures/yub-làm-đi.wav")
PERMISSION_QUESTION = "Giá Bitcoin hôm nay là bao nhiêu? Nếu trong sách không có thì hãy xin phép trước khi tìm internet."


def _auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


async def get_live_token(base_url: str, thread_id: str, access_token: str) -> tuple[str, str]:
    async with aiohttp.ClientSession(headers=_auth_headers(access_token)) as http:
        async with http.get(f"{base_url}/live-token/thread/{thread_id}") as response:
            response.raise_for_status()
            payload = await response.json()
            return str(payload["token"]), str(payload["room_name"])


async def get_messages(base_url: str, thread_id: str, access_token: str) -> list[dict[str, Any]]:
    async with aiohttp.ClientSession(headers=_auth_headers(access_token)) as http:
        async with http.get(f"{base_url}/threads/{thread_id}/messages") as response:
            response.raise_for_status()
            payload = await response.json()
            if not isinstance(payload, list):
                raise RuntimeError(f"Unexpected messages response: {payload!r}")
            return payload


async def publish_wav_as_mic(room: rtc.Room, wav_path: Path) -> None:
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        total_frames = wav.getnframes()

        if sample_width != 2:
            raise RuntimeError(f"WAV must be 16-bit PCM, got sample width={sample_width}")

        print(
            f"VOICE_PERMISSION_FIXTURE: path={wav_path} sample_rate={sample_rate} "
            f"channels={channels} duration={total_frames / sample_rate:.2f}s"
        )

        source = rtc.AudioSource(sample_rate, channels)
        track = rtc.LocalAudioTrack.create_audio_track("phase7-1-permission-reply", source)
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        await room.local_participant.publish_track(track, options)

        chunk_frames = max(1, sample_rate // 50)
        while True:
            pcm = wav.readframes(chunk_frames)
            if not pcm:
                break
            samples_per_channel = len(pcm) // (sample_width * channels)
            frame = rtc.AudioFrame(pcm, sample_rate, channels, samples_per_channel)
            await source.capture_frame(frame)

    await source.wait_for_playout()
    await asyncio.sleep(1.0)


async def wait_queue(queue: asyncio.Queue[Any], label: str, timeout: float) -> Any:
    try:
        return await asyncio.wait_for(queue.get(), timeout=timeout)
    except asyncio.TimeoutError as exc:
        raise RuntimeError(f"Timeout waiting for {label}") from exc


async def wait_transcript_role(
    queue: asyncio.Queue[dict[str, Any]],
    role: str,
    *,
    timeout: float,
) -> dict[str, Any]:
    deadline = asyncio.get_running_loop().time() + timeout
    while True:
        remaining = deadline - asyncio.get_running_loop().time()
        if remaining <= 0:
            raise RuntimeError(f"Timeout waiting for transcript role={role}")
        payload = await wait_queue(queue, f"transcript role={role}", remaining)
        if payload.get("role") == role and payload.get("text"):
            return payload


def drain_queue(queue: asyncio.Queue[Any]) -> None:
    while True:
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            return


def attach_data_handlers(
    room: rtc.Room,
    *,
    greeting_event: asyncio.Event,
    chat_queue: asyncio.Queue[str],
    transcript_queue: asyncio.Queue[dict[str, Any]],
) -> None:
    @room.on("data_received")
    def on_data_received(packet: rtc.DataPacket) -> None:
        participant_identity = packet.participant.identity if packet.participant else ""
        if "agent" not in participant_identity.lower():
            return

        try:
            text = packet.data.decode("utf-8")
        except UnicodeDecodeError:
            return

        if packet.topic == "lk.chat":
            if not greeting_event.is_set():
                print(f"GREETING_LK_CHAT: {text[:180]}")
                greeting_event.set()
            else:
                print(f"ASSISTANT_LK_CHAT: {text[:700]}")
                chat_queue.put_nowait(text)
            return

        if packet.topic != "lk.transcript":
            return

        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return

        if isinstance(payload, dict) and payload.get("type") == "transcript":
            role = payload.get("role")
            body = str(payload.get("text", ""))
            print(f"TRANSCRIPT_{role}: {body[:300]}")
            transcript_queue.put_nowait(payload)


async def send_web_search_toggle(room: rtc.Room, enabled: bool) -> None:
    payload = json.dumps({"type": "toggle_web_search", "enabled": enabled}).encode("utf-8")
    await room.local_participant.publish_data(payload, reliable=True, topic="lk.control")
    print(f"WEB_SEARCH_TOGGLE_SENT: {enabled}")


async def run_test(args: argparse.Namespace) -> None:
    wav_path = Path(args.wav)
    if not wav_path.exists():
        raise FileNotFoundError(f"Missing voice fixture: {wav_path}")

    before_messages = await get_messages(args.base_url, args.thread_id, args.access_token)
    print(f"DB_BEFORE_MESSAGES: {len(before_messages)}")

    token, room_name = await get_live_token(args.base_url, args.thread_id, args.access_token)
    print(f"LIVEKIT_ROOM: {room_name}")

    room = rtc.Room()
    greeting_event = asyncio.Event()
    chat_queue: asyncio.Queue[str] = asyncio.Queue()
    transcript_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
    attach_data_handlers(
        room,
        greeting_event=greeting_event,
        chat_queue=chat_queue,
        transcript_queue=transcript_queue,
    )

    print("CONNECTING_LIVEKIT...")
    await room.connect(args.livekit_url, token)
    try:
        await asyncio.wait_for(greeting_event.wait(), timeout=args.greeting_timeout)
        await send_web_search_toggle(room, True)
        await asyncio.sleep(0.5)

        print(f"OUT_OF_BOOK_QUESTION: {args.question}")
        drain_queue(chat_queue)
        drain_queue(transcript_queue)
        await room.local_participant.publish_data(
            args.question.encode("utf-8"),
            reliable=True,
            topic="lk.chat",
        )
        permission_reply = await wait_queue(chat_queue, "permission request reply", args.reply_timeout)
        print(f"PERMISSION_REQUEST_REPLY_OK: chars={len(permission_reply)}")

        drain_queue(chat_queue)
        drain_queue(transcript_queue)
        print("VOICE_PERMISSION_REPLY: publishing yub-làm-đi.wav")
        await publish_wav_as_mic(room, wav_path)
        user_transcript = await wait_transcript_role(transcript_queue, "user", timeout=args.voice_timeout)
        final_reply = await wait_queue(chat_queue, "assistant reply after voice grant", args.reply_timeout)

        print(f"VOICE_PERMISSION_TRANSCRIPT_OK: {user_transcript['text'][:300]}")
        print(f"FINAL_REPLY_AFTER_PERMISSION_OK: chars={len(final_reply)}")
        lowered_reply = final_reply.casefold()
        if "bắt đầu nghe" in lowered_reply or "cuốn sách nào" in lowered_reply:
            raise RuntimeError(f"Assistant replied with a generic greeting instead of handling permission: {final_reply}")
    finally:
        await room.disconnect()

    await asyncio.sleep(args.db_settle_seconds)
    after_messages = await get_messages(args.base_url, args.thread_id, args.access_token)
    delta = len(after_messages) - len(before_messages)
    print(f"DB_AFTER_MESSAGES: {len(after_messages)}")
    print(f"DB_MESSAGE_DELTA: {delta}")

    if delta < 4:
        raise RuntimeError(f"Expected at least 4 new DB messages, got {delta}")

    print("RESULT: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 7.1 voice permission integration test.")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--livekit-url", default=LIVEKIT_URL)
    parser.add_argument("--thread-id", default=THREAD_ID)
    parser.add_argument("--wav", default=str(VOICE_WAV))
    parser.add_argument("--question", default=PERMISSION_QUESTION)
    parser.add_argument("--access-token", default=os.getenv("TRIAM_ACCESS_TOKEN"))
    parser.add_argument("--greeting-timeout", type=float, default=60.0)
    parser.add_argument("--reply-timeout", type=float, default=90.0)
    parser.add_argument("--voice-timeout", type=float, default=75.0)
    parser.add_argument("--db-settle-seconds", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        if not args.access_token:
            raise RuntimeError("Missing access token. Pass --access-token or set TRIAM_ACCESS_TOKEN.")
        asyncio.run(run_test(args))
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        print(f"RESULT: FAIL | {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
