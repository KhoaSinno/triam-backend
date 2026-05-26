import uuid
from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem
from app.repositories.spaced_review_repo import cancel_unanchored_review_items_for_chapter, create_review_item_once, has_active_review_chain_for_chapter

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


def create_spaced_reviews_after_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode | str,
    review_text: str,
    completed_at: datetime,
    source_progress_id: uuid.UUID,
) -> list[SpacedReviewItem]:
    clean_review_text = review_text.strip()
    if not clean_review_text:
        return []

    # Old Phase 4.1 rows were anchored to chapter READY, not user completion.
    # Cancel them before creating the production review chain.
    cancel_unanchored_review_items_for_chapter(session, user_id=user_id, chapter_id=chapter_id)
    if has_active_review_chain_for_chapter(session, user_id=user_id, chapter_id=chapter_id):
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
            due_at=completed_at + timedelta(days=days),
            status=ReviewItemStatus.PENDING,
            review_text_snapshot=clean_review_text,
            anchor_completed_at=completed_at,
            source_progress_id=source_progress_id,
        )
        created_item = create_review_item_once(session, item)
        if created_item:
            created.append(created_item)
    return created
