import json
import wave
from argparse import Namespace

import pytest

from scripts.manual_integration.phase10_agent_eval import (
    access_token_passed_via_cli,
    case_isolation_quality,
    eval_thread_ids,
    evaluate_case,
    inspect_wav_fixture,
    load_case_thread_map,
    read_trace_events,
    validate_voice_isolation_args,
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


def test_load_case_thread_map_validates_uuid_values(tmp_path):
    map_path = tmp_path / "case_threads.json"
    map_path.write_text(json.dumps({"voice-case": "11111111-1111-1111-1111-111111111111"}), encoding="utf-8")

    mapping = load_case_thread_map(str(map_path))

    assert mapping == {"voice-case": "11111111-1111-1111-1111-111111111111"}


def test_load_case_thread_map_rejects_invalid_uuid(tmp_path):
    map_path = tmp_path / "case_threads.json"
    map_path.write_text(json.dumps({"voice-case": "not-a-uuid"}), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid thread_id"):
        load_case_thread_map(str(map_path))


def test_case_thread_strategy_requires_isolated_voice_cases():
    args = Namespace(
        isolate_voice_cases=False,
        voice_isolation_strategy="case_thread_new_room",
        thread_id="00000000-0000-0000-0000-000000000000",
    )
    cases = [{"id": "voice-case", "input_mode": "voice"}]

    with pytest.raises(ValueError, match="requires --isolate-voice-cases"):
        validate_voice_isolation_args(args, cases, {"voice-case": "11111111-1111-1111-1111-111111111111"})


def test_case_thread_strategy_requires_map_entry_for_each_voice_case():
    args = Namespace(
        isolate_voice_cases=True,
        voice_isolation_strategy="case_thread_new_room",
        thread_id="00000000-0000-0000-0000-000000000000",
    )
    cases = [{"id": "voice-case", "input_mode": "voice"}]

    with pytest.raises(ValueError, match="Missing case thread ids"):
        validate_voice_isolation_args(args, cases, {})


def test_eval_thread_ids_include_case_thread_map_values():
    args = Namespace(
        voice_isolation_strategy="case_thread_new_room",
        thread_id="00000000-0000-0000-0000-000000000000",
    )
    cases = [
        {"id": "text-case", "input_mode": "text"},
        {"id": "voice-case", "input_mode": "voice"},
    ]

    thread_ids = eval_thread_ids(cases, args, {"voice-case": "11111111-1111-1111-1111-111111111111"})

    assert thread_ids == [
        "00000000-0000-0000-0000-000000000000",
        "11111111-1111-1111-1111-111111111111",
    ]


def test_case_isolation_quality_reports_room_only_for_shared_thread_reconnect():
    args = Namespace(isolate_voice_cases=True, voice_isolation_strategy="shared_thread_new_room")

    assert case_isolation_quality({"input_mode": "voice"}, args) == "room_only"
    assert case_isolation_quality({"input_mode": "text"}, args) == "not_applicable"


async def test_evaluate_case_accepts_clarification_source_as_clarification_intent():
    result = await evaluate_case(
        {
            "id": "ambiguous",
            "input_mode": "voice",
            "expected_intent": "clarification_required",
            "expected_answer_source": "clarification",
            "expected_section_paths": [],
            "must_include": [],
            "must_not_include": [],
            "web_search_allowed": False,
        },
        response_text="Bạn muốn tóm tắt chương nào?",
        user_transcript="Tóm tắt chương",
        trace={
            "detected_intent": None,
            "answer_source": "clarification",
            "resolved_section_ids": [],
            "retrieval_section_ids": [],
        },
        section_id_by_path={},
        include_text_preview=False,
    )

    assert result["status"] == "passed"
    assert result["checks"]["expected_intent"] is True
    assert result["checks"]["expected_answer_source"] is True


async def test_evaluate_case_marks_minor_stt_warning_without_failing_semantic_success():
    result = await evaluate_case(
        {
            "id": "author",
            "input_mode": "voice",
            "expected_intent": "book_metadata.author",
            "expected_answer_source": "book_metadata",
            "expected_section_paths": [],
            "transcript_must_include_any": ["tác giả"],
            "must_include": ["John Steinbeck"],
            "must_not_include": [],
            "web_search_allowed": False,
        },
        response_text="Tác giả là John Steinbeck.",
        user_transcript="Giả của quyển sách là ai?",
        trace={
            "detected_intent": "book_metadata.author",
            "answer_source": "book_metadata",
            "resolved_section_ids": [],
            "retrieval_section_ids": [],
        },
        section_id_by_path={},
        include_text_preview=False,
    )

    assert result["status"] == "passed"
    assert result["checks"]["voice_transcript_meaning"] is False
    assert result["warnings"] == ["INPUT_STT_MINOR"]
