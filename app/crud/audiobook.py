import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan

# ---------------------------------------------------------------------------
# Book
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Chapter
# ---------------------------------------------------------------------------


def create_chapter(session: Session, chapter: Chapter) -> Chapter:
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.review_audio_url = review_audio_url
        session.add(chapter)
        session.commit()


def update_chapter_status(session: Session, chapter_id: uuid.UUID, status: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.status = status
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()


# ---------------------------------------------------------------------------
# ChapterSegment
# ---------------------------------------------------------------------------


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    for segment in segments:
        session.add(segment)
    session.commit()


# ---------------------------------------------------------------------------
# ReadingPlan
# ---------------------------------------------------------------------------


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


# ---------------------------------------------------------------------------
# Chapter (thêm helpers)
# ---------------------------------------------------------------------------


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.review_text = review_text
        session.add(chapter)
        session.commit()


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = (
        select(Chapter)
        .where(Chapter.book_id == book_id)
        .order_by(Chapter.chapter_index)
    )
    return list(session.exec(statement).all())

