import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
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
    table = BookLearningState.__table__
    statement = insert(table).values(
        id=uuid.uuid4(),
        user_id=user_id,
        book_id=book_id,
        mode=mode,
        status=status,
        book_progress_percent=book_progress_percent,
        completed_units=completed_units,
        playable_units=playable_units,
        last_learning_unit_id=last_learning_unit_id,
        last_segment_id=last_segment_id,
        last_segment_index=last_segment_index,
        position_ms=position_ms,
        started_at=started_at,
        last_activity_at=last_activity_at,
        completed_at=completed_at,
        created_at=now,
        updated_at=now,
    )
    statement = statement.on_conflict_do_update(
        constraint="uq_book_learning_state_user_book_mode",
        set_={
            "status": statement.excluded.status,
            "book_progress_percent": statement.excluded.book_progress_percent,
            "completed_units": statement.excluded.completed_units,
            "playable_units": statement.excluded.playable_units,
            "last_learning_unit_id": statement.excluded.last_learning_unit_id,
            "last_segment_id": statement.excluded.last_segment_id,
            "last_segment_index": statement.excluded.last_segment_index,
            "position_ms": statement.excluded.position_ms,
            # Once a book was started/completed, keep those original timestamps.
            "started_at": func.coalesce(table.c.started_at, statement.excluded.started_at),
            "last_activity_at": statement.excluded.last_activity_at,
            "completed_at": func.coalesce(table.c.completed_at, statement.excluded.completed_at),
            "updated_at": statement.excluded.updated_at,
        },
    ).returning(table.c.id)

    state_id = session.execute(statement).scalar_one()
    session.commit()
    state = session.get(BookLearningState, state_id)
    if state is None:
        raise RuntimeError("Book learning state was not found after upsert.")
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
