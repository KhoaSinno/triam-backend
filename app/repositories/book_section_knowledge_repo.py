import uuid
from dataclasses import dataclass

from sqlalchemy import delete, func, update
from sqlmodel import Session, col, select

from app.models.db_models import BookSection, BookSectionKnowledge


@dataclass(frozen=True)
class SectionKnowledgeSearchTextRow:
    id: int
    section_path: str
    section_title: str
    content: str
    search_text: str


def bulk_create_section_knowledge(session: Session, records: list[BookSectionKnowledge]) -> None:
    for record in records:
        session.add(record)


def delete_section_knowledge(
    session: Session,
    *,
    section_id: uuid.UUID,
    embedding_version: str,
) -> None:
    session.exec(
        delete(BookSectionKnowledge).where(
            BookSectionKnowledge.section_id == section_id,
            BookSectionKnowledge.embedding_version == embedding_version,
        )
    )


def list_section_hashes(
    session: Session,
    *,
    section_id: uuid.UUID,
    embedding_version: str,
) -> list[str]:
    rows = session.exec(
        select(BookSectionKnowledge.content_hash)
        .where(
            BookSectionKnowledge.section_id == section_id,
            BookSectionKnowledge.embedding_version == embedding_version,
        )
        .order_by(col(BookSectionKnowledge.chunk_index))
    ).all()
    return list(rows)


def count_indexed_sections(
    session: Session,
    *,
    book_id: uuid.UUID,
    embedding_version: str,
) -> int:
    return int(
        session.exec(
            select(func.count(func.distinct(BookSectionKnowledge.section_id))).where(
                BookSectionKnowledge.book_id == book_id,
                BookSectionKnowledge.embedding_version == embedding_version,
            )
        ).one()
        or 0
    )


def count_indexable_sections(session: Session, *, book_id: uuid.UUID) -> int:
    return int(
        session.exec(
            select(func.count(BookSection.id)).where(
                BookSection.book_id == book_id,
                BookSection.text_content.is_not(None),
                BookSection.text_char_count > 0,
            )
        ).one()
        or 0
    )


def list_section_knowledge_rows_for_search_text(
    session: Session,
    *,
    book_id: uuid.UUID,
) -> list[SectionKnowledgeSearchTextRow]:
    rows = session.exec(
        select(
            BookSectionKnowledge.id,
            BookSection.path,
            BookSection.title,
            BookSectionKnowledge.content,
            BookSectionKnowledge.search_text,
        )
        .join(BookSection, BookSection.id == BookSectionKnowledge.section_id)
        .where(BookSectionKnowledge.book_id == book_id)
        .order_by(col(BookSection.section_index), col(BookSectionKnowledge.chunk_index))
    ).all()
    return [
        SectionKnowledgeSearchTextRow(
            id=row[0],
            section_path=row[1],
            section_title=row[2],
            content=row[3],
            search_text=row[4],
        )
        for row in rows
        if row[0] is not None
    ]


def update_section_knowledge_search_text(session: Session, *, knowledge_id: int, search_text: str) -> None:
    session.exec(
        update(BookSectionKnowledge)
        .where(BookSectionKnowledge.id == knowledge_id)
        .values(search_text=search_text)
    )
