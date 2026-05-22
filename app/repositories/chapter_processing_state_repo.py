import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import PlanMode, ProcessingJobStatus
from app.models.db_models import ChapterProcessingState


def get_state_by_chapter_and_mode(session: Session, chapter_id: uuid.UUID, mode: PlanMode | str) -> ChapterProcessingState | None:
    mode_value = PlanMode(mode)
    return session.exec(
        select(ChapterProcessingState).where(
            ChapterProcessingState.chapter_id == chapter_id,
            ChapterProcessingState.mode == mode_value,
        )
    ).first()


def upsert_chapter_processing_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    job_id: uuid.UUID | None,
    mode: PlanMode | str,
    status: ProcessingJobStatus,
    raw_text_char_count: int = 0,
    estimated_tokens: int = 0,
    estimated_audio_seconds: int = 0,
) -> ChapterProcessingState:
    mode_value = PlanMode(mode)
    state = get_state_by_chapter_and_mode(session, chapter_id, mode_value)
    now = datetime.now(timezone.utc)

    if state is None:
        state = ChapterProcessingState(
            user_id=user_id,
            book_id=book_id,
            chapter_id=chapter_id,
            job_id=job_id,
            mode=mode_value,
            status=status,
            raw_text_char_count=raw_text_char_count,
            estimated_tokens=estimated_tokens,
            estimated_audio_seconds=estimated_audio_seconds,
            started_at=now if status == ProcessingJobStatus.PROCESSING else None,
        )
    else:
        state.job_id = job_id
        state.status = status
        state.raw_text_char_count = raw_text_char_count
        state.estimated_tokens = estimated_tokens
        state.estimated_audio_seconds = estimated_audio_seconds
        state.error_message = None
        state.updated_at = now
        if status == ProcessingJobStatus.PROCESSING:
            state.started_at = now
            state.finished_at = None

    session.add(state)
    session.commit()
    session.refresh(state)
    return state


def mark_chapter_state_ready(
    session: Session,
    chapter_id: uuid.UUID,
    mode: PlanMode | str,
    *,
    main_segment_count: int,
) -> ChapterProcessingState | None:
    state = get_state_by_chapter_and_mode(session, chapter_id, mode)
    if state is None:
        return None

    state.status = ProcessingJobStatus.READY
    state.main_segment_count = main_segment_count
    state.error_message = None
    state.finished_at = datetime.now(timezone.utc)
    state.updated_at = datetime.now(timezone.utc)
    session.add(state)
    session.commit()
    session.refresh(state)
    return state


def mark_chapter_state_error(
    session: Session,
    chapter_id: uuid.UUID,
    mode: PlanMode | str,
    error_message: str,
) -> ChapterProcessingState | None:
    state = get_state_by_chapter_and_mode(session, chapter_id, mode)
    if state is None:
        return None

    state.status = ProcessingJobStatus.ERROR
    state.error_message = error_message
    state.finished_at = datetime.now(timezone.utc)
    state.updated_at = datetime.now(timezone.utc)
    session.add(state)
    session.commit()
    session.refresh(state)
    return state
