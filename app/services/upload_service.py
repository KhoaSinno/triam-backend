import os
import uuid

import aiofiles
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, DocumentType, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import (
    AppException,
    BookNotFoundError,
    BookStatusConflictError,
    DatabaseError,
    DocumentExtractionError,
    ExternalServiceError,
    FileTooLargeError,
    ReadingPlanScheduleConflictError,
    UnsupportedFileTypeError,
)
from app.core.logger import log as logger
from app.models.db_models import Book, Chapter, ProcessingJob, ReadingPlan
from app.repositories.audiobook_repo import update_book_status
from app.repositories.processing_job_repo import update_processing_job
from app.schemas.plan import PlanInput
from app.services.document_parser_service import extract_chapters_by_document_type
from app.services.reading_plan_schedule_service import build_slots_for_plan, validate_plan_schedule_for_create
from app.services.storage_service import upload_file_to_supabase
from app.tasks.book_tasks import process_book_task

# HELPER FUNCTION: Detect document type based on MIME type or file extension


def _detect_document_type(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if filename.endswith(".pdf") or content_type == "application/pdf":
        return DocumentType.PDF.value
    if filename.endswith(".epub") or content_type == "application/epub+zip":
        return DocumentType.EPUB.value
    if filename.endswith(".docx") or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return DocumentType.DOCX.value

    raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")


# Dispatcher function to extract chapters based on document type
async def _extract_chapters_by_type(tmp_filename: str, document_type: str) -> list[dict]:
    with open(tmp_filename, "rb") as f:
        return await extract_chapters_by_document_type(f, document_type)


async def handle_upload_document(session: Session, file: UploadFile, user_id: uuid.UUID) -> dict:
    """
    Bước 1: Validate file, extract outline từ tài liệu, upload lên Supabase Storage,
    lưu Book + Chapter (DRAFT) vào DB, trả về outline cho Flutter.
    """
    # 1. Validate MIME Type hoặc đuôi file
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()
    document_type = _detect_document_type(file)

    if not is_valid_type:
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")

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
            raise DocumentExtractionError()

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.{document_type}"
        content_type = (
            file.content_type
            or {
                "pdf": "application/pdf",
                "epub": "application/epub+zip",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }[document_type]
        )

        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type=content_type,
        )
        logger.info(f"☁️  {document_type.upper()} uploaded to Storage: {storage_path}")

    finally:
        # Dọn rác: Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    # 5. Lưu DB: Book (DRAFT) + Chapters (DRAFT)
    title = (file.filename or "unknown").rsplit(".", 1)[0]
    try:
        book = Book(
            id=book_id,
            user_id=user_id,
            title=title,
            total_chapters=len(chapters_data),
            status=BookStatus.DRAFT,
            file_url=file_url,
            document_type=document_type,
        )
        chapters = [
            Chapter(
                book_id=book_id,
                chapter_index=i,
                title=chap.get("title", "Empty Chapter"),
                status=BookStatus.DRAFT,
            )
            for i, chap in enumerate(chapters_data)
        ]

        session.add(book)
        session.add_all(chapters)
        session.commit()
        logger.info(f"📘 Created DRAFT book {book_id} | {len(chapters_data)} chapters | file_url saved")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    # 6. Trả về outline để Flutter hiển thị
    outline = [
        {
            "title": c.get("title", f"Chương {i + 1}"),
            "page_start": c.get("page_start"),
        }
        for i, c in enumerate(chapters_data)
    ]

    return {
        "book_id": str(book_id),
        "total_chapters": len(chapters_data),
        "document_type": document_type,
        "outline": outline,
    }


async def handle_generate_plan(session: Session, payload: PlanInput, user_id: uuid.UUID) -> dict:
    """
    Bước 2: Validate trạng thái sách, tạo ReadingPlan, tạo progress job,
    kick-off background processing.
    """
    # 1. Validate book tồn tại và đang ở trạng thái DRAFT
    book = session.exec(select(Book).where(Book.id == payload.book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    if book.status not in (BookStatus.DRAFT,):
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    slots = validate_plan_schedule_for_create(session, user_id=user_id, schedule_config=payload.schedule_config)

    # 2. Lưu ReadingPlan + schedule slots + progress job + cập nhật Book status
    try:
        plan = ReadingPlan(
            book_id=payload.book_id,
            mode=payload.mode,
            pace=payload.pace,
            schedule_config=payload.schedule_config,
            status=PlanStatus.ACTIVE,
        )
        session.add(plan)
        session.flush()

        for slot in build_slots_for_plan(
            user_id=user_id,
            book_id=payload.book_id,
            plan_id=plan.id,
            slots=slots,
        ):
            session.add(slot)

        job = ProcessingJob(
            user_id=user_id,
            book_id=payload.book_id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.QUEUED,
            mode=payload.mode,
            total_units=book.total_chapters or 0,
            done_units=0,
            progress_percent=0,
            current_step="Đang chờ xử lý sách.",
        )
        session.add(job)

        book.status = BookStatus.PROCESSING
        session.add(book)
        session.commit()
        session.refresh(job)

        logger.info(f"📋 ReadingPlan created for book {payload.book_id} | mode={payload.mode.value} | job={job.id}")
    except IntegrityError as e:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from e
    except AppException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    try:
        process_book_task.apply_async(
            args=[str(payload.book_id), payload.mode.value, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step="Không thể đưa sách vào hàng đợi xử lý.",
            error_message=str(e),
        )
        update_book_status(session, payload.book_id, BookStatus.ERROR, "Không thể đưa sách vào hàng đợi xử lý.")
        raise ExternalServiceError("Không thể đưa sách vào hàng đợi xử lý. Vui lòng thử lại sau.") from e

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "job_id": str(job.id),
        "mode": payload.mode.value,
        "status": job.status,
        "progress_percent": job.progress_percent,
    }
