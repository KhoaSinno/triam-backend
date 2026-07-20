import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import StudyContext


def get_study_context(session: Session, context_id: uuid.UUID) -> StudyContext | None:
    return session.get(StudyContext, context_id)


def get_study_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return session.exec(
        select(StudyContext).where(
            StudyContext.user_id == user_id,
            StudyContext.is_auto_generated == False
        )
    ).all()



def create_study_context(session: Session, study_context: StudyContext) -> StudyContext:
    session.add(study_context)
    session.commit()
    session.refresh(study_context)
    return study_context


def update_study_context(
    session: Session, context_id: uuid.UUID, title: str | None = None
) -> StudyContext | None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        if title is not None:
            study_context.title = title
        study_context.updated_at = datetime.now(timezone.utc)
        session.add(study_context)
        session.commit()
        session.refresh(study_context)
        return study_context
    return None


def delete_study_context(session: Session, context_id: uuid.UUID) -> None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        session.delete(study_context)
        session.commit()
