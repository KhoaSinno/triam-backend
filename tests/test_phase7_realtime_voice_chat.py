"""
Manual integration test for the Phase 7 realtime agent.

This script is intentionally not a pytest test because it needs:
- a running FastAPI server;
- a running LiveKit realtime worker;
- a real Supabase access token;
- a real LiveKit Cloud room.

Example:
    uv run python tests/test_phase7_realtime_voice_chat.py --access-token "<jwt>"
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
VOICE_WAV = Path("tests/fixtures/Có-những-phương-pháp.wav")
TEXT_QUESTION = "Sách này nói gì về LLM GPT và Gemini? Trả lời thật ngắn."


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


def drain_queue(queue: asyncio.Queue[Any]) -> None:
    while True:
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            return


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


async def publish_wav_as_mic(room: rtc.Room, wav_path: Path) -> None:
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        total_frames = wav.getnframes()

        if sample_width != 2:
            raise RuntimeError(f"WAV must be 16-bit PCM, got sample width={sample_width}")

        print(
            f"VOICE_FIXTURE: path={wav_path} sample_rate={sample_rate} "
            f"channels={channels} duration={total_frames / sample_rate:.2f}s"
        )

        source = rtc.AudioSource(sample_rate, channels)
        track = rtc.LocalAudioTrack.create_audio_track("phase7-voice-question", source)
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
                print(f"ASSISTANT_LK_CHAT: {text[:500]}")
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


async def run_text_phase(
    room: rtc.Room,
    *,
    text_question: str,
    chat_queue: asyncio.Queue[str],
    transcript_queue: asyncio.Queue[dict[str, Any]],
    reply_timeout: float,
) -> None:
    print(f"TEXT_QUESTION: {text_question}")
    drain_queue(chat_queue)
    drain_queue(transcript_queue)
    await room.local_participant.publish_data(
        text_question.encode("utf-8"),
        reliable=True,
        topic="lk.chat",
    )
    text_reply = await wait_queue(chat_queue, "text chat reply", reply_timeout)
    print(f"TEXT_REPLY_OK: chars={len(text_reply)}")


async def run_voice_phase(
    room: rtc.Room,
    *,
    wav_path: Path,
    chat_queue: asyncio.Queue[str],
    transcript_queue: asyncio.Queue[dict[str, Any]],
    voice_timeout: float,
    reply_timeout: float,
) -> None:
    print("VOICE_QUESTION: publishing wav as microphone input")
    drain_queue(chat_queue)
    drain_queue(transcript_queue)
    await publish_wav_as_mic(room, wav_path)
    voice_user_transcript = await wait_transcript_role(
        transcript_queue,
        "user",
        timeout=voice_timeout,
    )
    voice_reply = await wait_queue(chat_queue, "voice assistant reply", reply_timeout)
    voice_assistant_transcript = await wait_transcript_role(
        transcript_queue,
        "assistant",
        timeout=reply_timeout,
    )
    print(f"VOICE_USER_TRANSCRIPT_OK: {voice_user_transcript['text'][:300]}")
    print(f"VOICE_REPLY_OK: chars={len(voice_reply)}")
    print(f"VOICE_ASSISTANT_TRANSCRIPT_OK: {voice_assistant_transcript['text'][:300]}")


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

        await run_text_phase(
            room,
            text_question=args.text_question,
            chat_queue=chat_queue,
            transcript_queue=transcript_queue,
            reply_timeout=args.reply_timeout,
        )
        await run_voice_phase(
            room,
            wav_path=wav_path,
            chat_queue=chat_queue,
            transcript_queue=transcript_queue,
            voice_timeout=args.voice_timeout,
            reply_timeout=args.reply_timeout,
        )
    finally:
        await room.disconnect()

    await asyncio.sleep(args.db_settle_seconds)
    after_messages = await get_messages(args.base_url, args.thread_id, args.access_token)
    delta = len(after_messages) - len(before_messages)
    print(f"DB_AFTER_MESSAGES: {len(after_messages)}")
    print(f"DB_MESSAGE_DELTA: {delta}")

    min_expected_delta = 4
    if delta < min_expected_delta:
        raise RuntimeError(f"Expected at least {min_expected_delta} new DB messages, got {delta}")

    print("RESULT: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a real LiveKit text+voice integration test.")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--livekit-url", default=LIVEKIT_URL)
    parser.add_argument("--thread-id", default=THREAD_ID)
    parser.add_argument("--wav", default=str(VOICE_WAV))
    parser.add_argument("--text-question", default=TEXT_QUESTION)
    parser.add_argument("--access-token", default=os.getenv("TRIAM_ACCESS_TOKEN"))
    parser.add_argument("--greeting-timeout", type=float, default=60.0)
    parser.add_argument("--reply-timeout", type=float, default=75.0)
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
