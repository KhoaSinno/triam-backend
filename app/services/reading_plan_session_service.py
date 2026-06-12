import uuid
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, PlanMode, PlanStatus, ReadingPlanSessionStatus, ReadingPlanSessionUnitStatus
from app.core.exceptions import BadRequestError, BookNotFoundError, ReadingPlanScheduleConflictError, ReadingPlanSessionNotFoundError, ReadingPlanSessionStatusConflictError
from app.models.db_models import (
    Book,
    LearningUnit,
    ReadingPlan,
    ReadingPlanScheduleSlot,
    ReadingPlanSession,
    ReadingPlanSessionUnit,
)
from app.repositories.learning_progress_repo import list_book_progress
from app.repositories.learning_unit_repo import list_learning_units
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.reading_plan_schedule_repo import list_slots_for_plan
from app.repositories.reading_plan_session_repo import (
    FINAL_SESSION_STATUSES,
    cancel_unfinished_sessions_for_plan,
    find_session_schedule_conflict,
    get_owned_session,
    get_session_unit_for_learning_unit,
    list_session_units,
    list_sessions_for_book,
    list_sessions_for_plan,
    list_sessions_for_user_local_date,
    list_sessions_for_user_range,
    mark_overdue_sessions_missed,
    mark_overdue_sessions_missed_rows,
)
from app.services.reminder_schedule_service import ensure_aware_utc, parse_hhmm, to_local

MAX_SESSION_RANGE_DAYS = 120


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _chunk_units(units: list[LearningUnit], pace: int) -> list[list[LearningUnit]]:
    safe_pace = max(1, int(pace or 1))
    return [units[index : index + safe_pace] for index in range(0, len(units), safe_pace)]


def _next_session_datetimes(
    *,
    slots: list[ReadingPlanScheduleSlot],
    now: datetime,
    count: int,
    lookahead_days: int = 370,
) -> list[datetime]:
    if count <= 0 or not slots:
        return []

    now = ensure_aware_utc(now)
    candidates: list[datetime] = []
    for slot in sorted(slots, key=lambda value: (value.weekday, value.reminder_time)):
        slot_time = parse_hhmm(slot.reminder_time)
        tz = ZoneInfo(slot.timezone)
        local_now = now.astimezone(tz)
        for offset in range(lookahead_days):
            local_day = local_now.date() + timedelta(days=offset)
            if local_day.weekday() != slot.weekday:
                continue
            local_dt = datetime.combine(local_day, slot_time, tzinfo=tz)
            scheduled_at = local_dt.astimezone(timezone.utc)
            if scheduled_at >= now:
                candidates.append(scheduled_at)

    unique_candidates = sorted(set(candidates))
    return unique_candidates[:count]


def _completed_unit_ids(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> set[uuid.UUID]:
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    return {row.learning_unit_id for row in progress_rows if row.status == LearningProgressStatus.COMPLETED}


def _remaining_units_for_plan(session: Session, *, plan: ReadingPlan, user_id: uuid.UUID) -> list[LearningUnit]:
    mode = PlanMode(plan.mode)
    units = list_learning_units(session, plan.book_id, mode)
    completed_ids = _completed_unit_ids(session, user_id=user_id, book_id=plan.book_id, mode=mode)
    return [unit for unit in units if unit.id not in completed_ids]


def _session_local_date(scheduled_at: datetime, timezone_name: str) -> str:
    return ensure_aware_utc(scheduled_at).astimezone(ZoneInfo(timezone_name)).date().isoformat()


def ensure_future_sessions_for_plan(
    session: Session,
    *,
    plan: ReadingPlan,
    user_id: uuid.UUID,
    now: datetime | None = None,
    replace_unfinished: bool = False,
) -> int:
    now = ensure_aware_utc(now or _now_utc())
    if plan.status == PlanStatus.COMPLETED.value:
        return 0

    if replace_unfinished:
        cancel_unfinished_sessions_for_plan(session, plan_id=plan.id, now=now)
    else:
        existing = [
            row
            for row in list_sessions_for_plan(session, plan_id=plan.id)
            if row.status not in FINAL_SESSION_STATUSES
        ]
        if existing:
            return 0

    slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
    if not slots:
        return 0

    remaining_units = _remaining_units_for_plan(session, plan=plan, user_id=user_id)
    unit_groups = _chunk_units(remaining_units, plan.pace)
    scheduled_times = _next_session_datetimes(slots=slots, now=now, count=len(unit_groups))
    created = 0

    for index, (scheduled_at, unit_group) in enumerate(zip(scheduled_times, unit_groups, strict=False)):
        slot = min(slots, key=lambda value: abs((scheduled_at.astimezone(ZoneInfo(value.timezone)).weekday() - value.weekday) % 7))
        plan_session = ReadingPlanSession(
            user_id=user_id,
            plan_id=plan.id,
            book_id=plan.book_id,
            mode=PlanMode(plan.mode),
            session_index=index,
            scheduled_at=scheduled_at,
            local_date=_session_local_date(scheduled_at, slot.timezone),
            reminder_time=slot.reminder_time,
            timezone=slot.timezone,
            status=ReadingPlanSessionStatus.SCHEDULED.value,
            completed_units=0,
            total_units=len(unit_group),
        )
        session.add(plan_session)
        session.flush()

        for unit_order, unit in enumerate(unit_group):
            session.add(
                ReadingPlanSessionUnit(
                    session_id=plan_session.id,
                    plan_id=plan.id,
                    book_id=plan.book_id,
                    learning_unit_id=unit.id,
                    unit_order=unit_order,
                    status=ReadingPlanSessionUnitStatus.PENDING.value,
                )
            )
        created += 1

    return created


def cancel_future_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    now: datetime | None = None,
) -> int:
    return cancel_unfinished_sessions_for_plan(session, plan_id=plan_id, now=ensure_aware_utc(now or _now_utc()))


def mark_due_sessions_missed(
    session: Session,
    *,
    user_id: uuid.UUID | None = None,
    now: datetime | None = None,
) -> int:
    return mark_overdue_sessions_missed(session, user_id=user_id, now=ensure_aware_utc(now or _now_utc()))


def mark_due_sessions_missed_rows(
    session: Session,
    *,
    user_id: uuid.UUID | None = None,
    now: datetime | None = None,
) -> list[ReadingPlanSession]:
    return mark_overdue_sessions_missed_rows(session, user_id=user_id, now=ensure_aware_utc(now or _now_utc()))


def _recalculate_parent_session(session: Session, plan_session: ReadingPlanSession, *, now: datetime) -> ReadingPlanSession:
    units = list_session_units(session, session_ids=[plan_session.id])
    completed_count = sum(1 for unit in units if unit.status == ReadingPlanSessionUnitStatus.COMPLETED.value)
    active_count = sum(
        1
        for unit in units
        if unit.status
        in (
            ReadingPlanSessionUnitStatus.IN_PROGRESS.value,
            ReadingPlanSessionUnitStatus.COMPLETED.value,
        )
    )

    plan_session.completed_units = completed_count
    plan_session.total_units = len(units)
    plan_session.updated_at = now

    if len(units) > 0 and completed_count >= len(units):
        plan_session.status = ReadingPlanSessionStatus.COMPLETED.value
        plan_session.completed_at = plan_session.completed_at or now
    elif active_count > 0:
        plan_session.status = ReadingPlanSessionStatus.IN_PROGRESS.value
        plan_session.started_at = plan_session.started_at or now
    elif plan_session.scheduled_at <= now and plan_session.status == ReadingPlanSessionStatus.SCHEDULED.value:
        plan_session.status = ReadingPlanSessionStatus.DUE.value

    session.add(plan_session)
    return plan_session


