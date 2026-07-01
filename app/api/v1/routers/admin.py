import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.api.dependencies.admin import AdminUserDependency
from app.api.dependencies.auth import CurrentUser
from app.core.constant import BookStatus, DocumentType, PlanMode, ProcessingJobStatus, ProcessingJobType
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


@router.get("/books", response_model=AdminBooksResponse)
def read_admin_books(
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    status: BookStatus | None = None,
    document_type: DocumentType | None = None,
    user_id: uuid.UUID | None = None,
    q: str | None = Query(default=None, min_length=1, max_length=120),
):
    return admin_service.get_books(
        session,
        limit=limit,
        offset=offset,
        status=status.value if status else None,
        document_type=document_type.value if document_type else None,
        user_id=user_id,
        q=q,
    )


@router.get("/books/{book_id}", response_model=AdminBookDetailResponse)
def read_admin_book_detail(
    book_id: uuid.UUID,
    admin_user: AdminUserDependency,
    session: Annotated[Session, Depends(get_session)],
):
    return admin_service.get_book_detail(session, book_id)


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
    is_shared: bool = Query(default=True, description="Tự động công khai sách lên thư viện ngay khi xử lý hoàn tất"),
):
    """
    Kích hoạt tiến trình sinh audio + vector RAG cho sách mẫu của Admin.
    Hoàn toàn bỏ qua việc tạo ReadingPlan và schedule slots cá nhân.
    """
    return await admin_service.start_admin_book_processing(session, book_id=book_id, mode=mode.value, admin_user_id=admin_user.user_id, is_shared=is_shared)
