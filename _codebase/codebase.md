# Project Export

## Project Statistics

- Total files: 26

## Folder Structure

```
pyproject.toml
.python-version
app
  api
    v1
      endpoints
        audiobooks.py
        chat.py
        live.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    config.py
    supabase.py
    __init__.py
  crud
    audiobook.py
    book_knowledge.py
  db.py
  helper
    run_background_processing.py
    upload2supabase.py
  main.py
  models
    db_models.py
  services
    embed.py
    llm_service.py
    pdf_service.py
    rag_service.py
    tts_service.py
    __init__.py
  __init__.py

```

### pyproject.toml

*(Unsupported file type)*

### .python-version

*(Unsupported file type)*

### app\api\v1\endpoints\audiobooks.py

```py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import uuid

from app.crud import audiobook as crud_book
from app.db import get_session
from app.models.db_models import Book, Chapter, ChapterSegment

router = APIRouter()


@router.get("/books", response_model=list[Book])
def read_all_books(session: Session = Depends(get_session)):
    return crud_book.get_audiobooks(session)


@router.post("/books", response_model=Book)
def add_new_book(book: Book, session: Session = Depends(get_session)):
    return crud_book.create_audiobook(session, book)


@router.get("/books/{book_id}/details")
def get_book_details(book_id: uuid.UUID, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()
    
    result = []
    for chap in chapters:
        segments = session.exec(select(ChapterSegment).where(ChapterSegment.chapter_id == chap.id).order_by(ChapterSegment.segment_index)).all()
        result.append({
            "id": str(chap.id),
            "title": chap.title,
            "status": chap.status,
            "chapter_index": chap.chapter_index,
            "chapter_segments": [s.model_dump() for s in segments]
        })
        
    return {
        "book_status": book.status,
        "total_chapters": book.total_chapters,
        "chapters": result
    }

```

### app\api\v1\endpoints\chat.py

```py
# Chat endpoint for Q&A
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(question: str):
    """
    Handle Q&A chat requests
    """
    # TODO: Implement chat logic with RAG
    return {"question": question, "answer": "Coming soon..."}

```

### app\api\v1\endpoints\live.py

```py
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from starlette.websockets import WebSocketState
from tavily import AsyncTavilyClient

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

# NOTE: google_search grounding tool CANNOT be combined with function_declarations
# in the Gemini Live API — it causes a server-side 1008 error after tool responses.
tools_config = [
    types.Tool(
        function_declarations=[
            # Tool search book knowledge in supabase
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
                parameters={
                    "type": "OBJECT",
                    "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                    "required": ["query"],
                },
            ),
            # Tool Tavily search web input for llm (rag)
            types.FunctionDeclaration(
                name="search_web",
                description="Tìm kiếm Internet bằng Tavily khi cần kiến thức cập nhật hoặc sách không có.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Câu hỏi tìm kiếm trên web",
                        }
                    },
                    "required": ["query"],
                },
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


# === MAIN ROUTE: WebSocket for Gemini Live ===
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
        tools=tools_config,
        system_instruction=types.Content(
            parts=[types.Part(text=SYSTEM_INSTRUCTION)]),
        generation_config=types.GenerationConfig(
            response_modalities=["AUDIO"]),
    )

    # Shared stop event: when one side exits, the other side will also stop
    stop_event = asyncio.Event()

    try:
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print("✅ Đã kết nối Gemini Live")

            # ── Task 1: Client → Gemini (Send PCM audio upstream) ──────────────
            async def send_to_gemini():
                try:
                    while not stop_event.is_set():
                        try:
                            # Timeout ensures we check stop_event periodically
                            data = await asyncio.wait_for(websocket.receive_bytes(), timeout=5.0)
                            await session.send_realtime_input(audio={"data": data, "mime_type": "audio/pcm"})
                        except asyncio.TimeoutError:
                            # No data arrived — check stop_event and loop again
                            continue
                        except WebSocketDisconnect:
                            print("📴 Client ngắt kết nối (send loop)")
                            break
                        except Exception as e:
                            print(f"❌ Lỗi nhận audio từ client: {e}")
                            break
                finally:
                    stop_event.set()
                    print("🔴 send_to_gemini() đã dừng")

            # ── Task 2: Gemini → Client (Receive audio + handle tool calls) ───
            async def receive_from_gemini():
                try:
                    async for response in session.receive():
                        if stop_event.is_set():
                            break

                        server_content = response.server_content

                        # ── Audio response ─────────────────────────────────────
                        if server_content and server_content.model_turn:
                            for part in server_content.model_turn.parts:
                                if part.inline_data and isinstance(part.inline_data.data, bytes):
                                    ok = await _safe_send_bytes(websocket, part.inline_data.data)
                                    if not ok:
                                        # WebSocket closed — stop this loop
                                        stop_event.set()
                                        return

                        # ── Turn complete — AI finished speaking ───────────────
                        if server_content and server_content.turn_complete:
                            print(
                                "🔔 Gemini turn complete — giữ session, tiếp tục lắng nghe")
                            await _safe_send_text(websocket, "SYSTEM:LISTENING")

                        # ── Tool call: RAG / Web Search ────────────────────────
                        if response.tool_call:
                            for call in response.tool_call.function_calls:
                                tool_name = call.name
                                await _safe_send_text(websocket, f"SYSTEM:TOOL_CALLING_START:{tool_name}")

                                result_text = "Không thể tra cứu thông tin lúc này."

                                if tool_name == "search_book_knowledge":
                                    query = call.args.get("query", "")
                                    print(
                                        f"🔍 RAG search: {query} (call.id={call.id})")
                                    if not call.id:
                                        print(
                                            "⚠️ Bỏ qua tool call vì call.id là None")
                                        continue
                                    try:
                                        result_text = await search_book_knowledge(query, book_id)
                                    except Exception as rag_err:
                                        print(f"❌ Lỗi RAG search: {rag_err}")

                                elif tool_name == "search_web":
                                    print("🌐 Đang search Tavily...")
                                    query = call.args.get("query", "")
                                    try:
                                        search_result = await tavily_client.search(
                                            query=query,
                                            search_depth="basic",
                                            max_results=3,
                                        )
                                        result_text = "\n".join(
                                            [f"- {r['content']}" for r in search_result["results"]])
                                    except Exception as tavily_err:
                                        print(
                                            f"❌ Lỗi Tavily search: {tavily_err}")

                                # Always send tool response back to Gemini to unblock session
                                try:
                                    await session.send_tool_response(
                                        function_responses=[
                                            types.FunctionResponse(
                                                name=tool_name,
                                                id=call.id,
                                                response={
                                                    "result": result_text},
                                            )
                                        ]
                                    )
                                    print(
                                        f"✅ Đã gửi {tool_name} response cho call.id={call.id}")
                                except Exception as send_err:
                                    print(
                                        f"❌ Lỗi gửi tool response: {send_err}")

                                await _safe_send_text(websocket, f"SYSTEM:TOOL_CALLING_END:{tool_name}")

                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (receive loop)")
                except Exception as e:
                    print(f"❌ Lỗi nhận từ Gemini: {e}")
                finally:
                    stop_event.set()
                    print("🔴 receive_from_gemini() đã dừng")

            # ── Run both tasks; cancel both when either finishes ───────────────
            send_task = asyncio.create_task(send_to_gemini())
            recv_task = asyncio.create_task(receive_from_gemini())

            try:
                # Wait until EITHER task finishes (e.g. client disconnects)
                done, pending = await asyncio.wait(
                    [send_task, recv_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
            finally:
                # Cancel whichever task is still running — prevents zombie tasks
                stop_event.set()
                for task in [send_task, recv_task]:
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

```

