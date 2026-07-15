import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.models.db_models import BookLearningState


def get_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningState | None:
    return session.exec(
        select(BookLearningState).where(
            BookLearningState.user_id == user_id,
            BookLearningState.book_id == book_id,
            BookLearningState.mode == mode,
        )
    ).first()


def upsert_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    status: str,
    book_progress_percent: int,
    completed_units: int,
    playable_units: int,
    last_learning_unit_id: uuid.UUID | None,
    last_segment_id: int | None,
    last_segment_index: int | None,
    position_ms: int,
    started_at: datetime | None,
    last_activity_at: datetime | None,
    completed_at: datetime | None,
) -> BookLearningState:
    now = datetime.now(timezone.utc)
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if state is None:
        state = BookLearningState(user_id=user_id, book_id=book_id, mode=mode)

    state.status = status
    state.book_progress_percent = book_progress_percent
    state.completed_units = completed_units
    state.playable_units = playable_units
    state.last_learning_unit_id = last_learning_unit_id
    state.last_segment_id = last_segment_id
    state.last_segment_index = last_segment_index
    state.position_ms = position_ms
    state.started_at = state.started_at or started_at
    state.last_activity_at = last_activity_at
    state.completed_at = state.completed_at or completed_at
    state.updated_at = now

    session.add(state)
    session.commit()
    session.refresh(state)
    return state


def reset_book_learning_state(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Đặt lại trạng thái tiến độ tổng quan của sách về ban đầu."""
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if state:
        state.status = "not_started"
        state.book_progress_percent = 0
        state.completed_units = 0
        state.playable_units = 0
        state.last_learning_unit_id = None
        state.last_segment_id = None
        state.last_segment_index = None
        state.position_ms = 0
        state.started_at = None
        state.completed_at = None
        state.updated_at = datetime.now(timezone.utc)
        session.add(state)
