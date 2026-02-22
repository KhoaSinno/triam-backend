import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from app.services.rag_service import search_book_knowledge
from app.core.config import settings

router = APIRouter()

client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    http_options={'api_version': 'v1beta'}
)

SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM, một chuyên gia hỗ trợ học tập qua giọng nói.
Nhiệm vụ của bạn:
1. Luôn ưu tiên sử dụng công cụ 'search_book_knowledge' để tìm câu trả lời trong sách của người dùng.
2. Nếu thông tin không có trong sách, hãy dùng 'google_search' để cung cấp thông tin chính xác từ internet.
3. Trả lời bằng giọng nói thân thiện, ngắn gọn, tập trung vào việc giúp người dùng hiểu bài.
"""

# Model hỗ trợ native audio output
MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# Audio format constants (PCM 16-bit, mono)
SEND_SAMPLE_RATE = 16000   # Microphone input rate
RECEIVE_SAMPLE_RATE = 24000  # AI output rate

tools_config = [
    types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="search_book_knowledge",
            description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
            parameters={
                "type": "OBJECT",
                "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                "required": ["query"]
            }
        )
    ]),
    types.Tool(google_search={})
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
        system_instruction=types.Content(
            parts=[types.Part(text=SYSTEM_INSTRUCTION)]
        ),
        generation_config=types.GenerationConfig(
            response_modalities=["AUDIO"]
        )
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
                        await session.send_realtime_input(
                            audio={"data": data, "mime_type": "audio/pcm"}
                        )
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
                                if call.name == "search_book_knowledge":
                                    query = call.args.get("query", "")
                                    print(f"🔍 RAG search: {query}")
                                    context = await search_book_knowledge(query, book_id)
                                    await session.send(
                                        input=types.LiveClientToolResponse(
                                            function_responses=[
                                                types.FunctionResponse(
                                                    name="search_book_knowledge",
                                                    id=call.id,
                                                    response={"result": context}
                                                )
                                            ]
                                        )
                                    )

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