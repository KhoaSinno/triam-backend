import asyncio
import uuid
import os

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
from app.core.constant import BookStatus, ProcessingJobStatus


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


@celery_app.task(name="triam.admin.ingest_book")
def admin_ingest_book_task(book_id: str, job_id: str, tmp_filepath: str, document_type: str, original_filename: str) -> None:
    """Celery Background Worker (Admin Queue): Bóc tách cấu trúc file PDF/EPUB,
    upload Supabase Storage, lưu BookSections, sinh Vector Embeddings và Tóm tắt AI.
    """

    from app.services.upload_service import _extract_structure_by_type
    from app.services.document_structure_types import flatten_sections
    from app.services.document_structure_service import validate_document_structure
    from app.repositories.book_section_repo import create_book_sections
    from app.services.storage_service import upload_file_to_supabase

    parsed_book_id = uuid.UUID(book_id)
    parsed_job_id = uuid.UUID(job_id)
    log.info(f"Celery admin_ingest_book_task started | book_id={book_id} | job_id={job_id}")

    with Session(engine) as session:
        book = session.get(Book, parsed_book_id)
        job = session.get(ProcessingJob, parsed_job_id)
        if not book or not job:
            log.error(f"admin_ingest_book_task skipped: Book or Job not found | book_id={book_id}")
            return

        try:
            # Step 1: Bóc tách cấu trúc (25%)
            job.status = ProcessingJobStatus.PROCESSING
            job.progress_percent = 15
            job.current_step = "Đang phân tích cấu trúc tài liệu..."
            session.add(job)
            session.commit()

            parsed_doc = asyncio.run(_extract_structure_by_type(tmp_filepath, document_type))
            validate_document_structure(parsed_doc)
            flat_sections = flatten_sections(parsed_doc.sections)
            create_book_sections(session, parsed_book_id, parsed_doc)
            book.total_sections = len(flat_sections)

            job.progress_percent = 35
            job.current_step = "Đang tải file tài liệu lên Supabase Storage..."
            session.add(job)
            session.add(book)
            session.commit()

            # Step 2: Upload Cloud Storage (50%)
            storage_path = f"{book_id}/original.{document_type}"
            content_type = {
                "pdf": "application/pdf",
                "epub": "application/epub+zip",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }.get(document_type, "application/octet-stream")

            file_url = asyncio.run(upload_file_to_supabase(
                tmp_filepath,
                storage_path,
                bucket="raw_books",
                content_type=content_type,
            ))
            book.file_url = file_url

            job.progress_percent = 60
            job.current_step = "Đang sinh khối Vector Embeddings (RAG Knowledge)..."
            session.add(job)
            session.add(book)
            session.commit()

            # Step 3: Index Vector Chunks (85%)
            asyncio.run(index_book_sections(session, book_id=parsed_book_id))

            job.progress_percent = 85
            job.current_step = "Đang sinh bản tóm tắt AI cuốn sách..."
            session.add(job)
            session.commit()

            # Step 4: Generate AI Summary (100%)
            try:
                asyncio.run(generate_ai_book_summary(session, parsed_book_id))
            except Exception as summary_err:
                log.warning(f"Admin summary warning for book {book_id}: {summary_err}")

            book.status = BookStatus.READY.value
            job.status = ProcessingJobStatus.READY
            job.progress_percent = 100
            job.current_step = "Xử lý sách hoàn tất."
            session.add(book)
            session.add(job)
            session.commit()
            log.info(f"Celery admin_ingest_book_task COMPLETED | book_id={book_id}")

        except Exception as exc:
            log.exception(f"Celery admin_ingest_book_task FAILED | book_id={book_id} | error={exc}")
            book.status = BookStatus.ERROR.value
            book.error_message = str(exc)
            job.status = ProcessingJobStatus.ERROR
            job.error_message = str(exc)
            session.add(book)
            session.add(job)
            session.commit()
            
        finally:
            if os.path.exists(tmp_filepath):
                try:
                    os.remove(tmp_filepath)
                except Exception:
                    pass

