import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select, text

from app.core.config import settings
from app.core.constant import BookStatus, LearningProgressStatus, NotificationType, PlanMode, PlanStatus, ProcessingJobStatus, ReviewItemStatus
from app.core.exceptions import ActiveLearningBookLimitExceededError, ReadingPlanScheduleConflictError
from app.db.database import engine
from app.main import app
from app.models.db_models import (
    Book,
    BookLearningState,
    BookSection,
    LearningUnit,
    LearningUnitProgress,
    LearningUnitSegment,
    NotificationOutbox,
    NotificationSettings,
    ReadingPlan,
    ReadingPlanScheduleSlot,
    ReadingPlanSession,
    SpacedReviewItem,
)
from app.services.notification_event_service import create_due_plan_reminder_outbox_rows
from app.services.reading_plan_schedule_service import (
    build_slots_for_plan,
    validate_active_learning_capacity,
    validate_plan_schedule_for_create,
    validate_plan_schedule_shape,
    validate_schedule_slots_available,
)

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


def _delete_notification_settings(user_id: uuid.UUID) -> None:
    with Session(engine) as session:
        settings_row = session.get(NotificationSettings, user_id)
        if settings_row:
            session.delete(settings_row)
            session.commit()


def _create_draft_book_with_section(session: Session, *, user_id: uuid.UUID, title: str = "Draft Book") -> Book:
    book = Book(
        user_id=user_id,
        title=title,
        total_sections=1,
        status=BookStatus.DRAFT,
        file_url="https://example.test/storage/v1/object/public/raw_books/test/original.pdf",
        document_type="pdf",
    )
    session.add(book)
    session.flush()
    session.add(
        BookSection(
            book_id=book.id,
            section_index=0,
            title="Unit Source",
            level=1,
            path="1",
            text_content="Nội dung đủ để tạo bài học.",
            text_char_count=28,
        )
    )
    session.commit()
    session.refresh(book)
    return book


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
            assert len(reviews) == 1
            assert {review.interval_days for review in reviews} == {1}
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
            assert len(reviews) == 1
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
            plan = ReadingPlan(book_id=book.id, mode=PlanMode.FULL, pace=1, status=PlanStatus.ACTIVE)
            session.add(plan)
            session.commit()
            session.refresh(plan)
            book_ids.append(book.id)

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
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
            plan = ReadingPlan(book_id=book.id, mode=PlanMode.FULL, pace=1, status=PlanStatus.ACTIVE, reminder_time="20:00")
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
            session.refresh(plan)

            now = datetime(2026, 5, 25, 13, 1, tzinfo=timezone.utc)
            session.add(
                ReadingPlanSession(
                    user_id=user_id,
                    plan_id=plan.id,
                    book_id=book.id,
                    mode=PlanMode.FULL,
                    session_index=0,
                    scheduled_at=datetime(2026, 5, 25, 13, 0, tzinfo=timezone.utc),
                    local_date="2026-05-25",
                    reminder_time="20:00",
                    timezone="Asia/Ho_Chi_Minh",
                    status="scheduled",
                    total_units=1,
                    completed_units=0,
                )
            )
            session.commit()
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

            assert create_due_plan_reminder_outbox_rows(session, now=now) == 0

            progress.last_activity_at = datetime(2026, 5, 20, 13, 1, tzinfo=timezone.utc)
            session.add(progress)
            session.commit()
            assert create_due_plan_reminder_outbox_rows(session, now=now) == 1
            outbox = session.exec(select(NotificationOutbox).where(NotificationOutbox.user_id == user_id)).first()
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
            session.execute(text("DELETE FROM reading_plan_schedule_slots WHERE user_id = :uid"), {"uid": user_id})
            session.execute(text("DELETE FROM reading_plans WHERE book_id IN (SELECT id FROM books WHERE user_id = :uid)"), {"uid": user_id})
            session.commit()
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Pause Resume Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Pause
        resp_pause = client.post(f"/api/v1/books/{book_id}/pause")
        assert resp_pause.status_code == 200
        assert resp_pause.json()["status"] == PlanStatus.INACTIVE.value

        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.INACTIVE.value
            all_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.plan_id == db_plan.id,
                )
            ).all()
            assert len(all_slots) == 1
            assert all_slots[0].is_active is False

        # Resume
        resp_resume = client.post(f"/api/v1/books/{book_id}/resume")
        assert resp_resume.status_code == 200
        assert resp_resume.json()["status"] == PlanStatus.ACTIVE.value

        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.ACTIVE.value
            active_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.plan_id == db_plan.id,
                    ReadingPlanScheduleSlot.is_active.is_(True),
                )
            ).all()
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
            session.execute(text("DELETE FROM reading_plan_schedule_slots WHERE user_id = :uid"), {"uid": user_id})
            session.execute(text("DELETE FROM reading_plans WHERE book_id IN (SELECT id FROM books WHERE user_id = :uid)"), {"uid": user_id})
            session.commit()
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Update Plan Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Update to Mon, Wed at 08:00
        resp_update = client.put(
            f"/api/v1/books/{book_id}/reading-plan",
            json={
                "pace": 2,
                "schedule_config": ["Mon", "Wed"],
                "reminder_time": "08:00",
            }
        )
        assert resp_update.status_code == 200
        data = resp_update.json()
        assert data["pace"] == 2
        assert data["schedule_config"] == ["Mon", "Wed"]
        assert data["reminder_time"] == "08:00"

        with Session(engine) as session:
            active_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.book_id == book_id,
                    ReadingPlanScheduleSlot.is_active.is_(True),
                )
            ).all()
            assert len(active_slots) == 2
            assert {slot.weekday for slot in active_slots} == {0, 2}  # Mon=0, Wed=2
            assert all(slot.reminder_time == "08:00" for slot in active_slots)
    finally:
        if book_id:
            _delete_book(book_id)


