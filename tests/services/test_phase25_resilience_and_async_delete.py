import uuid
import pytest
from sqlmodel import Session, delete

from app.db.database import engine, _connect_args_for
from app.models.db_models import Book
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


def test_get_book_details_graceful_fallback():
    """Verify that get_book_details returns HTTP 200 payload structure with learning_summary=None
    when a book has no active ReadingPlan.
    """
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()

    with Session(engine) as session:
        book = Book(id=book_id, user_id=user_id, title="Test Graceful Fallback Book", total_sections=10)
        session.add(book)
        session.commit()

        res = get_book_details(session, book_id, user_id, mode="pareto")

        assert res["book_id"] == book_id
        assert res["learning_summary"] is None
        assert res["total_units"] == 0
        assert res["units"] == []
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
