import json
import uuid

from fastapi import APIRouter
from livekit import api

from app.core.config import settings

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