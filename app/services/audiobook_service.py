import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.constant import BookStatus, PlanMode, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BookNotFoundError, BookStatusConflictError, ExternalServiceError, NoReadingPlanError, ReadingPlanNotFoundError, ReadingPlanScheduleConflictError
from app.models.db_models import Book, LearningUnit, LearningUnitSegment, ProcessingJob, ReadingPlan, ReadingPlanScheduleSlot, ReadingPlanSession, SpacedReviewItem
from app.repositories import audiobook_repo
from app.repositories.book_learning_state_repo import reset_book_learning_state
from app.repositories.book_read_repo import BookListProjection, get_book_library_projection, list_book_library_projections
from app.repositories.book_section_repo import BookSectionOutlineRow, list_book_section_outline_rows, list_book_sections
from app.repositories.learning_progress_repo import delete_book_progress
from app.repositories.learning_unit_repo import (
    count_unit_segments_by_book_and_mode,
    create_learning_units,
    get_first_playable_learning_unit,
    list_learning_units,
    list_unit_segments,
)
from app.repositories.notification_outbox_repo import delete_pending_outbox_by_keys
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
from app.repositories.reading_plan_repo import get_current_plan_for_owned_book
from app.repositories.reading_plan_schedule_repo import list_active_slots, list_slots_for_plan, replace_slots_for_plan, set_slots_active
from app.repositories.reading_plan_session_repo import delete_sessions_for_plan
from app.repositories.spaced_review_repo import delete_spaced_review_items
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.services.learning_progress_service import build_book_learning_summary_from_state
from app.services.learning_unit_planner_service import plan_learning_units_async
from app.services.reading_plan_schedule_service import WEEKDAY_LABELS, WEEKDAY_SHORT_LABELS, build_slots_for_plan, validate_plan_schedule_for_activation, validate_plan_schedule_shape
from app.services.reading_plan_session_service import (
    build_plan_session_summary,
    cancel_future_sessions_for_plan,
    ensure_future_sessions_for_plan,
    mark_due_sessions_missed,
    sync_existing_session_units_from_progress,
)
from app.tasks.book_tasks import switch_mode_task


def _book_to_response_dict(projection: BookListProjection, modes_map: dict[uuid.UUID, set[str]] | None = None) -> dict:
    book = projection.book
    book_data = book.model_dump()
    learning_status = None
    book_progress_percent = None
    completed_at = None
    if projection.learning_state:
        learning_status = projection.learning_state.status
        book_progress_percent = projection.learning_state.book_progress_percent
        completed_at = projection.learning_state.completed_at

    book_modes = (modes_map or {}).get(book.id, set())
    return {
        **book_data,
        "learning_status": learning_status,
        "book_progress_percent": book_progress_percent,
        "completed_at": completed_at,
        "has_full_mode": "full" in book_modes,
        "has_pareto_mode": "pareto" in book_modes,
    }


def list_books(session: Session, user_id: uuid.UUID) -> list[dict]:
    projections = list_book_library_projections(session, user_id=user_id)
    book_ids = [p.book.id for p in projections]
    modes_map = {}
    if book_ids:
        rows = session.exec(select(LearningUnit.book_id, LearningUnit.mode).where(LearningUnit.book_id.in_(book_ids)).group_by(LearningUnit.book_id, LearningUnit.mode)).all()
        for b_id, mode in rows:
            modes_map.setdefault(b_id, set()).add(mode.value)
    return [_book_to_response_dict(p, modes_map) for p in projections]


def get_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    projection = get_book_library_projection(session, user_id=user_id, book_id=book_id)
    if not projection:
        raise BookNotFoundError()
    rows = session.exec(select(LearningUnit.mode).where(LearningUnit.book_id == book_id).group_by(LearningUnit.mode)).all()
    book_modes = {mode.value for mode in rows}
    return _book_to_response_dict(projection, {book_id: book_modes})


