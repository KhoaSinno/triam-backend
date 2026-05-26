import uuid
from datetime import datetime

from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, PlanMode
from app.models.db_models import Chapter, ChapterLearningProgress, ChapterSegment


def get_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode,
) -> ChapterLearningProgress | None:
    return session.exec(
        select(ChapterLearningProgress).where(
            ChapterLearningProgress.user_id == user_id,
            ChapterLearningProgress.chapter_id == chapter_id,
            ChapterLearningProgress.mode == mode,
        )
    ).first()


def save_progress(session: Session, progress: ChapterLearningProgress) -> ChapterLearningProgress:
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
) -> list[ChapterLearningProgress]:
    return list(
        session.exec(
            select(ChapterLearningProgress)
            .where(
                ChapterLearningProgress.user_id == user_id,
                ChapterLearningProgress.book_id == book_id,
                ChapterLearningProgress.mode == mode,
            )
            .order_by(ChapterLearningProgress.updated_at)
        ).all()
    )


def get_latest_activity(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> ChapterLearningProgress | None:
    return session.exec(
        select(ChapterLearningProgress)
        .where(
            ChapterLearningProgress.user_id == user_id,
            ChapterLearningProgress.book_id == book_id,
            ChapterLearningProgress.mode == mode,
            ChapterLearningProgress.last_activity_at.is_not(None),
        )
        .order_by(ChapterLearningProgress.last_activity_at.desc())
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
            select(ChapterLearningProgress.id)
            .where(
                ChapterLearningProgress.user_id == user_id,
                ChapterLearningProgress.book_id == book_id,
                ChapterLearningProgress.mode == mode,
                ChapterLearningProgress.last_activity_at >= start_utc,
                ChapterLearningProgress.last_activity_at < end_utc,
            )
            .limit(1)
        ).first()
        is not None
    )


def list_playable_chapter_ids(session: Session, *, book_id: uuid.UUID, mode: PlanMode) -> list[uuid.UUID]:
    rows = session.exec(
        select(Chapter.id)
        .join(ChapterSegment, ChapterSegment.chapter_id == Chapter.id)
        .where(Chapter.book_id == book_id, ChapterSegment.mode == mode)
        .group_by(Chapter.id, Chapter.chapter_index)
        .order_by(Chapter.chapter_index)
    ).all()
    return list(rows)


def has_playable_uncompleted_chapter(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> bool:
    playable_ids = set(list_playable_chapter_ids(session, book_id=book_id, mode=mode))
    if not playable_ids:
        return False

    completed_ids = set(
        session.exec(
            select(ChapterLearningProgress.chapter_id).where(
                ChapterLearningProgress.user_id == user_id,
                ChapterLearningProgress.book_id == book_id,
                ChapterLearningProgress.mode == mode,
                ChapterLearningProgress.status == LearningProgressStatus.COMPLETED,
            )
        ).all()
    )
    return bool(playable_ids - completed_ids)
