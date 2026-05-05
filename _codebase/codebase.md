# Project Export

## Project Statistics

- Total files: 37

## Folder Structure

```
app
  api
    v1
      endpoints
        audiobooks.py
        live.py
        study_context.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    config.py
    constant.py
    supabase.py
    __init__.py
  crud
    audiobook.py
    book_knowledge.py
    chapter.py
    chapter_segment.py
    plan.py
    study_context.py
    study_context_document_link.py
    study_context_thread.py
  db.py
  helper
    run_background_processing.py
    upload2supabase.py
  main.py
  models
    db_models.py
  schemas
    plan.py
    study_context.py
  services
    agent_voice.py
    embed.py
    llm_service.py
    pdf_service.py
    rag_service.py
    tts_service.py
    __init__.py
  __init__.py
.python-version
pyproject.toml
rpc_match_book_knowledge.md

```

### app\api\v1\endpoints\audiobooks.py

```py
import json
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.repositories import audiobook as crud_book
from app.repositories.chapter_segment import count_segments_by_book_and_mode
from app.db import get_session
from app.helper.run_background_processing import run_switch_mode_processing
from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan
from app.schemas.plan import SwitchModeRequest

router = APIRouter()


@router.get("/books", response_model=list[Book])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return crud_book.get_audiobooks(session)


@router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return crud_book.get_book_by_id(session, book_id)


@router.post("/books", response_model=Book)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return crud_book.create_book(session, book)


@router.delete("/book/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await crud_book.delete_book_storage(session, book_id)
    return {"message": "Book deleted"}


@router.get("/books/{book_id}/details")
def get_book_details(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 1. Kiểm tra plan chặt chẽ
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise HTTPException(status_code=400, detail="User has no reading plan for this book")

    try:
        active_mode = PlanMode(plan.mode)
    except ValueError as e:
        print(f"Critical Error: Invalid mode '{plan.mode}' in DB for book {book_id}")
        raise HTTPException(status_code=500, detail="Data integrity error") from e

    # 2. Giải quyết N+1 bằng cách lấy TẤT CẢ segments một lần duy nhất
    chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()

    chapter_ids = [c.id for c in chapters]
    all_segments = session.exec(select(ChapterSegment).where(ChapterSegment.chapter_id.in_(chapter_ids), ChapterSegment.mode == active_mode).order_by(ChapterSegment.segment_index)).all()

    # Nhóm segments theo chapter_id để truy xuất nhanh
    segments_map = {}
    for s in all_segments:
        segments_map.setdefault(s.chapter_id, []).append(s.model_dump())

    # 3. Helper function để xử lý JSON "bẩn"
    def extract_json_content(raw_data, mode):
        if not raw_data:
            return ""
        try:
            data = json.loads(raw_data)
            return data.get(mode, "")
        except (json.JSONDecodeError, TypeError) as e:
            raise HTTPException(status_code=500, detail="Data integrity error") from e

    # 4. Gom kết quả
    result = []
    for chap in chapters:
        result.append(
            {
                "id": str(chap.id),
                "title": chap.title,
                "status": chap.status,
                "chapter_index": chap.chapter_index,
                "review_text": extract_json_content(chap.review_text, active_mode),
                "review_audio_url": extract_json_content(chap.review_audio_url, active_mode),
                "chapter_segments": segments_map.get(chap.id, []),
            }
        )

    return {"book_status": book.status, "total_chapters": book.total_chapters, "chapters": result}


@router.post("/books/{book_id}/switch-mode")
def switch_book_mode(book_id: uuid.UUID, payload: SwitchModeRequest, background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""

    payload_mode = payload.mode

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 1. Lấy ReadingPlan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Chưa có ReadingPlan cho sách này")

    # 2. Nếu switch sang cùng mode đang active → không cần làm gì thêm
    if plan.mode == payload_mode:
        # Đếm tổng segments trên toàn bộ sách (không chỉ chapter 1)
        total = count_segments_by_book_and_mode(session, book_id, payload_mode)
        if total > 0:
            return {"message": f"Đã ở mode {payload_mode} và audio đã có sẵn ({total} segments).", "needs_generation": False}
        else:
            # Đang ở đúng mode nhưng chưa có segments (do gen thất bại trước)
            background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
            return {"message": f"Mode {payload_mode} chưa có audio, đang gen lại.", "needs_generation": True}

    # 3. Cập nhật mode mới vào ReadingPlan
    plan.mode = payload_mode
    session.add(plan)
    session.commit()

    # 4. Kiểm tra xem audio của mode mới đã được sinh ra bao giờ chưa
    # Dùng count toàn sách — tránh trường hợp chương 1 có segment nhưng chương khác không có
    total = count_segments_by_book_and_mode(session, book_id, payload_mode)
    needs_generation = total == 0

    # 5. Kích hoạt Background Task sinh audio nếu cần
    if needs_generation:
        background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
        return {"message": f"Đã chuyển sang mode {payload_mode}. Hệ thống đang sinh audio trong background.", "needs_generation": True}

    return {"message": f"Đã chuyển sang mode {payload_mode}. Audio đã có sẵn.", "needs_generation": False}

```

