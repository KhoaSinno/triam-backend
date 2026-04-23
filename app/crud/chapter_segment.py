from sqlmodel import Session

from app.models.db_models import ChapterSegment


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    """Bulk tạo mới các segments."""
    for segment in segments:
        session.add(segment)
    session.commit()
