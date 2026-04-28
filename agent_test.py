from typing import Annotated

from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, function_tool, room_io, inference
from livekit.plugins import google, noise_cancellation, silero
from supabase import Client, create_client
from tavily import TavilyClient

from app.core.config import settings
from app.services.rag_service import search_book_knowledge

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# Khởi tạo Supabase (Dùng cho RAG)
supabase: Client = create_client(
    settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


class TriamAssistant(Agent):
    def __init__(self, book_id: str) -> None:
        super().__init__(
            instructions="""Bạn là Trợ lý TRIAM - Người hỗ trợ đọc sách qua giọng nói.
            1. Luôn dùng 'search_book_knowledge' trước khi trả lời về nội dung sách.
            2. Trả lời cực kỳ ngắn gọn (dưới 2 câu), thân thiện.
            3. Nếu không thấy trong sách, mới dùng 'search_web'."""
        )
        self.book_id = book_id

    @function_tool
    async def search_book_knowledge(self, query: Annotated[str, "Câu hỏi hoặc từ khóa cần tìm trong sách của người dùng"]) -> str:
        """Tra cứu nội dung trong cuốn sách hiện tại từ database kiến thức."""
        try:
            # Tối ưu RAG: Gọi RPC để thực hiện Vector Search + Metadata Filtering
            data = await search_book_knowledge(query, self.book_id)

            print("/////Data...........")
            print(data)
            print("...........Data/////")

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
            print("...........Context/////")
            return f"Thông tin từ sách: {context}"
        except Exception as e:
            return f"Lỗi truy xuất: {str(e)}"

    @function_tool
    async def search_web(self, query: Annotated[str, "Nội dung cần tìm kiếm trên internet"]) -> str:
        """Tìm kiếm thông tin từ Internet."""

        # Tavily Python SDK v0.3+ dùng sync, không có async wrapper
        import asyncio

        loop = asyncio.get_event_loop()
        search_result = await loop.run_in_executor(
            None,
            lambda: tavily_client.search(
                query=query, search_depth="basic", max_results=3),
        )
        result_text = "\n".join(
            [f"- {r['content']}" for r in search_result["results"]])

        # Print result_text to console
        print(result_text)

        return result_text


async def entrypoint(ctx: JobContext):
    # Bắt buộc với pattern WorkerOptions: phải connect Room trước khi start session
    await ctx.connect()

    # Nhận book_id từ thông tin Room (được định nghĩa trong /live-token endpoint)
    book_id = ctx.room.name
    print(f"[Agent] Bắt đầu phiên đọc sách cho Book ID: {book_id}")

    # Khởi tạo Session
    # session = AgentSession(
    #     llm=google.realtime.RealtimeModel(
    #         api_key=settings.GEMINI_API_KEY,
    #         model=settings.GEMINI_MODEL_NATIVE_AUDIO,
    #         voice="Puck",
    #     ),
    #     vad=silero.VAD.load(),
    # )

    session = AgentSession(
        stt=inference.STT(
            model="deepgram/flux-general",
            language="en"
        ),
        llm=inference.LLM(
            model="openai/gpt-5.3-chat-latest",
        ),
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    )

    # Chạy Agent
    await session.start(
        room=ctx.room,
        agent=TriamAssistant(book_id=book_id),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda _: noise_cancellation.BVC(),
            ),
            # Allow user to send text chat
            text_input=room_io.TextInputOptions(),
            # Allow agent to send text chat
            text_output=room_io.TextOutputOptions(),
        ),
    )

    # Start session with a message as the first message
    await session.generate_reply(instructions="Chào bạn! Tôi là trợ lý ảo TRIAM. Tôi đã sẵn sàng hỗ trợ bạn đọc sách.")


if __name__ == "__main__":
    # Tắt tính năng tự động ngắt khi CPU cao + đăng ký đúng agent_name
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=lambda: 0.0,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )
