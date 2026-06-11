import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.constant import BookStatus, PlanMode, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BookNotFoundError, BookStatusConflictError, ExternalServiceError, NoReadingPlanError, ReadingPlanNotFoundError, ReadingPlanScheduleConflictError
from app.models.db_models import Book, LearningUnit, LearningUnitSegment, ProcessingJob, ReadingPlan, ReadingPlanScheduleSlot
from app.repositories import audiobook_repo
from app.repositories.book_section_repo import BookSectionOutlineRow, list_book_section_outline_rows, list_book_sections
from app.repositories.learning_unit_repo import (
    count_unit_segments_by_book_and_mode,
    create_learning_units,
    list_learning_units,
    list_unit_segments,
)
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
from app.repositories.reading_plan_schedule_repo import delete_slots_for_plan, list_active_slots, list_slots_for_plan
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.services.learning_progress_service import build_book_learning_summary
from app.services.learning_unit_planner_service import plan_learning_units_async
from app.services.reading_plan_schedule_service import WEEKDAY_LABELS, build_slots_for_plan, validate_plan_schedule_for_activation, validate_plan_schedule_shape
from app.services.reading_plan_session_service import (
    build_plan_session_summary,
    cancel_future_sessions_for_plan,
    ensure_future_sessions_for_plan,
    mark_due_sessions_missed,
    sync_existing_session_units_from_progress,
)
from app.tasks.book_tasks import switch_mode_task


def _book_to_response_dict(session: Session, book: Book) -> dict:
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book.id)).first()
    learning_status = None
    book_progress_percent = None
    completed_at = None
    if plan:
        summary = build_book_learning_summary(session, user_id=book.user_id, book_id=book.id, mode=PlanMode(plan.mode))
        learning_status = summary.learning_status.value
        book_progress_percent = summary.book_progress_percent
        completed_at = summary.completed_at
    return {
        **book.model_dump(),
        "learning_status": learning_status,
        "book_progress_percent": book_progress_percent,
        "completed_at": completed_at,
    }


def list_books(session: Session, user_id: uuid.UUID) -> list[dict]:
    return [_book_to_response_dict(session, book) for book in audiobook_repo.get_audiobooks_by_user(session, user_id)]


def get_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    return _book_to_response_dict(session, book)


def create_new_book(session: Session, user_id: uuid.UUID, payload: BookCreateRequest) -> Book:
    book = Book(
        user_id=user_id,
        title=payload.title,
        author=payload.author,
    )
    return audiobook_repo.create_book(session, book)


