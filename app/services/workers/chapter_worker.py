"""
Worker xử lý 1 chapter trong pipeline background.

Trách nhiệm:
    - Điều phối 2 pipeline song song: RAG (embed) + TTS
    - Giới hạn concurrency qua Semaphore (tránh quá tải DB + external API)
    - Xử lý rollback gọn gàng khi chapter thất bại
    - Xử lý switch-mode (chỉ TTS, không RAG)

Concurrency model:
    sem = Semaphore(5) → tối đa 5 chapters xử lý song song cùng lúc.
    Mỗi chapter trong normal path sử dụng tối đa 3 DB sessions:
        - RAG pipeline: 1 session
        - TTS pipeline: 1 session (gom từ 3 sessions cũ)
        - Chapter status update: 1 session
    → 5 chapters × 3 sessions = 15 connections tối đa (pool_size=10 + overflow=20 → an toàn)
"""

import asyncio
import uuid

from sqlmodel import Session

from app.core.constant import BookStatus
from app.db.database import engine
from app.repositories.book_knowledge_repo import delete_knowledge_by_chapter
from app.repositories.chapter_repo import delete_chapter, update_chapter_status
from app.repositories.chapter_segment_repo import delete_segments_by_chapter_and_mode
from app.services.embed_service import embed_and_save_chapter
from app.services.workers.tts_worker import run_tts_pipeline

from app.core.logger import log as logger

# Tối đa 5 chapters xử lý song song — cân bằng giữa tốc độ và tải hệ thống
sem = asyncio.Semaphore(5)


async def _run_rag_pipeline(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    book_title: str,
    chapter_title: str,
    raw_text: str,
) -> None:
    """Pipeline RAG: cắt chunks → embed → lưu book_knowledge (1 session)."""
    with Session(engine) as session:
        await embed_and_save_chapter(book_id, chapter_id, book_title, chapter_title, raw_text, session)


async def process_chapter(
    book_id: uuid.UUID,
    book_title: str,
    chapter_title: str,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """
    Xử lý đầy đủ 1 chapter: chạy RAG + TTS song song, cập nhật status.

    Nếu thất bại: rollback book_knowledge + xóa chapter để đảm bảo
    không còn dữ liệu không nhất quán.
    """
    async with sem:
        try:
            # RAG và TTS chạy song song — mỗi pipeline dùng session riêng
            await asyncio.gather(
                _run_rag_pipeline(book_id, chapter_id, book_title, chapter_title, raw_text),
                run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode),
            )
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, BookStatus.READY)
            logger.info(f"✅ Chapter {chapter_index + 1} READY")

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} thất bại: {e}")
            # Rollback: xóa book_knowledge TRƯỚC (FK constraint) rồi mới xóa chapter
            try:
                with Session(engine) as session:
                    delete_knowledge_by_chapter(session, chapter_id)
                    delete_chapter(session, chapter_id)
                logger.info(f"🗑️ Rollback chapter {chapter_index + 1} thành công.")
            except Exception as rollback_err:
                logger.error(f"Failed to rollback chapter {chapter_index + 1}: {rollback_err}")
            raise


async def process_switch_mode_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
) -> None:
    """
    Switch mode 1 chapter: xóa segments cũ → chạy TTS mới (bỏ qua RAG).

    Không cần RAG vì knowledge base không thay đổi theo mode.
    """
    async with sem:
        try:
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, new_mode)

            await run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, new_mode)
            logger.info(f"✅ Chapter {chapter_index + 1} switch mode '{new_mode}' READY")

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} switch mode thất bại: {e}")
            raise
