from __future__ import annotations

from app.services.agent_grounding.contracts import (
    BookResolution,
    GroundingBook,
    GroundingScope,
    GroundingSection,
    NormalizedQuery,
    ResolutionQuality,
    SectionReference,
    SectionResolution,
)
from app.services.agent_grounding.query_normalizer import normalized_key
from app.services.agent_grounding.section_reference_parser import parse_section_reference


def _query_contains_key(query: NormalizedQuery, key: str) -> bool:
    query_key = " ".join(query.tokens)
    return f" {key} " in f" {query_key} "


def _named_books(scope: GroundingScope, query: NormalizedQuery) -> tuple[GroundingBook, ...]:
    return tuple(book for book in scope.books if normalized_key(book.title) and _query_contains_key(query, normalized_key(book.title)))


def resolve_metadata_book(scope: GroundingScope, query: NormalizedQuery) -> BookResolution:
    if not scope.books:
        return BookResolution(
            ResolutionQuality.NOT_FOUND,
            "no_allowed_books",
            clarification="Tôi chưa tìm thấy sách nào trong ngữ cảnh học tập hiện tại.",
        )

    named = _named_books(scope, query)
    if len(named) == 1:
        return BookResolution(ResolutionQuality.EXACT, "exact_book_title", book=named[0])
    if len(named) > 1:
        return BookResolution(
            ResolutionQuality.AMBIGUOUS,
            "multiple_named_books",
            candidates=named,
            clarification="Tôi tìm thấy nhiều sách phù hợp. Bạn muốn hỏi sách nào?",
        )
    if len(scope.books) == 1:
        return BookResolution(ResolutionQuality.UNIQUE, "single_book_scope", book=scope.books[0])

    if scope.allowed_book_ids:
        primary_id = scope.allowed_book_ids[0]
        primary_book = next((b for b in scope.books if b.id == primary_id), None)
        if primary_book is not None:
            return BookResolution(ResolutionQuality.UNIQUE, "primary_book_fallback", book=primary_book)

    return BookResolution(
        ResolutionQuality.AMBIGUOUS,
        "multiple_books_require_selection",
        candidates=scope.books,
        clarification="Ngữ cảnh hiện có nhiều sách. Bạn muốn hỏi thông tin của sách nào?",
    )


def _sections_for_book(scope: GroundingScope, book_id) -> tuple[GroundingSection, ...]:
    return tuple(sorted((section for section in scope.sections if section.book_id == book_id), key=lambda item: item.section_index))


def _ordinal_candidates(sections: tuple[GroundingSection, ...], ordinal: int) -> tuple[GroundingSection, ...]:
    roots = tuple(section for section in sections if section.parent_id is None)
    path_matches = tuple(section for section in roots if section.path == str(ordinal))
    if path_matches:
        return path_matches

    title_matches: list[GroundingSection] = []
    for section in roots:
        title_key = normalized_key(section.title)
        parsed = parse_section_reference(
            NormalizedQuery(
                original=section.title,
                normalized=section.title.casefold(),
                accent_folded=title_key,
                tokens=tuple(title_key.split()),
            )
        )
        if parsed.explicit_ordinal == ordinal:
            title_matches.append(section)
    if title_matches:
        return tuple(title_matches)
    return (roots[ordinal - 1],) if 0 < ordinal <= len(roots) else ()


def _title_candidates(sections: tuple[GroundingSection, ...], title_hint: str) -> tuple[GroundingSection, ...]:
    hint = normalized_key(title_hint)
    exact = tuple(section for section in sections if normalized_key(section.title) == hint)
    if exact or len(hint.split()) < 2:
        return exact
    return tuple(
        section
        for section in sections
        if f" {hint} " in f" {normalized_key(section.title)} " or f" {normalized_key(section.title)} " in f" {hint} "
    )


