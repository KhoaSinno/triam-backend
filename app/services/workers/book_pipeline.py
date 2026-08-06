import asyncio
import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import Book, LearningUnit, ProcessingJob
from app.repositories.audiobook_repo import update_book_status
from app.repositories.learning_unit_repo import get_learning_unit_source_text_map, list_learning_units
from app.repositories.processing_job_repo import update_processing_job
from app.services.notification_event_service import create_book_ready_outbox_once, create_first_playable_ready_outbox_once
from app.services.token_budget_service import TextBudget, estimate_text_budget
from app.services.workers.learning_unit_worker import process_learning_unit


@dataclass(frozen=True)
class UnitWorkItem:
    unit: LearningUnit
    raw_text: str
    budget: TextBudget


@dataclass(frozen=True)
class BookProcessingInput:
    book: Book
    units: list[LearningUnit]
    source_text_by_unit: dict[uuid.UUID, str]


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


def _set_book_status(book_id: uuid.UUID, status: BookStatus, *, current_job_id: uuid.UUID | None = None, error_message: str | None = None) -> None:
    with Session(engine) as session:
        # Nếu worker muốn đặt trạng thái READY cho sách
        if status == BookStatus.READY:
            # Kiểm tra xem còn tiến trình (Job) xử lý nào khác cho sách đang chạy không (loại trừ job hiện tại)
            query = select(ProcessingJob).where(ProcessingJob.book_id == book_id, ProcessingJob.status.in_([ProcessingJobStatus.QUEUED, ProcessingJobStatus.PROCESSING]))
            if current_job_id:
                query = query.where(ProcessingJob.id != current_job_id)

            active_jobs = session.exec(query).all()

            # Nếu còn ít nhất 1 job khác đang chạy (ví dụ chế độ còn lại đang gen)
            if active_jobs:
                logger.info(f"Sách {book_id} vẫn còn {len(active_jobs)} job khác đang xử lý. Giữ trạng thái ở mức PARTIAL_READY.")
                update_book_status(session, book_id, BookStatus.PARTIAL_READY, error_message)
                return

        # Thiết lập bình thường nếu không vướng job chạy song song
        update_book_status(session, book_id, status, error_message)


def _fail_job(
    job_id: uuid.UUID | None,
    current_step: str,
    error_message: str,
    *,
    progress_percent: int | None = None,
    total_units: int | None = None,
) -> None:
    _update_job(
        job_id,
        status=ProcessingJobStatus.ERROR,
        progress_percent=progress_percent,
        current_step=current_step,
        total_units=total_units,
        error_message=error_message,
        finished_at=datetime.now(timezone.utc),
    )


def _job_is_ready(job_id: uuid.UUID | None) -> bool:
    if not job_id:
        return False
    with Session(engine) as session:
        job = session.get(ProcessingJob, job_id)
        return bool(job and job.status == ProcessingJobStatus.READY)


def _load_book_processing_input(book_id: uuid.UUID, mode: PlanMode, job_id: uuid.UUID | None) -> BookProcessingInput | None:
    with Session(engine) as session:
        book = session.get(Book, book_id)
        units = list_learning_units(session, book_id, mode)
        source_text_by_unit = get_learning_unit_source_text_map(session, book_id, mode)

    if not book:
        _fail_job(job_id, "Không tìm thấy sách.", f"Book {book_id} not found")
        logger.error(f"Book {book_id} not found")
        return None

    if not units:
        message = "Sách chưa có bài học nào để xử lý. Hãy tạo kế hoạch học trước."
        _set_book_status(book_id, BookStatus.ERROR, message)
        _fail_job(job_id, message, message, progress_percent=0, total_units=0)
        return None

    if not source_text_by_unit:
        message = "Không tìm thấy nội dung nguồn của các bài học."
        _set_book_status(book_id, BookStatus.ERROR, message)
        _fail_job(job_id, message, message, progress_percent=0, total_units=len(units))
        return None

    return BookProcessingInput(book=book, units=list(units), source_text_by_unit=source_text_by_unit)


