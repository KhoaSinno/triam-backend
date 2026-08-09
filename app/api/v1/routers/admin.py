import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlmodel import Session

from app.api.dependencies.admin import AdminUserDependency
from app.api.dependencies.auth import CurrentUser
from app.core.constant import BookStatus, DocumentType, PlanMode, ProcessingJobStatus, ProcessingJobType, PlanMode 
from app.db.database import get_session
from app.models.db_models import Book
from app.schemas.admin import (
    AdminAuditLogsResponse,
    AdminBookDetailResponse,
    AdminBooksResponse,
    AdminDashboardResponse,
    AdminJobsResponse,
    AdminMeResponse,
    AdminRetryJobResponse,
    AdminUsersResponse,
    AdminBookSectionListItem,
    AdminBookSectionDetailResponse,
    AdminJobListItem,
    AdminBookExportResponse,
    AdminBookAudioUnitsResponse,
    AdminBookUpdateMetadataRequest,
    AdminBookSummaryResponse,
    AdminBookUploadResponse,
    AdminCancelJobResponse,
    AdminUserDirectNotifyPayload,
    AdminUserDirectNotifyResponse,
    AdminUserStatsResponse,
    AdminUserStatusUpdatePayload,
    AdminUserStatusUpdateResponse,
)
from app.schemas.responses import BookResponse
from app.services import admin_service

router = APIRouter(prefix="/admin")


LimitQuery = Annotated[int, Query(ge=1, le=100)]
OffsetQuery = Annotated[int, Query(ge=0)]


@router.get("/me", response_model=AdminMeResponse)
def read_admin_me(current_user: CurrentUser, admin_user: AdminUserDependency):
    return admin_service.get_admin_profile(current_user, admin_user)