### app\api\v1\endpoints\upload.py

```py
import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Body, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlmodel import Session

from app.crud.audiobook import (
    create_book,
    create_chapter,
    create_reading_plan,
    update_book_status,
)
from app.db import engine
from app.helper.run_background_processing import run_background_processing
from app.helper.upload2supabase import upload_file_to_supabase
from app.models.db_models import Book, Chapter, ReadingPlan
from app.services.pdf_service import extract_chapters_smart

logger = logging.getLogger("upload")

router = APIRouter()

# -----------------------------------------------------------------------
# Mock User — thay bằng JWT decode sau khi tích hợp Auth
# -----------------------------------------------------------------------
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")

ALLOWED_MIME_TYPES = {"application/pdf", "application/epub+zip", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


# -----------------------------------------------------------------------
# Pydantic Schema cho /generate-plan
# -----------------------------------------------------------------------
class GeneratePlanRequest(BaseModel):
    book_id: uuid.UUID
    mode: str  # "FULL_MODE" | "PARETO_MODE"
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]


# -----------------------------------------------------------------------
# ENDPOINT 1: POST /upload
# -----------------------------------------------------------------------
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):  # noqa: B008
    """
    Bước 1: Nhận file, extract outline, upload PDF lên Supabase Storage,
    lưu Book + Chapter (DRAFT), trả về outline cho Flutter.
    Không kích hoạt xử lý AI ở đây.
    """
    # 1. Validate MIME Type hoặc đuôi file (vì chọn file từ Google Drive hay trả về application/octet-stream)
    is_valid_type = file.content_type in ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()

    if not is_valid_type:
        # Fallback kiểm tra bằng đuôi file
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise HTTPException(status_code=400, detail=f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File vượt quá giới hạn 50MB.")

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)
    chapters_data = []
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract outline (danh sách chương)
        with open(tmp_filename, "rb") as f:
            chapters_data = await extract_chapters_smart(f)

        if not chapters_data:
            raise HTTPException(status_code=422, detail="Không thể trích xuất nội dung từ file. File có thể bị lỗi hoặc là scan ảnh.")

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.pdf"
        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type="application/pdf",
        )
        logger.info(f"☁️  PDF uploaded to Storage: {storage_path}")

    finally:
        # [Dọn Rác] Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    # 5. Lưu DB: Book (DRAFT) + Chapters (DRAFT)
    title = (file.filename or "unknown").rsplit(".", 1)[0]

    try:
        with Session(engine) as session:
            book = Book(
                id=book_id,
                user_id=MOCK_USER_ID,
                title=title,
                total_chapters=len(chapters_data),
                status="DRAFT",
                file_url=file_url,  # URL thật của PDF trên Supabase Storage
            )
            create_book(session, book)

            # Lưu Chapter DRAFT ngay để /generate-plan fetch lại được
            for i, chap in enumerate(chapters_data):
                chapter = Chapter(
                    book_id=book_id,
                    chapter_index=i,
                    title=chap.get("title", f"Chương {i + 1}"),
                    status="DRAFT",
                )
                create_chapter(session, chapter)

        logger.info(f"📘 Created DRAFT book {book_id} | {len(chapters_data)} chapters | file_url saved")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi lưu DB: {str(e)}") from e

    # 6. Trả về outline để Flutter hiển thị
    outline = [{"title": c.get("title", f"Chương {i + 1}"), "page_start": c.get("page_start", 0)} for i, c in enumerate(chapters_data)]

    return {
        "book_id": str(book_id),
        "total_chapters": len(chapters_data),
        "outline": outline,
    }


# -----------------------------------------------------------------------
# ENDPOINT 2: POST /generate-plan
# -----------------------------------------------------------------------
@router.post("/generate-plan")
async def generate_plan(
    background_tasks: BackgroundTasks,
    payload: GeneratePlanRequest = Body(...),  # noqa: B008
):
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    # 1. Validate book tồn tại
    with Session(engine) as session:
        book = session.get(Book, payload.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Không tìm thấy sách.")
        if book.status not in ("DRAFT", "ERROR"):
            raise HTTPException(status_code=409, detail=f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    # 2. Validate mode
    if payload.mode not in ("FULL_MODE", "PARETO_MODE"):
        raise HTTPException(status_code=400, detail="mode phải là 'FULL_MODE' hoặc 'PARETO_MODE'.")

    # 3. Lưu ReadingPlan + cập nhật Book status
    try:
        with Session(engine) as session:
            plan = ReadingPlan(
                book_id=payload.book_id,
                mode=payload.mode,
                pace=payload.pace,
                schedule_config=payload.schedule_config,
                status="ACTIVE",
            )
            create_reading_plan(session, plan)
            update_book_status(session, payload.book_id, "PROCESSING")

        logger.info(f"📋 ReadingPlan created for book {payload.book_id} | mode={payload.mode}")
    except Exception as e:
        logger.error(f"Failed to create reading plan: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi lưu ReadingPlan: {str(e)}") from e

    # 4. Kick-off background task — trả 200 OK ngay
    background_tasks.add_task(run_background_processing, payload.book_id, payload.mode)

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "mode": payload.mode,
    }

```

