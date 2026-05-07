import json
import uuid
from typing import Any

from fastapi import BackgroundTasks
from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.core.exceptions import (
    BookNotFoundError,
    DataIntegrityError,
    NoReadingPlanError,
    ReadingPlanNotFoundError,
)
from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan
from app.repositories.chapter_segment_repo import count_segments_by_book_and_mode
from app.services.workers.book_pipeline import run_switch_mode_processing


def _extract_json_content(raw_data: Any, mode: str) -> str:
    """Helper: Trích xuất nội dung theo mode từ chuỗi JSON."""
    if not raw_data:
        return ""
    try:
        data = json.loads(raw_data)
        return data.get(mode, "")
    except (json.JSONDecodeError, TypeError) as e:
        raise DataIntegrityError() from e


def get_book_details(session: Session, book_id: uuid.UUID) -> dict:
    """
    Lấy chi tiết sách kèm chapters và segments theo active mode.
    Tối ưu N+1 bằng cách query TẤT CẢ segments một lần duy nhất.
    """
    book = session.get(Book, book_id)
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
    chapters = session.exec(
        select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)
    ).all()

    chapter_ids = [c.id for c in chapters]
    all_segments = session.exec(
        select(ChapterSegment)
        .where(ChapterSegment.chapter_id.in_(chapter_ids), ChapterSegment.mode == active_mode)
        .order_by(ChapterSegment.segment_index)
    ).all()

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
    payload_mode: str,
) -> dict:
    """
    Đổi mode active trên ReadingPlan và sinh audio mới nếu mode chưa từng được gen.
    """
    book = session.get(Book, book_id)
    if not book:
        raise BookNotFoundError()

    # 1. Lấy ReadingPlan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise ReadingPlanNotFoundError()

    # 2. Nếu switch sang cùng mode đang active → không cần làm gì thêm
    if plan.mode == payload_mode:
        total = count_segments_by_book_and_mode(session, book_id, payload_mode)
        if total > 0:
            return {
                "message": f"Đã ở mode {payload_mode} và audio đã có sẵn ({total} segments).",
                "needs_generation": False,
            }
        else:
            # Đang ở đúng mode nhưng chưa có segments (do gen thất bại trước)
            background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
            return {"message": f"Mode {payload_mode} chưa có audio, đang gen lại.", "needs_generation": True}

    # 3. Cập nhật mode mới vào ReadingPlan
    plan.mode = payload_mode
    session.add(plan)
    session.commit()

    # 4. Kiểm tra xem audio của mode mới đã được sinh ra bao giờ chưa
    total = count_segments_by_book_and_mode(session, book_id, payload_mode)
    needs_generation = total == 0

    # 5. Kích hoạt Background Task sinh audio nếu cần
    if needs_generation:
        background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
        return {
            "message": f"Đã chuyển sang mode {payload_mode}. Hệ thống đang sinh audio trong background.",
            "needs_generation": True,
        }

    return {"message": f"Đã chuyển sang mode {payload_mode}. Audio đã có sẵn.", "needs_generation": False}
