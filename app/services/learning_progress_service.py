import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookLearningStatus, LearningProgressStatus, PlanMode, PlanStatus
from app.core.exceptions import BadRequestError, BookNotFoundError, NoPlayableAudioError
from app.models.db_models import Book, BookLearningState, LearningUnit, LearningUnitProgress, LearningUnitSegment
from app.repositories.book_learning_state_repo import get_book_learning_state, upsert_book_learning_state
from app.repositories.learning_progress_repo import get_latest_activity, get_progress, list_book_progress, list_playable_unit_ids, save_progress
from app.repositories.reading_plan_repo import get_plan_for_book_mode
from app.repositories.reading_plan_schedule_repo import set_slots_active
from app.repositories.spaced_review_repo import count_review_items_for_user
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    BookLearningSummaryResponse,
    LearningUnitProgressResponse,
    LearningUnitProgressUpdateRequest,
)
from app.services.reading_plan_session_service import cancel_future_sessions_for_plan, sync_reading_plan_session_unit_completion
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


def _complete_reading_plan_if_needed(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
    completed_at: datetime,
) -> None:
    plan = get_plan_for_book_mode(session, book_id=book_id, mode=mode)
    if not plan or plan.status == PlanStatus.COMPLETED.value:
        return

    plan.status = PlanStatus.COMPLETED.value
    plan.completed_at = plan.completed_at or completed_at
    plan.updated_at = datetime.now(timezone.utc)
    session.add(plan)
    set_slots_active(session, plan_id=plan.id, is_active=False)
    cancel_future_sessions_for_plan(session, plan_id=plan.id, now=completed_at)
    session.commit()


def sync_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningState:
    playable_ids = list_playable_unit_ids(session, book_id=book_id, mode=mode)
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    progress_by_unit = {progress.learning_unit_id: progress for progress in progress_rows}
    existing_state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)

    playable_count = len(playable_ids)
    total_percent = 0
    completed_count = 0
    started_at_candidates: list[datetime] = []
    latest_activity_candidates: list[datetime] = []
    completed_at_candidates: list[datetime] = []

    for learning_unit_id in playable_ids:
        progress = progress_by_unit.get(learning_unit_id)
        if not progress:
            continue
        total_percent += progress.max_progress_percent
        completed_count += int(progress.status == LearningProgressStatus.COMPLETED)
        if progress.started_at:
            started_at_candidates.append(progress.started_at)
        if progress.last_activity_at:
            latest_activity_candidates.append(progress.last_activity_at)
        if progress.completed_at:
            completed_at_candidates.append(progress.completed_at)

    latest = get_latest_activity(session, user_id=user_id, book_id=book_id, mode=mode)
    if playable_count and completed_count >= playable_count:
        learning_status = BookLearningStatus.COMPLETED
    elif progress_rows:
        learning_status = BookLearningStatus.IN_PROGRESS
    else:
        learning_status = BookLearningStatus.NOT_STARTED

    completed_at = None
    if learning_status == BookLearningStatus.COMPLETED:
        completed_at = existing_state.completed_at if existing_state and existing_state.completed_at else max(completed_at_candidates, default=datetime.now(timezone.utc))

    state = upsert_book_learning_state(
        session,
        user_id=user_id,
        book_id=book_id,
        mode=mode,
        status=learning_status.value,
        book_progress_percent=int(total_percent / playable_count) if playable_count else 0,
        completed_units=completed_count,
        playable_units=playable_count,
        last_learning_unit_id=latest.learning_unit_id if latest else None,
        last_segment_id=latest.current_segment_id if latest else None,
        last_segment_index=latest.last_segment_index if latest else None,
        position_ms=latest.position_ms if latest else 0,
        started_at=min(started_at_candidates, default=None),
        last_activity_at=max(latest_activity_candidates, default=None),
        completed_at=completed_at,
    )
    if learning_status == BookLearningStatus.COMPLETED and completed_at:
        _complete_reading_plan_if_needed(session, book_id=book_id, mode=mode, completed_at=completed_at)
    return state


def build_book_learning_summary(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningSummaryResponse:
    state = sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    return build_book_learning_summary_from_state(
        session,
        user_id=user_id,
        book_id=book_id,
        mode=mode,
        state=state,
    )


def build_book_learning_summary_from_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    state: BookLearningState | None = None,
    include_review_counts: bool = True,
) -> BookLearningSummaryResponse:
    state = state or get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    due_reviews_count = 0
    upcoming_reviews_count = 0
    if include_review_counts:
        now = datetime.now(timezone.utc)
        due_reviews_count = count_review_items_for_user(
            session,
            user_id=user_id,
            now=now,
            status_filter="due",
            book_id=book_id,
            mode=mode,
        )
        upcoming_reviews_count = count_review_items_for_user(
            session,
            user_id=user_id,
            now=now,
            status_filter="upcoming",
            book_id=book_id,
            mode=mode,
        )
    if state is None:
        learning_status = BookLearningStatus.NOT_STARTED
        return BookLearningSummaryResponse(
            book_id=book_id,
            mode=mode,
            learning_status=learning_status,
            is_completed=False,
            can_resume=False,
            can_review=due_reviews_count > 0 or upcoming_reviews_count > 0,
            book_progress_percent=0,
            completed_units=0,
            playable_units=0,
            last_learning_unit_id=None,
            last_segment_id=None,
            last_segment_index=None,
            position_ms=None,
            started_at=None,
            last_activity_at=None,
            completed_at=None,
            due_reviews_count=due_reviews_count,
            upcoming_reviews_count=upcoming_reviews_count,
        )

    learning_status = BookLearningStatus(state.status)
    return BookLearningSummaryResponse(
        book_id=book_id,
        mode=mode,
        learning_status=learning_status,
        is_completed=learning_status == BookLearningStatus.COMPLETED,
        can_resume=learning_status == BookLearningStatus.IN_PROGRESS,
        can_review=state.completed_units > 0 or due_reviews_count > 0 or upcoming_reviews_count > 0,
        book_progress_percent=state.book_progress_percent,
        completed_units=state.completed_units,
        playable_units=state.playable_units,
        last_learning_unit_id=state.last_learning_unit_id,
        last_segment_id=state.last_segment_id,
        last_segment_index=state.last_segment_index,
        position_ms=state.position_ms if state.last_learning_unit_id else None,
        started_at=state.started_at,
        last_activity_at=state.last_activity_at,
        completed_at=state.completed_at,
        due_reviews_count=due_reviews_count,
        upcoming_reviews_count=upcoming_reviews_count,
    )


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
    sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    sync_reading_plan_session_unit_completion(
        session,
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode,
        progress_status=saved.status,
        completed_at=saved.completed_at,
        now=saved.last_activity_at,
    )
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
    sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode_value)
    sync_reading_plan_session_unit_completion(
        session,
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode_value,
        progress_status=saved.status,
        completed_at=saved.completed_at,
        now=saved.last_activity_at,
    )
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
    for learning_unit_id in playable_ids:
        progress = progress_by_unit.get(learning_unit_id)
        if progress:
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

    summary = build_book_learning_summary(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return BookLearningProgressResponse(
        **summary.model_dump(),
        units=units,
    )
