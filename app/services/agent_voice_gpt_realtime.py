import asyncio
import json
import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    ConversationItemAddedEvent,
    FunctionToolsExecutedEvent,
    JobContext,
    JobExecutorType,
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
from openai.types.realtime import AudioTranscription

from app.core.config import settings
from app.core.logger import log
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer
from app.services.voice_agent.contracts import LK_CHAT_TOPIC, LK_CONTROL_TOPIC, VoiceJobMetadata
from app.services.voice_agent.rag_context import format_rag_context, search_voice_book_context, trim_text
from app.services.voice_agent.transcript_store import VoiceTranscriptStore, normalize_transcript_text
from app.services.voice_agent.web_permission_intent_classifier import normalize_intent_text
from app.services.voice_agent.web_permission_policy import WebSearchPermissionPolicy
from app.services.web_search_service import search_web as web_search

# FIX 1: Ép API Key vào biến môi trường để LiveKit SDK tự động nhận diện ngầm
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


VOICE_AGENT_INSTRUCTIONS = """
You are TRIAM, a Vietnamese audiobook study assistant.

Core rules:
- Answer in Vietnamese only.
- Keep replies natural and short: 2-3 sentences.
- Do not use Markdown, bullet lists, headings, or emoji.
- If audio is unclear, partial, noisy, silent, or unintelligible, ask the user to repeat in Vietnamese.

Tool rules:
- For any question about book content, concepts, chapters, learning topics, or study context, ALWAYS call `search_book_knowledge` first.
- If book context is missing or weak, call `ask_web_search_permission` exactly once.
- Read the returned question, then stop and wait for the user.
- Do not ask web-search permission in your own words. Always use `ask_web_search_permission` so the backend can track the pending request.
- After the user clearly agrees, call `execute_web_search` once for the pending query and answer from the result.
- NEVER call `execute_web_search` before the user grants permission.
- If `execute_web_search` returns a permission error, call `ask_web_search_permission` once and stop.
- If `execute_web_search` returns `WEB_SEARCH_PERMISSION_DENIED`, acknowledge the refusal and continue without web search.
- After `execute_web_search` returns a real web result, answer immediately from that result.
- Do not say you are still searching after a web result has been returned.
- Do not answer external or out-of-book facts from memory when web permission is required.
""".strip()


TEXT_AGENTIC_SYSTEM_INSTRUCTIONS = """
System facts:
- Current server time: {now_str}
- Use this server time for date/time questions.

Tool rules:
- For book-content questions, call `search_book_knowledge_text` first.
- For prices, news, recent events, or out-of-book facts, call `ask_web_search_permission_text` before any web search.
- If `search_book_knowledge_text` returns `BOOK_CONTEXT_NOT_FOUND`, call `ask_web_search_permission_text`.
- Call `execute_web_search_text` only after the user granted permission in the previous turn.
- If a tool returns `WEB_SEARCH_PERMISSION_REQUIRED` or `WEB_SEARCH_PERMISSION_UNCLEAR`, ask permission and stop.
- If a tool returns `WEB_SEARCH_PERMISSION_DENIED`, do not search the web.
- Answer in Vietnamese only, 2-3 short sentences, no Markdown, no emoji.
""".strip()


WEB_GRANTED_REPLY_INSTRUCTIONS = """
The user just granted permission to search the web for the previous question.
Approved query: {query}

Web result:
{web_result}

Answer in Vietnamese only, briefly.
Do not use Markdown, bullet lists, headings, numbering, or emoji.
If the web result is weak or incomplete, say so.
""".strip()


GREETING_INSTRUCTIONS = "Chào ông, tôi là TRIAM đây. Bạn muốn thảo luận về chương sách nào hôm nay?"


def _get_job_executor_type() -> JobExecutorType:
    executor_type = settings.LIVEKIT_AGENT_JOB_EXECUTOR_TYPE.strip().lower()
    if executor_type == JobExecutorType.PROCESS.value:
        return JobExecutorType.PROCESS
    if executor_type == JobExecutorType.THREAD.value:
        return JobExecutorType.THREAD

    log.warning(f"Invalid LIVEKIT_AGENT_JOB_EXECUTOR_TYPE={settings.LIVEKIT_AGENT_JOB_EXECUTOR_TYPE!r}; falling back to thread")
    return JobExecutorType.THREAD


