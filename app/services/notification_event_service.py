import json
import uuid
from datetime import datetime

from sqlalchemy.orm.exc import ObjectDeletedError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import (
    BookStatus,
    LearningProgressStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
    PlanMode,
    PlanStatus,
    ReviewItemStatus,
)
from app.core.logger import log
from app.models.db_models import (
    Book,
    LearningUnit,
    LearningUnitProgress,
    NotificationOutbox,
    ReadingPlan,
    SpacedReviewItem,
    UserNotification,
)
from app.repositories.learning_progress_repo import has_playable_uncompleted_unit, has_studied_book_between
from app.repositories.notification_outbox_repo import (
    count_outbox_for_user_between,
    create_outbox_once,
    get_outbox_by_idempotency_key,
    mark_outbox_sent,
)
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.spaced_review_repo import defer_review_item, get_due_review_items, mark_review_item_due
from app.repositories.user_notification_repo import create_user_notification_once
from app.services.fcm_service import send_fcm_notification
from app.services.notification_copy_service import build_notification_copy
from app.services.reminder_schedule_service import (
    local_day_bounds_utc,
    reminder_due_at_for_today,
    shift_out_of_quiet_hours,
    to_local,
    weekday_is_enabled,
)


def _daily_cap_available(session: Session, *, user_id: uuid.UUID, due_at: datetime, user_settings) -> bool:
    if user_settings.daily_cap <= 0:
        return False

    local_due = to_local(due_at, user_settings.timezone)
    start_utc, end_utc = local_day_bounds_utc(local_due.date(), user_settings.timezone)
    existing_count = count_outbox_for_user_between(
        session,
        user_id=user_id,
        start_utc=start_utc,
        end_utc=end_utc,
    )
    return existing_count < user_settings.daily_cap


def _adjust_due_time(session: Session, *, user_id: uuid.UUID, due_at: datetime) -> datetime | None:
    user_settings = get_or_create_notification_settings(session, user_id)
    shifted_due_at = shift_out_of_quiet_hours(
        due_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if not _daily_cap_available(session, user_id=user_id, due_at=shifted_due_at, user_settings=user_settings):
        return None
    return shifted_due_at


def create_content_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    learning_unit_id: uuid.UUID,
    unit_title: str,
    mode: PlanMode | str,
    due_at: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=due_at)
    if adjusted_due_at is None:
        log.info(
            f"Skip content-ready notification because daily cap is reached | "
            f"user_id={user_id} | learning_unit_id={learning_unit_id}"
        )
        return None

    payload = {
        "book_id": str(book_id),
        "book_title": book_title,
        "learning_unit_id": str(learning_unit_id),
        "unit_title": unit_title,
        "mode": mode_value,
        "message": f"{unit_title} đã sẵn sàng để nghe.",
        "action_type": "open_learning_unit",
        "action_payload": {
            "book_id": str(book_id),
            "learning_unit_id": str(learning_unit_id),
            "mode": mode_value,
        },
    }
    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:{user_id}:{learning_unit_id}:{mode_value}",
        ),
    )


def create_first_playable_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    mode: PlanMode | str,
    now: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=now)
    if adjusted_due_at is None:
        return None

    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload={
                "subtype": "first_playable",
                "book_id": str(book_id),
                "book_title": book_title,
                "mode": mode_value,
                "action_type": "open_book",
                "action_payload": {
                    "book_id": str(book_id),
                    "mode": mode_value,
                },
            },
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:first-playable:{user_id}:{book_id}:{mode_value}",
        ),
    )


def create_book_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    mode: PlanMode | str,
    now: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=now)
    if adjusted_due_at is None:
        return None

    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload={
                "subtype": "book_ready",
                "book_id": str(book_id),
                "book_title": book_title,
                "mode": mode_value,
                "action_type": "open_book",
                "action_payload": {
                    "book_id": str(book_id),
                    "mode": mode_value,
                },
            },
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:book-ready:{user_id}:{book_id}:{mode_value}",
        ),
    )