### app\api\v1\endpoints\__init__.py

```py
# API Endpoints module

```

### app\api\v1\__init__.py

```py
# API v1 module

```

### app\api\__init__.py

```py
# API v1 module

```

### app\core\config.py

```py
import os

from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-AvaMultilingualNeural")

settings = Settings()

```

### app\core\supabase.py

```py
from dotenv import load_dotenv
from supabase import Client, create_client

from app.core.config import settings

load_dotenv()

url: str = settings.SUPABASE_URL
# Use service role key for backend operations (bypasses RLS)
# Fall back to anon key if service role key is not set
key: str = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

```

### app\core\__init__.py

```py
# Core module

```

### app\crud\audiobook.py

```py
import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan

# ---------------------------------------------------------------------------
# Book
# ---------------------------------------------------------------------------


def get_audiobooks(session: Session) -> list[Book]:
    return session.exec(select(Book)).all()


def get_book_by_id(session: Session, book_id: uuid.UUID) -> Optional[Book]:
    return session.get(Book, book_id)


def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def update_book_status(session: Session, book_id: uuid.UUID, status: str, error_message: Optional[str] = None) -> None:
    book = session.get(Book, book_id)
    if book:
        book.status = status
        if error_message is not None:
            book.error_message = error_message
        session.add(book)
        session.commit()


# ---------------------------------------------------------------------------
# Chapter
# ---------------------------------------------------------------------------


def create_chapter(session: Session, chapter: Chapter) -> Chapter:
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.review_audio_url = review_audio_url
        session.add(chapter)
        session.commit()


def update_chapter_status(session: Session, chapter_id: uuid.UUID, status: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.status = status
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()


# ---------------------------------------------------------------------------
# ChapterSegment
# ---------------------------------------------------------------------------


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    for segment in segments:
        session.add(segment)
    session.commit()


# ---------------------------------------------------------------------------
# ReadingPlan
# ---------------------------------------------------------------------------


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


# ---------------------------------------------------------------------------
# Chapter (thêm helpers)
# ---------------------------------------------------------------------------


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.review_text = review_text
        session.add(chapter)
        session.commit()


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = (
        select(Chapter)
        .where(Chapter.book_id == book_id)
        .order_by(Chapter.chapter_index)
    )
    return list(session.exec(statement).all())


```

### app\crud\book_knowledge.py

