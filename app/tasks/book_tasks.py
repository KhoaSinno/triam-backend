import asyncio
import uuid

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.constant import ProcessingJobStatus, SummaryStatus
from app.core.logger import log
from app.core.supabase import supabase
from app.db.database import engine
from app.models.db_models import Book, ProcessingJob
from app.services.book_section_knowledge_indexer import index_book_sections
from app.services.book_summary_service import generate_ai_book_summary
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


@celery_app.task(
    name="triam.books.generate_summary",
    bind=True,
    max_retries=settings.AI_SUMMARY_MAX_RETRIES,
    default_retry_delay=settings.AI_SUMMARY_RETRY_DELAY_SECONDS,
)
def generate_book_summary_task(self, book_id: str) -> None:
    """Celery Background Worker: Sinh bản tóm tắt AI cho sách.
    Tự động retry tối đa 2 lần (mỗi lần cách 15s) nếu gặp sự cố.
    """
    log.info(f"Celery generate_book_summary_task started | book_id={book_id} | attempt={self.request.retries + 1}")
    parsed_book_id = uuid.UUID(book_id)

    with Session(engine) as session:
        book = session.get(Book, parsed_book_id)
        if not book:
            log.error(f"Generate summary task skipped: Book not found | book_id={book_id}")
            return

        book.ai_summary_status = SummaryStatus.PROCESSING.value
        session.add(book)
        session.commit()

        try:
            asyncio.run(generate_ai_book_summary(session, parsed_book_id))
            log.info(f"Celery generate_book_summary_task completed successfully | book_id={book_id}")
        except Exception as exc:
            log.warning(f"Celery generate_book_summary_task failed (attempt {self.request.retries + 1}) | error={exc}")
            if self.request.retries < self.max_retries:
                raise self.retry(exc=exc)
            else:
                log.error(f"Celery generate_book_summary_task permanently failed after max retries | book_id={book_id}")
                book.ai_summary_status = SummaryStatus.FAILED.value
                book.ai_summary_error = f"Không thể tạo tóm tắt AI sau {self.max_retries + 1} lần thử: {str(exc)}"
                session.add(book)
                session.commit()

