import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.constant import BookStatus, NotificationChannel, NotificationStatus, NotificationType, PlanMode, PlanStatus
from app.db.database import engine
from app.models.db_models import Book, NotificationOutbox, NotificationSettings, ReadingPlan, UserNotification
from app.repositories.notification_outbox_repo import claim_due_outbox, create_outbox_once, recover_stale_outbox
from app.services.notification_event_service import _build_plan_reminder_outbox
from app.tasks.notification_tasks import deliver_one_notification


def _cleanup(outbox_ids: list[uuid.UUID]) -> None:
    with Session(engine) as session:
        notifications = session.exec(select(UserNotification).where(UserNotification.outbox_id.in_(outbox_ids))).all()
        for notification in notifications:
            session.delete(notification)
        for outbox_id in outbox_ids:
            outbox = session.get(NotificationOutbox, outbox_id)
            if outbox:
                session.delete(outbox)
        session.commit()


def _outbox(*, status: NotificationStatus = NotificationStatus.PENDING, attempts: int = 0) -> NotificationOutbox:
    return NotificationOutbox(
        user_id=uuid.uuid4(),
        type=NotificationType.CONTENT_READY,
        channel=NotificationChannel.IN_APP,
        status=status,
        payload={
            "message": "Test content is ready.",
            "action_type": "open_book",
            "action_payload": {"book_id": str(uuid.uuid4())},
        },
        due_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        attempts=attempts,
        idempotency_key=f"test:{uuid.uuid4()}",
    )


def test_create_outbox_once_uses_unique_idempotency_key():
    outbox = _outbox()
    created_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            created = create_outbox_once(session, outbox)
            assert created is not None
            created_ids.append(created.id)

            duplicate = _outbox()
            duplicate.idempotency_key = outbox.idempotency_key
            assert create_outbox_once(session, duplicate) is None
    finally:
        _cleanup(created_ids)


def test_recover_stale_processing_outbox_returns_pending():
    stale_time = datetime.now(timezone.utc) - timedelta(minutes=30)
    outbox = _outbox(status=NotificationStatus.PROCESSING, attempts=1)
    outbox.locked_at = stale_time
    created_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            created = create_outbox_once(session, outbox)
            assert created is not None
            created_ids.append(created.id)

            recovered = recover_stale_outbox(
                session,
                now=datetime.now(timezone.utc),
                stale_before=datetime.now(timezone.utc) - timedelta(minutes=10),
                max_attempts=5,
            )
            assert recovered == 1

            saved = session.get(NotificationOutbox, created.id)
            assert saved.status == NotificationStatus.PENDING
            assert saved.locked_at is None
    finally:
        _cleanup(created_ids)


def test_claim_and_deliver_in_app_outbox_once():
    outbox = _outbox()
    created_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            created = create_outbox_once(session, outbox)
            assert created is not None
            created_ids.append(created.id)

            claimed = claim_due_outbox(
                session,
                now=datetime.now(timezone.utc),
                limit=10,
                worker_id="pytest-worker",
            )
            assert claimed == [created.id]

        deliver_one_notification(created_ids[0])
        deliver_one_notification(created_ids[0])

        with Session(engine) as session:
            saved = session.get(NotificationOutbox, created_ids[0])
            notifications = session.exec(select(UserNotification).where(UserNotification.outbox_id == created_ids[0])).all()
            assert saved.status == NotificationStatus.SENT
            assert len(notifications) == 1
    finally:
        _cleanup(created_ids)


def test_plan_reminder_scan_creates_one_outbox_per_day():
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()
    created_outbox_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            book = Book(
                id=book_id,
                user_id=user_id,
                title="Notification Plan Book",
                status=BookStatus.READY,
                total_chapters=1,
            )
            plan = ReadingPlan(
                book_id=book_id,
                mode=PlanMode.FULL,
                pace=1,
                schedule_config=["Mon"],
                status=PlanStatus.ACTIVE,
            )
            session.add(book)
            session.add(plan)
            session.commit()

            # 2026-05-25 20:01 Asia/Ho_Chi_Minh, Monday.
            now = datetime(2026, 5, 25, 13, 1, tzinfo=timezone.utc)
            assert _build_plan_reminder_outbox(session, plan, book, now=now) is not None
            assert _build_plan_reminder_outbox(session, plan, book, now=now) is None

            outboxes = session.exec(select(NotificationOutbox).where(NotificationOutbox.user_id == user_id)).all()
            created_outbox_ids.extend(outbox.id for outbox in outboxes)
            assert len(outboxes) == 1
            assert outboxes[0].type == NotificationType.PLAN_REMINDER
    finally:
        _cleanup(created_outbox_ids)
        with Session(engine) as session:
            notification_settings = session.get(NotificationSettings, user_id)
            if notification_settings:
                session.delete(notification_settings)
            book = session.get(Book, book_id)
            if book:
                session.delete(book)
            session.commit()
