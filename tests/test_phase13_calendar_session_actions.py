import uuid
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.constant import BookStatus, NotificationStatus, PlanMode, PlanStatus, ProcessingJobStatus, ReadingPlanSessionStatus, ReadingPlanSessionUnitStatus
from app.db.database import engine
from app.main import app
from app.models.db_models import (
    Book,
    LearningUnit,
    LearningUnitProgress,
    LearningUnitSegment,
    NotificationOutbox,
    NotificationSettings,
    ReadingPlan,
    ReadingPlanSession,
    ReadingPlanSessionUnit,
)
from app.services.notification_event_service import create_missed_plan_session_outbox_rows


def _delete_book(book_id: uuid.UUID) -> None:
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()


def _delete_notification_settings(user_id: uuid.UUID) -> None:
    with Session(engine) as session:
        settings = session.get(NotificationSettings, user_id)
        if settings:
            session.delete(settings)
            session.commit()


def _delete_outbox_for_user(user_id: uuid.UUID) -> None:
    with Session(engine) as session:
        rows = session.exec(select(NotificationOutbox).where(NotificationOutbox.user_id == user_id)).all()
        for row in rows:
            session.delete(row)
        session.commit()


def _create_book_plan_and_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    scheduled_at: datetime,
    title: str = "Phase 13 Calendar Book",
    status: str = ReadingPlanSessionStatus.SCHEDULED.value,
) -> tuple[Book, ReadingPlan, ReadingPlanSession, LearningUnit]:
    book = Book(
        user_id=user_id,
        title=title,
        total_units=1,
        status=BookStatus.READY.value,
    )
    session.add(book)
    session.flush()

    plan = ReadingPlan(
        book_id=book.id,
        mode=PlanMode.FULL,
        pace=1,
        status=PlanStatus.ACTIVE.value,
        reminder_time="08:00",
    )
    session.add(plan)
    session.flush()

    unit = LearningUnit(
        user_id=user_id,
        book_id=book.id,
        mode=PlanMode.FULL,
        unit_index=0,
        title="Unit 1",
        unit_type="full",
        status=ProcessingJobStatus.READY,
        review_text="Review unit 1",
        source_text_char_count=100,
        estimated_tokens=25,
        estimated_audio_seconds=10,
        main_segment_count=1,
    )
    session.add(unit)
    session.flush()
    session.add(
        LearningUnitSegment(
            learning_unit_id=unit.id,
            segment_index=0,
            audio_url="https://example.test/audio.mp3",
            text_content="Learning content",
            duration_ms=100000,
        )
    )

    local_dt = scheduled_at.astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
    plan_session = ReadingPlanSession(
        user_id=user_id,
        plan_id=plan.id,
        book_id=book.id,
        mode=PlanMode.FULL,
        session_index=0,
        scheduled_at=scheduled_at,
        local_date=local_dt.date().isoformat(),
        reminder_time=f"{local_dt.hour:02d}:{local_dt.minute:02d}",
        timezone="Asia/Ho_Chi_Minh",
        status=status,
        total_units=1,
    )
    session.add(plan_session)
    session.flush()
    session.add(
        ReadingPlanSessionUnit(
            session_id=plan_session.id,
            plan_id=plan.id,
            book_id=book.id,
            learning_unit_id=unit.id,
            unit_order=0,
        )
    )
    session.commit()
    session.refresh(book)
    session.refresh(plan)
    session.refresh(plan_session)
    session.refresh(unit)
    return book, plan, plan_session, unit