```py
import uuid

from sqlmodel import Session, select

from app.models.db_models import BookKnowledge


def bulk_create_knowledge(session: Session, records: list[BookKnowledge]) -> None:
    """Insert hàng loạt BookKnowledge (vector chunks) vào DB."""
    for record in records:
        session.add(record)
    session.commit()


def delete_knowledge_by_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    """Xóa toàn bộ vector chunks của 1 chapter (dùng khi rollback)."""
    records = session.exec(
        select(BookKnowledge).where(BookKnowledge.chapter_id == chapter_id)
    ).all()
    for record in records:
        session.delete(record)
    session.commit()


```

### app\db.py

```py
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

load_dotenv()

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

```

### app\helper\run_background_processing.py

```py
import asyncio
import logging
import os
import uuid

from sqlmodel import Session

from app.core.supabase import supabase
from app.crud.audiobook import (
    bulk_create_segments,
    delete_chapter,
    get_draft_chapters_by_book,
    update_book_status,
    update_chapter_review_audio,
    update_chapter_review_text,
    update_chapter_status,
)
from app.crud.book_knowledge import delete_knowledge_by_chapter
from app.db import engine
from app.helper.upload2supabase import upload_file_to_supabase
from app.models.db_models import Book, ChapterSegment
from app.services.embed import embed_and_save_chapter
from app.services.llm_service import normalize_text_for_speech
from app.services.pdf_service import extract_chapters_smart
from app.services.tts_service import generate_audio_and_get_duration

logger = logging.getLogger("background")

# Chapter concurrency limiter (tối đa 3 chương xử lý song song)
sem = asyncio.Semaphore(5)


# -----------------------------------------------------------------------
# BACKGROUND: 2 luồng song song RAG + TTS cho từng chapter
# -----------------------------------------------------------------------
async def _thread_1_rag(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
) -> None:
    """Luồng 1: Cắt chunks → Embed → Lưu vào book_knowledge."""
    with Session(engine) as session:
        await embed_and_save_chapter(book_id, chapter_id, raw_text, session)


async def _thread_2_tts(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """Luồng 2: LLM rewrite → TTS → Upload Storage → Lưu chapter_segments."""
    # Step 1: LLM Rewrite
    obj_chapter = await normalize_text_for_speech(raw_text)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # Lưu review_text vào chapter
    if review_text:
        with Session(engine) as session:
            update_chapter_review_text(session, chapter_id, review_text)

    # Step 2: TTS + Upload từng segment
    segments: list[ChapterSegment] = []
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/part_{i + 1}.mp3"
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            segments.append(
                ChapterSegment(
                    chapter_id=chapter_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                )
            )
        except Exception as seg_err:
            # Một segment thất bại — log kèm nội dung text để debug
            text_preview = script[:80] if script else "(empty)"
            logger.warning(f"⚠️ Segment {i + 1} chương {chapter_index + 1} lỗi TTS ({len(script)} chars, text='{text_preview}...'): {seg_err}")
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)

    # Step 3: Bulk save segments
    if segments:
        with Session(engine) as session:
            bulk_create_segments(session, segments)

    # Step 4 (optional): Sinh audio review
    if review_text and review_text.strip():
        local_review = f"uploads/{uuid.uuid4()}.mp3"
        try:
            await generate_audio_and_get_duration(review_text, local_review)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/review.mp3"
            review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
            with Session(engine) as session:
                update_chapter_review_audio(session, chapter_id, review_url)
        except Exception as rev_err:
            logger.warning(f"⚠️ Review audio chương {chapter_index + 1} lỗi, bỏ qua: {rev_err}")
        finally:
            if os.path.exists(local_review):
                os.remove(local_review)


async def _process_single_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """Xử lý 1 chương: chạy 2 luồng song song, bị giới hạn bởi Semaphore."""
    async with sem:
        try:
            await asyncio.gather(
                _thread_1_rag(book_id, chapter_id, raw_text),
                _thread_2_tts(book_id, chapter_id, chapter_index, raw_text, mode),
            )
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, "READY")
            logger.info(f"✅ Chapter {chapter_index + 1} READY")
        except Exception as e:
            logger.error(f"❌ Error processing chapter {chapter_index + 1}: {e}")
            # [FIX BUG 2] Rollback đúng thứ tự:
            # Phải xóa book_knowledge (có FK trỏ vào chapter) TRƯỚC khi xóa chapter
            try:
                with Session(engine) as session:
                    delete_knowledge_by_chapter(session, chapter_id)
                    delete_chapter(session, chapter_id)
                logger.info(f"🗑️ Rollback chapter {chapter_index + 1} thành công.")
            except Exception as del_err:
                logger.error(f"Failed to rollback chapter {chapter_index + 1}: {del_err}")
            raise


async def run_background_processing(book_id: uuid.UUID, mode: str) -> None:
    """
    Điều phối xử lý tất cả chapters song song.
    1. Fetch draft chapters từ DB.
    2. Download PDF từ Supabase Storage (file_url đã lưu lúc /upload).
    3. Re-extract text per-chapter, ghép với draft chapters theo chapter_index.
    4. Chạy 2 luồng song song: RAG + TTS cho từng chapter.
    """
    import io

    try:
        # 1. Fetch book + draft chapters từ DB
        with Session(engine) as session:
            book = session.get(Book, book_id)
            draft_chapters = get_draft_chapters_by_book(session, book_id)

        if not book:
            logger.error(f"Book {book_id} not found")
            return

        if not draft_chapters:
            with Session(engine) as session:
                update_book_status(session, book_id, "ERROR", "Không có chapter nào để xử lý.")
            return

        if not book.file_url or book.file_url == "pending":
            with Session(engine) as session:
                update_book_status(session, book_id, "ERROR", "file_url chưa được lưu — PDF chưa upload lên Storage.")
            logger.error(f"book.file_url is missing for book {book_id}")
            return

        # 2. Download PDF từ Supabase Storage
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF from Storage: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)

        # 3. Re-extract chapters (giữ text thật theo từng chapter)
        chapters_data = await extract_chapters_smart(pdf_file)

        # Ghép chapters_data với draft_chapters theo chapter_index
        # (draft_chapters đã sort theo chapter_index từ get_draft_chapters_by_book)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # 4. Tạo tasks song song cho từng chapter
        tasks = []
        for draft_chap in draft_chapters:
            raw_text = chapters_map.get(draft_chap.chapter_index, "")
            if not raw_text.strip():
                logger.warning(f"⚠️ Chapter {draft_chap.chapter_index + 1} '{draft_chap.title}' không có text — bỏ qua.")
                continue
            tasks.append(
                _process_single_chapter(
                    book_id,
                    draft_chap.id,
                    draft_chap.chapter_index,
                    raw_text,
                    mode,
                )
            )

        await asyncio.gather(*tasks)

        with Session(engine) as session:
            update_book_status(session, book_id, "READY")
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, "ERROR", str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")

```