def update_book_by_id(session: Session, book_data: BookUpdateRequest, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    return audiobook_repo.update_book_by_id(session, book_data, book_id, user_id)


async def delete_book_and_assets(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> None:
    await audiobook_repo.delete_book_storage(session, book_id, user_id)


def _active_plan(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise NoReadingPlanError()
    return plan


def _slot_to_dict(slot: ReadingPlanScheduleSlot) -> dict:
    return {
        "id": slot.id,
        "weekday": slot.weekday,
        "weekday_label": WEEKDAY_LABELS.get(slot.weekday, str(slot.weekday)),
        "reminder_time": slot.reminder_time,
        "timezone": slot.timezone,
        "is_active": slot.is_active,
    }


def _user_slot_to_dict(slot: ReadingPlanScheduleSlot) -> dict:
    return {
        **_slot_to_dict(slot),
        "plan_id": slot.plan_id,
        "book_id": slot.book_id,
    }


def _reading_plan_to_dict(session: Session, plan: ReadingPlan) -> dict:
    active_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
    return {
        "plan_id": plan.id,
        "book_id": plan.book_id,
        "mode": PlanMode(plan.mode),
        "pace": plan.pace,
        "schedule_config": list(plan.schedule_config or []),
        "reminder_time": plan.reminder_time,
        "status": plan.status,
        "plan_status": plan.status,
        "active_slots": [_slot_to_dict(slot) for slot in active_slots],
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
        "started_at": plan.started_at,
        "paused_at": plan.paused_at,
        "completed_at": plan.completed_at,
        "session_summary": build_plan_session_summary(session, plan_id=plan.id),
    }


def get_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise ReadingPlanNotFoundError()
    mark_due_sessions_missed(session, user_id=user_id)
    session.commit()
    return _reading_plan_to_dict(session, plan)


def list_reading_plan_slots(session: Session, user_id: uuid.UUID) -> list[dict]:
    return [_user_slot_to_dict(slot) for slot in list_active_slots(session, user_id=user_id)]


def _segments_by_unit(segments: list[LearningUnitSegment]) -> dict[uuid.UUID, list[dict]]:
    result: dict[uuid.UUID, list[dict]] = {}
    for segment in segments:
        result.setdefault(segment.learning_unit_id, []).append(segment.model_dump())
    return result


def _unit_to_dict(unit: LearningUnit, segments: list[dict] | None = None) -> dict:
    return {
        "id": str(unit.id),
        "title": unit.title,
        "status": unit.status,
        "unit_index": unit.unit_index,
        "unit_type": unit.unit_type,
        "source_text_char_count": unit.source_text_char_count,
        "estimated_audio_seconds": unit.estimated_audio_seconds,
        "main_segment_count": unit.main_segment_count,
        "review_text": unit.review_text or "",
        "review_audio_url": unit.review_audio_url or "",
        "planner_reason": unit.planner_reason,
        "segments": segments or [],
    }


def get_book_details(session: Session, book_id: uuid.UUID, user_id: uuid.UUID, *, mode: str | None = None) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    plan = _active_plan(session, book_id)
    active_mode = PlanMode(mode) if mode else PlanMode(plan.mode)
    learning_summary = build_book_learning_summary(session, user_id=user_id, book_id=book_id, mode=active_mode)
    units = list_learning_units(session, book_id, active_mode)
    segments_map = _segments_by_unit(list_unit_segments(session, [unit.id for unit in units]))

    return {
        "book_id": book.id,
        "book_status": book.status,
        "mode": active_mode.value,
        "total_sections": book.total_sections,
        "total_units": len(units),
        "learning_summary": learning_summary,
        "units": [_unit_to_dict(unit, segments_map.get(unit.id, [])) for unit in units],
    }


def get_book_outline(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    sections = list_book_section_outline_rows(session, book_id)
    by_parent: dict[uuid.UUID | None, list[BookSectionOutlineRow]] = {}
    for section in sections:
        by_parent.setdefault(section.parent_id, []).append(section)

    def walk(parent_id: uuid.UUID | None = None) -> list[dict]:
        return [
            {
                "id": str(section.id),
                "title": section.title,
                "level": section.level,
                "path": section.path,
                "page_start": section.page_start,
                "page_end": section.page_end,
                "text_char_count": section.text_char_count,
                "children": walk(section.id),
            }
            for section in by_parent.get(parent_id, [])
        ]

    return {
        "book_id": str(book_id),
        "total_sections": len(sections),
        "outline_tree": walk(),
    }


def get_book_learning_units(session: Session, book_id: uuid.UUID, user_id: uuid.UUID, mode: str) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    mode_value = PlanMode(mode)
    units = list_learning_units(session, book_id, mode_value)
    return {
        "book_id": str(book_id),
        "mode": mode_value.value,
        "total_units": len(units),
        "units": [_unit_to_dict(unit) for unit in units],
    }


async def _ensure_learning_units_for_mode(session: Session, *, book: Book, user_id: uuid.UUID, mode: PlanMode) -> list[LearningUnit]:
    existing = list_learning_units(session, book.id, mode)
    if existing:
        return existing

    sections = list_book_sections(session, book.id)
    planned_units = await plan_learning_units_async(sections, mode)
    if not planned_units:
        raise NoReadingPlanError()
    units = create_learning_units(session, user_id=user_id, book_id=book.id, mode=mode, planned_units=planned_units)
    book.total_units = len(units)
    session.add(book)
    session.commit()
    return units


async def switch_book_mode(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    payload_mode: str,
) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    requested_mode = PlanMode(payload_mode)

    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise ReadingPlanNotFoundError()

    units = await _ensure_learning_units_for_mode(session, book=book, user_id=user_id, mode=requested_mode)
    total_segments = count_unit_segments_by_book_and_mode(session, book_id, requested_mode)
    needs_generation = total_segments == 0

    plan.mode = requested_mode
    session.add(plan)
    session.commit()

    if needs_generation:
        job = _create_switch_mode_job(session, book, user_id, requested_mode, total_units=len(units))
        _enqueue_switch_mode_job(session, book_id, requested_mode.value, job)
        return {
            "message": f"Đã chuyển sang mode {requested_mode.value}. Hệ thống đang sinh audio trong background.",
            "needs_generation": True,
            "job_id": job.id,
            "status": job.status,
            "progress_percent": job.progress_percent,
        }

    return {
        "message": f"Đã chuyển sang mode {requested_mode.value}. Audio đã có sẵn.",
        "needs_generation": False,
        "job_id": None,
        "status": None,
        "progress_percent": None,
    }


def _create_switch_mode_job(session: Session, book: Book, user_id: uuid.UUID, mode: PlanMode, *, total_units: int) -> ProcessingJob:
    job = ProcessingJob(
        user_id=user_id,
        book_id=book.id,
        job_type=ProcessingJobType.SWITCH_MODE,
        status=ProcessingJobStatus.QUEUED,
        mode=mode,
        total_units=total_units,
        done_units=0,
        progress_percent=0,
        current_step=f"Đang chờ sinh audio mode {mode.value}.",
    )
    return create_processing_job(session, job)


def _enqueue_switch_mode_job(session: Session, book_id: uuid.UUID, mode: str, job: ProcessingJob) -> None:
    try:
        switch_mode_task.apply_async(
            args=[str(book_id), mode, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step=f"Không thể đưa tác vụ switch mode {mode} vào hàng đợi.",
            error_message=str(e),
        )
        raise ExternalServiceError("Không thể đưa tác vụ đổi mode vào hàng đợi xử lý. Vui lòng thử lại sau.") from e


def pause_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id)
    plan.status = PlanStatus.INACTIVE.value
    plan.paused_at = datetime.now(timezone.utc)
    session.add(plan)
    delete_slots_for_plan(session, plan_id=plan.id)
    cancel_future_sessions_for_plan(session, plan_id=plan.id)
    session.commit()
    return {"message": "Đã tạm dừng kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}


def resume_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id)

    if plan.status == PlanStatus.ACTIVE.value:
        return {"message": "Kế hoạch học tập đang hoạt động.", **_reading_plan_to_dict(session, plan)}
    if plan.status == PlanStatus.COMPLETED.value:
        raise BookStatusConflictError("Sách đã hoàn thành. Hãy dùng chức năng ôn tập hoặc học lại nếu muốn bắt đầu vòng mới.")

    if book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
        raise BookStatusConflictError("Tài liệu chưa sẵn sàng để bắt đầu học. Vui lòng chờ hệ thống xử lý thêm.")

    slots = validate_plan_schedule_for_activation(
        session,
        user_id=user_id,
        schedule_config=plan.schedule_config,
        reminder_time=plan.reminder_time,
    )

    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = plan.started_at or datetime.now(timezone.utc)
    plan.paused_at = None
    session.add(plan)
    delete_slots_for_plan(session, plan_id=plan.id)

    for slot in build_slots_for_plan(
        user_id=user_id,
        book_id=book_id,
        plan_id=plan.id,
        slots=slots,
    ):
        session.add(slot)

    try:
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)
        sync_existing_session_units_from_progress(session, plan=plan, user_id=user_id)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from exc
    return {"message": "Đã tiếp tục kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}


def update_reading_plan(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    pace: int | None = None,
    schedule_config: list[str] | None = None,
    reminder_time: str | None = None,
) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id)

    new_pace = pace if pace is not None else plan.pace
    new_schedule_config = schedule_config if schedule_config is not None else plan.schedule_config
    new_reminder_time = reminder_time if reminder_time is not None else plan.reminder_time

    if plan.status == PlanStatus.ACTIVE.value:
        slots = validate_plan_schedule_for_activation(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
            exclude_plan_id=plan.id,
        )

        delete_slots_for_plan(session, plan_id=plan.id)

        for slot in build_slots_for_plan(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan.id,
            slots=slots,
        ):
            session.add(slot)
    else:
        validate_plan_schedule_shape(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
        )
        delete_slots_for_plan(session, plan_id=plan.id)

    plan.pace = new_pace
    plan.schedule_config = new_schedule_config
    plan.reminder_time = new_reminder_time
    session.add(plan)
    try:
        if plan.status == PlanStatus.ACTIVE.value:
            ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)
            sync_existing_session_units_from_progress(session, plan=plan, user_id=user_id)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from exc

    return {
        "message": "Đã cập nhật kế hoạch học tập.",
        **_reading_plan_to_dict(session, plan),
    }
