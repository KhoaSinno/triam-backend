import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select, func

from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BadRequestError, BookNotFoundError, BookStatusConflictError, ExternalServiceError, ProcessingJobNotFoundError, ProcessingJobStatusConflictError
from app.models.db_models import AdminAuditLog, AdminUser, Book, LearningUnit, ProcessingJob, BookSection, BookSectionKnowledge
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
from app.schemas.admin import (
    AdminAuditLogItem,
    AdminAuditLogsResponse,
    AdminBookDetailResponse,
    AdminBookListItem,
    AdminBooksResponse,
    AdminDashboardResponse,
    AdminJobListItem,
    AdminJobsResponse,
    AdminMeResponse,
    AdminRetryJobResponse,
    AdminUsersResponse,
    AdminBookOwnerInfo,
    AdminBookSectionListItem,
    AdminSectionChunkItem,
    AdminBookSectionDetailResponse,
    AdminBookExportResponse,
    AdminExportSectionItem,
    AdminExportChunkItem,
)
from app.schemas.user import UserTokenPayload
from app.services.upload_service import _planned_units_for_book
from app.tasks.book_tasks import process_book_task, switch_mode_task
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
        has_full_mode="full" in book_modes,
        has_pareto_mode="pareto" in book_modes,
        created_at=book.created_at,
        updated_at=book.updated_at,
        latest_job=AdminJobListItem.model_validate(latest_job) if latest_job else None,
        learning_units_by_status=count_learning_units_by_status(session, book_id),
        segment_count=count_learning_unit_segments_for_book(session, book_id),
        owner_info=owner_info,
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
    process_book_task.apply_async(
        args=[str(book_id), requested_mode.value, str(job.id)],
        queue="document",
    )

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
        for s_id, mode in rows:
            section_modes_map.setdefault(s_id, set()).add(mode.value)

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


def export_book_json(session: Session, book_id: uuid.UUID) -> AdminBookExportResponse:
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
        for s_id, mode in rows:
            section_modes_map.setdefault(s_id, set()).add(mode.value)

    section_items = []
    for s in sections:
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
                modes=list(section_modes_map.get(s.id, set())),
                chunks=chunk_items
            )
        )

    return AdminBookExportResponse(
        book_id=book.id,
        title=book.title,
        author=book.author,
        document_type=book.document_type,
        sections=section_items
    )

