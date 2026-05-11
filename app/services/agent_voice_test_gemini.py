import os
import asyncio
import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Annotated, Any, Literal, TypedDict, cast

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
# from livekit.plugins.openai.realtime import RealtimeModel

from livekit.plugins.google.realtime import RealtimeModel
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import ChatMessage
from app.services.rag_service import search_book_knowledge as rag_search_book_knowledge
from app.services.web_search_service import search_web as web_search

from google.genai.types import Modality


class DataChannelMessage(TypedDict, total=False):
    v: int
    type: Literal["user_text", "chat", "transcript"]
    role: Literal["user", "assistant"]
    text: str
    id: str
    ts: str
    thread_id: str
    participant_id: str
    topic: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _encode_dc_payload(
    topic: str,
    msg_type: Literal["user_text", "chat", "transcript"],
    role: Literal["user", "assistant"],
    text: str,
    *,
    thread_id: str = "",
    participant_id: str = "",
) -> bytes:
    """Encode payload for LiveKit DataChannel.

    Best-practice is JSON with a stable schema, but allow rolling out gradually.
    """

    payload_mode = os.getenv("TRIAM_DC_PAYLOAD", "text").strip().lower()  # text|json
    if payload_mode != "json":
        return text.encode("utf-8")

    msg: DataChannelMessage = {
        "v": 1,
        "type": msg_type,
        "role": role,
        "text": text,
        "id": str(uuid.uuid4()),
        "ts": _now_iso(),
    }
    if thread_id:
        msg["thread_id"] = thread_id
    if participant_id:
        msg["participant_id"] = participant_id
    # Include topic for debugging/probing (optional)
    msg["topic"] = topic
    return json.dumps(msg, ensure_ascii=False).encode("utf-8")


def _try_decode_dc_payload(data: bytes) -> tuple[str, DataChannelMessage | None]:
    """Decode incoming data. Returns (text, parsed_message_or_None)."""
    try:
        s = data.decode("utf-8")
    except Exception:
        return "", None

    if not s:
        return "", None

    # Try JSON first (new protocol)
    try:
        obj = json.loads(s)
        if isinstance(obj, dict) and isinstance(obj.get("text"), str):
            return cast(str, obj.get("text")), cast(DataChannelMessage, obj)
    except Exception:
        pass

    # Fallback legacy plain text
    return s, None


