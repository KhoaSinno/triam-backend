import uuid

from sqlalchemy import delete, func
from sqlmodel import Session, col, select

from app.models.db_models import BookSection, BookSectionKnowledge


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
