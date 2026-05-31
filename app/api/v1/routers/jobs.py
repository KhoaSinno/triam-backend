import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.processing_job import ProcessingJobSummaryResponse
from app.services.processing_job_service import get_book_processing_status, get_job_status

router = APIRouter()


@router.get("/jobs/{job_id}", response_model=ProcessingJobSummaryResponse)
def read_job_status(job_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_job_status(session, current_user.sub, job_id)


@router.get("/books/{book_id}/processing-status", response_model=ProcessingJobSummaryResponse)
def read_book_processing_status(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_processing_status(session, current_user.sub, book_id)
