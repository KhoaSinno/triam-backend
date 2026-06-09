import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.constant import ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BadRequestError, BookNotFoundError, ExternalServiceError, ProcessingJobNotFoundError, ProcessingJobStatusConflictError
from app.models.db_models import AdminAuditLog, AdminUser, ProcessingJob
from app.repositories.admin_repo import (
    count_learning_unit_segments_for_book,
    count_learning_units_by_status,
    create_admin_audit_log,
    get_admin_book_by_id,
    get_admin_dashboard,
    get_latest_admin_job_for_book,
    list_admin_audit_logs,
    list_admin_books,
    list_admin_jobs,
    list_admin_users,
)
from app.repositories.processing_job_repo import get_processing_job_by_id
from app.schemas.admin import (
    AdminAuditLogItem,
    AdminAuditLogsResponse,
    AdminBookDetailResponse,
    AdminBooksResponse,
    AdminDashboardResponse,
    AdminJobListItem,
    AdminJobsResponse,
    AdminMeResponse,
    AdminRetryJobResponse,
    AdminUsersResponse,
)
from app.schemas.user import UserTokenPayload
from app.tasks.book_tasks import process_book_task, switch_mode_task

RETRYABLE_JOB_STATUSES = {ProcessingJobStatus.ERROR, ProcessingJobStatus.CANCELLED}
RETRYABLE_JOB_TYPES = {ProcessingJobType.GENERATE_PLAN, ProcessingJobType.SWITCH_MODE}


def get_admin_profile(current_user: UserTokenPayload, admin_user: AdminUser) -> AdminMeResponse:
    return AdminMeResponse(
        user_id=current_user.sub,
        email=current_user.email,
        role=admin_user.role,
        is_active=admin_user.is_active,
    )


def get_dashboard(session: Session) -> AdminDashboardResponse:
    return AdminDashboardResponse(**get_admin_dashboard(session))


def get_users(session: Session, *, limit: int, offset: int) -> AdminUsersResponse:
    items, total = list_admin_users(session, limit=limit, offset=offset)
    return AdminUsersResponse(total=total, limit=limit, offset=offset, items=items)


def get_books(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    document_type: str | None = None,
    user_id: uuid.UUID | None = None,
    q: str | None = None,
) -> AdminBooksResponse:
    books, total = list_admin_books(
        session,
        limit=limit,
        offset=offset,
        status=status,
        document_type=document_type,
        user_id=user_id,
        q=q,
    )
    return AdminBooksResponse(total=total, limit=limit, offset=offset, items=books)


def get_book_detail(session: Session, book_id: uuid.UUID) -> AdminBookDetailResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    latest_job = get_latest_admin_job_for_book(session, book_id)
    return AdminBookDetailResponse(
        **book.model_dump(),
        latest_job=AdminJobListItem.model_validate(latest_job) if latest_job else None,
        learning_units_by_status=count_learning_units_by_status(session, book_id),
        segment_count=count_learning_unit_segments_for_book(session, book_id),
    )


def get_jobs(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: ProcessingJobStatus | None = None,
    job_type: ProcessingJobType | None = None,
    user_id: uuid.UUID | None = None,
    book_id: uuid.UUID | None = None,
) -> AdminJobsResponse:
    jobs, total = list_admin_jobs(
        session,
        limit=limit,
        offset=offset,
        status=status,
        job_type=job_type,
        user_id=user_id,
        book_id=book_id,
    )
    return AdminJobsResponse(total=total, limit=limit, offset=offset, items=jobs)


def retry_job(session: Session, *, admin_user_id: uuid.UUID, job_id: uuid.UUID) -> AdminRetryJobResponse:
    job = get_processing_job_by_id(session, job_id)
    if not job:
        raise ProcessingJobNotFoundError()

    _validate_retryable_job(job)
    old_status = job.status
    now = datetime.now(timezone.utc)

    job.status = ProcessingJobStatus.QUEUED
    job.progress_percent = 0
    job.current_step = "Admin đã đưa job vào hàng đợi xử lý lại."
    job.done_units = 0
    job.failed_units = 0
    job.error_message = None
    job.started_at = None
    job.finished_at = None
    job.updated_at = now
    session.add(job)
    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="job.retry",
        target_type="processing_job",
        target_id=job.id,
        metadata={
            "book_id": str(job.book_id),
            "job_type": job.job_type.value,
            "mode": job.mode.value if job.mode else None,
            "old_status": old_status.value,
            "new_status": ProcessingJobStatus.QUEUED.value,
        },
    )
    session.commit()
    session.refresh(job)

    try:
        _enqueue_retry(job)
    except Exception as exc:
        job.status = ProcessingJobStatus.ERROR
        job.current_step = "Không thể đưa job vào hàng đợi retry."
        job.error_message = str(exc)
        job.updated_at = datetime.now(timezone.utc)
        session.add(job)
        create_admin_audit_log(
            session,
            admin_user_id=admin_user_id,
            action="job.retry_enqueue_failed",
            target_type="processing_job",
            target_id=job.id,
            metadata={"error": str(exc)},
        )
        session.commit()
        raise ExternalServiceError("Không thể đưa job vào hàng đợi retry.") from exc

    return AdminRetryJobResponse(job=AdminJobListItem.model_validate(job), message="Job đã được đưa vào hàng đợi xử lý lại.")


def _validate_retryable_job(job: ProcessingJob) -> None:
    if job.status not in RETRYABLE_JOB_STATUSES:
        raise ProcessingJobStatusConflictError()
    if job.job_type not in RETRYABLE_JOB_TYPES:
        raise BadRequestError("Job này không hỗ trợ retry từ admin.")
    if not job.book_id:
        raise BadRequestError("Job không gắn với sách nên không thể retry.")
    if not job.mode:
        raise BadRequestError("Job thiếu mode nên không thể retry.")


def _enqueue_retry(job: ProcessingJob) -> None:
    task_args = [str(job.book_id), job.mode.value, str(job.id)]
    if job.job_type == ProcessingJobType.GENERATE_PLAN:
        process_book_task.apply_async(args=task_args, queue="document")
        return
    if job.job_type == ProcessingJobType.SWITCH_MODE:
        switch_mode_task.apply_async(args=task_args, queue="document")
        return
    raise BadRequestError("Job này không hỗ trợ retry từ admin.")


def get_audit_logs(
    session: Session,
    *,
    limit: int,
    offset: int,
    action: str | None = None,
    admin_user_id: uuid.UUID | None = None,
) -> AdminAuditLogsResponse:
    logs, total = list_admin_audit_logs(
        session,
        limit=limit,
        offset=offset,
        action=action,
        admin_user_id=admin_user_id,
    )
    return AdminAuditLogsResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[_audit_log_response(log) for log in logs],
    )


def _audit_log_response(log: AdminAuditLog) -> AdminAuditLogItem:
    return AdminAuditLogItem(
        id=log.id,
        admin_user_id=log.admin_user_id,
        action=log.action,
        target_type=log.target_type,
        target_id=log.target_id,
        metadata=log.metadata_json,
        created_at=log.created_at,
    )
