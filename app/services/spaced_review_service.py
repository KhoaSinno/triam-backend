import uuid
from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem
from app.repositories.spaced_review_repo import create_review_item_once

SPACED_REVIEW_INTERVALS = [1, 3, 7, 14, 30]


def create_spaced_reviews_for_chapter(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode | str,
    review_text: str,
    base_time: datetime,
) -> list[SpacedReviewItem]:
    clean_review_text = review_text.strip()
    if not clean_review_text:
        return []

    mode_value = PlanMode(mode)
    created: list[SpacedReviewItem] = []
    for index, days in enumerate(SPACED_REVIEW_INTERVALS):
        item = SpacedReviewItem(
            user_id=user_id,
            book_id=book_id,
            chapter_id=chapter_id,
            mode=mode_value,
            interval_days=days,
            sequence_index=index,
            due_at=base_time + timedelta(days=days),
            status=ReviewItemStatus.PENDING,
            review_text_snapshot=clean_review_text,
        )
        created_item = create_review_item_once(session, item)
        if created_item:
            created.append(created_item)
    return created