@router.get("/dashboard", response_model=AdminDashboardResponse)
def read_admin_dashboard(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_dashboard(session)


@router.get("/users", response_model=AdminUsersResponse)
def read_admin_users(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
):
    return admin_service.get_users(session, limit=limit, offset=offset, user_id=admin_user.user_id)


@router.patch("/users/{user_id}/status", response_model=AdminUserStatusUpdateResponse)
def update_admin_user_status(
    user_id: uuid.UUID,
    payload: AdminUserStatusUpdatePayload,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.update_admin_user_status(
        session,
        target_user_id=user_id,
        is_active=payload.is_active,
        ban_reason=payload.ban_reason,
        admin_user_id=admin_user.user_id,
    )


@router.post("/users/{user_id}/notify", response_model=AdminUserDirectNotifyResponse)
def send_admin_user_notification(
    user_id: uuid.UUID,
    payload: AdminUserDirectNotifyPayload,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.send_admin_user_direct_notification(
        session,
        target_user_id=user_id,
        payload=payload,
        admin_user_id=admin_user.user_id,
    )


@router.get("/users/{user_id}/stats", response_model=AdminUserStatsResponse)
def read_admin_user_stats(
    user_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_admin_user_learning_stats(session, target_user_id=user_id)


@router.get("/books", response_model=AdminBooksResponse)
def read_admin_books(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    status: BookStatus | None = None,
    document_type: DocumentType | None = None,
    user_id: uuid.UUID | None = None,
    is_shared: bool | None = None,
    q: str | None = Query(default=None, min_length=1, max_length=120),
):
    return admin_service.get_books(
        session,
        limit=limit,
        offset=offset,
        status=status.value if status else None,
        document_type=document_type.value if document_type else None,
        user_id=user_id,
        is_shared=is_shared,
        q=q,
    )


@router.get("/books/{book_id}", response_model=AdminBookDetailResponse)
def read_admin_book_detail(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_book_detail(session, book_id)


@router.get("/books/{book_id}/sections", response_model=list[AdminBookSectionListItem])
def read_admin_book_sections(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_book_sections(session, book_id)


@router.get("/books/{book_id}/sections/{section_id}", response_model=AdminBookSectionDetailResponse)
def read_admin_book_section_detail(
    book_id: uuid.UUID,
    section_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_book_section_detail(session, book_id, section_id)


@router.get("/books/{book_id}/jobs", response_model=list[AdminJobListItem])
def read_admin_book_jobs(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_book_jobs(session, book_id)


@router.get("/books/{book_id}/export-json", response_model=AdminBookExportResponse)
def export_admin_book_json(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.export_book_json(session, book_id)


@router.put("/books/{book_id}", response_model=AdminBookDetailResponse)
def update_admin_book(
    book_id: uuid.UUID,
    payload: AdminBookUpdateMetadataRequest,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.update_admin_book_metadata(session, book_id, payload, admin_user.user_id)


@router.get("/books/{book_id}/audio-units", response_model=AdminBookAudioUnitsResponse)
def read_admin_book_audio_units(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    mode: PlanMode,
):
    return admin_service.get_admin_book_audio_units(session, book_id, mode=mode)


@router.get("/books/{book_id}/summary", response_model=AdminBookSummaryResponse)
def read_admin_book_summary(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_admin_book_summary(session, book_id)


@router.post("/books/{book_id}/summary/regenerate")
def regenerate_admin_book_summary(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.regenerate_admin_book_summary(session, book_id, admin_user.user_id)


@router.get("/jobs", response_model=AdminJobsResponse)
def read_admin_jobs(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    status: ProcessingJobStatus | None = None,
    job_type: ProcessingJobType | None = None,
    user_id: uuid.UUID | None = None,
    book_id: uuid.UUID | None = None,
):
    return admin_service.get_jobs(
        session,
        limit=limit,
        offset=offset,
        status=status,
        job_type=job_type,
        user_id=user_id,
        book_id=book_id,
    )


@router.post("/books/upload", response_model=AdminBookUploadResponse)
async def admin_upload_book(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    file: UploadFile = File(...),
):
    """
    Upload sách mới dành riêng cho Admin (Hệ thống/Shared Library).
    Trả về ngay HTTP 202 trong < 300ms và đẩy tiến trình bóc tách/vector ngầm.
    """
    return await admin_service.admin_upload_book_async(session, file=file, admin_user_id=admin_user.user_id)


@router.get("/jobs/{job_id}", response_model=AdminJobListItem)
def read_admin_job_by_id(
    job_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    """
    Đọc chi tiết tiến trình ngầm theo Job ID phục vụ Polling Widget góc màn hình Admin.
    """
    from app.repositories.processing_job_repo import get_processing_job_by_id
    from app.core.exceptions import ProcessingJobNotFoundError
    job = get_processing_job_by_id(session, job_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return AdminJobListItem.model_validate(job)


@router.post("/jobs/{job_id}/cancel", response_model=AdminCancelJobResponse)
def cancel_admin_job(
    job_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    """
    Hủy đột ngột tiến trình ngầm Celery và thực thi Clean Rollback dọn dẹp toàn bộ dữ liệu rác.
    """
    return admin_service.cancel_and_rollback_admin_job(session, job_id=job_id, admin_user_id=admin_user.user_id)


@router.post("/jobs/{job_id}/retry", response_model=AdminRetryJobResponse)
def retry_admin_job(
    job_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.retry_job(session, admin_user_id=admin_user.user_id, job_id=job_id)


@router.get("/audit-logs", response_model=AdminAuditLogsResponse)
def read_admin_audit_logs(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    action: str | None = Query(default=None, min_length=1, max_length=120),
    admin_user_id: uuid.UUID | None = None,
):
    return admin_service.get_audit_logs(
        session,
        limit=limit,
        offset=offset,
        action=action,
        admin_user_id=admin_user_id,
    )


@router.patch("/books/{book_id}/share", response_model=BookResponse)
def make_book_shared(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    share: bool = Query(default=True, description="Đặt trạng thái chia sẻ (True = Chia sẻ, False = Hủy chia sẻ)")
):
    """
    Đánh dấu hoặc hủy đánh dấu một cuốn sách mẫu thành sách dùng chung trong thư viện hệ thống.
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách mẫu.")
    
    if share and book.status not in ("ready", "partial_ready"):
        raise HTTPException(status_code=400, detail="Chỉ có thể chia sẻ sách đã hoàn thành xử lý dữ liệu (READY hoặc PARTIAL_READY).")

    book.is_shared = share
    session.add(book)
    session.commit()
    session.refresh(book)
    return book



@router.post("/books/{book_id}/process", response_model=AdminRetryJobResponse)
async def process_admin_book(
    book_id: uuid.UUID,
    mode: PlanMode,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    is_shared: bool = Query(default=False, description="Tự động công khai sách lên thư viện ngay khi xử lý hoàn tất"),
):
    """
    Kích hoạt tiến trình sinh audio + vector RAG cho sách mẫu của Admin.
    Hoàn toàn bỏ qua việc tạo ReadingPlan và schedule slots cá nhân.
    """
    return await admin_service.start_admin_book_processing(session, book_id=book_id, mode=mode.value, admin_user_id=admin_user.user_id, is_shared=is_shared)
