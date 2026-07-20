import asyncio
import uuid

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.constant import ProcessingJobStatus
from app.core.logger import log
from app.core.supabase import supabase
from app.db.database import engine
from app.models.db_models import ProcessingJob
from app.services.book_section_knowledge_indexer import index_book_sections
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


@celery_app.task(name="triam.books.index_sections")
def index_book_sections_task(book_id: str) -> None:
    """Build canonical BookSection vector knowledge for grounded RAG."""
    parsed_book_id = uuid.UUID(book_id)
    log.info(f"Celery index_book_sections_task started | book_id={parsed_book_id}")
    with Session(engine) as session:
        result = asyncio.run(index_book_sections(session, book_id=parsed_book_id))
    log.info(
        "Celery index_book_sections_task done | "
        f"book_id={parsed_book_id} | sections={result.total_sections} | "
        f"indexed={result.indexed_sections} | skipped={result.skipped_sections} | chunks={result.chunks_created}"
    )


@celery_app.task(name="triam.books.purge_storage_assets")
def purge_book_storage_assets_task(book_id: str) -> None:
    """Celery Background Worker: Dọn dẹp tất cả các file vật lý trên Supabase Storage
    sau khi bản ghi sách đã được xóa sạch trong Database.
    """
    log.info(f"Celery purge_book_storage_assets_task started | book_id={book_id}")
    target_buckets = ["audios", "raw_books"]
    try:
        result = supabase.rpc(
            "get_book_asset_paths",
            {"bucket_names": target_buckets, "book_id_prefix": book_id},
        ).execute()

        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    supabase.storage.from_(bucket).remove(paths)
                    log.info(f"Celery purge_storage_assets | Deleted {len(paths)} files from bucket '{bucket}' for book {book_id}")

        log.info(f"Celery purge_book_storage_assets_task completed | book_id={book_id}")
    except Exception as exc:
        log.exception(f"Celery purge_book_storage_assets_task failed | book_id={book_id} | error={exc}")
