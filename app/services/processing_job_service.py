import uuid

from sqlmodel import Session

from app.core.exceptions import ProcessingJobNotFoundError
from app.repositories.processing_job_repo import get_latest_processing_job_for_book, get_processing_job_by_id_and_user


def get_job_status(session: Session, user_id: uuid.UUID, job_id: uuid.UUID):
    job = get_processing_job_by_id_and_user(session, job_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job


def get_book_processing_status(session: Session, user_id: uuid.UUID, book_id: uuid.UUID):
    job = get_latest_processing_job_for_book(session, book_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job
