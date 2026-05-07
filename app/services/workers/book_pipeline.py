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
import logging
import uuid

from sqlmodel import Session, select

from app.core.constant import BookStatus
from app.core.supabase import supabase
from app.db.database import engine
from app.models.db_models import Book, Chapter
from app.repositories.audiobook_repo import update_book_status
from app.repositories.chapter_repo import get_draft_chapters_by_book
from app.services.pdf_service import extract_chapters_smart
from app.services.workers.chapter_worker import process_chapter, process_switch_mode_chapter

logger = logging.getLogger("book_pipeline")


async def run_background_processing(book_id: uuid.UUID, mode: str) -> None:
    """
    Điều phối xử lý tất cả chapters song song sau khi user upload sách.

    Flow:
        1. Fetch book + draft chapters từ DB
        2. Download PDF từ Supabase Storage (file_url đã lưu lúc /upload)
        3. Re-extract text per-chapter từ PDF
        4. Chạy process_chapter() song song cho tất cả chapters
        5. Cập nhật Book status → READY hoặc ERROR
    """
    try:
        # ── 1. Fetch book + draft chapters ───────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            draft_chapters = get_draft_chapters_by_book(session, book_id)

        if not book:
            logger.error(f"Book {book_id} not found")
            return

        if not draft_chapters:
            with Session(engine) as session:
                update_book_status(session, book_id, BookStatus.ERROR, "Không có chapter nào để xử lý.")
            return

        if not book.file_url:
            with Session(engine) as session:
                update_book_status(
                    session, book_id, BookStatus.ERROR,
                    "file_url chưa được lưu — PDF chưa upload lên Storage."
                )
            logger.error(f"book.file_url is missing for book {book_id}")
            return

        # ── 2. Download PDF từ Supabase Storage ──────────────────────────────
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF from Storage: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)

        # ── 3. Re-extract chapters text từ PDF ───────────────────────────────
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 4. Dispatch song song — bị giới hạn bởi Semaphore trong chapter_worker ──
        tasks = []
        for draft_chap in draft_chapters:
            raw_text = chapters_map.get(draft_chap.chapter_index, "")
            if not raw_text.strip():
                logger.warning(
                    f"⚠️ Chapter {draft_chap.chapter_index + 1} '{draft_chap.title}' "
                    f"không có text — bỏ qua."
                )
                continue
            tasks.append(
                process_chapter(book_id, draft_chap.id, draft_chap.chapter_index, raw_text, mode)
            )

        await asyncio.gather(*tasks)

        # ── 5. Cập nhật Book status → READY ──────────────────────────────────
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.READY)
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.ERROR, str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str) -> None:
    """
    Sinh lại audio cho tất cả chapters khi user chuyển mode học.

    Bỏ qua RAG — knowledge base không thay đổi theo mode.
    Chỉ xóa segments cũ của mode mới và sinh TTS mới.
    """
    try:
        # ── 1. Fetch book + all chapters ─────────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id)).all()

        if not book or not book.file_url:
            logger.error(f"Cannot switch mode for book {book_id}: book missing or no file_url")
            return

        # ── 2. Download PDF + extract text ───────────────────────────────────
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF for switch mode: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 3. Dispatch song song ─────────────────────────────────────────────
        tasks = [
            process_switch_mode_chapter(book_id, chap.id, chap.chapter_index, raw_text, new_mode)
            for chap in chapters
            if (raw_text := chapters_map.get(chap.chapter_index, "")) and raw_text.strip()
        ]

        await asyncio.gather(*tasks)
        logger.info(f"🎉 Book {book_id} đã gen xong audio cho mode: {new_mode}.")

    except Exception as e:
        logger.error(f"❌ LỖI SWITCH MODE SÁCH {book_id}: {e}")
