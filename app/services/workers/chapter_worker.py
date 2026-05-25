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
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import Book, Chapter
from app.repositories.book_knowledge_repo import delete_knowledge_by_chapter
from app.repositories.chapter_processing_state_repo import get_state_by_chapter_and_mode, mark_chapter_state_error, mark_chapter_state_ready, upsert_chapter_processing_state
from app.repositories.chapter_repo import update_chapter_status
from app.repositories.chapter_segment_repo import check_segments_exist_by_mode, delete_segments_by_chapter_and_mode
from app.services.embed_service import embed_and_save_chapter
from app.services.notification_event_service import create_chapter_ready_learning_events
from app.services.workers.tts_worker import run_tts_pipeline

# Tối đa N chapters xử lý song song — config thấp giúp giảm rate limit LLM/TTS.
sem = asyncio.Semaphore(settings.CHAPTER_PROCESSING_CONCURRENCY)


@dataclass(frozen=True)
class ChapterProcessingResult:
    chapter_id: uuid.UUID
    main_segment_count: int
    skipped: bool = False


def _create_learning_events_safely(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    chapter_id: uuid.UUID,
    chapter_title: str,
    mode: PlanMode,
    review_text: str,
) -> None:
    try:
        create_chapter_ready_learning_events(
            session,
            user_id=user_id,
            book_id=book_id,
            book_title=book_title,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            mode=mode,
            review_text=review_text,
            now=datetime.now(timezone.utc),
        )
    except Exception as exc:
        logger.warning(
            f"Learning event creation failed but chapter remains READY | "
            f"chapter_id={chapter_id} | mode={mode.value} | error={exc}"
        )


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
    async with sem:
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

        try:
            # RAG và TTS chạy song song — mỗi pipeline dùng session riêng
            logger.info(f"Chapter pipelines dispatch | chapter={chapter_index + 1} | mode={mode_value.value} | rag=true | tts=true")
            _, tts_result = await asyncio.gather(
                _run_rag_pipeline(book_id, chapter_id, book_title, chapter_title, raw_text),
                run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode_value.value, chapter_title),
            )
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, BookStatus.READY)
                mark_chapter_state_ready(session, chapter_id, mode_value, main_segment_count=tts_result.main_segment_count)
                _create_learning_events_safely(
                    session,
                    user_id=user_id,
                    book_id=book_id,
                    book_title=book_title,
                    chapter_id=chapter_id,
                    chapter_title=chapter_title,
                    mode=mode_value,
                    review_text=tts_result.review_text,
                )
            logger.info(f"✅ Chapter {chapter_index + 1} READY | mode={mode_value.value} | segments={tts_result.main_segment_count}")
            return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=tts_result.main_segment_count)

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} thất bại: {e}")
            try:
                with Session(engine) as session:
                    delete_knowledge_by_chapter(session, chapter_id)
                    delete_segments_by_chapter_and_mode(session, chapter_id, mode_value)
                    update_chapter_status(session, chapter_id, BookStatus.ERROR)
                    mark_chapter_state_error(session, chapter_id, mode_value, str(e))
                logger.info(f"🧹 Cleaned failed side effects for chapter {chapter_index + 1}.")
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
    async with sem:
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

        try:
            logger.info(f"Switch-mode TTS dispatch | chapter={chapter_index + 1} | mode={mode_value.value}")
            tts_result = await run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode_value.value)
            with Session(engine) as session:
                mark_chapter_state_ready(session, chapter_id, mode_value, main_segment_count=tts_result.main_segment_count)
                book = session.get(Book, book_id)
                chapter = session.get(Chapter, chapter_id)
                _create_learning_events_safely(
                    session,
                    user_id=user_id,
                    book_id=book_id,
                    book_title=book.title if book else "Sách của bạn",
                    chapter_id=chapter_id,
                    chapter_title=chapter.title if chapter else f"Chương {chapter_index + 1}",
                    mode=mode_value,
                    review_text=tts_result.review_text,
                )
            logger.info(f"✅ Chapter {chapter_index + 1} switch mode '{mode_value.value}' READY | segments={tts_result.main_segment_count}")
            return ChapterProcessingResult(chapter_id=chapter_id, main_segment_count=tts_result.main_segment_count)

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} switch mode thất bại: {e}")
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, mode_value)
                mark_chapter_state_error(session, chapter_id, mode_value, str(e))
            raise