### app\helper\upload2supabase.py

```py
import asyncio
import logging

import aiofiles

from app.core.supabase import supabase

logger = logging.getLogger("upload")


# -----------------------------------------------------------------------
# Helper: Upload file lên Supabase Storage
# -----------------------------------------------------------------------
async def upload_file_to_supabase(
    local_path: str,
    storage_path: str,
    bucket: str,
    content_type: str,
    max_retries: int = 3,
) -> str:
    """Upload file lên Supabase Storage và trả về public URL."""
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": content_type},
            )
            return supabase.storage.from_(bucket).get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Upload failed (attempt {attempt + 1}), retrying...")
                await asyncio.sleep(2**attempt)
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise

```

### app\main.py

```py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sqlmodel import SQLModel

from app.api.v1.endpoints import audiobooks, live, upload
from app.db import engine
from app.models import db_models  # Import db_models để SQLAlchemy nhận diện
from app.services.tts_service import stream_text_to_speech, stream_text_to_speech_edge


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Chạy khi STARTUP ---
    print("Đang khởi tạo database...")
    SQLModel.metadata.create_all(engine)

    yield  # Sau từ khóa yield là lúc ứng dụng đang chạy (đang phục vụ người dùng)
    # --- Chạy khi SHUTDOWN ---
    print("Đang dọn dẹp tài nguyên...")
    # (Ví dụ: đóng kết nối database nếu cần)


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)


# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


@app.get("/test-voice-stream")
async def test_voice_stream(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech(text), media_type="audio/mpeg")


@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech_edge(text), media_type="audio/mpeg")


if __name__ == "__main__":
    import uvicorn

    # Reload=True để code tới đâu server cập nhật tới đó
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

### app\models\db_models.py

```py
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    author: Optional[str] = Field(default=None, sa_column=Column(Text))
    file_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_chapters: Optional[int] = Field(default=None, sa_column=Column(Integer))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))


class ReadingPlan(SQLModel, table=True):
    __tablename__ = "reading_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    mode: str = Field(sa_column=Column(Text, nullable=False))
    pace: int = Field(sa_column=Column(Integer, nullable=False))
    schedule_config: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
    status: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))


class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    chapter_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    review_audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    review_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))


class ChapterSegment(SQLModel, table=True):
    __tablename__ = "chapter_segments"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: uuid.UUID = Field(foreign_key="chapters.id")
    segment_index: int = Field(sa_column=Column(Integer, nullable=False))
    audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    duration_ms: Optional[int] = Field(default=None, sa_column=Column(Integer))


class BookKnowledge(SQLModel, table=True):
    __tablename__ = "book_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    chapter_id: uuid.UUID = Field(foreign_key="chapters.id")
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    # Giả định vector có độ dài 1536 (OpenAI text-embedding-3-small)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))

```

### app\services\embed.py

```py
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
from sqlmodel import Session

from app.core.config import settings
from app.crud.book_knowledge import bulk_create_knowledge
from app.models.db_models import BookKnowledge

aclient = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""],
)


