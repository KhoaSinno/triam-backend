import asyncio
import json
import base64
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from app.services.rag_service import search_book_knowledge
from app.core.config import settings

router = APIRouter()

# 1. Khởi tạo Client Gemini (Sử dụng SDK google-genai mới)
client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    http_options={'api_version': 'v1alpha'}
)

MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# 2. Định nghĩa Cấu hình công cụ (Tools)
# Chúng ta đưa RAG (Supabase) và Google Search vào cùng một session
tools_config = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức chi tiết trong cuốn sách hiện tại từ database khi người dùng hỏi về nội dung sách.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING", 
                            "description": "Câu hỏi hoặc từ khóa cần tìm kiếm trong sách"
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
    ),
    types.Tool(google_search={}) # Grounding với Google Search cho kiến thức ngoài sách
]

SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM, một chuyên gia hỗ trợ học tập qua giọng nói.
Nhiệm vụ của bạn:
1. Luôn ưu tiên sử dụng công cụ 'search_book_knowledge' để tìm câu trả lời trong sách của người dùng.
2. Nếu thông tin không có trong sách, hãy dùng 'google_search' để cung cấp thông tin chính xác từ internet.
3. Trả lời bằng giọng nói thân thiện, ngắn gọn, tập trung vào việc giúp người dùng hiểu bài.
"""

@router.websocket("/ws/live-assistant/{book_id}")
async def live_assistant_endpoint(websocket: WebSocket, book_id: str):
    await websocket.accept()
    print(f"🚀 Client connected for RAG on Book: {book_id}")

    config = types.LiveConnectConfig(
        tools=tools_config,
        system_instruction=types.Content(
            parts=[types.Part(text=SYSTEM_INSTRUCTION)]
        ),
        generation_config=types.GenerationConfig(
            response_modalities=["AUDIO"]
        )
    )

    try:  # 👈 THÊM TRY/EXCEPT bao quanh Gemini connection
        print(f"🔗 Đang kết nối Gemini Live API...")
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print(f"✅ Gemini Live API connected!")
            
            async def send_to_gemini():
                try:
                    while True:
                        data = await websocket.receive_bytes()
                        print(f"🎤 Nhận {len(data)} bytes từ Flutter")
                        await session.send(input=types.LiveClientRealtimeInput(
                            media_chunks=[types.Blob(data=data, mime_type="audio/pcm")]
                        ), end_of_turn=True)
                except WebSocketDisconnect:
                    print("🔌 Flutter disconnected")
                except Exception as e:
                    print(f"❌ Error sending to Gemini: {type(e).__name__}: {e}")

            async def receive_from_gemini():
                try:
                    async for message in session.receive():
                        if message.server_content and message.server_content.model_turn:
                            parts = message.server_content.model_turn.parts
                            for part in parts:
                                if part.inline_data:
                                    print(f"🔊 Gửi {len(part.inline_data.data)} bytes audio về Flutter")
                                    await websocket.send_bytes(part.inline_data.data)
                        
                        if message.tool_call:
                            for call in message.tool_call.function_calls:
                                if call.name == "search_book_knowledge":
                                    query_text = call.args["query"]
                                    print(f"🔍 AI đang gọi RAG: {query_text}")
                                    context = await search_book_knowledge(query_text, book_id)
                                    await session.send(input=types.LiveClientToolResponse(
                                        function_responses=[
                                            types.FunctionResponse(
                                                name="search_book_knowledge",
                                                id=call.id,
                                                response={"result": context}
                                            )
                                        ]
                                    ))
                                    print("✅ Đã gửi context cho AI.")
                except Exception as e:
                    print(f"❌ Error receiving from Gemini: {type(e).__name__}: {e}")

            try:
                await asyncio.gather(send_to_gemini(), receive_from_gemini())
            except WebSocketDisconnect:
                print(f"🔌 Client disconnected for Book: {book_id}")
                
    except Exception as e:  # 👈 CATCH lỗi kết nối Gemini
        error_msg = f"❌ Gemini Live API Error: {type(e).__name__}: {e}"
        print(error_msg)
        # Gửi lỗi về Flutter trước khi đóng
        try:
            await websocket.send_text(error_msg)
        except:
            pass
        await websocket.close(code=1011, reason=str(e)[:120])

# @router.websocket("/ws/live-assistant/{book_id}")
# async def live_assistant_endpoint(websocket: WebSocket, book_id: str):
#     await websocket.accept()
#     print(f"🚀 Client connected for RAG on Book: {book_id}")

#     # Cấu hình phiên kết nối Live
#     config = types.LiveConnectConfig(
#         tools=tools_config,
#         system_instruction=types.Content(
#             parts=[types.Part(text=SYSTEM_INSTRUCTION)]
#         ),
#         generation_config=types.GenerationConfig(
#             response_modalities=["AUDIO"] # AI phản hồi bằng âm thanh
#         )
#     )

#     async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
        
#         # Hàm xử lý gửi Audio từ Flutter lên Gemini
#         async def send_to_gemini():
#             try:
#                 while True:
#                     data = await websocket.receive_bytes()
#                     # Flutter gửi PCM 16-bit 16kHz, gửi thẳng vào session
#                     await session.send(input=types.LiveClientRealtimeInput(
#                         media_chunks=[types.Blob(data=data, mime_type="audio/pcm")]
#                     ), end_of_turn=True)
#             except Exception as e:
#                 print(f"Error sending to Gemini: {e}")

#         # Hàm xử lý nhận phản hồi từ Gemini và điều phối Tool RAG
#         async def receive_from_gemini():
#             try:
#                 async for message in session.receive():
#                     # 1. Xử lý Audio trả về (Gửi ngược lại cho Flutter)
#                     if message.server_content and message.server_content.model_turn:
#                         parts = message.server_content.model_turn.parts
#                         for part in parts:
#                             if part.inline_data:
#                                 await websocket.send_bytes(part.inline_data.data)
                    
#                     # 2. Xử lý Native Tool Calling (RAG & Search)
#                     if message.tool_call:
#                         for call in message.tool_call.function_calls:
#                             if call.name == "search_book_knowledge":
#                                 query_text = call.args["query"]
#                                 print(f"🔍 AI đang gọi RAG: {query_text}")
                                
#                                 # Thực hiện tra cứu thực tế từ Supabase qua rag_service
#                                 context = await search_book_knowledge(query_text, book_id)
                                
#                                 # Gửi kết quả tra cứu ngược lại cho AI để nó tổng hợp câu trả lời
#                                 await session.send(input=types.LiveClientToolResponse(
#                                     function_responses=[
#                                         types.FunctionResponse(
#                                             name="search_book_knowledge",
#                                             id=call.id,
#                                             response={"result": context}
#                                         )
#                                     ]
#                                 ))
#                                 print("✅ Đã gửi context cho AI.")
#             except Exception as e:
#                 print(f"Error receiving from Gemini: {e}")

#         # Chạy song song hai luồng gửi/nhận
#         try:
#             await asyncio.gather(send_to_gemini(), receive_from_gemini())
#         except WebSocketDisconnect:
#             print(f"🔌 Client disconnected for Book: {book_id}")
#         except Exception as e:
#             print(f"❌ Connection Error: {e}")