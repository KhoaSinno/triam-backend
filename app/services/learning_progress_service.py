import json
import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import LearningProgressStatus, PlanMode
from app.core.exceptions import BadRequestError, BookNotFoundError, NoPlayableAudioError
from app.models.db_models import Book, Chapter, ChapterLearningProgress, ChapterSegment
from app.repositories.learning_progress_repo import get_latest_activity, get_progress, list_book_progress, list_playable_chapter_ids, save_progress
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    ChapterProgressResponse,
    ChapterProgressUpdateRequest,
)
from app.services.spaced_review_service import create_spaced_reviews_after_completion


def _extract_review_text(raw_data: str | None, mode: PlanMode) -> str:
    if not raw_data:
        return ""
    try:
        data = json.loads(raw_data)
    except (json.JSONDecodeError, TypeError):
        # Legacy chapters may contain a plain review script instead of the newer
        # mode-keyed JSON object. Progress completion should still succeed.
        return raw_data.strip()
    if isinstance(data, dict):
        return str(data.get(mode.value, "") or "").strip()
    return str(data or "").strip()


def _load_owned_book(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID) -> Book:
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    return book


def _load_chapter(session: Session, *, book_id: uuid.UUID, chapter_id: uuid.UUID) -> Chapter:
    chapter = session.exec(select(Chapter).where(Chapter.id == chapter_id, Chapter.book_id == book_id)).first()
    if not chapter:
        raise BadRequestError("Chapter không thuộc sách này.")
    return chapter


def _segments_for_chapter(session: Session, *, chapter_id: uuid.UUID, mode: PlanMode) -> list[ChapterSegment]:
    return list(
        session.exec(
            select(ChapterSegment)
            .where(ChapterSegment.chapter_id == chapter_id, ChapterSegment.mode == mode)
            .order_by(ChapterSegment.segment_index)
        ).all()
    )


def _resolve_segment(
    segments: list[ChapterSegment],
    *,
    segment_id: int | None,
    segment_index: int,
) -> ChapterSegment:
    if not segments:
        raise NoPlayableAudioError("Chương này chưa có audio để ghi nhận tiến độ.")

    if segment_id is not None:
        for segment in segments:
            if segment.id == segment_id:
                return segment
        raise BadRequestError("Segment không thuộc chapter/mode này.")

    for segment in segments:
        if segment.segment_index == segment_index:
            return segment
    raise BadRequestError("Segment index không thuộc chapter/mode này.")


def _compute_progress_percent(
    *,
    segments: list[ChapterSegment],
    segment_index: int,
    position_ms: int,
    fallback_percent: int | None,
    fallback_total_duration_ms: int | None,
) -> tuple[int, int]:
    durations = [segment.duration_ms or 0 for segment in segments]
    total_duration = sum(durations) or int(fallback_total_duration_ms or 0)
    if sum(durations) > 0:
        before = sum(durations[:segment_index])
        current = min(sum(durations), before + max(0, position_ms))
        return max(0, min(100, int(current * 100 / sum(durations)))), sum(durations)
    return max(0, min(100, int(fallback_percent or 0))), total_duration


def _to_chapter_response(progress: ChapterLearningProgress) -> ChapterProgressResponse:
    return ChapterProgressResponse(
        chapter_id=progress.chapter_id,
        mode=progress.mode,
        segment_id=progress.current_segment_id,
        segment_index=progress.last_segment_index,
        position_ms=progress.position_ms,
        progress_percent=progress.progress_percent,
        max_progress_percent=progress.max_progress_percent,
        status=progress.status,
        started_at=progress.started_at,
        last_activity_at=progress.last_activity_at,
        completed_at=progress.completed_at,
    )


def _create_reviews_after_completion_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book: Book,
    chapter: Chapter,
    mode: PlanMode,
    progress: ChapterLearningProgress,
) -> None:
    if not progress.completed_at:
        return
    review_text = _extract_review_text(chapter.review_text, mode)
    create_spaced_reviews_after_completion(
        session,
        user_id=user_id,
        book_id=book.id,
        chapter_id=chapter.id,
        mode=mode,
        review_text=review_text,
        completed_at=progress.completed_at,
        source_progress_id=progress.id,
    )


def _should_persist_progress(
    existing: ChapterLearningProgress | None,
    *,
    now: datetime,
    segment: ChapterSegment,
    progress_percent: int,
    force_persist: bool,
) -> bool:
    if existing is None:
        return True
    if force_persist:
        return True
    if existing.completed_at is None and progress_percent >= settings.LEARNING_COMPLETION_THRESHOLD_PERCENT:
        return True
    if existing.current_segment_id != segment.id or existing.last_segment_index != segment.segment_index:
        return True
    if progress_percent - existing.max_progress_percent >= settings.LEARNING_PROGRESS_MIN_DELTA_PERCENT:
        return True

    last_saved_at = existing.last_activity_at or existing.updated_at
    if last_saved_at and now - last_saved_at >= timedelta(seconds=settings.LEARNING_PROGRESS_STALE_SECONDS):
        return True
    return False


