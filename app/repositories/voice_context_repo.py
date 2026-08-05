from __future__ import annotations

import uuid

from sqlmodel import Session, select

from app.models.db_models import ChatThread, StudyContext, StudyContextDocumentLink
from app.services.voice_agent.contracts import VoiceContextResolution


def get_owned_voice_context_for_thread(
    session: Session,
    *,
    user_id: uuid.UUID,
    thread_id: uuid.UUID,
) -> VoiceContextResolution | None:
    """Resolve a thread into its current DB-owned RAG/persistence scope."""
    thread = session.get(ChatThread, thread_id)
    if thread is None:
        return None
    context = session.get(StudyContext, thread.context_id)
    if context is None or context.user_id != user_id:
        return None

    links = session.exec(
        select(StudyContextDocumentLink.book_id).where(
            StudyContextDocumentLink.context_id == context.id
        )
    ).all()
    document_ids = tuple(str(book_id) for book_id in links)
    if not document_ids:
        return None

    return VoiceContextResolution(
        context_id=context.id,
        thread_id=thread.id,
        document_ids=document_ids,
        context_title=context.title,
        thread_title=thread.title,
    )
