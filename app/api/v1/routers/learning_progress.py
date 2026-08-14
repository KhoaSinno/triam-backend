import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    LearningUnitProgressResponse,
    LearningUnitProgressUpdateRequest,
    ManualLearningUnitCompleteRequest,
)
from app.services.learning_progress_service import complete_learning_unit_manually, get_book_learning_progress, update_learning_unit_progress
from app.services.sync_event_service import record_event

router = APIRouter()


@router.put("/books/{book_id}/learning-units/{learning_unit_id}/progress", response_model=LearningUnitProgressResponse)
def update_learning_unit_progress_endpoint(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: LearningUnitProgressUpdateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    response = update_learning_unit_progress(session, user_id=current_user.sub, book_id=book_id, learning_unit_id=learning_unit_id, payload=payload)
    record_event(session, user_id=current_user.sub, domain="progress", entity_id=learning_unit_id, operation="update")
    session.commit()
    return response


@router.post("/books/{book_id}/learning-units/{learning_unit_id}/complete", response_model=LearningUnitProgressResponse)
def complete_learning_unit_endpoint(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: ManualLearningUnitCompleteRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    response = complete_learning_unit_manually(session, user_id=current_user.sub, book_id=book_id, learning_unit_id=learning_unit_id, mode=payload.mode)
    record_event(session, user_id=current_user.sub, domain="progress", entity_id=learning_unit_id, operation="update")
    session.commit()
    return response


@router.get("/books/{book_id}/learning-progress", response_model=BookLearningProgressResponse)
def get_book_learning_progress_endpoint(
    book_id: uuid.UUID,
    mode: str,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)
