import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, LearningProgressStatus, NotificationType, PlanMode, PlanStatus, ProcessingJobStatus, ReviewItemStatus
from app.core.exceptions import ActiveLearningBookLimitExceededError, ReadingPlanScheduleConflictError
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
    SpacedReviewItem,
)
from app.services.notification_event_service import _build_plan_reminder_outbox
from app.services.reading_plan_schedule_service import build_slots_for_plan, validate_active_learning_capacity, validate_plan_schedule_for_create, validate_schedule_slots_available

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def _create_playable_book(
    session: Session,
    *,
    user_id: uuid.UUID = MOCK_USER_ID,
    title: str = "Phase 4.2 Book",
    review_text: str = "Ôn lại kiến thức chính của bài học này.",
) -> tuple[Book, LearningUnit, LearningUnitSegment]:
    book = Book(
        user_id=user_id,
        title=title,
        total_units=1,
        status=BookStatus.READY,
    )
    session.add(book)
    session.flush()

    unit = LearningUnit(
        user_id=user_id,
        book_id=book.id,
        mode=PlanMode.FULL,
        unit_index=0,
        title="Unit 1",
        unit_type="full",
        status=ProcessingJobStatus.READY,
        review_text=review_text,
        source_text_char_count=100,
        estimated_tokens=25,
        estimated_audio_seconds=10,
        main_segment_count=1,
    )
    session.add(unit)
    session.flush()

    segment = LearningUnitSegment(
        learning_unit_id=unit.id,
        segment_index=0,
        audio_url="https://example.test/audio.mp3",
        text_content="Learning content",
        duration_ms=100000,
    )
    session.add(segment)
    session.commit()
    session.refresh(book)
    session.refresh(unit)
    session.refresh(segment)
    return book, unit, segment


def _delete_book(book_id: uuid.UUID) -> None:
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()


def test_learning_progress_creates_reviews_only_after_completion():
    client = TestClient(app)
    with Session(engine) as session:
        book, unit, segment = _create_playable_book(session)
        book_id = book.id
        unit_id = unit.id
        segment_id = segment.id

    try:
        response_50 = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 50000,
                "listened_ms": 50000,
                "progress_percent": 50,
            },
        )
        assert response_50.status_code == 200
        assert response_50.json()["status"] == LearningProgressStatus.IN_PROGRESS.value

        with Session(engine) as session:
            reviews = session.exec(select(SpacedReviewItem).where(SpacedReviewItem.learning_unit_id == unit_id)).all()
            assert reviews == []

        response_82 = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 82000,
                "listened_ms": 82000,
                "progress_percent": 82,
            },
        )
        assert response_82.status_code == 200
        assert response_82.json()["status"] == LearningProgressStatus.COMPLETED.value
        assert response_82.json()["completed_at"] is not None

        duplicate = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 90000,
                "listened_ms": 90000,
                "progress_percent": 90,
            },
        )
        assert duplicate.status_code == 200

        with Session(engine) as session:
            reviews = session.exec(select(SpacedReviewItem).where(SpacedReviewItem.learning_unit_id == unit_id, SpacedReviewItem.status != ReviewItemStatus.CANCELLED)).all()
            assert len(reviews) == 5
            assert {review.interval_days for review in reviews} == {1, 3, 7, 14, 30}
            progress = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.learning_unit_id == unit_id)).first()
            assert progress is not None
            assert progress.max_progress_percent == 90
    finally:
        _delete_book(book_id)


def test_learning_progress_accepts_legacy_plain_review_text():
    client = TestClient(app)
    with Session(engine) as session:
        book, unit, segment = _create_playable_book(
            session,
            title="Phase 4.2 Legacy Review Text Book",
            review_text="Ôn lại bản ghi chú cũ không theo JSON mode.",
        )
        book_id = book.id
        unit_id = unit.id
        segment_id = segment.id

    try:
        response = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 82000,
                "listened_ms": 82000,
                "progress_percent": 82,
            },
        )
        assert response.status_code == 200

        with Session(engine) as session:
            reviews = session.exec(select(SpacedReviewItem).where(SpacedReviewItem.learning_unit_id == unit_id)).all()
            assert len(reviews) == 5
            assert {review.review_text_snapshot for review in reviews} == {"Ôn lại bản ghi chú cũ không theo JSON mode."}
    finally:
        _delete_book(book_id)


