import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constant import LearningProgressStatus, PlanMode


class ChapterProgressUpdateRequest(BaseModel):
    mode: PlanMode
    segment_id: int | None = None
    segment_index: int = Field(ge=0)
    position_ms: int = Field(ge=0)
    listened_ms: int = Field(default=0, ge=0)
    total_duration_ms: int | None = Field(default=None, ge=0)
    progress_percent: int | None = Field(default=None, ge=0, le=100)
    force_persist: bool = False


class ManualChapterCompleteRequest(BaseModel):
    mode: PlanMode


class ChapterProgressResponse(BaseModel):
    chapter_id: uuid.UUID
    mode: PlanMode
    segment_id: int | None = None
    segment_index: int
    position_ms: int
    progress_percent: int
    max_progress_percent: int
    status: LearningProgressStatus
    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    completed_at: datetime | None = None


class BookLearningProgressResponse(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    book_progress_percent: int
    completed_chapters: int
    playable_chapters: int
    last_chapter_id: uuid.UUID | None = None
    last_segment_id: int | None = None
    last_segment_index: int | None = None
    position_ms: int | None = None
    chapters: list[ChapterProgressResponse]
