import json
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


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_audio = json.loads(chapter.review_audio_url) if chapter.review_audio_url else {}
        except:
            # Fallback nếu data cũ là string thường
            reviews_audio = {"full": chapter.review_audio_url} if chapter.review_audio_url else {}

        reviews_audio[mode] = review_audio_url
        chapter.review_audio_url = json.dumps(reviews_audio, ensure_ascii=False)
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
            reviews_text = json.loads(chapter.review_text) if chapter.review_text else {}
        except:
            # Fallback nếu data cũ là string thường
            reviews_text = {"full": chapter.review_text} if chapter.review_text else {}

        reviews_text[mode] = review_text
        chapter.review_text = json.dumps(reviews_text, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()
