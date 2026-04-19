import asyncio
import array
import os
from collections import deque
import time
from typing import Any, cast
from livekit import api

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import google.genai as genai
from google.genai import types
from starlette.websockets import WebSocketState
from tavily import AsyncTavilyClient
import uuid
from app.core.config import settings
from app.services.rag_service import search_book_knowledge

tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
router = APIRouter()

client = genai.Client(api_key=settings.GEMINI_API_KEY,
                      http_options={"api_version": "v1beta"})

# =======SYSTEM INSTRUCTION=======
SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM - Người hỗ trợ cho người dùng đọc sách qua giọng nói. Bạn có 2 công cụ hỗ trợ:
1. 'search_book_knowledge': Dùng để tìm trong sách của người dùng. Luôn ưu tiên cái này trước.
2. 'search_web': Dùng để tìm thông tin từ Internet nếu sách không có câu trả lời hoặc câu hỏi là về tin tức/kiến thức chung.
Hãy trả lời ngắn gọn, súc tích bằng giọng nói thân thiện.
"""

# Model hỗ trợ native audio output
MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# Audio format constants (PCM 16-bit, mono)
SEND_SAMPLE_RATE = 16000  # Microphone input rate
RECEIVE_SAMPLE_RATE = 24000  # AI output rate
SESSION_KEEPALIVE_INTERVAL_SEC = 15
INTERRUPT_WINDOW_MS = 280
INTERRUPT_MIN_SPEECH_FRAMES = 5
INTERRUPT_MIN_BURST_MS = 120
INTERRUPT_COOLDOWN_MS = 800
INTERRUPT_MIN_SPEAKING_MS = 600
PCM_SPEECH_THRESHOLD = 1500

# NOTE: google_search grounding tool CANNOT be combined with function_declarations
# in the Gemini Live API — it causes a server-side 1008 error after tool responses.
tools_config = [
    types.Tool(
        function_declarations=[
            # Tool search book knowledge in supabase
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
                parameters=cast(Any, {
                    "type": "OBJECT",
                    "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                    "required": ["query"],
                }),
            ),
            # Tool Tavily search web input for llm (rag)
            types.FunctionDeclaration(
                name="search_web",
                description="Tìm kiếm Internet bằng Tavily khi cần kiến thức cập nhật hoặc sách không có.",
                parameters=cast(Any, {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Câu hỏi tìm kiếm trên web",
                        }
                    },
                    "required": ["query"],
                }),
            ),
        ]
    ),
]


# === Helper: safe WebSocket send ===
async def _safe_send_bytes(websocket: WebSocket, data: bytes) -> bool:
    """Send bytes only if WebSocket is still connected. Returns False if send failed."""
    try:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_bytes(data)
            return True
    except Exception:
        pass
    return False


async def _safe_send_text(websocket: WebSocket, text: str) -> bool:
    """Send text only if WebSocket is still connected. Returns False if send failed."""
    try:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(text)
            return True
    except Exception:
        pass
    return False


async def _handle_tool_calls(session, tool_call, book_id: str, websocket: WebSocket):
    responses = []
    for call in tool_call.function_calls:
        tool_name = call.name
        await _safe_send_text(websocket, f"SYSTEM:TOOL_CALLING_START:{tool_name}")

        result_text = "Không thể tra cứu thông tin lúc này."

        if tool_name == "search_book_knowledge":
            args = call.args or {}
            query = args.get("query", "")
            print(f"🔍 RAG search: {query} (call.id={call.id})")
            try:
                result_text = await search_book_knowledge(query, book_id)
            except Exception as rag_err:
                print(f"❌ Lỗi RAG search: {rag_err}")

        elif tool_name == "search_web":
            print("🌐 Đang search Tavily...")
            args = call.args or {}
            query = args.get("query", "")
            try:
                search_result = await tavily_client.search(
                    query=query,
                    search_depth="basic",
                    max_results=3,
                )
                result_text = "\n".join(
                    [f"- {r['content']}" for r in search_result["results"]]
                )
            except Exception as tavily_err:
                print(f"❌ Lỗi Tavily search: {tavily_err}")

        if call.id:
            responses.append(
                types.FunctionResponse(
                    name=tool_name,
                    id=call.id,
                    response={"result": result_text},
                )
            )
        else:
            print(
                f"⚠️ Bỏ qua tool response vì call.id rỗng (tool={tool_name})")

        await _safe_send_text(websocket, f"SYSTEM:TOOL_CALLING_END:{tool_name}")

    if responses:
        try:
            await session.send_tool_response(function_responses=responses)
            print(f"✅ Đã gửi {len(responses)} tool response(s) cho Gemini")
        except Exception as send_err:
            print(f"❌ Lỗi gửi tool response: {send_err}")


# === MAIN ROUTE: WebSocket for Gemini Live ===
@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    # Cấu hình dispatch Agent ngay khi user join room
    # Điều này bắt buộc để LiveKit FE Flutter Session nhận diện được 'dispatchesAgent: true'
    agent_name = os.getenv("LIVEKIT_AGENT_NAME",
                           "my-agent").strip() or "my-agent"
    agent_dispatch = api.RoomAgentDispatch(agent_name=agent_name)
    room_config = api.RoomConfiguration(
        name=book_id,
        agents=[agent_dispatch]
    )

    # Tạo Token định danh cho User
    token = api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET) \
        .with_identity(f"user_{uuid.uuid4().hex[:6]}") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=book_id,  # Dùng chính book_id làm tên phòng
        )) \
        .with_room_config(room_config) \
        .with_metadata(book_id)  # Truyền book_id vào metadata cho Agent đọc

    return {"token": token.to_jwt()}


@router.websocket("/ws/live-assistant/{book_id}")
async def live_assistant_endpoint(websocket: WebSocket, book_id: str):
    """
    WebSocket endpoint for real-time voice conversation via Gemini Live API.

    Protocol:
    - Client → Server: raw PCM audio bytes (16kHz, 16-bit, mono)
    - Server → Client: raw PCM audio bytes (24kHz, 16-bit, mono) — AI voice response
    - Server → Client: text control messages (SYSTEM:*)
    """
    await websocket.accept()

    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        tools=tools_config,
        system_instruction=types.Content(
            parts=[types.Part(text=SYSTEM_INSTRUCTION)]),
        # generation_config=types.GenerationConfig(
        #     response_modalities=["AUDIO"]),
        context_window_compression=(
            # Configures compression with default parameters.
            types.ContextWindowCompressionConfig(
                sliding_window=types.SlidingWindow(),
            )
        ),
        # Enable automatic activity detection to optimize latency and resource usage.
        realtime_input_config=types.RealtimeInputConfig(
            automatic_activity_detection=types.AutomaticActivityDetection(
                disabled=False,  # Enable activity detection
                start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_HIGH,
                silence_duration_ms=1000,  # Milliseconds of silence to consider as inactivity
            )
        ),
        generation_config=types.GenerationConfig(
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Aoede")
                )
            )
        ),

    )

    # Shared stop event: when one side exits, the other side will also stop
    stop_event = asyncio.Event()
    ws_send_lock = asyncio.Lock()
    audio_out_queue: asyncio.Queue[tuple[str,
                                         bytes]] = asyncio.Queue(maxsize=256)
    active_turn_generation = 0
    active_turn_id = "turn-0"
    turn_state = "LISTENING"
    speech_frame_times: deque[float] = deque()
    last_interrupt_accepted_at = 0.0
    speaking_started_at = 0.0
    suppress_current_turn_audio = False

    def _is_speech_frame(pcm_bytes: bytes) -> bool:
        if not pcm_bytes:
            return False
        try:
            samples = array.array("h")
            samples.frombytes(pcm_bytes)
            if not samples:
                return False
            avg_abs = sum(abs(sample) for sample in samples) / len(samples)
            return avg_abs >= PCM_SPEECH_THRESHOLD
        except Exception:
            return False

    def _mark_speech_activity(pcm_bytes: bytes):
        if not _is_speech_frame(pcm_bytes):
            return
        now = time.monotonic()
        speech_frame_times.append(now)
        window_sec = INTERRUPT_WINDOW_MS / 1000.0
        while speech_frame_times and (now - speech_frame_times[0] > window_sec):
            speech_frame_times.popleft()

    def _should_accept_interrupt() -> tuple[bool, str]:
        nonlocal last_interrupt_accepted_at
        now = time.monotonic()
        window_sec = INTERRUPT_WINDOW_MS / 1000.0
        while speech_frame_times and (now - speech_frame_times[0] > window_sec):
            speech_frame_times.popleft()

        if turn_state != "SPEAKING":
            return False, "not_speaking"

        cooldown_sec = INTERRUPT_COOLDOWN_MS / 1000.0
        if now - last_interrupt_accepted_at < cooldown_sec:
            return False, "cooldown"

        min_speaking_sec = INTERRUPT_MIN_SPEAKING_MS / 1000.0
        if speaking_started_at > 0 and (now - speaking_started_at) < min_speaking_sec:
            return False, "speaking_too_early"

        if len(speech_frame_times) < INTERRUPT_MIN_SPEECH_FRAMES:
            return False, f"insufficient_speech_frames={len(speech_frame_times)}"

        burst_ms = (speech_frame_times[-1] - speech_frame_times[0]
                    ) * 1000 if len(speech_frame_times) >= 2 else 0
        if burst_ms < INTERRUPT_MIN_BURST_MS:
            return False, f"speech_burst_too_short={int(burst_ms)}ms"

        last_interrupt_accepted_at = now
        return True, "accepted"

    async def _send_text_locked(text: str) -> bool:
        async with ws_send_lock:
            return await _safe_send_text(websocket, text)

    async def _send_bytes_locked(data: bytes) -> bool:
        async with ws_send_lock:
            return await _safe_send_bytes(websocket, data)

    async def _flush_audio_queue_locked(reason: str, old_turn_id: str, new_turn_id: str) -> int:
        dropped = 0
        while True:
            try:
                audio_out_queue.get_nowait()
                audio_out_queue.task_done()
                dropped += 1
            except asyncio.QueueEmpty:
                break
        print(
            f"🧹 Flush audio queue ({reason}) old_turn={old_turn_id} new_turn={new_turn_id} dropped={dropped}"
        )
        return dropped

    async def _hard_interrupt(reason: str):
        nonlocal active_turn_generation, active_turn_id, turn_state, suppress_current_turn_audio
        async with ws_send_lock:
            old_turn_id = active_turn_id
            await _safe_send_text(websocket, "SYSTEM:INTERRUPTED")
            active_turn_generation += 1
            active_turn_id = f"turn-{active_turn_generation}"
            turn_state = "LISTENING"
            suppress_current_turn_audio = True
            await _flush_audio_queue_locked(reason, old_turn_id, active_turn_id)
            await _safe_send_text(websocket, "SYSTEM:BARGE_IN_ACK")
            await _safe_send_text(websocket, "SYSTEM:LISTENING")

    async def _enqueue_audio_chunk(turn_id: str, data: bytes):
        if audio_out_queue.full():
            try:
                old_turn_id, _ = audio_out_queue.get_nowait()
                audio_out_queue.task_done()
                print(
                    f"🗑️ Drop stale chunk do full queue old_turn={old_turn_id} active_turn={active_turn_id}"
                )
            except asyncio.QueueEmpty:
                pass
        try:
            audio_out_queue.put_nowait((turn_id, data))
        except asyncio.QueueFull:
            print(f"⚠️ Queue vẫn full, drop chunk turn_id={turn_id}")

    try:
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print("✅ Đã kết nối Gemini Live")

            # ── Task 1: Client → Gemini (Send PCM audio upstream) ──────────────
            async def send_to_gemini():
                try:
                    while not stop_event.is_set():
                        try:
                            # Read raw WS frames so text/control frames don't crash the audio loop.
                            message = await asyncio.wait_for(websocket.receive(), timeout=5.0)
                            message_type = message.get("type")
                            if message_type == "websocket.disconnect":
                                print("📴 Client ngắt kết nối (send loop)")
                                stop_event.set()
                                break

                            data = message.get("bytes")
                            if data:
                                _mark_speech_activity(data)
                                await session.send_realtime_input(
                                    audio={"data": data,
                                           "mime_type": "audio/pcm"}
                                )

                            # Optional text control frames from FE should not tear down session.
                            text = message.get("text")
                            if text and text.startswith("SYSTEM:HANGUP"):
                                print("📴 Nhận yêu cầu kết thúc phiên từ client")
                                stop_event.set()
                                break
                        except asyncio.TimeoutError:
                            # No data arrived — check stop_event and loop again
                            continue
                        except WebSocketDisconnect:
                            print("📴 Client ngắt kết nối (send loop)")
                            stop_event.set()
                            break
                        except Exception as e:
                            print(f"❌ Lỗi nhận audio từ client: {e}")
                            stop_event.set()
                            break
                finally:
                    print("🔴 send_to_gemini() đã dừng")

            # ── Task 1.5: Audio sender with hard turn_id filter ──────────────
            async def send_audio_to_client():
                nonlocal active_turn_id
                try:
                    while not stop_event.is_set():
                        try:
                            turn_id, chunk = await asyncio.wait_for(audio_out_queue.get(), timeout=1.0)
                        except asyncio.TimeoutError:
                            continue

                        async with ws_send_lock:
                            if turn_id != active_turn_id:
                                print(
                                    f"🗑️ Drop old turn chunk turn_id={turn_id} active_turn={active_turn_id}"
                                )
                                audio_out_queue.task_done()
                                continue

                            ok = await _safe_send_bytes(websocket, chunk)
                            audio_out_queue.task_done()
                            if not ok:
                                stop_event.set()
                                break
                finally:
                    print("🔴 send_audio_to_client() đã dừng")

            # ── Task 2.5: session keepalive event to FE ───────────────────────
            async def session_keepalive():
                try:
                    while not stop_event.is_set():
                        await asyncio.sleep(SESSION_KEEPALIVE_INTERVAL_SEC)
                        if stop_event.is_set():
                            break
                        ok = await _send_text_locked("SYSTEM:SESSION_KEEPALIVE")
                        if not ok:
                            stop_event.set()
                            break
                finally:
                    print("🔴 session_keepalive() đã dừng")

            # ── Task 2: Gemini → Client (Receive audio + handle tool calls) ───
            async def receive_from_gemini():
                nonlocal active_turn_generation, active_turn_id, turn_state, speaking_started_at, suppress_current_turn_audio
                try:
                    while not stop_event.is_set():
                        stream_had_messages = False
                        async for response in session.receive():
                            stream_had_messages = True
                            if stop_event.is_set():
                                break

                            server_content = response.server_content

                            # Barge-in signal from Gemini when user interrupts current AI speech.
                            if server_content and server_content.interrupted:
                                accepted, reason = _should_accept_interrupt()
                                if not accepted:
                                    print(
                                        f"🟨 Ignore interrupted ({reason}) turn_state={turn_state}")
                                    continue

                                print("⚠️ User interrupted - Stopping AI output")
                                await _hard_interrupt("gemini_interrupted")
                                continue

                            # ── Audio response ─────────────────────────────────
                            if server_content and server_content.model_turn and server_content.model_turn.parts:
                                if turn_state != "SPEAKING":
                                    active_turn_generation += 1
                                    active_turn_id = f"turn-{active_turn_generation}"
                                    turn_state = "SPEAKING"
                                    speaking_started_at = time.monotonic()
                                    await _send_text_locked(f"SYSTEM:SPEAKING:{active_turn_id}")

                                if suppress_current_turn_audio:
                                    print(
                                        "🧯 Suppress old-turn audio until turn_complete")
                                    continue

                                for part in server_content.model_turn.parts:
                                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                                        await _enqueue_audio_chunk(active_turn_id, part.inline_data.data)

                            # ── Turn complete — keep same session in LISTENING ─
                            if server_content and server_content.turn_complete:
                                print(
                                    "🔔 Gemini turn complete — giữ session, tiếp tục lắng nghe")
                                turn_state = "LISTENING"
                                suppress_current_turn_audio = False
                                speaking_started_at = 0.0
                                await _send_text_locked("SYSTEM:LISTENING")

                            # ── Tool call: RAG / Web Search ───────────────────
                            if response.tool_call:
                                await _handle_tool_calls(session, response.tool_call, book_id, websocket)

                        if stop_event.is_set():
                            break

                        # Some upstream stream closures are transient; keep FE socket alive and continue.
                        if stream_had_messages:
                            print(
                                "🟡 Luồng receive() của Gemini kết thúc, thử tiếp tục phiên")
                            await asyncio.sleep(0.15)
                        else:
                            await asyncio.sleep(0.3)

                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (receive loop)")
                    stop_event.set()
                except Exception as e:
                    print(f"❌ Lỗi nhận từ Gemini: {e}")
                    await _send_text_locked("SYSTEM:RECOVERING")
                    await asyncio.sleep(0.5)
                finally:
                    print("🔴 receive_from_gemini() đã dừng")

            # ── Run tasks and keep session until explicit disconnect/fatal error ─
            send_task = asyncio.create_task(send_to_gemini())
            audio_send_task = asyncio.create_task(send_audio_to_client())
            recv_task = asyncio.create_task(receive_from_gemini())
            keepalive_task = asyncio.create_task(session_keepalive())

            try:
                await stop_event.wait()
            finally:
                stop_event.set()
                for task in [send_task, audio_send_task, recv_task, keepalive_task]:
                    if not task.done():
                        task.cancel()
                        try:
                            await task
                        except (asyncio.CancelledError, Exception):
                            pass

            print("🏁 Session kết thúc sạch sẽ")

    except WebSocketDisconnect:
        print("📴 Client ngắt kết nối trước khi kết nối Gemini")
    except Exception as e:
        print(f"❌ Lỗi kết nối Gemini Live: {e}")
        await _safe_send_text(websocket, f"SYSTEM:FATAL_CLOSE:{e}")
