import uuid

from app.services.agent_grounding.contracts import (
    GroundingBook,
    GroundingScope,
    GroundingSection,
    GroundingSectionText,
)
from app.services.agent_grounding.section_context_builder import build_section_context, descendant_section_ids

BOOK_ID = uuid.UUID("10000000-0000-0000-0000-000000000001")
ROOT_ID = uuid.UUID("20000000-0000-0000-0000-000000000001")
CHILD_ID = uuid.UUID("20000000-0000-0000-0000-000000000002")


def _scope() -> GroundingScope:
    book = GroundingBook(
        id=BOOK_ID,
        title="Test Book",
        author="Author",
        document_type="pdf",
        total_sections=2,
        status="ready",
        root_section_count=1,
    )
    sections = (
        GroundingSection(ROOT_ID, BOOK_ID, None, 0, "Chapter 1", 1, "1", 100),
        GroundingSection(CHILD_ID, BOOK_ID, ROOT_ID, 1, "Details", 2, "1.1", 100),
    )
    return GroundingScope((BOOK_ID,), (book,), sections)


def test_descendant_section_ids_preserve_document_order():
    assert descendant_section_ids(_scope(), ROOT_ID) == (ROOT_ID, CHILD_ID)


def test_build_section_context_includes_descendants_and_deduplicates_exact_text():
    rows = (
        GroundingSectionText(ROOT_ID, BOOK_ID, 0, "Chapter 1", "1", "Shared content"),
        GroundingSectionText(CHILD_ID, BOOK_ID, 1, "Details", "1.1", "Shared content"),
    )

    result = build_section_context(_scope().books[0], _scope().sections[0], rows, max_chars=2000)

    assert result.has_content is True
    assert result.text.count("Shared content") == 1
    assert result.section_ids == (ROOT_ID, CHILD_ID)


def test_build_section_context_marks_truncation_and_keeps_multiple_sections():
    rows = (
        GroundingSectionText(ROOT_ID, BOOK_ID, 0, "Chapter 1", "1", "A" * 2000),
        GroundingSectionText(CHILD_ID, BOOK_ID, 1, "Details", "1.1", "B" * 2000),
    )

    result = build_section_context(_scope().books[0], _scope().sections[0], rows, max_chars=1000)

    assert result.truncated is True
    assert "[1 Chapter 1]" in result.text
    assert "[1.1 Details]" in result.text
    assert len(result.text) <= 1000
