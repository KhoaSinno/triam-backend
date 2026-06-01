import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import LearningProgressStatus, PlanMode, PlanStatus
from app.core.exceptions import BadRequestError, BookNotFoundError, NoPlayableAudioError
from app.models.db_models import Book, LearningUnit, LearningUnitProgress, LearningUnitSegment, ReadingPlan
from app.repositories.learning_progress_repo import get_latest_activity, get_progress, list_book_progress, list_playable_unit_ids, save_progress
from app.repositories.reading_plan_schedule_repo import delete_slots_for_plan
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    LearningUnitProgressResponse,
    LearningUnitProgressUpdateRequest,
)
from app.services.spaced_review_service import create_spaced_reviews_after_unit_completion


def _load_owned_book(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID) -> Book:
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    return book


def _load_learning_unit(session: Session, *, book_id: uuid.UUID, learning_unit_id: uuid.UUID, mode: PlanMode) -> LearningUnit:
    unit = session.exec(
        select(LearningUnit).where(
            LearningUnit.id == learning_unit_id,
            LearningUnit.book_id == book_id,
            LearningUnit.mode == mode,
        )
    ).first()
    if not unit:
        raise BadRequestError("Bài học không thuộc sách/mode này.")
    return unit


def _segments_for_unit(session: Session, *, learning_unit_id: uuid.UUID) -> list[LearningUnitSegment]:
    return list(
        session.exec(
            select(LearningUnitSegment)
            .where(LearningUnitSegment.learning_unit_id == learning_unit_id)
            .order_by(LearningUnitSegment.segment_index)
        ).all()
    )


def _resolve_segment(
    segments: list[LearningUnitSegment],
    *,
    segment_id: int | None,
    segment_index: int,
) -> LearningUnitSegment:
    if not segments:
        raise NoPlayableAudioError("Bài học này chưa có audio để ghi nhận tiến độ.")

    if segment_id is not None:
        for segment in segments:
            if segment.id == segment_id:
                return segment
        raise BadRequestError("Segment không thuộc bài học này.")

    for segment in segments:
        if segment.segment_index == segment_index:
            return segment
    raise BadRequestError("Segment index không thuộc bài học này.")


def _compute_progress_percent(
    *,
    segments: list[LearningUnitSegment],
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


def _to_unit_response(progress: LearningUnitProgress) -> LearningUnitProgressResponse:
    return LearningUnitProgressResponse(
        learning_unit_id=progress.learning_unit_id,
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
    unit: LearningUnit,
    progress: LearningUnitProgress,
) -> None:
    if not progress.completed_at:
        return
    create_spaced_reviews_after_unit_completion(
        session,
        user_id=user_id,
        book_id=book.id,
        learning_unit_id=unit.id,
        mode=unit.mode,
        review_text=unit.review_text or "",
        completed_at=progress.completed_at,
        source_unit_progress_id=progress.id,
    )


def _should_persist_progress(
    existing: LearningUnitProgress | None,
    *,
    now: datetime,
    segment: LearningUnitSegment,
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
    return bool(last_saved_at and now - last_saved_at >= timedelta(seconds=settings.LEARNING_PROGRESS_STALE_SECONDS))


def _check_and_deactivate_plan_on_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> None:
    playable_ids = list_playable_unit_ids(session, book_id=book_id, mode=mode)
    if not playable_ids:
        return
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    completed_count = sum(
        1
        for p in progress_rows
        if p.status == LearningProgressStatus.COMPLETED and p.learning_unit_id in playable_ids
    )
    if completed_count >= len(playable_ids):
        plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
        if plan and plan.status == PlanStatus.ACTIVE.value:
            plan.status = PlanStatus.INACTIVE.value
            session.add(plan)
            delete_slots_for_plan(session, plan_id=plan.id)
            session.commit()


def update_learning_unit_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: LearningUnitProgressUpdateRequest,
) -> LearningUnitProgressResponse:
    mode = PlanMode(payload.mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    unit = _load_learning_unit(session, book_id=book_id, learning_unit_id=learning_unit_id, mode=mode)
    segments = _segments_for_unit(session, learning_unit_id=learning_unit_id)
    segment = _resolve_segment(segments, segment_id=payload.segment_id, segment_index=payload.segment_index)
    progress_percent, total_duration_ms = _compute_progress_percent(
        segments=segments,
        segment_index=segment.segment_index,
        position_ms=payload.position_ms,
        fallback_percent=payload.progress_percent,
        fallback_total_duration_ms=payload.total_duration_ms,
    )

    now = datetime.now(timezone.utc)
    progress = get_progress(session, user_id=user_id, learning_unit_id=learning_unit_id)
    if not _should_persist_progress(
        progress,
        now=now,
        segment=segment,
        progress_percent=progress_percent,
        force_persist=payload.force_persist,
    ):
        return _to_unit_response(progress)

    first_completion = False
    if not progress:
        progress = LearningUnitProgress(
            user_id=user_id,
            book_id=book_id,
            learning_unit_id=learning_unit_id,
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
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, unit=unit, progress=saved)
        _check_and_deactivate_plan_on_completion(session, user_id=user_id, book_id=book_id, mode=mode)
    return _to_unit_response(saved)


def complete_learning_unit_manually(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode,
) -> LearningUnitProgressResponse:
    mode_value = PlanMode(mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    unit = _load_learning_unit(session, book_id=book_id, learning_unit_id=learning_unit_id, mode=mode_value)
    segments = _segments_for_unit(session, learning_unit_id=learning_unit_id)
    if not segments:
        raise NoPlayableAudioError("Bài học này chưa có audio để hoàn thành.")

    now = datetime.now(timezone.utc)
    last_segment = segments[-1]
    total_duration_ms = sum(segment.duration_ms or 0 for segment in segments)
    progress = get_progress(session, user_id=user_id, learning_unit_id=learning_unit_id)
    first_completion = False
    if not progress:
        progress = LearningUnitProgress(
            user_id=user_id,
            book_id=book_id,
            learning_unit_id=learning_unit_id,
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
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, unit=unit, progress=saved)
        _check_and_deactivate_plan_on_completion(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return _to_unit_response(saved)


def get_book_learning_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningProgressResponse:
    mode_value = PlanMode(mode)
    _load_owned_book(session, user_id=user_id, book_id=book_id)
    playable_ids = list_playable_unit_ids(session, book_id=book_id, mode=mode_value)
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode_value)
    progress_by_unit = {progress.learning_unit_id: progress for progress in progress_rows}

    units: list[LearningUnitProgressResponse] = []
    total_percent = 0
    completed = 0
    for learning_unit_id in playable_ids:
        progress = progress_by_unit.get(learning_unit_id)
        if progress:
            total_percent += progress.max_progress_percent
            completed += int(progress.status == LearningProgressStatus.COMPLETED)
            units.append(_to_unit_response(progress))
        else:
            units.append(
                LearningUnitProgressResponse(
                    learning_unit_id=learning_unit_id,
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
        completed_units=completed,
        playable_units=playable_count,
        last_learning_unit_id=latest.learning_unit_id if latest else None,
        last_segment_id=latest.current_segment_id if latest else None,
        last_segment_index=latest.last_segment_index if latest else None,
        position_ms=latest.position_ms if latest else None,
        units=units,
    )