def _build_review_outbox(session: Session, review_item: SpacedReviewItem, *, now: datetime) -> NotificationOutbox | None:
    user_settings = get_or_create_notification_settings(session, review_item.user_id)
    if not user_settings.spaced_review_enabled:
        return None

    progress = None
    if review_item.source_unit_progress_id:
        progress = session.get(LearningUnitProgress, review_item.source_unit_progress_id)
    if not progress and review_item.learning_unit_id:
        progress = session.exec(
            select(LearningUnitProgress).where(
                LearningUnitProgress.user_id == review_item.user_id,
                LearningUnitProgress.learning_unit_id == review_item.learning_unit_id,
                LearningUnitProgress.mode == review_item.mode,
                LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
            )
        ).first()
    if not progress or progress.status != LearningProgressStatus.COMPLETED:
        review_item.status = ReviewItemStatus.CANCELLED
        review_item.updated_at = now
        session.add(review_item)
        session.commit()
        return None

    due_at = shift_out_of_quiet_hours(
        review_item.due_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if due_at > now:
        defer_review_item(session, review_item, due_at)
        return None
    if not _daily_cap_available(session, user_id=review_item.user_id, due_at=due_at, user_settings=user_settings):
        return None

    unit = session.get(LearningUnit, review_item.learning_unit_id) if review_item.learning_unit_id else None
    book = session.get(Book, review_item.book_id)
    idempotency_key = f"spaced-review:{review_item.id}"
    payload = {
        "book_id": str(review_item.book_id),
        "book_title": book.title if book else "sách của bạn",
        "learning_unit_id": str(review_item.learning_unit_id) if review_item.learning_unit_id else None,
        "unit_title": unit.title if unit else "một bài học đã học",
        "review_item_id": str(review_item.id),
        "mode": review_item.mode.value,
        "interval_days": review_item.interval_days,
        "action_type": "open_review",
        "action_payload": {
            "book_id": str(review_item.book_id),
            "learning_unit_id": str(review_item.learning_unit_id) if review_item.learning_unit_id else None,
            "review_item_id": str(review_item.id),
            "mode": review_item.mode.value,
        },
    }
    outbox = create_outbox_once(
        session,
        NotificationOutbox(
            user_id=review_item.user_id,
            type=NotificationType.SPACED_REVIEW_DUE,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=due_at,
            idempotency_key=idempotency_key,
        ),
    )
    if outbox or get_outbox_by_idempotency_key(session, idempotency_key):
        mark_review_item_due(session, review_item)
    return outbox


def create_due_review_outbox_rows(session: Session, *, now: datetime) -> int:
    created_count = 0
    for review_item in get_due_review_items(session, now=now, limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE * 2):
        try:
            if _build_review_outbox(session, review_item, now=now):
                created_count += 1
        except ObjectDeletedError:
            session.rollback()
            log.warning(f"Review item was deleted concurrently during scan | review_item_id={getattr(review_item, 'id', 'unknown')}")
            continue
    return created_count


def _build_plan_reminder_outbox(session: Session, plan: ReadingPlan, book: Book, *, now: datetime) -> NotificationOutbox | None:
    user_settings = get_or_create_notification_settings(session, book.user_id)
    if not user_settings.reminders_enabled:
        return None

    local_now = to_local(now, user_settings.timezone)
    if not weekday_is_enabled(plan.schedule_config, local_now):
        return None

    reminder_time = plan.reminder_time or user_settings.reminder_time
    reminder_due_at = reminder_due_at_for_today(
        now_utc=now,
        timezone_name=user_settings.timezone,
        reminder_time=reminder_time,
    )
    if now < reminder_due_at:
        return None

    due_at = shift_out_of_quiet_hours(
        reminder_due_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if not _daily_cap_available(session, user_id=book.user_id, due_at=due_at, user_settings=user_settings):
        return None

    if not has_playable_uncompleted_unit(session, user_id=book.user_id, book_id=book.id, mode=plan.mode):
        return None

    start_utc, end_utc = local_day_bounds_utc(local_now.date(), user_settings.timezone)
    if has_studied_book_between(
        session,
        user_id=book.user_id,
        book_id=book.id,
        mode=plan.mode,
        start_utc=start_utc,
        end_utc=end_utc,
    ):
        return None

    local_date = local_now.date().isoformat()
    payload = {
        "book_id": str(book.id),
        "book_title": book.title,
        "plan_id": str(plan.id),
        "mode": plan.mode.value,
        "local_date": local_date,
        "action_type": "open_book",
        "action_payload": {
            "book_id": str(book.id),
            "mode": plan.mode.value,
        },
    }
    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=book.user_id,
            type=NotificationType.PLAN_REMINDER,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=due_at,
            idempotency_key=f"plan:{book.user_id}:{book.id}:{plan.id}:{local_date}",
        ),
    )


def create_due_plan_reminder_outbox_rows(session: Session, *, now: datetime) -> int:
    plan_ids = session.exec(
        select(ReadingPlan.id)
        .join(Book, ReadingPlan.book_id == Book.id)
        .where(ReadingPlan.status == PlanStatus.ACTIVE)
        .where(Book.status.in_([BookStatus.PARTIAL_READY.value, BookStatus.READY.value]))
    ).all()

    created_count = 0
    for plan_id in plan_ids:
        try:
            plan = session.get(ReadingPlan, plan_id)
            if not plan:
                continue
            book = session.get(Book, plan.book_id)
            if not book or book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
                continue
            if _build_plan_reminder_outbox(session, plan, book, now=now):
                created_count += 1
        except ObjectDeletedError:
            session.rollback()
            log.warning(f"Reading plan or book was deleted concurrently during scan | plan_id={plan_id}")
            continue
    return created_count


def deliver_outbox_notification(session: Session, outbox: NotificationOutbox, *, now: datetime) -> None:
    title, body = build_notification_copy(outbox.type, outbox.payload)

    # 1. In-app Delivery
    if outbox.channel in (NotificationChannel.IN_APP, NotificationChannel.ALL):
        notification = UserNotification(
            user_id=outbox.user_id,
            outbox_id=outbox.id,
            type=outbox.type,
            title=title,
            body=body,
            action_type=outbox.payload.get("action_type"),
            action_payload=outbox.payload.get("action_payload"),
        )
        create_user_notification_once(session, notification)

    # 2. Push/FCM Delivery
    if outbox.channel in (NotificationChannel.PUSH, NotificationChannel.ALL):
        fcm_data = {}
        if outbox.payload.get("action_type"):
            fcm_data["action_type"] = outbox.payload["action_type"]
        if outbox.payload.get("action_payload"):
            fcm_data["action_payload"] = json.dumps(outbox.payload["action_payload"])

        fcm_data["outbox_id"] = str(outbox.id)
        fcm_data["notification_type"] = outbox.type.value

        send_fcm_notification(session, user_id=outbox.user_id, title=title, body=body, data=fcm_data)

    mark_outbox_sent(session, outbox, now=now)
