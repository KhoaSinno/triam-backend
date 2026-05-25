import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import NotificationNotFoundError
from app.repositories.notification_settings_repo import get_or_create_notification_settings, update_notification_settings
from app.repositories.user_notification_repo import (
    count_unread_notifications,
    get_user_notification,
    list_user_notifications,
    mark_all_notifications_read,
    mark_notification_read,
)
from app.schemas.notification import NotificationSettingsRequest

MAX_NOTIFICATION_LIST_LIMIT = 100
DEFAULT_NOTIFICATION_LIST_LIMIT = 30


def get_settings(session: Session, user_id: uuid.UUID):
    return get_or_create_notification_settings(session, user_id)


def update_settings(session: Session, user_id: uuid.UUID, payload: NotificationSettingsRequest):
    return update_notification_settings(
        session,
        user_id,
        timezone_name=payload.timezone,
        reminders_enabled=payload.reminders_enabled,
        spaced_review_enabled=payload.spaced_review_enabled,
        reminder_time=payload.reminder_time,
        quiet_hours_start=payload.quiet_hours_start,
        quiet_hours_end=payload.quiet_hours_end,
        daily_cap=payload.daily_cap,
    )


def list_notifications(
    session: Session,
    user_id: uuid.UUID,
    *,
    limit: int = DEFAULT_NOTIFICATION_LIST_LIMIT,
    unread_only: bool = False,
) -> dict:
    safe_limit = max(1, min(limit, MAX_NOTIFICATION_LIST_LIMIT))
    items = list_user_notifications(session, user_id=user_id, limit=safe_limit, unread_only=unread_only)
    unread_count = count_unread_notifications(session, user_id=user_id)
    return {"items": items, "unread_count": unread_count}


def read_notification(session: Session, user_id: uuid.UUID, notification_id: uuid.UUID) -> dict:
    notification = get_user_notification(session, user_id=user_id, notification_id=notification_id)
    if not notification:
        raise NotificationNotFoundError()

    read_at = datetime.now(timezone.utc)
    saved = mark_notification_read(session, notification, read_at=read_at)
    return {"id": saved.id, "read_at": saved.read_at}


def read_all_notifications(session: Session, user_id: uuid.UUID) -> dict:
    read_at = datetime.now(timezone.utc)
    updated_count = mark_all_notifications_read(session, user_id=user_id, read_at=read_at)
    return {"updated_count": updated_count, "read_at": read_at}