### app\api\v1\endpoints\live.py

```py
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from livekit import api
from sqlmodel import Session, select

from app.core.config import settings
from app.db import get_session
from app.models.db_models import ChatThread, StudyContextDocumentLink

router = APIRouter()


@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    # Cấu hình dispatch Agent ngay khi user join room
    # Điều này bắt buộc để LiveKit FE Flutter Session nhận diện được 'dispatchesAgent: true'
    session_room_name = f"triam_{book_id[:8]}_{uuid.uuid4().hex[:6]}"

    agent_dispatch = api.RoomAgentDispatch(agent_name=settings.LIVEKIT_AGENT_NAME, metadata=json.dumps({"book_id": book_id}))
    room_config = api.RoomConfiguration(agents=[agent_dispatch])

    # Create Token for user join room
    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=session_room_name,
            )
        )
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": session_room_name}

@router.get("/live-token/thread/{thread_id}")
async def get_token_thread(thread_id: uuid.UUID, session: Session = Depends(get_session)):
    # 1. Validate thread and get context
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # 2. Get document_ids for context
    links = session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == thread.context_id)
    ).all()
    document_ids = [str(link.book_id) for link in links]

    # Cấu hình dispatch Agent ngay khi user join room
    session_room_name = f"triam_{str(thread_id)[:8]}_{uuid.uuid4().hex[:6]}"

    agent_dispatch = api.RoomAgentDispatch(
        agent_name=settings.LIVEKIT_AGENT_NAME,
        metadata=json.dumps({
            "thread_id": str(thread_id),
            "context_id": str(thread.context_id),
            "document_ids": document_ids
        })
    )
    room_config = api.RoomConfiguration(agents=[agent_dispatch])

    # Create Token for user join room
    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=session_room_name,
            )
        )
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": session_room_name}

```

### app\api\v1\endpoints\study_context.py

```py
import logging
import uuid
from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.repositories.audiobook import get_book_by_id
from app.repositories.study_context import (
    create_study_context,
    delete_study_context,
    get_study_context,
    get_study_contexts,
    update_study_context,
)
from app.repositories.study_context_document_link import (
    create_new_context_document,
    delete_study_context_document,
)
from app.repositories.study_context_thread import (
    create_new_thread,
    get_chat_history_by_thread_id,
    get_chat_threads_for_context,
)
from app.db import get_session
from app.models.db_models import ChatMessage, ChatThread, StudyContext, StudyContextDocumentLink
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)

logger = logging.getLogger("study_context")
router = APIRouter()

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")

# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContext])
async def get_study_contexts_api(session: Annotated[Session, Depends(get_session)]):
    return get_study_contexts(session, MOCK_USER_ID)


@router.get("/study-contexts/{context_id}", response_model=StudyContext)
async def get_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")
    return context


@router.post("/study-contexts", response_model=StudyContext)
async def create_study_context_api(payload: StudyContextInput, session: Annotated[Session, Depends(get_session)]):
    context = StudyContext(
        user_id=MOCK_USER_ID,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_study_context(session, context)


@router.patch("/study-contexts/{context_id}", response_model=StudyContext)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    updated_context = update_study_context(session, context_id, payload.title)
    if not updated_context:
        raise HTTPException(status_code=404, detail="Study context not found")
    return updated_context


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    delete_study_context(session, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=StudyContextDocumentLink)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, session: Annotated[Session, Depends(get_session)]):
    book = get_book_by_id(session, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    delete_study_context_document(session, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThread])
async def get_chat_threads_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")
    return get_chat_threads_for_context(session, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThread)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, session: Annotated[Session, Depends(get_session)]):
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessage])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_chat_history_by_thread_id(session, thread_id)

```

### app\api\v1\endpoints\upload.py

```py
import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Body, File, HTTPException, UploadFile
from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanStatus
from app.repositories.audiobook import create_book, update_book_status
from app.repositories.chapter import create_chapter
from app.repositories.plan import create_reading_plan
from app.db import engine
from app.helper.run_background_processing import run_background_processing
from app.helper.upload2supabase import upload_file_to_supabase
from app.models.db_models import Book, Chapter, ReadingPlan
from app.schemas.plan import PlanInput
from app.services.pdf_service import extract_chapters_smart

logger = logging.getLogger("upload")

router = APIRouter()

# -----------------------------------------------------------------------
# Mock User — thay bằng JWT decode sau khi tích hợp Auth
# -----------------------------------------------------------------------
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


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
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()

    if not is_valid_type:
        # Fallback kiểm tra bằng đuôi file
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise HTTPException(status_code=400, detail=f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File vượt quá giới hạn 50MB.")

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)
    chapters_data = []
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract outline
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
                    title=chap.get("title", "Empty Chapter"),
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
async def generate_plan(background_tasks: BackgroundTasks, payload: PlanInput = Body(...)):  # noqa: B008
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    # 1. Validate book tồn tại
    with Session(engine) as session:
        book = session.get(Book, payload.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Không tìm thấy sách.")
        if book.status not in (BookStatus.DRAFT):
            raise HTTPException(status_code=409, detail=f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    # 3. Lưu ReadingPlan + cập nhật Book status
    try:
        with Session(engine) as session:
            plan = ReadingPlan(
                book_id=payload.book_id,
                mode=payload.mode,
                pace=payload.pace,
                schedule_config=payload.schedule_config,
                status=PlanStatus.ACTIVE,
            )
            create_reading_plan(session, plan)
            update_book_status(session, payload.book_id, BookStatus.PROCESSING)

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

### app\api\v1\endpoints\_\_init\_\_.py

```py
# API Endpoints module

```

### app\api\v1\_\_init\_\_.py

```py
# API v1 module

```

### app\api\_\_init\_\_.py

```py
# API v1 module

```

### app\core\config.py

```py
import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or ""
    PINECONE_ENV = os.getenv("PINECONE_ENV") or ""
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or ""
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL") or ""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
    DATABASE_URL = os.getenv("DATABASE_URL") or ""
    SUPABASE_URL = os.getenv("SUPABASE_URL") or ""
    SUPABASE_KEY = os.getenv("SUPABASE_KEY") or ""
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
    EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-AvaMultilingualNeural") or ""
    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY") or ""
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET") or ""
    LIVEKIT_AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME") or ""
    GEMINI_MODEL_NATIVE_AUDIO = os.getenv("GEMINI_MODEL_NATIVE_AUDIO", "gemini-2.5-flash-native-audio-latest") or ""

    # Upload file
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }


settings = Settings()