def _create_first_playable_notification_safely(book: Book, mode: str) -> None:
    try:
        with Session(engine) as session:
            created = create_first_playable_ready_outbox_once(
                session,
                user_id=book.user_id,
                book_id=book.id,
                book_title=book.title,
                mode=mode,
                now=datetime.now(timezone.utc),
            )
            logger.info(f"Content-ready first-playable event | book_id={book.id} | mode={mode} | created={bool(created)}")
    except Exception as exc:
        logger.warning(f"Content-ready first-playable event failed | book_id={book.id} | mode={mode} | error={exc}")


def _create_book_ready_notification_safely(book_id: uuid.UUID, mode: str) -> None:
    try:
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                return
            created = create_book_ready_outbox_once(
                session,
                user_id=book.user_id,
                book_id=book.id,
                book_title=book.title,
                mode=mode,
                now=datetime.now(timezone.utc),
            )
            logger.info(f"Content-ready book-ready event | book_id={book.id} | mode={mode} | created={bool(created)}")
    except Exception as exc:
        logger.warning(f"Content-ready book-ready event failed | book_id={book_id} | mode={mode} | error={exc}")


def _build_work_items(units: list[LearningUnit], source_text_by_unit: dict[uuid.UUID, str]) -> list[UnitWorkItem]:
    work_items: list[UnitWorkItem] = []
    for unit in units:
        raw_text = source_text_by_unit.get(unit.id, "")
        if not raw_text.strip():
            logger.warning(f"Learning unit {unit.unit_index + 1} '{unit.title}' không có text, bỏ qua.")
            continue
        budget = estimate_text_budget(raw_text, mode=unit.mode)
        work_items.append(UnitWorkItem(unit=unit, raw_text=raw_text, budget=budget))
    return work_items


def _hard_limit_error(work_items: list[UnitWorkItem]) -> str | None:
    too_large = [item for item in work_items if item.budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT]
    if too_large:
        first = too_large[0]
        return (
            f"Có {len(too_large)} bài học vượt giới hạn xử lý. "
            f"Bài đầu tiên vượt giới hạn: '{first.unit.title}' khoảng {first.budget.estimated_tokens} tokens, "
            f"giới hạn là {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens."
        )

    total_audio_seconds = sum(item.budget.estimated_audio_seconds for item in work_items)
    if total_audio_seconds > settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK:
        return f"Tài liệu dự kiến khoảng {math.ceil(total_audio_seconds / 60)} phút audio, vượt giới hạn {math.ceil(settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK / 60)} phút cho mỗi sách."

    return None


