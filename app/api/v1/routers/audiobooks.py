import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.api.dependencies.auth import get_current_user
from app.db.database import get_session
from app.models.db_models import Book
from app.repositories import audiobook_repo
from app.schemas.plan import SwitchModeRequest
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.schemas.user import UserTokenPayload
from app.services.audiobook_service import get_book_details, switch_book_mode

router = APIRouter()


@router.get("/books", response_model=list[BookResponse])
def read_all_books(session: Annotated[Session, Depends(get_session)], current_user: UserTokenPayload = Depends(get_current_user) ):
    print(f"Current user: {current_user.email} (ID: {current_user.sub})")  # Debug log để xem thông tin user
    return audiobook_repo.get_audiobooks(session)


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.get_book_by_id(session, book_id)


@router.post("/books", response_model=BookResponse)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.create_book(session, book)


@router.delete("/book/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await audiobook_repo.delete_book_storage(session, book_id)
    return {"message": "Book deleted"}


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_details(session, book_id)


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, background_tasks, book_id, payload.mode)
