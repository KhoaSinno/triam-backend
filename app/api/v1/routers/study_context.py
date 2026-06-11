import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.responses import BookResponse, ChatThreadResponse, ContextDocumentResponse, StudyContextResponse
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)
from app.services import study_context_service

router = APIRouter()


# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContextResponse])
async def get_study_contexts_api(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.list_contexts(session, current_user.sub)


@router.get("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def get_study_context_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_context(session, current_user.sub, context_id)


@router.get("/study-contexts/{context_id}/documents", response_model=List[BookResponse])
async def get_study_context_documents_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_documents_in_context(session, current_user.sub, context_id)


@router.post("/study-contexts", response_model=StudyContextResponse)
async def create_study_context_api(payload: StudyContextInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_context(session, current_user.sub, payload)


@router.patch("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.update_context_title(session, current_user.sub, context_id, payload)


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_context(session, current_user.sub, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=ContextDocumentResponse)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.add_document_to_context(session, current_user.sub, context_id, payload)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_document_from_context(session, current_user.sub, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThreadResponse])
async def get_chat_threads_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_threads_for_context(session, current_user.sub, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThreadResponse)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_thread(session, current_user.sub, context_id, payload)
