import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.responses import ChatMessageResponse, ChatThreadResponse
from app.schemas.study_context import (
    ChatThreadUpdate,
)
from app.services.study_context_service import (
    delete_thread_by_id,
    get_or_create_thread_for_book,
    get_thread_messages,
    update_thread_by_id,
)

router = APIRouter()

# Get all threads for a context


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessageResponse])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    return get_thread_messages(session, current_user.sub, thread_id)


# Get or create thread for a book


@router.get("/threads/for-book/{book_id}")
async def get_thread_for_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    return get_or_create_thread_for_book(session, user_id=current_user.sub, book_id=book_id, title="New Book Chat")


# Update current thread by thread_id


@router.put("/threads/{thread_id}", response_model=ChatThreadResponse)
async def update_thread_api(thread_id: uuid.UUID, payload: ChatThreadUpdate, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    return update_thread_by_id(session, current_user.sub, thread_id, payload.title)


@router.delete("/threads/{thread_id}")
async def delete_thread_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    delete_thread_by_id(session, current_user.sub, thread_id)
    return {"message": "Thread deleted successfully"}
