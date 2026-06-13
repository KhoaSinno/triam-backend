import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.constant import PlanMode
from app.core.exceptions import BadRequestError, ReviewItemNotFoundError
from app.models.db_models import Book, LearningUnit, SpacedReviewItem
from app.repositories.spaced_review_repo import get_review_item_for_user, list_review_items_for_user, mark_review_item_completed, mark_review_item_skipped
from app.schemas.review import ReviewActionResponse, ReviewItemResponse, ReviewListResponse


def _to_review_item_response(session: Session, item: SpacedReviewItem) -> ReviewItemResponse:
    book = session.get(Book, item.book_id)
    unit = session.get(LearningUnit, item.learning_unit_id) if item.learning_unit_id else None
    return ReviewItemResponse(
        review_item_id=item.id,
        book_id=item.book_id,
        book_title=book.title if book else None,
        learning_unit_id=item.learning_unit_id,
        learning_unit_title=unit.title if unit else None,
        mode=item.mode,
        status=item.status,
        due_at=item.due_at,
        interval_days=item.interval_days,
        sequence_index=item.sequence_index,
        review_text=item.review_text_snapshot or (unit.review_text if unit else "") or "",
        review_audio_url=unit.review_audio_url if unit else None,
        anchor_completed_at=item.anchor_completed_at,
        last_reviewed_at=item.last_reviewed_at,
        completed_at=item.completed_at,
        notified_at=item.notified_at,
    )


def list_review_items(
    session: Session,
    *,
    user_id: uuid.UUID,
    status: str = "due",
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> ReviewListResponse:
    allowed_statuses = {"due", "upcoming", "completed", "skipped", "all"}
    if status not in allowed_statuses:
        raise BadRequestError("Trạng thái ôn tập không hợp lệ.")
    try:
        mode_value = PlanMode(mode) if mode else None
    except ValueError as exc:
        raise BadRequestError("Mode ôn tập không hợp lệ.") from exc
    now = datetime.now(timezone.utc)
    items = list_review_items_for_user(
        session,
        user_id=user_id,
        now=now,
        status_filter=status,
        book_id=book_id,
        mode=mode_value,
        limit=limit,
        offset=offset,
    )
    return ReviewListResponse(items=[_to_review_item_response(session, item) for item in items], total=len(items))


def get_review_item_detail(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewItemResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    return _to_review_item_response(session, item)


def complete_review_item(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewActionResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    saved = mark_review_item_completed(session, item, completed_at=datetime.now(timezone.utc))
    return ReviewActionResponse(review_item_id=saved.id, status=saved.status, completed_at=saved.completed_at)


def skip_review_item(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewActionResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    saved = mark_review_item_skipped(session, item, skipped_at=datetime.now(timezone.utc))
    return ReviewActionResponse(review_item_id=saved.id, status=saved.status, completed_at=saved.completed_at)
