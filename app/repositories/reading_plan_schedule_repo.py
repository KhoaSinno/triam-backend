import uuid

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, select

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


def deactivate_slots_for_plan(session: Session, *, plan_id: uuid.UUID) -> int:
    slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id, ReadingPlanScheduleSlot.is_active.is_(True))).all()
    for slot in slots:
        slot.is_active = False
        session.add(slot)
    session.commit()
    return len(slots)
