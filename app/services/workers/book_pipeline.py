"""
Pipeline điều phối xử lý toàn bộ sách ở background.

Trách nhiệm:
    - Fetch book data + draft chapters từ DB
    - Download PDF từ Supabase Storage
    - Re-extract text per-chapter
    - Dispatch chapter tasks song song
    - Cập nhật Book status khi hoàn tất hoặc lỗi

Entry points (được gọi từ FastAPI BackgroundTasks):
    - run_background_processing(): Xử lý sách mới (RAG + TTS)
    - run_switch_mode_processing(): Sinh lại audio khi user đổi mode
"""

import asyncio
import io
import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus
from app.core.exceptions import UnsupportedFileTypeError
from app.core.logger import log as logger
from app.core.supabase import supabase
from app.db.database import engine
from app.models.db_models import Book, Chapter
from app.repositories.audiobook_repo import update_book_status
from app.repositories.chapter_repo import get_draft_chapters_by_book
from app.repositories.processing_job_repo import update_processing_job
from app.services.document_parser_service import extract_chapters_by_document_type, infer_document_type_from_url
from app.services.token_budget_service import TextBudget, estimate_text_budget
from app.services.workers.chapter_worker import process_chapter, process_switch_mode_chapter


@dataclass(frozen=True)
class ChapterWorkItem:
    chapter: Chapter
    raw_text: str
    budget: TextBudget


def _storage_path_for_book(book: Book) -> tuple[str, str]:
    document_type = book.document_type or infer_document_type_from_url(book.file_url)
    storage_path = f"{book.id}/original.{document_type}"

    if book.file_url:
        parsed_path = urlparse(book.file_url).path
        marker = "/raw_books/"
        if marker in parsed_path:
            storage_path = parsed_path.split(marker, 1)[1]

    if not storage_path.endswith(tuple(f".{ext}" for ext in ("pdf", "epub", "docx"))):
        raise UnsupportedFileTypeError("Không xác định được định dạng tài liệu trong Storage.")

    return storage_path, document_type


def _update_job(
    job_id: uuid.UUID | None,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    estimated_input_tokens: int | None = None,
    estimated_audio_seconds: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> None:
    if not job_id:
        return

    with Session(engine) as session:
        update_processing_job(
            session,
            job_id,
            status=status,
            progress_percent=progress_percent,
            current_step=current_step,
            total_units=total_units,
            done_units=done_units,
            failed_units=failed_units,
            estimated_input_tokens=estimated_input_tokens,
            estimated_audio_seconds=estimated_audio_seconds,
            error_message=error_message,
            started_at=started_at,
            finished_at=finished_at,
        )


def _set_book_status(book_id: uuid.UUID, status: BookStatus, error_message: str | None = None) -> None:
    with Session(engine) as session:
        update_book_status(session, book_id, status, error_message)


def _fail_job(job_id: uuid.UUID | None, current_step: str, error_message: str, *, progress_percent: int | None = None, total_units: int | None = None) -> None:
    _update_job(
        job_id,
        status=ProcessingJobStatus.ERROR,
        progress_percent=progress_percent,
        current_step=current_step,
        total_units=total_units,
        error_message=error_message,
        finished_at=datetime.now(timezone.utc),
    )


def _processable_chapters(chapters: list[Chapter], chapters_map: dict[int, str]) -> list[tuple[Chapter, str]]:
    processable: list[tuple[Chapter, str]] = []
    for chapter in chapters:
        raw_text = chapters_map.get(chapter.chapter_index, "")
        if not raw_text.strip():
            logger.warning(f"⚠️ Chapter {chapter.chapter_index + 1} '{chapter.title}' không có text — bỏ qua.")
            continue
        processable.append((chapter, raw_text))
    return processable


def _build_work_items(chapters: list[tuple[Chapter, str]]) -> list[ChapterWorkItem]:
    return [
        ChapterWorkItem(
            chapter=chapter,
            raw_text=raw_text,
            budget=estimate_text_budget(raw_text),
        )
        for chapter, raw_text in chapters
    ]


def _hard_limit_error(work_items: list[ChapterWorkItem]) -> str | None:
    too_large = [item for item in work_items if item.budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT]
    if too_large:
        first = too_large[0]
        return (
            f"Có {len(too_large)} chương vượt giới hạn xử lý. "
            f"Chương đầu tiên vượt giới hạn: '{first.chapter.title}' "
            f"khoảng {first.budget.estimated_tokens} tokens, giới hạn là {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens."
        )

    total_audio_seconds = sum(item.budget.estimated_audio_seconds for item in work_items)
    if total_audio_seconds > settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK:
        return (
            f"Tài liệu dự kiến khoảng {math.ceil(total_audio_seconds / 60)} phút audio, "
            f"vượt giới hạn {math.ceil(settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK / 60)} phút cho mỗi sách."
        )

    return None


def _total_estimates(work_items: list[ChapterWorkItem]) -> tuple[int, int]:
    return (
        sum(item.budget.estimated_tokens for item in work_items),
        sum(item.budget.estimated_audio_seconds for item in work_items),
    )


async def _track_progress(
    tasks: list[asyncio.Task],
    job_id: uuid.UUID | None,
    total_units: int,
    book_id: uuid.UUID,
    step_template: str,
    completed_offset: int = 0,
) -> None:
    completed = completed_offset
    partial_threshold = min(total_units, max(1, settings.FIRST_PLAYABLE_CHAPTERS))

    try:
        for task in asyncio.as_completed(tasks):
            await task
            completed += 1
            progress = int(completed * 100 / total_units)
            is_partial = completed >= partial_threshold and completed < total_units
            job_status = ProcessingJobStatus.PARTIAL_READY if is_partial else ProcessingJobStatus.PROCESSING

            if is_partial:
                _set_book_status(book_id, BookStatus.PARTIAL_READY)

            _update_job(
                job_id,
                status=job_status,
                progress_percent=progress,
                current_step=step_template.format(completed=completed, total=total_units),
                done_units=completed,
            )
    except Exception:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        _update_job(job_id, failed_units=1)
        raise


async def run_background_processing(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None = None) -> None:
    """
    Điều phối xử lý tất cả chapters song song sau khi user upload sách.

    Flow:
        1. Fetch book + draft chapters từ DB
        2. Download PDF từ Supabase Storage (file_url đã lưu lúc /upload)
        3. Re-extract text per-chapter từ PDF
        4. Chạy process_chapter() song song cho tất cả chapters
        5. Cập nhật Book status → READY hoặc ERROR
    """
    mode_value = PlanMode(mode).value
    try:
        # ── 1. Fetch book + draft chapters ───────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            draft_chapters = get_draft_chapters_by_book(session, book_id)

        if not book:
            _fail_job(job_id, "Không tìm thấy sách.", f"Book {book_id} not found")
            logger.error(f"Book {book_id} not found")
            return

        if not draft_chapters:
            _set_book_status(book_id, BookStatus.ERROR, "Không có chapter nào để xử lý.")
            _fail_job(job_id, "Không có chapter nào để xử lý.", "Không có chapter nào để xử lý.")
            return

        if not book.file_url:
            error_message = "file_url chưa được lưu — PDF chưa upload lên Storage."
            _set_book_status(book_id, BookStatus.ERROR, error_message)
            _fail_job(job_id, "Tài liệu chưa được upload lên Storage.", error_message)
            logger.error(f"book.file_url is missing for book {book_id}")
            return

        # ── 2. Download document từ Supabase Storage ─────────────────────────
        storage_path, document_type = _storage_path_for_book(book)
        logger.info(f"⬇️  Downloading {document_type.upper()} from Storage: {storage_path}")
        document_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        document_file = io.BytesIO(document_bytes)

        # ── 3. Re-extract chapters text từ document ──────────────────────────
        chapters_data = await extract_chapters_by_document_type(document_file, document_type)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 4. Dispatch song song — bị giới hạn bởi Semaphore trong chapter_worker ──
        processable_chapters = _processable_chapters(draft_chapters, chapters_map)
        total_units = len(processable_chapters)
        if total_units == 0:
            error_message = "Không có chương nào có nội dung để xử lý."
            _set_book_status(book_id, BookStatus.ERROR, error_message)
            _fail_job(job_id, error_message, error_message, progress_percent=0, total_units=0)
            return

        work_items = _build_work_items(processable_chapters)
        hard_limit_error = _hard_limit_error(work_items)
        estimated_input_tokens, estimated_audio_seconds = _total_estimates(work_items)
        if hard_limit_error:
            _set_book_status(book_id, BookStatus.ERROR, hard_limit_error)
            _fail_job(
                job_id,
                "Tài liệu vượt giới hạn xử lý.",
                hard_limit_error,
                progress_percent=0,
                total_units=total_units,
            )
            return

        _update_job(
            job_id,
            status=ProcessingJobStatus.PROCESSING,
            progress_percent=0,
            current_step="Đã tải, phân tích và ước lượng kích thước tài liệu.",
            total_units=total_units,
            done_units=0,
            estimated_input_tokens=estimated_input_tokens,
            estimated_audio_seconds=estimated_audio_seconds,
            started_at=datetime.now(timezone.utc),
        )

        first_count = min(total_units, max(1, settings.FIRST_PLAYABLE_CHAPTERS))
        completed = 0
        for item in work_items[:first_count]:
            await process_chapter(
                book.user_id,
                book_id,
                book.title,
                item.chapter.title,
                item.chapter.id,
                item.chapter.chapter_index,
                item.raw_text,
                mode_value,
                job_id,
                item.budget.char_count,
                item.budget.estimated_tokens,
                item.budget.estimated_audio_seconds,
            )
            completed += 1
            progress = int(completed * 100 / total_units)
            if completed < total_units:
                _set_book_status(book_id, BookStatus.PARTIAL_READY)
                _update_job(
                    job_id,
                    status=ProcessingJobStatus.PARTIAL_READY,
                    progress_percent=progress,
                    current_step="Đã có nội dung đầu tiên có thể nghe. Phần còn lại đang được xử lý.",
                    done_units=completed,
                )

        remaining_items = work_items[first_count:]
        if remaining_items:
            tasks = [
                asyncio.create_task(
                    process_chapter(
                        book.user_id,
                        book_id,
                        book.title,
                        item.chapter.title,
                        item.chapter.id,
                        item.chapter.chapter_index,
                        item.raw_text,
                        mode_value,
                        job_id,
                        item.budget.char_count,
                        item.budget.estimated_tokens,
                        item.budget.estimated_audio_seconds,
                    )
                )
                for item in remaining_items
            ]
            await _track_progress(tasks, job_id, total_units, book_id, "Đã xử lý {completed}/{total} chương.", completed_offset=completed)

        # ── 5. Cập nhật Book status → READY ──────────────────────────────────
        _set_book_status(book_id, BookStatus.READY)
        _update_job(
            job_id,
            status=ProcessingJobStatus.READY,
            progress_percent=100,
            current_step="Sách đã xử lý xong.",
            done_units=total_units,
            finished_at=datetime.now(timezone.utc),
        )
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        _set_book_status(book_id, BookStatus.ERROR, str(e))
        _fail_job(job_id, "Xử lý sách thất bại.", str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str, job_id: uuid.UUID | None = None) -> None:
    """
    Sinh lại audio cho tất cả chapters khi user chuyển mode học.

    Bỏ qua RAG — knowledge base không thay đổi theo mode.
    Chỉ xóa segments cũ của mode mới và sinh TTS mới.
    """
    new_mode_value = PlanMode(new_mode).value
    try:
        # ── 1. Fetch book + all chapters ─────────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()

        if not book or not book.file_url:
            _fail_job(
                job_id,
                "Không thể switch mode vì thiếu sách hoặc file_url.",
                f"Cannot switch mode for book {book_id}: book missing or no file_url",
            )
            logger.error(f"Cannot switch mode for book {book_id}: book missing or no file_url")
            return

        # ── 2. Download document + extract text ──────────────────────────────
        storage_path, document_type = _storage_path_for_book(book)
        logger.info(f"⬇️  Downloading {document_type.upper()} for switch mode: {storage_path}")
        document_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        document_file = io.BytesIO(document_bytes)
        chapters_data = await extract_chapters_by_document_type(document_file, document_type)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 3. Dispatch song song ─────────────────────────────────────────────
        processable_chapters = _processable_chapters(list(chapters), chapters_map)
        total_units = len(processable_chapters)
        if total_units == 0:
            _set_book_status(book_id, BookStatus.ERROR, "Không có chương nào có nội dung để xử lý.")
            _fail_job(
                job_id,
                f"Không có chương nào có nội dung để sinh audio mode {new_mode}.",
                "Không có chương nào có nội dung để xử lý.",
                progress_percent=0,
                total_units=0,
            )
            return

        work_items = _build_work_items(processable_chapters)
        hard_limit_error = _hard_limit_error(work_items)
        estimated_input_tokens, estimated_audio_seconds = _total_estimates(work_items)
        if hard_limit_error:
            _set_book_status(book_id, BookStatus.ERROR, hard_limit_error)
            _fail_job(
                job_id,
                f"Sinh audio mode {new_mode_value} vượt giới hạn xử lý.",
                hard_limit_error,
                progress_percent=0,
                total_units=total_units,
            )
            return

        _set_book_status(book_id, BookStatus.PROCESSING)
        _update_job(
            job_id,
            status=ProcessingJobStatus.PROCESSING,
            progress_percent=0,
            current_step=f"Đã ước lượng tài liệu, đang sinh audio mode {new_mode_value}.",
            total_units=total_units,
            done_units=0,
            estimated_input_tokens=estimated_input_tokens,
            estimated_audio_seconds=estimated_audio_seconds,
            started_at=datetime.now(timezone.utc),
        )

        first_count = min(total_units, max(1, settings.FIRST_PLAYABLE_CHAPTERS))
        completed = 0
        for item in work_items[:first_count]:
            await process_switch_mode_chapter(
                book.user_id,
                book_id,
                item.chapter.id,
                item.chapter.chapter_index,
                item.raw_text,
                new_mode_value,
                job_id,
                item.budget.char_count,
                item.budget.estimated_tokens,
                item.budget.estimated_audio_seconds,
            )
            completed += 1
            progress = int(completed * 100 / total_units)
            if completed < total_units:
                _set_book_status(book_id, BookStatus.PARTIAL_READY)
                _update_job(
                    job_id,
                    status=ProcessingJobStatus.PARTIAL_READY,
                    progress_percent=progress,
                    current_step=f"Đã có audio đầu tiên cho mode {new_mode_value}. Phần còn lại đang được xử lý.",
                    done_units=completed,
                )

        remaining_items = work_items[first_count:]
        if remaining_items:
            tasks = [
                asyncio.create_task(
                    process_switch_mode_chapter(
                        book.user_id,
                        book_id,
                        item.chapter.id,
                        item.chapter.chapter_index,
                        item.raw_text,
                        new_mode_value,
                        job_id,
                        item.budget.char_count,
                        item.budget.estimated_tokens,
                        item.budget.estimated_audio_seconds,
                    )
                )
                for item in remaining_items
            ]
            await _track_progress(tasks, job_id, total_units, book_id, f"Đã sinh audio mode {new_mode_value} cho {{completed}}/{{total}} chương.", completed_offset=completed)

        _set_book_status(book_id, BookStatus.READY)
        _update_job(
            job_id,
            status=ProcessingJobStatus.READY,
            progress_percent=100,
            current_step=f"Đã sinh xong audio mode {new_mode_value}.",
            done_units=total_units,
            finished_at=datetime.now(timezone.utc),
        )
        logger.info(f"🎉 Book {book_id} đã gen xong audio cho mode: {new_mode_value}.")

    except Exception as e:
        _set_book_status(book_id, BookStatus.ERROR, str(e))
        _fail_job(job_id, f"Sinh audio mode {new_mode_value} thất bại.", str(e))
        logger.error(f"❌ LỖI SWITCH MODE SÁCH {book_id}: {e}")
