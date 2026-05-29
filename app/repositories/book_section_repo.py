import uuid

from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, col, select

from app.models.db_models import BookSection
from app.services.document_structure_types import ParsedDocument, ParsedSection


def delete_sections_by_book(session: Session, book_id: uuid.UUID) -> None:
    sections = session.exec(select(BookSection).where(BookSection.book_id == book_id)).all()
    for section in sections:
        session.delete(section)


def create_book_sections(session: Session, book_id: uuid.UUID, parsed_document: ParsedDocument) -> list[BookSection]:
    created: list[BookSection] = []
    section_index = 0

    def walk(sections: list[ParsedSection], parent_id: uuid.UUID | None = None) -> None:
        nonlocal section_index
        for section in sections:
            row = BookSection(
                book_id=book_id,
                parent_id=parent_id,
                section_index=section_index,
                title=section.title,
                level=section.level,
                path=section.path,
                text_content=section.text or None,
                text_char_count=len(section.text or ""),
                page_start=section.page_start,
                page_end=section.page_end,
                source_href=section.source_href,
                source_anchor=section.source_anchor,
            )
            section_index += 1
            session.add(row)
            session.flush()
            created.append(row)
            walk(section.children, row.id)

    walk(parsed_document.sections)
    return created


def list_book_sections(session: Session, book_id: uuid.UUID) -> list[BookSection]:
    try:
        return list(
            session.exec(
                select(BookSection)
                .where(BookSection.book_id == book_id)
                .order_by(col(BookSection.section_index))
            ).all()
        )
    except ProgrammingError as exc:
        if "book_sections" in str(exc) and "does not exist" in str(exc):
            session.rollback()
            return []
        raise


def list_book_sections_by_ids(session: Session, section_ids: list[uuid.UUID]) -> list[BookSection]:
    if not section_ids:
        return []
    sections = session.exec(select(BookSection).where(BookSection.id.in_(section_ids))).all()
    by_id = {section.id: section for section in sections}
    return [by_id[section_id] for section_id in section_ids if section_id in by_id]
