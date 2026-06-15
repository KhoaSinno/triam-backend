import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import BookLearningStatus, BookStatus, PlanMode, PlanStatus, ReviewItemStatus
from app.db.database import engine
from app.main import app
from app.models.db_models import Book, BookLearningState, ReadingPlan, SpacedReviewItem
from app.repositories.spaced_review_repo import count_review_items_for_user


def _delete_book(book_id: uuid.UUID) -> None:
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()


def test_list_books_reads_cached_learning_state_without_sync(auth_as):
    client = TestClient(app)
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id: uuid.UUID | None = None
    try:
        with Session(engine) as session:
            book = Book(user_id=user_id, title="Phase 14.4 Cached Library Book", status=BookStatus.READY.value)
            session.add(book)
            session.flush()
            session.add(
                ReadingPlan(
                    book_id=book.id,
                    mode=PlanMode.FULL,
                    pace=1,
                    status=PlanStatus.ACTIVE.value,
                    reminder_time="20:00",
                )
            )
            session.add(
                BookLearningState(
                    user_id=user_id,
                    book_id=book.id,
                    mode=PlanMode.FULL,
                    status=BookLearningStatus.IN_PROGRESS.value,
                    book_progress_percent=64,
                    completed_units=1,
                    playable_units=2,
                    position_ms=12000,
                )
            )
            session.commit()
            book_id = book.id

        response = client.get("/api/v1/books")

        assert response.status_code == 200
        body = response.json()
        target = next(item for item in body if item["id"] == str(book_id))
        assert target["learning_status"] == BookLearningStatus.IN_PROGRESS.value
        assert target["book_progress_percent"] == 64
    finally:
        if book_id:
            _delete_book(book_id)


def test_review_count_uses_sql_count_without_legacy_limit(auth_as):
    user_id = uuid.uuid4()
    auth_as(user_id)
    book_id: uuid.UUID | None = None
    now = datetime.now(timezone.utc)
    try:
        with Session(engine) as session:
            book = Book(user_id=user_id, title="Phase 14.4 Count Book", status=BookStatus.READY.value)
            session.add(book)
            session.flush()
            book_id = book.id
            session.add_all(
                [
                    SpacedReviewItem(
                        user_id=user_id,
                        book_id=book.id,
                        mode=PlanMode.FULL,
                        interval_days=1,
                        sequence_index=index,
                        due_at=now - timedelta(minutes=1),
                        status=ReviewItemStatus.PENDING,
                        review_text_snapshot="Review item",
                    )
                    for index in range(1005)
                ]
            )
            session.commit()

            assert (
                count_review_items_for_user(
                    session,
                    user_id=user_id,
                    now=now,
                    status_filter="due",
                    book_id=book.id,
                    mode=PlanMode.FULL,
                )
                == 1005
            )
    finally:
        if book_id:
            _delete_book(book_id)
