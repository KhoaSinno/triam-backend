import uuid
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, PlanMode, PlanStatus, ReadingPlanSessionStatus, ReadingPlanSessionUnitStatus
from app.core.exceptions import BookNotFoundError
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
    get_session_unit_for_learning_unit,
    list_session_units,
    list_sessions_for_book,
    list_sessions_for_plan,
    list_sessions_for_user_local_date,
    mark_overdue_sessions_missed,
)
from app.services.reminder_schedule_service import ensure_aware_utc, parse_hhmm, to_local


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
                "is_overdue": item.status != ReadingPlanSessionStatus.COMPLETED.value and item.scheduled_at < now,
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
