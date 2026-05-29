import asyncio
import uuid
from dataclasses import dataclass

from sqlmodel import Session

from app.core.config import settings
from app.core.constant import ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import LearningUnit
from app.repositories.book_knowledge_repo import delete_knowledge_by_learning_unit
from app.repositories.learning_unit_repo import delete_unit_segments, unit_segments_exist, update_learning_unit_processing
from app.services.async_limiter import get_loop_semaphore
from app.services.embed_service import embed_and_save_learning_unit
from app.services.workers.tts_worker import run_learning_unit_tts_pipeline


@dataclass(frozen=True)
class LearningUnitProcessingResult:
    learning_unit_id: uuid.UUID
    main_segment_count: int
    skipped: bool = False


async def _run_rag_pipeline(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    book_title: str,
    unit_title: str,
    raw_text: str,
) -> None:
    with Session(engine) as session:
        await embed_and_save_learning_unit(book_id, learning_unit_id, book_title, unit_title, raw_text, session)


async def _cancel_pending_tasks(tasks: list[asyncio.Task]) -> None:
    for task in tasks:
        if not task.done():
            task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


def _cleanup_failed_unit(learning_unit_id: uuid.UUID, unit_index: int, error_message: str) -> None:
    with Session(engine) as session:
        unit = session.get(LearningUnit, learning_unit_id)
        delete_knowledge_by_learning_unit(session, learning_unit_id)
        delete_unit_segments(session, learning_unit_id)
        if unit:
            update_learning_unit_processing(session, unit, status=ProcessingJobStatus.ERROR, error_message=error_message)
    logger.info(f"Cleaned failed side effects for learning unit {unit_index + 1}.")


async def process_learning_unit(
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    unit: LearningUnit,
    raw_text: str,
    job_id: uuid.UUID | None = None,
    raw_text_char_count: int = 0,
    estimated_tokens: int = 0,
    estimated_audio_seconds: int = 0,
    *,
    include_rag: bool = True,
) -> LearningUnitProcessingResult:
    async with get_loop_semaphore("learning_unit_processing", settings.CHAPTER_PROCESSING_CONCURRENCY):
        logger.info(
            f"Learning unit processing start | unit={unit.unit_index + 1} | mode={unit.mode.value} | "
            f"title={unit.title} | chars={raw_text_char_count or len(raw_text)} | "
            f"estimated_tokens={estimated_tokens} | estimated_audio_seconds={estimated_audio_seconds} | rag={include_rag}"
        )

        with Session(engine) as session:
            current_unit = session.get(LearningUnit, unit.id)
            if current_unit and current_unit.status == ProcessingJobStatus.READY and unit_segments_exist(session, unit.id):
                logger.info(f"Learning unit {unit.unit_index + 1} already READY, skip.")
                return LearningUnitProcessingResult(
                    learning_unit_id=unit.id,
                    main_segment_count=current_unit.main_segment_count,
                    skipped=True,
                )
            if current_unit:
                update_learning_unit_processing(
                    session,
                    current_unit,
                    status=ProcessingJobStatus.PROCESSING,
                    raw_text_char_count=raw_text_char_count,
                    estimated_tokens=estimated_tokens,
                    estimated_audio_seconds=estimated_audio_seconds,
                )

        pipeline_tasks: list[asyncio.Task] = []
        try:
            pipeline_tasks = [
                asyncio.create_task(
                    run_learning_unit_tts_pipeline(
                        book_id,
                        unit.id,
                        unit.unit_index,
                        raw_text,
                        unit.mode.value,
                        unit.title,
                    )
                )
            ]
            if include_rag:
                pipeline_tasks.append(
                    asyncio.create_task(
                        _run_rag_pipeline(book_id, unit.id, book_title, unit.title, raw_text)
                    )
                )

            tts_result = (await asyncio.gather(*pipeline_tasks))[0]
            with Session(engine) as session:
                current_unit = session.get(LearningUnit, unit.id)
                if current_unit:
                    update_learning_unit_processing(
                        session,
                        current_unit,
                        status=ProcessingJobStatus.READY,
                        main_segment_count=tts_result.main_segment_count,
                    )
            logger.info(f"Learning unit {unit.unit_index + 1} READY | segments={tts_result.main_segment_count}")
            return LearningUnitProcessingResult(unit.id, tts_result.main_segment_count)

        except asyncio.CancelledError:
            logger.warning(f"Learning unit {unit.unit_index + 1} bị hủy vì book job thất bại.")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                _cleanup_failed_unit(unit.id, unit.unit_index, "Learning unit processing cancelled because the book job failed.")
            except Exception as rollback_err:
                logger.error(f"Failed to clean cancelled learning unit {unit.unit_index + 1}: {rollback_err}")
            raise
        except Exception as exc:
            logger.error(f"Learning unit {unit.unit_index + 1} thất bại: {exc}")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                _cleanup_failed_unit(unit.id, unit.unit_index, str(exc))
            except Exception as rollback_err:
                logger.error(f"Failed to clean failed learning unit {unit.unit_index + 1}: {rollback_err}")
            raise

