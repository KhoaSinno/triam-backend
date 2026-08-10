from app.services.voice_agent.realtime_session_budget import build_realtime_session_budget_options


def test_disabled_session_budget_does_not_pass_truncation_option():
    options = build_realtime_session_budget_options(
        enabled=False,
        max_post_instructions_tokens=8000,
        retention_ratio=0.75,
    )

    assert options == {}


def test_enabled_session_budget_uses_configured_retention_ratio_policy():
    options = build_realtime_session_budget_options(
        enabled=True,
        max_post_instructions_tokens=8000,
        retention_ratio=0.75,
    )

    truncation = options["truncation"]
    assert truncation.type == "retention_ratio"
    assert truncation.retention_ratio == 0.75
    assert truncation.token_limits is not None
    assert truncation.token_limits.post_instructions == 8000
