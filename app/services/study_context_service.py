import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import BadRequestError, BookNotFoundError, StudyContextNotFoundError, ThreadNotFoundError
from app.models.db_models import ChatMessage, ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.audiobook_repo import get_book_by_id
from app.repositories.study_context_document_link_repo import create_new_context_document
from app.repositories.study_context_repo import create_study_context, get_study_context, get_study_contexts
from app.repositories.study_context_thread_repo import (
    create_new_thread,
    delete_thread,
    get_chat_history_by_thread_id,
    get_chat_threads_for_context,
    get_or_create_thread_for_book_repo,
    update_thread_by_id_repo,
)
from app.schemas.study_context import ChatThreadInput, StudyContextDocumentInput, StudyContextInput, StudyContextUpdate


def _get_owned_context(session: Session, context_id: uuid.UUID, user_id: uuid.UUID) -> StudyContext:
    """Helper: Lấy context và kiểm tra ownership. Raise nếu không tìm thấy hoặc không thuộc user."""
    context = get_study_context(session, context_id)
    if not context or context.user_id != user_id:
        raise StudyContextNotFoundError()
    return context


def _get_owned_thread(session: Session, thread_id: uuid.UUID, user_id: uuid.UUID) -> ChatThread:
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()
    _get_owned_context(session, thread.context_id, user_id)
    return thread


def get_documents_in_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list[dict]:
    """Lấy danh sách các tài liệu trong context sau khi kiểm tra quyền sở hữu."""
    context = _get_owned_context(session, context_id, user_id)

    def _book_to_dict(book) -> dict:
        return {
            "id": book.id,
            "user_id": book.user_id,
            "title": book.title,
            "author": book.author,
            "file_url": book.file_url,
            "document_type": book.document_type,
            "total_sections": book.total_sections,
            "total_units": book.total_units,
            "is_shared": book.is_shared,
            "parent_shared_id": book.parent_shared_id,
            "status": book.status,
            "created_at": book.created_at,
            "updated_at": book.updated_at,
            # Context document view không có learning state / mode flags
            "learning_status": None,
            "book_progress_percent": None,
            "completed_at": None,
            "has_full_mode": False,
            "has_pareto_mode": False,
        }

    return [_book_to_dict(book) for book in context.books]


def _build_capabilities(is_auto_generated: bool) -> dict:
    """Helper xây dựng cờ quyền hạn thao tác UI cho Frontend."""
    if is_auto_generated:
        return {
            "can_add_documents": False,
            "can_remove_documents": False,
            "can_create_threads": True,
            "can_rename_context": True,
            "can_delete_context": True,
            "can_rename_threads": True,
            "can_delete_threads": True,
        }
    return {
        "can_add_documents": True,
        "can_remove_documents": True,
        "can_create_threads": True,
        "can_rename_context": True,
        "can_delete_context": True,
        "can_rename_threads": True,
        "can_delete_threads": True,
    }


def _context_to_dict(session: Session, user_id: uuid.UUID, ctx: StudyContext) -> dict:
    docs = get_documents_in_context(session, user_id, ctx.id)
    return {
        "id": ctx.id,
        "title": ctx.title,
        "is_auto_generated": ctx.is_auto_generated,
        "document_count": len(docs),
        "documents": docs,
        "capabilities": _build_capabilities(ctx.is_auto_generated),
        "created_at": ctx.created_at,
        "updated_at": ctx.updated_at,
    }


def list_contexts(session: Session, user_id: uuid.UUID) -> list[dict]:
    contexts = get_study_contexts(session, user_id)
    return [_context_to_dict(session, user_id, ctx) for ctx in contexts]


def create_context(session: Session, user_id: uuid.UUID, payload: StudyContextInput) -> dict:
    """Tạo mới một StudyContext cho user."""
    context = StudyContext(
        user_id=user_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    created = create_study_context(session, context)
    return _context_to_dict(session, user_id, created)


def update_thread_by_id(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID, title: str) -> ChatThread:
    _get_owned_thread(session, thread_id, user_id)
    updated = update_thread_by_id_repo(session, thread_id, title)
    if not updated:
        raise ThreadNotFoundError("Không thể cập nhật thread.")
    return updated


def delete_thread_by_id(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> None:
    _get_owned_thread(session, thread_id, user_id)
    delete_thread(session, thread_id)


def get_thread_messages(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> list[ChatMessage]:
    thread = _get_owned_thread(session, thread_id, user_id)
    return get_chat_history_by_thread_id(session, thread.id)


def get_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> dict:
    """Lấy context và kiểm tra ownership. Dùng cho router GET."""
    ctx = _get_owned_context(session, context_id, user_id)
    return _context_to_dict(session, user_id, ctx)


def update_context_title(session: Session, user_id: uuid.UUID, context_id: uuid.UUID, payload: StudyContextUpdate) -> dict:
    """Validate ownership rồi cập nhật title."""
    from app.repositories.study_context_repo import update_study_context

    if payload.title is None:
        raise BadRequestError("Thiếu title để cập nhật Study Context.")
    _get_owned_context(session, context_id, user_id)
    updated = update_study_context(session, context_id, payload.title)
    if not updated:
        raise StudyContextNotFoundError()
    return _context_to_dict(session, user_id, updated)


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
    if not book or (book.user_id != user_id and not book.is_shared):
        raise BookNotFoundError()

    ctx = _get_owned_context(session, context_id, user_id)
    if ctx.is_auto_generated:
        raise BadRequestError("Không thể thêm sách phụ vào Direct Book Context tự động tạo.")

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


def delete_document_from_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    book_id: uuid.UUID,
) -> None:
    """Validate ownership rồi xóa document link."""
    from app.repositories.study_context_document_link_repo import delete_study_context_document

    ctx = _get_owned_context(session, context_id, user_id)
    if ctx.is_auto_generated:
        raise BadRequestError("Không thể xóa sách khỏi Direct Book Context tự động tạo.")

    delete_study_context_document(session, context_id, book_id)


def get_threads_for_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list:
    """Validate ownership rồi trả về danh sách threads."""
    _get_owned_context(session, context_id, user_id)
    return get_chat_threads_for_context(session, context_id)


def create_thread(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: ChatThreadInput,
) -> ChatThread:
    """Validate context ownership rồi tạo mới ChatThread."""
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


def get_or_create_thread_for_book(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str | None = None) -> dict:
    """Lấy hoặc tạo mới thread cho cuốn sách với tên sách mặc định thay vì 'New Book Chat'."""
    book = get_book_by_id(session, book_id)
    if not book or book.user_id != user_id:
        raise BookNotFoundError()

    default_title = title if (title and title != "New Book Chat") else (book.title or "Sách chưa đặt tên")
    ctx_id, thread_id = get_or_create_thread_for_book_repo(session, user_id, book_id, title=default_title)

    context = get_study_context(session, ctx_id)
    thread = session.get(ChatThread, thread_id)

    return {
        "context_id": ctx_id,
        "thread_id": thread_id,
        "is_auto_generated": True,
        "book_id": book.id,
        "book_title": book.title,
        "context_title": context.title if context else default_title,
        "thread_title": thread.title if thread else default_title,
    }