def update_chapter_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    payload: ChapterProgressUpdateRequest,
) -> ChapterProgressResponse:
    mode = PlanMode(payload.mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    chapter = _load_chapter(session, book_id=book_id, chapter_id=chapter_id)
    segments = _segments_for_chapter(session, chapter_id=chapter_id, mode=mode)
    segment = _resolve_segment(segments, segment_id=payload.segment_id, segment_index=payload.segment_index)
    progress_percent, total_duration_ms = _compute_progress_percent(
        segments=segments,
        segment_index=segment.segment_index,
        position_ms=payload.position_ms,
        fallback_percent=payload.progress_percent,
        fallback_total_duration_ms=payload.total_duration_ms,
    )

    now = datetime.now(timezone.utc)
    progress = get_progress(session, user_id=user_id, chapter_id=chapter_id, mode=mode)
    if not _should_persist_progress(
        progress,
        now=now,
        segment=segment,
        progress_percent=progress_percent,
        force_persist=payload.force_persist,
    ):
        return _to_chapter_response(progress)

    first_completion = False
    if not progress:
        progress = ChapterLearningProgress(
            user_id=user_id,
            book_id=book_id,
            chapter_id=chapter_id,
            mode=mode,
            started_at=now,
        )

    progress.current_segment_id = segment.id
    progress.last_segment_index = segment.segment_index
    progress.position_ms = payload.position_ms
    progress.listened_ms = max(progress.listened_ms, payload.listened_ms)
    progress.total_duration_ms = total_duration_ms
    progress.progress_percent = progress_percent
    progress.max_progress_percent = max(progress.max_progress_percent, progress_percent)
    progress.last_activity_at = now
    progress.updated_at = now

    if progress.completed_at is None and progress.max_progress_percent >= settings.LEARNING_COMPLETION_THRESHOLD_PERCENT:
        progress.status = LearningProgressStatus.COMPLETED
        progress.completed_at = now
        first_completion = True
    elif progress.completed_at is not None:
        progress.status = LearningProgressStatus.COMPLETED
    else:
        progress.status = LearningProgressStatus.IN_PROGRESS

    saved = save_progress(session, progress)
    if first_completion:
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, chapter=chapter, mode=mode, progress=saved)
    return _to_chapter_response(saved)


def complete_chapter_manually(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode,
) -> ChapterProgressResponse:
    mode_value = PlanMode(mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    chapter = _load_chapter(session, book_id=book_id, chapter_id=chapter_id)
    segments = _segments_for_chapter(session, chapter_id=chapter_id, mode=mode_value)
    if not segments:
        raise NoPlayableAudioError("Chương này chưa có audio để hoàn thành.")

    now = datetime.now(timezone.utc)
    last_segment = segments[-1]
    total_duration_ms = sum(segment.duration_ms or 0 for segment in segments)
    progress = get_progress(session, user_id=user_id, chapter_id=chapter_id, mode=mode_value)
    first_completion = False
    if not progress:
        progress = ChapterLearningProgress(
            user_id=user_id,
            book_id=book_id,
            chapter_id=chapter_id,
            mode=mode_value,
            started_at=now,
        )

    if progress.completed_at is None:
        progress.completed_at = now
        first_completion = True

    progress.current_segment_id = last_segment.id
    progress.last_segment_index = last_segment.segment_index
    progress.position_ms = last_segment.duration_ms or 0
    progress.total_duration_ms = total_duration_ms
    progress.progress_percent = 100
    progress.max_progress_percent = 100
    progress.status = LearningProgressStatus.COMPLETED
    progress.last_activity_at = now
    progress.updated_at = now
    saved = save_progress(session, progress)
    if first_completion:
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, chapter=chapter, mode=mode_value, progress=saved)
    return _to_chapter_response(saved)


def get_book_learning_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningProgressResponse:
    mode_value = PlanMode(mode)
    _load_owned_book(session, user_id=user_id, book_id=book_id)
    playable_ids = list_playable_chapter_ids(session, book_id=book_id, mode=mode_value)
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode_value)
    progress_by_chapter = {progress.chapter_id: progress for progress in progress_rows}

    chapters: list[ChapterProgressResponse] = []
    total_percent = 0
    completed = 0
    for chapter_id in playable_ids:
        progress = progress_by_chapter.get(chapter_id)
        if progress:
            total_percent += progress.max_progress_percent
            completed += int(progress.status == LearningProgressStatus.COMPLETED)
            chapters.append(_to_chapter_response(progress))
        else:
            chapters.append(
                ChapterProgressResponse(
                    chapter_id=chapter_id,
                    mode=mode_value,
                    segment_id=None,
                    segment_index=0,
                    position_ms=0,
                    progress_percent=0,
                    max_progress_percent=0,
                    status=LearningProgressStatus.NOT_STARTED,
                    started_at=None,
                    last_activity_at=None,
                    completed_at=None,
                )
            )

    playable_count = len(playable_ids)
    latest = get_latest_activity(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return BookLearningProgressResponse(
        book_id=book_id,
        mode=mode_value,
        book_progress_percent=int(total_percent / playable_count) if playable_count else 0,
        completed_chapters=completed,
        playable_chapters=playable_count,
        last_chapter_id=latest.chapter_id if latest else None,
        last_segment_id=latest.current_segment_id if latest else None,
        last_segment_index=latest.last_segment_index if latest else None,
        position_ms=latest.position_ms if latest else None,
        chapters=chapters,
    )
