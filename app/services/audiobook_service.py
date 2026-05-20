import json
import uuid
from typing import Any

from fastapi import BackgroundTasks
from sqlmodel import Session, select

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import (
    BookNotFoundError,
    DataIntegrityError,
    NoReadingPlanError,
    ReadingPlanNotFoundError,
)
from app.models.db_models import Book, Chapter, ChapterSegment, ProcessingJob, ReadingPlan
from app.repositories import audiobook_repo
from app.repositories.chapter_segment_repo import count_segments_by_book_and_mode
from app.repositories.processing_job_repo import create_processing_job
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.services.workers.book_pipeline import run_switch_mode_processing


def list_books(session: Session, user_id: uuid.UUID) -> list[Book]:
    return audiobook_repo.get_audiobooks_by_user(session, user_id)


def get_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    return book


def create_new_book(session: Session, user_id: uuid.UUID, payload: BookCreateRequest) -> Book:
    book = Book(
        user_id=user_id,
        title=payload.title,
        author=payload.author,
    )
    return audiobook_repo.create_book(session, book)


def update_book_by_id(session: Session, book_data: BookUpdateRequest, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    return audiobook_repo.update_book_by_id(session, book_data, book_id, user_id)


async def delete_book_and_assets(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> None:
    await audiobook_repo.delete_book_storage(session, book_id, user_id)


def _extract_json_content(raw_data: Any, mode: str) -> str:
    """Helper: Trích xuất nội dung theo mode từ chuỗi JSON."""
    if not raw_data:
        return ""
    try:
        data = json.loads(raw_data)
        return data.get(mode, "")
    except (json.JSONDecodeError, TypeError) as e:
        raise DataIntegrityError() from e


def get_book_details(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """
    Lấy chi tiết sách kèm chapters và segments theo active mode.
    Tối ưu N+1 bằng cách query TẤT CẢ segments một lần duy nhất.
    """
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    # 1. Lấy ReadingPlan và xác định active mode
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise NoReadingPlanError()

    try:
        active_mode = PlanMode(plan.mode)
    except ValueError as e:
        raise DataIntegrityError() from e

    # 2. Query tất cả chapters và segments một lần — tránh N+1
    chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()

    chapter_ids = [c.id for c in chapters]
    all_segments = session.exec(select(ChapterSegment).where(ChapterSegment.chapter_id.in_(chapter_ids), ChapterSegment.mode == active_mode).order_by(ChapterSegment.segment_index)).all()

    # 3. Nhóm segments theo chapter_id để truy xuất O(1)
    segments_map: dict = {}
    for s in all_segments:
        segments_map.setdefault(s.chapter_id, []).append(s.model_dump())

    # 4. Gom kết quả
    result = [
        {
            "id": str(chap.id),
            "title": chap.title,
            "status": chap.status,
            "chapter_index": chap.chapter_index,
            "review_text": _extract_json_content(chap.review_text, active_mode),
            "review_audio_url": _extract_json_content(chap.review_audio_url, active_mode),
            "chapter_segments": segments_map.get(chap.id, []),
        }
        for chap in chapters
    ]

    return {"book_status": book.status, "total_chapters": book.total_chapters, "chapters": result}


def switch_book_mode(
    session: Session,
    background_tasks: BackgroundTasks,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    payload_mode: str,
) -> dict:
    """
    Đổi mode active trên ReadingPlan và sinh audio mới nếu mode chưa từng được gen.
    """
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    requested_mode = PlanMode(payload_mode)
    requested_mode_value = requested_mode.value

    # 1. Lấy ReadingPlan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise ReadingPlanNotFoundError()

    # 2. Nếu switch sang cùng mode đang active → không cần làm gì thêm
    if PlanMode(plan.mode) == requested_mode:
        total = count_segments_by_book_and_mode(session, book_id, requested_mode)
        if total > 0:
            return {
                "message": f"Đã ở mode {requested_mode_value} và audio đã có sẵn ({total} segments).",
                "needs_generation": False,
                "job_id": None,
                "status": None,
                "progress_percent": None,
            }
        else:
            # Đang ở đúng mode nhưng chưa có segments (do gen thất bại trước)
            job = _create_switch_mode_job(session, book, user_id, requested_mode)
            background_tasks.add_task(run_switch_mode_processing, book_id, requested_mode_value, job.id)
            return {
                "message": f"Mode {requested_mode_value} chưa có audio, đang gen lại.",
                "needs_generation": True,
                "job_id": job.id,
                "status": job.status,
                "progress_percent": job.progress_percent,
            }

    # 3. Cập nhật mode mới vào ReadingPlan
    plan.mode = requested_mode
    session.add(plan)
    session.commit()

    # 4. Kiểm tra xem audio của mode mới đã được sinh ra bao giờ chưa
    total = count_segments_by_book_and_mode(session, book_id, requested_mode)
    needs_generation = total == 0

    # 5. Kích hoạt Background Task sinh audio nếu cần
    if needs_generation:
        job = _create_switch_mode_job(session, book, user_id, requested_mode)
        background_tasks.add_task(run_switch_mode_processing, book_id, requested_mode_value, job.id)
        return {
            "message": f"Đã chuyển sang mode {requested_mode_value}. Hệ thống đang sinh audio trong background.",
            "needs_generation": True,
            "job_id": job.id,
            "status": job.status,
            "progress_percent": job.progress_percent,
        }

    return {
        "message": f"Đã chuyển sang mode {requested_mode_value}. Audio đã có sẵn.",
        "needs_generation": False,
        "job_id": None,
        "status": None,
        "progress_percent": None,
    }


def _create_switch_mode_job(session: Session, book: Book, user_id: uuid.UUID, mode: PlanMode) -> ProcessingJob:
    job = ProcessingJob(
        user_id=user_id,
        book_id=book.id,
        job_type=ProcessingJobType.SWITCH_MODE,
        status=ProcessingJobStatus.QUEUED,
        mode=mode,
        total_units=book.total_chapters or 0,
        done_units=0,
        progress_percent=0,
        current_step=f"Đang chờ sinh audio mode {mode.value}.",
    )
    return create_processing_job(session, job)
