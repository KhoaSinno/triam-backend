import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Body, File, HTTPException, UploadFile
from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanStatus
from app.crud.audiobook import create_book, update_book_status
from app.crud.chapter import create_chapter
from app.crud.plan import create_reading_plan
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