def list_shared_library(session: Session) -> list[dict]:
    """
    Lấy danh sách sách mẫu được chia sẻ công khai kèm thông tin các chế độ học đã bóc tách xong.
    """
    books = session.exec(select(Book).where(Book.is_shared, Book.status == "ready")).all()

    book_ids = [b.id for b in books]
    modes_map = {}
    if book_ids:
        rows = session.exec(select(LearningUnit.book_id, LearningUnit.mode).where(LearningUnit.book_id.in_(book_ids)).group_by(LearningUnit.book_id, LearningUnit.mode)).all()
        for b_id, mode in rows:
            modes_map.setdefault(b_id, set()).add(mode.value)

    items = []
    for b in books:
        book_modes = modes_map.get(b.id, set())
        items.append(
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "total_sections": b.total_sections,
                "total_units": b.total_units,
                "status": b.status,
                "ai_summary": b.ai_summary,
                "ai_summary_status": b.ai_summary_status,
                "ai_summary_error": b.ai_summary_error,
                "learning_status": None,
                "book_progress_percent": 0,
                "completed_at": None,
                "document_type": b.document_type,
                "file_url": b.file_url,
                "is_shared": b.is_shared,
                "parent_shared_id": b.parent_shared_id,
                "has_full_mode": "full" in book_modes,
                "has_pareto_mode": "pareto" in book_modes,
                "created_at": b.created_at,
                "updated_at": b.updated_at,
            }
        )
    return items


