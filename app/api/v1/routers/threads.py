import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import UUID, Session

from app.db.database import get_session
from app.repositories.study_context_repo import get_study_contexts
from app.repositories.study_context_thread_repo import get_chat_history_by_thread_id
from app.schemas.responses import ChatMessageResponse, ChatThreadResponse, ContextDocumentResponse, StudyContextResponse
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)
from app.services.study_context_service import get_or_create_thread_for_book

router = APIRouter()

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessageResponse])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_chat_history_by_thread_id(session, thread_id)


@router.get('/threads/for-book/{book_id}')
async def get_thread_for_book(book_id: uuid.UUID, session: Session = Depends(get_session)):
    return get_or_create_thread_for_book(session, user_id=MOCK_USER_ID, book_id=book_id, title='New Book Chat')
