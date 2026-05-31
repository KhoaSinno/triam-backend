from app.services.voice_agent.web_permission_policy import WebSearchPermissionPolicy


def test_web_search_is_blocked_when_disabled():
    policy = WebSearchPermissionPolicy(enabled=False)

    message = policy.request_permission("giá vàng hôm nay")
    allowed, reason = policy.can_execute("giá vàng hôm nay")

    assert "đang tắt" in message
    assert allowed is False
    assert "đang tắt" in reason


def test_web_search_requires_user_grant_and_consumes_once():
    policy = WebSearchPermissionPolicy(enabled=True)

    permission_message = policy.request_permission("giá vàng hôm nay")
    blocked, reason = policy.can_execute("giá vàng hôm nay")
    decision = policy.observe_user_reply("có, tìm đi")
    allowed, allow_reason = policy.can_execute("giá vàng hôm nay")

    assert "Bạn có muốn" in permission_message
    assert blocked is False
    assert "WEB_SEARCH_PERMISSION_REQUIRED" in reason
    assert decision.granted_query == "giá vàng hôm nay"
    assert allowed is True
    assert allow_reason == ""

    policy.mark_search_consumed()
    allowed_again, reason_again = policy.can_execute("giá vàng hôm nay")

    assert allowed_again is False
    assert "WEB_SEARCH_PERMISSION_REQUIRED" in reason_again


def test_web_search_denial_clears_pending_query():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.request_permission("bitcoin hôm nay")
    decision = policy.observe_user_reply("không cần đâu")
    allowed, reason = policy.can_execute("bitcoin hôm nay")

    assert decision.denied is True
    assert allowed is False
    assert "WEB_SEARCH_PERMISSION_REQUIRED" in reason


def test_web_search_query_mismatch_is_blocked():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.request_permission("giá vàng hôm nay")
    policy.observe_user_reply("ok")
    allowed, reason = policy.can_execute("lịch thi đại học năm nay")

    assert allowed is False
    assert "QUERY_MISMATCH" in reason