def test_get_reading_plan_returns_current_schedule_for_prefill(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Get Plan Prefill Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=2,
                status=PlanStatus.ACTIVE.value,
                reminder_time="07:15",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(
                session,
                user_id=user_id,
                schedule_config=["Tue", "Thu"],
                reminder_time="07:15",
            )
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        response = client.get(f"/api/v1/books/{book_id}/reading-plan")

        assert response.status_code == 200
        body = response.json()
        assert body["book_id"] == str(book_id)
        assert body["mode"] == "full"
        assert body["pace"] == 2
        assert body["schedule_config"] == ["Tue", "Thu"]
        assert body["reminder_time"] == "07:15"
        assert body["status"] == "active"
        assert [(slot["weekday_label"], slot["reminder_time"]) for slot in body["active_slots"]] == [
            ("tuesday", "07:15"),
            ("thursday", "07:15"),
        ]

        slots_response = client.get("/api/v1/reading-plan-slots")
        assert slots_response.status_code == 200
        occupied_slots = slots_response.json()
        assert {(slot["book_id"], slot["weekday_label"], slot["reminder_time"]) for slot in occupied_slots} == {
            (str(book_id), "tuesday", "07:15"),
            (str(book_id), "thursday", "07:15"),
        }
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_generate_plan_inactive_does_not_conflict_with_active_schedule(auth_as, monkeypatch):
    calls = []

    def fake_apply_async(*, args, queue):
        calls.append({"args": args, "queue": queue})

    monkeypatch.setattr("app.services.upload_service.process_book_task.apply_async", fake_apply_async)

    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            active_book, _, _ = _create_playable_book(session, user_id=user_id, title="Already Active Book")
            draft_book = _create_draft_book_with_section(session, user_id=user_id, title="Deferred Draft Book")
            book_ids = [active_book.id, draft_book.id]

            active_plan = ReadingPlan(
                book_id=active_book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(active_plan)
            session.commit()
            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=active_book.id, plan_id=active_plan.id, slots=slots))
            session.commit()

        response = client.post(
            "/api/v1/generate-plan",
            json={
                "book_id": str(book_ids[1]),
                "mode": "full",
                "pace": 1,
                "schedule_config": ["Mon"],
                "reminder_time": "20:00",
                "activate": False,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["plan_status"] == PlanStatus.INACTIVE.value
        assert body["active_slots"] == []
        assert body["job_id"]
        assert calls == [{"args": [str(book_ids[1]), "full", body["job_id"]], "queue": "document"}]

        with Session(engine) as session:
            inactive_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_ids[1])).first()
            assert inactive_plan is not None
            assert inactive_plan.status == PlanStatus.INACTIVE.value
            active_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.book_id == book_ids[1],
                    ReadingPlanScheduleSlot.is_active.is_(True),
                )
            ).all()
            assert active_slots == []

        slots_response = client.get("/api/v1/reading-plan-slots")
        assert slots_response.status_code == 200
        occupied_slots = slots_response.json()
        assert {(slot["book_id"], slot["weekday_label"], slot["reminder_time"]) for slot in occupied_slots} == {
            (str(book_ids[0]), "monday", "20:00")
        }
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_get_reading_plan_without_plan_returns_404(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book = Book(user_id=user_id, title="Draft Without Plan", status=BookStatus.DRAFT)
            session.add(book)
            session.commit()
            session.refresh(book)
            book_id = book.id

        response = client.get(f"/api/v1/books/{book_id}/reading-plan")

        assert response.status_code == 404
        assert response.json()["detail"] == "Chưa có ReadingPlan cho sách này."
    finally:
        if book_id:
            _delete_book(book_id)


def test_update_reading_plan_keeps_self_slot_and_rejects_other_book_conflict(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            book_a, _, _ = _create_playable_book(session, user_id=user_id, title="Plan Conflict A")
            book_b, _, _ = _create_playable_book(session, user_id=user_id, title="Plan Conflict B")
            book_ids = [book_a.id, book_b.id]

            plan_a = ReadingPlan(
                book_id=book_a.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            plan_b = ReadingPlan(
                book_id=book_b.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="21:00",
            )
            session.add(plan_a)
            session.add(plan_b)
            session.commit()

            slots_a = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book_a.id, plan_id=plan_a.id, slots=slots_a))
            slots_b = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Wed"], reminder_time="21:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book_b.id, plan_id=plan_b.id, slots=slots_b))
            session.commit()

        same_slot_response = client.put(
            f"/api/v1/books/{book_ids[0]}/reading-plan",
            json={"pace": 2, "schedule_config": ["Mon"], "reminder_time": "20:00"},
        )
        assert same_slot_response.status_code == 200
        assert same_slot_response.json()["active_slots"][0]["weekday_label"] == "monday"

        conflict_response = client.put(
            f"/api/v1/books/{book_ids[1]}/reading-plan",
            json={"pace": 1, "schedule_config": ["Mon"], "reminder_time": "20:00"},
        )
        assert conflict_response.status_code == 409
        assert "Thứ hai lúc 20:00" in conflict_response.json()["detail"]

        with Session(engine) as session:
            active_slots_b = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.book_id == book_ids[1],
                    ReadingPlanScheduleSlot.is_active.is_(True),
                )
            ).all()
            assert len(active_slots_b) == 1
            assert active_slots_b[0].weekday == 2
            assert active_slots_b[0].reminder_time == "21:00"
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_resume_inactive_plan_rejects_processing_book(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book = Book(user_id=user_id, title="Processing Deferred Book", status=BookStatus.PROCESSING)
            session.add(book)
            session.commit()
            session.refresh(book)
            book_id = book.id

            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.INACTIVE.value,
                reminder_time="21:00",
            )
            session.add(plan)
            session.commit()

        response = client.post(f"/api/v1/books/{book_id}/resume")

        assert response.status_code == 409
        assert "Tài liệu chưa sẵn sàng" in response.json()["detail"]
        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.INACTIVE.value
            slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.book_id == book_id)).all()
            assert slots == []
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_resume_inactive_plan_detects_conflict_without_activating(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            active_book, _, _ = _create_playable_book(session, user_id=user_id, title="Resume Conflict Active")
            inactive_book, _, _ = _create_playable_book(session, user_id=user_id, title="Resume Conflict Deferred")
            book_ids = [active_book.id, inactive_book.id]

            active_plan = ReadingPlan(
                book_id=active_book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            inactive_plan = ReadingPlan(
                book_id=inactive_book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.INACTIVE.value,
                reminder_time="20:00",
            )
            session.add(active_plan)
            session.add(inactive_plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=active_book.id, plan_id=active_plan.id, slots=slots))
            inactive_slots = validate_plan_schedule_shape(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
            session.add_all(
                build_slots_for_plan(
                    user_id=user_id,
                    book_id=inactive_book.id,
                    plan_id=inactive_plan.id,
                    slots=inactive_slots,
                    is_active=False,
                )
            )
            session.commit()

        response = client.post(f"/api/v1/books/{book_ids[1]}/resume")

        assert response.status_code == 409
        assert "Thứ hai lúc 20:00" in response.json()["detail"]
        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_ids[1])).first()
            assert db_plan.status == PlanStatus.INACTIVE.value
            slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.book_id == book_ids[1])).all()
            assert len(slots) == 1
            assert slots[0].is_active is False
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_resume_inactive_plan_success_is_idempotent(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Resume Success Deferred")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.INACTIVE.value,
                reminder_time="21:00",
            )
            session.add(plan)
            session.flush()
            slots = validate_plan_schedule_shape(session, user_id=user_id, schedule_config=["Tue"], reminder_time="21:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots, is_active=False))
            session.commit()

        first = client.post(f"/api/v1/books/{book_id}/resume")
        second = client.post(f"/api/v1/books/{book_id}/resume")

        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json()["plan_status"] == PlanStatus.ACTIVE.value
        assert second.json()["plan_status"] == PlanStatus.ACTIVE.value

        with Session(engine) as session:
            active_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.book_id == book_id,
                    ReadingPlanScheduleSlot.is_active.is_(True),
                )
            ).all()
            assert len(active_slots) == 1
            assert active_slots[0].weekday == 1
            assert active_slots[0].reminder_time == "21:00"
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_update_inactive_plan_does_not_validate_active_conflict(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            active_book, _, _ = _create_playable_book(session, user_id=user_id, title="Update Inactive Active")
            inactive_book, _, _ = _create_playable_book(session, user_id=user_id, title="Update Inactive Deferred")
            book_ids = [active_book.id, inactive_book.id]

            active_plan = ReadingPlan(
                book_id=active_book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            inactive_plan = ReadingPlan(
                book_id=inactive_book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.INACTIVE.value,
                reminder_time="21:00",
            )
            session.add(active_plan)
            session.add(inactive_plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Mon"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=active_book.id, plan_id=active_plan.id, slots=slots))
            session.commit()

        response = client.put(
            f"/api/v1/books/{book_ids[1]}/reading-plan",
            json={"schedule_config": ["Mon"], "reminder_time": "20:00"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["plan_status"] == PlanStatus.INACTIVE.value
        assert body["schedule_config"] == ["Mon"]
        assert body["reminder_time"] == "20:00"
        assert body["active_slots"] == []
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_plan_marks_completed_on_100_percent():
    client = TestClient(app)
    user_id = MOCK_USER_ID
    book_id = None
    try:
        with Session(engine) as session:
            # Clean up any leftover plans/slots to avoid schedule conflict errors
            session.execute(text("DELETE FROM reading_plan_schedule_slots WHERE user_id = :uid"), {"uid": user_id})
            session.execute(text("DELETE FROM reading_plans WHERE book_id IN (SELECT id FROM books WHERE user_id = :uid)"), {"uid": user_id})
            session.commit()
            book, unit, _ = _create_playable_book(session, user_id=user_id, title="Auto Complete Book")
            book_id = book.id
            unit_id = unit.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        # Complete learning unit
        resp_complete = client.post(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/complete",
            json={"mode": "full"},
        )
        assert resp_complete.status_code == 200

        with Session(engine) as session:
            db_plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
            assert db_plan.status == PlanStatus.COMPLETED.value
            assert db_plan.completed_at is not None
            state = session.exec(select(BookLearningState).where(BookLearningState.book_id == book_id)).first()
            assert state is not None
            assert state.status == "completed"
            assert state.book_progress_percent == 100
            assert state.completed_at is not None
            all_slots = session.exec(
                select(ReadingPlanScheduleSlot).where(
                    ReadingPlanScheduleSlot.plan_id == db_plan.id,
                )
            ).all()
            assert len(all_slots) == 1
            assert all_slots[0].is_active is False
    finally:
        if book_id:
            _delete_book(book_id)


def test_completed_book_progress_detail_and_review_access():
    client = TestClient(app)
    user_id = MOCK_USER_ID
    book_id = None
    try:
        with Session(engine) as session:
            book, unit, _ = _create_playable_book(session, user_id=user_id, title="Completed UX Book")
            book_id = book.id
            unit_id = unit.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

        complete_response = client.post(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/complete",
            json={"mode": "full"},
        )
        assert complete_response.status_code == 200

        progress_response = client.get(f"/api/v1/books/{book_id}/learning-progress?mode=full")
        assert progress_response.status_code == 200
        progress_body = progress_response.json()
        assert progress_body["learning_status"] == "completed"
        assert progress_body["is_completed"] is True
        assert progress_body["can_resume"] is False
        assert progress_body["can_review"] is True
        assert progress_body["completed_at"] is not None

        detail_response = client.get(f"/api/v1/books/{book_id}/details?mode=full")
        assert detail_response.status_code == 200
        detail_summary = detail_response.json()["learning_summary"]
        assert detail_summary["learning_status"] == "completed"
        assert detail_summary["book_progress_percent"] == 100

        resume_response = client.post(f"/api/v1/books/{book_id}/resume")
        assert resume_response.status_code == 409
        assert "Sách đã hoàn thành" in resume_response.json()["detail"]

        reviews_response = client.get(f"/api/v1/books/{book_id}/reviews?status=upcoming&mode=full")
        assert reviews_response.status_code == 200
        reviews_body = reviews_response.json()
        assert reviews_body["total"] == 1
        assert reviews_body["items"][0]["book_id"] == str(book_id)
        assert reviews_body["items"][0]["learning_unit_id"] == str(unit_id)
    finally:
        if book_id:
            _delete_book(book_id)


def test_plan_update_accepts_partial_payload_without_breaking_contract(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _, _ = _create_playable_book(session, user_id=user_id, title="Partial Update Plan Book")
            book_id = book.id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=3,
                status=PlanStatus.ACTIVE.value,
                reminder_time="20:00",
            )
            session.add(plan)
            session.commit()

            slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=["Sat"], reminder_time="20:00")
            session.add_all(build_slots_for_plan(user_id=user_id, book_id=book.id, plan_id=plan.id, slots=slots))
            session.commit()

        response = client.put(
            f"/api/v1/books/{book_id}/reading-plan",
            json={"reminder_time": "08:00"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["pace"] == 3
        assert body["schedule_config"] == ["Sat"]
        assert body["reminder_time"] == "08:00"
        assert body["active_slots"][0]["weekday_label"] == "saturday"
        assert body["active_slots"][0]["reminder_time"] == "08:00"
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)

