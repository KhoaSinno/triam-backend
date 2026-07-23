import pytest

from app.services.voice_agent.web_permission_intent_classifier import classify_web_permission_intent


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("reply", "expected_intent"),
    [
        ("Yup", "grant"),
        ("Yub làm đi", "grant"),
        ("Sure, go ahead", "grant"),
        ("Ừ tìm đi anh", "grant"),
        ("Ok thử xem", "grant"),
        ("Nope", "deny"),
        ("Nah", "deny"),
        ("Khỏi nha", "deny"),
        ("Không cần đâu", "deny"),
        ("Tùy anh", "unclear"),
        ("Có những phương pháp nào trong tài liệu này?", "new_question"),
        ("Cái chương này nói gì tiếp?", "new_question"),
    ],
)
async def test_fast_path_classifies_common_voice_replies(reply: str, expected_intent: str):
    result = await classify_web_permission_intent(
        pending_query="giá vàng hôm nay",
        user_reply=reply,
        use_llm=False,
    )

    assert result.intent == expected_intent
    assert result.source in {"fast_path", "classifier", "local_embedding"}

