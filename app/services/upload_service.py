import os
import uuid

import aiofiles
from fastapi import BackgroundTasks, UploadFile
from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanStatus
from app.core.exceptions import (
    BookNotFoundError,
    BookStatusConflictError,
    DatabaseError,
    DocumentOutlineRequiredError,
    FileTooLargeError,
    PdfExtractionError,
    UnsupportedFileTypeError,
)
from app.models.db_models import Book, Chapter, ReadingPlan
from app.repositories.audiobook_repo import create_book, update_book_status
from app.repositories.chapter_repo import create_chapter
from app.repositories.plan_repo import create_reading_plan
from app.schemas.plan import PlanInput
from app.services.pdf_service import extract_pdf_chapters
from app.services.storage_service import upload_file_to_supabase
from app.services.workers.book_pipeline import run_background_processing

from app.core.logger import log as logger

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")

# HELPER FUNCTION: Detect document type based on MIME type or file extension


def _detect_document_type(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if filename.endswith(".pdf") or content_type == "application/pdf":
        return "pdf"
    if filename.endswith(".epub") or content_type == "application/epub+zip":
        return "epub"
    if (
        filename.endswith(".docx")
        or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return "docx"

    raise UnsupportedFileTypeError(
        f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX."
    )


# Dispatcher function to extract chapters based on document type
async def _extract_chapters_by_type(tmp_filename: str, document_type: str) -> list[dict]:
    with open(tmp_filename, "rb") as f:
        if document_type == "pdf":
            return await extract_pdf_chapters(f)

        if document_type == "epub":
            # TODO: implement extract_epub_chapters(f)
            raise DocumentOutlineRequiredError(
                "EPUB parser chưa được bật hoặc EPUB không có mục lục hợp lệ."
            )

        if document_type == "docx":
            # TODO: implement extract_docx_chapters(f)
            raise DocumentOutlineRequiredError(
                "DOCX parser chưa được bật hoặc DOCX không có heading/mục lục hợp lệ."
            )

    raise UnsupportedFileTypeError()


async def handle_upload_document(session: Session, file: UploadFile) -> dict:
    """
    Bước 1: Validate file, extract outline từ PDF, upload lên Supabase Storage,
    lưu Book + Chapter (DRAFT) vào DB, trả về outline cho Flutter.
    """
    # 1. Validate MIME Type hoặc đuôi file
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()
    document_type = _detect_document_type(file)

    if not is_valid_type:
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise UnsupportedFileTypeError(
                f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX."
            )

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError()

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)

    chapters_data = []
    file_url = ""
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract outline từ PDF
        chapters_data = await _extract_chapters_by_type(tmp_filename, document_type)

        if not chapters_data:
            raise PdfExtractionError()

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.{document_type}"
        content_type = file.content_type or {
            "pdf": "application/pdf",
            "epub": "application/epub+zip",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }[document_type]

        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type=content_type,
        )
        logger.info(
            f"☁️  {document_type.upper()} uploaded to Storage: {storage_path}")

    finally:
        # Dọn rác: Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    # 5. Lưu DB: Book (DRAFT) + Chapters (DRAFT)
    title = (file.filename or "unknown").rsplit(".", 1)[0]
    try:
        book = Book(
            id=book_id,
            user_id=MOCK_USER_ID,
            title=title,
            total_chapters=len(chapters_data),
            status=BookStatus.DRAFT,
            file_url=file_url,
        )
        create_book(session, book)

        for i, chap in enumerate(chapters_data):
            chapter = Chapter(
                book_id=book_id,
                chapter_index=i,
                title=chap.get("title", "Empty Chapter"),
                status=BookStatus.DRAFT,
            )
            create_chapter(session, chapter)

        session.commit()
        logger.info(
            f"📘 Created DRAFT book {book_id} | {len(chapters_data)} chapters | file_url saved")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    # 6. Trả về outline để Flutter hiển thị
    outline = [{"title": c.get("title", f"Chương {i + 1}"), "page_start": c.get(
        "page_start", 0)} for i, c in enumerate(chapters_data)]

    return {
        "book_id": str(book_id),
        "total_chapters": len(chapters_data),
        "outline": outline,
    }


async def handle_generate_plan(session: Session, background_tasks: BackgroundTasks, payload: PlanInput) -> dict:
    """
    Bước 2: Validate trạng thái sách, tạo ReadingPlan, kick-off background processing.
    """
    # 1. Validate book tồn tại và đang ở trạng thái DRAFT
    book = session.get(Book, payload.book_id)
    if not book:
        raise BookNotFoundError()
    if book.status not in (BookStatus.DRAFT,):
        raise BookStatusConflictError(
            f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    # 2. Lưu ReadingPlan + cập nhật Book status
    try:
        plan = ReadingPlan(
            book_id=payload.book_id,
            mode=payload.mode,
            pace=payload.pace,
            schedule_config=payload.schedule_config,
            status=PlanStatus.ACTIVE,
        )
        create_reading_plan(session, plan)
        update_book_status(session, payload.book_id, BookStatus.PROCESSING)

        logger.info(
            f"📋 ReadingPlan created for book {payload.book_id} | mode={payload.mode}")
    except Exception as e:
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    # 3. Kick-off background task — trả 200 OK ngay
    background_tasks.add_task(
        run_background_processing, payload.book_id, payload.mode)

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "mode": payload.mode,
    }
