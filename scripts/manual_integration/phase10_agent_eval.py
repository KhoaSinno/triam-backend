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
from datetime import datetime
from pathlib import Path
from typing import Any

import aiohttp
from livekit import rtc

from app.core.config import settings
from app.services.agent_observability.model_eval_report import (
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
DEFAULT_BOOK_ID = "dae3b3ae-8740-4485-9c16-12e685c6c970"
DEFAULT_THREAD_ID = "f4726e2c-8407-49de-804f-b45ca8b0c1c2"
TEXT_CASES_PATH = Path("tests/fixtures/agent_eval/book_grounding_cases.json")
VOICE_CASES_PATH = Path("tests/fixtures/agent_eval/voice_manifest.json")
CANDIDATE_MATRIX_PATH = Path("tests/fixtures/agent_eval/model_candidate_matrix.json")
TRACE_PATTERN = re.compile(r"AGENT_TRACE (?P<event>[a-z_]+) \| (?P<payload>\{.*\})")


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


def auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


async def get_json(http: aiohttp.ClientSession, url: str) -> Any:
    async with http.get(url) as response:
        response.raise_for_status()
        return await response.json()


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


def evaluate_case(
    case: dict[str, Any],
    *,
    response_text: str,
    user_transcript: str | None,
    trace: dict[str, Any] | None,
    section_id_by_path: dict[str, str],
    include_text_preview: bool,
) -> dict[str, Any]:
    checks: dict[str, bool | None] = {}
    checks["must_include"] = all(contains(response_text, value) for value in case.get("must_include", []))
    checks["must_not_include"] = all(not contains(response_text, value) for value in case.get("must_not_include", []))

    transcript_terms = case.get("transcript_must_include_any") or []
    checks["voice_transcript_meaning"] = (
        any(contains(user_transcript or "", value) for value in transcript_terms)
        if transcript_terms
        else None
    )

    if trace is None:
        checks["trace_available"] = False
        checks["expected_intent"] = None
        checks["expected_answer_source"] = None
        checks["expected_section"] = None
        checks["web_not_used_without_permission"] = None
    else:
        checks["trace_available"] = True
        checks["expected_intent"] = trace.get("detected_intent") == case.get("expected_intent")
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

    evaluated_checks = [value for value in checks.values() if value is not None]
    status = "passed" if evaluated_checks and all(evaluated_checks) else "failed"
    result: dict[str, Any] = {
        "id": case["id"],
        "input_mode": case["input_mode"],
        "status": status,
        "checks": checks,
        "response_char_count": len(response_text),
        "user_transcript_char_count": len(user_transcript or ""),
        "trace": trace,
    }
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

    model_config, candidate = load_declared_model_config(Path(args.candidate_matrix), args.candidate_name)
    trace_log = Path(args.trace_log) if args.trace_log else None
    async with aiohttp.ClientSession(headers=auth_headers(args.access_token)) as http:
        book = await get_json(http, f"{args.base_url}/books/{args.book_id}")
        outline_payload = await get_json(http, f"{args.base_url}/books/{args.book_id}/outline")
        before_messages = await get_json(http, f"{args.base_url}/threads/{args.thread_id}/messages")
        token, room_name = await get_live_token(http, args.base_url, args.thread_id)

        outline = flatten_outline(outline_payload.get("outline_tree") or [])
        section_id_by_path = {str(item["path"]): str(item["id"]) for item in outline}
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

        await room.connect(args.livekit_url, token)
        results: list[dict[str, Any]] = []
        try:
            await asyncio.wait_for(greeting_event.wait(), timeout=args.timeout)
            try:
                await wait_transcript_role(transcript_queue, "assistant", timeout=min(args.timeout, 15.0))
            except RuntimeError:
                # Some deployments may publish greeting only through lk.chat.
                pass
            drain_queue(chat_queue)
            drain_queue(transcript_queue)

            for index, case in enumerate(cases, start=1):
                print(f"CASE {index}/{len(cases)}: {case['id']} ({case['input_mode']})")
                offset = trace_log_offset(trace_log)
                try:
                    response_text, user_transcript, user_payload, assistant_payload, case_metadata = await run_case(
                        room,
                        case,
                        transcript_queue=transcript_queue,
                        chat_queue=chat_queue,
                        timeout=args.timeout,
                    )
                    await asyncio.sleep(args.trace_settle_seconds)
                    trace = read_trace_events(
                        trace_log,
                        offset,
                        input_mode=case["input_mode"],
                        thread_id=args.thread_id,
                        room_name=room_name,
                    )
                    result = evaluate_case(
                        case,
                        response_text=response_text,
                        user_transcript=user_transcript,
                        trace=trace,
                        section_id_by_path=section_id_by_path,
                        include_text_preview=args.include_text_preview,
                    )
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
            await room.disconnect()

        await asyncio.sleep(args.db_settle_seconds)
        after_messages = await get_json(http, f"{args.base_url}/threads/{args.thread_id}/messages")

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
    report = {
        "candidate": args.candidate_name,
        "candidate_description": candidate.get("description") if candidate else None,
        "environment": args.base_url,
        "generated_at": datetime.now().astimezone().isoformat(),
        "model_config": model_config,
        "runtime_config_applied_by_runner": False,
        "runtime_config_note": "External server/worker mode: set candidate env before starting server and LiveKit worker.",
        "snapshot": snapshot,
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
        "db_message_delta": len(after_messages) - len(before_messages),
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
    parser.add_argument("--trace-log", default=f"logs/app_{today}.log")
    parser.add_argument("--output-dir", default="_docs_implemented/eval_reports/phase10_8")
    parser.add_argument("--report-prefix", default="phase10_8_eval")
    parser.add_argument("--include-text-preview", action="store_true")
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
