from uuid import UUID

from app.services.agent_grounding.contracts import GroundingBook, GroundingScope, GroundingSection
from app.services.voice_agent.transcription_prompt import build_realtime_transcription_prompt


def _scope() -> GroundingScope:
    first_book_id = UUID("11111111-1111-1111-1111-111111111111")
    second_book_id = UUID("22222222-2222-2222-2222-222222222222")
    return GroundingScope(
        allowed_book_ids=(first_book_id, second_book_id),
        books=(
            GroundingBook(first_book_id, "Algorithms Notes for Professionals", "GoalKicker", "book", 12, None, 12),
            GroundingBook(second_book_id, "C# Fundamentals", "Tri Âm Press", "book", 8, None, 8),
        ),
        sections=(
            GroundingSection(UUID("33333333-3333-3333-3333-333333333333"), first_book_id, None, 12, "Dynamic Programming", 1, "12", 100),
        ),
    )


def _build(*, context_hints_enabled: bool, legacy_prompt_term_limit: int = 8):
    return build_realtime_transcription_prompt(
        base_prompt="Vietnamese audiobook study app.",
        grounding_scope=_scope(),
        enabled=True,
        max_chars=900,
        max_terms=45,
        max_section_terms=20,
        context_hints_enabled=context_hints_enabled,
        legacy_prompt_term_limit=legacy_prompt_term_limit,
    )


def test_legacy_dynamic_prompt_is_unchanged_when_context_hints_are_disabled():
    result = _build(context_hints_enabled=False)

    assert result.context_hints_enabled is False
    assert result.keyword_candidates == ()
    assert result.prompt_term_count == 0
    assert "Chào bạn! Hôm nay chúng ta sẽ cùng thảo luận" in result.prompt
    assert "Algorithms Notes for Professionals" not in result.prompt


def test_prioritized_context_hints_prefer_book_metadata_over_generic_terms():
    result = _build(context_hints_enabled=True, legacy_prompt_term_limit=4)

    assert result.context_hints_enabled is True
    assert result.keyword_candidates[:4] == (
        "Algorithms Notes for Professionals",
        "C# Fundamentals",
        "GoalKicker",
        "book",
    )
    assert result.prompt_term_count == 4
    assert "Chào bạn! Hôm nay chúng ta sẽ cùng thảo luận" not in result.prompt
    assert "Expected names may include: Algorithms Notes for Professionals, C# Fundamentals, GoalKicker, book." in result.prompt
    assert "Tri Âm" not in result.prompt


def test_prioritized_context_hints_can_keep_candidates_without_adding_prompt_terms():
    result = _build(context_hints_enabled=True, legacy_prompt_term_limit=0)

    assert result.keyword_candidates
    assert result.prompt_term_count == 0
    assert "Expected names may include:" not in result.prompt
