"""Manual Phase 10.0 text and voice evaluation runner.

Requires a running FastAPI server, LiveKit voice worker, test access token, and
real provider access. It is intentionally outside pytest's default test path.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import uuid
import wave
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import aiohttp
from livekit import rtc

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings  # noqa: E402
from app.services.agent_observability.llm_as_a_judge import get_retrieved_context, judge_answer  # noqa: E402
from app.services.agent_observability.model_eval_report import (  # noqa: E402
    build_metrics,
    build_snapshot_metadata,
    classify_exception_failure_codes,
    classify_failure_codes,
    find_candidate,
    load_candidate_matrix,
    safe_model_config_from_settings,
    summarize_results,
    write_eval_reports,
)

DEFAULT_BASE_URL = "http://127.0.0.1:8000/api/v1"
DEFAULT_LIVEKIT_URL = "wss://tri-am-bmdl413w.livekit.cloud"
DEFAULT_BOOK_ID = "c3f13d07-4494-4995-ba75-30a12589b8fc"
DEFAULT_THREAD_ID = "07be00b9-c6da-4801-8ba2-7558205b92b2"
TEXT_CASES_PATH = Path("tests/fixtures/agent_eval/book_grounding_cases.json")
VOICE_CASES_PATH = Path("tests/fixtures/agent_eval/voice_manifest.json")
CANDIDATE_MATRIX_PATH = Path("tests/fixtures/agent_eval/model_candidate_matrix.json")
TRACE_PATTERN = re.compile(r"AGENT_TRACE (?P<event>[a-z_]+) \| (?P<payload>\{.*\})")


@dataclass
class EvalRoomSession:
    room: rtc.Room
    room_name: str
    thread_id: str
    chat_queue: asyncio.Queue[str]
    transcript_queue: asyncio.Queue[dict[str, Any]]


def access_token_passed_via_cli(argv: list[str]) -> bool:
    return any(arg == "--access-token" or arg.startswith("--access-token=") for arg in argv)


def load_cases(mode: str, selected_ids: set[str]) -> list[dict[str, Any]]:
    paths: list[Path] = []
    if mode in {"text", "all"}:
        paths.append(TEXT_CASES_PATH)
    if mode in {"voice", "all"}:
        paths.append(VOICE_CASES_PATH)

    cases: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases.extend(case for case in payload if not selected_ids or case["id"] in selected_ids)
    return cases


def voice_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [case for case in cases if case.get("input_mode") == "voice"]


def load_case_thread_map(path: str | None) -> dict[str, str]:
    if not path:
        return {}

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Case thread map must be a JSON object mapping case_id to thread_id.")

    mapping: dict[str, str] = {}
    for case_id, thread_id in payload.items():
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("Case thread map contains an invalid case id.")
        try:
            mapping[case_id] = str(uuid.UUID(str(thread_id)))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Case thread map has invalid thread_id for case {case_id!r}.") from exc
    return mapping


def validate_voice_isolation_args(args: argparse.Namespace, cases: list[dict[str, Any]], case_thread_map: dict[str, str]) -> None:
    selected_voice_cases = voice_cases(cases)
    if not selected_voice_cases:
        return
    if args.voice_isolation_strategy == "case_thread_new_room" and not args.isolate_voice_cases:
        raise ValueError("case_thread_new_room requires --isolate-voice-cases.")
    if args.voice_isolation_strategy != "case_thread_new_room":
        return

    missing = [case["id"] for case in selected_voice_cases if case["id"] not in case_thread_map]
    if missing:
        raise ValueError(f"Missing case thread ids for voice cases: {', '.join(missing)}")


def effective_thread_id_for_case(case: dict[str, Any], args: argparse.Namespace, case_thread_map: dict[str, str]) -> str:
    if case.get("input_mode") == "voice" and args.voice_isolation_strategy == "case_thread_new_room":
        return case_thread_map[case["id"]]
    return str(args.thread_id)


def eval_thread_ids(cases: list[dict[str, Any]], args: argparse.Namespace, case_thread_map: dict[str, str]) -> list[str]:
    thread_ids = {effective_thread_id_for_case(case, args, case_thread_map) for case in cases}
    return sorted(thread_ids)


def case_isolation_quality(case: dict[str, Any], args: argparse.Namespace) -> str:
    if case.get("input_mode") != "voice":
        return "not_applicable"
    if not args.isolate_voice_cases:
        return "none"
    if args.voice_isolation_strategy == "case_thread_new_room":
        return "thread_and_room"
    return "room_only"


def voice_isolation_report(cases: list[dict[str, Any]], args: argparse.Namespace, thread_ids: list[str]) -> dict[str, Any]:
    selected_voice_cases = voice_cases(cases)
    if not selected_voice_cases:
        quality = "not_applicable"
    elif args.isolate_voice_cases and args.voice_isolation_strategy == "case_thread_new_room":
        quality = "thread_and_room"
    elif args.isolate_voice_cases:
        quality = "room_only"
    else:
        quality = "none"

    return {
        "enabled": bool(args.isolate_voice_cases),
        "strategy": args.voice_isolation_strategy,
        "quality": quality,
        "thread_count": len(thread_ids),
        "voice_case_count": len(selected_voice_cases),
    }


def auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


async def get_json(http: aiohttp.ClientSession, url: str) -> Any:
    async with http.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def get_message_counts(http: aiohttp.ClientSession, base_url: str, thread_ids: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for thread_id in thread_ids:
        messages = await get_json(http, f"{base_url}/threads/{thread_id}/messages")
        counts[thread_id] = len(messages)
    return counts


async def get_live_token(http: aiohttp.ClientSession, base_url: str, thread_id: str) -> tuple[str, str]:
    payload = await get_json(http, f"{base_url}/live-token/thread/{thread_id}")
    return str(payload["token"]), str(payload["room_name"])


def flatten_outline(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for item in items:
        flattened.append(item)
        flattened.extend(flatten_outline(item.get("children") or []))
    return flattened


def trace_log_offset(path: Path | None) -> int:
    if path is None or not path.exists():
        return 0
    return path.stat().st_size


def _parse_trace_events(lines: list[str], *, input_mode: str) -> list[tuple[str, dict[str, Any]]]:
    events: list[tuple[str, dict[str, Any]]] = []
    for line in lines:
        match = TRACE_PATTERN.search(line)
        if not match:
            continue
        try:
            payload = json.loads(match.group("payload"))
        except json.JSONDecodeError:
            continue
        if payload.get("input_mode") == input_mode:
            events.append((match.group("event"), payload))
    return events


def _trace_matches_context(payload: dict[str, Any], *, thread_id: str | None, room_name: str | None) -> bool:
    if thread_id and payload.get("thread_id") not in (None, thread_id):
        return False
    if room_name and payload.get("room_name") not in (None, room_name):
        return False
    return True


def _select_completed_trace(events: list[tuple[str, dict[str, Any]]]) -> dict[str, Any] | None:
    completed = [payload for event, payload in events if event == "turn_completed"]
    if not completed:
        return None
    with_assistant = [payload for payload in completed if int(payload.get("assistant_char_count") or 0) > 0]
    selected = (with_assistant or completed)[-1].copy()
    selected["trace_selection_quality"] = "strong" if with_assistant else "weak_no_assistant_chars"
    return selected


def _merge_late_transcript(selected: dict[str, Any], events: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    trace_id = selected.get("trace_id")
    for event, payload in events:
        if event == "late_transcript" and payload.get("trace_id") == trace_id:
            selected.update(payload)
            selected["trace_selection_quality"] = "strong_late_transcript_merged"
    return selected


def read_trace_events(
    path: Path | None,
    offset: int,
    *,
    input_mode: str,
    thread_id: str | None = None,
    room_name: str | None = None,
) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        handle.seek(offset)
        lines = handle.readlines()

    events = [
        (event, payload)
        for event, payload in _parse_trace_events(lines, input_mode=input_mode)
        if _trace_matches_context(payload, thread_id=thread_id, room_name=room_name)
    ]
    selected = _select_completed_trace(events)
    return _merge_late_transcript(selected, events) if selected else None


async def wait_queue(queue: asyncio.Queue[Any], label: str, timeout: float) -> Any:
    try:
        return await asyncio.wait_for(queue.get(), timeout=timeout)
    except asyncio.TimeoutError as exc:
        raise RuntimeError(f"Timeout waiting for {label}") from exc


def drain_queue(queue: asyncio.Queue[Any]) -> None:
    while True:
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            return


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


def inspect_wav_fixture(wav_path: Path) -> dict[str, int | str]:
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        frame_count = wav.getnframes()
        if sample_width != 2:
            raise RuntimeError(f"WAV must be 16-bit PCM: {wav_path}")
        if sample_rate <= 0 or channels <= 0 or frame_count <= 0:
            raise RuntimeError(f"WAV has invalid audio metadata: {wav_path}")

    duration_ms = round(frame_count / sample_rate * 1000)
    return {
        "path": str(wav_path),
        "sample_rate": sample_rate,
        "channels": channels,
        "sample_width_bytes": sample_width,
        "duration_ms": duration_ms,
    }


async def publish_wav_as_mic(room: rtc.Room, wav_path: Path, case_id: str) -> dict[str, int | str]:
    metadata = inspect_wav_fixture(wav_path)
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = int(metadata["sample_rate"])
        channels = int(metadata["channels"])
        sample_width = int(metadata["sample_width_bytes"])

        source = rtc.AudioSource(sample_rate, channels)
        track = rtc.LocalAudioTrack.create_audio_track(f"phase10-{case_id}", source)
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        await room.local_participant.publish_track(track, options)

        chunk_frames = max(1, sample_rate // 50)
        while True:
            pcm = wav.readframes(chunk_frames)
            if not pcm:
                break
            samples_per_channel = len(pcm) // (sample_width * channels)
            await source.capture_frame(rtc.AudioFrame(pcm, sample_rate, channels, samples_per_channel))

    await source.wait_for_playout()
    await asyncio.sleep(1.0)
    return metadata


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
                greeting_event.set()
            else:
                chat_queue.put_nowait(text)
            return

        if packet.topic != "lk.transcript":
            return
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return
        if isinstance(payload, dict) and payload.get("type") == "transcript":
            transcript_queue.put_nowait(payload)


async def connect_eval_room(
    http: aiohttp.ClientSession,
    *,
    base_url: str,
    livekit_url: str,
    thread_id: str,
    timeout: float,
) -> EvalRoomSession:
    token, room_name = await get_live_token(http, base_url, thread_id)
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

    await room.connect(livekit_url, token)
    await asyncio.wait_for(greeting_event.wait(), timeout=timeout)
    try:
        await wait_transcript_role(transcript_queue, "assistant", timeout=min(timeout, 15.0))
    except RuntimeError:
        # Some deployments may publish greeting only through lk.chat.
        pass
    drain_queue(chat_queue)
    drain_queue(transcript_queue)
    return EvalRoomSession(
        room=room,
        room_name=room_name,
        thread_id=thread_id,
        chat_queue=chat_queue,
        transcript_queue=transcript_queue,
    )


async def disconnect_eval_room(session: EvalRoomSession | None, *, grace_seconds: float = 0.5) -> None:
    if session is None:
        return
    try:
        await session.room.disconnect()
    finally:
        if grace_seconds > 0:
            await asyncio.sleep(grace_seconds)


async def send_web_search_toggle(room: rtc.Room, enabled: bool) -> None:
    payload = json.dumps({"type": "toggle_web_search", "enabled": enabled}).encode("utf-8")
    await room.local_participant.publish_data(payload, reliable=True, topic="lk.control")
    await asyncio.sleep(0.2)


def contains(text: str, expected: str) -> bool:
    return expected.casefold() in text.casefold()


def local_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def load_declared_model_config(candidate_matrix: Path, candidate_name: str) -> tuple[dict[str, str], dict[str, Any] | None]:
    config = safe_model_config_from_settings(settings)
    if not candidate_matrix.exists():
        config["AGENT_MODEL_PROFILE"] = candidate_name
        return config, None

    candidates = load_candidate_matrix(candidate_matrix)
    candidate = find_candidate(candidates, candidate_name)
    config.update({key: str(value) for key, value in candidate.get("env", {}).items()})
    config["AGENT_MODEL_PROFILE"] = candidate_name
    return config, candidate


def _transcript_required_field_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("v", "type", "role", "text", "id", "ts"):
        if key not in payload:
            errors.append(f"missing_{key}")
    for key in ("message_id", "thread_id", "source", "status"):
        if key not in payload:
            errors.append(f"missing_{key}")
    return errors


def _transcript_value_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("type") != "transcript":
        errors.append("invalid_type")
    if payload.get("source") != "livekit":
        errors.append("invalid_source")
    if payload.get("status") != "committed":
        errors.append("invalid_status")

    transcript_id = str(payload.get("id") or "")
    try:
        uuid.UUID(transcript_id)
    except ValueError:
        errors.append("invalid_id_uuid")

    message_id = payload.get("message_id")
    if message_id:
        if str(message_id) != transcript_id:
            errors.append("message_id_id_mismatch")
        try:
            uuid.UUID(str(message_id))
        except ValueError:
            errors.append("invalid_message_id_uuid")

    return errors


def validate_transcript_contract(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {"valid": False, "errors": ["missing_payload"]}

    errors = _transcript_required_field_errors(payload)
    errors.extend(_transcript_value_errors(payload))
    message_id = payload.get("message_id")
    return {
        "valid": not errors,
        "errors": errors,
        "has_message_id": bool(message_id),
        "has_thread_id": bool(payload.get("thread_id")),
    }


def expected_intent_matches(case: dict[str, Any], trace: dict[str, Any]) -> bool:
    expected_intent = case.get("expected_intent")
    if trace.get("detected_intent") == expected_intent:
        return True
    return expected_intent == "clarification_required" and trace.get("answer_source") == "clarification"


def semantic_behavior_passed(checks: dict[str, bool | None]) -> bool:
    status_keys = (
        "must_include",
        "must_not_include",
        "trace_available",
        "expected_intent",
        "expected_answer_source",
        "expected_section",
        "web_not_used_without_permission",
    )
    selected = [checks.get(key) for key in status_keys if checks.get(key) is not None]
    return bool(selected) and all(selected)


def voice_stt_minor_warning(checks: dict[str, bool | None]) -> bool:
    return checks.get("voice_transcript_meaning") is False and semantic_behavior_passed(checks)


async def evaluate_case(
    case: dict[str, Any],
    *,
    response_text: str,
    user_transcript: str | None,
    trace: dict[str, Any] | None,
    section_id_by_path: dict[str, str],
    include_text_preview: bool,
    llm_judge: bool = False,
) -> dict[str, Any]:
    checks: dict[str, bool | float | None] = {}
    checks["must_include"] = all(contains(response_text, value) for value in case.get("must_include", []))
    checks["must_not_include"] = all(not contains(response_text, value) for value in case.get("must_not_include", []))

    transcript_terms = case.get("transcript_must_include_any") or []
    checks["voice_transcript_meaning"] = (
        any(contains(user_transcript or "", value) for value in transcript_terms)
        if transcript_terms
        else None
    )

    llm_judge_data = {}
    if trace is None:
        checks["trace_available"] = False
        checks["expected_intent"] = None
        checks["expected_answer_source"] = None
        checks["expected_section"] = None
        checks["web_not_used_without_permission"] = None
        checks["llm_verdict"] = None
    else:
        checks["trace_available"] = True
        checks["expected_intent"] = expected_intent_matches(case, trace)
        checks["expected_answer_source"] = trace.get("answer_source") == case.get("expected_answer_source")
        expected_section_ids = {
            section_id_by_path[path]
            for path in case.get("expected_section_paths", [])
            if path in section_id_by_path
        }
        actual_section_ids = set(trace.get("resolved_section_ids") or []) | set(trace.get("retrieval_section_ids") or [])
        checks["expected_section"] = bool(expected_section_ids & actual_section_ids) if expected_section_ids else None
        checks["web_not_used_without_permission"] = (
            trace.get("answer_source") != "web"
            if not case.get("web_search_allowed", False)
            else None
        )

        if llm_judge and case.get("expected_answer_source") == "book_rag" and trace.get("answer_source") == "book_rag":
            chunk_ids = trace.get("retrieval_chunk_ids") or []
            context = get_retrieved_context(chunk_ids)
            if context:
                try:
                    score = await judge_answer(case["question"], context, response_text)
                    checks["llm_verdict"] = score.verdict
                    llm_judge_data = {
                        "faithfulness_score": score.faithfulness,
                        "answer_relevance_score": score.answer_relevance,
                        "verdict": score.verdict,
                        "reasoning": score.reasoning,
                    }
                except Exception as e:
                    checks["llm_verdict"] = False
                    llm_judge_data = {"error": str(e)}
            else:
                checks["llm_verdict"] = False
                llm_judge_data = {"error": "No retrieved context found in database"}
        else:
            checks["llm_verdict"] = None

    evaluated_checks = [value for value in checks.values() if value is not None and not isinstance(value, float)]
    warnings: list[str] = []
    if voice_stt_minor_warning(checks):
        warnings.append("INPUT_STT_MINOR")

    status = "passed" if evaluated_checks and (all(evaluated_checks) or warnings) else "failed"
    result: dict[str, Any] = {
        "id": case["id"],
        "input_mode": case["input_mode"],
        "status": status,
        "checks": checks,
        "response_char_count": len(response_text),
        "user_transcript_char_count": len(user_transcript or ""),
        "trace": trace,
    }
    if llm_judge_data:
        result["llm_judge"] = llm_judge_data
    if warnings:
        result["warnings"] = warnings
    if include_text_preview:
        result["response_preview"] = response_text[:240]
        result["user_transcript_preview"] = (user_transcript or "")[:160]
    if status == "failed":
        result["failure_codes"] = classify_failure_codes(case, checks, trace)
    return result


async def run_case(
    room: rtc.Room,
    case: dict[str, Any],
    *,
    transcript_queue: asyncio.Queue[dict[str, Any]],
    chat_queue: asyncio.Queue[str],
    timeout: float,
) -> tuple[str, str | None, dict[str, Any] | None, dict[str, Any], dict[str, Any]]:
    drain_queue(transcript_queue)
    drain_queue(chat_queue)
    await send_web_search_toggle(room, bool(case.get("web_search_enabled", False)))

    if case["input_mode"] == "text":
        await room.local_participant.publish_data(
            case["question"].encode("utf-8"),
            reliable=True,
            topic="lk.chat",
        )
        assistant = await wait_transcript_role(transcript_queue, "assistant", timeout=timeout)
        return str(assistant["text"]), None, None, assistant, {}

    wav_path = Path(case["audio_fixture"])
    if not wav_path.exists():
        raise FileNotFoundError(f"Voice fixture not found: {wav_path}")
    audio_metadata = await publish_wav_as_mic(room, wav_path, case["id"])
    user = await wait_transcript_role(transcript_queue, "user", timeout=timeout)
    assistant = await wait_transcript_role(transcript_queue, "assistant", timeout=timeout)
    return str(assistant["text"]), str(user["text"]), user, assistant, {"audio": audio_metadata}


async def run(args: argparse.Namespace) -> None:
    selected_ids = set(args.case_id or [])
    cases = load_cases(args.mode, selected_ids)
    if args.max_cases:
        cases = cases[: args.max_cases]
    if not cases:
        raise RuntimeError("No evaluation cases selected.")

    case_thread_map = load_case_thread_map(args.case_thread_map)
    validate_voice_isolation_args(args, cases, case_thread_map)
    all_eval_thread_ids = eval_thread_ids(cases, args, case_thread_map)
    model_config, candidate = load_declared_model_config(Path(args.candidate_matrix), args.candidate_name)
    trace_log = Path(args.trace_log) if args.trace_log else None
    async with aiohttp.ClientSession(headers=auth_headers(args.access_token)) as http:
        book = await get_json(http, f"{args.base_url}/books/{args.book_id}")
        outline_payload = await get_json(http, f"{args.base_url}/books/{args.book_id}/outline")
        before_message_counts = await get_message_counts(http, args.base_url, all_eval_thread_ids)

        outline = flatten_outline(outline_payload.get("outline_tree") or [])
        section_id_by_path = {str(item["path"]): str(item["id"]) for item in outline}
        session: EvalRoomSession | None = None
        results: list[dict[str, Any]] = []
        try:
            for index, case in enumerate(cases, start=1):
                print(f"CASE {index}/{len(cases)}: {case['id']} ({case['input_mode']})")
                effective_thread_id = effective_thread_id_for_case(case, args, case_thread_map)
                should_reconnect = (
                    session is None
                    or session.thread_id != effective_thread_id
                    or (case["input_mode"] == "voice" and args.isolate_voice_cases)
                )
                if should_reconnect:
                    await disconnect_eval_room(session, grace_seconds=args.disconnect_grace_seconds)
                    session = await connect_eval_room(
                        http,
                        base_url=args.base_url,
                        livekit_url=args.livekit_url,
                        thread_id=effective_thread_id,
                        timeout=args.timeout,
                    )

                isolation_metadata = {
                    "eval_thread_id": effective_thread_id,
                    "eval_room_name": session.room_name,
                    "isolation_strategy": args.voice_isolation_strategy,
                    "case_isolation_quality": case_isolation_quality(case, args),
                }
                offset = trace_log_offset(trace_log)
                try:
                    response_text, user_transcript, user_payload, assistant_payload, case_metadata = await run_case(
                        session.room,
                        case,
                        transcript_queue=session.transcript_queue,
                        chat_queue=session.chat_queue,
                        timeout=args.timeout,
                    )
                    await asyncio.sleep(args.trace_settle_seconds)
                    trace = read_trace_events(
                        trace_log,
                        offset,
                        input_mode=case["input_mode"],
                        thread_id=effective_thread_id,
                        room_name=session.room_name,
                    )
                    result = await evaluate_case(
                        case,
                        response_text=response_text,
                        user_transcript=user_transcript,
                        trace=trace,
                        section_id_by_path=section_id_by_path,
                        include_text_preview=args.include_text_preview,
                        llm_judge=args.llm_judge,
                    )
                    result.update(isolation_metadata)
                    result.update(case_metadata)
                    transcript_contract = {
                        "user": validate_transcript_contract(user_payload) if user_payload else None,
                        "assistant": validate_transcript_contract(assistant_payload),
                    }
                    result["transcript_contract"] = transcript_contract
                    contract_values = [value for value in transcript_contract.values() if value is not None]
                    if any(not value["valid"] for value in contract_values):
                        result["status"] = "failed"
                        result.setdefault("failure_codes", [])
                        if "TRANSCRIPT_CONTRACT" not in result["failure_codes"]:
                            result["failure_codes"].append("TRANSCRIPT_CONTRACT")
                except Exception as exc:
                    result = {
                        "id": case["id"],
                        "input_mode": case["input_mode"],
                        "status": "failed",
                        **isolation_metadata,
                        "failure_codes": classify_exception_failure_codes(
                            input_mode=str(case.get("input_mode") or ""),
                            error_type=type(exc).__name__,
                            error_message=str(exc),
                        ),
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                results.append(result)
                print(f"RESULT: {result['status']}")
        finally:
            await disconnect_eval_room(session, grace_seconds=args.disconnect_grace_seconds)

        await asyncio.sleep(args.db_settle_seconds)
        after_message_counts = await get_message_counts(http, args.base_url, all_eval_thread_ids)

    snapshot = build_snapshot_metadata(
        book=book,
        outline=outline,
        app_git_sha=args.app_git_sha or local_git_sha(),
        database_label=args.database_label,
        embedding_model=settings.BOOK_SECTION_EMBEDDING_MODEL,
        embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
        book_section_knowledge_count=args.book_section_knowledge_count,
    )
    snapshot["thread_id"] = args.thread_id
    snapshot["eval_thread_ids"] = all_eval_thread_ids
    db_message_delta = sum(after_message_counts[thread_id] - before_message_counts[thread_id] for thread_id in all_eval_thread_ids)
    report = {
        "candidate": args.candidate_name,
        "candidate_description": candidate.get("description") if candidate else None,
        "environment": args.base_url,
        "generated_at": datetime.now().astimezone().isoformat(),
        "model_config": model_config,
        "runtime_config_applied_by_runner": False,
        "runtime_config_note": "External server/worker mode: set candidate env before starting server and LiveKit worker.",
        "snapshot": snapshot,
        "voice_isolation": voice_isolation_report(cases, args, all_eval_thread_ids),
        "ground_truth": {
            "book_id": str(book.get("id")),
            "title": str(book.get("title")),
            "author": book.get("author"),
            "document_type": book.get("document_type"),
            "total_sections": book.get("total_sections"),
            "section_paths": list(section_id_by_path),
        },
        "summary": summarize_results(results),
        "metrics": build_metrics(results),
        "db_message_delta": db_message_delta,
        "results": results,
    }
    json_path, md_path = write_eval_reports(Path(args.output_dir), report, prefix=args.report_prefix)
    print(f"JSON_REPORT: {json_path}")
    print(f"MARKDOWN_REPORT: {md_path}")


def parse_args() -> argparse.Namespace:
    today = datetime.now().strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="Run Phase 10.0 grounded-agent evaluation.")
    parser.add_argument("--mode", choices=("text", "voice", "all"), default="all")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--livekit-url", default=DEFAULT_LIVEKIT_URL)
    parser.add_argument("--book-id", default=os.getenv("AGENT_EVAL_BOOK_ID", DEFAULT_BOOK_ID))
    parser.add_argument("--thread-id", default=os.getenv("AGENT_EVAL_THREAD_ID", DEFAULT_THREAD_ID))
    parser.add_argument("--access-token", default=os.getenv("TRIAM_ACCESS_TOKEN"))
    parser.add_argument("--case-id", action="append")
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--candidate-name", default=os.getenv("AGENT_MODEL_PROFILE", "baseline"))
    parser.add_argument("--candidate-matrix", default=str(CANDIDATE_MATRIX_PATH))
    parser.add_argument("--database-label", default=os.getenv("TRIAM_EVAL_DATABASE_LABEL", "unknown"))
    parser.add_argument("--app-git-sha", default=os.getenv("TRIAM_EVAL_APP_GIT_SHA"))
    parser.add_argument("--book-section-knowledge-count", type=int)
    parser.add_argument("--timeout", type=float, default=100.0)
    parser.add_argument("--trace-settle-seconds", type=float, default=1.0)
    parser.add_argument("--db-settle-seconds", type=float, default=2.0)
    parser.add_argument("--disconnect-grace-seconds", type=float, default=0.5)
    parser.add_argument("--trace-log", default=f"logs/app_{today}.log")
    parser.add_argument("--output-dir", default="_docs_implemented/eval_reports/phase10_9")
    parser.add_argument("--report-prefix", default="phase10_9_eval")
    parser.add_argument("--include-text-preview", action="store_true")
    parser.add_argument("--isolate-voice-cases", action="store_true")
    parser.add_argument(
        "--voice-isolation-strategy",
        choices=("shared_thread_new_room", "case_thread_new_room"),
        default="shared_thread_new_room",
    )
    parser.add_argument("--case-thread-map", default=os.getenv("AGENT_EVAL_CASE_THREAD_MAP"))
    parser.add_argument("--llm-judge", action="store_true", help="Enable LLM-as-a-Judge semantic evaluation.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if access_token_passed_via_cli(sys.argv[1:]):
        print("WARNING: --access-token can leak into shell history/logs. Prefer TRIAM_ACCESS_TOKEN.")
    if not args.access_token:
        print("RESULT: FAIL | Missing TRIAM_ACCESS_TOKEN or --access-token.")
        raise SystemExit(1)
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        print(f"RESULT: FAIL | {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
