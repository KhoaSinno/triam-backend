import uuid
from datetime import datetime

from pydantic import BaseModel

from app.core.constant import ReviewItemStatus


class ReviewActionResponse(BaseModel):
    review_item_id: uuid.UUID
    status: ReviewItemStatus
    completed_at: datetime | None = None
