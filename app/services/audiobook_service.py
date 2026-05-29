import uuid

from sqlmodel import Session, select

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BookNotFoundError, ExternalServiceError, NoReadingPlanError, ReadingPlanNotFoundError
from app.models.db_models import Book, BookSection, LearningUnit, LearningUnitSegment, ProcessingJob, ReadingPlan
from app.repositories import audiobook_repo
from app.repositories.book_section_repo import list_book_sections
from app.repositories.learning_unit_repo import (
    count_unit_segments_by_book_and_mode,
    create_learning_units,
    list_learning_units,
    list_unit_segments,
)
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.services.learning_unit_planner_service import plan_learning_units
from app.tasks.book_tasks import switch_mode_task


def list_books(session: Session, user_id: uuid.UUID) -> list[Book]:
    return audiobook_repo.get_audiobooks_by_user(session, user_id)


def get_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    return book


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
    units = list_learning_units(session, book_id, active_mode)
    segments_map = _segments_by_unit(list_unit_segments(session, [unit.id for unit in units]))

    return {
        "book_id": book.id,
        "book_status": book.status,
        "mode": active_mode.value,
        "total_sections": book.total_sections,
        "total_units": len(units),
        "units": [_unit_to_dict(unit, segments_map.get(unit.id, [])) for unit in units],
    }


def get_book_outline(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    sections = list_book_sections(session, book_id)
    by_parent: dict[uuid.UUID | None, list[BookSection]] = {}
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


def _ensure_learning_units_for_mode(session: Session, *, book: Book, user_id: uuid.UUID, mode: PlanMode) -> list[LearningUnit]:
    existing = list_learning_units(session, book.id, mode)
    if existing:
        return existing

    sections = list_book_sections(session, book.id)
    planned_units = plan_learning_units(sections, mode)
    if not planned_units:
        raise NoReadingPlanError()
    units = create_learning_units(session, user_id=user_id, book_id=book.id, mode=mode, planned_units=planned_units)
    book.total_units = len(units)
    session.add(book)
    session.commit()
    return units


def switch_book_mode(
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

    units = _ensure_learning_units_for_mode(session, book=book, user_id=user_id, mode=requested_mode)
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
