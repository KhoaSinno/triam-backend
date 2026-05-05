import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.services.live_service import get_token_for_book, get_token_for_thread

router = APIRouter()


@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    return get_token_for_book(book_id)


@router.get("/live-token/thread/{thread_id}")
async def get_token_thread(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_token_for_thread(session, thread_id)
