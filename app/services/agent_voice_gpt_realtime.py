import os
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
    room_io,
)
from livekit.agents.llm import ChatMessage as LLMMessage
from livekit.agents.voice import io as voice_io
from livekit.plugins import noise_cancellation, openai
from livekit.plugins.openai.realtime import RealtimeModel
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import ChatMessage
from app.services.rag_service import search_book_knowledge
from app.services.web_search_service import search_web as web_search

# FIX 1: Ép API Key vào biến môi trường để LiveKit SDK tự động nhận diện ngầm
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


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
        log.info(f"Text output ({len(message)} chars): {preview}")

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
                log.info(f"Text output publish failed: {exc}")

        # Flush is sync; schedule async publish.
        self._flush_task = asyncio.create_task(_publish(message))


class TriamAssistant(Agent):
    def __init__(self, document_ids: list[str]) -> None:
        super().__init__(
            instructions=(
                "Bạn là trợ lý AI sách nói TRIAM - Trợ lý đọc sách nói thông minh.\n"
                "\n"
                "## QUY TẮC SỬ DỤNG TOOL (BẮT BUỘC):\n"
                "- LUÔN LUÔN gọi 'search_book_knowledge' TRƯỚC TIÊN cho MỌI câu hỏi về kiến thức, nội dung, khái niệm, chương, đoạn văn hoặc bất kỳ thông tin nào liên quan đến sách.\n"
                "- CHỈ gọi 'search_web' khi: (a) 'search_book_knowledge' trả về không có dữ liệu, HOẶC (b) User hỏi về tin tức, sự kiện hiện tại, thông tin ngoài sách rõ ràng.\n"
                "- KHÔNG được tự trả lời từ bộ nhớ mà không gọi tool khi User hỏi về nội dung sách.\n"
                "\n"
                "## PHONG CÁCH TRẢ LỜI:\n"
                "- Trả lời cực kỳ NGẮN GỌN (2-3 câu), tự nhiên, đi thẳng vào trọng tâm.\n"
                "- Tuyệt đối KHÔNG dùng Markdown (**, *, #, -) và KHÔNG dùng EMOJI."
            )
        )
        self.document_ids = document_ids

    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"],
    ) -> str:
        """
        Tìm kiếm kiến thức, nội dung, khái niệm trong các quyển sách thuộc Study Context hiện tại.
        PHẢI gọi tool này trước tiên cho bất kỳ câu hỏi nào liên quan đến:
        - Nội dung, chương, đoạn văn trong sách
        - Khái niệm, định nghĩa, giải thích thuật ngữ
        - Tóm tắt, phân tích nội dung sách
        - Câu hỏi kiến thức mà User đang học từ sách
        Hệ thống tự động giới hạn tìm kiếm trong tài liệu User đã chọn.
        """
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
        """Tìm kiếm thông tin trên internet khi nội dung không có trong sách."""
        return await web_search(query)


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
        log.info("❌ Không tìm thấy document_ids trong metadata! Thoát.")
        return

    log.info(f"✅ Document IDs từ metadata: {document_ids}")
    log.info(f"🏠 Room Name (session): {ctx.room.name}")
    log.info(f"Bat dau phien doc sach cho Thread ID: {thread_id}")

    # Khởi tạo Model (Sử dụng stream realtime modal như user yêu cầu)
    model = RealtimeModel(model="gpt-4o-mini-realtime-preview", voice="alloy", temperature=0.8, modalities=["audio", "text"])

    session = AgentSession(
        llm=model,
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
            log.info(f"Lỗi khi lưu message: {e}")

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input from {participant_id}: {ev.text}")
        asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        await sess.interrupt()
        sess.generate_reply(user_input=ev.text)

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input from {participant_id or 'unknown'}: {text}")
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        await session.interrupt()
        session.generate_reply(user_input=text)

    def on_data_received(packet: rtc.DataPacket) -> None:
        if packet.topic != "lk.chat":
            return
        try:
            text = packet.data.decode("utf-8")
        except Exception as exc:
            log.info(f"Data input decode failed: {exc}")
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
        if hasattr(session, "chat_ctx") and session.chat_ctx is not None:
            for msg in history_msgs:
                session.chat_ctx.append(role="user" if msg.is_user else "assistant", text=msg.text)
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")

    await session.generate_reply(
        instructions="Chào ông, tôi là TRIAM đây. Ông muốn thảo luận về chương sách nào hôm nay?",
    )


if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=lambda: 0.0,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )
