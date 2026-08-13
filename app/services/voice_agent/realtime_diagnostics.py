"""Safe, structured diagnostics for OpenAI Realtime events.

The LiveKit OpenAI plugin exposes provider events as raw dictionaries.  This
module extracts only operational metadata; it must never retain audio,
transcripts, prompts, or tool payloads.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RealtimeRateLimitSnapshot:
    event_id: str | None
    token_limit: int | None
    token_remaining: int | None
    token_reset_seconds: float | None
    request_limit: int | None
    request_remaining: int | None
    request_reset_seconds: float | None


@dataclass(frozen=True)
class RealtimeResponseUsage:
    response_id: str
    input_tokens: int
    input_text_tokens: int
    input_audio_tokens: int
    input_cached_tokens: int
    output_tokens: int
    output_text_tokens: int
    output_audio_tokens: int
    total_tokens: int
    duration_ms: int
    ttft_ms: int | None
    cancelled: bool


@dataclass(frozen=True)
class RealtimeSessionTruncationSnapshot:
    """Safe scalar subset of OpenAI's acknowledged Realtime session configuration."""

    event_id: str | None
    configured: bool
    truncation_type: str | None
    max_post_instructions_tokens: int | None
    retention_ratio: float | None
    turn_detection_type: str | None
    turn_detection_create_response: bool | None
    turn_detection_interrupt_response: bool | None


@dataclass(frozen=True)
class RealtimeErrorDetails:
    code: str | None
    error_type: str | None


def parse_rate_limit_snapshot(event: Any) -> RealtimeRateLimitSnapshot | None:
    """Extract the documented ``rate_limits.updated`` event without raw payloads."""
    if not isinstance(event, Mapping) or event.get("type") != "rate_limits.updated":
        return None

    token_limit = token_remaining = request_limit = request_remaining = None
    token_reset_seconds = request_reset_seconds = None
    rate_limits = event.get("rate_limits")
    if not isinstance(rate_limits, list):
        return None

    found = False
    for item in rate_limits:
        if not isinstance(item, Mapping):
            continue
        name = str(item.get("name", "")).casefold()
        if name == "tokens":
            found = True
            token_limit = _non_negative_int(item.get("limit"))
            token_remaining = _non_negative_int(item.get("remaining"))
            token_reset_seconds = _non_negative_float(item.get("reset_seconds"))
        elif name == "requests":
            found = True
            request_limit = _non_negative_int(item.get("limit"))
            request_remaining = _non_negative_int(item.get("remaining"))
            request_reset_seconds = _non_negative_float(item.get("reset_seconds"))

    if not found:
        return None
    return RealtimeRateLimitSnapshot(
        event_id=_optional_string(event.get("event_id")),
        token_limit=token_limit,
        token_remaining=token_remaining,
        token_reset_seconds=token_reset_seconds,
        request_limit=request_limit,
        request_remaining=request_remaining,
        request_reset_seconds=request_reset_seconds,
    )


def parse_response_id(event: Any) -> str | None:
    if not isinstance(event, Mapping) or event.get("type") != "response.created":
        return None
    response = event.get("response")
    return _optional_string(response.get("id")) if isinstance(response, Mapping) else None


def parse_session_truncation_snapshot(event: Any) -> RealtimeSessionTruncationSnapshot | None:
    """Extract safe session-budget and VAD acknowledgement metadata."""
    if not isinstance(event, Mapping) or event.get("type") != "session.updated":
        return None

    session = event.get("session")
    if not isinstance(session, Mapping):
        return None

    turn_detection = _session_turn_detection(session)
    turn_detection_type = (
        _optional_string(turn_detection.get("type")) if isinstance(turn_detection, Mapping) else None
    )
    turn_detection_create_response = (
        _optional_bool(turn_detection.get("create_response"))
        if isinstance(turn_detection, Mapping)
        else None
    )
    turn_detection_interrupt_response = (
        _optional_bool(turn_detection.get("interrupt_response"))
        if isinstance(turn_detection, Mapping)
        else None
    )

    truncation = session.get("truncation")
    if not isinstance(truncation, Mapping):
        return RealtimeSessionTruncationSnapshot(
            event_id=_optional_string(event.get("event_id")),
            configured=False,
            truncation_type=None,
            max_post_instructions_tokens=None,
            retention_ratio=None,
            turn_detection_type=turn_detection_type,
            turn_detection_create_response=turn_detection_create_response,
            turn_detection_interrupt_response=turn_detection_interrupt_response,
        )

    token_limits = truncation.get("token_limits")
    return RealtimeSessionTruncationSnapshot(
        event_id=_optional_string(event.get("event_id")),
        configured=True,
        truncation_type=_optional_string(truncation.get("type")),
        max_post_instructions_tokens=(
            _non_negative_int(token_limits.get("post_instructions"))
            if isinstance(token_limits, Mapping)
            else None
        ),
        retention_ratio=_non_negative_float(truncation.get("retention_ratio")),
        turn_detection_type=turn_detection_type,
        turn_detection_create_response=turn_detection_create_response,
        turn_detection_interrupt_response=turn_detection_interrupt_response,
    )


def response_usage_from_metrics(metrics: Any) -> RealtimeResponseUsage | None:
    """Convert LiveKit's RealtimeModelMetrics into stable, scalar-only fields."""
    response_id = _optional_string(getattr(metrics, "request_id", None))
    if response_id is None:
        return None

    input_details = getattr(metrics, "input_token_details", None)
    output_details = getattr(metrics, "output_token_details", None)
    ttft_seconds = _non_negative_float(getattr(metrics, "ttft", None))
    return RealtimeResponseUsage(
        response_id=response_id,
        input_tokens=_zero_int(getattr(metrics, "input_tokens", None)),
        input_text_tokens=_zero_int(getattr(input_details, "text_tokens", None)),
        input_audio_tokens=_zero_int(getattr(input_details, "audio_tokens", None)),
        input_cached_tokens=_zero_int(getattr(input_details, "cached_tokens", None)),
        output_tokens=_zero_int(getattr(metrics, "output_tokens", None)),
        output_text_tokens=_zero_int(getattr(output_details, "text_tokens", None)),
        output_audio_tokens=_zero_int(getattr(output_details, "audio_tokens", None)),
        total_tokens=_zero_int(getattr(metrics, "total_tokens", None)),
        duration_ms=int((_non_negative_float(getattr(metrics, "duration", None)) or 0) * 1000),
        ttft_ms=int(ttft_seconds * 1000) if ttft_seconds is not None else None,
        cancelled=bool(getattr(metrics, "cancelled", False)),
    )


def extract_realtime_error_details(error: Any) -> RealtimeErrorDetails:
    """Recover OpenAI's code/type from LiveKit's wrapped APIError when available."""
    containers = list(_error_detail_containers(error))
    return RealtimeErrorDetails(
        code=_first_present_field(containers, "code"),
        # The outer LiveKit RealtimeModelError has type="realtime_model_error".
        # Prefer the deepest provider payload, whose type is actionable (e.g. "tokens").
        error_type=_first_present_field(reversed(containers), "type"),
    )


def _error_detail_containers(error: Any):
    """Yield LiveKit -> APIError -> OpenAI Error objects once each."""
    pending = [error]
    seen: set[int] = set()
    while pending:
        current = pending.pop(0)
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((getattr(current, "error", None), getattr(current, "body", None)))


def _field_as_string(value: Any, field: str) -> str | None:
    if isinstance(value, Mapping):
        return _optional_string(value.get(field))
    return _optional_string(getattr(value, field, None))


def _first_present_field(containers: Any, field: str) -> str | None:
    for container in containers:
        value = _field_as_string(container, field)
        if value:
            return value
    return None


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _session_turn_detection(session: Mapping[str, Any]) -> Mapping[str, Any] | None:
    """Handle both current nested and legacy flat Realtime session shapes."""
    audio = session.get("audio")
    audio_input = audio.get("input") if isinstance(audio, Mapping) else None
    nested = audio_input.get("turn_detection") if isinstance(audio_input, Mapping) else None
    if isinstance(nested, Mapping):
        return nested
    flat = session.get("turn_detection")
    return flat if isinstance(flat, Mapping) else None


def _optional_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _non_negative_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def _zero_int(value: Any) -> int:
    return _non_negative_int(value) or 0


def _non_negative_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None