def test_book_learning_progress_returns_resume_position():
    client = TestClient(app)
    with Session(engine) as session:
        book, unit, segment = _create_playable_book(session, title="Phase 4.2 Resume Book")
        book_id = book.id
        unit_id = unit.id
        segment_id = segment.id

    try:
        response = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 42000,
                "listened_ms": 42000,
                "progress_percent": 42,
            },
        )
        assert response.status_code == 200

        summary = client.get(f"/api/v1/books/{book_id}/learning-progress?mode=full")
        assert summary.status_code == 200
        body = summary.json()
        assert body["book_progress_percent"] == 42
        assert body["last_learning_unit_id"] == str(unit_id)
        assert body["last_segment_id"] == segment_id
        assert body["position_ms"] == 42000
    finally:
        _delete_book(book_id)


def test_learning_progress_throttles_small_rapid_updates_but_accepts_force_persist():
    client = TestClient(app)
    with Session(engine) as session:
        book, unit, segment = _create_playable_book(session, title="Phase 4.2 Throttle Book")
        book_id = book.id
        unit_id = unit.id
        segment_id = segment.id

    try:
        first = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 42000,
                "listened_ms": 42000,
                "progress_percent": 42,
            },
        )
        assert first.status_code == 200

        small_update = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 43000,
                "listened_ms": 43000,
                "progress_percent": 43,
            },
        )
        assert small_update.status_code == 200
        assert small_update.json()["position_ms"] == 42000

        with Session(engine) as session:
            progress = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.learning_unit_id == unit_id)).first()
            assert progress is not None
            assert progress.position_ms == 42000
            assert progress.max_progress_percent == 42

        forced = client.put(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/progress",
            json={
                "mode": "full",
                "segment_id": segment_id,
                "segment_index": 0,
                "position_ms": 43000,
                "listened_ms": 43000,
                "progress_percent": 43,
                "force_persist": True,
            },
        )
        assert forced.status_code == 200
        assert forced.json()["position_ms"] == 43000

        with Session(engine) as session:
            progress = session.exec(select(LearningUnitProgress).where(LearningUnitProgress.learning_unit_id == unit_id)).first()
            assert progress is not None
            assert progress.position_ms == 43000
            assert progress.max_progress_percent == 43
    finally:
        _delete_book(book_id)


def test_schedule_guardrails_reject_conflict_and_active_book_limit(monkeypatch):
    user_id = uuid.uuid4()
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Schedule Book A")
            plan = ReadingPlan(book_id=book.id, mode=PlanMode.FULL, pace=1, schedule_config=["Mon"], status=PlanStatus.ACTIVE)
            session.add(plan)
            session.commit()
            session.refresh(plan)
            book_ids.append(book.id)

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"])
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

            with pytest.raises(ReadingPlanScheduleConflictError):
                validate_schedule_slots_available(session, user_id=user_id, slots=slots)

            monkeypatch.setattr(settings, "MAX_ACTIVE_LEARNING_BOOKS_PER_USER", 1)
            with pytest.raises(ActiveLearningBookLimitExceededError):
                validate_active_learning_capacity(session, user_id=user_id)
    finally:
        for book_id in book_ids:
            _delete_book(book_id)