async def embed_and_save_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
    session: Session,
) -> None:
    """
    Luồng 1 RAG:
    1. Cắt raw_text thành chunks bằng RecursiveCharacterTextSplitter.
    2. Gọi OpenAI Embedding API (batch).
    3. Lưu vào bảng book_knowledge qua SQLModel session.
    """
    chunks = _splitter.split_text(raw_text)
    if not chunks:
        return

    response = await aclient.embeddings.create(
        input=chunks,
        model="text-embedding-3-small",
    )

    records = [
        BookKnowledge(
            book_id=book_id,
            chapter_id=chapter_id,
            chunk_index=i,
            content=chunks[i],
            embedding=embedding_data.embedding,
        )
        for i, embedding_data in enumerate(response.data)
    ]

    bulk_create_knowledge(session, records)
    print(f"✅ RAG: Saved {len(records)} vectors for chapter_id={chapter_id}")

```

### app\services\llm_service.py

```py
import json
import re

from openai import AsyncOpenAI

from app.core.config import settings

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Prompt được nâng cấp để trả về JSON và xử lý logic chia đoạn thông minh
SYSTEM_PROMPT_REWRITE = """
Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Nội dung tóm tắt để ôn tập..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""


def _chunk_text_fallback(text: str, max_chars: int = 1200) -> list[str]:
    """Phân chia văn bản thô dài thành các chunk nhỏ nếu LLM thất bại."""
    paragraphs = re.split(r"\n+", text.strip())
    chunks = []
    current_chunk = []
    current_length = 0

    for p in paragraphs:
        if len(p) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", p)
            for s in sentences:
                if current_length + len(s) > max_chars and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [s]
                    current_length = len(s)
                else:
                    current_chunk.append(s)
                    current_length += len(s)
        else:
            if current_length + len(p) > max_chars and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [p]
                current_length = len(p)
            else:
                current_chunk.append(p)
                current_length += len(p)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------

async def normalize_text_for_speech(raw_text: str) -> dict:
    """
    Gửi text thô cho Gemini/GPT để biên tập và cấu trúc lại dữ liệu.
    Trả về Dictionary: {"main_scripts": [], "review_script": ""}
    """
    # Sử dụng fallback phân rã động thay vì ném cả đoạn lớn vào 1 chuỗi.
    # Ngăn chặn việc LLM lỗi làm file audio bị dài 18+ phút.
    fallback_result = {"main_scripts": _chunk_text_fallback(raw_text), "review_script": "Không thể tạo tóm tắt do độ dài văn bản gốc quá lớn."}

    try:
        response = await client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REWRITE}, {"role": "user", "content": raw_text}],
            temperature=0.3,  # Giảm sáng tạo để format JSON chuẩn
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON
        parsed_data = json.loads(content)

        # Nếu LLM chia chuỗi dài quá, cưỡng chế cắt bằng tay thêm lần nữa
        # để ngăn chặn issue của Edge TTS (Mặc dù prompt đã yêu cầu 3-5 câu / chunk).
        final_main_scripts = []
        for script in parsed_data.get("main_scripts", fallback_result["main_scripts"]):
            if len(script) > 1800:
                final_main_scripts.extend(_chunk_text_fallback(script))
            else:
                final_main_scripts.append(script)

        parsed_data["main_scripts"] = final_main_scripts

        return parsed_data

    except json.JSONDecodeError as de:
        print(f"Lỗi Parse JSON từ LLM ({de}). Raw content: Length {len(content)}")
        # Cố gắng lấy vớt lại text nếu có thể
        try:
            return {"main_scripts": _chunk_text_fallback(content), "review_script": "Rất tiếc tóm tắt của đoạn văn này bị lỗi do bộ nhớ quá giới hạn."}
        except:
            return fallback_result

    except Exception as e:
        print(f"Lỗi LLM Service: {e}")
        return fallback_result

```

### app\services\pdf_service.py

```py
import re

import pdfplumber
from pypdf import PdfReader


def get_pdf_outline_structure(file_obj):
    """
    Hàm này cố gắng đọc Mục lục (Bookmarks) từ metadata của PDF.
    Trả về: List [{"title": "Chapter 1", "page_start": 5}, ...] hoặc [] nếu không có.
    """
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        # reader.outline chứa cấu trúc mục lục
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    # Đệ quy nếu có mục lục con (Sub-chapter)
                    _parse_outline(item)
                else:
                    try:
                        # Lấy số trang (pypdf trả về page object, cần lấy index)
                        page_number = reader.get_destination_page_number(item)
                        # pypdf get đúng page number
                        outline_data.append({"title": item.title, "page_start": page_number})
                    except Exception:
                        pass  # Bỏ qua nếu item bị lỗi link

        _parse_outline(reader.outline)

        # Sắp xếp lại theo số trang để chắc chắn thứ tự đúng
        outline_data.sort(key=lambda x: x["page_start"])
        return outline_data
    except Exception as e:
        print(f"Lỗi đọc Outline: {e}")
        return []


async def extract_chapters_smart(file_obj, pages_per_chunk=10):
    """
    Hàm xử lý thông minh 3 cấp độ:
    Level 1: Dùng Outline (Mục lục ẩn).
    Level 2: Dùng Regex quét text.
    Level 3: Cắt theo số trang cố định.
    """
    # --- LEVEL 1: Dùng Mục lục Metadata ---
    # Lưu ý: Phải reset pointer file về 0 trước khi đọc
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)

    chapters = []

    if outlines and len(outlines) > 1:
        print(">> Đã tìm thấy Mục lục Metadata (Outline). Sử dụng Level 1.")

        # Mở lại bằng pdfplumber để lấy text (pdfplumber extract text ngon hơn pypdf)
        file_obj.seek(0)
        with pdfplumber.open(file_obj) as pdf:
            total_pages = len(pdf.pages)

            for i in range(len(outlines)):
                current_chap = outlines[i]
                start_p = current_chap["page_start"] - 1  # index từ 0

                # Xác định trang kết thúc (là trang bắt đầu của chương sau - 1)
                if i < len(outlines) - 1:
                    end_p = outlines[i + 1]["page_start"] - 1
                else:
                    end_p = total_pages  # Chương cuối thì lấy hết

                # Đảm bảo không vượt quá file
                end_p = min(end_p, total_pages)

                # Gom text từ start_p đến end_p
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    text = pdf.pages[p_idx].extract_text()
                    if text:
                        chap_text += text + "\n"

                if chap_text.strip():
                    chapters.append({"title": current_chap["title"], "text": chap_text, "page_start": start_p + 1, "page_end": end_p})
        return chapters

    # --- LEVEL 2: Dùng Regex (Nếu Level 1 thất bại) ---
    print(">> Không có Mục lục Metadata. Chuyển sang Level 2 (Regex Scan).")
    file_obj.seek(0)

    # Compile regex patterns cho tiêu đề chương
    chapter_patterns = [
        r"^\s*(?:Chương|CHƯƠNG|Chapter|CHAPTER)\s+(?:[IVX]+|\d+)",  # Chương 1, Chapter I, etc.
        r"^\s*(?:Phần|PHẦN|Part|PART)\s+(?:[IVX]+|\d+)",  # Phần 1, Part I, etc.
    ]
    combined_pattern = re.compile("|".join(chapter_patterns), re.MULTILINE)

    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        chapter_markers = []  # List of {title, page_idx}

        # Quét từng trang tìm tiêu đề
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            # Tách thành từng dòng và kiểm tra
            lines = text.split("\n")
            for line in lines[:10]:  # Chỉ check 10 dòng đầu mỗi trang
                if combined_pattern.match(line.strip()):
                    chapter_markers.append({"title": line.strip(), "page_idx": page_idx})
                    break  # Tìm được tiêu đề rồi thì next page

        # Nếu tìm được ít nhất 2 chương
        if len(chapter_markers) >= 2:
            print(f">> Tìm được {len(chapter_markers)} chương bằng Regex.")

            for i in range(len(chapter_markers)):
                start_p = chapter_markers[i]["page_idx"]

                # Xác định trang kết thúc
                if i < len(chapter_markers) - 1:
                    end_p = chapter_markers[i + 1]["page_idx"]
                else:
                    end_p = total_pages

                # Extract text từ start đến end
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    chap_text += (pdf.pages[p_idx].extract_text() or "") + "\n"

                if chap_text.strip():
                    chapters.append({"title": chapter_markers[i]["title"], "text": chap_text, "page_start": start_p + 1, "page_end": end_p})

            return chapters  # Return kết quả Level 2

    # --- LEVEL 3: Cắt Page cố định (Fallback cuối cùng) ---
    print(">> Không quét được tiêu đề. Chuyển sang Level 3 (Fixed Page Chunk).")
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        for i in range(0, total_pages, pages_per_chunk):
            chunk_text = ""
            end_page = min(i + pages_per_chunk, total_pages)
            for p_idx in range(i, end_page):
                chunk_text += (pdf.pages[p_idx].extract_text() or "") + "\n"

            chapters.append({"title": f"Phần {i // pages_per_chunk + 1} (Trang {i + 1}-{end_page})", "text": chunk_text, "page_start": i + 1, "page_end": end_page})

    return chapters


async def extract_text_from_pdf(file_obj, max_pages=None):
    """
    Helper function: Extract raw text từ PDF (không chia chương).
    Dùng cho demo endpoints như /process-book-intro.

    Args:
        file_obj: File object của PDF
        max_pages: Số trang tối đa cần extract (None = all pages)

    Returns:
        str: Raw text từ PDF
    """
    file_obj.seek(0)
    extracted_text = ""

    with pdfplumber.open(file_obj) as pdf:
        pages_to_read = len(pdf.pages) if max_pages is None else min(max_pages, len(pdf.pages))

        for i in range(pages_to_read):
            text = pdf.pages[i].extract_text()
            if text:
                extracted_text += text + "\n"

    return extracted_text.strip()


def extract_text_by_page_range(pdf_obj, start_page: int, end_page: int):
    """
    Trích xuất text từ trang A đến trang B.
    - pdf_obj: Đối tượng pdfplumber đã mở.
    - start_page: Số trang thực tế (ví dụ: 5).
    - end_page: Số trang thực tế (ví dụ: 10).
    -> Trả về text của trang 5, 6, 7, 8, 9, 10.
    """
    extracted_text = ""

    # Validate: Đảm bảo trang kết thúc không vượt quá tổng số trang
    total_pages = len(pdf_obj.pages)
    if end_page > total_pages:
        end_page = total_pages

    # Vòng lặp lấy text
    # LƯU Ý: Python index bắt đầu từ 0.
    # Nếu muốn lấy trang 5 (start_page), index phải là 4 (start_page - 1).
    # Hàm range(a, b) chạy đến b-1, nên tham số thứ 2 là end_page (tương ứng index end_page-1)

    # Ví dụ: Lấy trang 5 đến 7.
    # start_page=5 -> index=4
    # end_page=7
    # range(4, 7) sẽ chạy qua index: 4 (trang 5), 5 (trang 6), 6 (trang 7). CHUẨN.

    for i in range(start_page - 1, end_page):
        try:
            page = pdf_obj.pages[i]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception as e:
            print(f"Lỗi đọc trang {i + 1}: {e}")

    return extracted_text


def extract_clean_text(page):
    """
    Chỉ lấy phần thân trang, bỏ Header (trên cùng) và Footer (số trang dưới cùng)
    """
    width = page.width
    height = page.height

    # Giả sử Header chiếm 50px trên cùng, Footer chiếm 50px dưới cùng
    # Tọa độ crop: (x0, top, x1, bottom)
    bounding_box = (0, 50, width, height - 50)

    try:
        cropped_page = page.crop(bounding_box)
        return cropped_page.extract_text()
    except ValueError:
        # Fallback nếu trang không crop được (ví dụ trang trắng)
        return page.extract_text()

```

### app\services\rag_service.py

```py
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.supabase import supabase

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def search_book_knowledge(query: str, book_id: str):
    # 1. Tạo embedding cho câu hỏi của user
    res = await ai_client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC match_book_knowledge đã tạo ở Supabase
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.2,
        "match_count": 3,
        "filter_book_id": book_id
    }).execute()

    if not result.data:
        return "Không tìm thấy thông tin cụ thể trong sách."

    return "\n".join([item['content'] for item in result.data])

```

### app\services\tts_service.py

```py

import asyncio

import edge_tts
from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def stream_text_to_speech(text: str, voice: str = "alloy"):
    """
    Hàm này nhận text, gọi OpenAI TTS và trả về stream audio ngay lập tức.
    """
    try:
        async with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text,
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk

    except Exception as e:
        print(f"Error in TTS Stream: {e}")


async def stream_text_to_speech_edge(text: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Sử dụng Edge TTS: Hoàn toàn MIỄN PHÍ và chất lượng Neural rất tốt.
    """
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


