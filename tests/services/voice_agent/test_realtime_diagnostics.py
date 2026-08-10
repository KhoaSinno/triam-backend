from types import SimpleNamespace

from app.services.voice_agent.realtime_diagnostics import (
    extract_realtime_error_details,
    parse_rate_limit_snapshot,
    parse_response_id,
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
        SimpleNamespace(body=SimpleNamespace(code="rate_limit_exceeded", type="tokens"))
    )

    assert usage is not None
    assert usage.input_cached_tokens == 7000
    assert usage.output_audio_tokens == 280
    assert usage.ttft_ms == 200
    assert details.code == "rate_limit_exceeded"
    assert details.error_type == "tokens"
