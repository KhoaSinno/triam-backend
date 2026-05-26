import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import BookStatus, NotificationType
from app.db.database import engine
from app.main import app
from app.models.db_models import Book, ChatThread, StudyContext, UserNotification


def test_books_are_scoped_to_current_user(auth_as):
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()
    book_ids: list[uuid.UUID] = []

    with Session(engine) as session:
        book_a = Book(user_id=user_a, title="User A Book", status=BookStatus.DRAFT, total_chapters=0)
        book_b = Book(user_id=user_b, title="User B Book", status=BookStatus.DRAFT, total_chapters=0)
        session.add(book_a)
        session.add(book_b)
        session.commit()
        session.refresh(book_a)
        session.refresh(book_b)
        book_ids.extend([book_a.id, book_b.id])

    try:
        auth_as(user_a)
        client = TestClient(app)

        list_response = client.get("/api/v1/books")
        assert list_response.status_code == 200
        returned_ids = {item["id"] for item in list_response.json()}
        assert str(book_ids[0]) in returned_ids
        assert str(book_ids[1]) not in returned_ids

        read_other_response = client.get(f"/api/v1/books/{book_ids[1]}")
        assert read_other_response.status_code == 404

        update_other_response = client.put(f"/api/v1/books/{book_ids[1]}", json={"title": "Should Not Update"})
        assert update_other_response.status_code == 404
    finally:
        with Session(engine) as session:
            for book_id in book_ids:
                book = session.get(Book, book_id)
                if book:
                    session.delete(book)
            session.commit()


def test_notifications_are_scoped_to_current_user(auth_as):
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()
    notification_id = uuid.uuid4()

    with Session(engine) as session:
        session.add(
            UserNotification(
                id=notification_id,
                user_id=user_b,
                type=NotificationType.CONTENT_READY,
                title="Private notification",
                body="Only user B can read this.",
                action_type="open_book",
                action_payload={"book_id": str(uuid.uuid4())},
            )
        )
        session.commit()

    try:
        auth_as(user_a)
        client = TestClient(app)

        list_response = client.get("/api/v1/notifications?limit=20")
        assert list_response.status_code == 200
        assert all(item["id"] != str(notification_id) for item in list_response.json()["items"])

        read_response = client.patch(f"/api/v1/notifications/{notification_id}/read")
        assert read_response.status_code == 404
    finally:
        with Session(engine) as session:
            notification = session.get(UserNotification, notification_id)
            if notification:
                session.delete(notification)
                session.commit()


def test_livekit_thread_token_requires_thread_owner(auth_as):
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()
    context_id: uuid.UUID | None = None

    with Session(engine) as session:
        context = StudyContext(user_id=user_b, title="Private context")
        session.add(context)
        session.flush()
        thread = ChatThread(context_id=context.id, title="Private thread")
        session.add(thread)
        session.commit()
        session.refresh(context)
        session.refresh(thread)
        context_id = context.id
        thread_id = thread.id

    try:
        auth_as(user_a)
        client = TestClient(app)

        token_response = client.get(f"/api/v1/live-token/thread/{thread_id}")
        assert token_response.status_code == 404
    finally:
        with Session(engine) as session:
            if context_id:
                context = session.get(StudyContext, context_id)
                if context:
                    session.delete(context)
                    session.commit()
