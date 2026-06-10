from __future__ import annotations

import uuid

from sqlmodel import Session, col, select

from app.db.database import engine
from app.models.db_models import Book, BookSection
from app.services.agent_grounding.contracts import GroundingBook, GroundingScope, GroundingSection, GroundingSectionText


def parse_allowed_book_ids(document_ids: list[str]) -> list[uuid.UUID]:
    result: list[uuid.UUID] = []
    for value in document_ids:
        try:
            parsed = uuid.UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            continue
        if parsed not in result:
            result.append(parsed)
    return result


def get_grounding_scope(session: Session, allowed_book_ids: list[uuid.UUID]) -> GroundingScope:
    if not allowed_book_ids:
        return GroundingScope((), (), ())

    books = list(session.exec(select(Book).where(col(Book.id).in_(allowed_book_ids))).all())

    books_by_id = {book.id: book for book in books}

    ordered_books = [books_by_id[book_id] for book_id in allowed_book_ids if book_id in books_by_id]

    actual_book_ids = [book.id for book in ordered_books]

    if not actual_book_ids:
        return GroundingScope(tuple(allowed_book_ids), (), ())

    sections = list(session.exec(select(BookSection).where(col(BookSection.book_id).in_(actual_book_ids)).order_by(col(BookSection.book_id), col(BookSection.section_index))).all())

    root_count_by_book: dict[uuid.UUID, int] = {}
    for section in sections:
        if section.parent_id is None:
            root_count_by_book[section.book_id] = root_count_by_book.get(section.book_id, 0) + 1

    grounding_books = tuple(
        GroundingBook(
            id=book.id,
            title=book.title,
            author=book.author,
            document_type=book.document_type,
            total_sections=book.total_sections,
            status=book.status,
            root_section_count=root_count_by_book.get(book.id, 0),
        )
        for book in ordered_books
    )

    grounding_sections = tuple(
        GroundingSection(
            id=section.id,
            book_id=section.book_id,
            parent_id=section.parent_id,
            section_index=section.section_index,
            title=section.title,
            level=section.level,
            path=section.path,
            text_char_count=section.text_char_count,
        )
        for section in sections
    )

    return GroundingScope(tuple(actual_book_ids), grounding_books, grounding_sections)


def load_grounding_scope(document_ids: list[str]) -> GroundingScope:
    allowed_book_ids = parse_allowed_book_ids(document_ids)
    with Session(engine) as session:
        return get_grounding_scope(session, allowed_book_ids)


def get_scoped_section_texts(
    session: Session,
    *,
    book_id: uuid.UUID,
    section_ids: tuple[uuid.UUID, ...],
    allowed_book_ids: tuple[uuid.UUID, ...],
) -> tuple[GroundingSectionText, ...]:
    if not section_ids or book_id not in allowed_book_ids:
        return ()
    sections = list(
        session.exec(
            select(BookSection)
            .where(
                BookSection.book_id == book_id,
                col(BookSection.book_id).in_(allowed_book_ids),
                col(BookSection.id).in_(section_ids),
            )
            .order_by(col(BookSection.section_index))
        ).all()
    )
    return tuple(
        GroundingSectionText(
            id=section.id,
            book_id=section.book_id,
            section_index=section.section_index,
            title=section.title,
            path=section.path,
            text_content=section.text_content,
        )
        for section in sections
    )


def load_scoped_section_texts(
    book_id: uuid.UUID,
    section_ids: tuple[uuid.UUID, ...],
    allowed_book_ids: tuple[uuid.UUID, ...],
) -> tuple[GroundingSectionText, ...]:
    with Session(engine) as session:
        return get_scoped_section_texts(
            session,
            book_id=book_id,
            section_ids=section_ids,
            allowed_book_ids=allowed_book_ids,
        )
