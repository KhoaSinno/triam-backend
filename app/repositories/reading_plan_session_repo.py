import uuid
from datetime import datetime

from sqlmodel import Session, col, func, select

from app.core.constant import PlanMode, ReadingPlanSessionStatus
from app.models.db_models import ReadingPlanSession, ReadingPlanSessionUnit

FINAL_SESSION_STATUSES = {
    ReadingPlanSessionStatus.COMPLETED.value,
    ReadingPlanSessionStatus.SKIPPED.value,
    ReadingPlanSessionStatus.CANCELLED.value,
}


def list_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_sessions_for_book(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode | None = None,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.book_id == book_id,
    )
    if mode:
        statement = statement.where(ReadingPlanSession.mode == mode)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_sessions_for_user_local_date(
    session: Session,
    *,
    user_id: uuid.UUID,
    local_date: str,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.local_date == local_date,
    )
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_due_reminder_sessions(
    session: Session,
    *,
    now: datetime,
    limit: int,
) -> list[ReadingPlanSession]:
    return list(
        session.exec(
            select(ReadingPlanSession)
            .where(ReadingPlanSession.scheduled_at <= now)
            .where(
                ReadingPlanSession.status.in_(
                    [
                        ReadingPlanSessionStatus.SCHEDULED.value,
                        ReadingPlanSessionStatus.DUE.value,
                    ]
                )
            )
            .order_by(col(ReadingPlanSession.scheduled_at))
            .limit(limit)
        ).all()
    )


def has_non_cancelled_sessions_for_plan(session: Session, *, plan_id: uuid.UUID) -> bool:
    return (
        session.exec(
            select(ReadingPlanSession.id)
            .where(ReadingPlanSession.plan_id == plan_id)
            .where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
            .limit(1)
        ).first()
        is not None
    )


def get_session_unit_for_learning_unit(
    session: Session,
    *,
    plan_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> ReadingPlanSessionUnit | None:
    return session.exec(
        select(ReadingPlanSessionUnit).where(
            ReadingPlanSessionUnit.plan_id == plan_id,
            ReadingPlanSessionUnit.learning_unit_id == learning_unit_id,
        )
    ).first()


def list_session_units(session: Session, *, session_ids: list[uuid.UUID]) -> list[ReadingPlanSessionUnit]:
    if not session_ids:
        return []
    return list(
        session.exec(
            select(ReadingPlanSessionUnit)
            .where(ReadingPlanSessionUnit.session_id.in_(session_ids))
            .order_by(col(ReadingPlanSessionUnit.session_id), col(ReadingPlanSessionUnit.unit_order))
        ).all()
    )


def count_completed_session_units(session: Session, *, session_id: uuid.UUID) -> int:
    result = session.exec(
        select(func.count(ReadingPlanSessionUnit.id)).where(
            ReadingPlanSessionUnit.session_id == session_id,
            ReadingPlanSessionUnit.status == "completed",
        )
    ).one()
    return int(result or 0)


def cancel_unfinished_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    now: datetime,
) -> int:
    rows = session.exec(
        select(ReadingPlanSession).where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status.notin_(list(FINAL_SESSION_STATUSES)),
        )
    ).all()
    for row in rows:
        row.status = ReadingPlanSessionStatus.CANCELLED.value
        row.updated_at = now
        session.add(row)
    return len(rows)


def mark_overdue_sessions_missed(
    session: Session,
    *,
    user_id: uuid.UUID | None,
    now: datetime,
) -> int:
    statement = (
        select(ReadingPlanSession)
        .where(ReadingPlanSession.scheduled_at < now)
        .where(
            ReadingPlanSession.status.in_(
                [
                    ReadingPlanSessionStatus.SCHEDULED.value,
                    ReadingPlanSessionStatus.DUE.value,
                    ReadingPlanSessionStatus.IN_PROGRESS.value,
                ]
            )
        )
        .where(ReadingPlanSession.completed_units < ReadingPlanSession.total_units)
    )
    if user_id:
        statement = statement.where(ReadingPlanSession.user_id == user_id)

    rows = session.exec(statement).all()
    for row in rows:
        row.status = ReadingPlanSessionStatus.MISSED.value
        row.missed_at = row.missed_at or now
        row.updated_at = now
        session.add(row)
    return len(rows)
