import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.constant import NotificationChannel, NotificationStatus
from app.core.logger import log
from app.db.database import engine
from app.repositories.notification_outbox_repo import (
    claim_due_outbox,
    get_outbox_by_id,
    has_due_outbox,
    mark_outbox_failed,
    mark_outbox_retry,
    recover_stale_outbox,
)
from app.services.notification_event_service import create_due_plan_reminder_outbox_rows, create_due_review_outbox_rows, deliver_outbox_notification


@celery_app.task(name="triam.notifications.scan_due")
def scan_due_notifications_task() -> None:
    now = datetime.now(timezone.utc)
    created_count = 0
    recovered_count = 0
    should_deliver = False

    with Session(engine) as session:
        recovered_count = recover_stale_outbox(
            session,
            now=now,
            stale_before=now - timedelta(minutes=settings.NOTIFICATION_STALE_LOCK_MINUTES),
            max_attempts=settings.NOTIFICATION_MAX_ATTEMPTS,
        )
        created_count += create_due_review_outbox_rows(session, now=now)
        created_count += create_due_plan_reminder_outbox_rows(session, now=now)
        should_deliver = created_count > 0 or recovered_count > 0 or has_due_outbox(session, now=now)

    log.info(f"Notification scan done | created={created_count} | recovered={recovered_count} | should_deliver={should_deliver}")
    if should_deliver:
        deliver_due_notifications_task.apply_async(queue="notification")


@celery_app.task(name="triam.notifications.deliver_due")
def deliver_due_notifications_task() -> None:
    now = datetime.now(timezone.utc)
    worker_id = f"notification-worker:{uuid.uuid4()}"

    with Session(engine) as session:
        recover_stale_outbox(
            session,
            now=now,
            stale_before=now - timedelta(minutes=settings.NOTIFICATION_STALE_LOCK_MINUTES),
            max_attempts=settings.NOTIFICATION_MAX_ATTEMPTS,
        )
        outbox_ids = claim_due_outbox(
            session,
            now=now,
            limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE,
            worker_id=worker_id,
        )

    for outbox_id in outbox_ids:
        deliver_one_notification(outbox_id)

    log.info(f"Notification delivery batch done | worker_id={worker_id} | delivered_attempts={len(outbox_ids)}")


def _next_retry_at(attempts: int, now: datetime) -> datetime:
    delay_seconds = min(3600, 60 * (2 ** max(0, attempts - 1)))
    return now + timedelta(seconds=delay_seconds)


def deliver_one_notification(outbox_id: uuid.UUID) -> None:
    now = datetime.now(timezone.utc)
    with Session(engine) as session:
        outbox = get_outbox_by_id(session, outbox_id)
        if not outbox or outbox.status != NotificationStatus.PROCESSING:
            return

        try:
            if outbox.channel not in (NotificationChannel.IN_APP, NotificationChannel.PUSH, NotificationChannel.ALL):
                raise ValueError(f"Unsupported notification channel: {outbox.channel}")
            deliver_outbox_notification(session, outbox, now=now)
        except Exception as exc:
            error_message = str(exc)
            log.warning(f"Notification delivery failed | outbox_id={outbox_id} | attempts={outbox.attempts} | error={error_message}")
            if outbox.attempts >= settings.NOTIFICATION_MAX_ATTEMPTS:
                mark_outbox_failed(session, outbox, error_message=error_message)
            else:
                mark_outbox_retry(
                    session,
                    outbox,
                    next_retry_at=_next_retry_at(outbox.attempts, now),
                    error_message=error_message,
                )
