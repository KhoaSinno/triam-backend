import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.config import settings
from app.models.db_models import NotificationSettings

MIN_DAILY_CAP = 0
MAX_DAILY_CAP = 10


def _normalize_notification_settings(session: Session, notification_settings: NotificationSettings) -> NotificationSettings:
    safe_daily_cap = min(max(notification_settings.daily_cap, MIN_DAILY_CAP), MAX_DAILY_CAP)
    if notification_settings.daily_cap != safe_daily_cap:
        notification_settings.daily_cap = safe_daily_cap
        notification_settings.updated_at = datetime.now(timezone.utc)
        session.add(notification_settings)
        session.commit()
        session.refresh(notification_settings)
    return notification_settings


def get_notification_settings(session: Session, user_id: uuid.UUID) -> NotificationSettings | None:
    notification_settings = session.get(NotificationSettings, user_id)
    if not notification_settings:
        return None
    return _normalize_notification_settings(session, notification_settings)


def get_or_create_notification_settings(session: Session, user_id: uuid.UUID) -> NotificationSettings:
    existing = get_notification_settings(session, user_id)
    if existing:
        return _normalize_notification_settings(session, existing)

    new_settings = NotificationSettings(
        user_id=user_id,
        timezone=settings.NOTIFICATION_DEFAULT_TIMEZONE,
        reminder_time=settings.NOTIFICATION_DEFAULT_REMINDER_TIME,
        daily_cap=settings.NOTIFICATION_DEFAULT_DAILY_CAP,
        quiet_hours_start=settings.NOTIFICATION_DEFAULT_QUIET_START,
        quiet_hours_end=settings.NOTIFICATION_DEFAULT_QUIET_END,
    )
    try:
        session.add(new_settings)
        session.commit()
        session.refresh(new_settings)
        return new_settings
    except IntegrityError:
        session.rollback()
        existing = get_notification_settings(session, user_id)
        if existing:
            return existing
        raise


def update_notification_settings(
    session: Session,
    user_id: uuid.UUID,
    *,
    timezone_name: str,
    reminders_enabled: bool,
    spaced_review_enabled: bool,
    reminder_time: str,
    quiet_hours_start: str,
    quiet_hours_end: str,
    daily_cap: int,
) -> NotificationSettings:
    notification_settings = get_or_create_notification_settings(session, user_id)
    notification_settings.timezone = timezone_name
    notification_settings.reminders_enabled = reminders_enabled
    notification_settings.spaced_review_enabled = spaced_review_enabled
    notification_settings.reminder_time = reminder_time
    notification_settings.quiet_hours_start = quiet_hours_start
    notification_settings.quiet_hours_end = quiet_hours_end
    notification_settings.daily_cap = daily_cap
    notification_settings.updated_at = datetime.now(timezone.utc)
    session.add(notification_settings)
    session.commit()
    session.refresh(notification_settings)
    return notification_settings
