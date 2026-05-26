import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.review import ReviewActionResponse
from app.services.review_service import complete_review_item, skip_review_item

router = APIRouter()

# TODO: Replace with JWT user later.
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.post("/reviews/{review_item_id}/complete", response_model=ReviewActionResponse)
def complete_review_endpoint(review_item_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return complete_review_item(session, user_id=MOCK_USER_ID, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/skip", response_model=ReviewActionResponse)
def skip_review_endpoint(review_item_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return skip_review_item(session, user_id=MOCK_USER_ID, review_item_id=review_item_id)
