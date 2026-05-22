import asyncio
import uuid

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.constant import ProcessingJobStatus
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import ProcessingJob
from app.services.workers.book_pipeline import run_background_processing, run_switch_mode_processing


def _job_is_ready(job_id: uuid.UUID) -> bool:
    with Session(engine) as session:
        job = session.get(ProcessingJob, job_id)
        return bool(job and job.status == ProcessingJobStatus.READY)


@celery_app.task(name="triam.books.process")
def process_book_task(book_id: str, mode: str, job_id: str) -> None:
    """Run initial book processing from a Celery worker."""
    log.info(f"Celery process_book_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    parsed_book_id = uuid.UUID(book_id)
    parsed_job_id = uuid.UUID(job_id)

    if _job_is_ready(parsed_job_id):
        log.info(f"Skip process_book_task because job is already READY | book_id={book_id} | job_id={job_id}")
        return

    asyncio.run(
        run_background_processing(
            parsed_book_id,
            mode,
            parsed_job_id,
        )
    )


@celery_app.task(name="triam.books.switch_mode")
def switch_mode_task(book_id: str, mode: str, job_id: str) -> None:
    """Run switch-mode audio generation from a Celery worker."""
    log.info(f"Celery switch_mode_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    parsed_book_id = uuid.UUID(book_id)
    parsed_job_id = uuid.UUID(job_id)

    if _job_is_ready(parsed_job_id):
        log.info(f"Skip switch_mode_task because job is already READY | book_id={book_id} | job_id={job_id}")
        return

    asyncio.run(
        run_switch_mode_processing(
            parsed_book_id,
            mode,
            parsed_job_id,
        )
    )