```

### app\core\constant.py

```py
from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class BookStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class PlanMode(str, Enum):
    FULL = "full"
    PARETO = "pareto"

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

### app\core\_\_init\_\_.py

```py
# Core module

```

### app\crud\audiobook.py

```py
import uuid
from typing import Optional

from sqlmodel import Session, select

from app.core.supabase import supabase
from app.models.db_models import Book


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


def delete_book(session: Session, book_id: uuid.UUID) -> None:
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


async def delete_book_storage(session: Session, book_id: uuid.UUID):
    """
    Xóa sạch assets trong Storage và bản ghi trong Database.
    """
    str_book_id = str(book_id)
    target_buckets = ["audios", "raw_books"]

    try:
        # 1. Lấy danh sách file từ tất cả bucket liên quan qua RPC (SELECT)
        result = supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute()

        # 2. Phân loại và xóa file qua Storage API
        if result.data:
            for bucket in target_buckets:
                # Lọc ra danh sách file thuộc bucket hiện tại
                paths = [item["name"] for item in result.data if item["bucket_id"] == bucket]

                if paths:
                    # Xóa hàng loạt file trong bucket này (Đúng quy trình API)
                    supabase.storage.from_(bucket).remove(paths)
                    print(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # 3. Xóa record trong DB
        delete_book(session, book_id)
        print(f"Đã dọn dẹp sạch sẽ database cho book: {str_book_id}")

    except Exception as e:
        # Rollback session nếu có lỗi ở tầng DB để tránh mất dữ liệu không đồng bộ
        session.rollback()
        print(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise e

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

### app\crud\chapter.py

```py
import json
import uuid

from aiohttp.web import HTTPException
from sqlmodel import Session, select

from app.models.db_models import Chapter


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)
    return list(session.exec(statement).all())


def create_chapter(session: Session, chapter: Chapter) -> Chapter:
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_audio = json.loads(chapter.review_audio_url) if chapter.review_audio_url else {}
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Data integrity error: {e}")
            raise HTTPException(status_code=500, detail="Data integrity error") from e

        reviews_audio[mode] = review_audio_url
        chapter.review_audio_url = json.dumps(reviews_audio, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def update_chapter_status(session: Session, chapter_id: uuid.UUID, status: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.status = status
        session.add(chapter)
        session.commit()


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_text = json.loads(chapter.review_text) if chapter.review_text else {}
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Data integrity error: {e}")
            raise HTTPException(status_code=500, detail="Data integrity error") from e

        reviews_text[mode] = review_text
        chapter.review_text = json.dumps(reviews_text, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()

```

### app\crud\chapter_segment.py

```py
import uuid

from sqlmodel import Session, func, select

from app.models.db_models import ChapterSegment


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    """Bulk tạo mới các segments."""
    for segment in segments:
        session.add(segment)
    session.commit()


def check_segments_exist_by_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> bool:
    """Kiểm tra xem đã có segment nào của mode này sinh ra chưa (trong 1 chapter)."""
    return (
        session.exec(
            select(ChapterSegment).where(
                ChapterSegment.chapter_id == chapter_id,
                ChapterSegment.mode == mode,
            )
        ).first()
        is not None
    )


def count_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: str) -> int:
    """
    Đếm tổng số segments của một mode trên toàn bộ sách.
    Dùng để xác định chính xác xem mode đó đã được gen hoàn chỉnh chưa.
    Thay thế check_segments_exist_by_mode khi cần kiểm tra cả sách.
    """
    from app.models.db_models import Chapter  # tránh circular import

    result = session.exec(
        select(func.count(ChapterSegment.id))
        .join(Chapter, ChapterSegment.chapter_id == Chapter.id)  # type: ignore[arg-type]
        .where(Chapter.book_id == book_id)
        .where(ChapterSegment.mode == mode)
    ).one()
    return result or 0


def delete_segments_by_chapter_and_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> None:
    """Xóa tất cả các segments của 1 chapter theo mode (dùng khi gen lại)."""
    segments = session.exec(
        select(ChapterSegment).where(
            ChapterSegment.chapter_id == chapter_id,
            ChapterSegment.mode == mode,
        )
    ).all()
    for s in segments:
        session.delete(s)
    session.commit()

```

### app\crud\plan.py

```py
import uuid

from sqlmodel import Session, select

from app.core.constant import PlanStatus
from app.models.db_models import ReadingPlan


def check_plan_exist(session: Session, book_id: uuid.UUID) -> bool:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first() is not None


def get_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()


def get_active_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id).where(ReadingPlan.status == PlanStatus.ACTIVE)).first()


