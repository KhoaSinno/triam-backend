from app.services.voice_agent.query_guard import assess_voice_query, guard_voice_book_query
from app.services.voice_agent.turn_state import PendingVoiceClarification, VoiceTranscriptSnapshot


def _snapshot(text: str) -> VoiceTranscriptSnapshot:
    return VoiceTranscriptSnapshot(text=text, created_monotonic=0.0)


def test_clear_book_metadata_question_is_valid_without_transcript() -> None:
    result = assess_voice_query("Tác giả của sách là ai?")

    assert result.valid is True


def test_section_question_without_target_is_valid() -> None:
    result = assess_voice_query("Tóm tắt chương.")

    assert result.valid is True


def test_short_web_permission_reply_is_not_treated_as_book_query() -> None:
    result = assess_voice_query("Yub làm đi")

    assert result.valid is False
    assert result.reason_code == "permission_reply"


def test_concise_tool_query_can_match_longer_voice_transcript() -> None:
    transcript = _snapshot("Bạn có thể vui lòng tóm tắt giúp mình nội dung chương 4 được không ạ?")

    result = guard_voice_book_query("tóm tắt chương 4", transcript)

    assert result.valid is True
    assert result.reason_code == "valid_transcript_snapshot_available"
    assert result.transcript_source == "final_transcript"


def test_tool_query_with_different_intent_is_not_blocked_by_overlap() -> None:
    transcript = _snapshot("Tác giả của quyển sách là ai?")

    result = guard_voice_book_query("đại ý chương 4", transcript)

    assert result.valid is True
    assert result.reason_code == "valid_transcript_snapshot_available"


def test_voice_query_can_use_vietnamese_number_words() -> None:
    result = assess_voice_query("Tóm tắt chương mười bốn.")

    assert result.valid is True


def test_acronym_question_is_valid_when_it_has_question_context() -> None:
    result = assess_voice_query("SLR là gì?")

    assert result.valid is True


def test_pending_clarification_confirmation_allows_query_when_it_matches_prompt() -> None:
    pending = PendingVoiceClarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        candidate_query=None,
        reason_code="assistant_confirmation",
        created_monotonic=0.0,
    )
    transcript = _snapshot("đúng rồi")

    result = guard_voice_book_query(
        "tóm tắt chương 5",
        transcript,
        pending_clarification=pending,
    )

    assert result.valid is True
    assert result.reason_code == "valid_clarification_confirmation"
    assert result.guard_mode == "clarification_confirmed"


def test_pending_clarification_confirmation_blocks_when_query_does_not_match_prompt() -> None:
    pending = PendingVoiceClarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        candidate_query=None,
        reason_code="assistant_confirmation",
        created_monotonic=0.0,
    )
    transcript = _snapshot("yup làm đi")

    result = guard_voice_book_query(
        "tóm tắt chương 6",
        transcript,
        pending_clarification=pending,
    )

    assert result.valid is False
    assert result.reason_code == "clarification_query_mismatch"


def test_pending_clarification_deny_is_blocked_before_rag() -> None:
    pending = PendingVoiceClarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        candidate_query=None,
        reason_code="assistant_confirmation",
        created_monotonic=0.0,
    )
    transcript = _snapshot("không phải")

    result = guard_voice_book_query(
        "tóm tắt chương 5",
        transcript,
        pending_clarification=pending,
    )

    assert result.valid is False
    assert result.reason_code == "clarification_denied"


def test_pending_clarification_new_question_is_reported_for_caller_rerun() -> None:
    pending = PendingVoiceClarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        candidate_query=None,
        reason_code="assistant_confirmation",
        created_monotonic=0.0,
    )
    transcript = _snapshot("ai là tác giả")

    result = guard_voice_book_query(
        "tác giả của sách là ai",
        transcript,
        pending_clarification=pending,
    )

    assert result.valid is False
    assert result.reason_code == "clarification_new_question"


def test_valid_book_query_with_confirmation_transcript_uses_snapshot_mode() -> None:
    transcript = _snapshot("đúng rồi")
    result = guard_voice_book_query(
        "tóm tắt chương 5",
        transcript,
        pending_clarification=None,
    )
    assert result.valid is True
    assert result.reason_code == "valid_transcript_snapshot_available"
    assert result.guard_mode == "transcript_snapshot"


def test_confirmation_with_generic_pending_clarification_allows_query() -> None:
    pending = PendingVoiceClarification(
        prompt_text="Mình nghe chưa chắc câu hỏi. Bạn nói lại ngắn gọn giúp mình nhé.",
        candidate_query=None,
        reason_code="too_short_or_ack_only",
        created_monotonic=0.0,
    )
    transcript = _snapshot("ok")
    result = guard_voice_book_query(
        "tóm tắt chương 5",
        transcript,
        pending_clarification=pending,
    )
    assert result.valid is True
    assert result.reason_code == "valid_clarification_confirmation"
    assert result.guard_mode == "clarification_confirmed"
