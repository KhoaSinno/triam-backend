import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session

from app.models.db_models import ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.audiobook_repo import get_book_by_id
from app.repositories.study_context_document_link_repo import create_new_context_document
from app.repositories.study_context_repo import create_study_context, get_study_context
from app.repositories.study_context_thread_repo import create_new_thread
from app.schemas.study_context import ChatThreadInput, StudyContextDocumentInput, StudyContextInput


def _get_owned_context(session: Session, context_id: uuid.UUID, user_id: uuid.UUID) -> StudyContext:
    """Helper: Lấy context và kiểm tra ownership. Raise 404 nếu không tìm thấy hoặc không thuộc user."""
    context = get_study_context(session, context_id)
    if not context or context.user_id != user_id:
        raise HTTPException(status_code=404, detail="Study context not found")
    return context


def create_context(session: Session, user_id: uuid.UUID, payload: StudyContextInput) -> StudyContext:
    """Tạo mới một StudyContext cho user."""
    context = StudyContext(
        user_id=user_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_study_context(session, context)


def add_document_to_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: StudyContextDocumentInput,
) -> StudyContextDocumentLink:
    """Validate book và context, sau đó tạo link giữa context và document."""
    book = get_book_by_id(session, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    _get_owned_context(session, context_id, user_id)

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


def create_thread(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: ChatThreadInput,
) -> ChatThread:
    """Validate context ownership rồi tạo mới ChatThread."""
    _get_owned_context(session, context_id, user_id)

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)
