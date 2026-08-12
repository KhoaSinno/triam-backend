import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.constant import (
    BookStatus,
    LearningProgressStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
    PlanMode,
    ProcessingJobStatus,
    ProcessingJobType,
    ReviewItemStatus,
)
from app.core.exceptions import BadRequestError, BookNotFoundError, BookStatusConflictError, ExternalServiceError, ProcessingJobNotFoundError, ProcessingJobStatusConflictError, UserNotFoundError
from app.core.logger import log
from app.models.db_models import (
    AdminAuditLog,
    AdminUser,
    Book,
    BookSection,
    BookSectionKnowledge,
    LearningUnit,
    LearningUnitProgress,
    LearningUnitSegment,
    LearningUnitSource,
    NotificationOutbox,
    ProcessingJob,
    ReadingPlanSession,
    SpacedReviewItem,
)
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
from app.repositories.learning_unit_repo import create_learning_units
from app.repositories.processing_job_repo import get_processing_job_by_id
from fastapi import UploadFile
from app.schemas.admin import (
    AdminAuditLogItem,
    AdminAuditLogsResponse,
    AdminBookDetailResponse,
    AdminBookLifecycleResponse,
    AdminBookListItem,
    AdminBooksResponse,
    AdminDashboardResponse,
    AdminJobListItem,
    AdminJobsResponse,
    AdminMeResponse,
    AdminRetryJobResponse,
    AdminUserDirectNotifyPayload,
    AdminUserDirectNotifyResponse,
    AdminUserStatsResponse,
    AdminUserStatusUpdateResponse,
    AdminUsersResponse,
    AdminBookOwnerInfo,
    AdminBookSectionListItem,
    AdminSectionChunkItem,
    AdminBookSectionDetailResponse,
    AdminBookExportResponse,
    AdminExportLearningModeItem,
    AdminExportLearningUnitItem,
    AdminExportLearningUnitSegmentItem,
    AdminExportLearningUnitSourceItem,
    AdminExportSectionItem,
    AdminExportChunkItem,
    AdminSegmentItem,
    AdminLearningUnitSourceItem,
    AdminLearningUnitItem,
    AdminBookAudioUnitsResponse,
    AdminBookUpdateMetadataRequest,
    AdminBookSummaryResponse,
    AdminBookUploadResponse,
    AdminCancelJobResponse,
)
from app.schemas.user import UserTokenPayload
from app.services.upload_service import _planned_units_for_book
from app.tasks.book_tasks import process_book_task, switch_mode_task, generate_book_summary_task
from app.repositories.admin_repo import auth_users

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


def get_users(session: Session, *, limit: int, offset: int, user_id: uuid.UUID | None = None) -> AdminUsersResponse:
    items, total = list_admin_users(session, limit=limit, offset=offset, user_id=user_id)
    return AdminUsersResponse(total=total, limit=limit, offset=offset, items=items)


def _get_admin_target_user(session: Session, target_user_id: uuid.UUID):
    user_row = session.exec(
        select(
            auth_users.c.id,
            auth_users.c.email,
            auth_users.c.created_at,
            auth_users.c.raw_user_meta_data,
        ).where(auth_users.c.id == target_user_id)
    ).first()
    if not user_row:
        raise UserNotFoundError()
    return user_row


def update_admin_user_status(
    session: Session,
    *,
    target_user_id: uuid.UUID,
    is_active: bool,
    ban_reason: str | None,
    admin_user_id: uuid.UUID,
) -> AdminUserStatusUpdateResponse:
    if target_user_id == admin_user_id:
        raise BadRequestError("Bạn không thể tự khóa tài khoản của chính mình.")
    _get_admin_target_user(session, target_user_id)
    if session.get(AdminUser, target_user_id):
        raise BadRequestError("Không thể thay đổi trạng thái tài khoản quản trị viên.")

    try:
        from app.core.supabase import supabase

        supabase.auth.admin.update_user_by_id(
            str(target_user_id),
            {"ban_duration": "none" if is_active else "876000h"},
        )
    except Exception as exc:
        log.error(f"Không thể cập nhật trạng thái Auth của user {target_user_id}: {exc}")
        raise ExternalServiceError("Không thể cập nhật trạng thái tài khoản.") from exc

    banned_until = None if is_active else datetime.now(timezone.utc) + timedelta(hours=876000)
    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="user.unban" if is_active else "user.ban",
        target_type="user",
        target_id=target_user_id,
        metadata={"is_active": is_active, "ban_reason": ban_reason},
    )
    session.commit()

    return AdminUserStatusUpdateResponse(
        user_id=target_user_id,
        is_active=is_active,
        banned_until=banned_until,
        message="Đã mở khóa tài khoản người dùng." if is_active else "Đã khóa tài khoản người dùng.",
    )


