import os
from typing import Annotated

from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, function_tool, room_io
from livekit.plugins import google, noise_cancellation, silero
from supabase import Client, create_client
from tavily import TavilyClient

from app.core.config import settings
from app.services.rag_service import search_book_knowledge

# Load environment
load_dotenv()

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


# Khởi tạo Supabase (Dùng cho RAG)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


class TriamAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""Bạn là Trợ lý TRIAM - Người hỗ trợ đọc sách qua giọng nói.
            1. Luôn dùng 'search_book_knowledge' trước khi trả lời về nội dung sách.
            2. Trả lời cực kỳ ngắn gọn (dưới 2 câu), thân thiện.
            3. Nếu không thấy trong sách, mới dùng 'search_web'."""
        )

    @function_tool
    async def search_book_knowledge(self, query: Annotated[str, "Câu hỏi hoặc từ khóa cần tìm trong sách của người dùng"]) -> str:
        """Tra cứu nội dung trong cuốn sách hiện tại từ database kiến thức."""
        try:
            # Tối ưu RAG: Gọi RPC để thực hiện Vector Search + Metadata Filtering
            data = await search_book_knowledge(query, "87543419-c71f-4d7e-9e0d-036b4ab9b81e")

            print("/////Data...........")
            print(data)

            if not data:
                return "Không tìm thấy thông tin này trong sách."

            formatted_chunks = []
            for i, item in enumerate(data):
                # Format rõ ràng từng đoạn, cung cấp index để LLM biết đây là các đoạn rời rạc
                chunk_text = f"--- Đoạn {i + 1} (Chương ID: ...{item.get('chapter_id', '')[-6:]}, Index: {item.get('chunk_index', 'N/A')}) ---\n{item.get('content', '')}"
                formatted_chunks.append(chunk_text)

            context = "\n\n".join(formatted_chunks)
            print("/////Context...........")
            print(context)
            return f"Thông tin từ sách: {context}"
        except Exception as e:
            return f"Lỗi truy xuất: {str(e)}"

    @function_tool
    async def search_web(self, query: Annotated[str, "Nội dung cần tìm kiếm trên internet"]) -> str:
        """Tìm kiếm thông tin từ Internet."""

        search_result = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=3,
        )
        result_text = "\n".join([f"- {r['content']}" for r in search_result["results"]])

        # Print result_text to console
        print(result_text)

        return result_text


async def entrypoint(ctx: JobContext):
    # Khởi tạo Session
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="models/gemini-2.5-flash-native-audio-latest",
            voice="Puck",
        ),
        vad=silero.VAD.load(),
    )

    # Chạy Agent
    await session.start(
        room=ctx.room,
        agent=TriamAssistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda _: noise_cancellation.BVC(),
            ),
        ),
    )

    # FIX LỖI Ở ĐÂY: Thêm 'instructions='
    await session.generate_reply(instructions="Chào bạn! Tôi là trợ lý ảo TRIAM. Tôi đã sẵn sàng hỗ trợ bạn đọc sách.")


if __name__ == "__main__":
    agents.cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
