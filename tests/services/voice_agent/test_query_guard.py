from app.services.voice_agent.query_guard import assess_voice_query, guard_voice_book_query
from app.services.voice_agent.turn_state import VoiceTranscriptSnapshot


def _snapshot(text: str) -> VoiceTranscriptSnapshot:
    return VoiceTranscriptSnapshot(text=text, created_monotonic=0.0)


def test_clear_book_metadata_question_is_valid_without_transcript() -> None:
    result = assess_voice_query("Tác giả của sách là ai?")

    assert result.valid is True


def test_section_question_without_target_asks_clarification() -> None:
    result = assess_voice_query("Tóm tắt chương.")

    assert result.valid is False
    assert result.reason_code == "missing_section_reference"


def test_short_web_permission_reply_is_not_treated_as_book_query() -> None:
    result = assess_voice_query("Yub làm đi")

    assert result.valid is False
    assert result.reason_code == "permission_reply"


def test_concise_tool_query_can_match_longer_voice_transcript() -> None:
    transcript = _snapshot("Bạn có thể vui lòng tóm tắt giúp mình nội dung chương 4 được không ạ?")

    result = guard_voice_book_query("tóm tắt chương 4", transcript)

    assert result.valid is True
    assert result.overlap_ratio == 1.0
    assert result.transcript_source == "final_transcript"


def test_tool_query_with_different_intent_is_blocked() -> None:
    transcript = _snapshot("Tác giả của quyển sách là ai?")

    result = guard_voice_book_query("đại ý chương 4", transcript)

    assert result.valid is False
    assert result.reason_code == "tool_query_transcript_mismatch"


def test_voice_query_can_use_vietnamese_number_words() -> None:
    result = assess_voice_query("Tóm tắt chương mười bốn.")

    assert result.valid is True


def test_acronym_question_is_valid_when_it_has_question_context() -> None:
    result = assess_voice_query("SLR là gì?")

    assert result.valid is True
