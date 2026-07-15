import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, func, select

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
    review_item.notified_at = datetime.now(timezone.utc)
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


def has_active_review_chain_for_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> bool:
    return (
        session.exec(
            select(SpacedReviewItem.id)
            .where(
                SpacedReviewItem.user_id == user_id,
                SpacedReviewItem.learning_unit_id == learning_unit_id,
                SpacedReviewItem.status != ReviewItemStatus.CANCELLED,
            )
            .limit(1)
        ).first()
        is not None
    )


def cancel_unanchored_review_items_for_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> int:
    rows = session.exec(
        select(SpacedReviewItem).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.learning_unit_id == learning_unit_id,
            SpacedReviewItem.source_unit_progress_id.is_(None),
            SpacedReviewItem.status != ReviewItemStatus.CANCELLED,
        )
    ).all()
    now = datetime.now(timezone.utc)
    for row in rows:
        row.status = ReviewItemStatus.CANCELLED
        row.updated_at = now
        session.add(row)
    session.commit()
    return len(rows)


def get_review_item_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    review_item_id: uuid.UUID,
) -> SpacedReviewItem | None:
    return session.exec(
        select(SpacedReviewItem).where(
            SpacedReviewItem.id == review_item_id,
            SpacedReviewItem.user_id == user_id,
        )
    ).first()


def list_review_items_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    now: datetime,
    status_filter: str = "due",
    book_id: uuid.UUID | None = None,
    mode: PlanMode | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[SpacedReviewItem]:
    statement = select(SpacedReviewItem).where(SpacedReviewItem.user_id == user_id)
    if book_id:
        statement = statement.where(SpacedReviewItem.book_id == book_id)
    if mode:
        statement = statement.where(SpacedReviewItem.mode == mode)

    if status_filter == "due":
        statement = statement.where(
            SpacedReviewItem.status.in_([ReviewItemStatus.DUE, ReviewItemStatus.PENDING]),
            SpacedReviewItem.due_at <= now,
        )
    elif status_filter == "upcoming":
        statement = statement.where(
            SpacedReviewItem.status == ReviewItemStatus.PENDING,
            SpacedReviewItem.due_at > now,
        )
    elif status_filter == "completed":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.COMPLETED)
    elif status_filter == "skipped":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.SKIPPED)
    elif status_filter != "all":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus(status_filter))

    if status_filter == "all":
        statement = statement.where(SpacedReviewItem.status != ReviewItemStatus.CANCELLED)

    return list(session.exec(statement.order_by(SpacedReviewItem.due_at).offset(offset).limit(limit)).all())


def count_review_items_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    now: datetime,
    status_filter: str,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> int:
    statement = select(func.count(SpacedReviewItem.id)).where(
        SpacedReviewItem.user_id == user_id,
        SpacedReviewItem.book_id == book_id,
        SpacedReviewItem.mode == mode,
    )

    if status_filter == "due":
        statement = statement.where(
            SpacedReviewItem.status.in_([ReviewItemStatus.DUE, ReviewItemStatus.PENDING]),
            SpacedReviewItem.due_at <= now,
        )
    elif status_filter == "upcoming":
        statement = statement.where(
            SpacedReviewItem.status == ReviewItemStatus.PENDING,
            SpacedReviewItem.due_at > now,
        )
    elif status_filter == "completed":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.COMPLETED)
    elif status_filter == "skipped":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.SKIPPED)
    elif status_filter == "all":
        statement = statement.where(SpacedReviewItem.status != ReviewItemStatus.CANCELLED)
    else:
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus(status_filter))

    result = session.exec(statement).one()
    return int(result or 0)


def mark_review_item_completed(session: Session, review_item: SpacedReviewItem, *, completed_at: datetime) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.COMPLETED
    review_item.completed_at = completed_at
    review_item.last_reviewed_at = completed_at
    review_item.updated_at = completed_at
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def mark_review_item_skipped(session: Session, review_item: SpacedReviewItem, *, skipped_at: datetime) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.SKIPPED
    review_item.last_reviewed_at = skipped_at
    review_item.updated_at = skipped_at
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def delete_spaced_review_items(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ các thẻ ôn tập ngắt quãng của user đối với sách và mode nhất định."""
    session.execute(
        delete(SpacedReviewItem)
        .where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    )