def send_admin_user_direct_notification(
    session: Session,
    *,
    target_user_id: uuid.UUID,
    payload: AdminUserDirectNotifyPayload,
    admin_user_id: uuid.UUID,
) -> AdminUserDirectNotifyResponse:
    _get_admin_target_user(session, target_user_id)
    idempotency_key = f"admin-announcement:{target_user_id}:{payload.idempotency_key}"
    existing = session.exec(
        select(NotificationOutbox).where(NotificationOutbox.idempotency_key == idempotency_key)
    ).first()
    if existing:
        return AdminUserDirectNotifyResponse(
            user_id=target_user_id,
            outbox_id=existing.id,
            status=existing.status.value,
            message="Thông báo này đã được tiếp nhận trước đó.",
        )

    outbox = NotificationOutbox(
        user_id=target_user_id,
        type=NotificationType.ADMIN_ANNOUNCEMENT,
        channel=NotificationChannel.ALL,
        status=NotificationStatus.PENDING,
        payload={
            "title": payload.title,
            "body": payload.body,
            "data": payload.data or {},
        },
        due_at=datetime.now(timezone.utc),
        idempotency_key=idempotency_key,
    )
    session.add(outbox)
    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="user.send_notification",
        target_type="user",
        target_id=target_user_id,
        metadata={
            "outbox_id": str(outbox.id),
            "status": NotificationStatus.PENDING.value,
            "title_length": len(payload.title),
            "body_length": len(payload.body),
        },
    )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.exec(
            select(NotificationOutbox).where(NotificationOutbox.idempotency_key == idempotency_key)
        ).first()
        if existing:
            return AdminUserDirectNotifyResponse(
                user_id=target_user_id,
                outbox_id=existing.id,
                status=existing.status.value,
                message="Thông báo này đã được tiếp nhận trước đó.",
            )
        raise

    return AdminUserDirectNotifyResponse(
        user_id=target_user_id,
        outbox_id=outbox.id,
        status=NotificationStatus.PENDING.value,
        message="Đã đưa thông báo vào hàng đợi gửi.",
    )


def get_admin_user_learning_stats(session: Session, *, target_user_id: uuid.UUID) -> AdminUserStatsResponse:
    user_id, email, created_at, meta = _get_admin_target_user(session, target_user_id)
    meta_dict = meta if isinstance(meta, dict) else {}

    total_listened_ms = int(
        session.exec(
            select(func.coalesce(func.sum(LearningUnitProgress.listened_ms), 0)).where(
                LearningUnitProgress.user_id == target_user_id
            )
        ).one()
        or 0
    )
    total_units_completed = int(
        session.exec(
            select(func.count(LearningUnitProgress.id)).where(
                LearningUnitProgress.user_id == target_user_id,
                LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
            )
        ).one()
        or 0
    )
    total_sessions_completed = int(
        session.exec(
            select(func.count(ReadingPlanSession.id)).where(
                ReadingPlanSession.user_id == target_user_id,
                ReadingPlanSession.status == "completed",
            )
        ).one()
        or 0
    )
    total_reviews_completed = int(
        session.exec(
            select(func.count(SpacedReviewItem.id)).where(
                SpacedReviewItem.user_id == target_user_id,
                SpacedReviewItem.status == ReviewItemStatus.COMPLETED,
            )
        ).one()
        or 0
    )
    books_owned_count = int(
        session.exec(select(func.count(Book.id)).where(Book.user_id == target_user_id)).one() or 0
    )
    last_active_at = session.exec(
        select(func.max(LearningUnitProgress.last_activity_at)).where(
            LearningUnitProgress.user_id == target_user_id
        )
    ).one()

    return AdminUserStatsResponse(
        user_id=user_id,
        display_name=meta_dict.get("name") or meta_dict.get("full_name"),
        email=email,
        total_listened_ms=total_listened_ms,
        total_hours_listened=round(total_listened_ms / 3_600_000, 1),
        total_sessions_completed=total_sessions_completed,
        total_units_completed=total_units_completed,
        total_reviews_completed=total_reviews_completed,
        books_owned_count=books_owned_count,
        created_at=created_at,
        last_active_at=last_active_at,
    )


