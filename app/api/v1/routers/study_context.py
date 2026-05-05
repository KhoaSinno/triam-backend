import logging
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.database import get_session
from app.models.db_models import ChatMessage, ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.study_context_repo import (
    delete_study_context,
    get_study_context,
    get_study_contexts,
    update_study_context,
)
from app.repositories.study_context_thread_repo import (
    get_chat_history_by_thread_id,
    get_chat_threads_for_context,
)
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)
from app.services.study_context_service import (
    add_document_to_context,
    create_context,
    create_thread,
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
    return create_context(session, MOCK_USER_ID, payload)


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
    return add_document_to_context(session, MOCK_USER_ID, context_id, payload)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    from app.repositories.study_context_document_link_repo import delete_study_context_document
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
    return create_thread(session, MOCK_USER_ID, context_id, payload)


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessage])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_chat_history_by_thread_id(session, thread_id)
