import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.models.db_models import Book
from app.schemas.audiobook import BookInput
from app.schemas.plan import SwitchModeRequest
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.services.audiobook_service import (
    create_new_book,
    delete_book_and_assets,
    get_book,
    get_book_details,
    list_books,
    switch_book_mode,
    update_book_by_id
)

router = APIRouter()


# @router.get("/books", response_model=list[BookResponse])
# def read_all_books(session: Annotated[Session, Depends(get_session)], current_user: Annotated[UserTokenPayload, Depends(get_current_user)]):
#     print(f"Current user: {current_user.email} (ID: {current_user.sub})")  # Debug log để xem thông tin user
#     return audiobook_repo.get_audiobooks(session)

# Get books by user_id TODO
@router.get("/books", response_model=list[BookResponse])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return list_books(session)

# Get book by id


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book(session, book_id)

# Get book details with chapters and segments by active mode, optimized to avoid N+1 query problem


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_details(session, book_id)

# Switch mode and trigger background processing if needed


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, background_tasks, book_id, payload.mode)

# Create new book


@router.post("/books", response_model=BookResponse)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return create_new_book(session, book)

# Update book by id


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: uuid.UUID, book: BookInput, session: Annotated[Session, Depends(get_session)]):
    return update_book_by_id(session, book, book_id)


# Delete book by id, including all associated assets in storage and database records
@router.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await delete_book_and_assets(session, book_id)
    return {"message": "Book deleted"}
