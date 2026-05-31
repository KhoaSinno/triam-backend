from datetime import datetime, timedelta, timezone

import pytest

from app.services.voice_agent.contracts import WebPermissionIntentResult
from app.services.voice_agent.web_permission_policy import WebSearchPermissionPolicy


async def fake_classifier(*, pending_query: str, user_reply: str) -> WebPermissionIntentResult:
    del pending_query
    lowered = user_reply.casefold()
    if "grant" in lowered or "yub" in lowered:
        return WebPermissionIntentResult("grant", 0.95, "fake grant", "fake")
    if "deny" in lowered:
        return WebPermissionIntentResult("deny", 0.95, "fake deny", "fake")
    if "new" in lowered:
        return WebPermissionIntentResult("new_question", 0.95, "fake new", "fake")
    return WebPermissionIntentResult("unclear", 0.95, "fake unclear", "fake")


def test_web_search_is_blocked_when_disabled():
    policy = WebSearchPermissionPolicy(enabled=False)

    message = policy.request_permission("giá vàng hôm nay")
    allowed, reason = policy.can_execute("giá vàng hôm nay")

    assert "đang tắt" in message
    assert allowed is False
    assert "đang tắt" in reason


@pytest.mark.asyncio
async def test_web_search_requires_user_grant_and_consumes_once():
    policy = WebSearchPermissionPolicy(enabled=True)

    permission_message = policy.request_permission("giá vàng hôm nay")
    blocked, reason = policy.can_execute("giá vàng hôm nay")
    decision = await policy.observe_user_reply("có, tìm đi")
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


@pytest.mark.asyncio
async def test_web_search_resolves_yub_voice_reply_before_tool_execution():
    policy = WebSearchPermissionPolicy(enabled=True, intent_classifier=fake_classifier)

    policy.request_permission("giá bitcoin hôm nay")
    policy.record_user_reply("Yub làm đi")
    allowed, reason = await policy.resolve_before_web_search("giá bitcoin hôm nay")

    assert allowed is True
    assert reason == ""


@pytest.mark.asyncio
async def test_web_search_recovers_when_model_asked_permission_without_tool():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.record_user_reply("Có, làm đi.")
    allowed, reason = await policy.resolve_before_web_search("cách chọn mô hình LLM tốt")

    assert allowed is True
    assert reason == ""


@pytest.mark.asyncio
async def test_implicit_permission_does_not_treat_new_question_as_grant():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.record_user_reply("Bạn cho tôi biết cách chọn LLM tốt?")
    allowed, reason = await policy.resolve_before_web_search("cách chọn mô hình LLM tốt")

    assert allowed is False
    assert "NEW_QUESTION" in reason


@pytest.mark.asyncio
async def test_implicit_permission_expires_quickly():
    policy = WebSearchPermissionPolicy(enabled=True, implicit_grant_window_seconds=1)

    policy.record_user_reply("Có, làm đi.")
    policy.state.last_user_reply_at = datetime.now(timezone.utc) - timedelta(seconds=5)
    allowed, reason = await policy.resolve_before_web_search("cách chọn mô hình LLM tốt")

    assert allowed is False
    assert "WEB_SEARCH_PERMISSION_REQUIRED" in reason


@pytest.mark.asyncio
async def test_web_search_denial_clears_pending_query():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.request_permission("bitcoin hôm nay")
    decision = await policy.observe_user_reply("không cần đâu")
    allowed, reason = policy.can_execute("bitcoin hôm nay")

    assert decision.denied is True
    assert policy.state.pending_query is None
    assert allowed is False
    assert "WEB_SEARCH_PERMISSION_REQUIRED" in reason


@pytest.mark.asyncio
async def test_unclear_reply_keeps_pending_query():
    policy = WebSearchPermissionPolicy(enabled=True, intent_classifier=fake_classifier)

    policy.request_permission("giá vàng hôm nay")
    decision = await policy.observe_user_reply("unclear")

    assert decision.unclear is True
    assert policy.state.pending_query == "giá vàng hôm nay"


@pytest.mark.asyncio
async def test_new_question_clears_pending_query():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.request_permission("giá vàng hôm nay")
    decision = await policy.observe_user_reply("Có những phương pháp nào trong tài liệu này?")

    assert decision.new_question == "Có những phương pháp nào trong tài liệu này?"
    assert policy.state.pending_query is None


@pytest.mark.asyncio
async def test_web_search_query_mismatch_is_blocked():
    policy = WebSearchPermissionPolicy(enabled=True)

    policy.request_permission("giá vàng hôm nay")
    await policy.observe_user_reply("ok")
    allowed, reason = policy.can_execute("lịch thi đại học năm nay")

    assert allowed is False
    assert "QUERY_MISMATCH" in reason


@pytest.mark.asyncio
async def test_expired_grant_is_blocked():
    policy = WebSearchPermissionPolicy(enabled=True, grant_ttl_seconds=1)

    policy.request_permission("giá vàng hôm nay")
    await policy.observe_user_reply("ok")
    policy.state.granted_at = datetime.now(timezone.utc) - timedelta(seconds=5)
    allowed, reason = policy.can_execute("giá vàng hôm nay")

    assert allowed is False
    assert "EXPIRED" in reason
