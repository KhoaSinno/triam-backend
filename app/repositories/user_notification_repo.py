import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.db_models import UserNotification


def create_user_notification_once(session: Session, notification: UserNotification) -> UserNotification | None:
    try:
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification
    except IntegrityError:
        session.rollback()
        return None


def list_user_notifications(
    session: Session,
    *,
    user_id: uuid.UUID,
    limit: int,
    unread_only: bool = False,
) -> list[UserNotification]:
    statement = select(UserNotification).where(UserNotification.user_id == user_id)
    if unread_only:
        statement = statement.where(UserNotification.read_at.is_(None))
    return list(session.exec(statement.order_by(UserNotification.created_at.desc()).limit(limit)).all())


def count_unread_notifications(session: Session, *, user_id: uuid.UUID) -> int:
    count = session.exec(
        select(func.count(UserNotification.id)).where(
            UserNotification.user_id == user_id,
            UserNotification.read_at.is_(None),
        )
    ).one()
    return int(count or 0)


def get_user_notification(session: Session, *, user_id: uuid.UUID, notification_id: uuid.UUID) -> UserNotification | None:
    return session.exec(
        select(UserNotification).where(
            UserNotification.id == notification_id,
            UserNotification.user_id == user_id,
        )
    ).first()


def mark_notification_read(session: Session, notification: UserNotification, *, read_at: datetime | None = None) -> UserNotification:
    notification.read_at = read_at or datetime.now(timezone.utc)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


def mark_all_notifications_read(session: Session, *, user_id: uuid.UUID, read_at: datetime | None = None) -> int:
    current_time = read_at or datetime.now(timezone.utc)
    notifications = list(
        session.exec(
            select(UserNotification).where(
                UserNotification.user_id == user_id,
                UserNotification.read_at.is_(None),
            )
        ).all()
    )
    for notification in notifications:
        notification.read_at = current_time
        session.add(notification)
    session.commit()
    return len(notifications)
