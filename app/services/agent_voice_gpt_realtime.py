import asyncio
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Annotated, Any, cast

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    function_tool,
    room_io,
)
from livekit.agents import (
    llm as agents_llm,
)
from livekit.agents.llm import ChatMessage as LLMMessage
from livekit.agents.voice import io as voice_io
from livekit.plugins import noise_cancellation
from livekit.plugins.openai import LLM as OpenAILLM
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
    def __init__(
        self,
        room: rtc.Room,
        save_cb=None,
        topic: str = "lk.chat",
        transcript_topic: str | None = None,
    ) -> None:
        super().__init__(label="ChatTextOutput", next_in_chain=None)
        self._room = room
        self._topic = topic
        self._transcript_topic = transcript_topic
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

        async def _publish(topic: str, payload: str) -> None:
            if not self._room.isconnected():
                return
            try:
                await self._room.local_participant.publish_data(
                    payload,
                    reliable=True,
                    topic=topic,
                )
            except Exception as exc:
                log.info(f"Text output publish failed: {exc}")

        # Flush is sync; schedule async publish.
        self._flush_task = asyncio.create_task(_publish(self._topic, message))

        if self._transcript_topic:
            transcript_payload = {
                "v": 1,
                "type": "transcript",
                "role": "assistant",
                "text": message,
                "id": str(uuid.uuid4()),
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            self._flush_task = asyncio.create_task(
                _publish(
                    self._transcript_topic,
                    json.dumps(transcript_payload, ensure_ascii=False).encode("utf-8"),
                )
            )


class TriamAssistant(Agent):
    def __init__(self, document_ids: list[str]) -> None:
        super().__init__(
            instructions=(
                "Bạn là trợ lý AI sách nói TRIAM - Trợ lý đọc sách nói thông minh.\n"
                "\n"
                "## QUY TẮC SỬ DỤNG TOOL (BẮT BUỘC TUÂN THỦ):\n"
                "- LUÔN LUÔN gọi 'search_book_knowledge' TRƯỚC TIÊN cho MỌI câu hỏi về kiến thức, nội dung, khái niệm hoặc bất kỳ thông tin nào liên quan đến sách.\n"
                "- Nếu 'search_book_knowledge' không trả về thông tin đủ và liên quan:\n"
                "  → PHẢI gọi 'ask_web_search_permission' để xin phép user trước.\n"
                "  → TUYỆT ĐỐI KHÔNG gọi 'execute_web_search' trực tiếp mà không có bước xin phép trước.\n"
                "- Chỉ gọi 'execute_web_search' khi user đã xác nhận đồng ý ở turn hội thoại trước.\n"
                "- KHÔNG được tự trả lời từ bộ nhớ mà không gọi tool khi user hỏi về nội dung sách.\n"
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
        """
        [VOICE - Pha 2] Chỉ gọi tool này SAU KHI user đã xác nhận đồng ý ở turn hội thoại trước.
        THỰC HIỆN tìm kiếm thực sự trên internet và trả về kết quả.
        TRAO ĐỔI VUI: Nếu chưa có turn hỏi xin phép trước → không gọi tool này.
        """
        log.info(f"🌐 [Voice] Thực hiện web search: {query}")
        return await web_search(query)

    @function_tool
    async def ask_web_search_permission(
        self,
        query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"],
    ) -> str:
        """
        [VOICE - Pha 1] Gọi tool này khi search_book_knowledge không có đủ thông tin liên quan.
        Tool này KHÔNG tìm web ngay. Nó chỉ trả về mẫu câu hỏi xác nhận để AI đọc lên cho user nghe.
        Sau khi AI đọc câu hỏi này, AI kết thúc turn và đợi user trả lời ở turn tiếp theo.
        Nếu user đồng ý (bất kỳ cách nào) → AI tự quyết định gọi 'search_web'.
        Nếu user từ chối → AI không gọi tool và trả lời phù hợp.
        """
        log.info(f"🔔 [Voice] Xin phép tìm web với query: {query}")
        # Trả về câu hỏi xác nhận → AI sẽ đọc câu này ra giọng nói cho user
        return (
            f"Thông tin về '{query}' không có trong sách. "
            f"Bạn có muốn tôi tìm kiếm thêm trên internet không?"
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    try:
        job_meta = json.loads(ctx.job.metadata or "{}")
        # TODO: Hardcoded to test console => My intention
        # book_id = job_meta.get("book_id", "9cda7cbc-c9e4-4325-9fc9-cb74d71e14b3")
        # thread_id = job_meta.get("thread_id", "f25f309f-1dbb-4517-90b9-5fbbc88e3070")
        book_id = job_meta.get("book_id", "")
        thread_id = job_meta.get("thread_id", "")
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

    thread_uuid: uuid.UUID | None = None
    if thread_id:
        try:
            thread_uuid = uuid.UUID(thread_id)
        except ValueError:
            log.info(f"Invalid thread_id UUID; skipping DB persistence: {thread_id}")
            thread_uuid = None

    def _is_model_not_found(exc: Exception) -> bool:
        msg = str(exc)
        return "NOT_FOUND" in msg or "404" in msg or "model" in msg.lower() and "not" in msg.lower() and "found" in msg.lower()

    configured_model_name = settings.OPENAI_STREAM_MODEL_NAME
    model_candidates = [configured_model_name, "gpt-realtime-1.5"]
    # de-dupe while preserving order
    seen_models: set[str] = set()
    model_candidates = [m for m in model_candidates if not (m in seen_models or seen_models.add(m))]

    agent_instance = TriamAssistant(document_ids=document_ids)
    chat_llm = OpenAILLM(model="gpt-4o-mini", temperature=0.7)

    # Toggle: cho phép AI tự động tìm web khi sách không đủ thông tin.
    # Frontend bật/tắt qua DataChannel topic "lk.control".
    web_search_enabled: bool = False

    session: AgentSession

    async def _publish_transcript(role: str, text: str) -> None:
        if not text or not ctx.room.isconnected():
            return
        payload = {
            "v": 1,
            "type": "transcript",
            "role": role,
            "text": text,
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        try:
            await ctx.room.local_participant.publish_data(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                reliable=True,
                topic="lk.transcript",
            )
        except Exception as exc:
            log.info(f"Transcript publish failed: {exc}")

    def _save_message(text: str, is_user: bool):
        if not thread_uuid:
            return
        try:
            with Session(engine) as db:
                new_msg = ChatMessage(thread_id=thread_uuid, is_user=is_user, text=text, source="livekit", timestamp=datetime.now(timezone.utc))
                db.add(new_msg)
                db.commit()
        except Exception as e:
            log.info(f"Lỗi khi lưu message: {e}")

    saved_user_transcripts: set[str] = set()

    async def _save_and_publish_user_transcript(text: str) -> None:
        normalized = " ".join(text.split())
        if not normalized:
            return

        # LiveKit realtime transcription can arrive through multiple event paths.
        # Keep user voice persistence idempotent for this in-memory session.
        if normalized in saved_user_transcripts:
            return
        saved_user_transcripts.add(normalized)

        await asyncio.to_thread(_save_message, normalized, True)
        await _publish_transcript("user", normalized)

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent

    async def _chat_naive_rag(user_text: str) -> str:
        """Chế độ RAG Naive (toggle TẮT): luôn search sách, không dùng tool web."""
        log.info("[Text Chat] Chế độ Naive RAG (web search TẮT)")
        search_result = await agent_instance.search_book_knowledge(user_text)
        temp_ctx = session.history.copy()
        if search_result and "RAG don't have data" not in search_result:
            temp_ctx.add_message(
                role="system",
                content=f"Thông tin trích xuất từ sách (dùng để trả lời):\n{search_result}",
            )
        response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
        return response.text

    async def _chat_with_agentic_loop(user_text: str) -> str:
        """
        Chế độ Agentic (toggle BẬT): gpt-4o-mini tự quyết định dùng tool nào.
        Dùng LLMStream.collect() + llm.execute_function_call() theo chuẩn SDK.
        LLM tự phán xét RAG có đủ không, nếu không tự gọi search_web.
        """
        log.info("[Text Chat] Chế độ Agentic Loop (web search BẬT)")

        # Tạo standalone async functions để tránh trực tiếp dùng agent_instance.tools.
        # ToolContext.__init__ nội bộ gọi find_function_tools(self) → crash khi agent
        # chưa có activity context. Ta wrap thủ công bằng @function_tool decorator.
        async def _search_book(
            query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"]
        ) -> str:
            """Tìm kiếm kiến thức trong sách thuộc Study Context hiện tại."""
            return await agent_instance.search_book_knowledge(query)

        async def _search_web(
            query: Annotated[str, "Nội dung cần tìm kiếm trên internet"]
        ) -> str:
            """Tìm kiếm thông tin trên internet khi nội dung không có trong sách."""
            return await agent_instance.search_web(query)

        book_fn_tool = function_tool(_search_book)
        web_fn_tool = function_tool(_search_web)
        standalone_tools = [book_fn_tool, web_fn_tool]

        # Tạo ToolContext thủ công để tránh gọi __init__ (nó gọi find_function_tools(self))
        tool_ctx = agents_llm.ToolContext.__new__(agents_llm.ToolContext)
        tool_ctx._tools = standalone_tools
        tool_ctx._fnc_tools_map = {t.info.name: t for t in standalone_tools}
        tool_ctx._provider_tools = []
        tool_ctx._tool_sets = []

        ctx_copy = session.history.copy()
        # Inject ngày giờ thực từ server và quy tắc dùng tool.
        # Lý do inject datetime: Tavily có thể trả về trang cũ được cache → ngày sai.
        # Ngày/giờ là fact của server, không cần web search.
        now_str = datetime.now(timezone.utc).astimezone().strftime("%A, %d/%m/%Y %H:%M (UTC+7)")
        ctx_copy.add_message(
            role="system",
            content=(
                f"## THÔNG TIN HỆ THỐNG:\n"
                f"- Ngày giờ hiện tại (server): {now_str}\n"
                f"- Hãy dùng thông tin ngày này khi user hỏi về ngày/giờ hiện tại.\n"
                f"\n"
                f"## QUY TẮC SỬ DỤNG TOOL (BẮT BUỘC):\n"
                f"- Câu hỏi về nội dung sách: gọi `_search_book` trước tiên.\n"
                f"- Câu hỏi về giá cả, tin tức, sự kiện mới, thông tin ngoài sách: "
                f"PHẢI gọi `_search_web`.\n"
                f"- Sau khi `_search_book` không đủ thông tin → gọi `_search_web` để bổ sung.\n"
                f"- Chỉ trả lời bằng text SAU KHI đã dùng tool phù hợp."
            ),
        )

        MAX_STEPS = 4  # Giới hạn vòng lặp tool call, tránh loop vô tận
        for step in range(MAX_STEPS):
            response = await chat_llm.chat(
                chat_ctx=ctx_copy,
                tools=standalone_tools,
            ).collect()

            # Nếu không có tool call → LLM đã có câu trả lời cuối
            if not response.tool_calls:
                log.info(f"[Agentic] Hoàn thành sau {step + 1} bước. Reply: {len(response.text)} chars")
                return response.text

            # Thực thi tool calls theo đúng chuẩn SDK
            log.info(f"[Agentic] Bước {step + 1}: thực thi {len(response.tool_calls)} tool call(s)")
            for tc in response.tool_calls:
                result = await agents_llm.execute_function_call(tc, tool_ctx)
                ctx_copy.insert(result.fnc_call)
                if result.fnc_call_out:
                    ctx_copy.insert(result.fnc_call_out)

        # Hết MAX_STEPS, trả về text của lần gọi cuối cùng
        log.warning("[Agentic] Đạt giới hạn MAX_STEPS, trả về text hiện tại")
        return response.text

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input from {participant_id or 'unknown'}: {text}")

        # Save DB and update transcript immediately (await to guarantee insertion order)
        await asyncio.to_thread(_save_message, text, True)
        asyncio.create_task(_publish_transcript("user", text))

        # Interrupt if livekit is currently speaking
        await session.interrupt()

        # Put input into shared memory
        session.history.add_message(role="user", content=text)

        try:
            # Phân nhánh dựa theo toggle web_search_enabled
            if web_search_enabled:
                full_reply = await _chat_with_agentic_loop(text)
            else:
                full_reply = await _chat_naive_rag(text)

            log.info(f"LLM Reply completed. Length: {len(full_reply)}")

            if full_reply:
                # Save DB and update transcript immediately
                await asyncio.to_thread(_save_message, full_reply, False)
                asyncio.create_task(_publish_transcript("assistant", full_reply))

                # Publish raw text to data channel for UI
                try:
                    await ctx.room.local_participant.publish_data(
                        full_reply.encode("utf-8"),
                        reliable=True,
                        topic="lk.chat",
                    )
                except Exception as exc:
                    log.info(f"Data output publish failed: {exc}")

            # Update shared memory with assistant reply
            session.history.add_message(role="assistant", content=full_reply)
        except Exception as e:
            log.error(f"Error in handle_data_input: {e}")

    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input from {participant_id}: {ev.text}")
        # call handle_data_input to process the text input
        await handle_data_input(ev.text, participant_id)
        # asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        # await sess.interrupt()
        # try:
        #     sess.generate_reply(user_input=ev.text)
        # except Exception as exc:
        #     msg = str(exc)
        #     if "NOT_FOUND" in msg or "404" in msg:
        #         log.info(f"Realtime model unavailable ({configured_model_name}); please set OPENAI_STREAM_MODEL_NAME. Error: {exc}")
        #     raise

    def on_data_received(packet: rtc.DataPacket) -> None:
        nonlocal web_search_enabled
        try:
            raw = packet.data.decode("utf-8")
        except Exception as exc:
            log.info(f"Data input decode failed: {exc}")
            return

        # --- Kênh điều khiển: bật/tắt web search ---
        if packet.topic == "lk.control":
            try:
                payload = json.loads(raw)
                if payload.get("type") == "toggle_web_search":
                    web_search_enabled = bool(payload.get("enabled", False))
                    log.info(f"🌐 Web search toggle: {'BẬT' if web_search_enabled else 'TẮT'}")
            except json.JSONDecodeError:
                log.info("lk.control: payload không phải JSON hợp lệ")
            return

        # --- Kênh chat thông thường ---
        if packet.topic == "lk.chat":
            participant_id = packet.participant.identity if packet.participant else None
            asyncio.create_task(handle_data_input(raw, participant_id))

    ctx.room.on("data_received", on_data_received)

    def _attach_session_handlers(sess: AgentSession) -> None:
        @sess.on("user_input_transcribed")  # type: ignore[arg-type]
        def on_user_input_transcribed(ev):
            is_final = bool(getattr(ev, "is_final", False))
            transcript = str(getattr(ev, "transcript", "") or "").strip()
            log.info(
                f"user_input_transcribed received: final={is_final}, chars={len(transcript)}"
            )
            if is_final and transcript:
                asyncio.create_task(_save_and_publish_user_transcript(transcript))

        @sess.on("user_speech_committed")  # type: ignore[arg-type]
        def on_user_speech(msg: LLMMessage):
            content = getattr(msg, "content", getattr(msg, "text", ""))
            if content:
                text = str(content)
                asyncio.create_task(_save_and_publish_user_transcript(text))
                # Ghi vào session.history để gpt-4o-mini (text chat) cũng thấy
                sess.history.add_message(role="user", content=text)

        @sess.on("agent_speech_committed")  # type: ignore[arg-type]
        def on_agent_speech(msg: LLMMessage):
            content = getattr(msg, "content", getattr(msg, "text", ""))
            if content:
                text = str(content)
                asyncio.create_task(asyncio.to_thread(_save_message, text, False))
                asyncio.create_task(_publish_transcript("assistant", text))
                # Ghi vào session.history để gpt-4o-mini (text chat) cũng thấy
                sess.history.add_message(role="assistant", content=text)

    # Start session with fallback when a configured model is unavailable.
    last_start_exc: Exception | None = None
    for model_name in model_candidates:
        try:
            log.info(f"Starting realtime session with model: {model_name}")
            model = RealtimeModel(
                model=model_name,
                voice="alloy",
                temperature=0.8,
                modalities=["audio", "text"],
            )
            session = AgentSession(llm=model)
            _attach_session_handlers(session)

            await session.start(
                room=ctx.room,
                agent=agent_instance,
                room_options=room_io.RoomOptions(
                    audio_input=room_io.AudioInputOptions(
                        noise_cancellation=lambda _: noise_cancellation.BVC(),
                    ),
                    text_input=room_io.TextInputOptions(  # type: ignore[call-arg]
                        text_input_cb=handle_text_input
                    ),
                    text_output=room_io.TextOutputOptions(
                        sync_transcription=False,
                        next_in_chain=ChatTextOutput(
                            ctx.room,
                            save_cb=_save_message,
                            topic="lk.chat",
                            transcript_topic="lk.transcript",
                        ),
                    ),
                    close_on_disconnect=True,
                ),
            )

            configured_model_name = model_name
            break
        except Exception as exc:
            last_start_exc = exc
            if _is_model_not_found(exc) and model_name != model_candidates[-1]:
                log.info(f"Realtime model not available ({model_name}); trying fallback")
                continue
            raise

    if last_start_exc is not None and not ctx.room.isconnected():
        # Defensive: in case we failed before connecting properly.
        raise last_start_exc

    # Load history
    def _load_history():
        if not thread_uuid:
            return []
        with Session(engine) as db:
            # SQLModel typing sometimes marks timestamp as datetime; avoid .asc() to reduce type-check noise.
            return db.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_uuid).order_by(cast(Any, ChatMessage.timestamp))).all()

    try:
        history_msgs = await asyncio.to_thread(_load_history)
        # type: ignore[attr-defined]
        if hasattr(session, "history") and session.history is not None:
            for msg in history_msgs:
                # type: ignore[attr-defined]
                session.history.add_message(role="user" if msg.is_user else "assistant", content=msg.text)
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
