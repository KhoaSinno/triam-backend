import json
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select

from app.crud import audiobook as crud_book
from app.crud.audiobook import delete_book_storage
from app.crud.chapter_segment import count_segments_by_book_and_mode
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

    # Lấy Mode đang active của người dùng
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    active_mode = plan.mode if plan else "full"

    chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()

    result = []
    for chap in chapters:
        # Chỉ lấy các segments của mode hiện tại
        segments = session.exec(select(ChapterSegment).where(ChapterSegment.chapter_id == chap.id, ChapterSegment.mode == active_mode).order_by(ChapterSegment.segment_index)).all()

        # Bóc tách JSON để lấy nội dung review của mode hiện tại
        review_text = ""
        if chap.review_text:
            try:
                reviews_text = json.loads(chap.review_text)
                review_text = reviews_text.get(active_mode, "")
            except json.JSONDecodeError:
                review_text = chap.review_text if active_mode == "full" else ""

        review_audio_url = ""
        if chap.review_audio_url:
            try:
                reviews_audio = json.loads(chap.review_audio_url)
                review_audio_url = reviews_audio.get(active_mode, "")
            except json.JSONDecodeError:
                review_audio_url = chap.review_audio_url if active_mode == "full" else ""

        result.append(
            {
                "id": str(chap.id),
                "title": chap.title,
                "status": chap.status,
                "chapter_index": chap.chapter_index,
                "review_text": review_text,
                "review_audio_url": review_audio_url,
                "chapter_segments": [s.model_dump() for s in segments],
            }
        )

    return {"book_status": book.status, "total_chapters": book.total_chapters, "chapters": result}


@router.post("/books/{book_id}/switch-mode")
def switch_book_mode(book_id: uuid.UUID, payload: SwitchModeRequest, background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    if payload.mode not in ("full", "pareto"):
        raise HTTPException(status_code=400, detail="Mode không hợp lệ. Chỉ chấp nhận 'full' hoặc 'pareto'")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 1. Lấy ReadingPlan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Chưa có ReadingPlan cho sách này")

    # 2. Nếu switch sang cùng mode đang active → không cần làm gì thêm
    if plan.mode == payload.mode:
        # Đếm tổng segments trên toàn bộ sách (không chỉ chapter 1)
        total = count_segments_by_book_and_mode(session, book_id, payload.mode)
        if total > 0:
            return {"message": f"Đã ở mode {payload.mode} và audio đã có sẵn ({total} segments).", "needs_generation": False}
        else:
            # Đang ở đúng mode nhưng chưa có segments (do gen thất bại trước)
            background_tasks.add_task(run_switch_mode_processing, book_id, payload.mode)
            return {"message": f"Mode {payload.mode} chưa có audio, đang gen lại.", "needs_generation": True}

    # 3. Cập nhật mode mới vào ReadingPlan
    plan.mode = payload.mode
    session.add(plan)
    session.commit()

    # 4. Kiểm tra xem audio của mode mới đã được sinh ra bao giờ chưa
    # Dùng count toàn sách — tránh trường hợp chương 1 có segment nhưng chương khác không có
    total = count_segments_by_book_and_mode(session, book_id, payload.mode)
    needs_generation = total == 0

    # 5. Kích hoạt Background Task sinh audio nếu cần
    if needs_generation:
        background_tasks.add_task(run_switch_mode_processing, book_id, payload.mode)
        return {"message": f"Đã chuyển sang mode {payload.mode}. Hệ thống đang sinh audio trong background.", "needs_generation": True}

    return {"message": f"Đã chuyển sang mode {payload.mode}. Audio đã có sẵn.", "needs_generation": False}
