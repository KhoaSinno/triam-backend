import uuid

from sqlmodel import Session, select

from app.models.db_models import StudyContextDocumentLink


def create_new_context_document(
    session: Session, link: StudyContextDocumentLink
) -> StudyContextDocumentLink:
    existing = session.exec(
        select(StudyContextDocumentLink).where(
            StudyContextDocumentLink.context_id == link.context_id,
            StudyContextDocumentLink.book_id == link.book_id,
        )
    ).first()
    if existing:
        return existing

    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_context_documents(session: Session, context_id: uuid.UUID) -> list[StudyContextDocumentLink]:
    return session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == context_id)
    ).all()


def delete_study_context_document(session: Session, context_id: uuid.UUID, book_id: uuid.UUID) -> None:
    link = session.exec(
        select(StudyContextDocumentLink).where(
            StudyContextDocumentLink.context_id == context_id, StudyContextDocumentLink.book_id == book_id
        )
    ).first()
    if link:
        session.delete(link)
        session.commit()
