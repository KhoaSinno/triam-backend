import os
import uuid
from typing import Any, cast

import google.genai as genai
from fastapi import APIRouter
from google.genai import types
from livekit import api
from tavily import AsyncTavilyClient

from app.core.config import settings

tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
router = APIRouter()

client = genai.Client(api_key=settings.GEMINI_API_KEY, http_options={"api_version": "v1beta"})

# =======SYSTEM INSTRUCTION=======
SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM - Người hỗ trợ cho người dùng đọc sách qua giọng nói. Bạn có 2 công cụ hỗ trợ:
1. 'search_book_knowledge': Dùng để tìm trong sách của người dùng. Luôn ưu tiên cái này trước.
2. 'search_web': Dùng để tìm thông tin từ Internet nếu sách không có câu trả lời hoặc câu hỏi là về tin tức/kiến thức chung.
Hãy trả lời ngắn gọn, súc tích bằng giọng nói thân thiện.
"""

# Model hỗ trợ native audio output
MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# NOTE: google_search grounding tool CANNOT be combined with function_declarations
# in the Gemini Live API — it causes a server-side 1008 error after tool responses.
tools_config = [
    types.Tool(
        function_declarations=[
            # Tool search book knowledge in supabase
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
                parameters=cast(
                    Any,
                    {
                        "type": "OBJECT",
                        "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                        "required": ["query"],
                    },
                ),
            ),
            # Tool Tavily search web input for llm (rag)
            types.FunctionDeclaration(
                name="search_web",
                description="Tìm kiếm Internet bằng Tavily khi cần kiến thức cập nhật hoặc sách không có.",
                parameters=cast(
                    Any,
                    {
                        "type": "OBJECT",
                        "properties": {
                            "query": {
                                "type": "STRING",
                                "description": "Câu hỏi tìm kiếm trên web",
                            }
                        },
                        "required": ["query"],
                    },
                ),
            ),
        ]
    ),
]

# === MAIN ROUTE: WebSocket for Gemini Live ===
@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    # Cấu hình dispatch Agent ngay khi user join room
    # Điều này bắt buộc để LiveKit FE Flutter Session nhận diện được 'dispatchesAgent: true'
    agent_name = os.getenv("LIVEKIT_AGENT_NAME", "my-agent").strip() or "my-agent"
    agent_dispatch = api.RoomAgentDispatch(agent_name=agent_name)
    room_config = api.RoomConfiguration(name=book_id, agents=[agent_dispatch])

    # Tạo Token định danh cho User
    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=book_id,  # Dùng chính book_id làm tên phòng
            )
        )
        .with_room_config(room_config)
        .with_metadata(book_id)
    )  # Truyền book_id vào metadata cho Agent đọc

    return {"token": token.to_jwt()}
