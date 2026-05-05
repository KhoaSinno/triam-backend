import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from livekit import api
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Session, select

from app.core.config import settings
from app.db.database import get_session
from app.models.db_models import ChatThread, StudyContextDocumentLink

router = APIRouter()


@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    # Cấu hình dispatch Agent ngay khi user join room
    # Điều này bắt buộc để LiveKit FE Flutter Session nhận diện được 'dispatchesAgent: true'
    session_room_name = f"triam_{book_id[:8]}_{uuid.uuid4().hex[:6]}"

    agent_dispatch = api.RoomAgentDispatch(agent_name=settings.LIVEKIT_AGENT_NAME, metadata=json.dumps({"book_id": book_id}))
    room_config = api.RoomConfiguration(agents=[agent_dispatch])

    # Create Token for user join room
    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=session_room_name,
            )
        )
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": session_room_name}


@router.get("/live-token/thread/{thread_id}")
async def get_token_thread(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    # 1. Validate thread and get context
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # 2. Get document_ids for context
    links = session.exec(select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == thread.context_id)).all()
    document_ids = [str(link.book_id) for link in links]

    # Cấu hình dispatch Agent ngay khi user join room
    session_room_name = f"triam_{str(thread_id)[:8]}_{uuid.uuid4().hex[:6]}"

    agent_dispatch = api.RoomAgentDispatch(
        agent_name=settings.LIVEKIT_AGENT_NAME, metadata=json.dumps({"thread_id": str(thread_id), "context_id": str(thread.context_id), "document_ids": document_ids})
    )
    room_config = api.RoomConfiguration(agents=[agent_dispatch])

    # Create Token for user join room
    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=session_room_name,
            )
        )
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": session_room_name}