TRIAM_INSTRUCTIONS = (
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


def _patch_google_genai_live_connect_config() -> None:
    """Patch google-genai schema drift for livekit-plugins-google.

    livekit-plugins-google==1.5.8 passes `history_config` to
    `google.genai.types.LiveConnectConfig`, but google-genai>=1.63.0 no longer
    supports that field (and doesn't define `HistoryConfig`). This keeps the
    realtime test script runnable without downgrading dependencies.
    """

    try:
        import google.genai.types as genai_types

        if "history_config" not in getattr(genai_types.LiveConnectConfig, "model_fields", {}):
            original_cls = genai_types.LiveConnectConfig

            def _LiveConnectConfig(*args, **kwargs):
                kwargs.pop("history_config", None)
                return original_cls(*args, **kwargs)

            genai_types.LiveConnectConfig = _LiveConnectConfig  # type: ignore[assignment]

        if not hasattr(genai_types, "HistoryConfig"):
            class _HistoryConfig:  # pragma: no cover
                def __init__(self, *args, **kwargs):
                    pass

            genai_types.HistoryConfig = _HistoryConfig  # type: ignore[attr-defined]
    except Exception as exc:
        log.info(f"google-genai patch skipped/failed: {exc}")


_patch_google_genai_live_connect_config()


def _silence_noisy_loggers() -> None:
    # With loguru intercept enabled, Python logging DEBUG from HTTP/2 stacks can
    # leak sensitive headers (e.g., apikey/authorization). Keep those quiet.
    for name in (
        "hpack",
        "hpack.hpack",
        "hpack.table",
        "h2",
        "httpcore",
        "httpx",
    ):
        logging.getLogger(name).setLevel(logging.WARNING)


_silence_noisy_loggers()

# FIX 1: Ép API Key vào biến môi trường để LiveKit SDK tự động nhận diện ngầm
# os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY


class ChatTextOutput(voice_io.TextOutput):
    def __init__(self, room: rtc.Room, save_cb=None, topic: str = "lk.transcript") -> None:
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
                payload = _encode_dc_payload(
                    self._topic,
                    msg_type="transcript",
                    role="assistant",
                    text=text,
                )
                await self._room.local_participant.publish_data(
                    payload,
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
            instructions=TRIAM_INSTRUCTIONS
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
            data = await rag_search_book_knowledge(query, self.document_ids)

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
    # model = RealtimeModel(model="gpt-4o-mini-realtime-preview", voice="alloy", temperature=0.8, modalities=["audio", "text"])
    
    async def _resolve_live_modalities(model_name: str) -> list[Modality]:
        """Try to keep voice+chat in one session.

        Some Gemini Live audio models reject TEXT in response modalities.
        We probe with google-genai and fall back to AUDIO-only to keep the
        LiveKit session runnable.
        """

        desired = [Modality.AUDIO, Modality.TEXT]
        try:
            import google.genai as genai
            from google.genai import types

            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            cfg = types.LiveConnectConfig(response_modalities=desired)

            async with client.aio.live.connect(model=model_name, config=cfg):
                return desired
        except Exception as exc:
            log.info(
                "Gemini Live does not accept TEXT modality; falling back to AUDIO-only. "
                f"Reason: {type(exc).__name__}: {exc}"
            )
            return [Modality.AUDIO]

    model_name = "gemini-2.5-flash-native-audio-preview-12-2025"
    modalities = await _resolve_live_modalities(model_name)

    model = RealtimeModel(
        model=model_name,
        api_key=settings.GEMINI_API_KEY,
        vertexai=False,
        voice="Puck",
        temperature=0.8,
        modalities=modalities,
    )

    session = AgentSession(
        llm=model,
    )

    def _session_running(sess: AgentSession) -> bool:
        # LiveKit Agents doesn't expose an official is_running flag;
        # generate_reply() raises when _activity is None.
        return getattr(sess, "_activity", None) is not None

    def _safe_generate_reply(
        sess: AgentSession,
        *,
        user_input: str | None = None,
        instructions: str | None = None,
    ) -> None:
        if not _session_running(sess):
            log.info("AgentSession isn't running; skipping generate_reply")
            return
        try:
            if user_input is not None:
                sess.generate_reply(user_input=user_input)
            elif instructions is not None:
                sess.generate_reply(instructions=instructions)
            else:
                return
        except RuntimeError as exc:
            log.info(f"generate_reply skipped: {exc}")

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

    async def _publish_chat_text(text: str) -> None:
        if not text:
            return
        if not ctx.room.isconnected():
            return
        try:
            payload = _encode_dc_payload(
                "lk.chat",
                msg_type="chat",
                role="assistant",
                text=text,
                thread_id=thread_id,
            )
            await ctx.room.local_participant.publish_data(
                payload,
                reliable=True,
                topic="lk.chat",
            )
        except Exception as exc:
            log.info(f"Chat publish failed: {exc}")

    def _format_rag_context(data: object) -> str:
        if not data or not isinstance(data, list):
            return ""
        chunks: list[str] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            chapter_id = str(item.get("chapter_id", ""))
            chunk_index = item.get("chunk_index", "N/A")
            content = str(item.get("content", "")).strip()
            if not content:
                continue
            chunks.append(
                f"[Chapter ...{chapter_id[-6:]} | Chunk {chunk_index}]\n{content}"
            )
        return "\n\n".join(chunks)

    async def _generate_chat_text_reply(user_text: str) -> str:
        """Cheaper text-only reply for chat UI (separate from voice/audio)."""
        try:
            import google.genai as genai
            from google.genai import types

            rag_data = await rag_search_book_knowledge(user_text, document_ids)
            rag_context = _format_rag_context(rag_data)

            prompt_parts = []
            if rag_context:
                prompt_parts.append(f"Book Knowledge:\n{rag_context}")
            else:
                prompt_parts.append("Book Knowledge: (no relevant content found)")
            prompt_parts.append(f"User: {user_text}")
            prompt_parts.append("Assistant:")
            contents = "\n\n".join(prompt_parts)

            text_model = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.0-flash")
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            resp = await client.aio.models.generate_content(
                model=text_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=TRIAM_INSTRUCTIONS,
                    temperature=0.2,
                    max_output_tokens=256,
                ),
            )
            reply = (getattr(resp, "text", None) or "").strip()
            if reply:
                log.info(f"Chat text generated ({len(reply)} chars) via {text_model}")
            return reply
        except Exception as exc:
            log.info(f"Text chat generation failed: {type(exc).__name__}: {exc}")
            return ""

    _chat_text_task: asyncio.Task[None] | None = None

    def _schedule_chat_text_reply(user_text: str) -> None:
        nonlocal _chat_text_task
        if not user_text:
            return

        async def _run() -> None:
            try:
                reply = await _generate_chat_text_reply(user_text)
                if not reply:
                    return
                asyncio.create_task(asyncio.to_thread(_save_message, reply, False))
                await _publish_chat_text(reply)
            except asyncio.CancelledError:
                return

        if _chat_text_task and not _chat_text_task.done():
            _chat_text_task.cancel()
        _chat_text_task = asyncio.create_task(_run())

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input from {participant_id}: {ev.text}")
        asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        if _env_flag("TRIAM_TEXT_INPUT_VOICE_REPLY", default=False):
            await sess.interrupt()
            _safe_generate_reply(sess, user_input=ev.text)
        _schedule_chat_text_reply(ev.text)

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input from {participant_id or 'unknown'}: {text}")
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        if _env_flag("TRIAM_TEXT_INPUT_VOICE_REPLY", default=False):
            await session.interrupt()
            _safe_generate_reply(session, user_input=text)
        _schedule_chat_text_reply(text)

    def _extract_event_text(msg: object) -> str:
        if msg is None:
            return ""
        if isinstance(msg, str):
            return msg.strip()

        # Common shapes across LiveKit Agents / LLM providers
        for attr in ("text", "transcript", "content"):
            try:
                val = getattr(msg, attr)
            except Exception:
                val = None

            if isinstance(val, str) and val.strip():
                return val.strip()

            if isinstance(val, list) and val:
                parts: list[str] = []
                for p in val:
                    if isinstance(p, str) and p.strip():
                        parts.append(p.strip())
                        continue
                    t = getattr(p, "text", None)
                    if isinstance(t, str) and t.strip():
                        parts.append(t.strip())
                joined = " ".join(parts).strip()
                if joined:
                    return joined

        inner = getattr(msg, "message", None)
        if inner is not None and inner is not msg:
            return _extract_event_text(inner)

        return ""

    def on_data_received(packet: rtc.DataPacket) -> None:
        if packet.topic != "lk.chat":
            return
        try:
            # Avoid feedback loops if local participant messages are echoed.
            if (
                packet.participant
                and ctx.room.local_participant
                and packet.participant.identity == ctx.room.local_participant.identity
            ):
                return
        except Exception:
            pass
        text, parsed = _try_decode_dc_payload(packet.data)
        if not text:
            return
        # If FE sends JSON, accept only user_text (or unknown) as an input signal.
        if parsed and parsed.get("type") in {"chat", "transcript"}:
            return
        participant_id = packet.participant.identity if packet.participant else None
        asyncio.create_task(handle_data_input(text, participant_id))

    ctx.room.on("data_received", on_data_received)

    @session.on("user_speech_committed")  # type: ignore[arg-type]
    def on_user_speech(msg: LLMMessage):
        content = _extract_event_text(msg)
        log.debug(f"user_speech_committed received ({type(msg).__name__})")
        if content:
            asyncio.create_task(asyncio.to_thread(_save_message, content, True))
            # Generate cheap text reply for chat UI from the committed transcript.
            _schedule_chat_text_reply(content)

    @session.on("agent_speech_committed")  # type: ignore[arg-type]
    def on_agent_speech(msg: LLMMessage):
        content = _extract_event_text(msg)
        log.debug(f"agent_speech_committed received ({type(msg).__name__})")
        if content:
            asyncio.create_task(asyncio.to_thread(_save_message, content, False))

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
                # Publish transcripts on a separate topic; chat replies are published via _publish_chat_text.
                next_in_chain=ChatTextOutput(ctx.room, save_cb=_save_message, topic="lk.transcript"),
            ),
            close_on_disconnect=True,
        ),
    )

    # Load history
    def _load_history():
        if not thread_id:
            return []
        with Session(engine) as db:
            return db.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()  # type: ignore[attr-defined]

    try:
        history_msgs = await asyncio.to_thread(_load_history)
        if hasattr(session, "chat_ctx") and session.chat_ctx is not None:  # type: ignore[attr-defined]
            for msg in history_msgs:
                session.chat_ctx.append(role="user" if msg.is_user else "assistant", text=msg.text)  # type: ignore[attr-defined]
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")

    _safe_generate_reply(
        session,
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
