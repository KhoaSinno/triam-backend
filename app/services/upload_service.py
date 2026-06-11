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
from app.models.db_models import Book, ProcessingJob, ReadingPlan
from app.repositories.audiobook_repo import update_book_status
from app.repositories.book_section_repo import create_book_sections, list_book_sections
from app.repositories.learning_unit_repo import create_learning_units
from app.repositories.processing_job_repo import update_processing_job
from app.repositories.reading_plan_schedule_repo import list_slots_for_plan
from app.schemas.plan import PlanInput
from app.services.document_parser_service import parse_document_structure
from app.services.document_structure_service import build_outline_preview, detect_structure_warnings, validate_document_structure
from app.services.document_structure_types import flatten_sections
from app.services.learning_unit_planner_service import plan_learning_units_async
from app.services.reading_plan_schedule_service import WEEKDAY_LABELS, build_slots_for_plan, validate_plan_schedule_for_activation, validate_plan_schedule_shape
from app.services.reading_plan_session_service import build_plan_session_summary, ensure_future_sessions_for_plan
from app.services.storage_service import upload_file_to_supabase
from app.tasks.book_tasks import index_book_sections_task, process_book_task

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


async def _planned_units_for_book(session: Session, book_id: uuid.UUID, mode) -> list:
    sections = list_book_sections(session, book_id)
    if not sections:
        return []

    planned_units = await plan_learning_units_async(sections, mode)
    if not planned_units:
        raise DocumentExtractionError("Không tạo được bài học từ cấu trúc tài liệu.")
    return planned_units


def _enqueue_section_indexing(book_id: uuid.UUID) -> None:
    if not settings.BOOK_SECTION_INDEXING_ENABLED:
        return
    try:
        index_book_sections_task.apply_async(args=[str(book_id)], queue="document")
    except Exception as exc:
        logger.warning(f"BookSectionKnowledge indexing enqueue failed | book_id={book_id} | reason={type(exc).__name__}")


def _slot_response(slot) -> dict:
    return {
        "id": str(slot.id),
        "weekday": slot.weekday,
        "weekday_label": WEEKDAY_LABELS.get(slot.weekday, str(slot.weekday)),
        "reminder_time": slot.reminder_time,
        "timezone": slot.timezone,
        "is_active": slot.is_active,
    }


async def _create_plan_and_job_async(
    session: Session,
    *,
    book: Book,
    payload: PlanInput,
    user_id: uuid.UUID,
    slots: list,
    resolved_reminder_time: str,
    plan_status: PlanStatus,
) -> tuple[ProcessingJob, list, ReadingPlan]:
    planned_units = await _planned_units_for_book(session, payload.book_id, payload.mode)

    plan = ReadingPlan(
        book_id=payload.book_id,
        mode=payload.mode,
        pace=payload.pace,
        schedule_config=payload.schedule_config,
        status=plan_status.value,
        reminder_time=resolved_reminder_time,
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

    if planned_units:
        created_units = create_learning_units(
            session,
            user_id=user_id,
            book_id=payload.book_id,
            mode=payload.mode,
            planned_units=planned_units,
        )
        book.total_units = len(created_units)

    if plan.status == PlanStatus.ACTIVE.value:
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)

    job = ProcessingJob(
        user_id=user_id,
        book_id=payload.book_id,
        job_type=ProcessingJobType.GENERATE_PLAN,
        status=ProcessingJobStatus.QUEUED,
        mode=payload.mode,
        total_units=len(planned_units) if planned_units else book.total_units or 0,
        done_units=0,
        progress_percent=0,
        current_step="Đang chờ xử lý sách.",
    )
    session.add(job)
    book.status = BookStatus.PROCESSING
    session.add(book)
    return job, planned_units, plan


# Dispatcher function to extract document structure based on document type
async def _extract_structure_by_type(tmp_filename: str, document_type: str):
    with open(tmp_filename, "rb") as f:
        return await parse_document_structure(f, document_type)


async def handle_upload_document(session: Session, file: UploadFile, user_id: uuid.UUID) -> dict:
    """
    Bước 1: Validate file, extract outline từ tài liệu, upload lên Supabase Storage,
    lưu Book + BookSection vào DB, trả về outline tree cho Flutter.
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

    parsed_document = None
    file_url = ""
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract deterministic outline tree từ tài liệu
        parsed_document = await _extract_structure_by_type(tmp_filename, document_type)
        validate_document_structure(parsed_document)
        flat_sections = flatten_sections(parsed_document.sections)
        if not flat_sections:
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

    if not parsed_document:
        raise DocumentExtractionError()

    flat_sections = flatten_sections(parsed_document.sections)
    warnings = detect_structure_warnings(parsed_document)

    # 5. Lưu DB: Book (DRAFT) + BookSection tree
    title = (file.filename or "unknown").rsplit(".", 1)[0]
    try:
        book = Book(
            id=book_id,
            user_id=user_id,
            title=title,
            total_sections=len(flat_sections),
            total_units=0,
            status=BookStatus.DRAFT,
            file_url=file_url,
            document_type=document_type,
        )

        session.add(book)
        session.flush()
        create_book_sections(session, book_id, parsed_document)
        session.commit()
        logger.info(f"📘 Created DRAFT book {book_id} | {len(flat_sections)} sections | file_url saved")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    _enqueue_section_indexing(book_id)

    outline_tree = build_outline_preview(parsed_document)
    return {
        "book_id": str(book_id),
        "total_sections": len(flat_sections),
        "max_depth": parsed_document.max_depth,
        "outline_tree": outline_tree,
        "warnings": warnings,
        "document_type": document_type,
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

    if payload.activate:
        slots = validate_plan_schedule_for_activation(
            session,
            user_id=user_id,
            schedule_config=payload.schedule_config,
            reminder_time=payload.reminder_time,
        )
        plan_status = PlanStatus.ACTIVE
        slots_to_create = slots
    else:
        slots = validate_plan_schedule_shape(
            session,
            user_id=user_id,
            schedule_config=payload.schedule_config,
            reminder_time=payload.reminder_time,
        )
        plan_status = PlanStatus.INACTIVE
        slots_to_create = []
    resolved_reminder_time = slots[0].reminder_time

    # 2. Lưu ReadingPlan + schedule slots + learning units + progress job
    try:
        job, planned_units, plan = await _create_plan_and_job_async(
            session,
            book=book,
            payload=payload,
            user_id=user_id,
            slots=slots_to_create,
            resolved_reminder_time=resolved_reminder_time,
            plan_status=plan_status,
        )
        session.commit()
        session.refresh(job)
        session.refresh(plan)

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
        "plan_id": str(plan.id),
        "job_id": str(job.id),
        "mode": payload.mode.value,
        "plan_status": plan.status,
        "pace": plan.pace,
        "schedule_config": list(plan.schedule_config or []),
        "reminder_time": plan.reminder_time,
        "status": job.status,
        "progress_percent": job.progress_percent,
        "active_slots": [_slot_response(slot) for slot in list_slots_for_plan(session, plan_id=plan.id, active_only=True)] if plan.status == PlanStatus.ACTIVE.value else [],
        "session_summary": build_plan_session_summary(session, plan_id=plan.id),
        "planned_units": [
            {
                "unit_index": index,
                "title": unit.title,
                "unit_type": unit.unit_type,
                "source_section_count": len(unit.source_section_ids),
                "estimated_audio_seconds": unit.estimated_audio_seconds,
            }
            for index, unit in enumerate(planned_units)
        ],
    }