async def generate_audio_file_edge(text: str, filename: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Tạo file audio từ text bằng Edge TTS và lưu vào file.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"✓ Audio saved to {filename}")
    except Exception as e:
        print(f"Error creating audio file: {e}")


# -----------------------------------------------------------------------
# Giới hạn concurrent TTS calls.
# Microsoft Edge TTS service đang bị intermittent failure (Apr 2026).
# Ref: https://github.com/rany2/edge-tts/issues/473
# Semaphore(5) giúp giảm áp lực lên server, tăng tỉ lệ thành công.
# -----------------------------------------------------------------------
_tts_sem = asyncio.Semaphore(5)


async def generate_audio_and_get_duration(
    text: str,
    filename: str,
    voice: str = settings.EDGE_TTS_VOICE,
    max_retries: int = 6,
) -> int:
    """
    Tạo file audio bằng Edge TTS và đo thời lượng (milliseconds).

    - Semaphore(5): giới hạn 5 TTS calls đồng thời (tránh overwhelm server)
    - 6 retries với backoff dài: 3s, 6s, 12s, 24s, 48s
    - receive_timeout=300: chờ Microsoft server đủ lâu
    - KHÔNG dùng voice fallback: giữ giọng đọc nhất quán

    Trả về duration_ms.
    """
    from mutagen.mp3 import MP3

    # Clean and Valid text: too short (page numbers, special characters)
    cleaned = text.strip()
    if len(cleaned) < 10:
        raise ValueError(f"Text too short for TTS ({len(cleaned)} chars): '{cleaned}'")

    async with _tts_sem:
        for attempt in range(max_retries):
            try:
                communicate = edge_tts.Communicate(
                    cleaned,
                    voice,
                    receive_timeout=300,
                )
                await communicate.save(filename)

                try:
                    audio = MP3(filename)
                    duration_ms = int(audio.info.length * 1000)
                except Exception:
                    duration_ms = 0

                return duration_ms

            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 3 * (2 ** attempt)  # 3s, 6s, 12s, 24s, 48s
                    print(
                        f"⚠️ TTS attempt {attempt + 1}/{max_retries} failed "
                        f"({len(cleaned)} chars): {e}. Retry in {wait}s..."
                    )
                    await asyncio.sleep(wait)
                else:
                    print(f"❌ TTS failed after {max_retries} attempts ({len(cleaned)} chars): {e}")
                    raise
    return 0  # unreachable

```

### app\services\__init__.py

```py
# Services module

```

### app\__init__.py

```py
# TRIAM Backend Application

```
