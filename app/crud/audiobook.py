from sqlmodel import Session, select

from app.models.db_models import Book


def get_audiobooks(session: Session):
    # Lấy danh sách tất cả sách
    return session.exec(select(Book)).all()


def create_audiobook(session: Session, book: Book):
    # Lưu một cuốn sách mới vào Supabase
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
