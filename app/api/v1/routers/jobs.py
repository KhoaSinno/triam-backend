import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.processing_job import ProcessingJobSummaryResponse
from app.services.processing_job_service import get_book_processing_status, get_job_status

router = APIRouter()

# TODO: Replace with JWT user later.
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.get("/jobs/{job_id}", response_model=ProcessingJobSummaryResponse)
def read_job_status(job_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_job_status(session, MOCK_USER_ID, job_id)


@router.get("/books/{book_id}/processing-status", response_model=ProcessingJobSummaryResponse)
def read_book_processing_status(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_processing_status(session, MOCK_USER_ID, book_id)