def _reference_candidates(sections: tuple[GroundingSection, ...], reference: SectionReference) -> tuple[GroundingSection, ...]:
    if reference.explicit_path:
        return tuple(section for section in sections if section.path == reference.explicit_path)
    if reference.explicit_ordinal is not None:
        return _ordinal_candidates(sections, reference.explicit_ordinal)
    if reference.title_hint:
        return _title_candidates(sections, reference.title_hint)
    return ()


def _clarification_for_candidates(candidates: tuple[GroundingSection, ...]) -> str:
    if len(candidates) == 2:
        return f'Tôi tìm thấy hai mục phù hợp: mục {candidates[0].path} và mục {candidates[1].path}. Bạn muốn hỏi mục nào?'
    return "Tôi tìm thấy nhiều đề mục phù hợp. Bạn vui lòng nói rõ số mục hoặc đường dẫn mục lục."


def _primary_book_with_reference(scope: GroundingScope, reference: SectionReference) -> GroundingBook | None:
    if not scope.allowed_book_ids:
        return None

    primary_id = scope.allowed_book_ids[0]
    primary_book = next((book for book in scope.books if book.id == primary_id), None)
    if primary_book is None:
        return None

    candidates = _reference_candidates(_sections_for_book(scope, primary_book.id), reference)
    return primary_book if candidates else None


def _candidate_books_for_reference(
    scope: GroundingScope,
    query: NormalizedQuery,
    reference: SectionReference,
) -> tuple[GroundingBook, ...]:
    named_books = _named_books(scope, query)
    if named_books:
        return named_books

    if not scope.books:
        return ()

    primary_book = _primary_book_with_reference(scope, reference)
    if primary_book is not None:
        return (primary_book,)

    return scope.books


def _section_matches(
    scope: GroundingScope,
    candidate_books: tuple[GroundingBook, ...],
    reference: SectionReference,
) -> list[tuple[GroundingBook, GroundingSection]]:
    matches: list[tuple[GroundingBook, GroundingSection]] = []
    for book in candidate_books:
        sections = _sections_for_book(scope, book.id)
        for section in _reference_candidates(sections, reference):
            matches.append((book, section))
    return matches


def _section_resolution_from_matches(
    matches: list[tuple[GroundingBook, GroundingSection]],
    reference: SectionReference,
) -> SectionResolution | None:
    if len(matches) == 1:
        book, section = matches[0]
        reason = "exact_section_path" if reference.explicit_path or reference.explicit_ordinal is not None else "exact_section_title"
        return SectionResolution(ResolutionQuality.EXACT, reason, book=book, section=section)

    if len(matches) > 1:
        candidates = tuple(section for _, section in matches)
        return SectionResolution(
            ResolutionQuality.AMBIGUOUS,
            "multiple_section_matches",
            candidates=candidates,
            clarification=_clarification_for_candidates(candidates),
        )

    return None


def resolve_section(scope: GroundingScope, query: NormalizedQuery, reference: SectionReference) -> SectionResolution:
    if not reference.has_target:
        return SectionResolution(
            ResolutionQuality.NOT_FOUND,
            "missing_section_reference",
            clarification="Bạn muốn hỏi chương hoặc đề mục nào?",
        )

    candidate_books = _candidate_books_for_reference(scope, query, reference)
    if not candidate_books:
        return SectionResolution(
            ResolutionQuality.NOT_FOUND,
            "no_allowed_books",
            clarification="Tôi chưa tìm thấy sách nào trong ngữ cảnh học tập hiện tại.",
        )

    resolution = _section_resolution_from_matches(
        _section_matches(scope, candidate_books, reference),
        reference,
    )
    if resolution is not None:
        return resolution

    return SectionResolution(
        ResolutionQuality.NOT_FOUND,
        "section_not_found",
        clarification="Tôi không tìm thấy chương hoặc đề mục đó trong sách hiện tại. Bạn vui lòng kiểm tra lại số hoặc tên mục.",
    )
