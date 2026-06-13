import uuid

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, delete, select

from app.models.db_models import ReadingPlanScheduleSlot


def count_active_learning_books(session: Session, *, user_id: uuid.UUID) -> int:
    rows = session.exec(
        select(ReadingPlanScheduleSlot.book_id)
        .where(
            ReadingPlanScheduleSlot.user_id == user_id,
            ReadingPlanScheduleSlot.is_active.is_(True),
        )
        .distinct()
    ).all()
    return len(rows)


def find_conflicting_slot(
    session: Session,
    *,
    user_id: uuid.UUID,
    weekday: int,
    reminder_time: str,
    exclude_plan_id: uuid.UUID | None = None,
) -> ReadingPlanScheduleSlot | None:
    statement = select(ReadingPlanScheduleSlot).where(
        ReadingPlanScheduleSlot.user_id == user_id,
        ReadingPlanScheduleSlot.weekday == weekday,
        ReadingPlanScheduleSlot.reminder_time == reminder_time,
        ReadingPlanScheduleSlot.is_active.is_(True),
    )
    if exclude_plan_id:
        statement = statement.where(ReadingPlanScheduleSlot.plan_id != exclude_plan_id)
    return session.exec(statement).first()


def list_active_slots(session: Session, *, user_id: uuid.UUID) -> list[ReadingPlanScheduleSlot]:
    return list(
        session.exec(
            select(ReadingPlanScheduleSlot)
            .where(ReadingPlanScheduleSlot.user_id == user_id, ReadingPlanScheduleSlot.is_active.is_(True))
            .order_by(col(ReadingPlanScheduleSlot.weekday), col(ReadingPlanScheduleSlot.reminder_time))
        ).all()
    )


def list_slots_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    active_only: bool = True,
) -> list[ReadingPlanScheduleSlot]:
    statement = select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id)
    if active_only:
        statement = statement.where(ReadingPlanScheduleSlot.is_active.is_(True))
    statement = statement.order_by(col(ReadingPlanScheduleSlot.weekday), col(ReadingPlanScheduleSlot.reminder_time))
    return list(session.exec(statement).all())


def create_slots_for_plan(
    session: Session,
    *,
    slots: list[ReadingPlanScheduleSlot],
) -> list[ReadingPlanScheduleSlot]:
    try:
        for slot in slots:
            session.add(slot)
        session.commit()
        for slot in slots:
            session.refresh(slot)
        return slots
    except IntegrityError:
        session.rollback()
        raise


def delete_slots_for_plan(session: Session, *, plan_id: uuid.UUID) -> int:
    statement = delete(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id)
    result = session.exec(statement)
    return int(result.rowcount or 0)


def set_slots_active(session: Session, *, plan_id: uuid.UUID, is_active: bool) -> int:
    slots = list_slots_for_plan(session, plan_id=plan_id, active_only=False)
    for slot in slots:
        slot.is_active = is_active
        session.add(slot)
    return len(slots)


def replace_slots_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    slots: list[ReadingPlanScheduleSlot],
) -> list[ReadingPlanScheduleSlot]:
    delete_slots_for_plan(session, plan_id=plan_id)
    for slot in slots:
        session.add(slot)
    return slots
