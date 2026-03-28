import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from tavily import AsyncTavilyClient

from app.core.config import settings
from app.services.rag_service import search_book_knowledge

tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
router = APIRouter()

client = genai.Client(api_key=settings.GEMINI_API_KEY, http_options={"api_version": "v1beta"})
# =======OLD SYSTEM INSTRUCTION=======
# SYSTEM_INSTRUCTION = """
# Bạn là Trợ lý TRIAM, một chuyên gia hỗ trợ học tập qua giọng nói.
# Nhiệm vụ của bạn:
# 1. Luôn ưu tiên sử dụng công cụ 'search_book_knowledge' để tìm câu trả lời trong sách của người dùng.
# 2. Nếu thông tin không có trong sách, hãy dùng kiến thức nền của bạn để trả lời.
# 3. Trả lời bằng giọng nói thân thiện, ngắn gọn, tập trung vào việc giúp người dùng hiểu bài.
# """
SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM - Người hỗ trợ cho người dùng đọc sách qua giọng nói. Bạn có 2 công cụ hỗ trợ:
1. 'search_book_knowledge': Dùng để tìm trong sách của người dùng. Luôn ưu tiên cái này trước.
2. 'search_web': Dùng để tìm thông tin từ Internet nếu sách không có câu trả lời hoặc câu hỏi là về tin tức/kiến thức chung.
Hãy trả lời ngắn gọn, súc tích bằng giọng nói thân thiện.
"""

# Model hỗ trợ native audio output
MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# Audio format constants (PCM 16-bit, mono)
SEND_SAMPLE_RATE = 16000  # Microphone input rate
RECEIVE_SAMPLE_RATE = 24000  # AI output rate

# NOTE: google_search grounding tool CANNOT be combined with function_declarations
# in the Gemini Live API — it causes a server-side 1008 error after tool responses.
tools_config = [
    types.Tool(
        function_declarations=[
            # Tool search book knowledge in supabase
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
                parameters={
                    "type": "OBJECT",
                    "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                    "required": ["query"],
                },
            ),
            # Tool Tavily search web input for llm (rag)
            types.FunctionDeclaration(
                name="search_web",
                description="Tìm kiếm Internet bằng Tavily khi cần kiến thức cập nhật hoặc sách không có.",
                parameters={
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
        ]
    ),
]


@router.websocket("/ws/live-assistant/{book_id}")
async def live_assistant_endpoint(websocket: WebSocket, book_id: str):
    """
    WebSocket endpoint for real-time voice conversation via Gemini Live API.

    Protocol:
    - Client → Server: raw PCM audio bytes (16kHz, 16-bit, mono)
    - Server → Client: raw PCM audio bytes (24kHz, 16-bit, mono) — AI voice response
    """
    await websocket.accept()

    config = types.LiveConnectConfig(
        tools=tools_config,
        system_instruction=types.Content(parts=[types.Part(text=SYSTEM_INSTRUCTION)]),
        generation_config=types.GenerationConfig(response_modalities=["AUDIO"]),
    )

    try:
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print("✅ Đã kết nối Gemini Live")

            async def send_to_gemini():
                """
                Reads PCM audio bytes from the WebSocket and streams them
                to Gemini using send_realtime_input — the correct Live API method.
                """
                try:
                    while True:
                        data = await websocket.receive_bytes()
                        await session.send_realtime_input(audio={"data": data, "mime_type": "audio/pcm"})
                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (send loop)")
                except Exception as e:
                    print(f"❌ Lỗi gửi audio: {e}")

            async def receive_from_gemini():
                """
                Receives responses from Gemini using the async-for pattern shown
                in the reference code. Sends audio chunks to the client immediately.
                Handles tool calls (RAG search) inline.
                """
                result_text = ""
                try:
                    # Single async-for loop — the correct pattern from the reference code
                    async for response in session.receive():
                        server_content = response.server_content

                        # ── Audio response ──────────────────────────────────
                        if server_content and server_content.model_turn:
                            for part in server_content.model_turn.parts:
                                if part.inline_data and isinstance(part.inline_data.data, bytes):
                                    # Send audio chunk directly to client (no large buffer)
                                    await websocket.send_bytes(part.inline_data.data)

                        # ── Turn complete — AI finished speaking ─────────────
                        if server_content and server_content.turn_complete:
                            print("🔔 Gemini turn complete")

                        # ── Tool call: RAG search ────────────────────────────
                        if response.tool_call:
                            for call in response.tool_call.function_calls:
                                tool_name = call.name
                                if tool_name == "search_book_knowledge":
                                    query = call.args.get("query", "")
                                    print(f"🔍 RAG search: {query} (call.id={call.id})")
                                    if not call.id:
                                        print("⚠️ Bỏ qua tool call vì call.id là None")
                                        continue
                                    try:
                                        context = await search_book_knowledge(query, book_id)
                                        result_text = context
                                    except Exception as rag_err:
                                        print(f"❌ Lỗi RAG search: {rag_err}")
                                        result_text = "Không thể tra cứu thông tin lúc này."
                                elif tool_name == "search_web":
                                    # Gọi Tavily Search
                                    print("🌐 Đang search Tavily...")
                                    query = call.args.get("query", "")
                                    try:
                                        search_result = await tavily_client.search(
                                            query=query,
                                            search_depth="basic",  # "advanced" cho chất lượng cao nhất
                                            max_results=3,
                                        )
                                    except Exception as tavily_err:
                                        print(f"❌ Lỗi Tavily search: {tavily_err}")
                                        result_text = "Không thể tra cứu thông tin lúc này."
                                    # Tóm tắt kết quả cho Gemini đọc
                                    result_text = "\n".join([f"- {r['content']}" for r in search_result["results"]])
                                try:
                                    await session.send_tool_response(
                                        function_responses=[
                                            types.FunctionResponse(
                                                name=tool_name,
                                                id=call.id,
                                                response={"result": result_text},
                                            )
                                        ]
                                    )
                                    print(f"✅ Đã gửi {tool_name} response cho call.id={call.id}")
                                except Exception as send_err:
                                    print(f"❌ Lỗi gửi tool response: {send_err}")
                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (receive loop)")
                except Exception as e:
                    print(f"❌ Lỗi nhận audio: {e}")

            # Run both tasks concurrently; cancel the other when one finishes
            await asyncio.gather(send_to_gemini(), receive_from_gemini())

    except WebSocketDisconnect:
        print("📴 Client ngắt kết nối trước khi kết nối Gemini")
    except Exception as e:
        print(f"❌ Lỗi kết nối Gemini Live: {e}")
        try:
            await websocket.send_text(f"Lỗi kết nối Gemini Live: {e}")
        except Exception:
            pass
