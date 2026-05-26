import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    ChapterProgressResponse,
    ChapterProgressUpdateRequest,
    ManualChapterCompleteRequest,
)
from app.services.learning_progress_service import complete_chapter_manually, get_book_learning_progress, update_chapter_progress

router = APIRouter()


@router.put("/books/{book_id}/chapters/{chapter_id}/progress", response_model=ChapterProgressResponse)
def update_chapter_progress_endpoint(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    payload: ChapterProgressUpdateRequest,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
):
    return update_chapter_progress(session, user_id=current_user.sub, book_id=book_id, chapter_id=chapter_id, payload=payload)


@router.post("/books/{book_id}/chapters/{chapter_id}/complete", response_model=ChapterProgressResponse)
def complete_chapter_endpoint(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    payload: ManualChapterCompleteRequest,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
):
    return complete_chapter_manually(session, user_id=current_user.sub, book_id=book_id, chapter_id=chapter_id, mode=payload.mode)


@router.get("/books/{book_id}/learning-progress", response_model=BookLearningProgressResponse)
def get_book_learning_progress_endpoint(
    book_id: uuid.UUID,
    mode: str,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
):
    return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