def get_all_plan_by_user_id(session: Session, user_id: uuid.UUID) -> list[ReadingPlan]:
    return session.exec(select(ReadingPlan).where(ReadingPlan.user_id == user_id)).all()


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

```

### app\crud\study_context.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import StudyContext


def get_study_context(session: Session, context_id: uuid.UUID) -> StudyContext | None:
    return session.get(StudyContext, context_id)


def get_study_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return session.exec(select(StudyContext).where(StudyContext.user_id == user_id)).all()


def create_study_context(session: Session, study_context: StudyContext) -> StudyContext:
    session.add(study_context)
    session.commit()
    session.refresh(study_context)
    return study_context


def update_study_context(
    session: Session, context_id: uuid.UUID, title: str | None = None
) -> StudyContext | None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        if title is not None:
            study_context.title = title
        study_context.updated_at = datetime.now(timezone.utc)
        session.add(study_context)
        session.commit()
        session.refresh(study_context)
        return study_context
    return None


def delete_study_context(session: Session, context_id: uuid.UUID) -> None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        session.delete(study_context)
        session.commit()

```

### app\crud\study_context_document_link.py

```py
import uuid

from sqlmodel import Session, select

from app.models.db_models import StudyContextDocumentLink


def create_new_context_document(
    session: Session, link: StudyContextDocumentLink
) -> StudyContextDocumentLink:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_context_documents(session: Session, context_id: uuid.UUID) -> list[StudyContextDocumentLink]:
    return session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == context_id)
    ).all()


def delete_study_context_document(session: Session, context_id: uuid.UUID, book_id: uuid.UUID) -> None:
    link = session.exec(
        select(StudyContextDocumentLink).where(
            StudyContextDocumentLink.context_id == context_id, StudyContextDocumentLink.book_id == book_id
        )
    ).first()
    if link:
        session.delete(link)
        session.commit()

```

### app\crud\study_context_thread.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import ChatMessage, ChatThread


def get_chat_threads_for_context(session: Session, context_id: uuid.UUID) -> list[ChatThread]:
    threads = session.exec(select(ChatThread).where(ChatThread.context_id == context_id)).all()
    return threads


def get_chat_history_by_thread_id(session: Session, thread_id: uuid.UUID) -> list[ChatMessage]:
    messages = session.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()
    return messages


