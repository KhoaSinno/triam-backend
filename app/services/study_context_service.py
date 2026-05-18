import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import BadRequestError, BookNotFoundError, StudyContextNotFoundError
from app.models.db_models import ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.audiobook_repo import get_book_by_id
from app.repositories.study_context_document_link_repo import create_new_context_document
from app.repositories.study_context_repo import create_study_context, get_study_context
from app.repositories.study_context_thread_repo import create_new_thread, get_or_create_thread_for_book_repo
from app.schemas.study_context import ChatThreadInput, StudyContextDocumentInput, StudyContextInput


def _get_owned_context(session: Session, context_id: uuid.UUID, user_id: uuid.UUID) -> StudyContext:
    """Helper: Lấy context và kiểm tra ownership. Raise nếu không tìm thấy hoặc không thuộc user."""
    context = get_study_context(session, context_id)
    if not context or context.user_id != user_id:
        raise StudyContextNotFoundError()
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


def get_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> StudyContext:
    """Lấy context và kiểm tra ownership. Dùng cho router GET."""
    return _get_owned_context(session, context_id, user_id)


def update_context_title(session: Session, user_id: uuid.UUID, context_id: uuid.UUID, title: str) -> StudyContext:
    """Validate ownership rồi cập nhật title."""
    from app.repositories.study_context_repo import update_study_context
    _get_owned_context(session, context_id, user_id)
    updated = update_study_context(session, context_id, title)
    if not updated:
        raise StudyContextNotFoundError()
    return updated


def delete_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> None:
    """Validate ownership rồi xóa context."""
    from app.repositories.study_context_repo import delete_study_context
    _get_owned_context(session, context_id, user_id)
    delete_study_context(session, context_id)


def add_document_to_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: StudyContextDocumentInput,
) -> StudyContextDocumentLink:
    """Validate book và context, sau đó tạo link giữa context và document."""
    book = get_book_by_id(session, payload.book_id)
    if not book:
        raise BookNotFoundError()

    _get_owned_context(session, context_id, user_id)

    link = StudyContextDocumentLink(
        context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


def delete_document_from_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    book_id: uuid.UUID,
) -> None:
    """Validate ownership rồi xóa document link."""
    from app.repositories.study_context_document_link_repo import delete_study_context_document
    _get_owned_context(session, context_id, user_id)
    delete_study_context_document(session, context_id, book_id)


def get_threads_for_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list:
    """Validate ownership rồi trả về danh sách threads."""
    from app.repositories.study_context_thread_repo import get_chat_threads_for_context
    _get_owned_context(session, context_id, user_id)
    return get_chat_threads_for_context(session, context_id)


def create_thread(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: ChatThreadInput,
) -> ChatThread:
    """Validate context ownership rồi tạo mới ChatThread."""
    _get_owned_context(session, context_id, user_id)

    context = _get_owned_context(session, context_id, user_id)
    if context.is_auto_generated:
        raise BadRequestError("Không thể tạo thêm thread cho Direct Book Context.")

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)


def get_or_create_thread_for_book(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str):
    ctx_id, thread_id = get_or_create_thread_for_book_repo(
        session, user_id, book_id, title=title)
    return {'context_id': str(ctx_id), 'thread_id': str(thread_id), 'is_auto_generated': True}
