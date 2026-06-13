import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constant import PlanMode, ReviewItemStatus


class ReviewItemResponse(BaseModel):
    review_item_id: uuid.UUID
    book_id: uuid.UUID
    book_title: str | None = None
    learning_unit_id: uuid.UUID | None = None
    learning_unit_title: str | None = None
    mode: PlanMode
    status: ReviewItemStatus
    due_at: datetime
    interval_days: int
    sequence_index: int
    review_text: str = ""
    review_audio_url: str | None = None
    anchor_completed_at: datetime | None = None
    last_reviewed_at: datetime | None = None
    completed_at: datetime | None = None
    notified_at: datetime | None = None


class ReviewListResponse(BaseModel):
    items: list[ReviewItemResponse] = Field(default_factory=list)
    total: int


class ReviewActionResponse(BaseModel):
    review_item_id: uuid.UUID
    status: ReviewItemStatus
    completed_at: datetime | None = None
