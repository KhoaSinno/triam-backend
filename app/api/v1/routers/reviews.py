import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.review import ReviewActionResponse
from app.services.review_service import complete_review_item, skip_review_item

router = APIRouter()


@router.post("/reviews/{review_item_id}/complete", response_model=ReviewActionResponse)
def complete_review_endpoint(review_item_id: uuid.UUID, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    return complete_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/skip", response_model=ReviewActionResponse)
def skip_review_endpoint(review_item_id: uuid.UUID, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    return skip_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)
