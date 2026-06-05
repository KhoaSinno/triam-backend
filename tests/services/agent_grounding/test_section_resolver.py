import uuid

from app.services.agent_grounding.contracts import (
    GroundingBook,
    GroundingScope,
    GroundingSection,
    ResolutionQuality,
    SectionReference,
)
from app.services.agent_grounding.query_normalizer import normalize_query
from app.services.agent_grounding.section_resolver import resolve_metadata_book, resolve_section


def _scope(*, duplicate_title: bool = False, two_books: bool = False) -> GroundingScope:
    book_a = GroundingBook(
        id=uuid.UUID("10000000-0000-0000-0000-000000000001"),
        title="Of Mice and Men",
        author="John Steinbeck",
        document_type="pdf",
        total_sections=4,
        status="ready",
        root_section_count=2,
    )
    sections = [
        GroundingSection(
            id=uuid.UUID("20000000-0000-0000-0000-000000000001"),
            book_id=book_a.id,
            parent_id=None,
            section_index=0,
            title="Chapter 1",
            level=1,
            path="1",
            text_char_count=100,
        ),
        GroundingSection(
            id=uuid.UUID("20000000-0000-0000-0000-000000000002"),
            book_id=book_a.id,
            parent_id=None,
            section_index=1,
            title="Chapter 4",
            level=1,
            path="4",
            text_char_count=100,
        ),
        GroundingSection(
            id=uuid.UUID("20000000-0000-0000-0000-000000000003"),
            book_id=book_a.id,
            parent_id=uuid.UUID("20000000-0000-0000-0000-000000000002"),
            section_index=2,
            title="Crooks and Lennie",
            level=2,
            path="4.1",
            text_char_count=100,
        ),
    ]
    if duplicate_title:
        sections.append(
            GroundingSection(
                id=uuid.UUID("20000000-0000-0000-0000-000000000004"),
                book_id=book_a.id,
                parent_id=uuid.UUID("20000000-0000-0000-0000-000000000001"),
                section_index=3,
                title="Crooks and Lennie",
                level=2,
                path="1.1",
                text_char_count=100,
            )
        )

    books = [book_a]
    if two_books:
        book_b = GroundingBook(
            id=uuid.UUID("10000000-0000-0000-0000-000000000002"),
            title="Research Methods",
            author="A. Researcher",
            document_type="docx",
            total_sections=1,
            status="ready",
            root_section_count=1,
        )
        books.append(book_b)
        sections.append(
            GroundingSection(
                id=uuid.UUID("30000000-0000-0000-0000-000000000001"),
                book_id=book_b.id,
                parent_id=None,
                section_index=0,
                title="Chapter 4",
                level=1,
                path="4",
                text_char_count=100,
            )
        )

    return GroundingScope(allowed_book_ids=tuple(book.id for book in books), books=tuple(books), sections=tuple(sections))


def test_resolves_explicit_root_path_without_using_section_index():
    scope = _scope()
    reference = SectionReference(marker_present=True, explicit_ordinal=4)

    result = resolve_section(scope, normalize_query("Tóm tắt chương 4"), reference)

    assert result.quality == ResolutionQuality.EXACT
    assert result.section is not None
    assert result.section.path == "4"
    assert result.section.section_index == 1


def test_resolves_unique_exact_title():
    result = resolve_section(
        _scope(),
        normalize_query('Giải thích mục "Crooks and Lennie"'),
        SectionReference(marker_present=True, title_hint="Crooks and Lennie"),
    )

    assert result.quality == ResolutionQuality.EXACT
    assert result.section is not None
    assert result.section.path == "4.1"


def test_duplicate_title_requires_clarification():
    result = resolve_section(
        _scope(duplicate_title=True),
        normalize_query('Giải thích mục "Crooks and Lennie"'),
        SectionReference(marker_present=True, title_hint="Crooks and Lennie"),
    )

    assert result.quality == ResolutionQuality.AMBIGUOUS
    assert result.section is None
    assert "hai" in result.clarification.lower()


def test_multiple_books_require_selection_for_metadata():
    result = resolve_metadata_book(_scope(two_books=True), normalize_query("Tác giả là ai?"))

    assert result.quality == ResolutionQuality.AMBIGUOUS
    assert result.book is None


def test_named_book_resolves_metadata_in_multi_book_scope():
    result = resolve_metadata_book(
        _scope(two_books=True),
        normalize_query("Tác giả của Of Mice and Men là ai?"),
    )

    assert result.quality == ResolutionQuality.EXACT
    assert result.book is not None
    assert result.book.author == "John Steinbeck"

