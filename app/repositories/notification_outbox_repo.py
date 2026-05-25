import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.constant import NotificationStatus
from app.models.db_models import NotificationOutbox


def create_outbox_once(session: Session, outbox: NotificationOutbox) -> NotificationOutbox | None:
    try:
        session.add(outbox)
        session.commit()
        session.refresh(outbox)
        return outbox
    except IntegrityError:
        session.rollback()
        return None


def get_outbox_by_id(session: Session, outbox_id: uuid.UUID) -> NotificationOutbox | None:
    return session.get(NotificationOutbox, outbox_id)


def get_outbox_by_idempotency_key(session: Session, idempotency_key: str) -> NotificationOutbox | None:
    return session.exec(select(NotificationOutbox).where(NotificationOutbox.idempotency_key == idempotency_key)).first()


def recover_stale_outbox(
    session: Session,
    *,
    now: datetime,
    stale_before: datetime,
    max_attempts: int,
) -> int:
    rows = list(
        session.exec(
            select(NotificationOutbox).where(NotificationOutbox.status == NotificationStatus.PROCESSING).where(NotificationOutbox.locked_at < stale_before).with_for_update(skip_locked=True)
        ).all()
    )

    recovered = 0
    for row in rows:
        if row.attempts >= max_attempts:
            row.status = NotificationStatus.FAILED
            row.error_message = row.error_message or "Notification delivery exceeded max attempts."
        else:
            row.status = NotificationStatus.PENDING
            row.locked_at = None
            row.locked_by = None
            row.next_retry_at = now
            recovered += 1
        row.updated_at = now
        session.add(row)

    session.commit()
    return recovered


def has_due_outbox(session: Session, *, now: datetime) -> bool:
    return (
        session.exec(
            select(NotificationOutbox.id)
            .where(NotificationOutbox.status == NotificationStatus.PENDING)
            .where(NotificationOutbox.due_at <= now)
            .where((NotificationOutbox.next_retry_at.is_(None)) | (NotificationOutbox.next_retry_at <= now))
            .limit(1)
        ).first()
        is not None
    )


def claim_due_outbox(
    session: Session,
    *,
    now: datetime,
    limit: int,
    worker_id: str,
) -> list[uuid.UUID]:
    rows = list(
        session.exec(
            select(NotificationOutbox)
            .where(NotificationOutbox.status == NotificationStatus.PENDING)
            .where(NotificationOutbox.due_at <= now)
            .where((NotificationOutbox.next_retry_at.is_(None)) | (NotificationOutbox.next_retry_at <= now))
            .order_by(NotificationOutbox.due_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        ).all()
    )

    ids: list[uuid.UUID] = []
    for row in rows:
        row.status = NotificationStatus.PROCESSING
        row.locked_at = now
        row.locked_by = worker_id
        row.attempts += 1
        row.error_message = None
        row.updated_at = now
        ids.append(row.id)
        session.add(row)

    session.commit()
    return ids


def mark_outbox_sent(session: Session, outbox: NotificationOutbox, *, now: datetime | None = None) -> NotificationOutbox:
    current_time = now or datetime.now(timezone.utc)
    outbox.status = NotificationStatus.SENT
    outbox.sent_at = current_time
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.next_retry_at = None
    outbox.error_message = None
    outbox.updated_at = current_time
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def mark_outbox_retry(
    session: Session,
    outbox: NotificationOutbox,
    *,
    next_retry_at: datetime,
    error_message: str,
) -> NotificationOutbox:
    outbox.status = NotificationStatus.PENDING
    outbox.next_retry_at = next_retry_at
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.error_message = error_message[:1000]
    outbox.updated_at = datetime.now(timezone.utc)
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def mark_outbox_failed(session: Session, outbox: NotificationOutbox, *, error_message: str) -> NotificationOutbox:
    outbox.status = NotificationStatus.FAILED
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.error_message = error_message[:1000]
    outbox.updated_at = datetime.now(timezone.utc)
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def count_outbox_for_user_between(
    session: Session,
    *,
    user_id: uuid.UUID,
    start_utc: datetime,
    end_utc: datetime,
) -> int:
    count = session.exec(
        select(func.count(NotificationOutbox.id)).where(
            NotificationOutbox.user_id == user_id,
            NotificationOutbox.due_at >= start_utc,
            NotificationOutbox.due_at < end_utc,
            NotificationOutbox.status != NotificationStatus.CANCELLED,
            NotificationOutbox.status != NotificationStatus.FAILED,
        )
    ).one()
    return int(count or 0)
