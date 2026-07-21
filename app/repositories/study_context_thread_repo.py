import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.exceptions import DirectBookContextConflictError
from app.models.db_models import ChatMessage, ChatThread, DirectBookContext, StudyContext, StudyContextDocumentLink


def get_chat_threads_for_context(session: Session, context_id: uuid.UUID) -> list[ChatThread]:
    threads = session.exec(select(ChatThread).where(
        ChatThread.context_id == context_id)).all()
    return threads


def get_chat_history_by_thread_id(session: Session, thread_id: uuid.UUID) -> list[ChatMessage]:
    messages = session.exec(select(ChatMessage).where(
        ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()
    return messages


def update_thread_by_id_repo(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def get_or_create_thread_for_book_repo(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str) -> tuple[uuid.UUID, uuid.UUID]:
    # Get existing thread for the book
    direct_ctx = session.exec(select(DirectBookContext).where(
        DirectBookContext.book_id == book_id, DirectBookContext.user_id == user_id)).first()

    if direct_ctx:
        # Self-healing: Cập nhật lại tiêu đề nếu Context/Thread cũ đang bị dính tên mặc định 'New Book Chat'
        context = session.get(StudyContext, direct_ctx.context_id)
        thread = session.get(ChatThread, direct_ctx.primary_thread_id)

        need_commit = False
        if context and context.title == "New Book Chat" and title and title != "New Book Chat":
            context.title = title
            session.add(context)
            need_commit = True

        if thread and thread.title == "New Book Chat" and title and title != "New Book Chat":
            thread.title = title
            session.add(thread)
            need_commit = True

        if need_commit:
            session.commit()

        return direct_ctx.context_id, direct_ctx.primary_thread_id

    try:

        # Create new context
        new_context = StudyContext(
            user_id=user_id,
            title=title,
            is_auto_generated=True,
        )

        session.add(new_context)
        session.flush()  # To get new_context.id populated

        # Link context with book
        new_study_context_book_link = StudyContextDocumentLink(
            context_id=new_context.id,
            book_id=book_id,
        )
        session.add(new_study_context_book_link)

        # Create new thread

        new_thread = ChatThread(
            context_id=new_context.id,
            title=title,
        )

        session.add(new_thread)
        session.flush()  # To get new_thread.id populated

        # Create new DirectBookContext
        new_direct_ctx = DirectBookContext(
            user_id=user_id,
            book_id=book_id,
            context_id=new_context.id,
            primary_thread_id=new_thread.id,
        )

        session.add(new_direct_ctx)
        session.commit()

        # Final: Return new context_id and thread_id
        return new_context.id, new_thread.id

    except IntegrityError:
        session.rollback()
        raise DirectBookContextConflictError() from None


def create_new_thread(session: Session, thread: ChatThread) -> ChatThread:
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def update_thread_title(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def delete_thread(session: Session, thread_id: uuid.UUID) -> None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        session.delete(thread)
        session.commit()
