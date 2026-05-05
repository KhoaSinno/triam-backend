import uuid

from sqlmodel import Session, select

from app.models.db_models import BookKnowledge


def bulk_create_knowledge(session: Session, records: list[BookKnowledge]) -> None:
    """Insert hàng loạt BookKnowledge (vector chunks) vào DB."""
    for record in records:
        session.add(record)
    session.commit()


def delete_knowledge_by_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    """Xóa toàn bộ vector chunks của 1 chapter (dùng khi rollback)."""
    records = session.exec(
        select(BookKnowledge).where(BookKnowledge.chapter_id == chapter_id)
    ).all()
    for record in records:
        session.delete(record)
    session.commit()

