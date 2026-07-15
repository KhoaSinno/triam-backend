import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Session, col, delete, func, select

from app.core.constant import PlanMode, ReadingPlanSessionStatus
from app.models.db_models import ReadingPlanSession, ReadingPlanSessionUnit

FINAL_SESSION_STATUSES = {
    ReadingPlanSessionStatus.COMPLETED.value,
    ReadingPlanSessionStatus.SKIPPED.value,
    ReadingPlanSessionStatus.CANCELLED.value,
}
ACTIVE_SESSION_STATUSES = {
    ReadingPlanSessionStatus.SCHEDULED.value,
    ReadingPlanSessionStatus.DUE.value,
    ReadingPlanSessionStatus.IN_PROGRESS.value,
    ReadingPlanSessionStatus.MISSED.value,
}


@dataclass(frozen=True)
class PlanSessionSummaryCounts:
    total_sessions: int
    completed_sessions: int
    missed_sessions: int


def get_owned_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession).where(
            ReadingPlanSession.id == session_id,
            ReadingPlanSession.user_id == user_id,
        )
    ).first()


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


def list_sessions_for_user_range(
    session: Session,
    *,
    user_id: uuid.UUID,
    from_local_date: str,
    to_local_date: str,
    book_id: uuid.UUID | None = None,
    mode: PlanMode | None = None,
    status: str | None = None,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.local_date >= from_local_date,
        ReadingPlanSession.local_date <= to_local_date,
    )
    if book_id:
        statement = statement.where(ReadingPlanSession.book_id == book_id)
    if mode:
        statement = statement.where(ReadingPlanSession.mode == mode)
    if status:
        statement = statement.where(ReadingPlanSession.status == status)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def get_plan_session_summary_counts(session: Session, *, plan_id: uuid.UUID) -> PlanSessionSummaryCounts:
    rows = session.exec(
        select(ReadingPlanSession.status, func.count(ReadingPlanSession.id))
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value,
        )
        .group_by(ReadingPlanSession.status)
    ).all()
    counts = {status: int(count or 0) for status, count in rows}
    return PlanSessionSummaryCounts(
        total_sessions=sum(counts.values()),
        completed_sessions=counts.get(ReadingPlanSessionStatus.COMPLETED.value, 0),
        missed_sessions=counts.get(ReadingPlanSessionStatus.MISSED.value, 0),
    )


def get_next_session_for_plan(session: Session, *, plan_id: uuid.UUID) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession)
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status.notin_(list(FINAL_SESSION_STATUSES)),
        )
        .order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    ).first()


def find_session_schedule_conflict(
    session: Session,
    *,
    user_id: uuid.UUID,
    scheduled_at: datetime,
    exclude_session_id: uuid.UUID,
) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession)
        .where(
            ReadingPlanSession.user_id == user_id,
            ReadingPlanSession.scheduled_at == scheduled_at,
            ReadingPlanSession.id != exclude_session_id,
            ReadingPlanSession.status.in_(list(ACTIVE_SESSION_STATUSES)),
        )
        .order_by(col(ReadingPlanSession.scheduled_at))
    ).first()


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


def mark_overdue_sessions_missed_rows(
    session: Session,
    *,
    user_id: uuid.UUID | None,
    now: datetime,
) -> list[ReadingPlanSession]:
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

    rows = list(session.exec(statement).all())
    for row in rows:
        row.status = ReadingPlanSessionStatus.MISSED.value
        row.missed_at = row.missed_at or now
        row.updated_at = now
        session.add(row)
    return rows


def list_missed_sessions_pending_notification(
    session: Session,
    *,
    now: datetime,
    limit: int,
) -> list[ReadingPlanSession]:
    return list(
        session.exec(
            select(ReadingPlanSession)
            .where(ReadingPlanSession.status == ReadingPlanSessionStatus.MISSED.value)
            .where(ReadingPlanSession.missed_at.is_not(None))
            .where(ReadingPlanSession.missed_at <= now)
            .where(ReadingPlanSession.missed_notified_at.is_(None))
            .order_by(col(ReadingPlanSession.missed_at))
            .limit(limit)
        ).all()
    )


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


def delete_sessions_for_plan(session: Session, *, plan_id: uuid.UUID) -> None:
    """Xóa toàn bộ các buổi học và chi tiết buổi học của kế hoạch học tập."""
    session.execute(
        delete(ReadingPlanSessionUnit)
        .where(ReadingPlanSessionUnit.plan_id == plan_id)
    )
    session.execute(
        delete(ReadingPlanSession)
        .where(ReadingPlanSession.plan_id == plan_id)
    )