def _calculate_agent_load(server: Any) -> float:
    max_jobs = max(settings.LIVEKIT_AGENT_MAX_CONCURRENT_JOBS, 1)
    active_jobs = len(getattr(server, "active_jobs", []) or [])
    return min(active_jobs / max_jobs, 1.0)


def _coerce_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _parse_job_metadata(raw_metadata: str | None, room_name: str) -> VoiceJobMetadata:
    try:
        payload = json.loads(raw_metadata or "{}")
    except (json.JSONDecodeError, TypeError):
        payload = {}

    thread_id = str(payload.get("thread_id") or "")
    document_ids = _coerce_string_list(payload.get("document_ids"))
    book_id = str(payload.get("book_id") or "")

    if book_id and not document_ids:
        document_ids = [book_id]

    if room_name == "console":
        if not thread_id:
            thread_id = settings.VOICE_AGENT_CONSOLE_THREAD_ID
        if not document_ids and settings.VOICE_AGENT_CONSOLE_BOOK_ID:
            document_ids = [settings.VOICE_AGENT_CONSOLE_BOOK_ID]

    return VoiceJobMetadata(thread_id=thread_id, document_ids=document_ids)


def _extract_conversation_item_text(item: LLMMessage) -> str:
    text_content = getattr(item, "text_content", None)
    if isinstance(text_content, str) and text_content.strip():
        return normalize_transcript_text(text_content)

    content = getattr(item, "content", getattr(item, "text", ""))
    if isinstance(content, list):
        text_parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif hasattr(part, "text"):
                text_parts.append(str(part.text))
        return normalize_transcript_text(" ".join(text_parts))

    return normalize_transcript_text(str(content or ""))


class ChatTextOutput(voice_io.TextOutput):
    def __init__(
        self,
        room: rtc.Room,
        topic: str = LK_CHAT_TOPIC,
    ) -> None:
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
        log.info(f"Text output flushed | chars={len(message)} | topic={self._topic}")

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


class TriamAssistant(Agent):
    def __init__(
        self,
        document_ids: list[str],
        web_search_policy: WebSearchPermissionPolicy,
        tracer: AgentTurnTracer,
    ) -> None:
        super().__init__(instructions=VOICE_AGENT_INSTRUCTIONS)
        self.document_ids = document_ids
        self.web_search_policy = web_search_policy
        self.tracer = tracer
        self._web_search_lock = asyncio.Lock()
        self._cached_web_query: str | None = None
        self._cached_web_result: str | None = None
        self._cached_web_at: datetime | None = None

    def _get_cached_web_result(self, query: str) -> str | None:
        if not self._cached_web_query or not self._cached_web_result or not self._cached_web_at:
            return None
        if datetime.now(timezone.utc) - self._cached_web_at > timedelta(seconds=settings.VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS):
            return None
        if normalize_intent_text(self._cached_web_query) != normalize_intent_text(query):
            return None
        return self._cached_web_result

    def _remember_web_result(self, query: str, result: str) -> None:
        self._cached_web_query = query
        self._cached_web_result = result
        self._cached_web_at = datetime.now(timezone.utc)

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
        self.tracer.record_tool(AgentInputMode.VOICE, "search_book_knowledge")
        try:
            result = await search_voice_book_context(
                query,
                self.document_ids,
                tracer=self.tracer,
                input_mode=AgentInputMode.VOICE,
            )
            if result.found:
                self.tracer.record_answer_source(AgentInputMode.VOICE, AgentAnswerSource.BOOK_RAG)
            return format_rag_context(result)
        except Exception as e:
            self.tracer.record_error(AgentInputMode.VOICE, "voice_rag_search_error")
            log.warning(f"Voice RAG search failed | document_count={len(self.document_ids)} | error={e}")
            return "BOOK_CONTEXT_ERROR: Không thể tìm kiếm dữ liệu trong sách lúc này."

    @function_tool
    async def execute_web_search(
        self,
        query: Annotated[str, "Nội dung cần tìm kiếm trên internet"],
    ) -> str:
        """
        [VOICE - Pha 2] Chỉ gọi tool này SAU KHI user đã xác nhận đồng ý ở turn hội thoại trước.
        THỰC HIỆN tìm kiếm thực sự trên internet và trả về kết quả.
        TRAO ĐỔI VUI: Nếu chưa có turn hỏi xin phép trước → không gọi tool này.
        """
        return await self._execute_web_search_for_mode(query, AgentInputMode.VOICE)

    async def _execute_web_search_for_mode(self, query: str, input_mode: AgentInputMode) -> str:
        self.tracer.record_tool(input_mode, "execute_web_search")
        async with self._web_search_lock:
            cached_result = self._get_cached_web_result(query)
            if cached_result is not None:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.WEB)
                log.info(f"Voice web search cached result reused | query_chars={len(query)}")
                return cached_result

            allowed, reason = await self.web_search_policy.resolve_before_web_search(query)
            if not allowed:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.POLICY)
                log.info(f"Voice web search blocked | reason={reason}")
                return reason

            log.info(f"Voice web search executing | query_chars={len(query)}")
            started = time.perf_counter()
            try:
                result = await web_search(query)
                self._remember_web_result(query, result)
                self.tracer.record_latency(input_mode, "web_search", int((time.perf_counter() - started) * 1000))
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.WEB)
                return result
            except Exception:
                self.tracer.record_latency(input_mode, "web_search", int((time.perf_counter() - started) * 1000))
                self.tracer.record_error(input_mode, "web_search_error")
                raise
            finally:
                self.web_search_policy.mark_search_consumed()

    @function_tool
    async def ask_web_search_permission(
        self,
        query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"],
    ) -> str:
        """
        [VOICE - Pha 1] Gọi tool này khi search_book_knowledge không có đủ thông tin liên quan.
        Tool này KHÔNG tìm web ngay. Nó chỉ trả về mẫu câu hỏi xác nhận để AI đọc lên cho user nghe.
        Sau khi AI đọc câu hỏi này, AI kết thúc turn và đợi user trả lời ở turn tiếp theo.
        Nếu user đồng ý (bất kỳ cách nào) → AI tự quyết định gọi 'execute_web_search'.
        Nếu user từ chối → AI không gọi tool và trả lời phù hợp.
        """
        self.tracer.record_tool(AgentInputMode.VOICE, "ask_web_search_permission")
        self.tracer.record_answer_source(AgentInputMode.VOICE, AgentAnswerSource.POLICY)
        log.info(f"Voice web search permission requested | query_chars={len(query)}")
        return self.web_search_policy.request_permission(query)


