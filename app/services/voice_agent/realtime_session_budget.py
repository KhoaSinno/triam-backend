"""Configuration for bounded OpenAI Realtime conversation retention."""

from typing import Any

from openai.types.realtime import RealtimeTruncationRetentionRatio
from openai.types.realtime.realtime_truncation_retention_ratio import TokenLimits


def build_realtime_session_budget_options(
    *,
    enabled: bool,
    max_post_instructions_tokens: int,
    retention_ratio: float,
) -> dict[str, Any]:
    """Return optional Realtime model settings for remote conversation truncation.

    An empty mapping is intentional when disabled.  In that state the caller must
    not pass ``truncation`` to LiveKit/OpenAI, preserving the provider default.
    """
    if not enabled:
        return {}

    return {
        "truncation": RealtimeTruncationRetentionRatio(
            type="retention_ratio",
            retention_ratio=retention_ratio,
            token_limits=TokenLimits(
                post_instructions=max_post_instructions_tokens,
            ),
        ),
    }