def _total_estimates(work_items: list[UnitWorkItem]) -> tuple[int, int]:
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
    partial_threshold = min(total_units, max(1, settings.FIRST_PLAYABLE_UNITS))

    try:
        for task in asyncio.as_completed(tasks):
            await task
            completed += 1
            progress = int(completed * 100 / total_units)
            is_partial = completed >= partial_threshold and completed < total_units
            job_status = ProcessingJobStatus.PARTIAL_READY if is_partial else ProcessingJobStatus.PROCESSING

            if is_partial:
                await asyncio.to_thread(_set_book_status, book_id, BookStatus.PARTIAL_READY)

            await asyncio.to_thread(
                _update_job,
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
        await asyncio.to_thread(_update_job, job_id, done_units=completed, failed_units=max(1, total_units - completed))
        raise


async def _run_unit_pipeline(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None) -> None:
    if await asyncio.to_thread(_job_is_ready, job_id):
        logger.info(f"Skip book processing because job is already READY | book_id={book_id} | job_id={job_id}")
        return

    mode_value = PlanMode(mode)
    processing_input = await asyncio.to_thread(_load_book_processing_input, book_id, mode_value, job_id)
    if not processing_input:
        return

    book = processing_input.book
    work_items = _build_work_items(processing_input.units, processing_input.source_text_by_unit)
    total_units = len(work_items)
    if total_units == 0:
        error_message = "Không có bài học nào có nội dung để xử lý."
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=error_message)
        await asyncio.to_thread(_fail_job, job_id, error_message, error_message, progress_percent=0, total_units=0)
        return

    hard_limit_error = _hard_limit_error(work_items)
    estimated_input_tokens, estimated_audio_seconds = _total_estimates(work_items)
    if hard_limit_error:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=hard_limit_error)
        await asyncio.to_thread(_fail_job, job_id, "Tài liệu vượt giới hạn xử lý.", hard_limit_error, progress_percent=0, total_units=total_units)
        return

    await asyncio.to_thread(
        _update_job,
        job_id,
        status=ProcessingJobStatus.PROCESSING,
        progress_percent=0,
        current_step="Đã tạo các bài học, đang xử lý audio.",
        total_units=total_units,
        done_units=0,
        estimated_input_tokens=estimated_input_tokens,
        estimated_audio_seconds=estimated_audio_seconds,
        started_at=datetime.now(timezone.utc),
    )

    # Priority Processing Unit firstable to listing immediately user
    first_count = min(total_units, max(1, settings.FIRST_PLAYABLE_UNITS))
    completed = 0
    for item in work_items[:first_count]:
        await process_learning_unit(
            book.user_id,
            book_id,
            book.title,
            item.unit,
            item.raw_text,
            job_id,
            item.budget.char_count,
            item.budget.estimated_tokens,
            item.budget.estimated_audio_seconds,
        )
        completed += 1
        progress = int(completed * 100 / total_units)
        if completed < total_units:
            await asyncio.to_thread(_set_book_status, book_id=book_id, status=BookStatus.PARTIAL_READY, current_job_id=job_id)
            await asyncio.to_thread(
                _update_job,
                job_id,
                status=ProcessingJobStatus.PARTIAL_READY,
                progress_percent=progress,
                current_step="Đã có bài học đầu tiên có thể nghe. Phần còn lại đang được xử lý.",
                done_units=completed,
            )
    _create_first_playable_notification_safely(book, mode_value.value)

    # Processing remaining units except first unit
    remaining_items = work_items[first_count:]
    if remaining_items:
        tasks = [
            asyncio.create_task(
                process_learning_unit(
                    book.user_id,
                    book_id,
                    book.title,
                    item.unit,
                    item.raw_text,
                    job_id,
                    item.budget.char_count,
                    item.budget.estimated_tokens,
                    item.budget.estimated_audio_seconds,
                )
            )
            for item in remaining_items
        ]
        await _track_progress(tasks, job_id, total_units, book_id, "Đã xử lý {completed}/{total} bài học.", completed_offset=completed)

    await asyncio.to_thread(_set_book_status, book_id=book_id, status=BookStatus.READY, current_job_id=job_id)
    _create_book_ready_notification_safely(book_id, mode_value.value)
    await asyncio.to_thread(
        _update_job,
        job_id,
        status=ProcessingJobStatus.READY,
        progress_percent=100,
        current_step="Sách đã xử lý xong.",
        done_units=total_units,
        finished_at=datetime.now(timezone.utc),
    )
    logger.info(f"Book {book_id} READY | processed_units={total_units} | mode={mode_value.value}")


async def run_background_processing(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None = None) -> None:
    try:
        await _run_unit_pipeline(book_id, mode, job_id)
    except Exception as exc:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=str(exc))
        await asyncio.to_thread(_fail_job, job_id, "Xử lý sách thất bại.", str(exc))
        logger.error(f"LỖI XỬ LÝ SÁCH {book_id}: {exc}")


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str, job_id: uuid.UUID | None = None) -> None:
    try:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.PROCESSING)
        await _run_unit_pipeline(book_id, new_mode, job_id)
    except Exception as exc:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=str(exc))
        await asyncio.to_thread(_fail_job, job_id, f"Sinh audio mode {new_mode} thất bại.", str(exc))
        logger.error(f"LỖI SWITCH MODE SÁCH {book_id}: {exc}")
