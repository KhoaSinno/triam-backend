import asyncio
import uuid

from app.core.celery_app import celery_app
from app.core.logger import log
from app.services.workers.book_pipeline import run_background_processing, run_switch_mode_processing


@celery_app.task(name="triam.books.process")
def process_book_task(book_id: str, mode: str, job_id: str) -> None:
    """Run initial book processing from a Celery worker."""
    log.info(f"Celery process_book_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    asyncio.run(
        run_background_processing(
            uuid.UUID(book_id),
            mode,
            uuid.UUID(job_id),
        )
    )


@celery_app.task(name="triam.books.switch_mode")
def switch_mode_task(book_id: str, mode: str, job_id: str) -> None:
    """Run switch-mode audio generation from a Celery worker."""
    log.info(f"Celery switch_mode_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    asyncio.run(
        run_switch_mode_processing(
            uuid.UUID(book_id),
            mode,
            uuid.UUID(job_id),
        )
    )
