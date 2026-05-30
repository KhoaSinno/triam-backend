import uuid

from sqlmodel import Session, select

from app.models.db_models import BookKnowledge


def bulk_create_knowledge(session: Session, records: list[BookKnowledge]) -> None:
    """Insert hàng loạt BookKnowledge (vector chunks) vào DB."""
    for record in records:
        session.add(record)
    session.commit()


def delete_knowledge_by_learning_unit(session: Session, learning_unit_id: uuid.UUID) -> None:
    records = session.exec(
        select(BookKnowledge).where(BookKnowledge.learning_unit_id == learning_unit_id)
    ).all()
    for record in records:
        session.delete(record)
    session.commit()

