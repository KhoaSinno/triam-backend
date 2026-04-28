import uuid
from typing import Optional

from sqlmodel import Session, select

from app.core.supabase import supabase
from app.models.db_models import Book


def get_audiobooks(session: Session) -> list[Book]:
    return session.exec(select(Book)).all()


def get_book_by_id(session: Session, book_id: uuid.UUID) -> Optional[Book]:
    return session.get(Book, book_id)


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


def delete_book(session: Session, book_id: uuid.UUID) -> None:
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


async def delete_book_storage(session: Session, book_id: uuid.UUID):
    """
    Xóa sạch assets trong Storage và bản ghi trong Database.
    """
    str_book_id = str(book_id)
    target_buckets = ["audios", "raw_books"]

    try:
        # 1. Lấy danh sách file từ tất cả bucket liên quan qua RPC (SELECT)
        result = supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute()

        # 2. Phân loại và xóa file qua Storage API
        if result.data:
            for bucket in target_buckets:
                # Lọc ra danh sách file thuộc bucket hiện tại
                paths = [item["name"] for item in result.data if item["bucket_id"] == bucket]

                if paths:
                    # Xóa hàng loạt file trong bucket này (Đúng quy trình API)
                    supabase.storage.from_(bucket).remove(paths)
                    print(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # 3. Xóa record trong DB
        # Lưu ý: CASCADE (Alembic) sẽ tự động xóa các bảng liên quan
        # (chapters, book_knowledge...) khi lệnh commit chạy.
        delete_book(session, book_id)
        print(f"Đã dọn dẹp sạch sẽ database cho book: {str_book_id}")

    except Exception as e:
        # Rollback session nếu có lỗi ở tầng DB để tránh mất dữ liệu không đồng bộ
        session.rollback()
        print(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise e
