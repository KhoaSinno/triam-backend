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
from dataclasses import dataclass

from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.repositories.book_knowledge_repo import delete_knowledge_by_chapter
from app.repositories.chapter_processing_state_repo import get_state_by_chapter_and_mode, mark_chapter_state_error, mark_chapter_state_ready, upsert_chapter_processing_state
from app.repositories.chapter_repo import update_chapter_status
from app.repositories.chapter_segment_repo import check_segments_exist_by_mode, delete_segments_by_chapter_and_mode
from app.services.async_limiter import get_loop_semaphore
from app.services.embed_service import embed_and_save_chapter
from app.services.workers.tts_worker import run_tts_pipeline


@dataclass(frozen=True)
class ChapterProcessingResult:
    chapter_id: uuid.UUID
    main_segment_count: int
    skipped: bool = False


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


async def _cancel_pending_tasks(tasks: list[asyncio.Task]) -> None:
    for task in tasks:
        if not task.done():
            task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


def _cleanup_failed_chapter(chapter_id: uuid.UUID, chapter_index: int, mode: PlanMode, error_message: str) -> None:
    with Session(engine) as session:
        delete_knowledge_by_chapter(session, chapter_id)
        delete_segments_by_chapter_and_mode(session, chapter_id, mode)
        update_chapter_status(session, chapter_id, BookStatus.ERROR)
        mark_chapter_state_error(session, chapter_id, mode, error_message)
    logger.info(f"🧹 Cleaned failed side effects for chapter {chapter_index + 1}.")


def _cleanup_failed_switch_mode_chapter(chapter_id: uuid.UUID, chapter_index: int, mode: PlanMode, error_message: str) -> None:
    with Session(engine) as session:
        delete_segments_by_chapter_and_mode(session, chapter_id, mode)
        mark_chapter_state_error(session, chapter_id, mode, error_message)
    logger.info(f"🧹 Cleaned failed switch-mode side effects for chapter {chapter_index + 1}.")


async def process_chapter(
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    chapter_title: str,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
    job_id: uuid.UUID | None = None,
    raw_text_char_count: int = 0,
    estimated_tokens: int = 0,
    estimated_audio_seconds: int = 0,
) -> ChapterProcessingResult:
    """
    Xử lý đầy đủ 1 chapter: chạy RAG + TTS song song, cập nhật status.

    Nếu thất bại: rollback book_knowledge + xóa chapter để đảm bảo
    không còn dữ liệu không nhất quán.
    """
    async with get_loop_semaphore("chapter_processing", settings.CHAPTER_PROCESSING_CONCURRENCY):
        mode_value = PlanMode(mode)
        logger.info(
            f"Chapter processing start | chapter={chapter_index + 1} | mode={mode_value.value} | "
            f"title={chapter_title} | chars={raw_text_char_count or len(raw_text)} | "
            f"estimated_tokens={estimated_tokens} | estimated_audio_seconds={estimated_audio_seconds}"
        )
        with Session(engine) as session:
            existing_state = get_state_by_chapter_and_mode(session, chapter_id, mode_value)
            if existing_state and existing_state.status == ProcessingJobStatus.READY and check_segments_exist_by_mode(session, chapter_id, mode_value):
                logger.info(f"↩️ Chapter {chapter_index + 1} mode '{mode_value.value}' already READY, skip.")
                return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=existing_state.main_segment_count, skipped=True)

        with Session(engine) as session:
            upsert_chapter_processing_state(
                session,
                user_id=user_id,
                book_id=book_id,
                chapter_id=chapter_id,
                job_id=job_id,
                mode=mode_value,
                status=ProcessingJobStatus.PROCESSING,
                raw_text_char_count=raw_text_char_count,
                estimated_tokens=estimated_tokens,
                estimated_audio_seconds=estimated_audio_seconds,
            )

        pipeline_tasks: list[asyncio.Task] = []
        try:
            # RAG và TTS chạy song song — mỗi pipeline dùng session riêng
            logger.info(f"Chapter pipelines dispatch | chapter={chapter_index + 1} | mode={mode_value.value} | rag=true | tts=true")
            pipeline_tasks = [
                asyncio.create_task(_run_rag_pipeline(book_id, chapter_id, book_title, chapter_title, raw_text)),
                asyncio.create_task(run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode_value.value, chapter_title)),
            ]
            _, tts_result = await asyncio.gather(*pipeline_tasks)
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, BookStatus.READY)
                mark_chapter_state_ready(session, chapter_id, mode_value, main_segment_count=tts_result.main_segment_count)
            logger.info(f"✅ Chapter {chapter_index + 1} READY | mode={mode_value.value} | segments={tts_result.main_segment_count}")
            return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=tts_result.main_segment_count)

        except asyncio.CancelledError:
            logger.warning(f"Chapter {chapter_index + 1} bị hủy vì book job đã thất bại ở chapter khác.")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                _cleanup_failed_chapter(chapter_id, chapter_index, mode_value, "Chapter processing cancelled because the book job failed.")
            except Exception as rollback_err:
                logger.error(f"Failed to clean cancelled chapter {chapter_index + 1}: {rollback_err}")
            raise
        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} thất bại: {e}")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                _cleanup_failed_chapter(chapter_id, chapter_index, mode_value, str(e))
            except Exception as rollback_err:
                logger.error(f"Failed to clean failed chapter {chapter_index + 1}: {rollback_err}")
            raise