def test_plan_reminder_skips_when_user_already_studied_today():
    user_id = uuid.uuid4()
    book_id: uuid.UUID | None = None
    created_outbox_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            book, unit, segment = _create_playable_book(session, user_id=user_id, title="Studied Today Book")
            book_id = book.id
            plan = ReadingPlan(book_id=book.id, mode=PlanMode.FULL, pace=1, schedule_config=["Mon"], status=PlanStatus.ACTIVE)
            session.add(plan)
            session.add(
                NotificationSettings(
                    user_id=user_id,
                    timezone="Asia/Ho_Chi_Minh",
                    reminders_enabled=True,
                    spaced_review_enabled=True,
                    reminder_time="20:00",
                    quiet_hours_start="22:00",
                    quiet_hours_end="07:00",
                    daily_cap=3,
                )
            )
            session.commit()

            now = datetime(2026, 5, 25, 13, 1, tzinfo=timezone.utc)
            progress = LearningUnitProgress(
                user_id=user_id,
                book_id=book.id,
                learning_unit_id=unit.id,
                mode=PlanMode.FULL,
                current_segment_id=segment.id,
                last_segment_index=0,
                position_ms=1000,
                listened_ms=1000,
                total_duration_ms=100000,
                progress_percent=1,
                max_progress_percent=1,
                status=LearningProgressStatus.IN_PROGRESS,
                started_at=now,
                last_activity_at=now,
            )
            session.add(progress)
            session.commit()

            assert _build_plan_reminder_outbox(session, plan, book, now=now) is None

            progress.last_activity_at = datetime(2026, 5, 20, 13, 1, tzinfo=timezone.utc)
            session.add(progress)
            session.commit()
            outbox = _build_plan_reminder_outbox(session, plan, book, now=now)
            assert outbox is not None
            created_outbox_ids.append(outbox.id)
            assert outbox.type == NotificationType.PLAN_REMINDER
    finally:
        with Session(engine) as session:
            notifications = session.exec(select(NotificationOutbox).where(NotificationOutbox.id.in_(created_outbox_ids))).all()
            for outbox in notifications:
                session.delete(outbox)
            settings_row = session.get(NotificationSettings, user_id)
            if settings_row:
                session.delete(settings_row)
            session.commit()
        if book_id:
            _delete_book(book_id)


def test_pause_resume_reading_plan():
    client = TestClient(app)
    user_id = MOCK_USER_ID
    book_id = None
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Pause Resume Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                schedule_config=["Sat"],
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()
            
            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"])
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Pause
        resp_pause = client.post(f"/api/v1/books/{book_id}/pause")
        assert resp_pause.status_code == 200
        assert resp_pause.json()["status"] == PlanStatus.INACTIVE.value

        from app.models.db_models import ReadingPlanScheduleSlot
        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.INACTIVE.value
            active_slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == db_plan.id, ReadingPlanScheduleSlot.is_active == True)).all()
            assert len(active_slots) == 0

        # Resume
        resp_resume = client.post(f"/api/v1/books/{book_id}/resume")
        assert resp_resume.status_code == 200
        assert resp_resume.json()["status"] == PlanStatus.ACTIVE.value

        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.ACTIVE.value
            active_slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == db_plan.id, ReadingPlanScheduleSlot.is_active == True)).all()
            assert len(active_slots) == 1
            assert active_slots[0].weekday == 5  # Sat is 5 (Mon=0, Tue=1, ..., Sat=5)
    finally:
        if book_id:
            _delete_book(book_id)


def test_update_reading_plan():
    client = TestClient(app)
    user_id = MOCK_USER_ID
    book_id = None
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Update Plan Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                schedule_config=["Sat"],
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"])
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Update to Mon, Wed at 08:00
        resp_update = client.put(
            f"/api/v1/books/{book_id}/reading-plan",
            json={
                "pace": 2,
                "schedule_config": ["Mon", "Wed"],
                "reminder_time": "08:00"
            }
        )
        assert resp_update.status_code == 200
        data = resp_update.json()
        assert data["pace"] == 2
        assert data["schedule_config"] == ["Mon", "Wed"]
        assert data["reminder_time"] == "08:00"

        from app.models.db_models import ReadingPlanScheduleSlot
        with Session(engine) as session:
            active_slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.book_id == book_id, ReadingPlanScheduleSlot.is_active == True)).all()
            assert len(active_slots) == 2
            assert {slot.weekday for slot in active_slots} == {0, 2}  # Mon=0, Wed=2
            assert all(slot.reminder_time == "08:00" for slot in active_slots)
    finally:
        if book_id:
            _delete_book(book_id)


def test_plan_auto_deactivate_on_100_percent():
    client = TestClient(app)
    user_id = MOCK_USER_ID
    book_id = None
    try:
        with Session(engine) as session:
            book, unit, segment = _create_playable_book(session, user_id=user_id, title="Auto Complete Book")
            book_id = book.id
            unit_id = unit.id
            segment_id = segment.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                schedule_config=["Sat"],
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"])
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Complete learning unit
        resp_complete = client.post(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/complete",
            json={"mode": "full"}
        )
        assert resp_complete.status_code == 200

        from app.models.db_models import ReadingPlanScheduleSlot
        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.INACTIVE.value
            active_slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == db_plan.id, ReadingPlanScheduleSlot.is_active == True)).all()
            assert len(active_slots) == 0
    finally:
        if book_id:
            _delete_book(book_id)
