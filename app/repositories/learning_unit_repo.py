import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, col, func, select

from app.core.constant import PlanMode, ProcessingJobStatus
from app.models.db_models import BookSection, LearningUnit, LearningUnitSegment, LearningUnitSource
from app.services.learning_unit_planner_service import PlannedLearningUnit


def delete_learning_units_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: PlanMode) -> None:
    units = session.exec(select(LearningUnit).where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)).all()
    for unit in units:
        session.delete(unit)


def create_learning_units(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    planned_units: list[PlannedLearningUnit],
) -> list[LearningUnit]:
    delete_learning_units_by_book_and_mode(session, book_id, mode)
    session.flush()

    created: list[LearningUnit] = []
    for unit_index, planned in enumerate(planned_units):
        unit = LearningUnit(
            user_id=user_id,
            book_id=book_id,
            mode=mode,
            unit_index=unit_index,
            title=planned.title,
            unit_type=planned.unit_type,
            status=ProcessingJobStatus.QUEUED,
            source_text_char_count=planned.source_text_char_count,
            estimated_tokens=planned.estimated_tokens,
            estimated_audio_seconds=planned.estimated_audio_seconds,
            planner_reason=planned.planner_reason,
        )
        session.add(unit)
        session.flush()

        for source_order, section_id in enumerate(planned.source_section_ids):
            session.add(
                LearningUnitSource(
                    learning_unit_id=unit.id,
                    section_id=section_id,
                    source_order=source_order,
                )
            )

        created.append(unit)

    return created


def list_learning_units(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> list[LearningUnit]:
    mode_value = PlanMode(mode)
    try:
        return list(session.exec(select(LearningUnit).where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value).order_by(col(LearningUnit.unit_index))).all())
    except ProgrammingError as exc:
        if "learning_units" in str(exc) and "does not exist" in str(exc):
            session.rollback()
            return []
        raise


def get_learning_unit_by_book(session: Session, *, book_id: uuid.UUID, learning_unit_id: uuid.UUID) -> LearningUnit | None:
    return session.exec(select(LearningUnit).where(LearningUnit.id == learning_unit_id, LearningUnit.book_id == book_id)).first()


def get_first_playable_learning_unit(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode | str,
) -> LearningUnit | None:
    """Find one unit with a real audio URL without loading every segment."""
    mode_value = PlanMode(mode)
    return session.exec(
        select(LearningUnit)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        .where(
            LearningUnit.book_id == book_id,
            LearningUnit.mode == mode_value,
            LearningUnitSegment.audio_url.is_not(None),
        )
        .order_by(col(LearningUnit.unit_index), col(LearningUnitSegment.segment_index))
        .limit(1)
    ).first()


def get_learning_unit_source_text_map(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> dict[uuid.UUID, str]:
    mode_value = PlanMode(mode)
    rows = session.exec(
        select(LearningUnit, LearningUnitSource, BookSection)
        .join(LearningUnitSource, LearningUnitSource.learning_unit_id == LearningUnit.id)
        .join(BookSection, BookSection.id == LearningUnitSource.section_id)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
        .order_by(col(LearningUnit.unit_index), col(LearningUnitSource.source_order))
    ).all()

    result: dict[uuid.UUID, list[str]] = {}
    for unit, _source, section in rows:
        if section.text_content and section.text_content.strip():
            result.setdefault(unit.id, []).append(section.text_content.strip())

    return {unit_id: "\n\n".join(parts).strip() for unit_id, parts in result.items()}


def update_learning_unit_processing(
    session: Session,
    unit: LearningUnit,
    *,
    status: ProcessingJobStatus,
    raw_text_char_count: int | None = None,
    estimated_tokens: int | None = None,
    estimated_audio_seconds: int | None = None,
    main_segment_count: int | None = None,
    error_message: str | None = None,
) -> LearningUnit:
    now = datetime.now(timezone.utc)
    unit.status = status
    unit.updated_at = now
    unit.error_message = error_message
    if raw_text_char_count is not None:
        unit.source_text_char_count = raw_text_char_count
    if estimated_tokens is not None:
        unit.estimated_tokens = estimated_tokens
    if estimated_audio_seconds is not None:
        unit.estimated_audio_seconds = estimated_audio_seconds
    if main_segment_count is not None:
        unit.main_segment_count = main_segment_count
    if status == ProcessingJobStatus.PROCESSING:
        unit.started_at = now
        unit.finished_at = None
    if status in (ProcessingJobStatus.READY, ProcessingJobStatus.ERROR, ProcessingJobStatus.CANCELLED):
        unit.finished_at = now
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit


def update_learning_unit_review(session: Session, unit_id: uuid.UUID, *, review_text: str, review_audio_url: str | None) -> None:
    unit = session.get(LearningUnit, unit_id)
    if not unit:
        return
    unit.review_text = review_text
    if review_audio_url:
        unit.review_audio_url = review_audio_url
    unit.updated_at = datetime.now(timezone.utc)
    session.add(unit)
    session.commit()


def bulk_create_unit_segments(session: Session, segments: list[LearningUnitSegment]) -> None:
    for segment in segments:
        session.add(segment)
    session.commit()


def delete_unit_segments(session: Session, learning_unit_id: uuid.UUID) -> None:
    segments = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id == learning_unit_id)).all()
    for segment in segments:
        session.delete(segment)
    session.commit()


def unit_segments_exist(session: Session, learning_unit_id: uuid.UUID) -> bool:
    return session.exec(select(LearningUnitSegment.id).where(LearningUnitSegment.learning_unit_id == learning_unit_id).limit(1)).first() is not None


def count_unit_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> int:
    mode_value = PlanMode(mode)
    result = session.exec(
        select(func.count(LearningUnitSegment.id))
        .join(LearningUnit, LearningUnitSegment.learning_unit_id == LearningUnit.id)  # type: ignore[arg-type]
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
    ).one()
    return result or 0


def list_unit_segments(session: Session, learning_unit_ids: list[uuid.UUID]) -> list[LearningUnitSegment]:
    if not learning_unit_ids:
        return []
    return list(
        session.exec(
            select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id.in_(learning_unit_ids)).order_by(LearningUnitSegment.learning_unit_id, LearningUnitSegment.segment_index)
        ).all()
    )
