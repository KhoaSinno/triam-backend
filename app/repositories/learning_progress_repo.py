import uuid
from datetime import datetime

from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, PlanMode
from app.models.db_models import LearningUnit, LearningUnitProgress, LearningUnitSegment


def get_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress).where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.learning_unit_id == learning_unit_id,
        )
    ).first()


def save_progress(session: Session, progress: LearningUnitProgress) -> LearningUnitProgress:
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


def list_book_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> list[LearningUnitProgress]:
    return list(
        session.exec(
            select(LearningUnitProgress)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
            )
            .order_by(LearningUnitProgress.updated_at)
        ).all()
    )


def get_latest_activity(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
            LearningUnitProgress.last_activity_at.is_not(None),
        )
        .order_by(LearningUnitProgress.last_activity_at.desc())
    ).first()


def has_studied_book_between(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    start_utc: datetime,
    end_utc: datetime,
) -> bool:
    return (
        session.exec(
            select(LearningUnitProgress.id)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
                LearningUnitProgress.last_activity_at >= start_utc,
                LearningUnitProgress.last_activity_at < end_utc,
            )
            .limit(1)
        ).first()
        is not None
    )


def list_playable_unit_ids(session: Session, *, book_id: uuid.UUID, mode: PlanMode) -> list[uuid.UUID]:
    rows = session.exec(
        select(LearningUnit.id)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)
        .group_by(LearningUnit.id, LearningUnit.unit_index)
        .order_by(LearningUnit.unit_index)
    ).all()
    return list(rows)


def has_playable_uncompleted_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> bool:
    playable_ids = set(list_playable_unit_ids(session, book_id=book_id, mode=mode))
    if not playable_ids:
        return False

    completed_ids = set(
        session.exec(
            select(LearningUnitProgress.learning_unit_id).where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
                LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
            )
        ).all()
    )
    return bool(playable_ids - completed_ids)
