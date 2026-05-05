import uuid

from sqlmodel import Session, func, select

from app.models.db_models import ChapterSegment


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    """Bulk tạo mới các segments."""
    for segment in segments:
        session.add(segment)
    session.commit()


def check_segments_exist_by_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> bool:
    """Kiểm tra xem đã có segment nào của mode này sinh ra chưa (trong 1 chapter)."""
    return (
        session.exec(
            select(ChapterSegment).where(
                ChapterSegment.chapter_id == chapter_id,
                ChapterSegment.mode == mode,
            )
        ).first()
        is not None
    )


def count_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: str) -> int:
    """
    Đếm tổng số segments của một mode trên toàn bộ sách.
    Dùng để xác định chính xác xem mode đó đã được gen hoàn chỉnh chưa.
    Thay thế check_segments_exist_by_mode khi cần kiểm tra cả sách.
    """
    from app.models.db_models import Chapter  # tránh circular import

    result = session.exec(
        select(func.count(ChapterSegment.id))
        .join(Chapter, ChapterSegment.chapter_id == Chapter.id)  # type: ignore[arg-type]
        .where(Chapter.book_id == book_id)
        .where(ChapterSegment.mode == mode)
    ).one()
    return result or 0


def delete_segments_by_chapter_and_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> None:
    """Xóa tất cả các segments của 1 chapter theo mode (dùng khi gen lại)."""
    segments = session.exec(
        select(ChapterSegment).where(
            ChapterSegment.chapter_id == chapter_id,
            ChapterSegment.mode == mode,
        )
    ).all()
    for s in segments:
        session.delete(s)
    session.commit()
