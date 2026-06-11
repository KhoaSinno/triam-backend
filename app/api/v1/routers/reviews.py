import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.review import ReviewActionResponse, ReviewItemResponse, ReviewListResponse
from app.services.review_service import complete_review_item, get_review_item_detail, list_review_items, skip_review_item

router = APIRouter()


@router.get("/reviews", response_model=ReviewListResponse)
def list_reviews_endpoint(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    status: str = Query(default="due"),
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_review_items(
        session,
        user_id=current_user.sub,
        status=status,
        book_id=book_id,
        mode=mode,
        limit=limit,
        offset=offset,
    )


@router.get("/books/{book_id}/reviews", response_model=ReviewListResponse)
def list_book_reviews_endpoint(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    status: str = Query(default="due"),
    mode: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_review_items(
        session,
        user_id=current_user.sub,
        status=status,
        book_id=book_id,
        mode=mode,
        limit=limit,
        offset=offset,
    )


@router.get("/reviews/{review_item_id}", response_model=ReviewItemResponse)
def get_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_review_item_detail(session, user_id=current_user.sub, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/complete", response_model=ReviewActionResponse)
def complete_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return complete_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/skip", response_model=ReviewActionResponse)
def skip_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return skip_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)
