import json
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.db.database import get_session
from app.helper.run_background_processing import run_switch_mode_processing
from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan
from app.repositories import audiobook_repo
from app.repositories.chapter_segment_repo import count_segments_by_book_and_mode
from app.schemas.plan import SwitchModeRequest

router = APIRouter()


@router.get("/books", response_model=list[Book])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.get_audiobooks(session)


@router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.get_book_by_id(session, book_id)


@router.post("/books", response_model=Book)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.create_book(session, book)


@router.delete("/book/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await audiobook_repo.delete_book_storage(session, book_id)
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