def _book_outline_tree(session: Session, book_id: uuid.UUID) -> tuple[list[dict], int]:
    sections = list_book_section_outline_rows(session, book_id)
    by_parent: dict[uuid.UUID | None, list[BookSectionOutlineRow]] = {}
    for section in sections:
        by_parent.setdefault(section.parent_id, []).append(section)

    def walk(parent_id: uuid.UUID | None = None) -> list[dict]:
        return [
            {
                "id": section.id,
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

    return walk(), len(sections)


def _shared_book_response(book: Book, modes: set[str]) -> dict:
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "total_sections": book.total_sections,
        "total_units": book.total_units,
        "status": book.status,
        "ai_summary": book.ai_summary,
        "ai_summary_status": book.ai_summary_status,
        "ai_summary_error": book.ai_summary_error,
        "learning_status": None,
        "book_progress_percent": 0,
        "completed_at": None,
        "document_type": book.document_type,
        "file_url": book.file_url,
        "is_shared": True,
        "parent_shared_id": None,
        "has_full_mode": PlanMode.FULL.value in modes,
        "has_pareto_mode": PlanMode.PARETO.value in modes,
        "created_at": book.created_at,
        "updated_at": book.updated_at,
    }


def get_shared_book_preview(
    session: Session,
    shared_book_id: uuid.UUID,
    *,
    mode: PlanMode,
) -> dict:
    """Expose a small, read-only catalog preview without granting ownership."""
    book = audiobook_repo.get_ready_shared_book_by_id(session, shared_book_id)
    if not book:
        raise BookNotFoundError()

    mode_rows = session.exec(select(LearningUnit.mode).where(LearningUnit.book_id == book.id).group_by(LearningUnit.mode)).all()
    available_modes = {item.value for item in mode_rows}
    outline_tree, total_sections = _book_outline_tree(session, book.id)
    units = list_learning_units(session, book.id, mode)
    audio_sample_unit = get_first_playable_learning_unit(session, book_id=book.id, mode=mode)
    sample_segments = _segments_by_unit(list_unit_segments(session, [audio_sample_unit.id])).get(audio_sample_unit.id, []) if audio_sample_unit else []

    return {
        "book": _shared_book_response(book, available_modes),
        "mode": mode.value,
        "available_modes": sorted(available_modes),
        "total_sections": total_sections,
        "outline_tree": outline_tree,
        "total_units": len(units),
        "learning_outline": [
            {
                "id": unit.id,
                "title": unit.title,
                "status": unit.status,
                "unit_index": unit.unit_index,
                "unit_type": unit.unit_type,
                "estimated_audio_seconds": unit.estimated_audio_seconds,
                "planner_reason": unit.planner_reason,
                "has_audio_sample": bool(audio_sample_unit and unit.id == audio_sample_unit.id),
            }
            for unit in units
        ],
        "audio_sample": _unit_to_dict(audio_sample_unit, sample_segments) if audio_sample_unit else None,
    }


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


def _active_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> ReadingPlan:
    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
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


def _slots_to_schedule_config(slots: list[ReadingPlanScheduleSlot]) -> list[str]:
    return [WEEKDAY_SHORT_LABELS.get(slot.weekday, str(slot.weekday)) for slot in slots]


def _reading_plan_to_dict(session: Session, plan: ReadingPlan) -> dict:
    all_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    active_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
    return {
        "plan_id": plan.id,
        "book_id": plan.book_id,
        "mode": PlanMode(plan.mode),
        "pace": plan.pace,
        "schedule_config": _slots_to_schedule_config(all_slots),
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
    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
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

    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
    active_mode = PlanMode(mode) if mode else PlanMode(plan.mode) if plan else PlanMode.PARETO
    learning_summary = (
        build_book_learning_summary_from_state(session, user_id=user_id, book_id=book_id, mode=active_mode)
        if plan
        else None
    )
    units = list_learning_units(session, book_id, active_mode)
    segments_map = _segments_by_unit(list_unit_segments(session, [unit.id for unit in units]))

    return {
        "book_id": book.id,
        "book_status": book.status,
        "mode": active_mode.value,
        "total_sections": book.total_sections,
        "total_units": len(units),
        "ai_summary": book.ai_summary,
        "ai_summary_status": book.ai_summary_status,
        "ai_summary_error": book.ai_summary_error,
        "learning_summary": learning_summary,
        "units": [_unit_to_dict(unit, segments_map.get(unit.id, [])) for unit in units],
    }


def get_book_outline(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    outline_tree, total_sections = _book_outline_tree(session, book_id)

    return {
        "book_id": str(book_id),
        "total_sections": total_sections,
        "outline_tree": outline_tree,
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

    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
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
    plan = _active_plan(session, book_id, user_id)
    plan.status = PlanStatus.INACTIVE.value
    plan.paused_at = datetime.now(timezone.utc)
    session.add(plan)
    set_slots_active(session, plan_id=plan.id, is_active=False)
    cancel_future_sessions_for_plan(session, plan_id=plan.id)
    session.commit()
    return {"message": "Đã tạm dừng kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}


def resume_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id, user_id)

    if plan.status == PlanStatus.ACTIVE.value:
        return {"message": "Kế hoạch học tập đang hoạt động.", **_reading_plan_to_dict(session, plan)}
    if plan.status == PlanStatus.COMPLETED.value:
        raise BookStatusConflictError("Sách đã hoàn thành. Hãy dùng chức năng ôn tập hoặc học lại nếu muốn bắt đầu vòng mới.")

    if book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
        raise BookStatusConflictError("Tài liệu chưa sẵn sàng để bắt đầu học. Vui lòng chờ hệ thống xử lý thêm.")

    existing_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    if not existing_slots:
        raise ReadingPlanScheduleConflictError("Kế hoạch học tập chưa có lịch học. Vui lòng cập nhật lịch học trước khi tiếp tục.")

    slots = validate_plan_schedule_for_activation(
        session,
        user_id=user_id,
        schedule_config=_slots_to_schedule_config(existing_slots),
        reminder_time=plan.reminder_time,
        exclude_plan_id=plan.id,
    )

    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = plan.started_at or datetime.now(timezone.utc)
    plan.paused_at = None
    session.add(plan)
    replace_slots_for_plan(
        session,
        plan_id=plan.id,
        slots=build_slots_for_plan(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan.id,
            slots=slots,
            is_active=True,
        ),
    )

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
    plan = _active_plan(session, book_id, user_id)

    new_pace = pace if pace is not None else plan.pace
    existing_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    new_schedule_config = schedule_config if schedule_config is not None else _slots_to_schedule_config(existing_slots)
    new_reminder_time = reminder_time if reminder_time is not None else plan.reminder_time

    if plan.status == PlanStatus.ACTIVE.value:
        slots = validate_plan_schedule_for_activation(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
            exclude_plan_id=plan.id,
        )

        replace_slots_for_plan(
            session,
            plan_id=plan.id,
            slots=build_slots_for_plan(
                user_id=user_id,
                book_id=book_id,
                plan_id=plan.id,
                slots=slots,
                is_active=True,
            ),
        )
    else:
        slots = validate_plan_schedule_shape(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
        )
        replace_slots_for_plan(
            session,
            plan_id=plan.id,
            slots=build_slots_for_plan(
                user_id=user_id,
                book_id=book_id,
                plan_id=plan.id,
                slots=slots,
                is_active=False,
            ),
        )

    plan.pace = new_pace
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


def select_shared_book_to_user(session: Session, *, shared_book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    """
    Nhân bản toàn bộ metadata của một sách hệ thống (shared) cho một User cụ thể.
    Sử dụng PostgreSQL Stored Procedure (clone_shared_book) để tối ưu hóa hiệu năng tối đa.
    """

    # 1. Kiểm tra sách gốc có tồn tại và được chia sẻ không
    shared_book = session.get(Book, shared_book_id)
    if not shared_book or not shared_book.is_shared or shared_book.archived_at is not None:
        raise ValueError("Sách hệ thống không tồn tại hoặc chưa được chia sẻ công khai.")

    # 2. Kiểm tra xem user đã chọn sách này trước đây chưa
    existing = session.exec(select(Book).where(Book.parent_shared_id == shared_book_id, Book.user_id == user_id)).first()
    if existing:
        return existing

    # 3. Gọi PostgreSQL Stored Function để nhân bản cực nhanh
    new_book_id = uuid.uuid4()
    session.execute(text("SELECT clone_shared_book(:shared_book_id, :new_user_id, :new_book_id)"), {"shared_book_id": shared_book_id, "new_user_id": user_id, "new_book_id": new_book_id})
    session.commit()

    # 4. Trả về đối tượng Book vừa được clone thành công
    cloned_book = session.get(Book, new_book_id)
    if not cloned_book:
        raise ValueError("Lỗi nhân bản sách từ thư viện.")
    return cloned_book


def reset_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """
    Đặt lại toàn bộ tiến độ học tập và lịch biểu của cuốn sách từ đầu cho chế độ học hiện tại.
    """
    # 1. Xác thực sách và kế hoạch học tập hiện có
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    plan = _active_plan(session, book_id, user_id)
    now = datetime.now(timezone.utc)
    mode = PlanMode(plan.mode)

    # 2. Thu thập danh sách ID của các buổi học (sessions) cũ
    sessions = session.exec(select(ReadingPlanSession.id).where(ReadingPlanSession.plan_id == plan.id)).all()
    session_ids = [str(sid) for sid in sessions]

    # 3. Thu thập danh sách ID của các thẻ ôn tập (spaced review items) cũ
    review_items = session.exec(
        select(SpacedReviewItem.id).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    ).all()
    review_ids = [str(rid) for rid in review_items]

    # 4. Tạo danh sách các idempotency_key tương ứng trong hàng đợi thông báo để xóa
    keys_to_delete = []
    for sid in session_ids:
        keys_to_delete.append(f"plan-session-reminder:{sid}")
        keys_to_delete.append(f"plan-session-missed:{sid}")
    for rid in review_ids:
        keys_to_delete.append(f"spaced-review:{rid}")

    # 5. Gọi các Repo xóa sạch dữ liệu tiến trình & lịch học
    delete_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    reset_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_spaced_review_items(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_sessions_for_plan(session, plan_id=plan.id)

    # 6. Hủy toàn bộ các thông báo đẩy PENDING còn sót lại trong Outbox
    delete_pending_outbox_by_keys(session, keys=keys_to_delete)

    # Commit trung gian để đồng bộ xóa CSDL tránh xung đột khóa ngoại
    session.flush()

    # 7. Đặt lại trạng thái kế hoạch học tập ban đầu
    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = now
    plan.paused_at = None
    plan.completed_at = None
    plan.updated_at = now
    session.add(plan)
    session.flush()

    # 8. Tự động xếp lịch mới bắt đầu từ Bài học thứ nhất
    ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)

    session.commit()
    return {"message": "Đã đặt lại kế hoạch học tập từ đầu thành công.", **_reading_plan_to_dict(session, plan)}