def get_books(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    document_type: str | None = None,
    user_id: uuid.UUID | None = None,
    is_shared: bool | None = None,
    archived: bool | None = None,
    q: str | None = None,
) -> AdminBooksResponse:
    books, total = list_admin_books(
        session,
        limit=limit,
        offset=offset,
        status=status,
        document_type=document_type,
        user_id=user_id,
        is_shared=is_shared,
        archived=archived,
        q=q,
    )

    book_ids = [b.id for b in books]
    modes_map = {}
    if book_ids:
        rows = session.exec(
            select(LearningUnit.book_id, LearningUnit.mode)
            .where(LearningUnit.book_id.in_(book_ids))
            .group_by(LearningUnit.book_id, LearningUnit.mode)
        ).all()
        for b_id, mode in rows:
            modes_map.setdefault(b_id, set()).add(mode.value)

    user_ids = list(set([b.user_id for b in books if b.user_id]))
    users_map = {}
    if user_ids:
        users_rows = session.exec(
            select(
                auth_users.c.id,
                auth_users.c.email,
                auth_users.c.raw_user_meta_data
            ).where(auth_users.c.id.in_(user_ids))
        ).all()
        for u_id, email, meta in users_rows:
            meta_dict = meta if isinstance(meta, dict) else {}
            users_map[u_id] = {
                "email": email,
                "display_name": meta_dict.get("name") or meta_dict.get("full_name"),
                "avatar_url": meta_dict.get("avatar_url") or meta_dict.get("picture"),
            }

    items = []
    clone_counts: dict[uuid.UUID, int] = {}
    if book_ids:
        clone_counts = {
            source_id: int(count)
            for source_id, count in session.exec(
                select(Book.parent_shared_id, func.count(Book.id))
                .where(Book.parent_shared_id.in_(book_ids))
                .group_by(Book.parent_shared_id)
            ).all()
            if source_id is not None
        }
    for b in books:
        book_modes = modes_map.get(b.id, set())
        u_info = users_map.get(b.user_id, {})
        items.append(
            AdminBookListItem(
                id=b.id,
                user_id=b.user_id,
                title=b.title,
                author=b.author,
                document_type=b.document_type,
                status=b.status,
                total_sections=b.total_sections,
                total_units=b.total_units,
                error_message=b.error_message,
                is_shared=b.is_shared,
                parent_shared_id=b.parent_shared_id,
                archived_at=b.archived_at,
                clone_count=clone_counts.get(b.id, 0),
                can_permanently_delete=bool(b.archived_at and clone_counts.get(b.id, 0) == 0),
                has_full_mode="full" in book_modes,
                has_pareto_mode="pareto" in book_modes,
                user_email=u_info.get("email"),
                user_display_name=u_info.get("display_name"),
                user_avatar_url=u_info.get("avatar_url"),
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
        )
    return AdminBooksResponse(total=total, limit=limit, offset=offset, items=items)


def get_book_detail(session: Session, book_id: uuid.UUID) -> AdminBookDetailResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    latest_job = get_latest_admin_job_for_book(session, book_id)
    clone_count = int(
        session.exec(select(func.count(Book.id)).where(Book.parent_shared_id == book_id)).one() or 0
    )
    
    # Query modes
    rows = session.exec(
        select(LearningUnit.mode)
        .where(LearningUnit.book_id == book_id)
        .group_by(LearningUnit.mode)
    ).all()
    book_modes = {mode.value for mode in rows}

    owner_info = None
    if book.user_id:
        from app.repositories.admin_repo import auth_users
        user_row = session.exec(
            select(auth_users.c.id, auth_users.c.email, auth_users.c.created_at, auth_users.c.last_sign_in_at, auth_users.c.raw_user_meta_data)
            .where(auth_users.c.id == book.user_id)
        ).first()
        if user_row:
            u_id, email, c_at, l_in, meta = user_row
            meta_dict = meta if isinstance(meta, dict) else {}
            owner_info = AdminBookOwnerInfo(
                user_id=u_id,
                email=email,
                display_name=meta_dict.get("name") or meta_dict.get("full_name"),
                avatar_url=meta_dict.get("avatar_url") or meta_dict.get("picture"),
                account_created_at=c_at,
                last_sign_in_at=l_in
            )

    file_url = None
    if book.document_type:
        from app.core.supabase import supabase
        storage_path = f"{book.id}/original.{book.document_type}"
        file_url = supabase.storage.from_("raw_books").get_public_url(storage_path)

    return AdminBookDetailResponse(
        id=book.id,
        user_id=book.user_id,
        title=book.title,
        author=book.author,
        document_type=book.document_type,
        status=book.status,
        total_sections=book.total_sections,
        total_units=book.total_units,
        error_message=book.error_message,
        is_shared=book.is_shared,
        parent_shared_id=book.parent_shared_id,
        archived_at=book.archived_at,
        clone_count=clone_count,
        can_permanently_delete=bool(book.archived_at and clone_count == 0),
        has_full_mode="full" in book_modes,
        has_pareto_mode="pareto" in book_modes,
        created_at=book.created_at,
        updated_at=book.updated_at,
        file_url=file_url,
        latest_job=AdminJobListItem.model_validate(latest_job) if latest_job else None,
        learning_units_by_status=count_learning_units_by_status(session, book_id),
        segment_count=count_learning_unit_segments_for_book(session, book_id),
        owner_info=owner_info,
        ai_summary=book.ai_summary,
        ai_summary_status=book.ai_summary_status,
        ai_summary_error=book.ai_summary_error,
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
    try:
        if job.job_type == ProcessingJobType.GENERATE_PLAN:
            process_book_task.apply_async(args=task_args, task_id=str(job.id), queue="document")
            return
        if job.job_type == ProcessingJobType.SWITCH_MODE:
            switch_mode_task.apply_async(args=task_args, task_id=str(job.id), queue="document")
            return
    except Exception as exc:
        log.warning(f"Could not enqueue Celery retry task for job {job.id}: {exc}")
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


async def start_admin_book_processing(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: str,
    admin_user_id: uuid.UUID,
    is_shared: bool = False
) -> AdminRetryJobResponse:
    """
    Kích hoạt trực tiếp tiến trình băm chữ, tạo RAG vector và sinh audio cho sách mẫu
    mà không cần bất kỳ lịch trình học cá nhân (ReadingPlan) nào của Admin.
    """

    book = session.get(Book, book_id)
    if not book:
        raise BookNotFoundError()

    # 1. Cho phép xử lý sách mẫu nếu sách ở trạng thái nháp, đang xử lý, đã xong (READY) hoặc lỗi
    if book.status not in (BookStatus.DRAFT.value, BookStatus.PROCESSING.value, BookStatus.READY.value, BookStatus.ERROR.value):
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể xử lý.")

    requested_mode = PlanMode(mode)

    # 2. Ngăn chặn việc chạy trùng lặp cùng một mode đang xử lý
    existing_job = session.exec(
        select(ProcessingJob).where(
            ProcessingJob.book_id == book_id,
            ProcessingJob.mode == requested_mode,
            ProcessingJob.status.in_([ProcessingJobStatus.QUEUED, ProcessingJobStatus.PROCESSING])
        )
    ).first()
    if existing_job:
        raise BookStatusConflictError(f"Chế độ học tập '{mode}' đang được xử lý cho cuốn sách này.")

    # 3. Sinh cấu trúc bài học dự kiến
    planned_units = await _planned_units_for_book(session, book_id, requested_mode)

    # 4. Lưu học phần (LearningUnits) vào DB
    created_units = create_learning_units(
        session,
        user_id=admin_user_id,
        book_id=book_id,
        mode=requested_mode,
        planned_units=planned_units,
    )
    # Cập nhật thông minh tránh ghi đè số lượng lớn hơn của FULL mode
    book.total_units = max(book.total_units or 0, len(created_units))
    book.status = BookStatus.PROCESSING.value
    if is_shared:
        book.is_shared = True
    session.add(book)

    # 5. Tạo ProcessingJob để theo dõi tiến trình
    job = ProcessingJob(
        user_id=admin_user_id,
        book_id=book_id,
        job_type=ProcessingJobType.GENERATE_PLAN,
        status=ProcessingJobStatus.QUEUED,
        mode=requested_mode,
        total_units=len(planned_units) if planned_units else book.total_units or 0,
        done_units=0,
        progress_percent=0,
        current_step="Đang chờ xử lý sách (Admin).",
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    session.refresh(book)

    # 6. Ghi Audit Log hành động của Admin
    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="book.admin_process",
        target_type="book",
        target_id=book_id,
        metadata={"mode": mode, "job_id": str(job.id), "is_shared": is_shared},
    )
    session.commit()

    # 7. Kích hoạt Celery Task
    try:
        process_book_task.apply_async(
            args=[str(book_id), requested_mode.value, str(job.id)],
            task_id=str(job.id),
            queue="document",
        )
    except Exception as exc:
        log.warning(f"Could not enqueue Celery task for job {job.id}: {exc}")

    return AdminRetryJobResponse(
        job=AdminJobListItem.model_validate(job),
        message="Sách đã được đưa vào hàng đợi xử lý âm thanh & vector."
    )


def get_book_sections(session: Session, book_id: uuid.UUID) -> list[AdminBookSectionListItem]:
    sections = session.exec(
        select(BookSection)
        .where(BookSection.book_id == book_id)
        .order_by(BookSection.section_index.asc())
    ).all()
    
    chunks_count_map = {}
    if sections:
        chunk_counts = session.exec(
            select(BookSectionKnowledge.section_id, func.count(BookSectionKnowledge.id))
            .where(BookSectionKnowledge.book_id == book_id)
            .group_by(BookSectionKnowledge.section_id)
        ).all()
        chunks_count_map = {s_id: count for s_id, count in chunk_counts}

    # Query modes for sections
    from app.models.db_models import LearningUnitSource
    section_modes_map = {}
    if sections:
        rows = session.exec(
            select(LearningUnitSource.section_id, LearningUnit.mode)
            .join(LearningUnit, LearningUnit.id == LearningUnitSource.learning_unit_id)
            .where(LearningUnit.book_id == book_id)
        ).all()
        for s_id, mapped_mode in rows:
            section_modes_map.setdefault(s_id, set()).add(mapped_mode.value)

    return [
        AdminBookSectionListItem(
            id=s.id,
            section_index=s.section_index,
            title=s.title,
            level=s.level,
            path=s.path,
            text_char_count=s.text_char_count,
            page_start=s.page_start,
            page_end=s.page_end,
            modes=list(section_modes_map.get(s.id, set())),
            chunk_count=chunks_count_map.get(s.id, 0),
            has_text=bool(s.text_content and s.text_content.strip())
        )
        for s in sections
    ]


def get_book_section_detail(session: Session, book_id: uuid.UUID, section_id: uuid.UUID) -> AdminBookSectionDetailResponse:
    from fastapi import HTTPException
    section = session.exec(
        select(BookSection)
        .where(BookSection.book_id == book_id, BookSection.id == section_id)
    ).first()
    
    if not section:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục lục sách.")

    chunks = session.exec(
        select(BookSectionKnowledge)
        .where(BookSectionKnowledge.section_id == section_id)
        .order_by(BookSectionKnowledge.chunk_index.asc())
    ).all()

    chunk_items = [
        AdminSectionChunkItem(
            id=c.id,
            chunk_index=c.chunk_index,
            content=c.content,
            search_text=c.search_text,
            embedding_model=c.embedding_model,
            embedding_version=c.embedding_version,
            char_count=c.char_count,
            token_count=c.token_count if c.token_count is not None else int(len(c.content.split()) * 1.3),
            has_embedding=c.embedding is not None
        )
        for c in chunks
    ]

    return AdminBookSectionDetailResponse(
        id=section.id,
        section_index=section.section_index,
        title=section.title,
        level=section.level,
        path=section.path,
        text_content=section.text_content,
        text_char_count=section.text_char_count,
        page_start=section.page_start,
        page_end=section.page_end,
        chunks=chunk_items
    )


def get_book_jobs(session: Session, book_id: uuid.UUID) -> list[AdminJobListItem]:
    jobs = session.exec(
        select(ProcessingJob)
        .where(ProcessingJob.book_id == book_id)
        .order_by(ProcessingJob.created_at.desc())
    ).all()
    
    return [AdminJobListItem.model_validate(j) for j in jobs]


def export_book_json(
    session: Session,
    book_id: uuid.UUID,
    mode: PlanMode | None = None,
) -> AdminBookExportResponse:
    from app.models.db_models import LearningUnitSource
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    sections = session.exec(
        select(BookSection)
        .where(BookSection.book_id == book_id)
        .order_by(BookSection.section_index.asc())
    ).all()

    chunks = session.exec(
        select(BookSectionKnowledge)
        .where(BookSectionKnowledge.book_id == book_id)
        .order_by(BookSectionKnowledge.section_id, BookSectionKnowledge.chunk_index.asc())
    ).all()

    chunks_by_section = {}
    for c in chunks:
        chunks_by_section.setdefault(c.section_id, []).append(c)

    section_modes_map = {}
    if sections:
        rows = session.exec(
            select(LearningUnitSource.section_id, LearningUnit.mode)
            .join(LearningUnit, LearningUnit.id == LearningUnitSource.learning_unit_id)
            .where(LearningUnit.book_id == book_id)
        ).all()
        for s_id, mapped_mode in rows:
            section_modes_map.setdefault(s_id, set()).add(mapped_mode.value)

    section_items = []
    for s in sections:
        mapped_modes = section_modes_map.get(s.id, set())
        if mode is not None and mode.value not in mapped_modes:
            continue
        s_chunks = chunks_by_section.get(s.id, [])
        chunk_items = [
            AdminExportChunkItem(
                chunk_index=c.chunk_index,
                content=c.content,
                embedding_model=c.embedding_model,
                embedding_version=c.embedding_version,
                token_count=c.token_count if c.token_count is not None else int(len(c.content.split()) * 1.3),
                has_embedding=c.embedding is not None
            )
            for c in s_chunks
        ]
        
        section_items.append(
            AdminExportSectionItem(
                section_index=s.section_index,
                title=s.title,
                level=s.level,
                path=s.path,
                page_start=s.page_start,
                page_end=s.page_end,
                modes=[mode.value] if mode is not None else sorted(mapped_modes),
                chunks=chunk_items
            )
        )

    units = list(
        session.exec(
            select(LearningUnit)
            .where(
                LearningUnit.book_id == book_id,
                *([LearningUnit.mode == mode] if mode is not None else []),
            )
            .order_by(LearningUnit.mode.asc(), LearningUnit.unit_index.asc())
        ).all()
    )
    unit_ids = [unit.id for unit in units]
    segments_by_unit: dict[uuid.UUID, list[AdminExportLearningUnitSegmentItem]] = {}
    sources_by_unit: dict[uuid.UUID, list[AdminExportLearningUnitSourceItem]] = {}
    if unit_ids:
        segment_rows = session.exec(
            select(LearningUnitSegment)
            .where(LearningUnitSegment.learning_unit_id.in_(unit_ids))
            .order_by(LearningUnitSegment.learning_unit_id, LearningUnitSegment.segment_index.asc())
        ).all()
        for segment in segment_rows:
            segments_by_unit.setdefault(segment.learning_unit_id, []).append(
                AdminExportLearningUnitSegmentItem(
                    segment_index=segment.segment_index,
                    text_content=segment.text_content,
                    audio_url=segment.audio_url,
                    duration_ms=segment.duration_ms,
                )
            )

        source_rows = session.exec(
            select(LearningUnitSource, BookSection)
            .join(BookSection, BookSection.id == LearningUnitSource.section_id)
            .where(LearningUnitSource.learning_unit_id.in_(unit_ids))
            .order_by(LearningUnitSource.learning_unit_id, LearningUnitSource.source_order.asc())
        ).all()
        for source, section in source_rows:
            sources_by_unit.setdefault(source.learning_unit_id, []).append(
                AdminExportLearningUnitSourceItem(
                    section_index=section.section_index,
                    section_title=section.title,
                    section_path=section.path,
                    page_start=section.page_start,
                    page_end=section.page_end,
                    source_order=source.source_order,
                )
            )

    export_modes = (mode,) if mode is not None else (PlanMode.FULL, PlanMode.PARETO)
    learning_modes: dict[str, AdminExportLearningModeItem] = {
        export_mode.value: AdminExportLearningModeItem(mode=export_mode)
        for export_mode in export_modes
    }
    for unit in units:
        mode_key = unit.mode.value
        learning_modes[mode_key].units.append(
            AdminExportLearningUnitItem(
                unit_index=unit.unit_index,
                title=unit.title,
                unit_type=unit.unit_type,
                status=unit.status.value if hasattr(unit.status, "value") else str(unit.status),
                source_text_char_count=unit.source_text_char_count,
                estimated_tokens=unit.estimated_tokens,
                estimated_audio_seconds=unit.estimated_audio_seconds,
                main_segment_count=unit.main_segment_count,
                planner_reason=unit.planner_reason,
                error_message=unit.error_message,
                review_text=unit.review_text,
                review_audio_url=unit.review_audio_url,
                sources=sources_by_unit.get(unit.id, []),
                segments=segments_by_unit.get(unit.id, []),
            )
        )
    for mode_export in learning_modes.values():
        mode_export.total_units = len(mode_export.units)

    return AdminBookExportResponse(
        selected_mode=mode,
        book_id=book.id,
        title=book.title,
        author=book.author,
        document_type=book.document_type,
        sections=section_items,
        learning_modes=learning_modes,
    )


def get_admin_book_audio_units(session: Session, book_id: uuid.UUID, mode: PlanMode) -> AdminBookAudioUnitsResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    try:
        mode_value = PlanMode(mode)
    except ValueError:
        mode_value = PlanMode.PARETO

    units = session.exec(
        select(LearningUnit)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
        .order_by(LearningUnit.unit_index.asc())
    ).all()

    unit_ids = [u.id for u in units]
    segments_map = {}
    sources_map = {}
    if unit_ids:
        segments = session.exec(
            select(LearningUnitSegment)
            .where(LearningUnitSegment.learning_unit_id.in_(unit_ids))
            .order_by(LearningUnitSegment.learning_unit_id, LearningUnitSegment.segment_index.asc())
        ).all()
        for seg in segments:
            segments_map.setdefault(seg.learning_unit_id, []).append(
                AdminSegmentItem(
                    id=seg.id,
                    segment_index=seg.segment_index,
                    audio_url=seg.audio_url,
                    text_content=seg.text_content,
                    duration_ms=seg.duration_ms,
                )
            )

        source_rows = session.exec(
            select(LearningUnitSource, BookSection)
            .join(BookSection, BookSection.id == LearningUnitSource.section_id)
            .where(LearningUnitSource.learning_unit_id.in_(unit_ids))
            .order_by(LearningUnitSource.learning_unit_id, LearningUnitSource.source_order.asc())
        ).all()
        for source, section in source_rows:
            sources_map.setdefault(source.learning_unit_id, []).append(
                AdminLearningUnitSourceItem(
                    section_id=section.id,
                    section_index=section.section_index,
                    section_title=section.title,
                    section_path=section.path,
                    page_start=section.page_start,
                    page_end=section.page_end,
                    source_order=source.source_order,
                )
            )

    unit_items = [
        AdminLearningUnitItem(
            id=u.id,
            unit_index=u.unit_index,
            title=u.title,
            unit_type=u.unit_type,
            mode=u.mode.value,
            status=u.status.value if hasattr(u.status, 'value') else str(u.status),
            estimated_audio_seconds=u.estimated_audio_seconds,
            main_segment_count=u.main_segment_count,
            review_text=u.review_text,
            review_audio_url=u.review_audio_url,
            planner_reason=u.planner_reason,
            segments=segments_map.get(u.id, []),
            sources=sources_map.get(u.id, []),
        )
        for u in units
    ]

    return AdminBookAudioUnitsResponse(
        book_id=book.id,
        mode=mode_value.value,
        total_units=len(unit_items),
        units=unit_items,
    )


def update_admin_book_metadata(
    session: Session,
    book_id: uuid.UUID,
    payload: AdminBookUpdateMetadataRequest,
    admin_user_id: uuid.UUID,
) -> AdminBookDetailResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    changes = {}
    if payload.title is not None and payload.title.strip() and payload.title.strip() != book.title:
        changes["old_title"] = book.title
        book.title = payload.title.strip()
        changes["new_title"] = book.title

    if payload.author is not None and payload.author.strip() != (book.author or ""):
        changes["old_author"] = book.author
        book.author = payload.author.strip()
        changes["new_author"] = book.author

    if payload.is_shared is not None and payload.is_shared != book.is_shared:
        if book.archived_at is not None:
            raise BookStatusConflictError("Hãy dùng thao tác khôi phục thay vì xuất bản trực tiếp sách đã gỡ.")
        changes["old_is_shared"] = book.is_shared
        book.is_shared = payload.is_shared
        changes["new_is_shared"] = book.is_shared

    if changes:
        session.add(book)
        session.commit()
        session.refresh(book)

        create_admin_audit_log(
            session,
            admin_user_id=admin_user_id,
            action="book.update_metadata",
            target_type="book",
            target_id=book_id,
            metadata=changes,
        )
        session.commit()

    return get_book_detail(session, book_id)


def _get_clone_count(session: Session, book_id: uuid.UUID) -> int:
    return int(session.exec(select(func.count(Book.id)).where(Book.parent_shared_id == book_id)).one() or 0)


def archive_system_book(
    session: Session, book_id: uuid.UUID, admin_user_id: uuid.UUID
) -> AdminBookLifecycleResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()
    if book.parent_shared_id is not None:
        raise BadRequestError("Chỉ có thể gỡ sách hệ thống gốc.")
    if book.archived_at:
        return AdminBookLifecycleResponse(book_id=book.id, clone_count=_get_clone_count(session, book.id), message="Sách đã ở trạng thái đã gỡ.")
    if not book.is_shared:
        raise BookStatusConflictError("Chỉ có thể gỡ sách đang được công khai trong thư viện hệ thống.")

    clone_count = _get_clone_count(session, book.id)
    book.is_shared = False
    book.archived_at = datetime.now(timezone.utc)
    session.add(book)
    create_admin_audit_log(session, admin_user_id=admin_user_id, action="system_book.archive", target_type="book", target_id=book.id, metadata={"clone_count": clone_count})
    session.commit()
    return AdminBookLifecycleResponse(book_id=book.id, clone_count=clone_count, message="Đã gỡ sách khỏi thư viện hệ thống; các bản sao hiện có vẫn dùng được.")


def restore_system_book(
    session: Session, book_id: uuid.UUID, admin_user_id: uuid.UUID
) -> AdminBookLifecycleResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()
    if not book.archived_at:
        raise BookStatusConflictError("Sách này chưa ở trạng thái đã gỡ.")
    if book.parent_shared_id is not None:
        raise BadRequestError("Không thể khôi phục bản sao người dùng vào thư viện hệ thống.")

    book.archived_at = None
    book.is_shared = True
    session.add(book)
    create_admin_audit_log(session, admin_user_id=admin_user_id, action="system_book.restore", target_type="book", target_id=book.id, metadata={})
    session.commit()
    return AdminBookLifecycleResponse(book_id=book.id, clone_count=_get_clone_count(session, book.id), message="Đã khôi phục sách vào thư viện hệ thống.")


def purge_archived_system_book(
    session: Session, book_id: uuid.UUID, admin_user_id: uuid.UUID
) -> AdminBookLifecycleResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()
    if not book.archived_at:
        raise BookStatusConflictError("Chỉ có thể xóa vĩnh viễn sách đã gỡ.")
    clone_count = _get_clone_count(session, book.id)
    if clone_count:
        raise BookStatusConflictError(f"Không thể xóa vĩnh viễn vì còn {clone_count} bản sao người dùng.")

    from app.repositories.audiobook_repo import cleanup_book_side_effects
    from app.tasks.book_tasks import purge_book_storage_assets_task

    cleanup_book_side_effects(session, book_id=book.id, user_id=book.user_id)
    session.delete(book)
    create_admin_audit_log(session, admin_user_id=admin_user_id, action="system_book.purge", target_type="book", target_id=book_id, metadata={})
    session.commit()
    purge_book_storage_assets_task.delay(str(book_id))
    return AdminBookLifecycleResponse(book_id=book_id, clone_count=0, message="Đã xóa vĩnh viễn sách và lên lịch dọn tệp nền.")


def get_admin_book_summary(session: Session, book_id: uuid.UUID) -> AdminBookSummaryResponse:
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    return AdminBookSummaryResponse(
        book_id=book.id,
        status=book.ai_summary_status,
        ai_summary=book.ai_summary,
        error_message=book.ai_summary_error,
    )


def regenerate_admin_book_summary(
    session: Session,
    book_id: uuid.UUID,
    admin_user_id: uuid.UUID,
) -> dict:
    from app.core.constant import SummaryStatus
    book = get_admin_book_by_id(session, book_id)
    if not book:
        raise BookNotFoundError()

    prev_status = book.ai_summary_status
    book.ai_summary_status = SummaryStatus.PENDING.value
    book.ai_summary_error = None
    session.add(book)
    session.commit()

    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="book.regenerate_summary",
        target_type="book",
        target_id=book_id,
        metadata={"previous_status": prev_status},
    )
    session.commit()

    generate_book_summary_task.delay(str(book.id))
    return {
        "message": "Đã gửi yêu cầu tạo lại tóm tắt AI dưới nền.",
        "status": SummaryStatus.PENDING.value,
    }


async def admin_upload_book_async(
    session: Session,
    file: UploadFile,
    admin_user_id: uuid.UUID,
) -> AdminBookUploadResponse:
    import aiofiles
    import os

    filename = file.filename or "uploaded_book.pdf"
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        doc_type = "pdf"
    elif filename_lower.endswith(".epub"):
        doc_type = "epub"
    elif filename_lower.endswith(".docx"):
        doc_type = "docx"
    else:
        raise BadRequestError("Chỉ hỗ trợ upload file PDF, EPUB hoặc DOCX.")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise BadRequestError("Dung lượng file vượt quá giới hạn hệ thống cho phép.")

    book_id = uuid.uuid4()
    job_id = uuid.uuid4()

    tmp_filepath = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)

    async with aiofiles.open(tmp_filepath, "wb") as f:
        await f.write(content)

    clean_title = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title()

    book = Book(
        id=book_id,
        user_id=admin_user_id,
        title=clean_title,
        author="Tác giả chưa xác định",
        document_type=doc_type,
        status=BookStatus.PROCESSING.value,
        is_shared=False,
    )
    session.add(book)

    job = ProcessingJob(
        id=job_id,
        user_id=admin_user_id,
        book_id=book_id,
        job_type=ProcessingJobType.UPLOAD,
        status=ProcessingJobStatus.QUEUED,
        progress_percent=0,
        current_step="Đang đưa tài liệu vào hàng đợi xử lý ngầm...",
    )
    session.add(job)
    session.commit()
    session.refresh(book)
    session.refresh(job)

    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="book.admin_upload",
        target_type="book",
        target_id=book_id,
        metadata={"filename": filename, "job_id": str(job.id)},
    )
    session.commit()

    from app.tasks.book_tasks import admin_ingest_book_task
    try:
        admin_ingest_book_task.apply_async(
            args=[str(book_id), str(job.id), tmp_filepath, doc_type, filename],
            task_id=str(job.id),
            queue="document",
        )
    except Exception as exc:
        log.warning(f"Could not enqueue Celery ingest task for job {job.id}: {exc}")

    return AdminBookUploadResponse(
        book_id=book.id,
        job_id=job.id,
        message="Upload sách thành công. Tiến trình bóc tách và tạo vector đang chạy ngầm.",
    )