def create_new_thread(session: Session, thread: ChatThread) -> ChatThread:
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def update_thread_title(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def delete_thread(session: Session, thread_id: uuid.UUID) -> None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        session.delete(thread)
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

from sqlmodel import Session, select

from app.core.constant import BookStatus
from app.core.supabase import supabase
from app.repositories.audiobook import update_book_status
from app.repositories.book_knowledge import delete_knowledge_by_chapter
from app.repositories.chapter import (
    Chapter,
    delete_chapter,
    get_draft_chapters_by_book,
    update_chapter_review_audio,
    update_chapter_review_text,
    update_chapter_status,
)
from app.repositories.chapter_segment import bulk_create_segments, delete_segments_by_chapter_and_mode
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
    obj_chapter = await normalize_text_for_speech(raw_text, mode)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # Lưu review_text vào chapter
    if review_text:
        with Session(engine) as session:
            update_chapter_review_text(session, chapter_id, review_text, mode)

    # Step 2: TTS + Upload từng segment
    segments: list[ChapterSegment] = []
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/part_{i + 1}.mp3"
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            segments.append(
                ChapterSegment(
                    chapter_id=chapter_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                    mode=mode,
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
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/review.mp3"
            review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
            with Session(engine) as session:
                update_chapter_review_audio(session, chapter_id, review_url, mode)
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
                update_chapter_status(session, chapter_id, BookStatus.READY)
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
                update_book_status(session, book_id, BookStatus.ERROR, "Không có chapter nào để xử lý.")
            return

        if not book.file_url:
            with Session(engine) as session:
                update_book_status(session, book_id, BookStatus.ERROR, "file_url chưa được lưu — PDF chưa upload lên Storage.")
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
            update_book_status(session, book_id, BookStatus.READY)
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.ERROR, str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


async def _process_switch_mode_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
) -> None:
    """Xử lý switch mode 1 chương: chỉ chạy TTS, xóa segments cũ của mode này trước khi tạo."""
    async with sem:
        try:
            # 1. Xoá audio cũ của mode chuẩn bị gen (để ko bị trùng)
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, new_mode)

            # 2. Sinh Audio TTS mới
            await _thread_2_tts(book_id, chapter_id, chapter_index, raw_text, new_mode)

            logger.info(f"✅ Chapter {chapter_index + 1} SWITCH MODE {new_mode} READY")
        except Exception as e:
            logger.error(f"❌ Error switching mode chapter {chapter_index + 1}: {e}")
            raise


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str) -> None:
    """
    Luồng sinh audio riêng khi User switch mode:
    Bỏ qua RAG, lấy lại text từ PDF, gen audio TTS.
    """
    import io

    try:
        with Session(engine) as session:
            book = session.get(Book, book_id)
            chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id)).all()

        if not book or not book.file_url:
            logger.error(f"Cannot switch mode for book {book_id}: Invalid book or file_url")
            return

        # Tải PDF và lấy text gốc
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF for Switch Mode: {storage_path}")
        pdf_bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # Chạy task song song cho các chapter
        tasks = []
        for chap in chapters:
            raw_text = chapters_map.get(chap.chapter_index, "")
            if raw_text.strip():
                tasks.append(_process_switch_mode_chapter(book_id, chap.id, chap.chapter_index, raw_text, new_mode))

        await asyncio.gather(*tasks)
        logger.info(f"🎉 Sách {book_id} đã gen xong audio cho mode: {new_mode}.")

    except Exception as e:
        logger.error(f"❌ LỖI SWITCH MODE SÁCH {book_id}: {e}")

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
    upsert: bool = True,
) -> str:
    """
    Upload file lên Supabase Storage và trả về public URL.

    upsert=True (mặc định): Ghi đè nếu file đã tồn tại.
    Cần thiết để switch-mode hoạt động đúng (tránh 409 Duplicate).
    """
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
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

from app.api.v1.endpoints import audiobooks, live, study_context, upload
from app.db import engine
from app.models import db_models  # Import db_models để SQLAlchemy nhận diện
from app.services.tts_service import stream_text_to_speech_edge


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Chạy khi STARTUP ---
    print("Đang khởi tạo database...")
    SQLModel.metadata.create_all(engine)

    yield  # Sau từ khóa yield là lúc ứng dụng đang chạy (đang phục vụ người dùng)
    # --- Chạy khi SHUTDOWN ---
    print("Đang dọn dẹp tài nguyên...")


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)


# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])
app.include_router(study_context.router, prefix="/api/v1", tags=["Study Context"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


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

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

### app\models\db_models.py

```py
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlmodel import Field, Relationship, SQLModel

from app.core.constant import PlanMode


class StudyContextDocumentLink(SQLModel, table=True):
    __tablename__ = "study_context_document_links"
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, primary_key=True))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, primary_key=True))


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

    # === RELATIONSHIPS ===
    chapters: list["Chapter"] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    reading_plans: list["ReadingPlan"] = Relationship(back_populates="book")
    contexts: list["StudyContext"] = Relationship(back_populates="books", link_model=StudyContextDocumentLink)


class ReadingPlan(SQLModel, table=True):
    __tablename__ = "reading_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(Text, nullable=False))
    pace: int = Field(sa_column=Column(Integer, nullable=False))
    schedule_config: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
    status: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # === RELATIONSHIPS ===
    book: Book = Relationship(back_populates="reading_plans")


class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    chapter_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    review_audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    review_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))

    # === RELATIONSHIPS ===
    book: Book = Relationship(back_populates="chapters")
    segments: list["ChapterSegment"] = Relationship(back_populates="chapter", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChapterSegment(SQLModel, table=True):
    __tablename__ = "chapter_segments"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), index=True))
    segment_index: int = Field(sa_column=Column(Integer))
    audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    duration_ms: Optional[int] = Field(default=None, sa_column=Column(Integer))
    mode: PlanMode = Field(default=PlanMode.FULL, sa_column=Column(Text, nullable=False, server_default=PlanMode.FULL))

    # === RELATIONSHIPS ===
    chapter: Chapter = Relationship(back_populates="segments")


class BookKnowledge(SQLModel, table=True):
    __tablename__ = "book_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    chapter_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), index=True))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    # TODO: REPALCE 1536 (OpenAI text-embedding-3-small)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))


# === CONTEXT STUDY CONVERSATION===


class StudyContext(SQLModel, table=True):
    __tablename__ = "study_contexts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    is_auto_generated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # === RELATIONSHIPS ===
    books: list[Book] = Relationship(back_populates="contexts", link_model=StudyContextDocumentLink)
    threads: list["ChatThread"] = Relationship(back_populates="context", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatThread(SQLModel, table=True):
    __tablename__ = "chat_threads"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True))
    title: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # === RELATIONSHIPS ===
    context: StudyContext = Relationship(back_populates="threads")
    messages: list["ChatMessage"] = Relationship(back_populates="thread", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chat_threads.id", ondelete="CASCADE"), index=True))
    is_user: bool = Field(sa_column=Column(Boolean, nullable=False))
    text: str = Field(sa_column=Column(Text, nullable=False))
    source: str = Field(sa_column=Column(Text, nullable=False))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # === RELATIONSHIPS ===
    thread: ChatThread = Relationship(back_populates="messages")

```

### app\schemas\plan.py

```py
import uuid

from pydantic import BaseModel

from app.models.db_models import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]


class SwitchModeRequest(BaseModel):
    mode: PlanMode

```

### app\schemas\study_context.py

```py
import uuid

from pydantic import BaseModel


class StudyContextInput(BaseModel):
    title: str

class StudyContextUpdate(BaseModel):
    title: str | None = None

class StudyContextDocumentInput(BaseModel):
    book_id: uuid.UUID

class ChatThreadInput(BaseModel):
    title: str

class ChatThreadUpdate(BaseModel):
    title: str | None = None

```

### app\services\agent_voice.py

```py
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
from app.db import engine
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
        book_id = job_meta.get("book_id", "")
        thread_id = job_meta.get("thread_id", "")
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

```

### app\services\embed.py

```py
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
from sqlmodel import Session

from app.core.config import settings
from app.repositories.book_knowledge import bulk_create_knowledge
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
from app.core.constant import PlanMode

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Prompt được nâng cấp để trả về JSON và xử lý logic chia đoạn thông minh
SYSTEM_PROMPT_REWRITE_FULL = """
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

SYSTEM_PROMPT_REWRITE_PARETO = """
Bạn là một Chuyên gia Đọc nhanh & Giáo dục (TRIAM AI) áp dụng nguyên lý Pareto (80/20).
Nhiệm vụ: Chắt lọc 20% nội dung quan trọng nhất (ý chính, công thức, keyword) để mang lại 80% giá trị của văn bản gốc, sau đó chuyển thành kịch bản nói (TTS Script).

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. LƯỢC BỎ: Cắt bỏ hoàn toàn các ví dụ dài dòng, câu chuyện phụ, câu từ lan man "tốt thì biết".
2. TẬP TRUNG CỐT LÕI: Giữ lại định nghĩa, luận điểm chính, keyword (in đậm/in nghiêng trong ý đồ tác giả).
3. VĂN PHONG TTS: Nội dung chắt lọc phải được nối lại thành câu văn nói mượt mà, dễ hiểu, súc tích. Xử lý số liệu, chữ viết tắt như bình thường.
4. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
5. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
6. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
7. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
8. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Tóm tắt cốt lõi để ôn tập nhanh (100 từ)..."
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

async def normalize_text_for_speech(raw_text: str, mode: str) -> dict:
    """
    Gửi text thô cho Gemini/GPT để biên tập và cấu trúc lại dữ liệu.
    Trả về Dictionary: {"main_scripts": [], "review_script": ""}
    """
    # Sử dụng fallback phân rã động thay vì ném cả đoạn lớn vào 1 chuỗi.
    # Ngăn chặn việc LLM lỗi làm file audio bị dài 18+ phút.
    fallback_result = {"main_scripts": _chunk_text_fallback(raw_text), "review_script": "Không thể tạo tóm tắt do độ dài văn bản gốc quá lớn."}

    if mode.lower() == PlanMode.PARETO:
        mode_prompt = SYSTEM_PROMPT_REWRITE_PARETO
    else:
        # Default fallback to FULL
        mode_prompt = SYSTEM_PROMPT_REWRITE_FULL

    try:
        response = await client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "system", "content": mode_prompt}, {"role": "user", "content": raw_text}],
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

async def search_book_knowledge(query: str, document_ids: list[str]):
    # 1. Tạo embedding cho câu hỏi của user
    res = await ai_client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC match_book_knowledge đã tạo ở Supabase
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.3,
        "match_count": 10,
        "filter_book_ids": document_ids
    }).execute()

    if not result.data:
        return "Không tìm thấy thông tin cụ thể trong sách."

    return result.data

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

### app\services\_\_init\_\_.py

```py
# Services module

```

### app\_\_init\_\_.py

```py
# TRIAM Backend Application

```

### .python-version

_(Unsupported file type)_

### pyproject.toml

_(Unsupported file type)_

### rpc_match_book_knowledge.md

```md
      SELECT
        book_knowledge.id,
        book_knowledge.book_id,
        book_knowledge.chapter_id,
        book_knowledge.chunk_index,
        book_knowledge.content,
        1 - (book_knowledge.embedding <=> query_embedding) AS similarity
      FROM book_knowledge
      WHERE 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
        AND book_knowledge.book_id = ANY(filter_book_ids)
      ORDER BY book_knowledge.embedding <=> query_embedding
      LIMIT match_count;





    ///


    -- 4. Viết hàm RPC (Remote Procedure Call) để search vector

-- Hàm này giúp bạn gọi từ code Python/Flutter chỉ bằng 1 dòng
drop function if exists match_book_knowledge(vector, float, int, uuid[]);

create or replace function match_book_knowledge (
query_embedding vector(1536),
match_threshold float,
match_count int,
filter_book_ids uuid[]
)
returns table (
id integer,
book_id uuid,
chapter_id uuid,
chunk_index integer,
content text,
similarity float
)
language plpgsql
as $$
begin
return query
select
book_knowledge.id,
book_knowledge.book_id,
book_knowledge.chapter_id,
book_knowledge.chunk_index,
book_knowledge.content,
1 - (book_knowledge.embedding <=> query_embedding) as similarity
from book_knowledge
where 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
and book_knowledge.book_id = ANY(filter_book_ids)
order by book_knowledge.embedding <=> query_embedding
limit match_count;
end;

$$
;
$$
```
