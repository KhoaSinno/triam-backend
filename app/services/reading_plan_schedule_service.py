import uuid
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.config import settings
from app.core.exceptions import ActiveLearningBookLimitExceededError, ReadingPlanScheduleConflictError
from app.models.db_models import ReadingPlanScheduleSlot
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.reading_plan_schedule_repo import count_active_learning_books, create_slots_for_plan, find_conflicting_slot
from app.services.reminder_schedule_service import WEEKDAY_ALIASES, parse_hhmm


@dataclass(frozen=True)
class ScheduleSlotInput:
    weekday: int
    reminder_time: str
    timezone: str


def _weekday_from_value(value: object) -> int:
    weekday = WEEKDAY_ALIASES.get(str(value).strip().lower())
    if weekday is None:
        raise ReadingPlanScheduleConflictError(f"Ngày học không hợp lệ: {value}")
    return weekday


def normalize_schedule_config(
    schedule_config: object,
    *,
    reminder_time: str,
    timezone_name: str,
) -> list[ScheduleSlotInput]:
    if not isinstance(schedule_config, list) or not schedule_config:
        raise ReadingPlanScheduleConflictError("Vui lòng chọn ít nhất một ngày học.")

    parse_hhmm(reminder_time)
    weekdays = sorted({_weekday_from_value(day) for day in schedule_config})
    return [ScheduleSlotInput(weekday=weekday, reminder_time=reminder_time, timezone=timezone_name) for weekday in weekdays]


def validate_active_learning_capacity(session: Session, *, user_id: uuid.UUID) -> None:
    if count_active_learning_books(session, user_id=user_id) >= settings.MAX_ACTIVE_LEARNING_BOOKS_PER_USER:
        raise ActiveLearningBookLimitExceededError()


def validate_schedule_slots_available(
    session: Session,
    *,
    user_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
    exclude_plan_id: uuid.UUID | None = None,
) -> None:
    for slot in slots:
        conflict = find_conflicting_slot(
            session,
            user_id=user_id,
            weekday=slot.weekday,
            reminder_time=slot.reminder_time,
            exclude_plan_id=exclude_plan_id,
        )
        if conflict:
            raise ReadingPlanScheduleConflictError()


def build_slots_for_plan(
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    plan_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
) -> list[ReadingPlanScheduleSlot]:
    return [
        ReadingPlanScheduleSlot(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan_id,
            weekday=slot.weekday,
            reminder_time=slot.reminder_time,
            timezone=slot.timezone,
            is_active=True,
        )
        for slot in slots
    ]


def validate_plan_schedule_for_create(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
) -> list[ScheduleSlotInput]:
    user_settings = get_or_create_notification_settings(session, user_id)
    slots = normalize_schedule_config(
        schedule_config,
        reminder_time=user_settings.reminder_time,
        timezone_name=user_settings.timezone,
    )
    validate_active_learning_capacity(session, user_id=user_id)
    validate_schedule_slots_available(session, user_id=user_id, slots=slots)
    return slots


def create_schedule_slots_for_plan(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    plan_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
) -> list[ReadingPlanScheduleSlot]:
    try:
        return create_slots_for_plan(
            session,
            slots=build_slots_for_plan(user_id=user_id, book_id=book_id, plan_id=plan_id, slots=slots),
        )
    except IntegrityError as exc:
        raise ReadingPlanScheduleConflictError() from exc