async def entrypoint(ctx: JobContext):  # noqa: C901
    await ctx.connect()

    job_meta = _parse_job_metadata(ctx.job.metadata, ctx.room.name)
    thread_id = job_meta.thread_id
    document_ids = job_meta.document_ids

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

    model_candidates = [settings.OPENAI_STREAM_MODEL_NAME, "gpt-realtime-1.5"]
    # de-dupe while preserving order
    seen_models: set[str] = set()
    model_candidates = [m for m in model_candidates if not (m in seen_models or seen_models.add(m))]

    web_search_policy = WebSearchPermissionPolicy(
        enabled=settings.VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT,
        grant_ttl_seconds=settings.VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS,
        implicit_grant_window_seconds=settings.VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS,
    )
    tracer = AgentTurnTracer(
        enabled=settings.AGENT_TRACE_ENABLED,
        thread_id=str(thread_uuid) if thread_uuid else None,
        room_name=ctx.room.name,
        score_precision=settings.AGENT_TRACE_SCORE_PRECISION,
        late_transcript_window_seconds=settings.AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS,
    )
    agent_instance = TriamAssistant(
        document_ids=document_ids,
        web_search_policy=web_search_policy,
        tracer=tracer,
    )
    chat_llm = OpenAILLM(model=settings.VOICE_AGENT_TEXT_LLM_MODEL, temperature=0.7)
    transcript_store = VoiceTranscriptStore(
        room=ctx.room,
        thread_id=thread_uuid,
        dedupe_window_seconds=settings.VOICE_AGENT_DEDUPE_WINDOW_SECONDS,
    )

    session: AgentSession
    text_turn_lock = asyncio.Lock()

    def _truncate_session_history() -> None:
        if hasattr(session, "history") and session.history is not None:
            session.history.truncate(max_items=settings.VOICE_AGENT_HISTORY_LIMIT)

    def _record_web_permission_reply(text: str) -> None:
        web_search_policy.record_user_reply(text)

    async def _observe_web_permission_reply(text: str):
        decision = await web_search_policy.observe_user_reply(text)
        if decision.granted_query:
            log.info(f"Web search permission granted | query_chars={len(decision.granted_query)}")
        elif decision.denied:
            log.info("Web search permission denied")
        elif decision.unclear:
            log.info("Web search permission unclear")
        elif decision.new_question:
            log.info("Web search permission cleared because user asked a new question")
        return decision

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent

    async def _chat_naive_rag(user_text: str) -> str:
        """Chế độ RAG Naive (toggle TẮT): luôn search sách, không dùng tool web."""
        log.info("[Text Chat] Chế độ Naive RAG (web search TẮT)")
        tracer.record_tool(AgentInputMode.TEXT, "search_book_knowledge_text")
        rag_result = await search_voice_book_context(
            user_text,
            document_ids,
            tracer=tracer,
            input_mode=AgentInputMode.TEXT,
        )
        temp_ctx = session.history.copy()
        if rag_result.found:
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.BOOK_RAG)
            temp_ctx.add_message(
                role="system",
                content=f"Thông tin trích xuất từ sách (dùng để trả lời):\n{format_rag_context(rag_result)}",
            )
        else:
            temp_ctx.add_message(
                role="system",
                content=("Không tìm thấy thông tin phù hợp trong sách cho câu hỏi này. Hãy nói ngắn gọn rằng nội dung hiện không có trong sách, không tự bịa thông tin ngoài sách."),
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
        async def search_book_knowledge_text(query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"]) -> str:
            """Tìm kiếm kiến thức trong sách thuộc Study Context hiện tại."""
            tracer.record_tool(AgentInputMode.TEXT, "search_book_knowledge_text")
            result = await search_voice_book_context(
                query,
                document_ids,
                tracer=tracer,
                input_mode=AgentInputMode.TEXT,
            )
            if result.found:
                tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.BOOK_RAG)
            return format_rag_context(result)

        async def ask_web_search_permission_text(query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"]) -> str:
            """Xin phép user trước khi tìm kiếm internet."""
            tracer.record_tool(AgentInputMode.TEXT, "ask_web_search_permission_text")
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
            return web_search_policy.request_permission(query)

        async def execute_web_search_text(query: Annotated[str, "Nội dung cần tìm kiếm trên internet"]) -> str:
            """Tìm kiếm thông tin trên internet sau khi user đã đồng ý."""
            return await agent_instance._execute_web_search_for_mode(query, AgentInputMode.TEXT)

        book_fn_tool = function_tool(search_book_knowledge_text)
        ask_web_permission_tool = function_tool(ask_web_search_permission_text)
        web_fn_tool = function_tool(execute_web_search_text)
        standalone_tools = [book_fn_tool, ask_web_permission_tool, web_fn_tool]

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
            content=TEXT_AGENTIC_SYSTEM_INSTRUCTIONS.format(now_str=now_str),
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
                tracer.record_tool(AgentInputMode.TEXT, str(getattr(tc, "name", "unknown_tool")))
                result = await agents_llm.execute_function_call(tc, tool_ctx)
                ctx_copy.insert(result.fnc_call)
                if result.fnc_call_out:
                    ctx_copy.insert(result.fnc_call_out)

        # Hết MAX_STEPS, trả về text của lần gọi cuối cùng
        log.warning("[Agentic] Đạt giới hạn MAX_STEPS, trả về text hiện tại")
        return response.text

    async def _chat_with_granted_web_search(query: str) -> str:
        log.info(f"[Text Chat] Web search granted by user | query_chars={len(query)}")
        web_result = await agent_instance._execute_web_search_for_mode(query, AgentInputMode.TEXT)
        temp_ctx = session.history.copy()
        temp_ctx.add_message(
            role="system",
            content=WEB_GRANTED_REPLY_INSTRUCTIONS.format(query=query, web_result=web_result),
        )
        response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
        return response.text

    async def _publish_assistant_reply(full_reply: str) -> None:
        full_reply = full_reply.strip()
        if not full_reply:
            return

        await transcript_store.save_and_publish_assistant(full_reply)
        try:
            await ctx.room.local_participant.publish_data(
                full_reply.encode("utf-8"),
                reliable=True,
                topic=LK_CHAT_TOPIC,
            )
        except Exception as exc:
            log.info(f"Data output publish failed: {exc}")

        session.history.add_message(role="assistant", content=full_reply)
        _truncate_session_history()

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        normalized_text = normalize_transcript_text(text)
        if not normalized_text:
            return

        async with text_turn_lock:
            tracer.begin_turn(AgentInputMode.TEXT)
            tracer.record_transcript(
                AgentInputMode.TEXT,
                char_count=len(normalized_text),
                language="text",
            )
            log.info(f"Data input received | participant={participant_id or 'unknown'} | chars={len(normalized_text)} | thread_id={thread_uuid}")
            if settings.VOICE_AGENT_LOG_TRANSCRIPT_TEXT:
                log.debug(f"Data input preview: {trim_text(normalized_text, 160)}")

            # Save DB and update transcript immediately (await to guarantee insertion order)
            await transcript_store.save_and_publish_user(normalized_text)
            permission_decision = await _observe_web_permission_reply(normalized_text)

            # Interrupt if livekit is currently speaking
            await session.interrupt()

            # Put input into shared memory
            session.history.add_message(role="user", content=normalized_text)
            _truncate_session_history()

            try:
                if permission_decision.granted_query:
                    full_reply = await _chat_with_granted_web_search(permission_decision.granted_query)
                elif permission_decision.denied:
                    tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
                    full_reply = "Được, tôi sẽ không tìm trên internet. Mình tiếp tục trao đổi dựa trên nội dung sách nhé."
                elif permission_decision.unclear:
                    tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.CLARIFICATION)
                    full_reply = "Tôi chưa rõ ý ông. Bạn muốn tôi tìm thêm trên internet cho câu vừa rồi không?"
                # Phân nhánh dựa theo web search policy từ lk.control.
                elif web_search_policy.enabled:
                    started = time.perf_counter()
                    full_reply = await _chat_with_agentic_loop(normalized_text)
                    tracer.record_latency(AgentInputMode.TEXT, "answer_pipeline", int((time.perf_counter() - started) * 1000))
                else:
                    started = time.perf_counter()
                    full_reply = await _chat_naive_rag(normalized_text)
                    tracer.record_latency(AgentInputMode.TEXT, "answer_pipeline", int((time.perf_counter() - started) * 1000))

                full_reply = full_reply.strip()
                log.info(f"LLM Reply completed. Length: {len(full_reply)}")

                if full_reply:
                    await _publish_assistant_reply(full_reply)
                    tracer.record_assistant(AgentInputMode.TEXT, char_count=len(full_reply))
                tracer.complete_turn(AgentInputMode.TEXT)
            except Exception as e:
                tracer.record_error(AgentInputMode.TEXT, type(e).__name__)
                tracer.complete_turn(AgentInputMode.TEXT, error_code=type(e).__name__)
                log.error(f"Error in handle_data_input: {e}")

    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input received | participant={participant_id} | chars={len(ev.text or '')}")
        # call handle_data_input to process the text input
        await handle_data_input(ev.text, participant_id)

    def on_data_received(packet: rtc.DataPacket) -> None:
        try:
            raw = packet.data.decode("utf-8")
        except Exception as exc:
            log.info(f"Data input decode failed: {exc}")
            return

        # --- Kênh điều khiển: bật/tắt web search ---
        if packet.topic == LK_CONTROL_TOPIC:
            try:
                payload = json.loads(raw)
                if payload.get("type") == "toggle_web_search":
                    web_search_policy.set_enabled(bool(payload.get("enabled", False)))
                    log.info(f"Web search toggle: {'BẬT' if web_search_policy.enabled else 'TẮT'}")
            except json.JSONDecodeError:
                log.info("lk.control: payload không phải JSON hợp lệ")
            return

        # --- Kênh chat thông thường ---
        if packet.topic == LK_CHAT_TOPIC:
            participant_id = packet.participant.identity if packet.participant else None
            asyncio.create_task(handle_data_input(raw, participant_id))

    ctx.room.on("data_received", on_data_received)

    def _handle_user_input_transcribed(ev: Any) -> None:
        is_final = bool(getattr(ev, "is_final", False))
        transcript = str(getattr(ev, "transcript", "") or "").strip()
        language = getattr(ev, "language", None)
        log.info(f"user_input_transcribed received | final={is_final} | chars={len(transcript)} | thread_id={thread_uuid}")
        if settings.VOICE_AGENT_LOG_TRANSCRIPT_TEXT and transcript:
            log.debug(f"user_input_transcribed preview: {trim_text(transcript, 160)}")
        if is_final and transcript:
            tracer.record_transcript(
                AgentInputMode.VOICE,
                char_count=len(transcript),
                language=str(language) if language else None,
            )
            _record_web_permission_reply(transcript)

    def _handle_conversation_item_added(ev: ConversationItemAddedEvent) -> None:
        item = ev.item
        if not isinstance(item, LLMMessage):
            return

        text = _extract_conversation_item_text(item)
        if not text:
            return

        if item.role == "user":
            tracer.ensure_turn(AgentInputMode.VOICE)
            log.info(f"User voice speech saved | text_len={len(text)} | thread_id={thread_uuid}")
            _record_web_permission_reply(text)
            asyncio.create_task(transcript_store.save_and_publish_user(text))
        elif item.role == "assistant":
            tracer.record_assistant(AgentInputMode.VOICE, char_count=len(text))
            tracer.complete_turn(AgentInputMode.VOICE)
            log.info(f"Assistant voice speech saved | text_len={len(text)} | thread_id={thread_uuid}")
            asyncio.create_task(transcript_store.save_and_publish_assistant(text))

    def _handle_function_tools_executed(ev: FunctionToolsExecutedEvent) -> None:
        if not tracer.has_active_turn(AgentInputMode.VOICE):
            return
        for function_call in ev.function_calls:
            tracer.record_tool(
                AgentInputMode.VOICE,
                str(getattr(function_call, "name", "unknown_tool")),
            )

    def _attach_session_handlers(sess: AgentSession) -> None:
        @sess.on("user_input_transcribed")  # type: ignore[arg-type]
        def on_user_input_transcribed(ev):
            _handle_user_input_transcribed(ev)

        @sess.on("conversation_item_added")  # type: ignore[arg-type]
        def on_conversation_item_added(ev: ConversationItemAddedEvent):
            _handle_conversation_item_added(ev)

        @sess.on("function_tools_executed")  # type: ignore[arg-type]
        def on_function_tools_executed(ev: FunctionToolsExecutedEvent):
            _handle_function_tools_executed(ev)

    # Start session with fallback when a configured model is unavailable.
    last_start_exc: Exception | None = None
    for model_name in model_candidates:
        try:
            log.info(f"Starting realtime session with model: {model_name}, voice: {settings.OPENAI_REALTIME_VOICE}")
            model = RealtimeModel(
                model=model_name,
                voice=settings.OPENAI_REALTIME_VOICE,
                modalities=["audio"],
                input_audio_transcription=AudioTranscription(
                    model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
                    language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
                    prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
                ),
                input_audio_noise_reduction="near_field",
            )
            session = AgentSession(
                llm=model,
                turn_handling={
                    "interruption": {
                        "enabled": True,
                        "min_duration": settings.VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS,
                        "min_words": settings.VOICE_AGENT_INTERRUPTION_MIN_WORDS,
                        "resume_false_interruption": True,
                        "false_interruption_timeout": settings.VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS,
                        "discard_audio_if_uninterruptible": True,
                    },
                    "preemptive_generation": {
                        "enabled": settings.VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED,
                    },
                },
            )
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
                            topic=LK_CHAT_TOPIC,
                        ),
                    ),
                    close_on_disconnect=True,
                ),
            )

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

    try:
        history_msgs = await transcript_store.load_recent_history(settings.VOICE_AGENT_HISTORY_LIMIT)
        # type: ignore[attr-defined]
        if hasattr(session, "history") and session.history is not None:
            for msg in history_msgs:
                # type: ignore[attr-defined]
                session.history.add_message(role="user" if msg.is_user else "assistant", content=msg.text)
            _truncate_session_history()
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")

    await session.generate_reply(
        instructions=GREETING_INSTRUCTIONS,
    )


if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=_calculate_agent_load,
            load_threshold=settings.LIVEKIT_AGENT_LOAD_THRESHOLD,
            job_executor_type=_get_job_executor_type(),
            num_idle_processes=settings.LIVEKIT_AGENT_NUM_IDLE_PROCESSES,
            initialize_process_timeout=settings.LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT,
            shutdown_process_timeout=settings.LIVEKIT_AGENT_SHUTDOWN_PROCESS_TIMEOUT,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )
