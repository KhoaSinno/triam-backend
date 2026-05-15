import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

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
from app.services import study_context_service

router = APIRouter()

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContextResponse])
async def get_study_contexts_api(session: Annotated[Session, Depends(get_session)]):
    return get_study_contexts(session, MOCK_USER_ID)


@router.get("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def get_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_context(session, MOCK_USER_ID, context_id)


@router.post("/study-contexts", response_model=StudyContextResponse)
async def create_study_context_api(payload: StudyContextInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_context(session, MOCK_USER_ID, payload)


@router.patch("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.update_context_title(session, MOCK_USER_ID, context_id, payload.title)


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_context(session, MOCK_USER_ID, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=ContextDocumentResponse)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.add_document_to_context(session, MOCK_USER_ID, context_id, payload)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_document_from_context(session, MOCK_USER_ID, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThreadResponse])
async def get_chat_threads_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_threads_for_context(session, MOCK_USER_ID, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThreadResponse)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_thread(session, MOCK_USER_ID, context_id, payload)


