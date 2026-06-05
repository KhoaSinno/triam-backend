from app.services.agent_grounding.query_normalizer import contains_phrase, normalize_query, normalized_key


def test_normalize_query_preserves_original_and_builds_accent_folded_tokens():
    result = normalize_query("  TÓM TẮT   Chương  Bốn! ")

    assert result.original == "TÓM TẮT   Chương  Bốn!"
    assert result.normalized == "tóm tắt chương bốn!"
    assert result.accent_folded == "tom tat chuong bon!"
    assert result.tokens == ("tom", "tat", "chuong", "bon")


def test_contains_phrase_uses_token_boundaries():
    query = normalize_query("This paragraph describes a flawless argument.")

    assert contains_phrase(query, "law") is False
    assert contains_phrase(normalize_query("The law is important."), "law") is True


def test_normalized_key_is_stable_for_titles():
    assert normalized_key("  Chương 4: Phương pháp nghiên cứu ") == "chuong 4 phuong phap nghien cuu"

