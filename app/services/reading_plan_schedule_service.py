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

WEEKDAY_LABELS = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

WEEKDAY_SHORT_LABELS = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun",
}

WEEKDAY_VI_LABELS = {
    0: "Thứ hai",
    1: "Thứ ba",
    2: "Thứ tư",
    3: "Thứ năm",
    4: "Thứ sáu",
    5: "Thứ bảy",
    6: "Chủ nhật",
}


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

    try:
        parse_hhmm(reminder_time)
    except (TypeError, ValueError) as exc:
        raise ReadingPlanScheduleConflictError(f"Giờ học không hợp lệ: {reminder_time}. Vui lòng dùng định dạng HH:MM.") from exc
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
            weekday_label = WEEKDAY_VI_LABELS.get(slot.weekday, f"ngày {slot.weekday}")
            raise ReadingPlanScheduleConflictError(
                f"Lịch học bị trùng vào {weekday_label} lúc {slot.reminder_time}. Hãy chọn ngày hoặc giờ khác."
            )


def build_slots_for_plan(
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    plan_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
    is_active: bool = True,
) -> list[ReadingPlanScheduleSlot]:
    return [
        ReadingPlanScheduleSlot(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan_id,
            weekday=slot.weekday,
            reminder_time=slot.reminder_time,
            timezone=slot.timezone,
            is_active=is_active,
        )
        for slot in slots
    ]


def validate_plan_schedule_shape(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
) -> list[ScheduleSlotInput]:
    user_settings = get_or_create_notification_settings(session, user_id)
    resolved_reminder_time = reminder_time or user_settings.reminder_time
    return normalize_schedule_config(
        schedule_config,
        reminder_time=resolved_reminder_time,
        timezone_name=user_settings.timezone,
    )


def validate_plan_schedule_for_activation(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
    exclude_plan_id: uuid.UUID | None = None,
) -> list[ScheduleSlotInput]:
    slots = validate_plan_schedule_shape(
        session,
        user_id=user_id,
        schedule_config=schedule_config,
        reminder_time=reminder_time,
    )
    if exclude_plan_id is None:
        validate_active_learning_capacity(session, user_id=user_id)
    validate_schedule_slots_available(session, user_id=user_id, slots=slots, exclude_plan_id=exclude_plan_id)
    return slots


def validate_plan_schedule_for_create(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
    exclude_plan_id: uuid.UUID | None = None,
) -> list[ScheduleSlotInput]:
    return validate_plan_schedule_for_activation(
        session,
        user_id=user_id,
        schedule_config=schedule_config,
        reminder_time=reminder_time,
        exclude_plan_id=exclude_plan_id,
    )


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