async def process_switch_mode_chapter(
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
    job_id: uuid.UUID | None = None,
    raw_text_char_count: int = 0,
    estimated_tokens: int = 0,
    estimated_audio_seconds: int = 0,
) -> ChapterProcessingResult:
    """
    Switch mode 1 chapter: xóa segments cũ → chạy TTS mới (bỏ qua RAG).

    Không cần RAG vì knowledge base không thay đổi theo mode.
    """
    async with get_loop_semaphore("chapter_processing", settings.CHAPTER_PROCESSING_CONCURRENCY):
        mode_value = PlanMode(new_mode)
        logger.info(
            f"Switch-mode chapter start | chapter={chapter_index + 1} | mode={mode_value.value} | "
            f"chars={raw_text_char_count or len(raw_text)} | estimated_tokens={estimated_tokens} | "
            f"estimated_audio_seconds={estimated_audio_seconds}"
        )
        with Session(engine) as session:
            existing_state = get_state_by_chapter_and_mode(session, chapter_id, mode_value)
            if existing_state and existing_state.status == ProcessingJobStatus.READY and check_segments_exist_by_mode(session, chapter_id, mode_value):
                logger.info(f"↩️ Chapter {chapter_index + 1} switch mode '{mode_value.value}' already has segments, skip.")
                return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=existing_state.main_segment_count, skipped=True)

            upsert_chapter_processing_state(
                session,
                user_id=user_id,
                book_id=book_id,
                chapter_id=chapter_id,
                job_id=job_id,
                mode=mode_value,
                status=ProcessingJobStatus.PROCESSING,
                raw_text_char_count=raw_text_char_count,
                estimated_tokens=estimated_tokens,
                estimated_audio_seconds=estimated_audio_seconds,
            )

        tts_task: asyncio.Task | None = None
        try:
            logger.info(f"Switch-mode TTS dispatch | chapter={chapter_index + 1} | mode={mode_value.value}")
            tts_task = asyncio.create_task(run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode_value.value))
            tts_result = await tts_task
            with Session(engine) as session:
                mark_chapter_state_ready(session, chapter_id, mode_value, main_segment_count=tts_result.main_segment_count)
            logger.info(f"✅ Chapter {chapter_index + 1} switch mode '{mode_value.value}' READY | segments={tts_result.main_segment_count}")
            return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=tts_result.main_segment_count)

        except asyncio.CancelledError:
            logger.warning(f"Chapter {chapter_index + 1} switch mode bị hủy vì book job đã thất bại ở chapter khác.")
            await _cancel_pending_tasks([tts_task] if tts_task else [])
            _cleanup_failed_switch_mode_chapter(chapter_id, chapter_index, mode_value, "Switch-mode chapter processing cancelled because the book job failed.")
            raise
        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} switch mode thất bại: {e}")
            await _cancel_pending_tasks([tts_task] if tts_task else [])
            _cleanup_failed_switch_mode_chapter(chapter_id, chapter_index, mode_value, str(e))
            raise
