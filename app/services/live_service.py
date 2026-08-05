import json
import uuid

from livekit import api
from sqlmodel import Session, select

from app.core.config import settings
from app.core.exceptions import BookNotFoundError, ThreadNotFoundError
from app.models.db_models import Book, ChatThread, StudyContext, StudyContextDocumentLink


def _build_livekit_token(room_name: str, metadata: dict) -> dict:
    """
    Helper dùng chung: Tạo AccessToken LiveKit với room config và trả về JWT + room_name.
    """
    agent_dispatch = api.RoomAgentDispatch(
        agent_name=settings.LIVEKIT_AGENT_NAME,
        metadata=json.dumps(metadata),
    )
    room_config = api.RoomConfiguration(
        agents=[agent_dispatch],
        empty_timeout=settings.LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS,
        departure_timeout=settings.LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS,
    )

    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": room_name}


def get_token_for_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """Tạo LiveKit token cho session đọc sách đơn lẻ sau khi kiểm tra ownership."""
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()

    book_id_value = str(book_id)
    session_room_name = f"triam_{book_id_value[:8]}_{uuid.uuid4().hex[:6]}"
    return _build_livekit_token(
        session_room_name,
        {"book_id": book_id_value, "user_id": str(user_id)},
    )


def get_token_for_thread(session: Session, thread_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """Tạo LiveKit token cho session gắn với Study Context thread sau khi kiểm tra ownership."""
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()
    context = session.get(StudyContext, thread.context_id)
    if not context or context.user_id != user_id:
        raise ThreadNotFoundError()

    # Lấy danh sách document_ids từ context
    links = session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == thread.context_id)
    ).all()
    document_ids = [str(link.book_id) for link in links]

    session_room_name = f"triam_{str(thread_id)[:8]}_{uuid.uuid4().hex[:6]}"
    metadata = {
        "thread_id": str(thread_id),
        "context_id": str(thread.context_id),
        "document_ids": document_ids,
        "user_id": str(user_id),
    }
    return _build_livekit_token(session_room_name, metadata)