def cancel_and_rollback_admin_job(
    session: Session,
    job_id: uuid.UUID,
    admin_user_id: uuid.UUID,
) -> AdminCancelJobResponse:
    from app.core.celery_app import celery_app
    from app.models.db_models import LearningUnitSegment, LearningUnitSource

    job = session.get(ProcessingJob, job_id)
    if not job:
        raise ProcessingJobNotFoundError()

    if job.status in [ProcessingJobStatus.READY, ProcessingJobStatus.COMPLETED, ProcessingJobStatus.CANCELLED]:
        raise ProcessingJobStatusConflictError("Tiến trình đã hoàn thành hoặc đã bị hủy trước đó.")

    # 1. Celery Revoke Task (fire-and-forget in background thread to prevent blocking HTTP endpoint)
    def _revoke_celery_task_bg():
        try:
            celery_app.control.revoke(str(job.id))
        except Exception as exc:
            log.warning(f"Could not revoke Celery task {job.id}: {exc}")

    import threading
    threading.Thread(target=_revoke_celery_task_bg, daemon=True).start()

    target_book_id = job.book_id

    # 2. Clean Rollback Dữ liệu Rác
    if target_book_id:
        # Delete BookSectionKnowledge
        knowledges = session.exec(select(BookSectionKnowledge).where(BookSectionKnowledge.book_id == target_book_id)).all()
        for k in knowledges:
            session.delete(k)

        # Delete LearningUnits, Segments & LearningUnitSource associations
        units = session.exec(select(LearningUnit).where(LearningUnit.book_id == target_book_id)).all()
        u_ids = [u.id for u in units]
        if u_ids:
            segs = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id.in_(u_ids))).all()
            for s in segs:
                session.delete(s)
            unit_sources = session.exec(select(LearningUnitSource).where(LearningUnitSource.learning_unit_id.in_(u_ids))).all()
            for us in unit_sources:
                session.delete(us)
            for u in units:
                session.delete(u)

        # Delete BookSections
        sections = session.exec(select(BookSection).where(BookSection.book_id == target_book_id)).all()
        for sec in sections:
            session.delete(sec)

        # Delete Book if it was an Upload job; otherwise set status to CANCELLED
        book = session.get(Book, target_book_id)
        if book:
            if job.job_type == ProcessingJobType.UPLOAD:
                job.book_id = None
                session.add(job)
                session.flush()
                session.delete(book)
            else:
                book.status = BookStatus.CANCELLED
                book.error_message = "Tiến trình đã bị Admin hủy."
                session.add(book)

    job.status = ProcessingJobStatus.CANCELLED
    job.error_message = "Tiến trình đã bị Admin hủy và dọn dẹp sạch dữ liệu (Clean Rollback)."
    session.add(job)
    session.commit()

    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="job.cancel_and_rollback",
        target_type="job",
        target_id=job.id,
        metadata={"book_id": str(target_book_id) if target_book_id else None},
    )
    session.commit()

    return AdminCancelJobResponse(
        job_id=job.id,
        status="cancelled",
        message="Đã hủy tiến trình thành công và dọn dẹp toàn bộ dữ liệu rác!",
        rolled_back=True,
    )

