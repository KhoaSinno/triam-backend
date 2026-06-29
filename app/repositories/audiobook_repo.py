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
    Xóa assets vật lý trên Storage (chỉ áp dụng cho sách tự upload)
    và dọn dẹp sạch bản ghi metadata trong Database.
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)

    # Logic CLone book
    if book.parent_shared_id is not None:
        log.info(f"Book {str_book_id} là sách clone. Bỏ qua bước xóa file vật lý trên Storage.")
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Clear Clone Book: {str_book_id}")
        return

    # --- Normal logic DEL Book + Related object + Storage object ---
    target_buckets = ["audios", "raw_books"]
    try:
        # Lấy danh sách file từ tất cả bucket liên quan qua RPC
        result = await asyncio.to_thread(
            supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute
        )

        # Xóa file vật lý qua Storage API
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    await asyncio.to_thread(supabase.storage.from_(bucket).remove, paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # Xóa record trong DB
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch database cho book tự upload: {str_book_id}")

    except Exception as e:
        session.rollback()
        log.exception(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise StorageOperationError("Không thể xóa tài nguyên sách trong Storage.") from e

