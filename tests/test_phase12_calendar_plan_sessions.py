import uuid
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.constant import BookStatus, PlanMode, PlanStatus, ProcessingJobStatus, ReadingPlanSessionStatus
from app.db.database import engine
from app.main import app
from app.models.db_models import (
    Book,
    LearningUnit,
    LearningUnitSegment,
    NotificationSettings,
    ReadingPlan,
    ReadingPlanSession,
    ReadingPlanSessionUnit,
)
from app.services.reading_plan_schedule_service import build_slots_for_plan, validate_plan_schedule_shape

WEEKDAY_INPUTS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _weekday_input_for(local_dt: datetime) -> str:
    return WEEKDAY_INPUTS[local_dt.weekday()]


def _add_inactive_plan_slots(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, plan: ReadingPlan, schedule_config: list[str]) -> None:
    slots = validate_plan_schedule_shape(session, user_id=user_id, schedule_config=schedule_config, reminder_time=plan.reminder_time)
    for slot in build_slots_for_plan(user_id=user_id, book_id=book_id, plan_id=plan.id, slots=slots, is_active=False):
        session.add(slot)


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


def _create_playable_book_with_units(
    session: Session,
    *,
    user_id: uuid.UUID,
    total_units: int = 3,
    title: str = "Phase 12 Calendar Book",
) -> tuple[Book, list[LearningUnit]]:
    book = Book(
        user_id=user_id,
        title=title,
        total_units=total_units,
        status=BookStatus.READY.value,
    )
    session.add(book)
    session.flush()

    units: list[LearningUnit] = []
    for index in range(total_units):
        unit = LearningUnit(
            user_id=user_id,
            book_id=book.id,
            mode=PlanMode.FULL,
            unit_index=index,
            title=f"Unit {index + 1}",
            unit_type="full",
            status=ProcessingJobStatus.READY,
            review_text=f"Review unit {index + 1}",
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
                audio_url=f"https://example.test/audio-{index}.mp3",
                text_content=f"Learning content {index}",
                duration_ms=100000,
            )
        )
        units.append(unit)

    session.commit()
    session.refresh(book)
    for unit in units:
        session.refresh(unit)
    return book, units


