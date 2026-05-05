import logging
import uuid
from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.audiobook import get_book_by_id
from app.crud.study_context import (
    create_study_context,
    delete_study_context,
    get_study_context,
    get_study_contexts,
    update_study_context,
)
from app.crud.study_context_document_link import (
    create_new_context_document,
    delete_study_context_document,
)
from app.crud.study_context_thread import (
    create_new_thread,
    get_chat_history_by_thread_id,
    get_chat_threads_for_context,
)
from app.db import get_session
from app.models.db_models import ChatMessage, ChatThread, StudyContext, StudyContextDocumentLink
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)

logger = logging.getLogger("study_context")
router = APIRouter()

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")

# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContext])
async def get_study_contexts_api(session: Annotated[Session, Depends(get_session)]):
    return get_study_contexts(session, MOCK_USER_ID)


@router.get("/study-contexts/{context_id}", response_model=StudyContext)
async def get_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")
    return context


@router.post("/study-contexts", response_model=StudyContext)
async def create_study_context_api(payload: StudyContextInput, session: Annotated[Session, Depends(get_session)]):
    context = StudyContext(
        user_id=MOCK_USER_ID,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_study_context(session, context)


@router.patch("/study-contexts/{context_id}", response_model=StudyContext)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    updated_context = update_study_context(session, context_id, payload.title)
    if not updated_context:
        raise HTTPException(status_code=404, detail="Study context not found")
    return updated_context


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    delete_study_context(session, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=StudyContextDocumentLink)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, session: Annotated[Session, Depends(get_session)]):
    book = get_book_by_id(session, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    delete_study_context_document(session, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThread])
async def get_chat_threads_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")
    return get_chat_threads_for_context(session, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThread)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessage])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_chat_history_by_thread_id(session, thread_id)
