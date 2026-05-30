import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.schemas.plan import PlanUpdateRequest, SwitchModeRequest
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.services.audiobook_service import (
    create_new_book,
    delete_book_and_assets,
    get_book,
    get_book_details,
    get_book_learning_units,
    get_book_outline,
    list_books,
    pause_reading_plan,
    resume_reading_plan,
    switch_book_mode,
    update_book_by_id,
    update_reading_plan,
)

router = APIRouter()


@router.get("/books", response_model=list[BookResponse])
def read_all_books(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return list_books(session, current_user.sub)


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book(session, book_id, current_user.sub)


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)], mode: str | None = None):
    return get_book_details(session, book_id, current_user.sub, mode=mode)


@router.get("/books/{book_id}/outline")
def get_book_outline_endpoint(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_outline(session, book_id, current_user.sub)


@router.get("/books/{book_id}/learning-units")
def get_book_learning_units_endpoint(book_id: uuid.UUID, mode: str, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_learning_units(session, book_id, current_user.sub, mode)


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, book_id, current_user.sub, payload.mode)


@router.post("/books", response_model=BookResponse)
def add_new_book(payload: BookCreateRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return create_new_book(session, current_user.sub, payload)


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: uuid.UUID, payload: BookUpdateRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return update_book_by_id(session, payload, book_id, current_user.sub)


# Delete book by id, including all associated assets in storage and database records
@router.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    await delete_book_and_assets(session, book_id, current_user.sub)
    return {"message": "Book deleted"}


@router.post("/books/{book_id}/pause")
def pause_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Tạm dừng kế hoạch học tập của sách và giải phóng lịch học."""
    return pause_reading_plan(session, book_id, current_user.sub)


@router.post("/books/{book_id}/resume")
def resume_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Tiếp tục kế hoạch học tập của sách (kiểm tra trùng lịch các slot)."""
    return resume_reading_plan(session, book_id, current_user.sub)


@router.put("/books/{book_id}/reading-plan")
def update_plan(
    book_id: uuid.UUID,
    payload: PlanUpdateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Cập nhật cấu hình kế hoạch học tập (pace, schedule, reminder_time) không ảnh hưởng tới audio."""
    return update_reading_plan(
        session,
        book_id,
        current_user.sub,
        pace=payload.pace,
        schedule_config=payload.schedule_config,
        reminder_time=payload.reminder_time,
    )
