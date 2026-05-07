import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Annotated

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    function_tool,
    inference,
    room_io,
)
from livekit.agents.llm import ChatMessage as LLMMessage
from livekit.agents.voice import io as voice_io
from livekit.plugins import noise_cancellation, silero
from sqlmodel import Session, select
from supabase import Client, create_client
from tavily import TavilyClient

from app.core.config import settings
from app.db.database import engine
from app.models.db_models import ChatMessage
from app.services.rag_service import search_book_knowledge

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# Supabase (RAG)
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,
)


class ChatTextOutput(voice_io.TextOutput):
    def __init__(self, room: rtc.Room, save_cb=None, topic: str = "lk.chat") -> None:
        super().__init__(label="ChatTextOutput", next_in_chain=None)
        self._room = room
        self._topic = topic
        self._buffer: list[str] = []
        self._flush_task: asyncio.Task[None] | None = None
        self._save_cb = save_cb

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

        if self._save_cb:
            asyncio.create_task(asyncio.to_thread(self._save_cb, message, False))

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
    def __init__(self, document_ids: list[str]) -> None:
        super().__init__(
            instructions=(
                "Bạn là trợ lý AI sách nói TRIAM - Trợ lý đọc sách nói thông minh.\n"
                "1. Bạn đang ở trong một 'Study Context' (Ngữ cảnh học tập) chứa các sách mà User đã chọn.\n"
                "2. Khi User hỏi về kiến thức, hoặc nhắc tới 'quyển sách này', TUYỆT ĐỐI PHẢI GỌI hàm 'search_book_knowledge' để tìm kiếm. Truyền thẳng câu hỏi của User vào biến query (không cần hỏi lại tên sách vì hệ thống đã tự động giới hạn vùng tìm kiếm).\n"
                "3. Trả lời cực kỳ NGẮN GỌN (dưới 2-3 câu), tự nhiên rành mạch, đi thẳng vào trọng tâm câu hỏi.\n"
                "4. Tuyệt đối KHÔNG SỬ DỤNG Markdown (không dùng dấu **, *, #, -) và KHÔNG SỬ DỤNG EMOJI trong câu trả lời.\n"
                "5. Chỉ dùng 'search_web' nếu nội dung không có trong sách."
            )
        )
        self.document_ids = document_ids

    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"],
    ) -> str:
        try:
            data = await search_book_knowledge(query, self.document_ids)

            if not data:
                return "RAG don't have data"

            if not isinstance(data, list):
                return "RAG invalid RAG data format"

            formatted_chunks = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    continue
                chapter_id = str(item.get("chapter_id", ""))
                chunk_index = item.get("chunk_index", "N/A")
                content = item.get("content", "")

                chunk_text = f"--- Segment {i + 1} (Chapter ID: ...{chapter_id[-6:]}, Index: {chunk_index}) ---\n{content}"
                formatted_chunks.append(chunk_text)

            context = "\n\n".join(formatted_chunks)
            return f"Book Knowledge: {context}"
        except Exception as e:
            return f"Error: {str(e)}"

    @function_tool
    async def search_web(
        self,
        query: Annotated[str, "Nội dung cần tìm kiếm trên internet"],
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
        result_text = "\n".join([f"- {r['content']}" for r in search_result["results"]])
        return result_text


async def entrypoint(ctx: JobContext):

    await ctx.connect()

    try:
        job_meta = json.loads(ctx.job.metadata or "{}")
        # TODO: Hardcoded to test console => My intention
        book_id = job_meta.get("book_id", "9cda7cbc-c9e4-4325-9fc9-cb74d71e14b3")
        thread_id = job_meta.get("thread_id", "f25f309f-1dbb-4517-90b9-5fbbc88e3070")
        document_ids = job_meta.get("document_ids", [])

        if book_id and not document_ids:
            document_ids = [book_id]

    except (json.JSONDecodeError, AttributeError, TypeError):
        thread_id = ""
        document_ids = []

    if not document_ids:
        print("[Agent] ❌ Không tìm thấy document_ids trong metadata! Thoát.")
        return

    print(f"[Agent] ✅ Document IDs từ metadata: {document_ids}")
    print(f"[Agent] 🏠 Room Name (session): {ctx.room.name}")
    print(f"[Agent] Bat dau phien doc sach cho Thread ID: {thread_id}")

    session = AgentSession(
        stt=inference.STT(
            model="deepgram/nova-3",  # Nova-3 is more accurate for Vietnamese than Flux-General
            language="vi",
            extra_kwargs={"language_hints": ["vi"], "smart_format": True},
        ),
        llm=inference.LLM(
            model="openai/gpt-5.3-chat-latest",
        ),
        tts=inference.TTS(
            model="elevenlabs/eleven_flash_v2_5",
            language="vi",
            extra_kwargs={
                "voice_id": "Lcf7z35dm7QXBoD0f107",  # Custom voice Vietnamese - Linh
                "add_timestamps": True,
                "voice_settings": {
                    "stability": 0.45,  # Giảm để AI nhấn dấu hỏi/ngã chuẩn hơn
                    "similarity_boost": 0.8,  # Tăng để giữ đặc trưng giọng người Việt
                    "style": 0.1,  # Thêm chút cảm xúc
                    "use_speaker_boost": True,
                },
            },
        ),
        vad=silero.VAD.load(),
    )

    def _save_message(text: str, is_user: bool):
        if not thread_id:
            return
        try:
            with Session(engine) as db:
                new_msg = ChatMessage(thread_id=uuid.UUID(thread_id), is_user=is_user, text=text, source="livekit", timestamp=datetime.now(timezone.utc))
                db.add(new_msg)
                db.commit()
        except Exception as e:
            print(f"[Agent] Lỗi khi lưu message: {e}")

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent,
    # because TextInputEvent may not be supported or reliable in all client implementations. By listening to data packets directly, we can ensure that text input works consistently regardless of the client.
    # THIS IS A TEXT STREAM implement
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        print(f"[Agent] Text input from {participant_id}: {ev.text}")
        asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        await sess.interrupt()
        sess.generate_reply(user_input=ev.text)

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        print(f"[Agent] Data input from {participant_id or 'unknown'}: {text}")
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        await session.interrupt()
        session.generate_reply(user_input=text)

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

    @session.on("user_speech_committed")
    def on_user_speech(msg: LLMMessage):
        content = getattr(msg, "content", getattr(msg, "text", ""))
        if content:
            asyncio.create_task(asyncio.to_thread(_save_message, str(content), True))

    @session.on("agent_speech_committed")
    def on_agent_speech(msg: LLMMessage):
        content = getattr(msg, "content", getattr(msg, "text", ""))
        if content:
            asyncio.create_task(asyncio.to_thread(_save_message, str(content), False))

    await session.start(
        room=ctx.room,
        agent=TriamAssistant(document_ids=document_ids),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda _: noise_cancellation.BVC(),
            ),
            text_input=room_io.TextInputOptions(text_input_cb=handle_text_input),
            text_output=room_io.TextOutputOptions(
                sync_transcription=False,
                next_in_chain=ChatTextOutput(ctx.room, save_cb=_save_message),
            ),
            close_on_disconnect=True,
        ),
    )

    # Load history
    def _load_history():
        if not thread_id:
            return []
        with Session(engine) as db:
            return db.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()

    try:
        history_msgs = await asyncio.to_thread(_load_history)
        if hasattr(session, "chat_ctx") and session.chat_ctx:
            for msg in history_msgs:
                session.chat_ctx.append(role="user" if msg.is_user else "assistant", text=msg.text)
    except Exception as e:
        print(f"[Agent] Lỗi khi load history: {e}")

    await session.generate_reply(
        instructions=("Chào bạn! Tôi là trợ lý ảo TRIAM. Tôi sẵn sàng hỗ trợ bạn ngay lúc này."),
    )


if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=lambda: 0.0,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )
