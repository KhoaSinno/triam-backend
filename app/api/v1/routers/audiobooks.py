import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.schemas.plan import SwitchModeRequest
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.services.audiobook_service import create_new_book, delete_book_and_assets, get_book, get_book_details, list_books, switch_book_mode, update_book_by_id

router = APIRouter()

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.get("/books", response_model=list[BookResponse])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return list_books(session, MOCK_USER_ID)


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book(session, book_id, MOCK_USER_ID)


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_details(session, book_id, MOCK_USER_ID)


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, background_tasks, book_id, MOCK_USER_ID, payload.mode)


@router.post("/books", response_model=BookResponse)
def add_new_book(payload: BookCreateRequest, session: Annotated[Session, Depends(get_session)]):
    return create_new_book(session, MOCK_USER_ID, payload)


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: uuid.UUID, payload: BookUpdateRequest, session: Annotated[Session, Depends(get_session)]):
    return update_book_by_id(session, payload, book_id, MOCK_USER_ID)


# Delete book by id, including all associated assets in storage and database records
@router.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await delete_book_and_assets(session, book_id, MOCK_USER_ID)
    return {"message": "Book deleted"}
