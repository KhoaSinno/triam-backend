import uuid
from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem
from app.repositories.spaced_review_repo import (
    cancel_unanchored_review_items_for_unit,
    create_review_item_once,
    has_active_review_chain_for_unit,
)

SPACED_REVIEW_INTERVALS = [1, 3, 7, 14, 30]


def create_spaced_reviews_after_unit_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode | str,
    review_text: str,
    completed_at: datetime,
    source_unit_progress_id: uuid.UUID,
) -> list[SpacedReviewItem]:
    clean_review_text = review_text.strip()
    if not clean_review_text:
        return []

    cancel_unanchored_review_items_for_unit(session, user_id=user_id, learning_unit_id=learning_unit_id)
    if has_active_review_chain_for_unit(session, user_id=user_id, learning_unit_id=learning_unit_id):
        return []

    mode_value = PlanMode(mode)
    first_interval_days = SPACED_REVIEW_INTERVALS[0]
    
    item = SpacedReviewItem(
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode_value,
        interval_days=first_interval_days,
        sequence_index=0,
        due_at=completed_at + timedelta(days=first_interval_days),
        status=ReviewItemStatus.PENDING,
        review_text_snapshot=clean_review_text,
        anchor_completed_at=completed_at,
        source_unit_progress_id=source_unit_progress_id,
    )
    created_item = create_review_item_once(session, item)
    return [created_item] if created_item else []

