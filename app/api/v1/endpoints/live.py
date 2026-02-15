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

# ✅ SỬA LẠI MODEL ID ĐÚNG
MODEL_ID = "gemini-2.5-flash-native-audio-latest" 

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
    await websocket.accept()
    
    # ✅ THÊM VOICE CONFIG ĐỂ AI BIẾT CÁCH TRẢ LỜI
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
                try:
                    while True:
                        data = await websocket.receive_bytes()
                        # ✅ QUAN TRỌNG: end_of_turn=False để stream liên tục
                        await session.send(input=types.LiveClientRealtimeInput(
                            media_chunks=[types.Blob(data=data, mime_type="audio/pcm")]
                        ), end_of_turn=False) 
                except Exception as e:
                    print(f"Gửi lỗi: {e}")

            async def receive_from_gemini():
                # Giảm kích thước buffer xuống để AI phản hồi nhanh hơn nhưng vẫn không bị dập
                CHUNK_SIZE = 96000 # ~1 giây âm thanh
                audio_buffer = bytearray()
    
                try:
                    async for message in session.receive():
                        if message.server_content and message.server_content.model_turn:
                            parts = message.server_content.model_turn.parts
                            for part in parts:
                                if part.inline_data:
                                    audio_buffer.extend(part.inline_data.data)
                                    
                                    if len(audio_buffer) >= CHUNK_SIZE:
                                        await websocket.send_bytes(bytes(audio_buffer))
                                        audio_buffer.clear()
                        
                        # Khi AI kết thúc lượt nói, gửi nốt phần còn dư
                        if message.server_content and message.server_content.turn_complete:
                            if audio_buffer:
                                await websocket.send_bytes(bytes(audio_buffer))
                                audio_buffer.clear()

                        # Xử lý RAG tự động
                        if message.tool_call:
                            for call in message.tool_call.function_calls:
                                print(f"🔍 Đang RAG: {call.args['query']}")
                                context = await search_book_knowledge(call.args["query"], book_id)
                                await session.send(input=types.LiveClientToolResponse(
                                    function_responses=[types.FunctionResponse(
                                        name="search_book_knowledge", id=call.id, response={"result": context}
                                    )]
                                ))
                except Exception as e:
                    print(f"Nhận lỗi: {e}")

            await asyncio.gather(send_to_gemini(), receive_from_gemini())
    except Exception as e:
        print(f"Lỗi kết nối Gemini Live: {e}")
        try: await websocket.send_text(f"Lỗi kết nối Gemini Live: {e}")
        except: pass