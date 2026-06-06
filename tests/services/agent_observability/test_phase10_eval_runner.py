import json
import wave

from scripts.manual_integration.phase10_agent_eval import (
    access_token_passed_via_cli,
    inspect_wav_fixture,
    read_trace_events,
)


def _trace_line(event: str, payload: dict) -> str:
    return f"2026-06-06 AGENT_TRACE {event} | {json.dumps(payload, sort_keys=True)}\n"


def test_read_trace_events_filters_by_thread_room_and_prefers_assistant_trace(tmp_path):
    log_path = tmp_path / "trace.log"
    weak = {
        "trace_id": "weak",
        "thread_id": "thread-1",
        "room_name": "room-1",
        "input_mode": "voice",
        "assistant_char_count": 0,
    }
    strong = {
        "trace_id": "strong",
        "thread_id": "thread-1",
        "room_name": "room-1",
        "input_mode": "voice",
        "assistant_char_count": 42,
    }
    other_room = {
        "trace_id": "other",
        "thread_id": "thread-1",
        "room_name": "room-2",
        "input_mode": "voice",
        "assistant_char_count": 99,
    }
    log_path.write_text(
        "".join(
            [
                _trace_line("turn_completed", weak),
                _trace_line("turn_completed", other_room),
                _trace_line("turn_completed", strong),
            ]
        ),
        encoding="utf-8",
    )

    selected = read_trace_events(
        log_path,
        0,
        input_mode="voice",
        thread_id="thread-1",
        room_name="room-1",
    )

    assert selected is not None
    assert selected["trace_id"] == "strong"
    assert selected["trace_selection_quality"] == "strong"


def test_read_trace_events_merges_late_transcript(tmp_path):
    log_path = tmp_path / "trace.log"
    completed = {
        "trace_id": "trace-1",
        "thread_id": "thread-1",
        "room_name": "room-1",
        "input_mode": "voice",
        "assistant_char_count": 42,
        "transcript_final_seen": False,
    }
    late = {
        **completed,
        "transcript_final_seen": True,
        "correlation_quality": "late_transcript_last_completed_turn",
    }
    log_path.write_text(
        _trace_line("turn_completed", completed) + _trace_line("late_transcript", late),
        encoding="utf-8",
    )

    selected = read_trace_events(log_path, 0, input_mode="voice", thread_id="thread-1", room_name="room-1")

    assert selected is not None
    assert selected["transcript_final_seen"] is True
    assert selected["trace_selection_quality"] == "strong_late_transcript_merged"


def test_access_token_passed_via_cli_detects_sensitive_argument():
    assert access_token_passed_via_cli(["--access-token", "secret"]) is True
    assert access_token_passed_via_cli(["--access-token=secret"]) is True
    assert access_token_passed_via_cli(["--mode", "text"]) is False


def test_inspect_wav_fixture_returns_safe_metadata(tmp_path):
    wav_path = tmp_path / "sample.wav"
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 1600)

    metadata = inspect_wav_fixture(wav_path)

    assert metadata["path"] == str(wav_path)
    assert metadata["sample_rate"] == 16000
    assert metadata["channels"] == 1
    assert metadata["sample_width_bytes"] == 2
    assert metadata["duration_ms"] == 100