def sync_reading_plan_session_unit_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode,
    progress_status: LearningProgressStatus,
    completed_at: datetime | None = None,
    now: datetime | None = None,
) -> None:
    now = ensure_aware_utc(now or _now_utc())
    plans = session.exec(
        select(ReadingPlan).where(
            ReadingPlan.book_id == book_id,
            ReadingPlan.mode == mode,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
    ).all()
    changed = False
    for plan in plans:
        session_unit = get_session_unit_for_learning_unit(session, plan_id=plan.id, learning_unit_id=learning_unit_id)
        if not session_unit:
            continue

        if progress_status == LearningProgressStatus.COMPLETED:
            session_unit.status = ReadingPlanSessionUnitStatus.COMPLETED.value
            session_unit.completed_at = session_unit.completed_at or completed_at or now
        elif progress_status == LearningProgressStatus.IN_PROGRESS and session_unit.status == ReadingPlanSessionUnitStatus.PENDING.value:
            session_unit.status = ReadingPlanSessionUnitStatus.IN_PROGRESS.value
        else:
            continue

        session_unit.updated_at = now
        session.add(session_unit)
        parent = session.get(ReadingPlanSession, session_unit.session_id)
        if parent:
            _recalculate_parent_session(session, parent, now=now)
        changed = True

    if changed:
        session.commit()


def _learning_unit_title_map(session: Session, unit_ids: list[uuid.UUID]) -> dict[uuid.UUID, str]:
    if not unit_ids:
        return {}
    rows = session.exec(select(LearningUnit.id, LearningUnit.title).where(LearningUnit.id.in_(unit_ids))).all()
    return dict(rows)


def sessions_to_response(session: Session, sessions: list[ReadingPlanSession]) -> list[dict]:
    units = list_session_units(session, session_ids=[item.id for item in sessions])
    units_by_session: dict[uuid.UUID, list[ReadingPlanSessionUnit]] = {}
    for unit in units:
        units_by_session.setdefault(unit.session_id, []).append(unit)

    titles = _learning_unit_title_map(session, [unit.learning_unit_id for unit in units])
    now = _now_utc()
    result: list[dict] = []
    for item in sessions:
        item_units = units_by_session.get(item.id, [])
        result.append(
            {
                "id": item.id,
                "plan_id": item.plan_id,
                "book_id": item.book_id,
                "mode": item.mode,
                "session_index": item.session_index,
                "scheduled_at": item.scheduled_at,
                "local_date": item.local_date,
                "reminder_time": item.reminder_time,
                "timezone": item.timezone,
                "status": item.status,
                "completed_units": item.completed_units,
                "total_units": item.total_units,
                "is_overdue": item.status not in FINAL_SESSION_STATUSES and item.scheduled_at < now,
                "started_at": item.started_at,
                "completed_at": item.completed_at,
                "missed_at": item.missed_at,
                "skipped_at": item.skipped_at,
                "units": [
                    {
                        "id": unit.id,
                        "learning_unit_id": unit.learning_unit_id,
                        "unit_title": titles.get(unit.learning_unit_id, ""),
                        "unit_order": unit.unit_order,
                        "status": unit.status,
                        "completed_at": unit.completed_at,
                    }
                    for unit in item_units
                ],
            }
        )
    return result


def build_plan_session_summary(session: Session, *, plan_id: uuid.UUID) -> dict:
    sessions = list_sessions_for_plan(session, plan_id=plan_id)
    next_session = next(
        (
            item
            for item in sessions
            if item.status
            not in (
                ReadingPlanSessionStatus.COMPLETED.value,
                ReadingPlanSessionStatus.SKIPPED.value,
                ReadingPlanSessionStatus.CANCELLED.value,
            )
        ),
        None,
    )
    return {
        "total_sessions": len(sessions),
        "completed_sessions": sum(1 for item in sessions if item.status == ReadingPlanSessionStatus.COMPLETED.value),
        "missed_sessions": sum(1 for item in sessions if item.status == ReadingPlanSessionStatus.MISSED.value),
        "next_session": sessions_to_response(session, [next_session])[0] if next_session else None,
    }


def list_book_reading_plan_sessions(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode | str | None = None,
) -> dict:
    now = _now_utc()
    mode_value = PlanMode(mode) if mode else None
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()
    sessions = list_sessions_for_book(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return {
        "book_id": book_id,
        "total": len(sessions),
        "items": sessions_to_response(session, sessions),
    }


def list_today_reading_plan_sessions(
    session: Session,
    *,
    user_id: uuid.UUID,
    local_date: date | None = None,
) -> dict:
    now = _now_utc()
    user_settings = get_or_create_notification_settings(session, user_id)
    resolved_date = local_date or to_local(now, user_settings.timezone).date()
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()
    sessions = list_sessions_for_user_local_date(session, user_id=user_id, local_date=resolved_date.isoformat())
    return {
        "local_date": resolved_date.isoformat(),
        "timezone": user_settings.timezone,
        "total": len(sessions),
        "items": sessions_to_response(session, sessions),
    }


def _resolve_status_filter(status: str | None) -> str | None:
    if status is None:
        return None
    try:
        return ReadingPlanSessionStatus(status).value
    except ValueError as exc:
        raise BadRequestError("Trạng thái buổi học không hợp lệ.") from exc


def _resolve_mode_filter(mode: PlanMode | str | None) -> PlanMode | None:
    if mode is None:
        return None
    try:
        return PlanMode(mode)
    except ValueError as exc:
        raise BadRequestError("Mode kế hoạch học không hợp lệ.") from exc


def _resolve_timezone_name(timezone_name: str | None, fallback: str) -> str:
    resolved = timezone_name or fallback or "Asia/Ho_Chi_Minh"
    try:
        ZoneInfo(resolved)
    except ZoneInfoNotFoundError as exc:
        raise BadRequestError("Timezone không hợp lệ.") from exc
    return resolved


def _scheduled_at_from_local(*, local_date: date, reminder_time: str, timezone_name: str) -> datetime:
    try:
        local_time = parse_hhmm(reminder_time)
    except ValueError as exc:
        raise BadRequestError("Giờ nhắc học phải đúng định dạng HH:MM.") from exc
    tz = ZoneInfo(timezone_name)
    return datetime.combine(local_date, local_time, tzinfo=tz).astimezone(timezone.utc)


def _session_summary_counts(sessions: list[ReadingPlanSession]) -> dict[str, int]:
    return {status.value: sum(1 for item in sessions if item.status == status.value) for status in ReadingPlanSessionStatus}


def list_reading_plan_sessions_range(
    session: Session,
    *,
    user_id: uuid.UUID,
    from_date: date | None = None,
    to_date: date | None = None,
    book_id: uuid.UUID | None = None,
    mode: PlanMode | str | None = None,
    status: str | None = None,
) -> dict:
    now = _now_utc()
    user_settings = get_or_create_notification_settings(session, user_id)
    local_today = to_local(now, user_settings.timezone).date()
    resolved_from = from_date or local_today - timedelta(days=7)
    resolved_to = to_date or local_today + timedelta(days=30)
    if resolved_from > resolved_to:
        raise BadRequestError("from_date không được lớn hơn to_date.")
    if (resolved_to - resolved_from).days > MAX_SESSION_RANGE_DAYS:
        raise BadRequestError(f"Khoảng thời gian không được vượt quá {MAX_SESSION_RANGE_DAYS} ngày.")

    if book_id:
        book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
        if not book:
            raise BookNotFoundError()

    mode_value = _resolve_mode_filter(mode)
    status_value = _resolve_status_filter(status)
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()

    sessions = list_sessions_for_user_range(
        session,
        user_id=user_id,
        from_local_date=resolved_from.isoformat(),
        to_local_date=resolved_to.isoformat(),
        book_id=book_id,
        mode=mode_value,
        status=status_value,
    )
    return {
        "book_id": book_id,
        "timezone": user_settings.timezone,
        "from_date": resolved_from,
        "to_date": resolved_to,
        "total": len(sessions),
        "summary": _session_summary_counts(sessions),
        "items": sessions_to_response(session, sessions),
    }


def _ensure_session_can_change(plan_session: ReadingPlanSession, *, action: str) -> None:
    if plan_session.status in FINAL_SESSION_STATUSES:
        raise ReadingPlanSessionStatusConflictError(f"Buổi học đã ở trạng thái cuối, không thể {action}.")


def skip_reading_plan_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    reason: str | None = None,
) -> dict:
    now = _now_utc()
    plan_session = get_owned_session(session, user_id=user_id, session_id=session_id)
    if not plan_session:
        raise ReadingPlanSessionNotFoundError()
    _ensure_session_can_change(plan_session, action="bỏ qua")

    plan_session.status = ReadingPlanSessionStatus.SKIPPED.value
    plan_session.skipped_at = plan_session.skipped_at or now
    plan_session.updated_at = now
    session.add(plan_session)

    units = list_session_units(session, session_ids=[plan_session.id])
    for unit in units:
        if unit.status in (ReadingPlanSessionUnitStatus.PENDING.value, ReadingPlanSessionUnitStatus.IN_PROGRESS.value):
            unit.status = ReadingPlanSessionUnitStatus.SKIPPED.value
            unit.updated_at = now
            session.add(unit)

    session.commit()
    session.refresh(plan_session)
    return {
        "message": "Đã bỏ qua buổi học.",
        "session": sessions_to_response(session, [plan_session])[0],
    }


def reschedule_reading_plan_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    local_date: date,
    reminder_time: str,
    timezone_name: str | None = None,
) -> dict:
    now = _now_utc()
    plan_session = get_owned_session(session, user_id=user_id, session_id=session_id)
    if not plan_session:
        raise ReadingPlanSessionNotFoundError()
    _ensure_session_can_change(plan_session, action="dời lịch")

    resolved_timezone = _resolve_timezone_name(timezone_name, plan_session.timezone)
    scheduled_at = _scheduled_at_from_local(
        local_date=local_date,
        reminder_time=reminder_time,
        timezone_name=resolved_timezone,
    )
    conflict = find_session_schedule_conflict(
        session,
        user_id=user_id,
        scheduled_at=scheduled_at,
        exclude_session_id=plan_session.id,
    )
    if conflict:
        conflict_book = session.get(Book, conflict.book_id)
        conflict_title = conflict_book.title if conflict_book else "một sách khác"
        raise ReadingPlanScheduleConflictError(
            f'Lịch học bị trùng với sách "{conflict_title}" vào {reminder_time} ngày {local_date.isoformat()}.'
        )

    units = list_session_units(session, session_ids=[plan_session.id])
    has_started_unit = any(unit.status in (ReadingPlanSessionUnitStatus.IN_PROGRESS.value, ReadingPlanSessionUnitStatus.COMPLETED.value) for unit in units)
    plan_session.scheduled_at = scheduled_at
    plan_session.local_date = local_date.isoformat()
    plan_session.reminder_time = reminder_time
    plan_session.timezone = resolved_timezone
    plan_session.updated_at = now
    if has_started_unit or plan_session.started_at:
        plan_session.status = ReadingPlanSessionStatus.IN_PROGRESS.value
        plan_session.started_at = plan_session.started_at or now
        if scheduled_at > now:
            plan_session.missed_at = None
    elif scheduled_at > now:
        plan_session.status = ReadingPlanSessionStatus.SCHEDULED.value
        plan_session.missed_at = None
    else:
        plan_session.status = ReadingPlanSessionStatus.MISSED.value
        plan_session.missed_at = plan_session.missed_at or now

    session.add(plan_session)
    session.commit()
    session.refresh(plan_session)
    return {
        "message": "Đã dời lịch buổi học.",
        "session": sessions_to_response(session, [plan_session])[0],
    }


def sync_existing_session_units_from_progress(session: Session, *, plan: ReadingPlan, user_id: uuid.UUID) -> None:
    progress_rows = list_book_progress(session, user_id=user_id, book_id=plan.book_id, mode=PlanMode(plan.mode))
    for progress in progress_rows:
        sync_reading_plan_session_unit_completion(
            session,
            user_id=user_id,
            book_id=plan.book_id,
            learning_unit_id=progress.learning_unit_id,
            mode=PlanMode(plan.mode),
            progress_status=progress.status,
            completed_at=progress.completed_at,
            now=progress.completed_at or progress.last_activity_at or _now_utc(),
        )
