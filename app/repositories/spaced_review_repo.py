import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem


def create_review_item_once(session: Session, item: SpacedReviewItem) -> SpacedReviewItem | None:
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except IntegrityError:
        session.rollback()
        return None


def get_due_review_items(session: Session, *, now: datetime, limit: int = 100) -> list[SpacedReviewItem]:
    return list(
        session.exec(select(SpacedReviewItem).where(SpacedReviewItem.status == ReviewItemStatus.PENDING).where(SpacedReviewItem.due_at <= now).order_by(SpacedReviewItem.due_at).limit(limit)).all()
    )


def mark_review_item_due(session: Session, review_item: SpacedReviewItem) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.DUE
    review_item.updated_at = datetime.now(timezone.utc)
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def defer_review_item(session: Session, review_item: SpacedReviewItem, due_at: datetime) -> SpacedReviewItem:
    review_item.due_at = due_at
    review_item.updated_at = datetime.now(timezone.utc)
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def get_review_item_by_chapter_mode_interval(
    session: Session,
    *,
    user_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode,
    interval_days: int,
) -> SpacedReviewItem | None:
    return session.exec(
        select(SpacedReviewItem).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.chapter_id == chapter_id,
            SpacedReviewItem.mode == mode,
            SpacedReviewItem.interval_days == interval_days,
        )
    ).first()
