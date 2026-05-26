import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import ReviewItemNotFoundError
from app.repositories.spaced_review_repo import get_review_item_for_user, mark_review_item_completed, mark_review_item_skipped
from app.schemas.review import ReviewActionResponse


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
