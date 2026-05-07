import json
import uuid

from fastapi import HTTPException
from sqlmodel import Session, col, select

from app.core.logger import log
from app.models.db_models import Chapter


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = select(Chapter).where(Chapter.book_id ==
                                      book_id).order_by(col(Chapter.chapter_index))
    return list(session.exec(statement).all())


def create_chapter(session: Session, chapter: Chapter) -> Chapter:
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_audio = json.loads(
                chapter.review_audio_url) if chapter.review_audio_url else {}
        except (json.JSONDecodeError, TypeError) as e:
            log.error(f"Data integrity error: {e}")
            raise HTTPException(
                status_code=500, detail="Data integrity error") from e

        reviews_audio[mode] = review_audio_url
        chapter.review_audio_url = json.dumps(
            reviews_audio, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def update_chapter_status(session: Session, chapter_id: uuid.UUID, status: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.status = status
        session.add(chapter)
        session.commit()


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_text = json.loads(
                chapter.review_text) if chapter.review_text else {}
        except (json.JSONDecodeError, TypeError) as e:
            log.error(f"Data integrity error: {e}")
            raise HTTPException(
                status_code=500, detail="Data integrity error") from e

        reviews_text[mode] = review_text
        chapter.review_text = json.dumps(reviews_text, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()
