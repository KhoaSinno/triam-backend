import uuid

import pytest
from sqlmodel import Session, delete

from app.core.constant import PlanMode, ProcessingJobStatus
from app.db.database import _connect_args_for, engine
from app.models.db_models import Book, LearningUnit, LearningUnitSegment
from app.repositories.audiobook_repo import delete_book_storage
from app.services.audiobook_service import get_book_details


def test_db_connect_args_keepalives():
    """Verify that _connect_args_for correctly includes PostgreSQL TCP keepalives."""
    pg_url = "postgresql://user:pass@localhost:5432/dbname"
    args = _connect_args_for(pg_url)

    assert "keepalives" in args
    assert args["keepalives"] == 1
    assert args["keepalives_idle"] == 30
    assert args["keepalives_interval"] == 10
    assert args["keepalives_count"] == 5
    assert args.get("application_name") == "triam-backend"


def test_get_book_details_returns_cloned_units_without_reading_plan():
    """A clone can expose its ready audio before its owner creates a ReadingPlan."""
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()

    with Session(engine) as session:
        book = Book(id=book_id, user_id=user_id, title="Test Graceful Fallback Book", total_sections=10)
        unit = LearningUnit(
            user_id=user_id,
            book_id=book_id,
            mode=PlanMode.PARETO,
            unit_index=0,
            title="Pareto unit",
            unit_type="pareto",
            status=ProcessingJobStatus.READY,
        )
        session.add(book)
        session.add(unit)
        session.flush()
        session.add(LearningUnitSegment(learning_unit_id=unit.id, segment_index=0, audio_url="https://example.test/unit.mp3"))
        session.commit()

        res = get_book_details(session, book_id, user_id, mode="pareto")

        assert res["book_id"] == book_id
        assert res["learning_summary"] is None
        assert res["total_units"] == 1
        assert res["units"][0]["id"] == str(unit.id)
        assert res["units"][0]["segments"][0]["audio_url"] == "https://example.test/unit.mp3"
        assert res["mode"] == "pareto"

        # Cleanup
        session.execute(delete(Book).where(Book.id == book_id))
        session.commit()


@pytest.mark.asyncio
async def test_fast_delete_book():
    """Verify that delete_book_storage performs fast synchronous DB deletion
    without throwing errors or blocking on external storage requests.
    """
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()

    with Session(engine) as session:
        book = Book(id=book_id, user_id=user_id, title="Test Fast Delete Book")
        session.add(book)
        session.commit()

        await delete_book_storage(session, book_id, user_id)

        # Book must be removed from DB immediately
        deleted_book = session.get(Book, book_id)
        assert deleted_book is None
