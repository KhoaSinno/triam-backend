import uuid

from sqlmodel import Session, select

from app.models.db_models import Chapter


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)
    return list(session.exec(statement).all())


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


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.review_text = review_text
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()