def test_resume_plan_creates_calendar_sessions_and_today_query(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _units = _create_playable_book_with_units(session, user_id=user_id, total_units=3)
            book_id = book.id
            local_target = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")) + timedelta(days=1)
            weekday = _weekday_input_for(local_target)
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=2,
                status=PlanStatus.INACTIVE.value,
                reminder_time="08:00",
            )
            session.add(plan)
            session.flush()
            _add_inactive_plan_slots(session, user_id=user_id, book_id=book.id, plan=plan, schedule_config=[weekday])
            session.commit()

        response = client.post(f"/api/v1/books/{book_id}/resume")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == PlanStatus.ACTIVE.value
        assert body["session_summary"]["total_sessions"] == 2
        assert body["session_summary"]["next_session"]["total_units"] == 2

        sessions_response = client.get(f"/api/v1/books/{book_id}/reading-plan/sessions?mode=full")
        assert sessions_response.status_code == 200
        sessions_body = sessions_response.json()
        assert sessions_body["total"] == 2
        assert [len(item["units"]) for item in sessions_body["items"]] == [2, 1]

        first_local_date = sessions_body["items"][0]["local_date"]
        today_response = client.get(f"/api/v1/reading-plan/sessions/today?local_date={first_local_date}")
        assert today_response.status_code == 200
        today_body = today_response.json()
        assert today_body["local_date"] == first_local_date
        assert today_body["total"] == 1
        assert today_body["items"][0]["book_id"] == str(book_id)
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_list_books_keeps_book_fields_after_learning_summary_commit(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_ids: list[uuid.UUID] = []
    try:
        with Session(engine) as session:
            progress_targets: list[tuple[uuid.UUID, uuid.UUID, int]] = []
            for index in range(2):
                book, units = _create_playable_book_with_units(session, user_id=user_id, total_units=1, title=f"Phase 12 List Books Book {index + 1}")
                book_ids.append(book.id)
                unit_id = units[0].id
                segment = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id == unit_id)).first()
                progress_targets.append((book.id, unit_id, segment.id))
                session.add(
                    ReadingPlan(
                        book_id=book.id,
                        mode=PlanMode.FULL,
                        pace=1,
                        status=PlanStatus.ACTIVE.value,
                        reminder_time="08:00",
                    )
                )
            session.commit()

        for book_id, unit_id, segment_id in progress_targets:
            progress_response = client.put(
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
            assert progress_response.status_code == 200

        response = client.get("/api/v1/books")
        assert response.status_code == 200
        response_books = {item["id"]: item for item in response.json()}
        for index, book_id in enumerate(book_ids):
            book = response_books[str(book_id)]
            assert book["title"] == f"Phase 12 List Books Book {index + 1}"
            assert book["created_at"] is not None
            assert book["updated_at"] is not None
            assert book["learning_status"] == "in_progress"
            assert book["book_progress_percent"] == 50
    finally:
        for book_id in book_ids:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_learning_completion_marks_missed_session_completed(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    unit_id = None
    try:
        with Session(engine) as session:
            book, units = _create_playable_book_with_units(session, user_id=user_id, total_units=1, title="Phase 12 Catch Up Book")
            book_id = book.id
            unit_id = units[0].id
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=1,
                status=PlanStatus.ACTIVE.value,
                reminder_time="08:00",
            )
            session.add(plan)
            session.flush()

            scheduled_at = datetime.now(timezone.utc) - timedelta(days=1)
            plan_session = ReadingPlanSession(
                user_id=user_id,
                plan_id=plan.id,
                book_id=book.id,
                mode=PlanMode.FULL,
                session_index=0,
                scheduled_at=scheduled_at,
                local_date=scheduled_at.astimezone(ZoneInfo("Asia/Ho_Chi_Minh")).date().isoformat(),
                reminder_time="08:00",
                timezone="Asia/Ho_Chi_Minh",
                status=ReadingPlanSessionStatus.SCHEDULED.value,
                total_units=1,
            )
            session.add(plan_session)
            session.flush()
            session.add(
                ReadingPlanSessionUnit(
                    session_id=plan_session.id,
                    plan_id=plan.id,
                    book_id=book.id,
                    learning_unit_id=units[0].id,
                    unit_order=0,
                )
            )
            session.commit()

        sessions_response = client.get(f"/api/v1/books/{book_id}/reading-plan/sessions")
        assert sessions_response.status_code == 200
        assert sessions_response.json()["items"][0]["status"] == ReadingPlanSessionStatus.MISSED.value

        complete_response = client.post(
            f"/api/v1/books/{book_id}/learning-units/{unit_id}/complete",
            json={"mode": "full"},
        )
        assert complete_response.status_code == 200

        with Session(engine) as session:
            db_session = session.exec(select(ReadingPlanSession).where(ReadingPlanSession.book_id == book_id)).first()
            assert db_session.status == ReadingPlanSessionStatus.COMPLETED.value
            assert db_session.completed_units == 1
            assert db_session.completed_at is not None
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)


def test_update_active_plan_regenerates_unfinished_sessions(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id = None
    try:
        with Session(engine) as session:
            book, _units = _create_playable_book_with_units(session, user_id=user_id, total_units=4, title="Phase 12 Update Book")
            book_id = book.id
            local_target = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")) + timedelta(days=1)
            weekday = _weekday_input_for(local_target)
            plan = ReadingPlan(
                book_id=book.id,
                mode=PlanMode.FULL,
                pace=2,
                status=PlanStatus.INACTIVE.value,
                reminder_time="08:00",
            )
            session.add(plan)
            session.flush()
            _add_inactive_plan_slots(session, user_id=user_id, book_id=book.id, plan=plan, schedule_config=[weekday])
            session.commit()

        resume_response = client.post(f"/api/v1/books/{book_id}/resume")
        assert resume_response.status_code == 200

        with Session(engine) as session:
            before_ids = {
                item.id
                for item in session.exec(
                    select(ReadingPlanSession).where(
                        ReadingPlanSession.book_id == book_id,
                        ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value,
                    )
                ).all()
            }
            assert len(before_ids) == 2

        update_response = client.put(
            f"/api/v1/books/{book_id}/reading-plan",
            json={"pace": 1, "schedule_config": [weekday], "reminder_time": "09:00"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["session_summary"]["total_sessions"] == 4

        with Session(engine) as session:
            all_sessions = session.exec(select(ReadingPlanSession).where(ReadingPlanSession.book_id == book_id)).all()
            cancelled_ids = {item.id for item in all_sessions if item.status == ReadingPlanSessionStatus.CANCELLED.value}
            active_ids = {item.id for item in all_sessions if item.status != ReadingPlanSessionStatus.CANCELLED.value}
            assert before_ids <= cancelled_ids
            assert len(active_ids) == 4
            assert all(item.reminder_time == "09:00" for item in all_sessions if item.id in active_ids)
    finally:
        if book_id:
            _delete_book(book_id)
        _delete_notification_settings(user_id)
