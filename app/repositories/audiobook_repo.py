import uuid
import asyncio
from typing import Optional

from sqlalchemy import or_
from sqlmodel import Session, col, delete, select

from app.core.exceptions import BookNotFoundError, StorageOperationError
from app.core.logger import log
from app.core.supabase import supabase
from app.models.db_models import Book, NotificationOutbox, UserNotification
from app.schemas.audiobook import BookUpdateRequest


def get_audiobooks(session: Session) -> list[Book]:
    return list(session.exec(select(Book)).all())


def get_audiobooks_by_user(session: Session, user_id: uuid.UUID) -> list[Book]:
    return list(session.exec(select(Book).where(Book.user_id == user_id)).all())


def get_book_by_id(session: Session, book_id: uuid.UUID) -> Optional[Book]:
    return session.get(Book, book_id)


def get_book_by_id_and_user(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Book]:
    return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()


def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def update_book_status(session: Session, book_id: uuid.UUID, status: str, error_message: Optional[str] = None) -> None:
    book = session.get(Book, book_id)
    if book:
        book.status = status
        if error_message is not None:
            book.error_message = error_message
        session.add(book)
        session.commit()


def update_book_by_id(session: Session, book_data: BookUpdateRequest, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def delete_book(session: Session, book_id: uuid.UUID) -> None:
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


def cleanup_book_side_effects(session: Session, *, book_id: uuid.UUID, user_id: uuid.UUID) -> None:
    book_id_str = str(book_id)

    outbox_filter = or_(
        NotificationOutbox.payload.contains({"book_id": book_id_str}),
        NotificationOutbox.payload.contains({"action_payload": {"book_id": book_id_str}}),
    )

    outbox_ids = list(session.exec(select(NotificationOutbox.id).where(NotificationOutbox.user_id == user_id, outbox_filter)).all())

    user_notification_filter = UserNotification.action_payload.contains({"book_id": book_id_str})

    if outbox_ids:
        user_notification_filter = or_(
            UserNotification.action_payload.contains({"book_id": book_id_str}),
            col(UserNotification.outbox_id).in_(outbox_ids),
        )

    session.exec(delete(UserNotification).where(UserNotification.user_id == user_id, user_notification_filter))
    if outbox_ids:
        session.exec(
            delete(NotificationOutbox).where(
                NotificationOutbox.user_id == user_id,
                col(NotificationOutbox.id).in_(outbox_ids),
            )
        )

    session.flush()


async def delete_book_storage(session: Session, book_id: uuid.UUID, user_id: uuid.UUID):
    """
    Xóa bản ghi trong Database ngay lập tức (Synchronous - < 50ms) và đẩy nhiệm vụ xóa file
    trên Supabase Storage sang Celery Worker chạy ngầm (Asynchronous).
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)
    is_clone = book.parent_shared_id is not None

    # 1. Dọn dẹp các bảng phụ thuộc & Xóa bản ghi trong Postgres DB
    cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
    delete_book(session, book_id)
    log.info(f"Fast DB delete complete for book: {str_book_id}")

    # 2. Đẩy nhiệm vụ xóa file vật lý trên Storage cho Celery Worker (chỉ với sách tự upload)
    if not is_clone:
        try:
            from app.tasks.book_tasks import purge_book_storage_assets_task

            purge_book_storage_assets_task.delay(str_book_id)
            log.info(f"Dispatched background storage purge task for book: {str_book_id}")
        except Exception as exc:
            log.warning(f"Failed to dispatch purge task (will rely on periodic cleanup): {exc}")