def test_calendar_range_endpoint_filters_current_user(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        target_local = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")) + timedelta(days=2)
        target_local = target_local.replace(hour=20, minute=0, second=0, microsecond=0)
        target_utc = target_local.astimezone(timezone.utc)
        with Session(engine) as session:
            book, *_ = _create_book_plan_and_session(session, user_id=user_id, scheduled_at=target_utc)
            other_book, *_ = _create_book_plan_and_session(session, user_id=other_user_id, scheduled_at=target_utc, title="Other User Book")
            book_ids.extend([book.id, other_book.id])

        response = client.get(
            "/api/v1/reading-plan/sessions",
            params={
                "from_date": target_local.date().isoformat(),
                "to_date": target_local.date().isoformat(),
                "status": "scheduled",
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["from_date"] == target_local.date().isoformat()
        assert body["to_date"] == target_local.date().isoformat()
        assert body["total"] == 1
        assert body["items"][0]["book_id"] == str(book.id)
        assert body["summary"]["scheduled"] == 1
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)
        _delete_notification_settings(other_user_id)


def test_skip_session_does_not_complete_learning_progress(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _plan, plan_session, unit = _create_book_plan_and_session(
                session,
                user_id=user_id,
                scheduled_at=datetime.now(timezone.utc) + timedelta(days=1),
            )
            book_id = book.id
            session_id = plan_session.id
            unit_id = unit.id

        response = client.post(f"/api/v1/reading-plan/sessions/{session_id}/skip", json={"reason": "busy"})
        assert response.status_code == 200
        assert response.json()["session"]["status"] == ReadingPlanSessionStatus.SKIPPED.value

        with Session(engine) as session:
            db_session = session.get(ReadingPlanSession, session_id)
            db_unit = session.exec(select(ReadingPlanSessionUnit).where(ReadingPlanSessionUnit.session_id == session_id)).first()
            progress = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.learning_unit_id == unit_id)).first()
            assert db_session.status == ReadingPlanSessionStatus.SKIPPED.value
            assert db_unit.status == ReadingPlanSessionUnitStatus.SKIPPED.value
            assert progress is None
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_reschedule_session_updates_time_and_rejects_conflict(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        first_local = (datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")) + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0)
        second_local = first_local.replace(hour=21, minute=0)
        with Session(engine) as session:
            first_book, _plan, first_session, _unit = _create_book_plan_and_session(
                session,
                user_id=user_id,
                scheduled_at=first_local.astimezone(timezone.utc),
                title="First Book",
            )
            second_book, _plan2, second_session, _unit2 = _create_book_plan_and_session(
                session,
                user_id=user_id,
                scheduled_at=second_local.astimezone(timezone.utc),
                title="Second Book",
            )
            book_ids.extend([first_book.id, second_book.id])
            first_session_id = first_session.id
            second_session_id = second_session.id

        conflict_response = client.put(
            f"/api/v1/reading-plan/sessions/{first_session_id}/schedule",
            json={"local_date": second_local.date().isoformat(), "reminder_time": "21:00"},
        )
        assert conflict_response.status_code == 409
        assert "Second Book" in conflict_response.json()["detail"]

        new_local = first_local + timedelta(days=1)
        success_response = client.put(
            f"/api/v1/reading-plan/sessions/{first_session_id}/schedule",
            json={"local_date": new_local.date().isoformat(), "reminder_time": "20:30"},
        )
        assert success_response.status_code == 200
        body = success_response.json()["session"]
        assert body["id"] == str(first_session_id)
        assert body["local_date"] == new_local.date().isoformat()
        assert body["reminder_time"] == "20:30"
        assert body["status"] == ReadingPlanSessionStatus.SCHEDULED.value

        with Session(engine) as session:
            unchanged = session.get(ReadingPlanSession, second_session_id)
            assert unchanged.reminder_time == "21:00"
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_missed_session_notification_is_idempotent(auth_as):
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            settings = NotificationSettings(
                user_id=user_id,
                timezone="Asia/Ho_Chi_Minh",
                reminders_enabled=True,
                daily_cap=10,
            )
            session.add(settings)
            book, _plan, plan_session, _unit = _create_book_plan_and_session(
                session,
                user_id=user_id,
                scheduled_at=datetime.now(timezone.utc) - timedelta(days=1),
                status=ReadingPlanSessionStatus.MISSED.value,
            )
            book_id = book.id
            plan_session.missed_at = datetime.now(timezone.utc) - timedelta(hours=1)
            session.add(plan_session)
            session.commit()

            created = create_missed_plan_session_outbox_rows(session, now=datetime.now(timezone.utc))
            created_again = create_missed_plan_session_outbox_rows(session, now=datetime.now(timezone.utc))
            assert created == 1
            assert created_again == 0

            outboxes = session.exec(
                select(NotificationOutbox).where(
                    NotificationOutbox.user_id == user_id,
                    NotificationOutbox.status == NotificationStatus.PENDING,
                )
            ).all()
            assert len(outboxes) == 1
            assert outboxes[0].payload["subtype"] == "missed_session"
            session.refresh(plan_session)
            assert plan_session.missed_notified_at is not None
    finally:
        _delete_outbox_for_user(user_id)
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)
