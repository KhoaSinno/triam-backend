import pytest

from app.services.voice_agent.voice_intent_classifier import classify_voice_reply_intent_fast_path
from app.services.voice_agent.web_permission_intent_classifier import classify_web_permission_intent_fast_path


@pytest.mark.parametrize(
    ("reply", "expected_intent"),
    [
        ("đúng rồi", "grant"),
        ("Yup làm đi", "grant"),
        ("ok tiếp đi", "grant"),
        ("chính xác", "grant"),
        ("cho phép", "grant"),
        ("cho phép đi", "grant"),
        ("được phép", "grant"),
        ("không phải", "deny"),
        ("thôi bỏ qua", "deny"),
        ("Nope", "deny"),
        ("chương 6 thì sao", "new_question"),
        ("ai là tác giả", "new_question"),
        ("tóm tắt chương 4", "new_question"),
        ("tùy anh", "unclear"),
    ],
)
def test_voice_reply_intent_fast_path_classifies_common_replies(reply: str, expected_intent: str) -> None:
    result = classify_voice_reply_intent_fast_path(reply, max_grant_tokens=4)

    assert result is not None
    assert result.intent == expected_intent


def test_web_permission_fast_path_reuses_shared_voice_intent() -> None:
    grant = classify_web_permission_intent_fast_path("yup làm đi")
    deny = classify_web_permission_intent_fast_path("không")

    assert grant is not None
    assert grant.intent == "grant"
    assert deny is not None
    assert deny.intent == "deny"
