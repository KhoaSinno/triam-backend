import uuid
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, select

from app.core.constant import LearningProgressStatus, PlanMode
from app.models.db_models import LearningUnit, LearningUnitProgress, LearningUnitSegment


def get_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress).where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.learning_unit_id == learning_unit_id,
        )
    ).first()


def save_progress(session: Session, progress: LearningUnitProgress) -> LearningUnitProgress:
    try:
        session.add(progress)
        session.commit()
        session.refresh(progress)
        return progress
    except IntegrityError:
        session.rollback()
        # Race condition: hai luồng cùng tạo progress cho cùng một unit.
        # Lấy bản ghi đã tồn tại và ghi đè các field trạng thái lên bản ghi đó.
        existing = session.exec(
            select(LearningUnitProgress).where(
                LearningUnitProgress.user_id == progress.user_id,
                LearningUnitProgress.learning_unit_id == progress.learning_unit_id,
            )
        ).first()
        if not existing:
            raise
        existing.current_segment_id = progress.current_segment_id
        existing.last_segment_index = progress.last_segment_index
        existing.position_ms = progress.position_ms
        existing.listened_ms = max(existing.listened_ms, progress.listened_ms)
        existing.total_duration_ms = progress.total_duration_ms
        existing.progress_percent = progress.progress_percent
        existing.max_progress_percent = max(existing.max_progress_percent, progress.max_progress_percent)
        existing.status = progress.status
        existing.last_activity_at = progress.last_activity_at
        existing.updated_at = progress.updated_at
        if existing.completed_at is None and progress.completed_at is not None:
            existing.completed_at = progress.completed_at
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing


def list_book_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> list[LearningUnitProgress]:
    return list(
        session.exec(
            select(LearningUnitProgress)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
            )
            .order_by(LearningUnitProgress.updated_at)
        ).all()
    )


def get_latest_activity(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
            LearningUnitProgress.last_activity_at.is_not(None),
        )
        .order_by(LearningUnitProgress.last_activity_at.desc())
    ).first()


def has_studied_book_between(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    start_utc: datetime,
    end_utc: datetime,
) -> bool:
    return (
        session.exec(
            select(LearningUnitProgress.id)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
                LearningUnitProgress.last_activity_at >= start_utc,
                LearningUnitProgress.last_activity_at < end_utc,
            )
            .limit(1)
        ).first()
        is not None
    )


def list_playable_unit_ids(session: Session, *, book_id: uuid.UUID, mode: PlanMode) -> list[uuid.UUID]:
    rows = session.exec(
        select(LearningUnit.id)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)
        .group_by(LearningUnit.id, LearningUnit.unit_index)
        .order_by(LearningUnit.unit_index)
    ).all()
    return list(rows)


def has_playable_uncompleted_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> bool:
    """
    Kiểm tra xem cuốn sách còn bài học nào có thể phát (playable) mà user chưa hoàn thành không.
    Tối ưu hóa: Dùng LEFT OUTER JOIN trực tiếp ở tầng DB Engine, giới hạn LIMIT 1, RAM/CPU gần như bằng 0.
    """
    statement = (
        select(LearningUnit.id)
        # 1. Kết nối với Segment để đảm bảo bài học đó có dữ liệu âm thanh phát được (Playable)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        # 2. LEFT OUTER JOIN với bảng tiến độ của User cụ thể để tìm những bài chưa hoàn thành
        .join(
            LearningUnitProgress,
            (LearningUnitProgress.learning_unit_id == LearningUnit.id) & (LearningUnitProgress.user_id == user_id) & (LearningUnitProgress.status == LearningProgressStatus.COMPLETED),
            isouter=True,  # LEFT OUTER JOIN
        )
        # 3. Lọc theo thông tin sách và chế độ học
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)
        # 4. Điều kiện chí mạng: Bản ghi tiến độ COMPLETED phải KHÔNG tồn tại (IS NULL)
        .where(LearningUnitProgress.id.is_(None))
        # 5. Chỉ cần tìm thấy 1 bài thỏa mãn là đủ kết luận, không quét toàn bộ DB
        .limit(1)
    )

    # Thực thi câu lệnh
    result = session.exec(statement).first()

    # Nếu kết quả khác None nghĩa là tồn tại ít nhất 1 bài playable chưa completed -> True
    return result is not None


# def has_playable_uncompleted_unit(
#     session: Session,
#     *,
#     user_id: uuid.UUID,
#     book_id: uuid.UUID,
#     mode: PlanMode,
# ) -> bool:
#     playable_ids = set(list_playable_unit_ids(session, book_id=book_id, mode=mode))
#     if not playable_ids:
#         return False

#     completed_ids = set(
#         session.exec(
#             select(LearningUnitProgress.learning_unit_id).where(
#                 LearningUnitProgress.user_id == user_id,
#                 LearningUnitProgress.book_id == book_id,
#                 LearningUnitProgress.mode == mode,
#                 LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
#             )
#         ).all()
#     )
#     return bool(playable_ids - completed_ids)


def delete_book_progress(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ tiến độ các bài học của user đối với sách và mode nhất định."""
    session.execute(
        delete(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
        )
    )
