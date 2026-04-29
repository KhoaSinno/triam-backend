import asyncio
from typing import Annotated

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    function_tool,
    room_io,
    inference,
    LanguageCode,
)
from livekit.agents.voice import io as voice_io
from livekit.plugins import google, noise_cancellation, silero, deepgram, openai
from supabase import Client, create_client
from tavily import TavilyClient

from app.core.config import settings
from app.services.rag_service import search_book_knowledge

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# Supabase (RAG)
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,
)


class ChatTextOutput(voice_io.TextOutput):
    def __init__(self, room: rtc.Room, topic: str = "lk.chat") -> None:
        super().__init__(label="ChatTextOutput", next_in_chain=None)
        self._room = room
        self._topic = topic
        self._buffer: list[str] = []
        self._flush_task: asyncio.Task[None] | None = None

    async def capture_text(self, text: str) -> None:
        if not text:
            return

        self._buffer.append(text)

    def flush(self) -> None:
        if not self._buffer:
            return

        message = "".join(self._buffer)
        self._buffer.clear()
        preview = message if len(message) <= 120 else f"{message[:120]}..."
        print(f"[Agent] Text output ({len(message)} chars): {preview}")

        async def _publish(text: str) -> None:
            if not self._room.isconnected():
                return
            try:
                await self._room.local_participant.publish_data(
                    text,
                    reliable=True,
                    topic=self._topic,
                )
            except Exception as exc:
                print(f"[Agent] Text output publish failed: {exc}")

        # Flush is sync; schedule async publish.
        self._flush_task = asyncio.create_task(_publish(message))


class TriamAssistant(Agent):
    def __init__(self, book_id: str) -> None:
        super().__init__(
            instructions=(
                "Bạn là Trợ lý TRIAM - Hỗ trợ đọc sách qua giọng nói. "
                "CHỈ SỬ DỤNG 'search_book_knowledge' KHI người dùng đặt câu hỏi liên quan đến nội dung sách. "  # Sửa ở đây
                "Trả lời cực kỳ ngắn gọn (dưới 2 câu), thân thiện. "
                "Nếu không tìm thấy trong sách, mới dùng 'search_web'."
            )
        )
        self.book_id = book_id

    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Cau hoi hoac tu khoa can tim trong sach"],
    ) -> str:
        try:
            data = await search_book_knowledge(query, self.book_id)

            if not data:
                return "RAG don't have data"

            if not isinstance(data, list):
                return "RAG invalid RAG data format"

            formatted_chunks = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    continue
                chapter_id = str(item.get('chapter_id', ''))
                chunk_index = item.get('chunk_index', 'N/A')
                content = item.get('content', '')

                chunk_text = (
                    f"--- Doan {i + 1} (Chuong ID: ...{chapter_id[-6:]}, "
                    f"Index: {chunk_index}) ---\n"
                    f"{content}"
                )
                formatted_chunks.append(chunk_text)

            context = "\n\n".join(formatted_chunks)
            return f"Thong tin tu sach: {context}"
        except Exception as e:
            return f"Loi truy xuat: {str(e)}"

    @function_tool
    async def search_web(
        self,
        query: Annotated[str, "Noi dung can tim kiem tren internet"],
    ) -> str:
        import asyncio

        loop = asyncio.get_event_loop()
        search_result = await loop.run_in_executor(
            None,
            lambda: tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=3,
            ),
        )
        result_text = "\n".join(
            [f"- {r['content']}" for r in search_result["results"]])
        return result_text


async def entrypoint(ctx: JobContext):
    # Bat buoc: connect Room truoc khi start session
    await ctx.connect()

    book_id = ctx.room.name
    print(f"[Agent] Bat dau phien doc sach cho Book ID: {book_id}")

    # session = AgentSession(
    #     stt=inference.STT(
    #         model="deepgram/flux-general",
    #         language="en",
    #     ),
    #     llm=inference.LLM(
    #         model="openai/gpt-5.3-chat-latest",
    #     ),
    #     tts=inference.TTS(
    #         model="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    #         extra_kwargs={
    #             "add_timestamps": False,
    #             "add_phoneme_timestamps": False,
    #             "use_normalized_timestamps": False,
    #         },
    #     ),
    #     vad=silero.VAD.load(),
    # )

    session = AgentSession(
        stt=inference.STT(
            model="deepgram/nova-3",  # Nova-3 nhận diện tiếng Việt tốt hơn Flux hiện tại
            language="vi",           # Thử ép hẳn về "vi" để xem nó còn ra "Hello" không
            extra_kwargs={
                "language_hints": ["vi"],
                "smart_format": True
            }
        ),
        llm=inference.LLM(
            model="openai/gpt-5.3-chat-latest",
        ),
        tts=inference.TTS(
            model="elevenlabs/eleven_flash_v2_5",
            language="vi",  # ÉP NGÔN NGỮ Ở ĐÂY
            extra_kwargs={
                # BẮT BUỘC: Thay voice_id này bằng một giọng thuần Việt
                # Khoa nên lấy từ Voice Library của ElevenLabs
                "voice_id": "Lcf7z35dm7QXBoD0f107",  # Ví dụ Voice ID thuần Việt
                "add_timestamps": True,
                "voice_settings": {
                    "stability": 0.45,        # Giảm để AI nhấn dấu hỏi/ngã chuẩn hơn
                    "similarity_boost": 0.8,   # Tăng để giữ đặc trưng giọng người Việt
                    "style": 0.1,             # Thêm chút cảm xúc
                    "use_speaker_boost": True
                }
            },
        ),
        vad=silero.VAD.load(),
    )

    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        print(f"[Agent] Text input from {participant_id}: {ev.text}")
        await sess.interrupt()
        sess.generate_reply(user_input=ev.text)

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        print(f"[Agent] Data input from {participant_id or 'unknown'}: {text}")
        await session.interrupt()
        session.generate_reply(user_input=text)

    await session.start(
        room=ctx.room,
        agent=TriamAssistant(book_id=book_id),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda _: noise_cancellation.BVC(),
            ),
            text_input=room_io.TextInputOptions(
                text_input_cb=handle_text_input),
            text_output=room_io.TextOutputOptions(
                sync_transcription=False,
                next_in_chain=ChatTextOutput(ctx.room),
            ),
            close_on_disconnect=False,
        ),
    )

    def on_data_received(packet: rtc.DataPacket) -> None:
        if packet.topic != "lk.chat":
            return

        try:
            text = packet.data.decode("utf-8")
        except Exception as exc:
            print(f"[Agent] Data input decode failed: {exc}")
            return

        participant_id = packet.participant.identity if packet.participant else None
        asyncio.create_task(handle_data_input(text, participant_id))

    ctx.room.on("data_received", on_data_received)

    # await session.generate_reply(
    #     instructions=(
    #         "Bạn là trợ lý TRIAM. "
    #         "BẮT BUỘC trả lời bằng tiếng Việt, kể cả khi transcript đầu vào bị nhận diện nhầm là tiếng Anh. "
    #         "Chỉ nói tiếng Anh khi người dùng thực sự yêu cầu."
    #     )
    # )
    await session.say(
        "Chào bạn! Mình là TRIAM. Bạn muốn tìm hiểu gì về cuốn sách này?",
        allow_interruptions=True
    )

if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=lambda: 0.0,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )
