from types import SimpleNamespace

from app.services.voice_agent.realtime_diagnostics import (
    extract_realtime_error_details,
    parse_rate_limit_snapshot,
    parse_response_id,
    parse_session_transcription_snapshot,
    parse_session_truncation_snapshot,
    response_usage_from_metrics,
)


def test_parses_openai_rate_limit_event_without_retaining_raw_event():
    snapshot = parse_rate_limit_snapshot(
        {
            "type": "rate_limits.updated",
            "event_id": "event-1",
            "rate_limits": [
                {"name": "tokens", "limit": 40000, "remaining": 1234, "reset_seconds": 9.5},
                {"name": "requests", "limit": 200, "remaining": 198, "reset_seconds": 9.5},
            ],
            "private_prompt": "must never be returned",
        }
    )

    assert snapshot is not None
    assert snapshot.event_id == "event-1"
    assert snapshot.token_remaining == 1234
    assert snapshot.request_remaining == 198
    assert "private_prompt" not in repr(snapshot)


def test_parses_response_id_metrics_and_wrapped_openai_error():
    assert parse_response_id({"type": "response.created", "response": {"id": "resp-1"}}) == "resp-1"
    metrics = SimpleNamespace(
        request_id="resp-1",
        input_tokens=12000,
        output_tokens=300,
        total_tokens=12300,
        duration=1.25,
        ttft=0.2,
        cancelled=False,
        input_token_details=SimpleNamespace(text_tokens=9000, audio_tokens=100, cached_tokens=7000),
        output_token_details=SimpleNamespace(text_tokens=20, audio_tokens=280),
    )

    usage = response_usage_from_metrics(metrics)
    details = extract_realtime_error_details(
        SimpleNamespace(
            type="realtime_model_error",
            error=SimpleNamespace(
                body=SimpleNamespace(code="rate_limit_exceeded", type="tokens"),
            ),
        )
    )

    assert usage is not None
    assert usage.input_cached_tokens == 7000
    assert usage.output_audio_tokens == 280
    assert usage.ttft_ms == 200
    assert details.code == "rate_limit_exceeded"
    assert details.error_type == "tokens"


def test_parses_acknowledged_session_truncation_without_retaining_session_content():
    snapshot = parse_session_truncation_snapshot(
        {
            "type": "session.updated",
            "event_id": "event-session-1",
            "session": {
                "instructions": "must never be retained",
                "truncation": {
                    "type": "retention_ratio",
                    "retention_ratio": 0.75,
                    "token_limits": {"post_instructions": 8000},
                },
                "audio": {
                    "input": {
                        "turn_detection": {
                            "type": "semantic_vad",
                            "create_response": False,
                            "interrupt_response": False,
                        }
                    }
                },
            },
        }
    )

    assert snapshot is not None
    assert snapshot.event_id == "event-session-1"
    assert snapshot.configured is True
    assert snapshot.truncation_type == "retention_ratio"
    assert snapshot.max_post_instructions_tokens == 8000
    assert snapshot.retention_ratio == 0.75
    assert snapshot.turn_detection_type == "semantic_vad"
    assert snapshot.turn_detection_create_response is False
    assert snapshot.turn_detection_interrupt_response is False
    assert "must never be retained" not in repr(snapshot)


def test_parses_session_update_without_a_truncation_policy():
    snapshot = parse_session_truncation_snapshot(
        {
            "type": "session.updated",
            "event_id": "event-session-2",
            "session": {"instructions": "must never be retained"},
        }
    )

    assert snapshot is not None
    assert snapshot.configured is False
    assert snapshot.truncation_type is None
    assert snapshot.max_post_instructions_tokens is None
    assert snapshot.retention_ratio is None
    assert snapshot.turn_detection_type is None


def test_parses_acknowledged_transcription_scalars_without_retaining_text_fields():
    snapshot = parse_session_transcription_snapshot(
        {
            "type": "session.updated",
            "event_id": "event-session-stt-1",
            "session": {
                "audio": {
                    "input": {
                        "transcription": {
                            "model": "gpt-live-transcribe",
                            "languages": ["vi", "en"],
                            "keywords": ["private title", "AC-42"],
                            "delay": "medium",
                            "prompt": "private transcription prompt",
                        }
                    }
                }
            },
        }
    )

    assert snapshot is not None
    assert snapshot.event_id == "event-session-stt-1"
    assert snapshot.configured is True
    assert snapshot.model == "gpt-live-transcribe"
    assert snapshot.language_mode == "languages"
    assert snapshot.language_count == 2
    assert snapshot.keyword_count == 2
    assert snapshot.delay == "medium"
    assert snapshot.prompt_chars == len("private transcription prompt")
    assert "private title" not in repr(snapshot)
    assert "private transcription prompt" not in repr(snapshot)


def test_parses_legacy_singular_transcription_language_and_missing_transcription():
    singular = parse_session_transcription_snapshot(
        {
            "type": "session.updated",
            "session": {"input_audio_transcription": {"model": "legacy", "language": "vi"}},
        }
    )
    missing = parse_session_transcription_snapshot(
        {"type": "session.updated", "session": {"instructions": "must never be retained"}}
    )

    assert singular is not None
    assert singular.language_mode == "language"
    assert singular.language_count == 1
    assert singular.keyword_count is None
    assert missing is not None
    assert missing.configured is False
    assert missing.language_mode == "none"
    assert "must never be retained" not in repr(missing)
