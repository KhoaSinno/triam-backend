# Project Export

## Project Statistics

- Total files: 174

## Folder Structure

```
Makefile
start.sh
app
  api
    dependencies
      admin.py
      auth.py
    v1
      routers
        admin.py
        audiobooks.py
        health.py
        jobs.py
        learning_progress.py
        live.py
        notifications.py
        reading_plan_sessions.py
        reviews.py
        study_context.py
        threads.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    celery_app.py
    config.py
    constant.py
    exceptions.py
    logger.py
    security.py
    stopwords.py
    supabase.py
    __init__.py
  db
    database.py
    migrations
      env.py
      README
      script.py.mako
      versions
        054450a4d3fc_added_new_logic_context_conversation_.py
        0899ce396ec2_add_fcm_device_tokens.py
        1a04ac7f0a85_add_mode_to_chapter_segments.py
        2b7c9d1e4f6a_admin_users_and_audit_logs.py
        2f6b7c8d9e01_phase_11_learning_completion_state.py
        34b51c319023_optimize_all_db_schema_add_plan_table.py
        78b35db4eddb_add_server_default_to_created_at_and_.py
        7a12b34c56d8_phase_12_calendar_reading_plan_sessions.py
        7c1f860609e9_added_error_message_to_book.py
        8b34c56d7e90_phase_12_allow_session_regeneration_history.py
        8c31c9cd4c1f_add_reminder_time_to_reading_plans.py
        91b0326bdf19_added_directbookcontext_to_update_logic_.py
        951590abaacf_hotfix_book_ref.py
        960bf5ca365d_udpate_cascade_role.py
        9c45d67e8f01_phase_12_allow_session_unit_regeneration.py
        a13f1e2d3c4b_phase_13_calendar_session_actions.py
        a2c9e7f1b5d0_phase_5_document_structure_learning_units.py
        b14a05b2dfeb_add_shared_book_columns_and_clone_.py
        b14c2d3e4f50_phase_14_drop_legacy_book_knowledge.py
        b8e4f2a7c9d1_add_document_type_and_unique_constraints.py
        c15d3e4f5061_phase_14_1_clean_reading_plan_schedule_config.py
        c4f0a9d8e2b1_add_processing_jobs.py
        c5d6e7f8a901_phase_6_cleanup_legacy_chapter_schema.py
        d16e5f607182_phase_14_4_read_path_indexes.py
        d7a2f4c9b8e1_phase_3_generation_guardrails.py
        e4f7a9c2d1b0_phase_4_1_in_app_notifications.py
        f0a1b2c3d4e5_phase_10_2_book_section_knowledge.py
        f1b2c3d4e5f6_phase_10_3_hybrid_retrieval.py
        f6a8c2d4e9b1_phase_4_2_learning_progress.py
  main.py
  models
    db_models.py
  repositories
    admin_repo.py
    agent_grounding_repo.py
    audiobook_repo.py
    book_learning_state_repo.py
    book_read_repo.py
    book_section_knowledge_repo.py
    book_section_repo.py
    learning_progress_repo.py
    learning_unit_repo.py
    notification_outbox_repo.py
    notification_settings_repo.py
    processing_job_repo.py
    reading_plan_repo.py
    reading_plan_schedule_repo.py
    reading_plan_session_repo.py
    spaced_review_repo.py
    study_context_document_link_repo.py
    study_context_repo.py
    study_context_thread_repo.py
    user_notification_repo.py
  schemas
    admin.py
    audiobook.py
    learning_progress.py
    notification.py
    plan.py
    processing_job.py
    responses
      audiobook_res.py
      study_context_res.py
      __init__.py
    review.py
    study_context.py
    user.py
  services
    admin_service.py
    agent_grounding
      contracts.py
      grounding_router.py
      hybrid_retrieval.py
      intent_router.py
      query_normalizer.py
      reranker.py
      response_renderer.py
      section_context_builder.py
      section_reference_parser.py
      section_resolver.py
      __init__.py
    agent_observability
      contracts.py
      llm_as_a_judge.py
      model_eval_report.py
      turn_trace.py
      __init__.py
    agent_policy
      contracts.py
      renderers.py
      shared_policy.py
      __init__.py
    agent_voice_gpt_realtime.py
    async_limiter.py
    audiobook_service.py
    book_section_chunker.py
    book_section_knowledge_indexer.py
    chapter_chunking_service.py
    document_parser_service.py
    document_structure_service.py
    document_structure_types.py
    docx_service.py
    epub_service.py
    fcm_service.py
    health_service.py
    learning_progress_service.py
    learning_unit_planner_service.py
    live_service.py
    llm_service.py
    notification_copy_service.py
    notification_event_service.py
    notification_service.py
    pareto_planner_service.py
    pareto_signal_service.py
    pdf_service.py
    processing_job_service.py
    rag_service.py
    reading_plan_schedule_service.py
    reading_plan_session_service.py
    reminder_schedule_service.py
    review_service.py
    spaced_review_service.py
    storage_service.py
    study_context_service.py
    token_budget_service.py
    tts_script_quality_service.py
    tts_service.py
    upload_service.py
    voice_agent
      contracts.py
      query_guard.py
      rag_context.py
      tool_reply_watchdog.py
      transcription_prompt.py
      transcript_store.py
      turn_state.py
      voice_intent_classifier.py
      web_permission_intent_classifier.py
      web_permission_policy.py
      __init__.py
    web_search_service.py
    workers
      book_pipeline.py
      learning_unit_tts_worker.py
      learning_unit_worker.py
      __init__.py
    __init__.py
  tasks
    book_tasks.py
    notification_tasks.py
    __init__.py
  __init__.py
pyproject.toml

```

### Makefile

```makefile
login_get_AT: 
	uv run python -m scripts.auth_script_test_supabase.test_login

get_supabase_user: 
	uv run python -m scripts.auth_script_test_supabase.test_supabase_sdk

clean: 
	./clean.sh

gat:
	uv run python scripts/get_supabase_access_token.py

t1:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

t2:
	uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo --concurrency 1

t3:
	uv run celery -A app.core.celery_app.celery_app worker -Q notification,maintenance -l info --pool=solo --concurrency 1

t4:
	uv run celery -A app.core.celery_app.celery_app beat -l info

t5:
	uv run python -m app.services.agent_voice_gpt_realtime start

t5c:
	uv run python -m app.services.agent_voice_gpt_realtime console
```

### start.sh

```sh
#!/usr/bin/env bash
set -e

export PYTHONUNBUFFERED=1
export UV_NO_SYNC="${UV_NO_SYNC:-1}"

# Giới hạn luồng tính toán cho PyTorch/MKL/OpenMP trên CPU basic HF Spaces.
# Mặc định PyTorch sẽ cố dùng hết tất cả cores vật lý của máy chủ ảo hóa,
# gây thrashing trên container 2 vCPU và làm container treo khi khởi động.
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export TORCH_NUM_THREADS=1

# Gọi binary trực tiếp từ .venv (nhanh hơn uv run, tránh lock contention khi
# nhiều tiến trình khởi động đồng thời). .venv được tạo bởi Dockerfile (uv sync).
PYTHON_BIN="./.venv/bin/python"
CELERY_BIN="./.venv/bin/celery"
ALEMBIC_BIN="./.venv/bin/alembic"
UVICORN_BIN="./.venv/bin/uvicorn"

if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
  echo "Running Alembic migrations..."
  "$ALEMBIC_BIN" upgrade head
fi

if [ "${ENABLE_VOICE_AGENT:-true}" = "true" ]; then
  AGENT_MODE="${AGENT_MODE:-start}"
  echo "Starting realtime voice agent (mode=$AGENT_MODE)..."
  "$PYTHON_BIN" -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" 2>&1 | tee worker.log &
else
  echo "Skipping realtime voice agent (ENABLE_VOICE_AGENT=false)"
fi

if [ "${ENABLE_CELERY_WORKER:-false}" = "true" ]; then
  echo "Starting Celery document worker..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app worker \
    -Q document \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_DOCUMENT_CONCURRENCY:-1}" \
    2>&1 | tee celery_document.log &
else
  echo "Skipping Celery document worker (ENABLE_CELERY_WORKER=false)"
fi

if [ "${ENABLE_NOTIFICATION_WORKER:-false}" = "true" ]; then
  echo "Starting Celery notification worker..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app worker \
    -Q notification,maintenance \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_NOTIFICATION_CONCURRENCY:-1}" \
    2>&1 | tee celery_notification.log &
else
  echo "Skipping Celery notification worker (ENABLE_NOTIFICATION_WORKER=false)"
fi

if [ "${ENABLE_CELERY_BEAT:-false}" = "true" ]; then
  echo "Starting Celery Beat..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app beat \
    -l "${CELERY_LOG_LEVEL:-info}" \
    2>&1 | tee celery_beat.log &
else
  echo "Skipping Celery Beat (ENABLE_CELERY_BEAT=false)"
fi

BACKEND_PORT="${BACKEND_PORT:-7860}"
UVICORN_RELOAD="${UVICORN_RELOAD:-false}"

if [ "$UVICORN_RELOAD" = "true" ]; then
  echo "Starting FastAPI with reload on port ${BACKEND_PORT}..."
  exec "$UVICORN_BIN" app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
else
  echo "Starting FastAPI on port ${BACKEND_PORT}..."
  exec "$UVICORN_BIN" app.main:app --host 0.0.0.0 --port "$BACKEND_PORT"
fi

```

### app\api\dependencies\admin.py

```py
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.models.db_models import AdminUser
from app.repositories.admin_repo import get_active_admin_user


def require_admin_user(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]) -> AdminUser:
    admin_user = get_active_admin_user(session, current_user.sub)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required.",
        )
    return admin_user


AdminUserDependency = Annotated[AdminUser, Depends(require_admin_user)]

```

### app\api\dependencies\auth.py

```py
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.supabase import supabase
from app.schemas.user import UserTokenPayload

security = HTTPBearer()


def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> UserTokenPayload:
    """
    Dependency lấy và verify JWT token từ Header sử dụng Supabase Python SDK.
    Dùng Depends(get_current_user) trong mọi endpoint cần bảo mật.
    """
    token = credentials.credentials
    try:
        # Sử dụng SDK chính thức của Supabase để kiểm tra auth qua server
        # Phương pháp này hỗ trợ chuẩn Asymmetric Keys mới nhất (ES256/RS256) một cách mượt mà nhất.
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ hoặc đã hết hạn.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = user_response.user

        return UserTokenPayload(
            sub=UUID(str(user.id)),
            email=user.email,
            role=user.role,
            aud=user.aud,
        )

    except HTTPException:
        raise
    except Exception:
        # Bắt mọi lỗi decode, hết hạn auth hoặc token rác
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


CurrentUser = Annotated[UserTokenPayload, Depends(get_current_user)]

```

### app\api\v1\routers\admin.py

```py
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
    AdminBookSectionListItem,
    AdminBookSectionDetailResponse,
    AdminJobListItem,
    AdminBookExportResponse,
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

```

### app\api\v1\routers\audiobooks.py

```py
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.models.db_models import Book
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.schemas.plan import (
    PlanUpdateRequest,
    ReadingPlanResponse,
    ReadingPlanSessionListResponse,
    ReadingPlanUpdateResponse,
    ReadingPlanUserSlotResponse,
    SwitchModeRequest,
)
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.services.audiobook_service import (
    create_new_book,
    delete_book_and_assets,
    get_book,
    get_book_details,
    get_book_learning_units,
    get_book_outline,
    get_reading_plan,
    list_books,
    list_reading_plan_slots,
    list_shared_library,
    pause_reading_plan,
    reset_reading_plan,
    resume_reading_plan,
    select_shared_book_to_user,
    switch_book_mode,
    update_book_by_id,
    update_reading_plan,
)
from app.services.reading_plan_session_service import list_book_reading_plan_sessions, list_today_reading_plan_sessions

router = APIRouter()


@router.get("/books", response_model=list[BookResponse])
def read_all_books(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return list_books(session, current_user.sub)


@router.get("/books/library", response_model=list[BookResponse])
def read_shared_library(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    """
    Lấy danh sách sách mẫu được chia sẻ công khai từ Thư viện Hệ thống.
    """
    return list_shared_library(session)


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book(session, book_id, current_user.sub)


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)], mode: str | None = None):
    return get_book_details(session, book_id, current_user.sub, mode=mode)


@router.get("/books/{book_id}/outline")
def get_book_outline_endpoint(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_outline(session, book_id, current_user.sub)


@router.get("/books/{book_id}/learning-units")
def get_book_learning_units_endpoint(book_id: uuid.UUID, mode: str, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_learning_units(session, book_id, current_user.sub, mode)


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
async def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return await switch_book_mode(session, book_id, current_user.sub, payload.mode)


@router.post("/books", response_model=BookResponse)
def add_new_book(payload: BookCreateRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return create_new_book(session, current_user.sub, payload)


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: uuid.UUID, payload: BookUpdateRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return update_book_by_id(session, payload, book_id, current_user.sub)


# Delete book by id, including all associated assets in storage and database records
@router.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    await delete_book_and_assets(session, book_id, current_user.sub)
    return {"message": "Book deleted"}


# READING PLAN
@router.post("/books/{book_id}/pause")
def pause_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Tạm dừng kế hoạch học tập của sách và giải phóng lịch học."""
    return pause_reading_plan(session, book_id, current_user.sub)


@router.post("/books/{book_id}/resume")
def resume_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Tiếp tục kế hoạch học tập của sách (kiểm tra trùng lịch các slot)."""
    return resume_reading_plan(session, book_id, current_user.sub)


@router.get("/reading-plan-slots", response_model=list[ReadingPlanUserSlotResponse])
def get_active_plan_slots(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Lấy toàn bộ slot lịch học active của user để FE tránh chọn trùng khi tạo/sửa plan."""
    return list_reading_plan_slots(session, current_user.sub)


@router.get("/books/{book_id}/reading-plan", response_model=ReadingPlanResponse)
def get_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Lấy cấu hình lịch học hiện tại của sách để FE prefill màn hình chỉnh lịch."""
    return get_reading_plan(session, book_id, current_user.sub)


@router.get("/books/{book_id}/reading-plan/sessions", response_model=ReadingPlanSessionListResponse)
def get_book_plan_sessions(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    mode: str | None = None,
):
    """Lấy các buổi học cụ thể đã được sinh từ ReadingPlan của sách."""
    return list_book_reading_plan_sessions(session, user_id=current_user.sub, book_id=book_id, mode=mode)


@router.get("/reading-plan/sessions/today", response_model=ReadingPlanSessionListResponse)
def get_today_plan_sessions(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    local_date: date | None = None,
):
    """Lấy lịch học của user trong ngày cục bộ để FE hiển thị trang hôm nay."""
    return list_today_reading_plan_sessions(session, user_id=current_user.sub, local_date=local_date)


@router.put("/books/{book_id}/reading-plan", response_model=ReadingPlanUpdateResponse)
def update_plan(
    book_id: uuid.UUID,
    payload: PlanUpdateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Cập nhật cấu hình kế hoạch học tập (pace, schedule, reminder_time) không ảnh hưởng tới audio."""
    return update_reading_plan(
        session,
        book_id,
        current_user.sub,
        pace=payload.pace,
        schedule_config=payload.schedule_config,
        reminder_time=payload.reminder_time,
    )


@router.post("/books/{shared_book_id}/select", response_model=BookResponse)
def select_book_from_library(shared_book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    """
    User chọn một cuốn sách từ thư viện dùng chung.
    Backend thực hiện nhân bản nhanh toàn bộ cấu trúc để có thể bắt đầu học ngay lập tức.
    """
    try:
        cloned_book = select_shared_book_to_user(session, shared_book_id=shared_book_id, user_id=current_user.sub)
        
        # Query modes associated with the cloned learning units to populate has_full_mode/has_pareto_mode
        from app.models.db_models import LearningUnit
        rows = session.exec(
            select(LearningUnit.mode)
            .where(LearningUnit.book_id == cloned_book.id)
            .group_by(LearningUnit.mode)
        ).all()
        book_modes = {mode.value for mode in rows}
        
        book_data = cloned_book.model_dump()
        return {
            **book_data,
            "learning_status": "not_started",
            "book_progress_percent": 0,
            "has_full_mode": "full" in book_modes,
            "has_pareto_mode": "pareto" in book_modes,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/books/{book_id}/reset", response_model=ReadingPlanResponse)
def reset_plan(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """
    Đặt lại kế hoạch học tập của cuốn sách từ đầu.
    Xóa sạch tiến độ học tập cũ của user và sinh lại các buổi học từ bài 1.
    """
    return reset_reading_plan(session, book_id, current_user.sub)

```

### app\api\v1\routers\health.py

```py
from typing import Any

from fastapi import APIRouter

from app.services.health_service import get_background_health

router = APIRouter()


@router.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok", "service": "triam-backend"}


@router.get("/health/background")
def read_background_health() -> dict[str, Any]:
    return get_background_health()

```

### app\api\v1\routers\jobs.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.processing_job import ProcessingJobSummaryResponse
from app.services.processing_job_service import get_book_processing_status, get_job_status

router = APIRouter()


@router.get("/jobs/{job_id}", response_model=ProcessingJobSummaryResponse)
def read_job_status(job_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_job_status(session, current_user.sub, job_id)


@router.get("/books/{book_id}/processing-status", response_model=ProcessingJobSummaryResponse)
def read_book_processing_status(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_book_processing_status(session, current_user.sub, book_id)

```

### app\api\v1\routers\learning_progress.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    LearningUnitProgressResponse,
    LearningUnitProgressUpdateRequest,
    ManualLearningUnitCompleteRequest,
)
from app.services.learning_progress_service import complete_learning_unit_manually, get_book_learning_progress, update_learning_unit_progress

router = APIRouter()


@router.put("/books/{book_id}/learning-units/{learning_unit_id}/progress", response_model=LearningUnitProgressResponse)
def update_learning_unit_progress_endpoint(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: LearningUnitProgressUpdateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return update_learning_unit_progress(session, user_id=current_user.sub, book_id=book_id, learning_unit_id=learning_unit_id, payload=payload)


@router.post("/books/{book_id}/learning-units/{learning_unit_id}/complete", response_model=LearningUnitProgressResponse)
def complete_learning_unit_endpoint(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: ManualLearningUnitCompleteRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return complete_learning_unit_manually(session, user_id=current_user.sub, book_id=book_id, learning_unit_id=learning_unit_id, mode=payload.mode)


@router.get("/books/{book_id}/learning-progress", response_model=BookLearningProgressResponse)
def get_book_learning_progress_endpoint(
    book_id: uuid.UUID,
    mode: str,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return get_book_learning_progress(session, user_id=current_user.sub, book_id=book_id, mode=mode)

```

### app\api\v1\routers\live.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.services.live_service import get_token_for_book, get_token_for_thread

router = APIRouter()


@router.get("/live-token/{book_id}")
async def get_token(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_token_for_book(session, book_id, current_user.sub)


@router.get("/live-token/thread/{thread_id}")
async def get_token_thread(thread_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_token_for_thread(session, thread_id, current_user.sub)

```

### app\api\v1\routers\notifications.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.notification import (
    DeviceTokenRegisterRequest,
    DeviceTokenResponse,
    MarkAllNotificationsReadResponse,
    MarkNotificationReadResponse,
    NotificationListResponse,
    NotificationSettingsRequest,
    NotificationSettingsResponse,
)
from app.services.fcm_service import register_user_device_token, unregister_user_device_token
from app.services.notification_service import get_settings, list_notifications, read_all_notifications, read_notification, update_settings

router = APIRouter()


@router.get("/notifications", response_model=NotificationListResponse)
def get_notifications(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    unread_only: bool = False,
):
    return list_notifications(session, current_user.sub, limit=limit, unread_only=unread_only)


@router.patch("/notifications/read-all", response_model=MarkAllNotificationsReadResponse)
def mark_all_read(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return read_all_notifications(session, current_user.sub)


@router.patch("/notifications/{notification_id}/read", response_model=MarkNotificationReadResponse)
def mark_notification_read(notification_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return read_notification(session, current_user.sub, notification_id)


@router.get("/notifications/settings", response_model=NotificationSettingsResponse)
def get_notification_settings(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_settings(session, current_user.sub)


@router.put("/notifications/settings", response_model=NotificationSettingsResponse)
def update_notification_settings(payload: NotificationSettingsRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return update_settings(session, current_user.sub, payload)


@router.post("/notifications/devices", response_model=DeviceTokenResponse, status_code=201)
def register_device(
    payload: DeviceTokenRegisterRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return register_user_device_token(session, current_user.sub, payload.device_token)


@router.delete("/notifications/devices/{device_token}")
def unregister_device(
    device_token: str,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    success = unregister_user_device_token(session, current_user.sub, device_token)
    return {"status": "success" if success else "not_found"}

```

### app\api\v1\routers\reading_plan_sessions.py

```py
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.plan import (
    ReadingPlanSessionActionResponse,
    ReadingPlanSessionRangeResponse,
    ReadingPlanSessionRescheduleRequest,
    ReadingPlanSessionSkipRequest,
)
from app.services.reading_plan_session_service import (
    list_reading_plan_sessions_range,
    reschedule_reading_plan_session,
    skip_reading_plan_session,
)

router = APIRouter()


@router.get("/reading-plan/sessions", response_model=ReadingPlanSessionRangeResponse)
def get_reading_plan_sessions(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    from_date: date | None = None,
    to_date: date | None = None,
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    status: str | None = None,
):
    """Lấy lịch học theo khoảng ngày để FE vẽ calendar tuần/tháng."""
    return list_reading_plan_sessions_range(
        session,
        user_id=current_user.sub,
        from_date=from_date,
        to_date=to_date,
        book_id=book_id,
        mode=mode,
        status=status,
    )


@router.post("/reading-plan/sessions/{session_id}/skip", response_model=ReadingPlanSessionActionResponse)
def skip_plan_session(
    session_id: uuid.UUID,
    payload: ReadingPlanSessionSkipRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Bỏ qua một buổi học mà không đánh dấu learning progress là completed."""
    return skip_reading_plan_session(
        session,
        user_id=current_user.sub,
        session_id=session_id,
        reason=payload.reason,
    )


@router.put("/reading-plan/sessions/{session_id}/schedule", response_model=ReadingPlanSessionActionResponse)
def reschedule_plan_session(
    session_id: uuid.UUID,
    payload: ReadingPlanSessionRescheduleRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Dời lịch một buổi học cụ thể, giữ nguyên các learning units trong buổi đó."""
    return reschedule_reading_plan_session(
        session,
        user_id=current_user.sub,
        session_id=session_id,
        local_date=payload.local_date,
        reminder_time=payload.reminder_time,
        timezone_name=payload.timezone,
    )

```

### app\api\v1\routers\reviews.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.review import ReviewActionResponse, ReviewItemResponse, ReviewListResponse
from app.services.review_service import complete_review_item, get_review_item_detail, list_review_items, skip_review_item

router = APIRouter()


@router.get("/reviews", response_model=ReviewListResponse)
def list_reviews_endpoint(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    status: str = Query(default="due"),
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_review_items(
        session,
        user_id=current_user.sub,
        status=status,
        book_id=book_id,
        mode=mode,
        limit=limit,
        offset=offset,
    )


@router.get("/books/{book_id}/reviews", response_model=ReviewListResponse)
def list_book_reviews_endpoint(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    status: str = Query(default="due"),
    mode: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return list_review_items(
        session,
        user_id=current_user.sub,
        status=status,
        book_id=book_id,
        mode=mode,
        limit=limit,
        offset=offset,
    )


@router.get("/reviews/{review_item_id}", response_model=ReviewItemResponse)
def get_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_review_item_detail(session, user_id=current_user.sub, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/complete", response_model=ReviewActionResponse)
def complete_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return complete_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)


@router.post("/reviews/{review_item_id}/skip", response_model=ReviewActionResponse)
def skip_review_endpoint(review_item_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return skip_review_item(session, user_id=current_user.sub, review_item_id=review_item_id)

```

### app\api\v1\routers\study_context.py

```py
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.responses import BookResponse, ChatThreadResponse, ContextDocumentResponse, StudyContextResponse
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)
from app.services import study_context_service

router = APIRouter()


# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContextResponse])
async def get_study_contexts_api(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.list_contexts(session, current_user.sub)


@router.get("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def get_study_context_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_context(session, current_user.sub, context_id)


@router.get("/study-contexts/{context_id}/documents", response_model=List[BookResponse])
async def get_study_context_documents_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_documents_in_context(session, current_user.sub, context_id)


@router.post("/study-contexts", response_model=StudyContextResponse)
async def create_study_context_api(payload: StudyContextInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_context(session, current_user.sub, payload)


@router.patch("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.update_context_title(session, current_user.sub, context_id, payload)


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_context(session, current_user.sub, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=ContextDocumentResponse)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.add_document_to_context(session, current_user.sub, context_id, payload)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_document_from_context(session, current_user.sub, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThreadResponse])
async def get_chat_threads_api(context_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_threads_for_context(session, current_user.sub, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThreadResponse)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_thread(session, current_user.sub, context_id, payload)

```

### app\api\v1\routers\threads.py

```py
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.responses import ChatMessageResponse, ChatThreadResponse
from app.schemas.study_context import (
    ChatThreadUpdate,
)
from app.services.study_context_service import (
    delete_thread_by_id,
    get_or_create_thread_for_book,
    get_thread_messages,
    update_thread_by_id,
)

router = APIRouter()

# Get all threads for a context


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessageResponse])
async def get_thread_messages_api(thread_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_thread_messages(session, current_user.sub, thread_id)


# Get or create thread for a book


@router.get("/threads/for-book/{book_id}")
async def get_thread_for_book(book_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_or_create_thread_for_book(session, user_id=current_user.sub, book_id=book_id, title="New Book Chat")


# Update current thread by thread_id


@router.put("/threads/{thread_id}", response_model=ChatThreadResponse)
async def update_thread_api(thread_id: uuid.UUID, payload: ChatThreadUpdate, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return update_thread_by_id(session, current_user.sub, thread_id, payload.title)


@router.delete("/threads/{thread_id}")
async def delete_thread_api(thread_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    delete_thread_by_id(session, current_user.sub, thread_id)
    return {"message": "Thread deleted successfully"}

```

### app\api\v1\routers\upload.py

```py
from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, UploadFile
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.plan import PlanInput
from app.services.upload_service import handle_generate_plan, handle_upload_document

router = APIRouter()


# -----------------------------------------------------------------------
# ENDPOINT 1: POST /upload
# -----------------------------------------------------------------------
@router.post("/upload")
async def upload_document(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile, File(...)],
):
    """
    Bước 1: Nhận file, extract outline, upload tài liệu lên Supabase Storage,
    lưu Book + BookSection tree, trả về outline cho Flutter.
    """
    return await handle_upload_document(session, file, current_user.sub)


# -----------------------------------------------------------------------
# ENDPOINT 2: POST /generate-plan
# -----------------------------------------------------------------------
@router.post("/generate-plan")
async def generate_plan(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
):
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    return await handle_generate_plan(session, payload, current_user.sub)

```

### app\api\v1\routers\__init__.py

```py
# API Endpoints module

```

### app\api\v1\__init__.py

```py
# API v1 module

```

### app\api\__init__.py

```py
# API v1 module

```

### app\core\celery_app.py

```py
from celery import Celery
from celery.schedules import schedule

from app.core.config import settings

celery_app = Celery(
    "triam",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND or None,
    include=["app.tasks.book_tasks", "app.tasks.notification_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_ignore_result=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,
    broker_pool_limit=settings.CELERY_BROKER_POOL_LIMIT,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    worker_cancel_long_running_tasks_on_connection_loss=settings.CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS,
    broker_connection_retry_on_startup=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    broker_transport_options={
        "visibility_timeout": settings.CELERY_VISIBILITY_TIMEOUT_SECONDS,
        "socket_keepalive": True,
        "health_check_interval": 30,
    },
    task_routes={
        "triam.books.process": {"queue": "document"},
        "triam.books.switch_mode": {"queue": "document"},
        "triam.books.index_sections": {"queue": "document"},
        "triam.notifications.scan_due": {"queue": "maintenance"},
        "triam.notifications.deliver_due": {"queue": "notification"},
    },
    beat_schedule={
        "scan-due-notifications": {
            "task": "triam.notifications.scan_due",
            "schedule": schedule(run_every=settings.NOTIFICATION_SCAN_INTERVAL_SECONDS),
            "options": {"queue": "maintenance"},
        }
    },
)

```

### app\core\config.py

```py
from typing import Set

from dotenv import load_dotenv
from pydantic.v1.env_settings import BaseSettings

load_dotenv(override=True)

import os

if "SPACE_ID" not in os.environ and os.environ.get("RUNNING_ON_HF_SPACES") != "true":
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")



class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    GEMINI_BASE_URL: str
    GEMINI_API_KEY: str
    DATABASE_URL: str
    # hardening DB pool/config
    DATABASE_ECHO: bool = False
    DATABASE_POOL_MODE: str = "auto"
    DATABASE_POOL_SIZE: int = 3
    DATABASE_MAX_OVERFLOW: int = 2
    DATABASE_POOL_TIMEOUT: int = 5
    DATABASE_POOL_RECYCLE: int = 900
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_USE_LIFO: bool = True
    DATABASE_APPLICATION_NAME: str = "triam-backend"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # TTS
    EDGE_TTS_VOICE: str = "en-US-AvaMultilingualNeural"
    TTS_PROVIDER: str = "edge"
    TTS_RECEIVE_TIMEOUT_SECONDS: int = 300
    TTS_RETRY_BASE_SECONDS: int = 3
    TTS_MIN_TEXT_CHARS: int = 10
    TTS_GOOGLE_API_KEY: str | None = None
    GOOGLE_TTS_LANGUAGE_CODE: str = "vi-VN"
    GOOGLE_TTS_VOICE: str = "vi-VN-Chirp3-HD-Iapetus"
    GOOGLE_TTS_MAX_BYTES_PER_REQUEST: int = 4500
    GOOGLE_TTS_ENABLE_COST_LOG: bool = True
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_AGENT_NAME: str
    LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS: int = 60
    LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS: int = 20
    LIVEKIT_AGENT_EMPTY_ROOM_GRACE_SECONDS: float = 8.0
    GEMINI_MODEL_LLM: str = "gemini-2.5-flash"

    # Realtime voice agent behavior
    OPENAI_STREAM_MODEL_NAME: str = "gpt-realtime-mini"
    OPENAI_REALTIME_VOICE: str = "cedar"
    # Text and local console test behavior
    VOICE_AGENT_HISTORY_LIMIT: int = 24
    VOICE_AGENT_RAG_MAX_CHARS: int = 12000
    # Local console fallback only. Production LiveKit rooms must provide
    # thread_id and document_ids through job metadata from the backend token flow.
    VOICE_AGENT_CONSOLE_BOOK_ID: str = "c3f13d07-4494-4995-ba75-30a12589b8fc"
    VOICE_AGENT_CONSOLE_THREAD_ID: str = "07be00b9-c6da-4801-8ba2-7558205b92b2"

    # Dynamic Prompt cho OpenAI Realtime Transcription
    OPENAI_REALTIME_TRANSCRIPTION_MODEL: str = "gpt-4o-transcribe"
    OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE: str = "vi"
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT: str = "Vietnamese audio in the TRIAM audiobook study app. Expect terms: Tri Âm, chương, sách, định lý, phương pháp, GPT, Gemini."
    OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS: int = 900
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS: int = 45
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS: int = 20
    OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION: str = "near_field"

    VOICE_AGENT_TEXT_LLM_MODEL: str = "gpt-4o-mini"
    VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT: bool = True
    VOICE_AGENT_LOG_TRANSCRIPT_TEXT: bool = True
    VOICE_AGENT_DEDUPE_WINDOW_SECONDS: int = 3
    VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS: int = 180
    # Policy websearch
    VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS: int = 20
    VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS: int = 120
    VOICE_AGENT_PERMISSION_CLASSIFIER_ENABLED: bool = True
    VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL: str = "gpt-4o-mini"
    VOICE_AGENT_PERMISSION_CLASSIFIER_TIMEOUT_SECONDS: float = 5.0
    VOICE_AGENT_PERMISSION_CLASSIFIER_CONFIDENCE_THRESHOLD: float = 0.72
    VOICE_AGENT_QUERY_GUARD_ENABLED: bool = True
    VOICE_AGENT_QUERY_GUARD_MIN_CHARS: int = 6
    VOICE_AGENT_QUERY_GUARD_MIN_TOKENS: int = 2
    VOICE_AGENT_QUERY_GUARD_TRANSCRIPT_TTL_SECONDS: float = 15.0
    VOICE_AGENT_QUERY_GUARD_LOG_DETAILS: bool = True
    VOICE_AGENT_CLARIFICATION_STATE_ENABLED: bool = True
    VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS: float = 30.0
    VOICE_AGENT_CLARIFICATION_CONFIRMATION_MAX_TOKENS: int = 4
    VOICE_AGENT_CLARIFICATION_MIN_QUERY_PROMPT_OVERLAP: float = 0.45
    VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED: bool = False
    VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS: float = 0.8
    VOICE_AGENT_INTERRUPTION_MIN_WORDS: int = 2
    VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS: float = 1.5
    VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED: bool = False

    # Phase 10.11 Voice Tool Reply Watchdog config
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED: bool = True
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS: float = 4.0
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS: float = 8.0
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_TOOLS: str = "search_book_knowledge,ask_web_search_permission,execute_web_search"
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS: bool = False
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE: bool = True

    AGENT_MODEL_PROFILE: str = "baseline"
    AGENT_TRACE_ENABLED: bool = True
    AGENT_TRACE_SCORE_PRECISION: int = 4
    AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS: float = 15.0
    AGENT_GROUNDING_ROUTER_ENABLED: bool = True
    AGENT_SHARED_POLICY_ENABLED: bool = True
    AGENT_INTENT_CLASSIFIER_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    AGENT_INTENT_CLASSIFIER_THRESHOLD: float = 0.60
    AGENT_SECTION_CONTEXT_MAX_CHARS: int = 24000

    AGENT_HYBRID_MIN_FINAL_SCORE: float = 0.25
    AGENT_HYBRID_LEXICAL_CANDIDATES: int = 20
    AGENT_HYBRID_MAX_CONTEXT_CHUNKS: int = 12
    AGENT_HYBRID_MAX_CHUNKS_PER_SECTION: int = 2
    AGENT_HYBRID_VALIDATE_EVIDENCE_ENABLED: bool = False
    # Reranker
    COHERE_API_KEY: str | None = None
    AGENT_RERANKER_ENABLED: bool = True
    AGENT_RERANKER_MODEL: str = "rerank-multilingual-v3.0"
    AGENT_RERANKER_TOP_N: int = 12  # Maximum cadidates Reranker reuturn
    AGENT_RERANKER_CANDIDATES_LIMIT: int = 20  # Maximum cadidates sent to Cohere
    # Upload file
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES: Set[str] = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    LOG_LEVEL: str = "INFO"
    LOG_THIRD_PARTY_LEVEL: str = "WARNING"

    # Celery / Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str | None = None
    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_EAGER_PROPAGATES: bool = False
    CELERY_BROKER_POOL_LIMIT: int = 1
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
    CELERY_DOCUMENT_CONCURRENCY: int = 1
    CELERY_NOTIFICATION_CONCURRENCY: int = 1
    CELERY_LOG_LEVEL: str = "info"
    CELERY_VISIBILITY_TIMEOUT_SECONDS: int = 3600
    CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS: bool = False
    ENABLE_CELERY_WORKER: bool = False
    ENABLE_NOTIFICATION_WORKER: bool = False
    ENABLE_CELERY_BEAT: bool = False

    # Runtime process toggles
    ENABLE_VOICE_AGENT: bool = True
    RUN_MIGRATIONS_ON_START: bool = False
    UVICORN_RELOAD: bool = False
    UV_NO_SYNC: bool = False

    # LiveKit agent runtime hardening
    LIVEKIT_AGENT_JOB_EXECUTOR_TYPE: str = "thread"
    LIVEKIT_AGENT_NUM_IDLE_PROCESSES: int = 1
    LIVEKIT_AGENT_MAX_CONCURRENT_JOBS: int = 2
    LIVEKIT_AGENT_LOAD_THRESHOLD: float = 0.95
    LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT: float = 60.0
    LIVEKIT_AGENT_SHUTDOWN_PROCESS_TIMEOUT: float = 20.0

    # Generation guardrails
    LLM_INPUT_SOFT_TOKEN_LIMIT: int = 12000
    LLM_INPUT_HARD_TOKEN_LIMIT: int = 60000
    LLM_CHUNK_TARGET_TOKENS: int = 5000
    LLM_CHUNK_OVERLAP_TOKENS: int = 300
    MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK: int = 4 * 60 * 60
    FIRST_PLAYABLE_UNITS: int = 1

    # Provider concurrency
    LEARNING_UNIT_PROCESSING_CONCURRENCY: int = 2
    LLM_NORMALIZE_CONCURRENCY: int = 1
    TTS_GENERATION_CONCURRENCY: int = 8
    BOOK_SECTION_INDEXING_ENABLED: bool = True
    BOOK_SECTION_EMBEDDING_MODEL: str = "text-embedding-3-small"
    BOOK_SECTION_EMBEDDING_VERSION: str = "section-v1"
    BOOK_SECTION_CHUNK_SIZE_CHARS: int = 3600
    BOOK_SECTION_CHUNK_OVERLAP_CHARS: int = 500
    BOOK_SECTION_EMBEDDING_BATCH_SIZE: int = 64
    BOOK_SECTION_RAG_MATCH_THRESHOLD: float = 0.3
    BOOK_SECTION_RAG_MATCH_COUNT: int = 10

    # Pareto learning unit planner
    PARETO_PLANNER_MODEL: str = "gemini-3.5-flash"
    PARETO_PLANNER_TIMEOUT_SECONDS: float = 90.0
    PARETO_PLANNER_MAX_UNITS: int = 8
    PARETO_PLANNER_MIN_UNITS: int = 3
    PARETO_TARGET_COVERAGE_RATIO: float = 0.25
    PARETO_SECTION_EXCERPT_CHARS: int = 1400
    PARETO_PLANNER_MAX_SECTION_CARDS: int = 120

    # Phase 4.1 notification/reminder workflow
    NOTIFICATION_SCAN_INTERVAL_SECONDS: int = 60
    NOTIFICATION_DELIVERY_BATCH_SIZE: int = 50
    NOTIFICATION_MAX_ATTEMPTS: int = 5
    NOTIFICATION_STALE_LOCK_MINUTES: int = 10
    NOTIFICATION_DEFAULT_TIMEZONE: str = "Asia/Ho_Chi_Minh"
    NOTIFICATION_DEFAULT_REMINDER_TIME: str = "20:00"
    NOTIFICATION_DEFAULT_DAILY_CAP: int = 3
    NOTIFICATION_DEFAULT_QUIET_START: str = "22:00"
    NOTIFICATION_DEFAULT_QUIET_END: str = "07:00"

    # Firebase Cloud Messaging
    FIREBASE_CREDENTIALS_JSON: str | None = None
    FIREBASE_CREDENTIALS_FILE: str | None = None

    # Phase 4.2 production learning loop
    MAX_ACTIVE_LEARNING_BOOKS_PER_USER: int = 7
    LEARNING_COMPLETION_THRESHOLD_PERCENT: int = 80
    LEARNING_PROGRESS_MIN_DELTA_PERCENT: int = 5
    LEARNING_PROGRESS_STALE_SECONDS: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

```

### app\core\constant.py

```py
from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    ERROR = "error"


class BookStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PARTIAL_READY = "partial_ready"
    READY = "ready"
    ERROR = "error"


class DocumentType(str, Enum):
    PDF = "pdf"
    EPUB = "epub"
    DOCX = "docx"


class PlanMode(str, Enum):
    FULL = "full"
    PARETO = "pareto"


class ProcessingJobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    PARTIAL_READY = "partial_ready"
    READY = "ready"
    ERROR = "error"
    CANCELLED = "cancelled"


class ProcessingJobType(str, Enum):
    UPLOAD = "upload"
    GENERATE_PLAN = "generate_plan"
    SWITCH_MODE = "switch_mode"
    NOTIFICATION = "notification"
    REVIEW = "review"


class NotificationType(str, Enum):
    PLAN_REMINDER = "plan_reminder"
    CONTENT_READY = "content_ready"
    SPACED_REVIEW_DUE = "spaced_review_due"


class NotificationChannel(str, Enum):
    IN_APP = "in_app"
    PUSH = "push"
    ALL = "all"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class ReviewItemStatus(str, Enum):
    PENDING = "pending"
    DUE = "due"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class LearningProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class BookLearningStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ReviewAction(str, Enum):
    COMPLETE = "complete"
    SKIP = "skip"


class ReadingPlanSessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    DUE = "due"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class ReadingPlanSessionUnitStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

```

### app\core\exceptions.py

```py
"""Domain exceptions raised by service/repository layers and rendered by FastAPI handlers."""


class AppException(Exception):
    """Base class cho tất cả domain exceptions của ứng dụng."""

    status_code: int = 500
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


# ---------------------------------------------------------------------------
# 404 Not Found
# ---------------------------------------------------------------------------


class BookNotFoundError(AppException):
    status_code = 404
    detail = "Book not found."


class ReadingPlanNotFoundError(AppException):
    status_code = 404
    detail = "Chưa có ReadingPlan cho sách này."


class ReadingPlanSessionNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy buổi học."


class NoReadingPlanError(AppException):
    """Book tồn tại nhưng user chưa có reading plan."""

    status_code = 400
    detail = "User has no reading plan for this book."


class StudyContextNotFoundError(AppException):
    status_code = 404
    detail = "Study context not found."


class ThreadNotFoundError(AppException):
    status_code = 404
    detail = "Thread not found."


class ProcessingJobNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy tiến trình xử lý."


class NotificationNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy thông báo."


class ReviewItemNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy mục ôn tập."


# ---------------------------------------------------------------------------
# 400 Bad Request
# ---------------------------------------------------------------------------


class BadRequestError(AppException):
    status_code = 400
    detail = "Yêu cầu không hợp lệ."


class AuthTokenInvalidError(AppException):
    status_code = 401
    detail = "Token không hợp lệ hoặc đã hết hạn."


class UnsupportedFileTypeError(AppException):
    status_code = 400
    detail = "Loại file không hỗ trợ. Chỉ chấp nhận PDF, EPUB, DOCX."


class FileTooLargeError(AppException):
    status_code = 400
    detail = "File vượt quá giới hạn 50MB."


# ---------------------------------------------------------------------------
# 409 Conflict
# ---------------------------------------------------------------------------


class BookStatusConflictError(AppException):
    status_code = 409
    detail = "Sách đang ở trạng thái không hợp lệ để thực hiện thao tác này."


class DirectBookContextConflictError(AppException):
    status_code = 409
    detail = "Direct Book Context đã được tạo đồng thời. Vui lòng thử lại."


class ReadingPlanScheduleConflictError(AppException):
    status_code = 409
    detail = "Lịch học này đang trùng với một sách khác. Hãy chọn ngày hoặc giờ khác."


class ReadingPlanSessionStatusConflictError(AppException):
    status_code = 409
    detail = "Buổi học đang ở trạng thái không thể thực hiện thao tác này."


class ProcessingJobStatusConflictError(AppException):
    status_code = 409
    detail = "Job không ở trạng thái có thể retry."


class ActiveLearningBookLimitExceededError(AppException):
    status_code = 409
    detail = "Bạn đã đạt giới hạn số sách đang học. Hãy hoàn thành hoặc tạm dừng một sách trước."


# ---------------------------------------------------------------------------
# 422 Unprocessable Entity
# ---------------------------------------------------------------------------


class DocumentExtractionError(AppException):
    status_code = 422
    detail = "Không thể trích xuất nội dung từ file. File có thể bị lỗi, là scan ảnh, hoặc không có text."


class PdfExtractionError(DocumentExtractionError):
    detail = "Không thể trích xuất nội dung từ PDF. File có thể bị lỗi hoặc là scan ảnh."


class DocumentOutlineRequiredError(AppException):
    status_code = 422
    detail = "Tài liệu không có cấu trúc chương hợp lệ. Vui lòng upload PDF có bookmark/outline, EPUB có mục lục, hoặc DOCX có heading."


class DocumentTooLargeError(AppException):
    status_code = 422
    detail = "Tài liệu quá lớn để xử lý tự động. Vui lòng tách tài liệu thành file nhỏ hơn."


class LearningUnitTooLargeError(AppException):
    status_code = 422
    detail = "Một bài học trong tài liệu quá lớn để xử lý. Vui lòng tách nội dung hoặc chọn tài liệu nhỏ hơn."


class TTSInputTooShortError(AppException):
    status_code = 422
    detail = "Nội dung quá ngắn để tạo audio."


class NoPlayableAudioError(AppException):
    status_code = 422
    detail = "Không tạo được audio có thể phát cho nội dung này."


# ---------------------------------------------------------------------------
# 500 Internal Server Error
# ---------------------------------------------------------------------------


class DataIntegrityError(AppException):
    """Dữ liệu trong DB bị corrupt hoặc không nhất quán."""

    status_code = 500
    detail = "Data integrity error."


class DatabaseError(AppException):
    """Lỗi khi thực hiện thao tác ghi vào DB."""

    status_code = 500
    detail = "Database operation failed."


class ExternalServiceError(AppException):
    """Lỗi khi gọi dịch vụ bên ngoài."""

    status_code = 502
    detail = "External service operation failed."


class LLMResponseFormatError(ExternalServiceError):
    detail = "LLM trả về dữ liệu không đúng định dạng yêu cầu."


class StorageOperationError(ExternalServiceError):
    detail = "Storage operation failed."

```

### app\core\logger.py

```py
import logging
import re
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

# Định cấu hình đường dẫn thư mục log
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

SENSITIVE_PATTERNS = (
    re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?Bearer\s+)[^'\",\s}]+"),
    re.compile(r"(?i)(apikey['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(api[_-]?key['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(api[_-]?secret['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(service_role['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(access[_-]?token['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(refresh[_-]?token['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
)

NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "hpack",
    "h11",
    "supabase",
    "postgrest",
    "storage3",
    "gotrue",
)

# Tùy chỉnh format log hiển thị trên console (có màu sắc)
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def _redact_message(message: str) -> str:
    redacted = message
    for pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub(r"\1[REDACTED]", redacted)
    return redacted


def setup_logger():
    # Bỏ cấu hình mặc định
    logger.remove()
    app_log_level = settings.LOG_LEVEL.upper()
    third_party_level = settings.LOG_THIRD_PARTY_LEVEL.upper()

    def redact_filter(record):
        record["message"] = _redact_message(record["message"])
        return True

    # 1. Cấu hình log ra console (cho môi trường dev)
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level=app_log_level,
        colorize=True,
        filter=redact_filter,
        backtrace=False,
        diagnose=False,
    )

    # 2. Cấu hình log ra file văn bản chuẩn (để xem local)
    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        rotation="10 MB",     # Cắt file khi đạt 10MB
        retention="7 days",   # Giữ file trong 7 ngày
        level=app_log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8",
        filter=redact_filter,
        backtrace=False,
        diagnose=False,
    )

    # 3. Cấu hình log dạng JSON (để đẩy lên ELK / Datadog trên Production)
    logger.add(
        LOG_DIR / "app_json_{time:YYYY-MM-DD}.log",
        rotation="50 MB",
        retention="14 days",
        level=app_log_level,
        serialize=True,       # Ghi log dưới dạng JSON chuẩn
        encoding="utf-8",
        filter=redact_filter,
        backtrace=False,
        diagnose=False,
    )

    # 4. Cấu hình log riêng cho phiên chạy console test
    if "console" in sys.argv:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        session_log_dir = LOG_DIR / "agent_eval"
        session_log_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            session_log_dir / f"voice_console_{timestamp}.log",
            level=app_log_level,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            encoding="utf-8",
            filter=redact_filter,
            backtrace=False,
            diagnose=False,
        )

    # Chuyển hướng log từ standard logging của Python sang loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, _redact_message(record.getMessage()))

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # Bắt luôn cả log của Uvicorn và FastAPI nếu chúng chạy độc lập
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.setLevel(app_log_level)
        logging_logger.propagate = False

    for logger_name in NOISY_LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.setLevel(third_party_level)
        logging_logger.propagate = False

    return logger


# Singleton logger instance
log = setup_logger()

```

### app\core\security.py

```py
# Xử lý JWT, Auth (sau này)

```

### app\core\stopwords.py

```py
ENGLISH_STOPWORDS = {
    "a",
    "about",
    "an",
    "and",
    "are",
    "as",
    "at",
    "book",
    "chapter",
    "chapters",
    "content",
    "detail",
    "details",
    "do",
    "does",
    "for",
    "from",
    "give",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "please",
    "section",
    "sections",
    "summary",
    "tell",
    "the",
    "this",
    "to",
    "what",
    "where",
    "who",
    "why",
    "with",
    "you",
}

VIETNAMESE_STOPWORDS = {
    "anh",
    "bai",
    "ban",
    "bao",
    "chuong",
    "co",
    "cua",
    "cuon",
    "de",
    "doc",
    "duoc",
    "gi",
    "hay",
    "hoi",
    "ke",
    "la",
    "lai",
    "minh",
    "muc",
    "nao",
    "nay",
    "noi",
    "phan",
    "quyen",
    "sach",
    "tat",
    "them",
    "thong",
    "tin",
    "toi",
    "tom",
    "trong",
    "ve",
}

STOPWORDS = ENGLISH_STOPWORDS | VIETNAMESE_STOPWORDS

```

### app\core\supabase.py

```py
from dotenv import load_dotenv
from supabase import Client, create_client

from app.core.config import settings

load_dotenv()

url: str = settings.SUPABASE_URL
# Use service role key for backend operations (bypasses RLS)
# Fall back to anon key if service role key is not set
key: str = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

```

### app\core\__init__.py

```py
# Core module

```

### app\db\database.py

```py
from typing import Any, Generator

from dotenv import load_dotenv
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.core.logger import log

load_dotenv()

DATABASE_POOL_MODES = {"auto", "queue", "null"}


def _normalize_pool_mode(pool_mode: str) -> str:
    mode = (pool_mode or "auto").strip().lower()
    if mode not in DATABASE_POOL_MODES:
        allowed = ", ".join(sorted(DATABASE_POOL_MODES))
        raise ValueError(f"DATABASE_POOL_MODE must be one of: {allowed}")
    return mode


def _is_supabase_pooler(database_url: str) -> bool:
    url = make_url(database_url)
    host = (url.host or "").lower()
    return url.port == 6543 or host.endswith(".pooler.supabase.com")


def should_use_null_pool(database_url: str, pool_mode: str = "auto") -> bool:
    mode = _normalize_pool_mode(pool_mode)
    if mode == "null":
        return True
    if mode == "queue":
        return False
    return _is_supabase_pooler(database_url)


def _connect_args_for(database_url: str) -> dict[str, Any]:
    url = make_url(database_url)
    if url.get_backend_name().startswith("postgresql") and settings.DATABASE_APPLICATION_NAME:
        return {"application_name": settings.DATABASE_APPLICATION_NAME}
    return {}


def create_db_engine(database_url: str | None = None, *, pool_mode: str | None = None) -> Engine:
    database_url = database_url or settings.DATABASE_URL
    pool_mode = pool_mode or settings.DATABASE_POOL_MODE
    common_args: dict[str, Any] = {
        "echo": settings.DATABASE_ECHO,
        "connect_args": _connect_args_for(database_url),
        "pool_pre_ping": settings.DATABASE_POOL_PRE_PING,
    }

    if should_use_null_pool(database_url, pool_mode):
        log.info("Database engine configured with NullPool.")
        return create_engine(database_url, poolclass=NullPool, **common_args)

    log.info(
        "Database engine configured with QueuePool "
        f"size={settings.DATABASE_POOL_SIZE}, overflow={settings.DATABASE_MAX_OVERFLOW}."
    )
    return create_engine(
        database_url,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_recycle=settings.DATABASE_POOL_RECYCLE,
        pool_use_lifo=settings.DATABASE_POOL_USE_LIFO,
        **common_args,
    )


engine = create_db_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def dispose_engine() -> None:
    engine.dispose()

```

### app\db\migrations\env.py

```py
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

import app.models.db_models  # noqa: F401
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Import all db models to make sure they are included in SQLModel.metadata

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# Set sqlalchemy.url from our settings dynamically so we don't have to put it in alembic.ini.
# Alembic stores this in ConfigParser, so percent-encoded passwords such as %40
# must escape percent signs to avoid interpolation errors.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(compare_server_default=True,
                      url=url,
                      target_metadata=target_metadata,
                      literal_binds=True,
                      dialect_opts={"paramstyle": "named"},
                      )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(compare_server_default=True,
                          connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

### app\db\migrations\README

*(Unsupported file type)*

### app\db\migrations\script.py.mako

*(Unsupported file type)*

### app\db\migrations\versions\054450a4d3fc_added_new_logic_context_conversation_.py

```py
"""added new logic context conversation, optimized type/relationship

Revision ID: 054450a4d3fc
Revises: 960bf5ca365d
Create Date: 2026-05-05 08:46:18.296083

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '054450a4d3fc'
down_revision: Union[str, Sequence[str], None] = '960bf5ca365d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('study_contexts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('is_auto_generated', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_contexts_user_id'), 'study_contexts', ['user_id'], unique=False)
    op.create_table('chat_threads',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('context_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['context_id'], ['study_contexts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_threads_context_id'), 'chat_threads', ['context_id'], unique=False)
    op.create_table('study_context_document_links',
    sa.Column('context_id', sa.UUID(), nullable=False),
    sa.Column('book_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['context_id'], ['study_contexts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('context_id', 'book_id')
    )
    op.create_index(op.f('ix_study_context_document_links_book_id'), 'study_context_document_links', ['book_id'], unique=False)
    op.create_index(op.f('ix_study_context_document_links_context_id'), 'study_context_document_links', ['context_id'], unique=False)
    op.create_table('chat_messages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('thread_id', sa.UUID(), nullable=True),
    sa.Column('is_user', sa.Boolean(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['thread_id'], ['chat_threads.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_thread_id'), 'chat_messages', ['thread_id'], unique=False)
    op.create_index(op.f('ix_book_knowledge_book_id'), 'book_knowledge', ['book_id'], unique=False)
    op.create_index(op.f('ix_book_knowledge_chapter_id'), 'book_knowledge', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_chapter_segments_chapter_id'), 'chapter_segments', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_chapters_book_id'), 'chapters', ['book_id'], unique=False)
    op.create_index(op.f('ix_reading_plans_book_id'), 'reading_plans', ['book_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reading_plans_book_id'), table_name='reading_plans')
    op.drop_index(op.f('ix_chapters_book_id'), table_name='chapters')
    op.drop_index(op.f('ix_chapter_segments_chapter_id'), table_name='chapter_segments')
    op.drop_index(op.f('ix_book_knowledge_chapter_id'), table_name='book_knowledge')
    op.drop_index(op.f('ix_book_knowledge_book_id'), table_name='book_knowledge')
    op.drop_index(op.f('ix_chat_messages_thread_id'), table_name='chat_messages')
    op.drop_table('chat_messages')
    op.drop_index(op.f('ix_study_context_document_links_context_id'), table_name='study_context_document_links')
    op.drop_index(op.f('ix_study_context_document_links_book_id'), table_name='study_context_document_links')
    op.drop_table('study_context_document_links')
    op.drop_index(op.f('ix_chat_threads_context_id'), table_name='chat_threads')
    op.drop_table('chat_threads')
    op.drop_index(op.f('ix_study_contexts_user_id'), table_name='study_contexts')
    op.drop_table('study_contexts')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\0899ce396ec2_add_fcm_device_tokens.py

```py
"""add_fcm_device_tokens

Revision ID: 0899ce396ec2
Revises: 8c31c9cd4c1f
Create Date: 2026-05-30 07:44:12.139074

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0899ce396ec2'
down_revision: Union[str, Sequence[str], None] = '8c31c9cd4c1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("COMMIT")
    op.execute("ALTER TYPE notificationchannel ADD VALUE IF NOT EXISTS 'push'")
    op.execute("ALTER TYPE notificationchannel ADD VALUE IF NOT EXISTS 'all'")
    op.execute("ALTER TYPE notificationchannel ADD VALUE IF NOT EXISTS 'PUSH'")
    op.execute("ALTER TYPE notificationchannel ADD VALUE IF NOT EXISTS 'ALL'")
    op.create_table('user_device_tokens',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('device_token', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_device_tokens_device_token'), 'user_device_tokens', ['device_token'], unique=True)
    op.create_index(op.f('ix_user_device_tokens_user_id'), 'user_device_tokens', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_device_tokens_user_id'), table_name='user_device_tokens')
    op.drop_index(op.f('ix_user_device_tokens_device_token'), table_name='user_device_tokens')
    op.drop_table('user_device_tokens')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\1a04ac7f0a85_add_mode_to_chapter_segments.py

```py
"""add mode to chapter_segments

Revision ID: 1a04ac7f0a85
Revises: 34b51c319023
Create Date: 2026-04-24 08:38:44.287323

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1a04ac7f0a85'
down_revision: Union[str, Sequence[str], None] = '34b51c319023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chapter_segments', sa.Column('mode', sa.Text(), server_default='full', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapter_segments', 'mode')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\2b7c9d1e4f6a_admin_users_and_audit_logs.py

```py
"""admin users and audit logs

Revision ID: 2b7c9d1e4f6a
Revises: 0899ce396ec2
Create Date: 2026-06-02 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2b7c9d1e4f6a"
down_revision: Union[str, Sequence[str], None] = "0899ce396ec2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "admin_users",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.Text(), server_default="admin", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("revoked_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(op.f("ix_admin_users_is_active"), "admin_users", ["is_active"], unique=False)

    op.create_table(
        "admin_audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("admin_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("target_type", sa.Text(), nullable=True),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_audit_logs_action"), "admin_audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_admin_audit_logs_admin_user_id"), "admin_audit_logs", ["admin_user_id"], unique=False)
    op.create_index(op.f("ix_admin_audit_logs_created_at"), "admin_audit_logs", ["created_at"], unique=False)
    op.create_index(op.f("ix_admin_audit_logs_target_id"), "admin_audit_logs", ["target_id"], unique=False)
    op.create_index(op.f("ix_admin_audit_logs_target_type"), "admin_audit_logs", ["target_type"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_admin_audit_logs_target_type"), table_name="admin_audit_logs")
    op.drop_index(op.f("ix_admin_audit_logs_target_id"), table_name="admin_audit_logs")
    op.drop_index(op.f("ix_admin_audit_logs_created_at"), table_name="admin_audit_logs")
    op.drop_index(op.f("ix_admin_audit_logs_admin_user_id"), table_name="admin_audit_logs")
    op.drop_index(op.f("ix_admin_audit_logs_action"), table_name="admin_audit_logs")
    op.drop_table("admin_audit_logs")
    op.drop_index(op.f("ix_admin_users_is_active"), table_name="admin_users")
    op.drop_table("admin_users")

```

### app\db\migrations\versions\2f6b7c8d9e01_phase_11_learning_completion_state.py

```py
"""phase 11 learning completion state

Revision ID: 2f6b7c8d9e01
Revises: f1b2c3d4e5f6
Create Date: 2026-06-11
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "2f6b7c8d9e01"
down_revision: Union[str, None] = "f1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")

    op.add_column("reading_plans", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("reading_plans", sa.Column("paused_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("reading_plans", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_reading_plans_completed_at", "reading_plans", ["completed_at"])

    op.create_table(
        "book_learning_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", sa.Text(), server_default="not_started", nullable=False),
        sa.Column("book_progress_percent", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("playable_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_learning_unit_id", sa.UUID(), nullable=True),
        sa.Column("last_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=True),
        sa.Column("position_ms", sa.Integer(), server_default="0", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["last_learning_unit_id"], ["learning_units.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["last_segment_id"], ["learning_unit_segments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "book_id", "mode", name="uq_book_learning_state_user_book_mode"),
    )
    op.create_index("ix_book_learning_states_user_id", "book_learning_states", ["user_id"])
    op.create_index("ix_book_learning_states_book_id", "book_learning_states", ["book_id"])
    op.create_index("ix_book_learning_states_mode", "book_learning_states", ["mode"])
    op.create_index("ix_book_learning_states_status", "book_learning_states", ["status"])
    op.create_index("ix_book_learning_states_last_activity_at", "book_learning_states", ["last_activity_at"])
    op.create_index("ix_book_learning_states_completed_at", "book_learning_states", ["completed_at"])
    op.create_index("ix_book_learning_states_user_status", "book_learning_states", ["user_id", "status"])
    op.create_index("ix_book_learning_states_book_mode", "book_learning_states", ["book_id", "mode"])

    op.execute(
        """
        with playable_units as (
            select
                lu.user_id,
                lu.book_id,
                lu.mode,
                lu.id as learning_unit_id
            from learning_units lu
            where exists (
                select 1
                from learning_unit_segments seg
                where seg.learning_unit_id = lu.id
            )
        ),
        latest_progress as (
            select distinct on (lup.user_id, lup.book_id, lup.mode)
                lup.user_id,
                lup.book_id,
                lup.mode,
                lup.learning_unit_id,
                lup.current_segment_id,
                lup.last_segment_index,
                lup.position_ms,
                coalesce(lup.last_activity_at, lup.updated_at) as latest_at
            from learning_unit_progress lup
            order by
                lup.user_id,
                lup.book_id,
                lup.mode,
                coalesce(lup.last_activity_at, lup.updated_at) desc nulls last,
                lup.updated_at desc
        ),
        summary as (
            select
                pu.user_id,
                pu.book_id,
                pu.mode,
                count(*)::int as playable_units,
                count(lup.id) filter (where lup.status = 'COMPLETED')::int as completed_units,
                coalesce(round(avg(coalesce(lup.max_progress_percent, 0)))::int, 0) as book_progress_percent,
                min(lup.started_at) as started_at,
                max(coalesce(lup.last_activity_at, lup.updated_at)) as last_activity_at,
                max(lup.completed_at) as latest_completed_at
            from playable_units pu
            left join learning_unit_progress lup
                on lup.user_id = pu.user_id
                and lup.book_id = pu.book_id
                and lup.mode = pu.mode
                and lup.learning_unit_id = pu.learning_unit_id
            group by pu.user_id, pu.book_id, pu.mode
        )
        insert into book_learning_states (
            id,
            user_id,
            book_id,
            mode,
            status,
            book_progress_percent,
            completed_units,
            playable_units,
            last_learning_unit_id,
            last_segment_id,
            last_segment_index,
            position_ms,
            started_at,
            last_activity_at,
            completed_at
        )
        select
            gen_random_uuid(),
            s.user_id,
            s.book_id,
            s.mode,
            case
                when s.playable_units > 0 and s.completed_units >= s.playable_units then 'completed'
                when s.last_activity_at is not null then 'in_progress'
                else 'not_started'
            end as status,
            s.book_progress_percent,
            s.completed_units,
            s.playable_units,
            lp.learning_unit_id,
            lp.current_segment_id,
            lp.last_segment_index,
            coalesce(lp.position_ms, 0),
            s.started_at,
            s.last_activity_at,
            case
                when s.playable_units > 0 and s.completed_units >= s.playable_units then s.latest_completed_at
                else null
            end as completed_at
        from summary s
        left join latest_progress lp
            on lp.user_id = s.user_id
            and lp.book_id = s.book_id
            and lp.mode = s.mode
        on conflict (user_id, book_id, mode) do nothing;
        """
    )

    op.execute(
        """
        update reading_plans rp
        set
            status = 'completed',
            completed_at = bls.completed_at,
            updated_at = now()
        from book_learning_states bls
        where rp.book_id = bls.book_id
            and rp.mode = bls.mode
            and bls.status = 'completed';
        """
    )

    op.execute(
        """
        delete from reading_plan_schedule_slots slots
        using reading_plans rp
        where slots.plan_id = rp.id
            and rp.status = 'completed';
        """
    )


def downgrade() -> None:
    op.drop_index("ix_book_learning_states_book_mode", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_user_status", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_completed_at", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_last_activity_at", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_status", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_mode", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_book_id", table_name="book_learning_states")
    op.drop_index("ix_book_learning_states_user_id", table_name="book_learning_states")
    op.drop_table("book_learning_states")

    op.drop_index("ix_reading_plans_completed_at", table_name="reading_plans")
    op.drop_column("reading_plans", "completed_at")
    op.drop_column("reading_plans", "paused_at")
    op.drop_column("reading_plans", "started_at")

```

### app\db\migrations\versions\34b51c319023_optimize_all_db_schema_add_plan_table.py

```py
"""optimize all db schema, add plan table

Revision ID: 34b51c319023
Revises: 7c1f860609e9
Create Date: 2026-04-08 15:59:13.882212

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '34b51c319023'
down_revision: Union[str, Sequence[str], None] = '7c1f860609e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reading_plans',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('book_id', sa.Uuid(), nullable=False),
    sa.Column('mode', sa.Text(), nullable=False),
    sa.Column('pace', sa.Integer(), nullable=False),
    sa.Column('schedule_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # 1. Add columns as nullable=True to not break existing rows
    op.add_column('book_knowledge', sa.Column('chapter_id', sa.Uuid(), nullable=True))
    op.add_column('books', sa.Column('user_id', sa.UUID(), nullable=True))

    # Do normal operations
    op.create_foreign_key(None, 'book_knowledge', 'chapters', ['chapter_id'], ['id'])

    # 2. Fix data relationships
    # Xoá các chunk cũ không còn chapter tương ứng để map dữ liệu
    op.execute("""
        DELETE FROM book_knowledge bk
        WHERE NOT EXISTS (
            SELECT 1 FROM chapters c
            WHERE c.book_id = bk.book_id AND c.chapter_index = bk.chapter_index
        )
    """)
    # Ánh xạ chapter_id bằng cách join với thông tin cũ
    op.execute("""
        UPDATE book_knowledge bk
        SET chapter_id = c.id
        FROM chapters c
        WHERE c.book_id = bk.book_id AND c.chapter_index = bk.chapter_index
    """)

    # Cấp một Dummy UUID cho các sách cũ thiếu user_id (tránh lỗi null)
    op.execute("UPDATE books SET user_id = '00000000-0000-0000-0000-000000000000' WHERE user_id IS NULL")

    # 3. Alter các cột thành NOT NULL sau khi đã có dữ liệu hợp lệ
    op.alter_column('book_knowledge', 'chapter_id', nullable=False)
    op.alter_column('books', 'user_id', nullable=False)

    # Clean up operations
    op.drop_column('book_knowledge', 'chapter_index')
    op.add_column('books', sa.Column('file_url', sa.Text(), nullable=True))
    op.create_index(op.f('ix_books_user_id'), 'books', ['user_id'], unique=False)
    op.drop_column('books', 'gcs_pdf_url')
    op.add_column('chapter_segments', sa.Column('duration_ms', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapter_segments', 'duration_ms')
    op.add_column('books', sa.Column('gcs_pdf_url', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_books_user_id'), table_name='books')
    op.drop_column('books', 'file_url')
    op.drop_column('books', 'user_id')
    op.add_column('book_knowledge', sa.Column('chapter_index', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.drop_column('book_knowledge', 'chapter_id')
    op.drop_table('reading_plans')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\78b35db4eddb_add_server_default_to_created_at_and_.py

```py
"""Add server_default to created_at and updated_at

Revision ID: 78b35db4eddb
Revises: 951590abaacf
Create Date: 2026-05-07 13:20:01.447773

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '78b35db4eddb'
down_revision: Union[str, Sequence[str], None] = '951590abaacf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_messages', 'timestamp',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_threads', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_threads', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('reading_plans', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('reading_plans', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('study_contexts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('study_contexts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('study_contexts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('study_contexts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('reading_plans', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('reading_plans', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_threads', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_threads', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_messages', 'timestamp',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    # ### end Alembic commands ###

```

### app\db\migrations\versions\7a12b34c56d8_phase_12_calendar_reading_plan_sessions.py

```py
"""phase 12 calendar reading plan sessions

Revision ID: 7a12b34c56d8
Revises: 2f6b7c8d9e01
Create Date: 2026-06-11
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "7a12b34c56d8"
down_revision: Union[str, None] = "2f6b7c8d9e01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.create_table(
        "reading_plan_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("session_index", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("local_date", sa.Text(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("timezone", sa.Text(), server_default="Asia/Ho_Chi_Minh", nullable=False),
        sa.Column("status", sa.Text(), server_default="scheduled", nullable=False),
        sa.Column("completed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("skipped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("missed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_id", "session_index", name="uq_reading_plan_sessions_plan_index"),
    )
    op.create_index("ix_reading_plan_sessions_user_id", "reading_plan_sessions", ["user_id"])
    op.create_index("ix_reading_plan_sessions_plan_id", "reading_plan_sessions", ["plan_id"])
    op.create_index("ix_reading_plan_sessions_book_id", "reading_plan_sessions", ["book_id"])
    op.create_index("ix_reading_plan_sessions_mode", "reading_plan_sessions", ["mode"])
    op.create_index("ix_reading_plan_sessions_scheduled_at", "reading_plan_sessions", ["scheduled_at"])
    op.create_index("ix_reading_plan_sessions_local_date", "reading_plan_sessions", ["local_date"])
    op.create_index("ix_reading_plan_sessions_status", "reading_plan_sessions", ["status"])
    op.create_index("ix_reading_plan_sessions_completed_at", "reading_plan_sessions", ["completed_at"])
    op.create_index("ix_reading_plan_sessions_user_status", "reading_plan_sessions", ["user_id", "status"])
    op.create_index("ix_reading_plan_sessions_book_mode", "reading_plan_sessions", ["book_id", "mode"])
    op.create_index("ix_reading_plan_sessions_plan_status", "reading_plan_sessions", ["plan_id", "status"])
    op.create_index(
        "uq_reading_plan_sessions_user_scheduled_active",
        "reading_plan_sessions",
        ["user_id", "scheduled_at"],
        unique=True,
        postgresql_where=sa.text("status != 'cancelled'"),
    )

    op.create_table(
        "reading_plan_session_units",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("unit_order", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), server_default="pending", nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["reading_plan_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_id", "learning_unit_id", name="uq_reading_plan_session_units_plan_unit"),
        sa.UniqueConstraint("session_id", "unit_order", name="uq_reading_plan_session_units_session_order"),
    )
    op.create_index("ix_reading_plan_session_units_session_id", "reading_plan_session_units", ["session_id"])
    op.create_index("ix_reading_plan_session_units_plan_id", "reading_plan_session_units", ["plan_id"])
    op.create_index("ix_reading_plan_session_units_book_id", "reading_plan_session_units", ["book_id"])
    op.create_index("ix_reading_plan_session_units_learning_unit_id", "reading_plan_session_units", ["learning_unit_id"])
    op.create_index("ix_reading_plan_session_units_status", "reading_plan_session_units", ["status"])
    op.create_index("ix_reading_plan_session_units_completed_at", "reading_plan_session_units", ["completed_at"])
    op.create_index("ix_reading_plan_session_units_session_status", "reading_plan_session_units", ["session_id", "status"])
    op.create_index("ix_reading_plan_session_units_book_unit", "reading_plan_session_units", ["book_id", "learning_unit_id"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_session_units_book_unit", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_session_status", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_completed_at", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_status", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_learning_unit_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_book_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_plan_id", table_name="reading_plan_session_units")
    op.drop_index("ix_reading_plan_session_units_session_id", table_name="reading_plan_session_units")
    op.drop_table("reading_plan_session_units")

    op.drop_index("uq_reading_plan_sessions_user_scheduled_active", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_plan_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_book_mode", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_user_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_completed_at", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_status", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_local_date", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_scheduled_at", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_mode", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_book_id", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_plan_id", table_name="reading_plan_sessions")
    op.drop_index("ix_reading_plan_sessions_user_id", table_name="reading_plan_sessions")
    op.drop_table("reading_plan_sessions")

```

### app\db\migrations\versions\7c1f860609e9_added_error_message_to_book.py

```py
"""added error_message to book

Revision ID: 7c1f860609e9
Revises:
Create Date: 2026-04-07 22:49:48.167966

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7c1f860609e9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audiobook')
    op.alter_column('book_knowledge', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('book_knowledge', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book_knowledge', 'chunk_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book_knowledge', 'content',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_index(op.f('book_knowledge_embedding_idx'), table_name='book_knowledge', postgresql_ops={'embedding': 'vector_cosine_ops'}, postgresql_using='hnsw')
    op.drop_constraint(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(None, 'book_knowledge', 'books', ['book_id'], ['id'])
    op.add_column('books', sa.Column('error_message', sa.Text(), nullable=True))
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)
    op.alter_column('chapter_segments', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(None, 'chapter_segments', 'chapters', ['chapter_id'], ['id'])
    op.alter_column('chapters', 'book_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapters', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chapters', 'title',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_constraint(op.f('chapters_book_id_fkey'), 'chapters', type_='foreignkey')
    op.create_foreign_key(None, 'chapters', 'books', ['book_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chapters', type_='foreignkey')
    op.create_foreign_key(op.f('chapters_book_id_fkey'), 'chapters', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapters', 'title',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('chapters', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapters', 'book_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint(None, 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.drop_column('books', 'error_message')
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('book_knowledge_embedding_idx'), 'book_knowledge', ['embedding'], unique=False, postgresql_ops={'embedding': 'vector_cosine_ops'}, postgresql_using='hnsw')
    op.alter_column('book_knowledge', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('book_knowledge', 'chunk_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book_knowledge', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book_knowledge', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.create_table('audiobook',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('audiobook_pkey'))
    )
    # ### end Alembic commands ###

```

### app\db\migrations\versions\8b34c56d7e90_phase_12_allow_session_regeneration_history.py

```py
"""phase 12 allow session regeneration history

Revision ID: 8b34c56d7e90
Revises: 7a12b34c56d8
Create Date: 2026-06-11
"""

from typing import Sequence, Union

from alembic import op

revision: str = "8b34c56d7e90"
down_revision: Union[str, None] = "7a12b34c56d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_reading_plan_sessions_plan_index", "reading_plan_sessions", type_="unique")
    op.create_index("ix_reading_plan_sessions_plan_index", "reading_plan_sessions", ["plan_id", "session_index"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_sessions_plan_index", table_name="reading_plan_sessions")
    op.create_unique_constraint(
        "uq_reading_plan_sessions_plan_index",
        "reading_plan_sessions",
        ["plan_id", "session_index"],
    )

```

### app\db\migrations\versions\8c31c9cd4c1f_add_reminder_time_to_reading_plans.py

```py
"""add_reminder_time_to_reading_plans

Revision ID: 8c31c9cd4c1f
Revises: c5d6e7f8a901
Create Date: 2026-05-30 00:04:53.875259

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8c31c9cd4c1f'
down_revision: Union[str, Sequence[str], None] = 'c5d6e7f8a901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading_plans', sa.Column('reminder_time', sa.Text(), server_default='20:00', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reading_plans', 'reminder_time')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\91b0326bdf19_added_directbookcontext_to_update_logic_.py

```py
"""added DirectBookContext to update logic direct book detail discussion

Revision ID: 91b0326bdf19
Revises: 78b35db4eddb
Create Date: 2026-05-15 13:13:09.969012

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '91b0326bdf19'
down_revision: Union[str, Sequence[str], None] = '78b35db4eddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('direct_book_context',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('book_id', sa.UUID(), nullable=False),
    sa.Column('context_id', sa.UUID(), nullable=False),
    sa.Column('primary_thread_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['context_id'], ['study_contexts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['primary_thread_id'], ['chat_threads.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'book_id', name='direct_book_context_pk')
    )
    op.create_index(op.f('ix_direct_book_context_book_id'), 'direct_book_context', ['book_id'], unique=False)
    op.create_index(op.f('ix_direct_book_context_context_id'), 'direct_book_context', ['context_id'], unique=False)
    op.create_index(op.f('ix_direct_book_context_primary_thread_id'), 'direct_book_context', ['primary_thread_id'], unique=False)
    op.create_index(op.f('ix_direct_book_context_user_id'), 'direct_book_context', ['user_id'], unique=False)
    op.alter_column('books', 'id',
               existing_type=sa.UUID(),
               server_default=None,
               existing_nullable=False)
    op.alter_column('books', 'status',
               existing_type=sa.TEXT(),
               server_default=None,
               existing_nullable=True)
    op.alter_column('chapters', 'id',
               existing_type=sa.UUID(),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chapters', 'status',
               existing_type=sa.TEXT(),
               server_default=None,
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chapters', 'status',
               existing_type=sa.TEXT(),
               server_default=sa.text("'processing'::text"),
               existing_nullable=True)
    op.alter_column('chapters', 'id',
               existing_type=sa.UUID(),
               server_default=sa.text('gen_random_uuid()'),
               existing_nullable=False)
    op.alter_column('books', 'status',
               existing_type=sa.TEXT(),
               server_default=sa.text("'pending'::text"),
               existing_nullable=True)
    op.alter_column('books', 'id',
               existing_type=sa.UUID(),
               server_default=sa.text('gen_random_uuid()'),
               existing_nullable=False)
    op.drop_index(op.f('ix_direct_book_context_user_id'), table_name='direct_book_context')
    op.drop_index(op.f('ix_direct_book_context_primary_thread_id'), table_name='direct_book_context')
    op.drop_index(op.f('ix_direct_book_context_context_id'), table_name='direct_book_context')
    op.drop_index(op.f('ix_direct_book_context_book_id'), table_name='direct_book_context')
    op.drop_table('direct_book_context')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\951590abaacf_hotfix_book_ref.py

```py
"""Hotfix: book ref

Revision ID: 951590abaacf
Revises: 054450a4d3fc
Create Date: 2026-05-06 22:08:41.499014

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '951590abaacf'
down_revision: Union[str, Sequence[str], None] = '054450a4d3fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.add_column('books', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE books SET updated_at = NOW()")
    op.alter_column('books', 'updated_at', nullable=False)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    planmode_enum = sa.Enum('FULL', 'PARETO', name='planmode')
    planmode_enum.create(op.get_bind(), checkfirst=True)

    op.execute("UPDATE chapter_segments SET mode = 'PARETO' WHERE UPPER(mode) = 'PARETO_MODE'")
    op.execute("UPDATE chapter_segments SET mode = 'FULL' WHERE UPPER(mode) = 'FULL_MODE'")
    op.execute("UPDATE chapter_segments SET mode = UPPER(mode)")

    op.alter_column('chapter_segments', 'mode', server_default=None)

    op.alter_column('chapter_segments', 'mode',
               existing_type=sa.TEXT(),
               type_=planmode_enum,
               existing_nullable=False,
               postgresql_using='UPPER(mode)::planmode')
    op.alter_column('chat_messages', 'thread_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chat_threads', 'context_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.add_column('reading_plans', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE reading_plans SET updated_at = NOW()")
    op.alter_column('reading_plans', 'updated_at', nullable=False)

    op.execute("UPDATE reading_plans SET mode = 'PARETO' WHERE UPPER(mode) = 'PARETO_MODE'")
    op.execute("UPDATE reading_plans SET mode = 'FULL' WHERE UPPER(mode) = 'FULL_MODE'")
    op.execute("UPDATE reading_plans SET mode = UPPER(mode)")
    op.alter_column('reading_plans', 'mode',
               existing_type=sa.TEXT(),
               type_=planmode_enum,
               existing_nullable=False,
               postgresql_using='UPPER(mode)::planmode')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reading_plans', 'mode',
               existing_type=sa.Enum('FULL', 'PARETO', name='planmode'),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_column('reading_plans', 'updated_at')
    op.alter_column('chat_threads', 'context_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chat_messages', 'thread_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'mode',
               existing_type=sa.Enum('FULL', 'PARETO', name='planmode'),
               type_=sa.TEXT(),
               existing_nullable=False,
               existing_server_default=sa.text("'full'::text"))
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_column('books', 'updated_at')
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###

```

### app\db\migrations\versions\960bf5ca365d_udpate_cascade_role.py

```py
"""udpate CASCADE role

Revision ID: 960bf5ca365d
Revises: 1a04ac7f0a85
Create Date: 2026-04-27 19:58:47.509670

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '960bf5ca365d'
down_revision: Union[str, Sequence[str], None] = '1a04ac7f0a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.drop_constraint(op.f('book_knowledge_chapter_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(None, 'book_knowledge', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'book_knowledge', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(None, 'chapter_segments', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('chapters_book_id_fkey'), 'chapters', type_='foreignkey')
    op.create_foreign_key(None, 'chapters', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('reading_plans_book_id_fkey'), 'reading_plans', type_='foreignkey')
    op.create_foreign_key(None, 'reading_plans', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading_plans', type_='foreignkey')
    op.create_foreign_key(op.f('reading_plans_book_id_fkey'), 'reading_plans', 'books', ['book_id'], ['id'])
    op.drop_constraint(None, 'chapters', type_='foreignkey')
    op.create_foreign_key(op.f('chapters_book_id_fkey'), 'chapters', 'books', ['book_id'], ['id'])
    op.drop_constraint(None, 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', 'chapters', ['chapter_id'], ['id'])
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(op.f('book_knowledge_chapter_id_fkey'), 'book_knowledge', 'chapters', ['chapter_id'], ['id'])
    op.create_foreign_key(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', 'books', ['book_id'], ['id'])
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###

```

### app\db\migrations\versions\9c45d67e8f01_phase_12_allow_session_unit_regeneration.py

```py
"""phase 12 allow session unit regeneration

Revision ID: 9c45d67e8f01
Revises: 8b34c56d7e90
Create Date: 2026-06-11
"""

from typing import Sequence, Union

from alembic import op

revision: str = "9c45d67e8f01"
down_revision: Union[str, None] = "8b34c56d7e90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_reading_plan_session_units_plan_unit", "reading_plan_session_units", type_="unique")
    op.create_index("ix_reading_plan_session_units_plan_unit", "reading_plan_session_units", ["plan_id", "learning_unit_id"])


def downgrade() -> None:
    op.drop_index("ix_reading_plan_session_units_plan_unit", table_name="reading_plan_session_units")
    op.create_unique_constraint(
        "uq_reading_plan_session_units_plan_unit",
        "reading_plan_session_units",
        ["plan_id", "learning_unit_id"],
    )

```

### app\db\migrations\versions\a13f1e2d3c4b_phase_13_calendar_session_actions.py

```py
"""phase 13 calendar session actions

Revision ID: a13f1e2d3c4b
Revises: 9c45d67e8f01
Create Date: 2026-06-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a13f1e2d3c4b"
down_revision: Union[str, None] = "9c45d67e8f01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("reading_plan_sessions", sa.Column("missed_notified_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("reading_plan_sessions", "missed_notified_at")

```

### app\db\migrations\versions\a2c9e7f1b5d0_phase_5_document_structure_learning_units.py

```py
"""phase 5 document structure learning units

Revision ID: a2c9e7f1b5d0
Revises: f6a8c2d4e9b1
Create Date: 2026-05-28
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a2c9e7f1b5d0"
down_revision: Union[str, None] = "f6a8c2d4e9b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)
processing_job_status = postgresql.ENUM(
    "QUEUED",
    "PROCESSING",
    "PARTIAL_READY",
    "READY",
    "ERROR",
    "CANCELLED",
    name="processingjobstatus",
    create_type=False,
)
learning_progress_status = postgresql.ENUM(
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    name="learningprogressstatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.add_column("books", sa.Column("total_sections", sa.Integer(), nullable=True))
    op.add_column("books", sa.Column("total_units", sa.Integer(), nullable=True))

    op.create_table(
        "book_sections",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column("section_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("page_start", sa.Integer(), nullable=True),
        sa.Column("page_end", sa.Integer(), nullable=True),
        sa.Column("source_href", sa.Text(), nullable=True),
        sa.Column("source_anchor", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "path", name="uq_book_sections_book_path"),
        sa.UniqueConstraint("book_id", "section_index", name="uq_book_sections_book_index"),
    )
    op.create_index("ix_book_sections_book_id", "book_sections", ["book_id"])
    op.create_index("ix_book_sections_parent_id", "book_sections", ["parent_id"])

    op.create_table(
        "learning_units",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("unit_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("unit_type", sa.Text(), nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("source_text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_audio_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("main_segment_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("review_audio_url", sa.Text(), nullable=True),
        sa.Column("review_text", sa.Text(), nullable=True),
        sa.Column("planner_reason", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "mode", "unit_index", name="uq_learning_units_book_mode_index"),
    )
    op.create_index("ix_learning_units_book_id", "learning_units", ["book_id"])
    op.create_index("ix_learning_units_mode", "learning_units", ["mode"])
    op.create_index("ix_learning_units_status", "learning_units", ["status"])
    op.create_index("ix_learning_units_user_id", "learning_units", ["user_id"])

    op.create_table(
        "learning_unit_sources",
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("section_id", sa.UUID(), nullable=False),
        sa.Column("source_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("learning_unit_id", "section_id"),
    )

    op.create_table(
        "learning_unit_segments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("learning_unit_id", "segment_index", name="uq_learning_unit_segments_unit_index"),
    )
    op.create_index("ix_learning_unit_segments_learning_unit_id", "learning_unit_segments", ["learning_unit_id"])

    op.create_table(
        "learning_unit_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("learning_unit_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("current_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("position_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("listened_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", learning_progress_status, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["current_segment_id"], ["learning_unit_segments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["learning_unit_id"], ["learning_units.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "learning_unit_id", name="uq_unit_progress_user_unit"),
    )
    op.create_index("ix_learning_unit_progress_book_id", "learning_unit_progress", ["book_id"])
    op.create_index("ix_learning_unit_progress_completed_at", "learning_unit_progress", ["completed_at"])
    op.create_index("ix_learning_unit_progress_last_activity_at", "learning_unit_progress", ["last_activity_at"])
    op.create_index("ix_learning_unit_progress_learning_unit_id", "learning_unit_progress", ["learning_unit_id"])
    op.create_index("ix_learning_unit_progress_status", "learning_unit_progress", ["status"])
    op.create_index("ix_learning_unit_progress_user_id", "learning_unit_progress", ["user_id"])

    op.add_column("book_knowledge", sa.Column("learning_unit_id", sa.UUID(), nullable=True))
    op.alter_column("book_knowledge", "chapter_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key("fk_book_knowledge_learning_unit_id", "book_knowledge", "learning_units", ["learning_unit_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_book_knowledge_learning_unit_id", "book_knowledge", ["learning_unit_id"])
    op.create_unique_constraint("uq_book_knowledge_unit_chunk_index", "book_knowledge", ["learning_unit_id", "chunk_index"])

    op.add_column("spaced_review_items", sa.Column("learning_unit_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_unit_progress_id", sa.UUID(), nullable=True))
    op.alter_column("spaced_review_items", "chapter_id", existing_type=sa.UUID(), nullable=True)
    op.create_foreign_key("fk_spaced_review_items_learning_unit_id", "spaced_review_items", "learning_units", ["learning_unit_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_spaced_review_items_source_unit_progress_id", "spaced_review_items", "learning_unit_progress", ["source_unit_progress_id"], ["id"], ondelete="SET NULL")
    op.create_index("ix_spaced_review_items_learning_unit_id", "spaced_review_items", ["learning_unit_id"])
    op.create_index("ix_spaced_review_items_source_unit_progress_id", "spaced_review_items", ["source_unit_progress_id"])

    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          learning_unit_id uuid,
          chapter_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.learning_unit_id,
            book_knowledge.chapter_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.drop_index("ix_spaced_review_items_source_unit_progress_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_learning_unit_id", table_name="spaced_review_items")
    op.drop_constraint("fk_spaced_review_items_source_unit_progress_id", "spaced_review_items", type_="foreignkey")
    op.drop_constraint("fk_spaced_review_items_learning_unit_id", "spaced_review_items", type_="foreignkey")
    op.alter_column("spaced_review_items", "chapter_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("spaced_review_items", "source_unit_progress_id")
    op.drop_column("spaced_review_items", "learning_unit_id")
    op.drop_constraint("uq_book_knowledge_unit_chunk_index", "book_knowledge", type_="unique")
    op.drop_index("ix_book_knowledge_learning_unit_id", table_name="book_knowledge")
    op.drop_constraint("fk_book_knowledge_learning_unit_id", "book_knowledge", type_="foreignkey")
    op.alter_column("book_knowledge", "chapter_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("book_knowledge", "learning_unit_id")
    op.drop_index("ix_learning_unit_progress_user_id", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_status", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_learning_unit_id", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_last_activity_at", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_completed_at", table_name="learning_unit_progress")
    op.drop_index("ix_learning_unit_progress_book_id", table_name="learning_unit_progress")
    op.drop_table("learning_unit_progress")
    op.drop_index("ix_learning_unit_segments_learning_unit_id", table_name="learning_unit_segments")
    op.drop_table("learning_unit_segments")
    op.drop_table("learning_unit_sources")
    op.drop_index("ix_learning_units_user_id", table_name="learning_units")
    op.drop_index("ix_learning_units_status", table_name="learning_units")
    op.drop_index("ix_learning_units_mode", table_name="learning_units")
    op.drop_index("ix_learning_units_book_id", table_name="learning_units")
    op.drop_table("learning_units")
    op.drop_index("ix_book_sections_parent_id", table_name="book_sections")
    op.drop_index("ix_book_sections_book_id", table_name="book_sections")
    op.drop_table("book_sections")
    op.drop_column("books", "total_units")
    op.drop_column("books", "total_sections")

    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          chapter_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.chapter_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )

```

### app\db\migrations\versions\b14a05b2dfeb_add_shared_book_columns_and_clone_.py

```py
"""add_shared_book_columns_and_clone_function

Revision ID: b14a05b2dfeb
Revises: d16e5f607182
Create Date: 2026-06-25 12:20:21.950633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b14a05b2dfeb'
down_revision: Union[str, Sequence[str], None] = 'd16e5f607182'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Thêm cột mới vào bảng books
    op.add_column('books', sa.Column('is_shared', sa.Boolean(), server_default='false', nullable=False))
    op.create_index(op.f('ix_books_is_shared'), 'books', ['is_shared'], unique=False)
    op.add_column('books', sa.Column('parent_shared_id', sa.UUID(), nullable=True))
    op.create_index(op.f('ix_books_parent_shared_id'), 'books', ['parent_shared_id'], unique=False)
    op.create_foreign_key('fk_books_parent_shared_id', 'books', 'books', ['parent_shared_id'], ['id'], ondelete='SET NULL')

    # 2. Tạo PostgreSQL Stored Function để nhân bản sách (Metadata Cloning)
    op.execute("""
    CREATE OR REPLACE FUNCTION clone_shared_book(
        shared_book_id UUID,
        new_user_id UUID,
        new_book_id UUID
    )
    RETURNS VOID AS $$
    BEGIN
        -- a. Nhân bản bản ghi Book
        INSERT INTO books (
            id, user_id, title, author, file_url, document_type, 
            total_sections, total_units, status, is_shared, parent_shared_id, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, new_user_id, title, author, file_url, document_type, 
            total_sections, total_units, 'ready', false, shared_book_id, 
            now(), now()
        FROM books 
        WHERE id = shared_book_id;

        -- b. Tạo bảng tạm map ID của BookSection cũ sang ID mới
        CREATE TEMP TABLE temp_section_map ON COMMIT DROP AS
        SELECT 
            id AS old_section_id, 
            gen_random_uuid() AS new_section_id
        FROM book_sections 
        WHERE book_id = shared_book_id;

        -- c. Nhân bản các BookSection
        INSERT INTO book_sections (
            id, book_id, parent_id, section_index, title, level, path, 
            text_content, text_char_count, page_start, page_end, source_href, source_anchor, 
            created_at, updated_at
        )
        SELECT 
            m.new_section_id, 
            new_book_id, 
            old_sec.parent_id, -- Tạm thời copy old parent_id
            old_sec.section_index, 
            old_sec.title, 
            old_sec.level, 
            old_sec.path, 
            old_sec.text_content, 
            old_sec.text_char_count, 
            old_sec.page_start, 
            old_sec.page_end, 
            old_sec.source_href, 
            old_sec.source_anchor, 
            now(), 
            now()
        FROM book_sections old_sec
        JOIN temp_section_map m ON old_sec.id = m.old_section_id;

        -- d. Khôi phục cấu trúc cây phân cấp parent_id của BookSection (Dùng cú pháp an toàn tương thích mọi bản Postgres)
        UPDATE book_sections
        SET parent_id = m_parent.new_section_id
        FROM temp_section_map m_child,
             temp_section_map m_parent
        WHERE book_sections.book_id = new_book_id
          AND book_sections.id = m_child.new_section_id
          AND book_sections.parent_id = m_parent.old_section_id;

        -- e. Đặt các parent_id không thuộc cuốn sách về NULL
        UPDATE book_sections
        SET parent_id = NULL
        WHERE book_id = new_book_id
          AND parent_id IS NOT NULL
          AND parent_id NOT IN (SELECT new_section_id FROM temp_section_map);

        -- f. Nhân bản dữ liệu Vector pgvector (BookSectionKnowledge)
        INSERT INTO book_section_knowledge (
            book_id, section_id, chunk_index, content, search_text, content_hash, 
            embedding_model, embedding_version, char_count, token_count, embedding, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, 
            m.new_section_id, 
            old_kn.chunk_index, 
            old_kn.content, 
            old_kn.search_text, 
            old_kn.content_hash, 
            old_kn.embedding_model, 
            old_kn.embedding_version, 
            old_kn.char_count, 
            old_kn.token_count, 
            old_kn.embedding, 
            now(), 
            now()
        FROM book_section_knowledge old_kn
        JOIN temp_section_map m ON old_kn.section_id = m.old_section_id;

        -- g. Tạo bảng tạm map ID của LearningUnit cũ sang ID mới
        CREATE TEMP TABLE temp_unit_map ON COMMIT DROP AS
        SELECT 
            id AS old_unit_id, 
            gen_random_uuid() AS new_unit_id
        FROM learning_units 
        WHERE book_id = shared_book_id;

        -- h. Nhân bản các LearningUnit
        INSERT INTO learning_units (
            id, user_id, book_id, mode, unit_index, title, unit_type, status, 
            source_text_char_count, estimated_tokens, estimated_audio_seconds, main_segment_count, 
            review_audio_url, review_text, planner_reason, created_at, updated_at
        )
        SELECT 
            m.new_unit_id, 
            new_user_id, 
            new_book_id, 
            old_unit.mode, 
            old_unit.unit_index, 
            old_unit.title, 
            old_unit.unit_type, 
            old_unit.status, 
            old_unit.source_text_char_count, 
            old_unit.estimated_tokens, 
            old_unit.estimated_audio_seconds, 
            old_unit.main_segment_count, 
            old_unit.review_audio_url, 
            old_unit.review_text, 
            old_unit.planner_reason, 
            now(), 
            now()
        FROM learning_units old_unit
        JOIN temp_unit_map m ON old_unit.id = m.old_unit_id;

        -- i. Nhân bản bảng liên kết LearningUnitSource
        INSERT INTO learning_unit_sources (
            learning_unit_id, section_id, source_order
        )
        SELECT 
            mu.new_unit_id, 
            ms.new_section_id, 
            old_src.source_order
        FROM learning_unit_sources old_src
        JOIN temp_unit_map mu ON old_src.learning_unit_id = mu.old_unit_id
        JOIN temp_section_map ms ON old_src.section_id = ms.old_section_id;

        -- j. Nhân bản các phân đoạn file mp3 (LearningUnitSegment)
        INSERT INTO learning_unit_segments (
            learning_unit_id, segment_index, audio_url, text_content, duration_ms, created_at
        )
        SELECT 
            mu.new_unit_id, 
            old_seg.segment_index, 
            old_seg.audio_url, 
            old_seg.text_content, 
            old_seg.duration_ms, 
            now()
        FROM learning_unit_segments old_seg
        JOIN temp_unit_map mu ON old_seg.learning_unit_id = mu.old_unit_id;

    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    # Xóa Stored Function
    op.execute("DROP FUNCTION IF EXISTS clone_shared_book(UUID, UUID, UUID);")
    
    # Xóa cột và index
    op.drop_constraint('fk_books_parent_shared_id', 'books', type_='foreignkey')
    op.drop_index(op.f('ix_books_parent_shared_id'), table_name='books')
    op.drop_column('books', 'parent_shared_id')
    op.drop_index(op.f('ix_books_is_shared'), table_name='books')
    op.drop_column('books', 'is_shared')

```

### app\db\migrations\versions\b14c2d3e4f50_phase_14_drop_legacy_book_knowledge.py

```py
"""phase 14 drop legacy book knowledge

Revision ID: b14c2d3e4f50
Revises: a13f1e2d3c4b
Create Date: 2026-06-13
"""

from typing import Sequence, Union

from alembic import op

revision: str = "b14c2d3e4f50"
down_revision: Union[str, None] = "a13f1e2d3c4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.execute("drop table if exists book_knowledge cascade")


def downgrade() -> None:
    # `book_knowledge` stored legacy learning-unit embeddings. The table data
    # cannot be reconstructed by Alembic after a destructive cleanup; restore a
    # database backup if this migration must be rolled back in production.
    pass

```

### app\db\migrations\versions\b8e4f2a7c9d1_add_document_type_and_unique_constraints.py

```py
"""add document type and unique constraints

Revision ID: b8e4f2a7c9d1
Revises: 91b0326bdf19
Create Date: 2026-05-19 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8e4f2a7c9d1"
down_revision: Union[str, Sequence[str], None] = "91b0326bdf19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("books", sa.Column("document_type", sa.Text(), nullable=True))

    op.execute(
        """
        UPDATE books
        SET document_type = CASE
            WHEN lower(file_url) LIKE '%.pdf%' THEN 'pdf'
            WHEN lower(file_url) LIKE '%.epub%' THEN 'epub'
            WHEN lower(file_url) LIKE '%.docx%' THEN 'docx'
            ELSE document_type
        END
        WHERE document_type IS NULL
        """
    )

    op.create_unique_constraint(
        "uq_chapters_book_id_chapter_index",
        "chapters",
        ["book_id", "chapter_index"],
    )
    op.create_unique_constraint(
        "uq_segments_chapter_mode_segment_index",
        "chapter_segments",
        ["chapter_id", "mode", "segment_index"],
    )
    op.create_unique_constraint(
        "uq_book_knowledge_chapter_chunk_index",
        "book_knowledge",
        ["chapter_id", "chunk_index"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_book_knowledge_chapter_chunk_index", "book_knowledge", type_="unique")
    op.drop_constraint("uq_segments_chapter_mode_segment_index", "chapter_segments", type_="unique")
    op.drop_constraint("uq_chapters_book_id_chapter_index", "chapters", type_="unique")
    op.drop_column("books", "document_type")

```

### app\db\migrations\versions\c15d3e4f5061_phase_14_1_clean_reading_plan_schedule_config.py

```py
"""phase 14.1 clean reading plan schedule config

Revision ID: c15d3e4f5061
Revises: b14c2d3e4f50
Create Date: 2026-06-13
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c15d3e4f5061"
down_revision: Union[str, None] = "b14c2d3e4f50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DAY_TO_WEEKDAY_CASE = """
case lower(trim(day.value))
  when 'mon' then 0
  when 'monday' then 0
  when 'tue' then 1
  when 'tuesday' then 1
  when 'wed' then 2
  when 'wednesday' then 2
  when 'thu' then 3
  when 'thursday' then 3
  when 'fri' then 4
  when 'friday' then 4
  when 'sat' then 5
  when 'saturday' then 5
  when 'sun' then 6
  when 'sunday' then 6
  else null
end
"""


WEEKDAY_TO_DAY_CASE = """
case s.weekday
  when 0 then 'Mon'
  when 1 then 'Tue'
  when 2 then 'Wed'
  when 3 then 'Thu'
  when 4 then 'Fri'
  when 5 then 'Sat'
  when 6 then 'Sun'
  else s.weekday::text
end
"""


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")
    op.execute(
        f"""
        insert into reading_plan_schedule_slots (
            id,
            user_id,
            plan_id,
            book_id,
            weekday,
            reminder_time,
            timezone,
            is_active,
            created_at,
            updated_at
        )
        select
            gen_random_uuid(),
            b.user_id,
            rp.id,
            rp.book_id,
            {DAY_TO_WEEKDAY_CASE} as weekday,
            coalesce(rp.reminder_time, '20:00') as reminder_time,
            coalesce(ns.timezone, 'Asia/Ho_Chi_Minh') as timezone,
            (
                rp.status = 'active'
                and not exists (
                    select 1
                    from reading_plan_schedule_slots active_conflict
                    where active_conflict.user_id = b.user_id
                      and active_conflict.weekday = {DAY_TO_WEEKDAY_CASE}
                      and active_conflict.reminder_time = coalesce(rp.reminder_time, '20:00')
                      and active_conflict.is_active is true
                )
            ) as is_active,
            now(),
            now()
        from reading_plans rp
        join books b on b.id = rp.book_id
        left join notification_settings ns on ns.user_id = b.user_id
        cross join lateral jsonb_array_elements_text(rp.schedule_config) as day(value)
        where rp.schedule_config is not null
          and jsonb_typeof(rp.schedule_config) = 'array'
          and {DAY_TO_WEEKDAY_CASE} is not null
          and not exists (
              select 1
              from reading_plan_schedule_slots existing
              where existing.plan_id = rp.id
          )
        """
    )
    op.drop_column("reading_plans", "schedule_config")


def downgrade() -> None:
    op.add_column(
        "reading_plans",
        sa.Column("schedule_config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute(
        f"""
        update reading_plans rp
        set schedule_config = coalesce(
            (
                select jsonb_agg({WEEKDAY_TO_DAY_CASE} order by s.weekday)
                from reading_plan_schedule_slots s
                where s.plan_id = rp.id
            ),
            '[]'::jsonb
        )
        """
    )

```

### app\db\migrations\versions\c4f0a9d8e2b1_add_processing_jobs.py

```py
"""add processing jobs

Revision ID: c4f0a9d8e2b1
Revises: b8e4f2a7c9d1
Create Date: 2026-05-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c4f0a9d8e2b1"
down_revision: Union[str, None] = "b8e4f2a7c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


processing_job_type = postgresql.ENUM(
    "UPLOAD",
    "GENERATE_PLAN",
    "SWITCH_MODE",
    "NOTIFICATION",
    "REVIEW",
    name="processingjobtype",
    create_type=False,
)
processing_job_status = postgresql.ENUM(
    "QUEUED",
    "PROCESSING",
    "PARTIAL_READY",
    "READY",
    "ERROR",
    "CANCELLED",
    name="processingjobstatus",
    create_type=False,
)
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE processingjobtype AS ENUM ('UPLOAD', 'GENERATE_PLAN', 'SWITCH_MODE', 'NOTIFICATION', 'REVIEW');
        EXCEPTION WHEN duplicate_object THEN null;
        END $$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE processingjobstatus AS ENUM ('QUEUED', 'PROCESSING', 'PARTIAL_READY', 'READY', 'ERROR', 'CANCELLED');
        EXCEPTION WHEN duplicate_object THEN null;
        END $$;
        """
    )

    op.create_table(
        "processing_jobs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=True),
        sa.Column("job_type", processing_job_type, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("mode", plan_mode, nullable=True),
        sa.Column("progress_percent", sa.Integer(), server_default="0", nullable=False),
        sa.Column("current_step", sa.Text(), nullable=True),
        sa.Column("total_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("done_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("failed_units", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_processing_jobs_book_id", "processing_jobs", ["book_id"])
    op.create_index("ix_processing_jobs_job_type", "processing_jobs", ["job_type"])
    op.create_index("ix_processing_jobs_status", "processing_jobs", ["status"])
    op.create_index("ix_processing_jobs_user_id", "processing_jobs", ["user_id"])
    op.create_check_constraint(
        "ck_books_status_known",
        "books",
        "status IN ('draft', 'processing', 'partial_ready', 'ready', 'error') OR status IS NULL",
    )


def downgrade() -> None:
    op.drop_constraint("ck_books_status_known", "books", type_="check")
    op.drop_index("ix_processing_jobs_user_id", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_status", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_job_type", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_book_id", table_name="processing_jobs")
    op.drop_table("processing_jobs")
    processing_job_status.drop(op.get_bind(), checkfirst=True)
    processing_job_type.drop(op.get_bind(), checkfirst=True)

```

### app\db\migrations\versions\c5d6e7f8a901_phase_6_cleanup_legacy_chapter_schema.py

```py
"""phase 6 cleanup legacy chapter schema

Revision ID: c5d6e7f8a901
Revises: a2c9e7f1b5d0
Create Date: 2026-05-29
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c5d6e7f8a901"
down_revision: Union[str, None] = "a2c9e7f1b5d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)
processing_job_status = postgresql.ENUM(
    "QUEUED",
    "PROCESSING",
    "PARTIAL_READY",
    "READY",
    "ERROR",
    "CANCELLED",
    name="processingjobstatus",
    create_type=False,
)
learning_progress_status = postgresql.ENUM(
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    name="learningprogressstatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")

    op.execute("alter table if exists book_knowledge drop column if exists chapter_id cascade")
    op.execute("alter table if exists spaced_review_items drop column if exists source_progress_id cascade")
    op.execute("alter table if exists spaced_review_items drop column if exists chapter_id cascade")
    op.execute("alter table if exists books drop column if exists total_chapters")

    op.execute("drop table if exists chapter_learning_progress cascade")
    op.execute("drop table if exists chapter_processing_states cascade")
    op.execute("drop table if exists chapter_segments cascade")
    op.execute("drop table if exists chapters cascade")

    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          learning_unit_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.learning_unit_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and book_knowledge.learning_unit_id is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")

    op.add_column("books", sa.Column("total_chapters", sa.Integer(), nullable=True))

    op.create_table(
        "chapters",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("review_audio_url", sa.Text(), nullable=True),
        sa.Column("review_text", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "chapter_index", name="uq_chapters_book_id_chapter_index"),
    )
    op.create_index("ix_chapters_book_id", "chapters", ["book_id"])

    op.create_table(
        "chapter_segments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chapter_id", "mode", "segment_index", name="uq_segments_chapter_mode_segment_index"),
    )
    op.create_index("ix_chapter_segments_chapter_id", "chapter_segments", ["chapter_id"])

    op.create_table(
        "chapter_processing_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("raw_text_char_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_audio_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("main_segment_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["processing_jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chapter_id", "mode", name="uq_chapter_processing_state_chapter_mode"),
    )
    op.create_index("ix_chapter_processing_states_user_id", "chapter_processing_states", ["user_id"])
    op.create_index("ix_chapter_processing_states_book_id", "chapter_processing_states", ["book_id"])
    op.create_index("ix_chapter_processing_states_chapter_id", "chapter_processing_states", ["chapter_id"])
    op.create_index("ix_chapter_processing_states_job_id", "chapter_processing_states", ["job_id"])
    op.create_index("ix_chapter_processing_states_status", "chapter_processing_states", ["status"])

    op.create_table(
        "chapter_learning_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("current_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("position_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("listened_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", learning_progress_status, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["current_segment_id"], ["chapter_segments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "mode", name="uq_learning_progress_user_chapter_mode"),
    )
    op.create_index("ix_chapter_learning_progress_user_id", "chapter_learning_progress", ["user_id"])
    op.create_index("ix_chapter_learning_progress_book_id", "chapter_learning_progress", ["book_id"])
    op.create_index("ix_chapter_learning_progress_chapter_id", "chapter_learning_progress", ["chapter_id"])
    op.create_index("ix_chapter_learning_progress_status", "chapter_learning_progress", ["status"])

    op.add_column("book_knowledge", sa.Column("chapter_id", sa.UUID(), nullable=True))
    op.create_index("ix_book_knowledge_chapter_id", "book_knowledge", ["chapter_id"])
    op.create_foreign_key("book_knowledge_chapter_id_fkey", "book_knowledge", "chapters", ["chapter_id"], ["id"], ondelete="CASCADE")
    op.create_unique_constraint("uq_book_knowledge_chapter_chunk_index", "book_knowledge", ["chapter_id", "chunk_index"])

    op.add_column("spaced_review_items", sa.Column("chapter_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_progress_id", sa.UUID(), nullable=True))
    op.create_index("ix_spaced_review_items_chapter_id", "spaced_review_items", ["chapter_id"])
    op.create_index("ix_spaced_review_items_source_progress_id", "spaced_review_items", ["source_progress_id"])
    op.create_foreign_key("spaced_review_items_chapter_id_fkey", "spaced_review_items", "chapters", ["chapter_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(
        "spaced_review_items_source_progress_id_fkey",
        "spaced_review_items",
        "chapter_learning_progress",
        ["source_progress_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.execute(
        """
        create or replace function match_book_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[]
        )
        returns table (
          id integer,
          book_id uuid,
          learning_unit_id uuid,
          chapter_id uuid,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            book_knowledge.id,
            book_knowledge.book_id,
            book_knowledge.learning_unit_id,
            book_knowledge.chapter_id,
            book_knowledge.chunk_index,
            book_knowledge.content,
            1 - (book_knowledge.embedding <=> query_embedding) as similarity
          from book_knowledge
          where book_knowledge.embedding is not null
            and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
            and book_knowledge.book_id = any(filter_book_ids)
          order by book_knowledge.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )

```

### app\db\migrations\versions\d16e5f607182_phase_14_4_read_path_indexes.py

```py
"""phase 14.4 read path indexes

Revision ID: d16e5f607182
Revises: c15d3e4f5061
Create Date: 2026-06-15
"""

from typing import Sequence, Union

from alembic import op

revision: str = "d16e5f607182"
down_revision: Union[str, None] = "c15d3e4f5061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create index if not exists ix_books_user_created_at on books (user_id, created_at desc, id desc)")
    op.execute(
        """
        create index if not exists ix_reading_plans_book_status_updated
        on reading_plans (book_id, status, updated_at desc, created_at desc)
        """
    )
    op.execute(
        """
        create index if not exists ix_learning_unit_progress_user_book_mode_updated
        on learning_unit_progress (user_id, book_id, mode, updated_at desc)
        """
    )
    op.execute(
        """
        create index if not exists ix_learning_unit_progress_user_book_mode_activity
        on learning_unit_progress (user_id, book_id, mode, last_activity_at desc)
        where last_activity_at is not null
        """
    )
    op.execute(
        """
        create index if not exists ix_spaced_review_items_user_book_mode_status_due
        on spaced_review_items (user_id, book_id, mode, status, due_at)
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_user_local_date_scheduled
        on reading_plan_sessions (user_id, local_date, scheduled_at, session_index)
        where status <> 'cancelled'
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_user_book_mode_scheduled
        on reading_plan_sessions (user_id, book_id, mode, scheduled_at, session_index)
        where status <> 'cancelled'
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_overdue_user_status_scheduled
        on reading_plan_sessions (user_id, status, scheduled_at)
        where status in ('scheduled', 'due', 'in_progress')
        """
    )
    op.execute(
        """
        create index if not exists ix_rps_due_reminder_status_scheduled
        on reading_plan_sessions (status, scheduled_at)
        where status in ('scheduled', 'due')
        """
    )


def downgrade() -> None:
    op.execute("drop index if exists ix_rps_due_reminder_status_scheduled")
    op.execute("drop index if exists ix_rps_overdue_user_status_scheduled")
    op.execute("drop index if exists ix_rps_user_book_mode_scheduled")
    op.execute("drop index if exists ix_rps_user_local_date_scheduled")
    op.execute("drop index if exists ix_spaced_review_items_user_book_mode_status_due")
    op.execute("drop index if exists ix_learning_unit_progress_user_book_mode_activity")
    op.execute("drop index if exists ix_learning_unit_progress_user_book_mode_updated")
    op.execute("drop index if exists ix_reading_plans_book_status_updated")
    op.execute("drop index if exists ix_books_user_created_at")

```

### app\db\migrations\versions\d7a2f4c9b8e1_phase_3_generation_guardrails.py

```py
"""phase 3 generation guardrails

Revision ID: d7a2f4c9b8e1
Revises: c4f0a9d8e2b1
Create Date: 2026-05-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d7a2f4c9b8e1"
down_revision: Union[str, None] = "c4f0a9d8e2b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)
processing_job_status = postgresql.ENUM(
    "QUEUED",
    "PROCESSING",
    "PARTIAL_READY",
    "READY",
    "ERROR",
    "CANCELLED",
    name="processingjobstatus",
    create_type=False,
)


def upgrade() -> None:
    op.add_column("processing_jobs", sa.Column("estimated_input_tokens", sa.Integer(), nullable=True))
    op.add_column("processing_jobs", sa.Column("estimated_audio_seconds", sa.Integer(), nullable=True))

    op.create_table(
        "chapter_processing_states",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("raw_text_char_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("estimated_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("estimated_audio_seconds", sa.Integer(), server_default="0", nullable=False),
        sa.Column("main_segment_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["processing_jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chapter_id", "mode", name="uq_chapter_processing_state_chapter_mode"),
    )
    op.create_index("ix_chapter_processing_states_book_id", "chapter_processing_states", ["book_id"])
    op.create_index("ix_chapter_processing_states_chapter_id", "chapter_processing_states", ["chapter_id"])
    op.create_index("ix_chapter_processing_states_job_id", "chapter_processing_states", ["job_id"])
    op.create_index("ix_chapter_processing_states_status", "chapter_processing_states", ["status"])
    op.create_index("ix_chapter_processing_states_user_id", "chapter_processing_states", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_chapter_processing_states_user_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_status", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_job_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_chapter_id", table_name="chapter_processing_states")
    op.drop_index("ix_chapter_processing_states_book_id", table_name="chapter_processing_states")
    op.drop_table("chapter_processing_states")
    op.drop_column("processing_jobs", "estimated_audio_seconds")
    op.drop_column("processing_jobs", "estimated_input_tokens")

```

### app\db\migrations\versions\e4f7a9c2d1b0_phase_4_1_in_app_notifications.py

```py
"""phase 4.1 in app notifications

Revision ID: e4f7a9c2d1b0
Revises: d7a2f4c9b8e1
Create Date: 2026-05-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e4f7a9c2d1b0"
down_revision: Union[str, None] = "d7a2f4c9b8e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


notification_type = postgresql.ENUM(
    "PLAN_REMINDER",
    "CONTENT_READY",
    "SPACED_REVIEW_DUE",
    name="notificationtype",
    create_type=False,
)
notification_channel = postgresql.ENUM("IN_APP", name="notificationchannel", create_type=False)
notification_status = postgresql.ENUM(
    "PENDING",
    "PROCESSING",
    "SENT",
    "FAILED",
    "CANCELLED",
    "SKIPPED",
    name="notificationstatus",
    create_type=False,
)
review_item_status = postgresql.ENUM(
    "PENDING",
    "DUE",
    "COMPLETED",
    "SKIPPED",
    "CANCELLED",
    name="reviewitemstatus",
    create_type=False,
)
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    notification_type.create(op.get_bind(), checkfirst=True)
    notification_channel.create(op.get_bind(), checkfirst=True)
    notification_status.create(op.get_bind(), checkfirst=True)
    review_item_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "notification_settings",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.Column("reminders_enabled", sa.Boolean(), nullable=False),
        sa.Column("spaced_review_enabled", sa.Boolean(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("quiet_hours_start", sa.Text(), nullable=False),
        sa.Column("quiet_hours_end", sa.Text(), nullable=False),
        sa.Column("daily_cap", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "spaced_review_items",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("interval_days", sa.Integer(), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", review_item_status, nullable=False),
        sa.Column("review_text_snapshot", sa.Text(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "mode", "interval_days", name="uq_review_user_chapter_mode_interval"),
    )
    op.create_index("ix_spaced_review_items_user_id", "spaced_review_items", ["user_id"])
    op.create_index("ix_spaced_review_items_book_id", "spaced_review_items", ["book_id"])
    op.create_index("ix_spaced_review_items_chapter_id", "spaced_review_items", ["chapter_id"])
    op.create_index("ix_spaced_review_items_due_at", "spaced_review_items", ["due_at"])
    op.create_index("ix_spaced_review_items_status", "spaced_review_items", ["status"])
    op.create_index("ix_spaced_review_items_status_due_at", "spaced_review_items", ["status", "due_at"])

    op.create_table(
        "notification_outbox",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("type", notification_type, nullable=False),
        sa.Column("channel", notification_channel, nullable=False),
        sa.Column("status", notification_status, nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_by", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key", name="uq_notification_outbox_idempotency_key"),
    )
    op.create_index("ix_notification_outbox_user_id", "notification_outbox", ["user_id"])
    op.create_index("ix_notification_outbox_type", "notification_outbox", ["type"])
    op.create_index("ix_notification_outbox_channel", "notification_outbox", ["channel"])
    op.create_index("ix_notification_outbox_status", "notification_outbox", ["status"])
    op.create_index("ix_notification_outbox_due_at", "notification_outbox", ["due_at"])
    op.create_index("ix_notification_outbox_next_retry_at", "notification_outbox", ["next_retry_at"])
    op.create_index("ix_notification_outbox_status_due_at", "notification_outbox", ["status", "due_at"])
    op.create_index("ix_notification_outbox_status_next_retry_at", "notification_outbox", ["status", "next_retry_at"])

    op.create_table(
        "user_notifications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("outbox_id", sa.UUID(), nullable=True),
        sa.Column("type", notification_type, nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=True),
        sa.Column("action_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["outbox_id"], ["notification_outbox.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("outbox_id", name="uq_user_notifications_outbox_id"),
    )
    op.create_index("ix_user_notifications_user_id", "user_notifications", ["user_id"])
    op.create_index("ix_user_notifications_outbox_id", "user_notifications", ["outbox_id"])
    op.create_index("ix_user_notifications_type", "user_notifications", ["type"])
    op.create_index("ix_user_notifications_user_created_at", "user_notifications", ["user_id", "created_at"])
    op.create_index("ix_user_notifications_user_read_at", "user_notifications", ["user_id", "read_at"])


def downgrade() -> None:
    op.drop_index("ix_user_notifications_user_read_at", table_name="user_notifications")
    op.drop_index("ix_user_notifications_user_created_at", table_name="user_notifications")
    op.drop_index("ix_user_notifications_type", table_name="user_notifications")
    op.drop_index("ix_user_notifications_outbox_id", table_name="user_notifications")
    op.drop_index("ix_user_notifications_user_id", table_name="user_notifications")
    op.drop_table("user_notifications")

    op.drop_index("ix_notification_outbox_status_next_retry_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_status_due_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_next_retry_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_due_at", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_status", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_channel", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_type", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_user_id", table_name="notification_outbox")
    op.drop_table("notification_outbox")

    op.drop_index("ix_spaced_review_items_status_due_at", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_status", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_due_at", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_chapter_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_book_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_user_id", table_name="spaced_review_items")
    op.drop_table("spaced_review_items")

    op.drop_table("notification_settings")

    review_item_status.drop(op.get_bind(), checkfirst=True)
    notification_status.drop(op.get_bind(), checkfirst=True)
    notification_channel.drop(op.get_bind(), checkfirst=True)
    notification_type.drop(op.get_bind(), checkfirst=True)

```

### app\db\migrations\versions\f0a1b2c3d4e5_phase_10_2_book_section_knowledge.py

```py
"""phase 10.2 book section knowledge

Revision ID: f0a1b2c3d4e5
Revises: 2b7c9d1e4f6a
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "f0a1b2c3d4e5"
down_revision: Union[str, Sequence[str], None] = "2b7c9d1e4f6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book_section_knowledge",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("section_id", sa.UUID(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("embedding_model", sa.Text(), nullable=False),
        sa.Column("embedding_version", sa.Text(), nullable=False),
        sa.Column("char_count", sa.Integer(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["book_sections.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("section_id", "chunk_index", "embedding_version", name="uq_book_section_knowledge_section_chunk_version"),
        sa.UniqueConstraint("section_id", "content_hash", "embedding_version", name="uq_book_section_knowledge_section_hash_version"),
    )
    op.create_index(op.f("ix_book_section_knowledge_book_id"), "book_section_knowledge", ["book_id"])
    op.create_index(op.f("ix_book_section_knowledge_section_id"), "book_section_knowledge", ["section_id"])
    op.create_index("ix_bsk_book_version", "book_section_knowledge", ["book_id", "embedding_version"])
    op.create_index("ix_bsk_section_version", "book_section_knowledge", ["section_id", "embedding_version"])
    op.create_index("ix_bsk_book_section_version", "book_section_knowledge", ["book_id", "section_id", "embedding_version"])
    op.create_index(
        "ix_bsk_embedding_hnsw",
        "book_section_knowledge",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )

    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[],
          filter_section_ids uuid[] default null
        )
        returns table (
          id integer,
          book_id uuid,
          section_id uuid,
          section_path text,
          section_title text,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            bsk.id,
            bsk.book_id,
            bsk.section_id,
            bs.path as section_path,
            bs.title as section_title,
            bsk.chunk_index,
            bsk.content,
            1 - (bsk.embedding <=> query_embedding) as similarity
          from book_section_knowledge bsk
          join book_sections bs on bs.id = bsk.section_id
          where bsk.embedding is not null
            and bsk.book_id = any(filter_book_ids)
            and (filter_section_ids is null or bsk.section_id = any(filter_section_ids))
            and 1 - (bsk.embedding <=> query_embedding) > match_threshold
          order by bsk.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.drop_table("book_section_knowledge")

```

### app\db\migrations\versions\f1b2c3d4e5f6_phase_10_3_hybrid_retrieval.py

```py
"""phase 10.3 hybrid retrieval

Revision ID: f1b2c3d4e5f6
Revises: f0a1b2c3d4e5
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f0a1b2c3d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create extension if not exists pg_trgm")
    op.add_column(
        "book_section_knowledge",
        sa.Column("search_text", sa.Text(), server_default="", nullable=False),
    )
    op.execute(
        """
        create index if not exists ix_bsk_search_text_trgm
        on book_section_knowledge
        using gin (search_text gin_trgm_ops)
        """
    )
    op.execute(
        """
        create index if not exists ix_bsk_content_fts_simple
        on book_section_knowledge
        using gin (to_tsvector('simple', content))
        """
    )
    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[],
          filter_section_ids uuid[] default null
        )
        returns table (
          id integer,
          book_id uuid,
          section_id uuid,
          section_path text,
          section_title text,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            bsk.id,
            bsk.book_id,
            bsk.section_id,
            bs.path as section_path,
            bs.title as section_title,
            bsk.chunk_index,
            bsk.content,
            1 - (bsk.embedding <=> query_embedding) as similarity
          from book_section_knowledge bsk
          join book_sections bs on bs.id = bsk.section_id
          where bsk.embedding is not null
            and bsk.book_id = any(filter_book_ids)
            and (
              filter_section_ids is null
              or cardinality(filter_section_ids) = 0
              or bsk.section_id = any(filter_section_ids)
            )
            and 1 - (bsk.embedding <=> query_embedding) > match_threshold
          order by bsk.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )
    op.execute(
        """
        drop function if exists match_book_section_knowledge_lexical(
          text,
          text,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge_lexical(
          query_text text,
          normalized_query_text text,
          match_count int,
          filter_book_ids uuid[],
          filter_section_ids uuid[] default null
        )
        returns table (
          id integer,
          book_id uuid,
          section_id uuid,
          section_path text,
          section_title text,
          chunk_index integer,
          content text,
          lexical_score float
        )
        language sql stable
        as $$
          with fts_candidates as (
            select
              bsk.id,
              bsk.book_id,
              bsk.section_id,
              bs.path as section_path,
              bs.title as section_title,
              bsk.chunk_index,
              bsk.content,
              ts_rank_cd(
                to_tsvector('simple', bsk.content),
                websearch_to_tsquery('simple', query_text)
              )::float as score
            from book_section_knowledge bsk
            join book_sections bs on bs.id = bsk.section_id
            where bsk.book_id = any(filter_book_ids)
              and (
                filter_section_ids is null
                or cardinality(filter_section_ids) = 0
                or bsk.section_id = any(filter_section_ids)
              )
              and coalesce(query_text, '') <> ''
              and to_tsvector('simple', bsk.content) @@ websearch_to_tsquery('simple', query_text)
            order by score desc
            limit match_count
          ),
          trigram_candidates as (
            select
              bsk.id,
              bsk.book_id,
              bsk.section_id,
              bs.path as section_path,
              bs.title as section_title,
              bsk.chunk_index,
              bsk.content,
              word_similarity(normalized_query_text, bsk.search_text)::float as score
            from book_section_knowledge bsk
            join book_sections bs on bs.id = bsk.section_id
            where bsk.book_id = any(filter_book_ids)
              and (
                filter_section_ids is null
                or cardinality(filter_section_ids) = 0
                or bsk.section_id = any(filter_section_ids)
              )
              and coalesce(normalized_query_text, '') <> ''
              and normalized_query_text <% bsk.search_text
            order by score desc
            limit match_count
          )
          select
            merged.id,
            merged.book_id,
            merged.section_id,
            merged.section_path,
            merged.section_title,
            merged.chunk_index,
            merged.content,
            max(merged.score) as lexical_score
          from (
            select * from fts_candidates
            union all
            select * from trigram_candidates
          ) merged
          group by
            merged.id,
            merged.book_id,
            merged.section_id,
            merged.section_path,
            merged.section_title,
            merged.chunk_index,
            merged.content
          order by max(merged.score) desc
          limit match_count;
        $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop function if exists match_book_section_knowledge_lexical(
          text,
          text,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        drop function if exists match_book_section_knowledge(
          vector,
          double precision,
          integer,
          uuid[],
          uuid[]
        );
        """
    )
    op.execute(
        """
        create or replace function match_book_section_knowledge(
          query_embedding vector(1536),
          match_threshold float,
          match_count int,
          filter_book_ids uuid[],
          filter_section_ids uuid[] default null
        )
        returns table (
          id integer,
          book_id uuid,
          section_id uuid,
          section_path text,
          section_title text,
          chunk_index integer,
          content text,
          similarity float
        )
        language sql stable
        as $$
          select
            bsk.id,
            bsk.book_id,
            bsk.section_id,
            bs.path as section_path,
            bs.title as section_title,
            bsk.chunk_index,
            bsk.content,
            1 - (bsk.embedding <=> query_embedding) as similarity
          from book_section_knowledge bsk
          join book_sections bs on bs.id = bsk.section_id
          where bsk.embedding is not null
            and bsk.book_id = any(filter_book_ids)
            and (filter_section_ids is null or bsk.section_id = any(filter_section_ids))
            and 1 - (bsk.embedding <=> query_embedding) > match_threshold
          order by bsk.embedding <=> query_embedding
          limit match_count;
        $$;
        """
    )
    op.execute("drop index if exists ix_bsk_content_fts_simple")
    op.execute("drop index if exists ix_bsk_search_text_trgm")
    op.drop_column("book_section_knowledge", "search_text")

```

### app\db\migrations\versions\f6a8c2d4e9b1_phase_4_2_learning_progress.py

```py
"""phase 4.2 learning progress

Revision ID: f6a8c2d4e9b1
Revises: e4f7a9c2d1b0
Create Date: 2026-05-25
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f6a8c2d4e9b1"
down_revision: Union[str, None] = "e4f7a9c2d1b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


learning_progress_status = postgresql.ENUM(
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
    name="learningprogressstatus",
    create_type=False,
)
plan_mode = postgresql.ENUM("FULL", "PARETO", name="planmode", create_type=False)


def upgrade() -> None:
    learning_progress_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "reading_plan_schedule_slots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("reminder_time", sa.Text(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_id"], ["reading_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reading_plan_schedule_slots_user_id", "reading_plan_schedule_slots", ["user_id"])
    op.create_index("ix_reading_plan_schedule_slots_plan_id", "reading_plan_schedule_slots", ["plan_id"])
    op.create_index("ix_reading_plan_schedule_slots_book_id", "reading_plan_schedule_slots", ["book_id"])
    op.create_index("ix_reading_plan_schedule_slots_is_active", "reading_plan_schedule_slots", ["is_active"])
    op.create_index("ix_reading_plan_schedule_slots_user_active", "reading_plan_schedule_slots", ["user_id", "is_active"])
    op.create_index(
        "uq_active_plan_slot_user_weekday_time",
        "reading_plan_schedule_slots",
        ["user_id", "weekday", "reminder_time"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )

    op.create_table(
        "chapter_learning_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=False),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("mode", plan_mode, nullable=False),
        sa.Column("current_segment_id", sa.Integer(), nullable=True),
        sa.Column("last_segment_index", sa.Integer(), nullable=False),
        sa.Column("position_ms", sa.Integer(), nullable=False),
        sa.Column("listened_ms", sa.Integer(), nullable=False),
        sa.Column("total_duration_ms", sa.Integer(), nullable=False),
        sa.Column("progress_percent", sa.Integer(), nullable=False),
        sa.Column("max_progress_percent", sa.Integer(), nullable=False),
        sa.Column("status", learning_progress_status, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["current_segment_id"], ["chapter_segments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", "mode", name="uq_learning_progress_user_chapter_mode"),
    )
    op.create_index("ix_chapter_learning_progress_user_id", "chapter_learning_progress", ["user_id"])
    op.create_index("ix_chapter_learning_progress_book_id", "chapter_learning_progress", ["book_id"])
    op.create_index("ix_chapter_learning_progress_chapter_id", "chapter_learning_progress", ["chapter_id"])
    op.create_index("ix_chapter_learning_progress_status", "chapter_learning_progress", ["status"])
    op.create_index("ix_chapter_learning_progress_last_activity_at", "chapter_learning_progress", ["last_activity_at"])
    op.create_index("ix_chapter_learning_progress_completed_at", "chapter_learning_progress", ["completed_at"])
    op.create_index("ix_learning_progress_user_book_mode", "chapter_learning_progress", ["user_id", "book_id", "mode"])
    op.create_index("ix_learning_progress_user_book_status", "chapter_learning_progress", ["user_id", "book_id", "status"])
    op.create_index("ix_learning_progress_user_book_activity", "chapter_learning_progress", ["user_id", "book_id", "last_activity_at"])

    op.add_column("spaced_review_items", sa.Column("anchor_completed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("spaced_review_items", sa.Column("source_progress_id", sa.UUID(), nullable=True))
    op.add_column("spaced_review_items", sa.Column("notified_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("spaced_review_items", sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(
        "fk_spaced_review_items_source_progress_id",
        "spaced_review_items",
        "chapter_learning_progress",
        ["source_progress_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_spaced_review_items_anchor_completed_at", "spaced_review_items", ["anchor_completed_at"])
    op.create_index("ix_spaced_review_items_source_progress_id", "spaced_review_items", ["source_progress_id"])

    op.execute("UPDATE spaced_review_items SET status = 'CANCELLED' WHERE source_progress_id IS NULL")
    op.drop_constraint("uq_review_user_chapter_mode_interval", "spaced_review_items", type_="unique")
    op.create_index(
        "uq_review_active_user_chapter_interval",
        "spaced_review_items",
        ["user_id", "chapter_id", "interval_days"],
        unique=True,
        postgresql_where=sa.text("status != 'CANCELLED'"),
    )


def downgrade() -> None:
    op.drop_index("uq_review_active_user_chapter_interval", table_name="spaced_review_items")
    op.create_unique_constraint(
        "uq_review_user_chapter_mode_interval",
        "spaced_review_items",
        ["user_id", "chapter_id", "mode", "interval_days"],
    )
    op.drop_index("ix_spaced_review_items_source_progress_id", table_name="spaced_review_items")
    op.drop_index("ix_spaced_review_items_anchor_completed_at", table_name="spaced_review_items")
    op.drop_constraint("fk_spaced_review_items_source_progress_id", "spaced_review_items", type_="foreignkey")
    op.drop_column("spaced_review_items", "last_reviewed_at")
    op.drop_column("spaced_review_items", "notified_at")
    op.drop_column("spaced_review_items", "source_progress_id")
    op.drop_column("spaced_review_items", "anchor_completed_at")

    op.drop_index("ix_learning_progress_user_book_activity", table_name="chapter_learning_progress")
    op.drop_index("ix_learning_progress_user_book_status", table_name="chapter_learning_progress")
    op.drop_index("ix_learning_progress_user_book_mode", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_completed_at", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_last_activity_at", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_status", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_chapter_id", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_book_id", table_name="chapter_learning_progress")
    op.drop_index("ix_chapter_learning_progress_user_id", table_name="chapter_learning_progress")
    op.drop_table("chapter_learning_progress")

    op.drop_index("uq_active_plan_slot_user_weekday_time", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_user_active", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_is_active", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_book_id", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_plan_id", table_name="reading_plan_schedule_slots")
    op.drop_index("ix_reading_plan_schedule_slots_user_id", table_name="reading_plan_schedule_slots")
    op.drop_table("reading_plan_schedule_slots")

    learning_progress_status.drop(op.get_bind(), checkfirst=True)

```

### app\main.py

```py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.api.v1.routers import admin, audiobooks, health, jobs, learning_progress, live, notifications, reading_plan_sessions, reviews, study_context, threads, upload
from app.core.exceptions import AppException
from app.core.logger import log
from app.db.database import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Khởi động hệ thống... (TRIAM)")
    # Alembic owns schema migration; startup only manages runtime resources.
    yield
    log.info("Đang dọn dẹp tài nguyên...")
    dispose_engine()


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    message = f"AppException: {exc.detail} - Status Code: {exc.status_code}"
    if exc.status_code >= 500:
        log.error(message)
    else:
        log.warning(message)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception("Unhandled Exception:")
    return JSONResponse(status_code=500, content={"detail": "Lỗi hệ thống nội bộ."})


app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notifications"])
app.include_router(learning_progress.router, prefix="/api/v1", tags=["Learning Progress"])
app.include_router(reading_plan_sessions.router, prefix="/api/v1", tags=["Reading Plan Sessions"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
app.include_router(study_context.router, prefix="/api/v1", tags=["Study Context"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])

app.include_router(threads.router, prefix="/api/v1", tags=["Threads Chat"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

### app\models\db_models.py

```py
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlmodel import Field, PrimaryKeyConstraint, Relationship, SQLModel

from app.core.constant import (
    LearningProgressStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
    PlanMode,
    ProcessingJobStatus,
    ProcessingJobType,
    ReviewItemStatus,
)


class StudyContextDocumentLink(SQLModel, table=True):
    __tablename__ = "study_context_document_links"
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, primary_key=True))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, primary_key=True))


class AdminUser(SQLModel, table=True):
    __tablename__ = "admin_users"

    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), primary_key=True))
    role: str = Field(default="admin", sa_column=Column(Text, nullable=False, server_default="admin"))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, index=True, nullable=False, server_default="true"))
    note: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_by: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True)))
    revoked_by: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    revoked_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))


class AdminAuditLog(SQLModel, table=True):
    __tablename__ = "admin_audit_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    admin_user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    action: str = Field(sa_column=Column(Text, index=True, nullable=False))
    target_type: Optional[str] = Field(default=None, sa_column=Column(Text, index=True))
    target_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), index=True))
    metadata_json: Optional[Any] = Field(default=None, sa_column=Column("metadata", JSONB))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), index=True, server_default=func.now(), nullable=False))


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    author: Optional[str] = Field(default=None, sa_column=Column(Text))
    file_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    document_type: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_sections: Optional[int] = Field(default=None, sa_column=Column(Integer))
    total_units: Optional[int] = Field(default=None, sa_column=Column(Integer))
    is_shared: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, server_default="false", index=True))
    parent_shared_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="SET NULL"), nullable=True, index=True))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    reading_plans: list["ReadingPlan"] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    contexts: list["StudyContext"] = Relationship(back_populates="books", link_model=StudyContextDocumentLink)


class ReadingPlan(SQLModel, table=True):
    __tablename__ = "reading_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))
    pace: int = Field(sa_column=Column(Integer, nullable=False))
    status: str = Field(sa_column=Column(Text, nullable=False))
    reminder_time: str = Field(default="20:00", sa_column=Column(Text, nullable=False, server_default="20:00"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    paused_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))

    # === RELATIONSHIPS ===
    book: Book = Relationship(back_populates="reading_plans")


class ReadingPlanScheduleSlot(SQLModel, table=True):
    __tablename__ = "reading_plan_schedule_slots"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    weekday: int = Field(sa_column=Column(Integer, nullable=False))
    reminder_time: str = Field(sa_column=Column(Text, nullable=False))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, index=True, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class ReadingPlanSession(SQLModel, table=True):
    __tablename__ = "reading_plan_sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), index=True, nullable=False))
    session_index: int = Field(sa_column=Column(Integer, nullable=False))
    scheduled_at: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True, nullable=False))
    local_date: str = Field(sa_column=Column(Text, index=True, nullable=False))
    reminder_time: str = Field(sa_column=Column(Text, nullable=False))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False, server_default="Asia/Ho_Chi_Minh"))
    status: str = Field(default="scheduled", sa_column=Column(Text, index=True, nullable=False, server_default="scheduled"))
    completed_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    total_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    skipped_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    missed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    missed_notified_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        Index("ix_reading_plan_sessions_plan_index", "plan_id", "session_index"),
        Index("ix_reading_plan_sessions_user_status", "user_id", "status"),
        Index("ix_reading_plan_sessions_book_mode", "book_id", "mode"),
        Index("ix_reading_plan_sessions_plan_status", "plan_id", "status"),
    )


class ReadingPlanSessionUnit(SQLModel, table=True):
    __tablename__ = "reading_plan_session_units"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plan_sessions.id", ondelete="CASCADE"), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    learning_unit_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True, nullable=False))
    unit_order: int = Field(sa_column=Column(Integer, nullable=False))
    status: str = Field(default="pending", sa_column=Column(Text, index=True, nullable=False, server_default="pending"))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        Index("ix_reading_plan_session_units_plan_unit", "plan_id", "learning_unit_id"),
        UniqueConstraint("session_id", "unit_order", name="uq_reading_plan_session_units_session_order"),
        Index("ix_reading_plan_session_units_session_status", "session_id", "status"),
        Index("ix_reading_plan_session_units_book_unit", "book_id", "learning_unit_id"),
    )


class ProcessingJob(SQLModel, table=True):
    __tablename__ = "processing_jobs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True))
    job_type: ProcessingJobType = Field(sa_column=Column(SAEnum(ProcessingJobType), index=True, nullable=False))
    status: ProcessingJobStatus = Field(default=ProcessingJobStatus.QUEUED, sa_column=Column(SAEnum(ProcessingJobStatus), index=True, nullable=False))
    mode: Optional[PlanMode] = Field(default=None, sa_column=Column(SAEnum(PlanMode)))
    progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    current_step: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    done_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    failed_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    estimated_input_tokens: Optional[int] = Field(default=None, sa_column=Column(Integer))
    estimated_audio_seconds: Optional[int] = Field(default=None, sa_column=Column(Integer))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    finished_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))


class BookSection(SQLModel, table=True):
    __tablename__ = "book_sections"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    parent_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("book_sections.id", ondelete="CASCADE"), index=True))
    section_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    level: int = Field(sa_column=Column(Integer, nullable=False))
    path: str = Field(sa_column=Column(Text, nullable=False))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_char_count: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    page_start: Optional[int] = Field(default=None, sa_column=Column(Integer))
    page_end: Optional[int] = Field(default=None, sa_column=Column(Integer))
    source_href: Optional[str] = Field(default=None, sa_column=Column(Text))
    source_anchor: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        UniqueConstraint("book_id", "section_index", name="uq_book_sections_book_index"),
        UniqueConstraint("book_id", "path", name="uq_book_sections_book_path"),
    )


class LearningUnit(SQLModel, table=True):
    __tablename__ = "learning_units"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), index=True, nullable=False))
    unit_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    unit_type: str = Field(sa_column=Column(Text, nullable=False))
    status: ProcessingJobStatus = Field(default=ProcessingJobStatus.QUEUED, sa_column=Column(SAEnum(ProcessingJobStatus), index=True, nullable=False))
    source_text_char_count: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    estimated_tokens: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    estimated_audio_seconds: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    main_segment_count: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    review_audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    review_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    planner_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    finished_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    __table_args__ = (UniqueConstraint("book_id", "mode", "unit_index", name="uq_learning_units_book_mode_index"),)


class LearningUnitSource(SQLModel, table=True):
    __tablename__ = "learning_unit_sources"

    learning_unit_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), primary_key=True))
    section_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("book_sections.id", ondelete="CASCADE"), primary_key=True))
    source_order: int = Field(sa_column=Column(Integer, nullable=False))


class LearningUnitSegment(SQLModel, table=True):
    __tablename__ = "learning_unit_segments"

    id: Optional[int] = Field(default=None, primary_key=True)
    learning_unit_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True, nullable=False))
    segment_index: int = Field(sa_column=Column(Integer, nullable=False))
    audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    duration_ms: Optional[int] = Field(default=None, sa_column=Column(Integer))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))

    __table_args__ = (UniqueConstraint("learning_unit_id", "segment_index", name="uq_learning_unit_segments_unit_index"),)


class LearningUnitProgress(SQLModel, table=True):
    __tablename__ = "learning_unit_progress"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    learning_unit_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))
    current_segment_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("learning_unit_segments.id", ondelete="SET NULL")))
    last_segment_index: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    position_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    listened_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    total_duration_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    max_progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    status: LearningProgressStatus = Field(default=LearningProgressStatus.NOT_STARTED, sa_column=Column(SAEnum(LearningProgressStatus), index=True, nullable=False))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    last_activity_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (UniqueConstraint("user_id", "learning_unit_id", name="uq_unit_progress_user_unit"),)


class BookLearningState(SQLModel, table=True):
    __tablename__ = "book_learning_states"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), index=True, nullable=False))
    status: str = Field(default="not_started", sa_column=Column(Text, index=True, nullable=False, server_default="not_started"))
    book_progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    completed_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    playable_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    last_learning_unit_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="SET NULL")))
    last_segment_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("learning_unit_segments.id", ondelete="SET NULL")))
    last_segment_index: Optional[int] = Field(default=None, sa_column=Column(Integer))
    position_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    last_activity_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", "mode", name="uq_book_learning_state_user_book_mode"),
        Index("ix_book_learning_states_user_status", "user_id", "status"),
        Index("ix_book_learning_states_book_mode", "book_id", "mode"),
    )


class NotificationSettings(SQLModel, table=True):
    __tablename__ = "notification_settings"

    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), primary_key=True))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False))
    reminders_enabled: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    spaced_review_enabled: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    reminder_time: str = Field(default="20:00", sa_column=Column(Text, nullable=False))
    quiet_hours_start: str = Field(default="22:00", sa_column=Column(Text, nullable=False))
    quiet_hours_end: str = Field(default="07:00", sa_column=Column(Text, nullable=False))
    daily_cap: int = Field(default=15, sa_column=Column(Integer, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class SpacedReviewItem(SQLModel, table=True):
    __tablename__ = "spaced_review_items"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    learning_unit_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))
    interval_days: int = Field(sa_column=Column(Integer, nullable=False))
    sequence_index: int = Field(sa_column=Column(Integer, nullable=False))
    due_at: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True, nullable=False))
    status: ReviewItemStatus = Field(default=ReviewItemStatus.PENDING, sa_column=Column(SAEnum(ReviewItemStatus), index=True, nullable=False))
    review_text_snapshot: Optional[str] = Field(default=None, sa_column=Column(Text))
    anchor_completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    source_unit_progress_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_unit_progress.id", ondelete="SET NULL"), index=True))
    notified_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    last_reviewed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class NotificationOutbox(SQLModel, table=True):
    __tablename__ = "notification_outbox"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    type: NotificationType = Field(sa_column=Column(SAEnum(NotificationType), index=True, nullable=False))
    channel: NotificationChannel = Field(default=NotificationChannel.IN_APP, sa_column=Column(SAEnum(NotificationChannel), index=True, nullable=False))
    status: NotificationStatus = Field(default=NotificationStatus.PENDING, sa_column=Column(SAEnum(NotificationStatus), index=True, nullable=False))
    payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    due_at: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True, nullable=False))
    next_retry_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    locked_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    locked_by: Optional[str] = Field(default=None, sa_column=Column(Text))
    sent_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    attempts: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    idempotency_key: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (UniqueConstraint("idempotency_key", name="uq_notification_outbox_idempotency_key"),)


class UserNotification(SQLModel, table=True):
    __tablename__ = "user_notifications"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    outbox_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("notification_outbox.id", ondelete="SET NULL"), index=True))
    type: NotificationType = Field(sa_column=Column(SAEnum(NotificationType), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    body: str = Field(sa_column=Column(Text, nullable=False))
    action_type: Optional[str] = Field(default=None, sa_column=Column(Text))
    action_payload: Optional[dict[str, Any]] = Field(default=None, sa_column=Column(JSONB))
    read_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))

    __table_args__ = (UniqueConstraint("outbox_id", name="uq_user_notifications_outbox_id"),)


class UserDeviceToken(SQLModel, table=True):
    __tablename__ = "user_device_tokens"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    device_token: str = Field(sa_column=Column(Text, unique=True, index=True, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class BookSectionKnowledge(SQLModel, table=True):
    __tablename__ = "book_section_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    section_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("book_sections.id", ondelete="CASCADE"), index=True, nullable=False))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    search_text: str = Field(default="", sa_column=Column(Text, nullable=False, server_default=""))
    content_hash: str = Field(sa_column=Column(Text, nullable=False))
    embedding_model: str = Field(sa_column=Column(Text, nullable=False))
    embedding_version: str = Field(sa_column=Column(Text, nullable=False))
    char_count: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    token_count: Optional[int] = Field(default=None, sa_column=Column(Integer))
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        UniqueConstraint("section_id", "chunk_index", "embedding_version", name="uq_book_section_knowledge_section_chunk_version"),
        UniqueConstraint("section_id", "content_hash", "embedding_version", name="uq_book_section_knowledge_section_hash_version"),
        Index("ix_bsk_book_version", "book_id", "embedding_version"),
        Index("ix_bsk_section_version", "section_id", "embedding_version"),
        Index("ix_bsk_book_section_version", "book_id", "section_id", "embedding_version"),
    )


# === CONTEXT STUDY CONVERSATION===


class StudyContext(SQLModel, table=True):
    __tablename__ = "study_contexts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    is_auto_generated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    books: list[Book] = Relationship(back_populates="contexts", link_model=StudyContextDocumentLink)
    threads: list["ChatThread"] = Relationship(back_populates="context", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatThread(SQLModel, table=True):
    __tablename__ = "chat_threads"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    context: StudyContext = Relationship(back_populates="threads")
    messages: list["ChatMessage"] = Relationship(back_populates="thread", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chat_threads.id", ondelete="CASCADE"), index=True, nullable=False))
    is_user: bool = Field(sa_column=Column(Boolean, nullable=False))
    text: str = Field(sa_column=Column(Text, nullable=False))
    source: str = Field(sa_column=Column(Text, nullable=False))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    thread: ChatThread = Relationship(back_populates="messages")


class DirectBookContext(SQLModel, table=True):
    __tablename__ = "direct_book_context"

    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, nullable=False))
    primary_thread_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chat_threads.id", ondelete="CASCADE"), index=True, nullable=False))

    __table_args__ = (PrimaryKeyConstraint("user_id", "book_id", name="direct_book_context_pk"),)

```

### app\repositories\admin_repo.py

```py
import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from sqlalchemy import Column, DateTime, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlmodel import Session, func, select

from app.core.constant import ProcessingJobStatus, ProcessingJobType
from app.models.db_models import AdminAuditLog, AdminUser, Book, LearningUnit, LearningUnitSegment, ProcessingJob, UserNotification

# Define schema table
metadata = MetaData()
auth_users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("email", Text),
    Column("created_at", DateTime(timezone=True)),
    Column("last_sign_in_at", DateTime(timezone=True)),
    Column("raw_user_meta_data", JSONB),
    schema="auth"
)

def _key(value: object) -> str:
    if isinstance(value, Enum):
        return value.value
    return str(value or "unknown")


def get_active_admin_user(session: Session, user_id: uuid.UUID) -> AdminUser | None:
    return session.exec(select(AdminUser).where(AdminUser.user_id == user_id, AdminUser.is_active.is_(True))).first()


def create_admin_audit_log(
    session: Session,
    *,
    admin_user_id: uuid.UUID,
    action: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    metadata: dict[str, Any] | None = None,
) -> AdminAuditLog:
    audit_log = AdminAuditLog(
        admin_user_id=admin_user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        metadata_json=metadata,
    )
    session.add(audit_log)
    return audit_log


def get_admin_dashboard(session: Session) -> dict[str, Any]:
    since_24h = datetime.now(timezone.utc) - timedelta(hours=24)
    since_30d = datetime.now(timezone.utc) - timedelta(days=30)

    book_count = int(session.exec(select(func.count(Book.id))).one() or 0)
    job_count = int(session.exec(select(func.count(ProcessingJob.id))).one() or 0)
    user_count = count_admin_users(session)

    books_by_status = {
        _key(status): int(count)
        for status, count in session.exec(select(Book.status, func.count(Book.id)).group_by(Book.status)).all()
    }
    jobs_by_status = {
        _key(status): int(count)
        for status, count in session.exec(select(ProcessingJob.status, func.count(ProcessingJob.id)).group_by(ProcessingJob.status)).all()
    }
    failed_jobs_last_24h = int(
        session.exec(
            select(func.count(ProcessingJob.id)).where(
                ProcessingJob.status == ProcessingJobStatus.ERROR,
                ProcessingJob.updated_at >= since_24h,
            )
        ).one()
        or 0
    )
    usage_row = session.exec(
        select(
            func.coalesce(func.sum(ProcessingJob.estimated_input_tokens), 0),
            func.coalesce(func.sum(ProcessingJob.estimated_audio_seconds), 0),
        ).where(ProcessingJob.created_at >= since_30d)
    ).one()

    return {
        "user_count": user_count,
        "book_count": book_count,
        "job_count": job_count,
        "books_by_status": books_by_status,
        "jobs_by_status": jobs_by_status,
        "failed_jobs_last_24h": failed_jobs_last_24h,
        "estimated_input_tokens_last_30d": int(usage_row[0] or 0),
        "estimated_audio_seconds_last_30d": int(usage_row[1] or 0),
    }


def count_admin_users(session: Session, user_id: uuid.UUID | None = None) -> int:
    query = select(func.count(auth_users.c.id))
    if user_id:
        query = query.where(auth_users.c.id != user_id)

    return int(session.exec(query).one() or 0)


def list_admin_users(session: Session, *, limit: int, offset: int, user_id: uuid.UUID | None = None) -> tuple[list[dict[str, Any]], int]:
    query = select(auth_users.c.id, auth_users.c.email, auth_users.c.created_at, auth_users.c.last_sign_in_at, auth_users.c.raw_user_meta_data)
    if user_id:
        query = query.where(auth_users.c.id != user_id)

    users_data  = list(
        session.exec(
            query
            .order_by(auth_users.c.created_at.desc())
            .offset(offset)
            .limit(limit)
        ).all()
    )
    total = count_admin_users(session, user_id)
    if not users_data:
        return [], total

    user_ids = [u.id for u in users_data]

    book_stats = {
        user_id: {"book_count": int(book_count), "last_book_at": last_book_at}
        for user_id, book_count, last_book_at in session.exec(
            select(Book.user_id, func.count(Book.id), func.max(Book.updated_at)).where(Book.user_id.in_(user_ids)).group_by(Book.user_id)
        ).all()
    }
    job_stats = {
        user_id: {"job_count": int(job_count), "last_job_at": last_job_at}
        for user_id, job_count, last_job_at in session.exec(
            select(ProcessingJob.user_id, func.count(ProcessingJob.id), func.max(ProcessingJob.updated_at))
            .where(ProcessingJob.user_id.in_(user_ids))
            .group_by(ProcessingJob.user_id)
        ).all()
    }
    notification_stats = {
        user_id: {"notification_count": int(notification_count), "last_notification_at": last_notification_at}
        for user_id, notification_count, last_notification_at in session.exec(
            select(UserNotification.user_id, func.count(UserNotification.id), func.max(UserNotification.created_at))
            .where(UserNotification.user_id.in_(user_ids))
            .group_by(UserNotification.user_id)
        ).all()
    }

    items: list[dict[str, Any]] = []
    for user_id, email, created_at, last_sign_in_at, meta in users_data:
        meta_dict = meta if isinstance(meta, dict) else {}
        display_name = meta_dict.get("name") or meta_dict.get("full_name")
        avatar_url = meta_dict.get("avatar_url") or meta_dict.get("picture")

        book_data = book_stats.get(user_id, {})
        job_data = job_stats.get(user_id, {})
        notification_data = notification_stats.get(user_id, {})
        last_activity_candidates = [
            book_data.get("last_book_at"),
            job_data.get("last_job_at"),
            notification_data.get("last_notification_at"),
        ]
        items.append(
            {
                "user_id": user_id,
                "email": email,
                "display_name": display_name,
                "avatar_url": avatar_url,
                "account_created_at": created_at,
                "last_sign_in_at": last_sign_in_at,
                "book_count": book_data.get("book_count", 0),
                "job_count": job_data.get("job_count", 0),
                "notification_count": notification_data.get("notification_count", 0),
                "last_activity_at": max([value for value in last_activity_candidates if value], default=None),
            }
        )
    return items, total


def list_admin_books(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    document_type: str | None = None,
    user_id: uuid.UUID | None = None,
    q: str | None = None,
) -> tuple[list[Book], int]:
    filters = []
    if status:
        filters.append(Book.status == status)
    if document_type:
        filters.append(Book.document_type == document_type)
    if user_id:
        filters.append(Book.user_id == user_id)
    if q:
        filters.append(Book.title.ilike(f"%{q.strip()}%"))

    total = int(session.exec(select(func.count(Book.id)).where(*filters)).one() or 0)
    books = list(session.exec(select(Book).where(*filters).order_by(Book.created_at.desc()).offset(offset).limit(limit)).all())
    return books, total


def get_admin_book_by_id(session: Session, book_id: uuid.UUID) -> Book | None:
    return session.get(Book, book_id)


def get_latest_admin_job_for_book(session: Session, book_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(select(ProcessingJob).where(ProcessingJob.book_id == book_id).order_by(ProcessingJob.created_at.desc())).first()


def count_learning_units_by_status(session: Session, book_id: uuid.UUID) -> dict[str, int]:
    return {
        _key(status): int(count)
        for status, count in session.exec(
            select(LearningUnit.status, func.count(LearningUnit.id)).where(LearningUnit.book_id == book_id).group_by(LearningUnit.status)
        ).all()
    }


def count_learning_unit_segments_for_book(session: Session, book_id: uuid.UUID) -> int:
    return int(
        session.exec(
            select(func.count(LearningUnitSegment.id))
            .join(LearningUnit, LearningUnit.id == LearningUnitSegment.learning_unit_id)
            .where(LearningUnit.book_id == book_id)
        ).one()
        or 0
    )


def list_admin_jobs(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: ProcessingJobStatus | None = None,
    job_type: ProcessingJobType | None = None,
    user_id: uuid.UUID | None = None,
    book_id: uuid.UUID | None = None,
) -> tuple[list[ProcessingJob], int]:
    filters = []
    if status:
        filters.append(ProcessingJob.status == status)
    if job_type:
        filters.append(ProcessingJob.job_type == job_type)
    if user_id:
        filters.append(ProcessingJob.user_id == user_id)
    if book_id:
        filters.append(ProcessingJob.book_id == book_id)

    total = int(session.exec(select(func.count(ProcessingJob.id)).where(*filters)).one() or 0)
    jobs = list(session.exec(select(ProcessingJob).where(*filters).order_by(ProcessingJob.created_at.desc()).offset(offset).limit(limit)).all())
    return jobs, total


def list_admin_audit_logs(
    session: Session,
    *,
    limit: int,
    offset: int,
    action: str | None = None,
    admin_user_id: uuid.UUID | None = None,
) -> tuple[list[AdminAuditLog], int]:
    filters = []
    if action:
        filters.append(AdminAuditLog.action == action)
    if admin_user_id:
        filters.append(AdminAuditLog.admin_user_id == admin_user_id)

    total = int(session.exec(select(func.count(AdminAuditLog.id)).where(*filters)).one() or 0)
    logs = list(session.exec(select(AdminAuditLog).where(*filters).order_by(AdminAuditLog.created_at.desc()).offset(offset).limit(limit)).all())
    return logs, total

```

### app\repositories\agent_grounding_repo.py

```py
from __future__ import annotations

import uuid

from sqlmodel import Session, col, select

from app.db.database import engine
from app.models.db_models import Book, BookSection
from app.services.agent_grounding.contracts import GroundingBook, GroundingScope, GroundingSection, GroundingSectionText


def parse_allowed_book_ids(document_ids: list[str]) -> list[uuid.UUID]:
    result: list[uuid.UUID] = []
    for value in document_ids:
        try:
            parsed = uuid.UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            continue
        if parsed not in result:
            result.append(parsed)
    return result


def get_grounding_scope(session: Session, allowed_book_ids: list[uuid.UUID]) -> GroundingScope:
    if not allowed_book_ids:
        return GroundingScope((), (), ())

    books = list(session.exec(select(Book).where(col(Book.id).in_(allowed_book_ids))).all())

    books_by_id = {book.id: book for book in books}

    ordered_books = [books_by_id[book_id] for book_id in allowed_book_ids if book_id in books_by_id]

    actual_book_ids = [book.id for book in ordered_books]

    if not actual_book_ids:
        return GroundingScope(tuple(allowed_book_ids), (), ())

    sections = list(session.exec(select(BookSection).where(col(BookSection.book_id).in_(actual_book_ids)).order_by(col(BookSection.book_id), col(BookSection.section_index))).all())

    root_count_by_book: dict[uuid.UUID, int] = {}
    for section in sections:
        if section.parent_id is None:
            root_count_by_book[section.book_id] = root_count_by_book.get(section.book_id, 0) + 1

    grounding_books = tuple(
        GroundingBook(
            id=book.id,
            title=book.title,
            author=book.author,
            document_type=book.document_type,
            total_sections=book.total_sections,
            status=book.status,
            root_section_count=root_count_by_book.get(book.id, 0),
        )
        for book in ordered_books
    )

    grounding_sections = tuple(
        GroundingSection(
            id=section.id,
            book_id=section.book_id,
            parent_id=section.parent_id,
            section_index=section.section_index,
            title=section.title,
            level=section.level,
            path=section.path,
            text_char_count=section.text_char_count,
        )
        for section in sections
    )

    return GroundingScope(tuple(actual_book_ids), grounding_books, grounding_sections)


def load_grounding_scope(document_ids: list[str]) -> GroundingScope:
    allowed_book_ids = parse_allowed_book_ids(document_ids)
    with Session(engine) as session:
        return get_grounding_scope(session, allowed_book_ids)


def get_scoped_section_texts(
    session: Session,
    *,
    book_id: uuid.UUID,
    section_ids: tuple[uuid.UUID, ...],
    allowed_book_ids: tuple[uuid.UUID, ...],
) -> tuple[GroundingSectionText, ...]:
    if not section_ids or book_id not in allowed_book_ids:
        return ()
    sections = list(
        session.exec(
            select(BookSection)
            .where(
                BookSection.book_id == book_id,
                col(BookSection.book_id).in_(allowed_book_ids),
                col(BookSection.id).in_(section_ids),
            )
            .order_by(col(BookSection.section_index))
        ).all()
    )
    return tuple(
        GroundingSectionText(
            id=section.id,
            book_id=section.book_id,
            section_index=section.section_index,
            title=section.title,
            path=section.path,
            text_content=section.text_content,
        )
        for section in sections
    )


def load_scoped_section_texts(
    book_id: uuid.UUID,
    section_ids: tuple[uuid.UUID, ...],
    allowed_book_ids: tuple[uuid.UUID, ...],
) -> tuple[GroundingSectionText, ...]:
    with Session(engine) as session:
        return get_scoped_section_texts(
            session,
            book_id=book_id,
            section_ids=section_ids,
            allowed_book_ids=allowed_book_ids,
        )

```

### app\repositories\audiobook_repo.py

```py
import uuid
import asyncio
from typing import Optional

from sqlalchemy import or_
from sqlmodel import Session, col, delete, select

from app.core.exceptions import BookNotFoundError, StorageOperationError
from app.core.logger import log
from app.core.supabase import supabase
from app.models.db_models import Book, NotificationOutbox, UserNotification
from app.schemas.audiobook import BookUpdateRequest


def get_audiobooks(session: Session) -> list[Book]:
    return list(session.exec(select(Book)).all())


def get_audiobooks_by_user(session: Session, user_id: uuid.UUID) -> list[Book]:
    return list(session.exec(select(Book).where(Book.user_id == user_id)).all())


def get_book_by_id(session: Session, book_id: uuid.UUID) -> Optional[Book]:
    return session.get(Book, book_id)


def get_book_by_id_and_user(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Book]:
    return session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()


def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def update_book_status(session: Session, book_id: uuid.UUID, status: str, error_message: Optional[str] = None) -> None:
    book = session.get(Book, book_id)
    if book:
        book.status = status
        if error_message is not None:
            book.error_message = error_message
        session.add(book)
        session.commit()


def update_book_by_id(session: Session, book_data: BookUpdateRequest, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def delete_book(session: Session, book_id: uuid.UUID) -> None:
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


def cleanup_book_side_effects(session: Session, *, book_id: uuid.UUID, user_id: uuid.UUID) -> None:
    book_id_str = str(book_id)

    outbox_filter = or_(
        NotificationOutbox.payload.contains({"book_id": book_id_str}),
        NotificationOutbox.payload.contains({"action_payload": {"book_id": book_id_str}}),
    )

    outbox_ids = list(session.exec(select(NotificationOutbox.id).where(NotificationOutbox.user_id == user_id, outbox_filter)).all())

    user_notification_filter = UserNotification.action_payload.contains({"book_id": book_id_str})

    if outbox_ids:
        user_notification_filter = or_(
            UserNotification.action_payload.contains({"book_id": book_id_str}),
            col(UserNotification.outbox_id).in_(outbox_ids),
        )

    session.exec(delete(UserNotification).where(UserNotification.user_id == user_id, user_notification_filter))
    if outbox_ids:
        session.exec(
            delete(NotificationOutbox).where(
                NotificationOutbox.user_id == user_id,
                col(NotificationOutbox.id).in_(outbox_ids),
            )
        )

    session.flush()


async def delete_book_storage(session: Session, book_id: uuid.UUID, user_id: uuid.UUID):
    """
    Xóa assets vật lý trên Storage (chỉ áp dụng cho sách tự upload)
    và dọn dẹp sạch bản ghi metadata trong Database.
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)

    # Logic CLone book
    if book.parent_shared_id is not None:
        log.info(f"Book {str_book_id} là sách clone. Bỏ qua bước xóa file vật lý trên Storage.")
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Clear Clone Book: {str_book_id}")
        return

    # --- Normal logic DEL Book + Related object + Storage object ---
    target_buckets = ["audios", "raw_books"]
    try:
        # Lấy danh sách file từ tất cả bucket liên quan qua RPC
        result = await asyncio.to_thread(
            supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute
        )

        # Xóa file vật lý qua Storage API
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    await asyncio.to_thread(supabase.storage.from_(bucket).remove, paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # Xóa record trong DB
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch database cho book tự upload: {str_book_id}")

    except Exception as e:
        session.rollback()
        log.exception(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise StorageOperationError("Không thể xóa tài nguyên sách trong Storage.") from e


```

### app\repositories\book_learning_state_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.models.db_models import BookLearningState


def get_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningState | None:
    return session.exec(
        select(BookLearningState).where(
            BookLearningState.user_id == user_id,
            BookLearningState.book_id == book_id,
            BookLearningState.mode == mode,
        )
    ).first()


def upsert_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    status: str,
    book_progress_percent: int,
    completed_units: int,
    playable_units: int,
    last_learning_unit_id: uuid.UUID | None,
    last_segment_id: int | None,
    last_segment_index: int | None,
    position_ms: int,
    started_at: datetime | None,
    last_activity_at: datetime | None,
    completed_at: datetime | None,
) -> BookLearningState:
    now = datetime.now(timezone.utc)
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if state is None:
        state = BookLearningState(user_id=user_id, book_id=book_id, mode=mode)

    state.status = status
    state.book_progress_percent = book_progress_percent
    state.completed_units = completed_units
    state.playable_units = playable_units
    state.last_learning_unit_id = last_learning_unit_id
    state.last_segment_id = last_segment_id
    state.last_segment_index = last_segment_index
    state.position_ms = position_ms
    state.started_at = state.started_at or started_at
    state.last_activity_at = last_activity_at
    state.completed_at = state.completed_at or completed_at
    state.updated_at = now

    session.add(state)
    session.commit()
    session.refresh(state)
    return state


def reset_book_learning_state(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Đặt lại trạng thái tiến độ tổng quan của sách về ban đầu."""
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if state:
        state.status = "not_started"
        state.book_progress_percent = 0
        state.completed_units = 0
        state.playable_units = 0
        state.last_learning_unit_id = None
        state.last_segment_id = None
        state.last_segment_index = None
        state.position_ms = 0
        state.started_at = None
        state.completed_at = None
        state.updated_at = datetime.now(timezone.utc)
        session.add(state)

```

### app\repositories\book_read_repo.py

```py
import uuid
from dataclasses import dataclass

from sqlmodel import Session, col, select

from app.core.constant import PlanStatus
from app.models.db_models import Book, BookLearningState, ReadingPlan


@dataclass(frozen=True)
class BookListProjection:
    book: Book
    current_plan: ReadingPlan | None
    learning_state: BookLearningState | None


def _latest_plan_by_book(plans: list[ReadingPlan]) -> dict[uuid.UUID, ReadingPlan]:
    result: dict[uuid.UUID, ReadingPlan] = {}
    for plan in plans:
        result.setdefault(plan.book_id, plan)
    return result


def _mode_key(mode: object) -> str:
    return str(mode.value if hasattr(mode, "value") else mode)


def _learning_state_by_book_mode(states: list[BookLearningState]) -> dict[tuple[uuid.UUID, str], BookLearningState]:
    return {(state.book_id, _mode_key(state.mode)): state for state in states}


def list_book_library_projections(session: Session, *, user_id: uuid.UUID) -> list[BookListProjection]:
    books = list(
        session.exec(
            select(Book)
            .where(Book.user_id == user_id)
            .order_by(col(Book.created_at).desc(), col(Book.id).desc())
        ).all()
    )
    if not books:
        return []

    book_ids = [book.id for book in books]
    plans = list(
        session.exec(
            select(ReadingPlan)
            .where(
                col(ReadingPlan.book_id).in_(book_ids),
                ReadingPlan.status != PlanStatus.ERROR.value,
            )
            .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
        ).all()
    )
    states = list(
        session.exec(
            select(BookLearningState).where(
                BookLearningState.user_id == user_id,
                col(BookLearningState.book_id).in_(book_ids),
            )
        ).all()
    )

    plan_by_book = _latest_plan_by_book(plans)
    state_by_book_mode = _learning_state_by_book_mode(states)
    return [
        BookListProjection(
            book=book,
            current_plan=plan_by_book.get(book.id),
            learning_state=state_by_book_mode.get(
                (book.id, _mode_key(plan_by_book[book.id].mode))
            )
            if book.id in plan_by_book
            else None,
        )
        for book in books
    ]


def get_book_library_projection(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
) -> BookListProjection | None:
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        return None

    plan = session.exec(
        select(ReadingPlan)
        .where(
            ReadingPlan.book_id == book_id,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()
    state = None
    if plan:
        state = session.exec(
            select(BookLearningState).where(
                BookLearningState.user_id == user_id,
                BookLearningState.book_id == book_id,
                BookLearningState.mode == plan.mode,
            )
        ).first()

    return BookListProjection(book=book, current_plan=plan, learning_state=state)

```

### app\repositories\book_section_knowledge_repo.py

```py
import uuid
from dataclasses import dataclass

from sqlalchemy import delete, func, update
from sqlmodel import Session, col, select

from app.models.db_models import BookSection, BookSectionKnowledge


@dataclass(frozen=True)
class SectionKnowledgeSearchTextRow:
    id: int
    section_path: str
    section_title: str
    content: str
    search_text: str


def bulk_create_section_knowledge(session: Session, records: list[BookSectionKnowledge]) -> None:
    for record in records:
        session.add(record)


def delete_section_knowledge(
    session: Session,
    *,
    section_id: uuid.UUID,
    embedding_version: str,
) -> None:
    session.exec(
        delete(BookSectionKnowledge).where(
            BookSectionKnowledge.section_id == section_id,
            BookSectionKnowledge.embedding_version == embedding_version,
        )
    )


def list_section_hashes(
    session: Session,
    *,
    section_id: uuid.UUID,
    embedding_version: str,
) -> list[str]:
    rows = session.exec(
        select(BookSectionKnowledge.content_hash)
        .where(
            BookSectionKnowledge.section_id == section_id,
            BookSectionKnowledge.embedding_version == embedding_version,
        )
        .order_by(col(BookSectionKnowledge.chunk_index))
    ).all()
    return list(rows)


def count_indexed_sections(
    session: Session,
    *,
    book_id: uuid.UUID,
    embedding_version: str,
) -> int:
    return int(
        session.exec(
            select(func.count(func.distinct(BookSectionKnowledge.section_id))).where(
                BookSectionKnowledge.book_id == book_id,
                BookSectionKnowledge.embedding_version == embedding_version,
            )
        ).one()
        or 0
    )


def count_indexable_sections(session: Session, *, book_id: uuid.UUID) -> int:
    return int(
        session.exec(
            select(func.count(BookSection.id)).where(
                BookSection.book_id == book_id,
                BookSection.text_content.is_not(None),
                BookSection.text_char_count > 0,
            )
        ).one()
        or 0
    )


def list_section_knowledge_rows_for_search_text(
    session: Session,
    *,
    book_id: uuid.UUID,
) -> list[SectionKnowledgeSearchTextRow]:
    rows = session.exec(
        select(
            BookSectionKnowledge.id,
            BookSection.path,
            BookSection.title,
            BookSectionKnowledge.content,
            BookSectionKnowledge.search_text,
        )
        .join(BookSection, BookSection.id == BookSectionKnowledge.section_id)
        .where(BookSectionKnowledge.book_id == book_id)
        .order_by(col(BookSection.section_index), col(BookSectionKnowledge.chunk_index))
    ).all()
    return [
        SectionKnowledgeSearchTextRow(
            id=row[0],
            section_path=row[1],
            section_title=row[2],
            content=row[3],
            search_text=row[4],
        )
        for row in rows
        if row[0] is not None
    ]


def update_section_knowledge_search_text(session: Session, *, knowledge_id: int, search_text: str) -> None:
    session.exec(
        update(BookSectionKnowledge)
        .where(BookSectionKnowledge.id == knowledge_id)
        .values(search_text=search_text)
    )

```

### app\repositories\book_section_repo.py

```py
import uuid
from dataclasses import dataclass

from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, col, select

from app.models.db_models import BookSection
from app.services.book_section_chunker import normalize_section_text
from app.services.document_structure_types import ParsedDocument, ParsedSection


@dataclass(frozen=True)
class BookSectionOutlineRow:
    id: uuid.UUID
    parent_id: uuid.UUID | None
    section_index: int
    title: str
    level: int
    path: str
    page_start: int | None
    page_end: int | None
    text_char_count: int


def delete_sections_by_book(session: Session, book_id: uuid.UUID) -> None:
    sections = session.exec(select(BookSection).where(BookSection.book_id == book_id)).all()
    for section in sections:
        session.delete(section)


def create_book_sections(session: Session, book_id: uuid.UUID, parsed_document: ParsedDocument) -> list[BookSection]:
    created: list[BookSection] = []
    section_index = 0

    def walk(sections: list[ParsedSection], parent_id: uuid.UUID | None = None) -> None:
        nonlocal section_index
        for section in sections:
            normalized_text = normalize_section_text(section.text)
            row = BookSection(
                book_id=book_id,
                parent_id=parent_id,
                section_index=section_index,
                title=section.title,
                level=section.level,
                path=section.path,
                text_content=normalized_text or None,
                text_char_count=len(normalized_text or ""),
                page_start=section.page_start,
                page_end=section.page_end,
                source_href=section.source_href,
                source_anchor=section.source_anchor,
            )
            section_index += 1
            session.add(row)
            session.flush()
            created.append(row)
            walk(section.children, row.id)

    walk(parsed_document.sections)
    return created


def list_book_sections(session: Session, book_id: uuid.UUID) -> list[BookSection]:
    try:
        return list(
            session.exec(
                select(BookSection)
                .where(BookSection.book_id == book_id)
                .order_by(col(BookSection.section_index))
            ).all()
        )
    except ProgrammingError as exc:
        if "book_sections" in str(exc) and "does not exist" in str(exc):
            session.rollback()
            return []
        raise


def list_book_section_outline_rows(session: Session, book_id: uuid.UUID) -> list[BookSectionOutlineRow]:
    try:
        rows = session.exec(
            select(
                BookSection.id,
                BookSection.parent_id,
                BookSection.section_index,
                BookSection.title,
                BookSection.level,
                BookSection.path,
                BookSection.page_start,
                BookSection.page_end,
                BookSection.text_char_count,
            )
            .where(BookSection.book_id == book_id)
            .order_by(col(BookSection.section_index))
        ).all()
    except ProgrammingError as exc:
        if "book_sections" in str(exc) and "does not exist" in str(exc):
            session.rollback()
            return []
        raise

    return [
        BookSectionOutlineRow(
            id=row[0],
            parent_id=row[1],
            section_index=row[2],
            title=row[3],
            level=row[4],
            path=row[5],
            page_start=row[6],
            page_end=row[7],
            text_char_count=row[8],
        )
        for row in rows
    ]


def list_book_sections_by_ids(session: Session, section_ids: list[uuid.UUID]) -> list[BookSection]:
    if not section_ids:
        return []
    sections = session.exec(select(BookSection).where(BookSection.id.in_(section_ids))).all()
    by_id = {section.id: section for section in sections}
    return [by_id[section_id] for section_id in section_ids if section_id in by_id]

```

### app\repositories\learning_progress_repo.py

```py
import uuid
from datetime import datetime

from sqlmodel import Session, delete, select

from app.core.constant import LearningProgressStatus, PlanMode
from app.models.db_models import LearningUnit, LearningUnitProgress, LearningUnitSegment


def get_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress).where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.learning_unit_id == learning_unit_id,
        )
    ).first()


def save_progress(session: Session, progress: LearningUnitProgress) -> LearningUnitProgress:
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


def list_book_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> list[LearningUnitProgress]:
    return list(
        session.exec(
            select(LearningUnitProgress)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
            )
            .order_by(LearningUnitProgress.updated_at)
        ).all()
    )


def get_latest_activity(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> LearningUnitProgress | None:
    return session.exec(
        select(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
            LearningUnitProgress.last_activity_at.is_not(None),
        )
        .order_by(LearningUnitProgress.last_activity_at.desc())
    ).first()


def has_studied_book_between(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    start_utc: datetime,
    end_utc: datetime,
) -> bool:
    return (
        session.exec(
            select(LearningUnitProgress.id)
            .where(
                LearningUnitProgress.user_id == user_id,
                LearningUnitProgress.book_id == book_id,
                LearningUnitProgress.mode == mode,
                LearningUnitProgress.last_activity_at >= start_utc,
                LearningUnitProgress.last_activity_at < end_utc,
            )
            .limit(1)
        ).first()
        is not None
    )


def list_playable_unit_ids(session: Session, *, book_id: uuid.UUID, mode: PlanMode) -> list[uuid.UUID]:
    rows = session.exec(
        select(LearningUnit.id)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)
        .group_by(LearningUnit.id, LearningUnit.unit_index)
        .order_by(LearningUnit.unit_index)
    ).all()
    return list(rows)


def has_playable_uncompleted_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> bool:
    """
    Kiểm tra xem cuốn sách còn bài học nào có thể phát (playable) mà user chưa hoàn thành không.
    Tối ưu hóa: Dùng LEFT OUTER JOIN trực tiếp ở tầng DB Engine, giới hạn LIMIT 1, RAM/CPU gần như bằng 0.
    """
    statement = (
        select(LearningUnit.id)
        # 1. Kết nối với Segment để đảm bảo bài học đó có dữ liệu âm thanh phát được (Playable)
        .join(LearningUnitSegment, LearningUnitSegment.learning_unit_id == LearningUnit.id)
        # 2. LEFT OUTER JOIN với bảng tiến độ của User cụ thể để tìm những bài chưa hoàn thành
        .join(
            LearningUnitProgress,
            (LearningUnitProgress.learning_unit_id == LearningUnit.id) & (LearningUnitProgress.user_id == user_id) & (LearningUnitProgress.status == LearningProgressStatus.COMPLETED),
            isouter=True,  # LEFT OUTER JOIN
        )
        # 3. Lọc theo thông tin sách và chế độ học
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)
        # 4. Điều kiện chí mạng: Bản ghi tiến độ COMPLETED phải KHÔNG tồn tại (IS NULL)
        .where(LearningUnitProgress.id.is_(None))
        # 5. Chỉ cần tìm thấy 1 bài thỏa mãn là đủ kết luận, không quét toàn bộ DB
        .limit(1)
    )

    # Thực thi câu lệnh
    result = session.exec(statement).first()

    # Nếu kết quả khác None nghĩa là tồn tại ít nhất 1 bài playable chưa completed -> True
    return result is not None


# def has_playable_uncompleted_unit(
#     session: Session,
#     *,
#     user_id: uuid.UUID,
#     book_id: uuid.UUID,
#     mode: PlanMode,
# ) -> bool:
#     playable_ids = set(list_playable_unit_ids(session, book_id=book_id, mode=mode))
#     if not playable_ids:
#         return False

#     completed_ids = set(
#         session.exec(
#             select(LearningUnitProgress.learning_unit_id).where(
#                 LearningUnitProgress.user_id == user_id,
#                 LearningUnitProgress.book_id == book_id,
#                 LearningUnitProgress.mode == mode,
#                 LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
#             )
#         ).all()
#     )
#     return bool(playable_ids - completed_ids)


def delete_book_progress(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ tiến độ các bài học của user đối với sách và mode nhất định."""
    session.execute(
        delete(LearningUnitProgress)
        .where(
            LearningUnitProgress.user_id == user_id,
            LearningUnitProgress.book_id == book_id,
            LearningUnitProgress.mode == mode,
        )
    )

```

### app\repositories\learning_unit_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, col, func, select

from app.core.constant import PlanMode, ProcessingJobStatus
from app.models.db_models import BookSection, LearningUnit, LearningUnitSegment, LearningUnitSource
from app.services.learning_unit_planner_service import PlannedLearningUnit


def delete_learning_units_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: PlanMode) -> None:
    units = session.exec(select(LearningUnit).where(LearningUnit.book_id == book_id, LearningUnit.mode == mode)).all()
    for unit in units:
        session.delete(unit)


def create_learning_units(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    planned_units: list[PlannedLearningUnit],
) -> list[LearningUnit]:
    delete_learning_units_by_book_and_mode(session, book_id, mode)
    session.flush()

    created: list[LearningUnit] = []
    for unit_index, planned in enumerate(planned_units):
        unit = LearningUnit(
            user_id=user_id,
            book_id=book_id,
            mode=mode,
            unit_index=unit_index,
            title=planned.title,
            unit_type=planned.unit_type,
            status=ProcessingJobStatus.QUEUED,
            source_text_char_count=planned.source_text_char_count,
            estimated_tokens=planned.estimated_tokens,
            estimated_audio_seconds=planned.estimated_audio_seconds,
            planner_reason=planned.planner_reason,
        )
        session.add(unit)
        session.flush()

        for source_order, section_id in enumerate(planned.source_section_ids):
            session.add(
                LearningUnitSource(
                    learning_unit_id=unit.id,
                    section_id=section_id,
                    source_order=source_order,
                )
            )

        created.append(unit)

    return created


def list_learning_units(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> list[LearningUnit]:
    mode_value = PlanMode(mode)
    try:
        return list(
            session.exec(
                select(LearningUnit)
                .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
                .order_by(col(LearningUnit.unit_index))
            ).all()
        )
    except ProgrammingError as exc:
        if "learning_units" in str(exc) and "does not exist" in str(exc):
            session.rollback()
            return []
        raise


def get_learning_unit_by_book(session: Session, *, book_id: uuid.UUID, learning_unit_id: uuid.UUID) -> LearningUnit | None:
    return session.exec(select(LearningUnit).where(LearningUnit.id == learning_unit_id, LearningUnit.book_id == book_id)).first()


def get_learning_unit_source_text_map(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> dict[uuid.UUID, str]:
    mode_value = PlanMode(mode)
    rows = session.exec(
        select(LearningUnit, LearningUnitSource, BookSection)
        .join(LearningUnitSource, LearningUnitSource.learning_unit_id == LearningUnit.id)
        .join(BookSection, BookSection.id == LearningUnitSource.section_id)
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
        .order_by(col(LearningUnit.unit_index), col(LearningUnitSource.source_order))
    ).all()

    result: dict[uuid.UUID, list[str]] = {}
    for unit, _source, section in rows:
        if section.text_content and section.text_content.strip():
            result.setdefault(unit.id, []).append(section.text_content.strip())

    return {unit_id: "\n\n".join(parts).strip() for unit_id, parts in result.items()}


def update_learning_unit_processing(
    session: Session,
    unit: LearningUnit,
    *,
    status: ProcessingJobStatus,
    raw_text_char_count: int | None = None,
    estimated_tokens: int | None = None,
    estimated_audio_seconds: int | None = None,
    main_segment_count: int | None = None,
    error_message: str | None = None,
) -> LearningUnit:
    now = datetime.now(timezone.utc)
    unit.status = status
    unit.updated_at = now
    unit.error_message = error_message
    if raw_text_char_count is not None:
        unit.source_text_char_count = raw_text_char_count
    if estimated_tokens is not None:
        unit.estimated_tokens = estimated_tokens
    if estimated_audio_seconds is not None:
        unit.estimated_audio_seconds = estimated_audio_seconds
    if main_segment_count is not None:
        unit.main_segment_count = main_segment_count
    if status == ProcessingJobStatus.PROCESSING:
        unit.started_at = now
        unit.finished_at = None
    if status in (ProcessingJobStatus.READY, ProcessingJobStatus.ERROR, ProcessingJobStatus.CANCELLED):
        unit.finished_at = now
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit


def update_learning_unit_review(session: Session, unit_id: uuid.UUID, *, review_text: str, review_audio_url: str | None) -> None:
    unit = session.get(LearningUnit, unit_id)
    if not unit:
        return
    unit.review_text = review_text
    if review_audio_url:
        unit.review_audio_url = review_audio_url
    unit.updated_at = datetime.now(timezone.utc)
    session.add(unit)
    session.commit()


def bulk_create_unit_segments(session: Session, segments: list[LearningUnitSegment]) -> None:
    for segment in segments:
        session.add(segment)
    session.commit()


def delete_unit_segments(session: Session, learning_unit_id: uuid.UUID) -> None:
    segments = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id == learning_unit_id)).all()
    for segment in segments:
        session.delete(segment)
    session.commit()


def unit_segments_exist(session: Session, learning_unit_id: uuid.UUID) -> bool:
    return session.exec(select(LearningUnitSegment.id).where(LearningUnitSegment.learning_unit_id == learning_unit_id).limit(1)).first() is not None


def count_unit_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: PlanMode | str) -> int:
    mode_value = PlanMode(mode)
    result = session.exec(
        select(func.count(LearningUnitSegment.id))
        .join(LearningUnit, LearningUnitSegment.learning_unit_id == LearningUnit.id)  # type: ignore[arg-type]
        .where(LearningUnit.book_id == book_id, LearningUnit.mode == mode_value)
    ).one()
    return result or 0


def list_unit_segments(session: Session, learning_unit_ids: list[uuid.UUID]) -> list[LearningUnitSegment]:
    if not learning_unit_ids:
        return []
    return list(
        session.exec(
            select(LearningUnitSegment)
            .where(LearningUnitSegment.learning_unit_id.in_(learning_unit_ids))
            .order_by(LearningUnitSegment.learning_unit_id, LearningUnitSegment.segment_index)
        ).all()
    )

```

### app\repositories\notification_outbox_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, select

from app.core.constant import NotificationStatus
from app.models.db_models import NotificationOutbox


def create_outbox_once(session: Session, outbox: NotificationOutbox) -> NotificationOutbox | None:
    try:
        session.add(outbox)
        session.commit()
        session.refresh(outbox)
        return outbox
    except IntegrityError:
        session.rollback()
        return None


def get_outbox_by_id(session: Session, outbox_id: uuid.UUID) -> NotificationOutbox | None:
    return session.get(NotificationOutbox, outbox_id)


def get_outbox_by_idempotency_key(session: Session, idempotency_key: str) -> NotificationOutbox | None:
    return session.exec(select(NotificationOutbox).where(NotificationOutbox.idempotency_key == idempotency_key)).first()


def recover_stale_outbox(
    session: Session,
    *,
    now: datetime,
    stale_before: datetime,
    max_attempts: int,
) -> int:
    rows = list(
        session.exec(
            select(NotificationOutbox).where(NotificationOutbox.status == NotificationStatus.PROCESSING).where(NotificationOutbox.locked_at < stale_before).with_for_update(skip_locked=True)
        ).all()
    )

    recovered = 0
    for row in rows:
        if row.attempts >= max_attempts:
            row.status = NotificationStatus.FAILED
            row.error_message = row.error_message or "Notification delivery exceeded max attempts."
        else:
            row.status = NotificationStatus.PENDING
            row.locked_at = None
            row.locked_by = None
            row.next_retry_at = now
            recovered += 1
        row.updated_at = now
        session.add(row)

    session.commit()
    return recovered


def has_due_outbox(session: Session, *, now: datetime) -> bool:
    return (
        session.exec(
            select(NotificationOutbox.id)
            .where(NotificationOutbox.status == NotificationStatus.PENDING)
            .where(NotificationOutbox.due_at <= now)
            .where((NotificationOutbox.next_retry_at.is_(None)) | (NotificationOutbox.next_retry_at <= now))
            .limit(1)
        ).first()
        is not None
    )


def claim_due_outbox(
    session: Session,
    *,
    now: datetime,
    limit: int,
    worker_id: str,
) -> list[uuid.UUID]:
    rows = list(
        session.exec(
            select(NotificationOutbox)
            .where(NotificationOutbox.status == NotificationStatus.PENDING)
            .where(NotificationOutbox.due_at <= now)
            .where((NotificationOutbox.next_retry_at.is_(None)) | (NotificationOutbox.next_retry_at <= now))
            .order_by(NotificationOutbox.due_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        ).all()
    )

    ids: list[uuid.UUID] = []
    for row in rows:
        row.status = NotificationStatus.PROCESSING
        row.locked_at = now
        row.locked_by = worker_id
        row.attempts += 1
        row.error_message = None
        row.updated_at = now
        ids.append(row.id)
        session.add(row)

    session.commit()
    return ids


def mark_outbox_sent(session: Session, outbox: NotificationOutbox, *, now: datetime | None = None) -> NotificationOutbox:
    current_time = now or datetime.now(timezone.utc)
    outbox.status = NotificationStatus.SENT
    outbox.sent_at = current_time
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.next_retry_at = None
    outbox.error_message = None
    outbox.updated_at = current_time
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def mark_outbox_retry(
    session: Session,
    outbox: NotificationOutbox,
    *,
    next_retry_at: datetime,
    error_message: str,
) -> NotificationOutbox:
    outbox.status = NotificationStatus.PENDING
    outbox.next_retry_at = next_retry_at
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.error_message = error_message[:1000]
    outbox.updated_at = datetime.now(timezone.utc)
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def mark_outbox_failed(session: Session, outbox: NotificationOutbox, *, error_message: str) -> NotificationOutbox:
    outbox.status = NotificationStatus.FAILED
    outbox.locked_at = None
    outbox.locked_by = None
    outbox.error_message = error_message[:1000]
    outbox.updated_at = datetime.now(timezone.utc)
    session.add(outbox)
    session.commit()
    session.refresh(outbox)
    return outbox


def count_outbox_for_user_between(
    session: Session,
    *,
    user_id: uuid.UUID,
    start_utc: datetime,
    end_utc: datetime,
) -> int:
    count = session.exec(
        select(func.count(NotificationOutbox.id)).where(
            NotificationOutbox.user_id == user_id,
            NotificationOutbox.due_at >= start_utc,
            NotificationOutbox.due_at < end_utc,
            NotificationOutbox.status != NotificationStatus.CANCELLED,
            NotificationOutbox.status != NotificationStatus.FAILED,
        )
    ).one()
    return int(count or 0)


def delete_pending_outbox_by_keys(session: Session, *, keys: list[str]) -> None:
    """Xóa toàn bộ các thông báo đang chờ gửi (status = PENDING) có idempotency_key thuộc danh sách."""
    if not keys:
        return
    session.execute(
        delete(NotificationOutbox)
        .where(NotificationOutbox.status == NotificationStatus.PENDING)
        .where(NotificationOutbox.idempotency_key.in_(keys))
    )

```

### app\repositories\notification_settings_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.config import settings
from app.models.db_models import NotificationSettings

MIN_DAILY_CAP = 0
MAX_DAILY_CAP = 10


def _normalize_notification_settings(session: Session, notification_settings: NotificationSettings) -> NotificationSettings:
    safe_daily_cap = min(max(notification_settings.daily_cap, MIN_DAILY_CAP), MAX_DAILY_CAP)
    if notification_settings.daily_cap != safe_daily_cap:
        notification_settings.daily_cap = safe_daily_cap
        notification_settings.updated_at = datetime.now(timezone.utc)
        session.add(notification_settings)
        session.commit()
        session.refresh(notification_settings)
    return notification_settings


def get_notification_settings(session: Session, user_id: uuid.UUID) -> NotificationSettings | None:
    notification_settings = session.get(NotificationSettings, user_id)
    if not notification_settings:
        return None
    return _normalize_notification_settings(session, notification_settings)


def get_or_create_notification_settings(session: Session, user_id: uuid.UUID) -> NotificationSettings:
    existing = get_notification_settings(session, user_id)
    if existing:
        return _normalize_notification_settings(session, existing)

    new_settings = NotificationSettings(
        user_id=user_id,
        timezone=settings.NOTIFICATION_DEFAULT_TIMEZONE,
        reminder_time=settings.NOTIFICATION_DEFAULT_REMINDER_TIME,
        daily_cap=settings.NOTIFICATION_DEFAULT_DAILY_CAP,
        quiet_hours_start=settings.NOTIFICATION_DEFAULT_QUIET_START,
        quiet_hours_end=settings.NOTIFICATION_DEFAULT_QUIET_END,
    )
    try:
        session.add(new_settings)
        session.commit()
        session.refresh(new_settings)
        return new_settings
    except IntegrityError:
        session.rollback()
        existing = get_notification_settings(session, user_id)
        if existing:
            return existing
        raise


def update_notification_settings(
    session: Session,
    user_id: uuid.UUID,
    *,
    timezone_name: str,
    reminders_enabled: bool,
    spaced_review_enabled: bool,
    reminder_time: str,
    quiet_hours_start: str,
    quiet_hours_end: str,
    daily_cap: int,
) -> NotificationSettings:
    notification_settings = get_or_create_notification_settings(session, user_id)
    notification_settings.timezone = timezone_name
    notification_settings.reminders_enabled = reminders_enabled
    notification_settings.spaced_review_enabled = spaced_review_enabled
    notification_settings.reminder_time = reminder_time
    notification_settings.quiet_hours_start = quiet_hours_start
    notification_settings.quiet_hours_end = quiet_hours_end
    notification_settings.daily_cap = daily_cap
    notification_settings.updated_at = datetime.now(timezone.utc)
    session.add(notification_settings)
    session.commit()
    session.refresh(notification_settings)
    return notification_settings

```

### app\repositories\processing_job_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import ProcessingJobStatus
from app.models.db_models import ProcessingJob


def create_processing_job(session: Session, job: ProcessingJob) -> ProcessingJob:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_processing_job_by_id(session: Session, job_id: uuid.UUID) -> ProcessingJob | None:
    return session.get(ProcessingJob, job_id)


def get_processing_job_by_id_and_user(session: Session, job_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(select(ProcessingJob).where(ProcessingJob.id == job_id, ProcessingJob.user_id == user_id)).first()


def get_latest_processing_job_for_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(
        select(ProcessingJob)
        .where(
            ProcessingJob.book_id == book_id,
            ProcessingJob.user_id == user_id,
        )
        .order_by(ProcessingJob.created_at.desc())
    ).first()


def update_processing_job(
    session: Session,
    job_id: uuid.UUID,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    estimated_input_tokens: int | None = None,
    estimated_audio_seconds: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> ProcessingJob | None:
    job = session.get(ProcessingJob, job_id)
    if not job:
        return None

    updates = {
        "status": status,
        "current_step": current_step,
        "total_units": total_units,
        "done_units": done_units,
        "failed_units": failed_units,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_audio_seconds": estimated_audio_seconds,
        "error_message": error_message,
        "started_at": started_at,
        "finished_at": finished_at,
    }
    for field_name, value in updates.items():
        if value is not None:
            setattr(job, field_name, value)

    if progress_percent is not None:
        job.progress_percent = max(0, min(100, progress_percent))

    job.updated_at = datetime.now(timezone.utc)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

```

### app\repositories\reading_plan_repo.py

```py
import uuid

from sqlmodel import Session, col, select

from app.core.constant import PlanMode, PlanStatus
from app.models.db_models import Book, ReadingPlan


def get_current_plan_for_owned_book(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
) -> ReadingPlan | None:
    return session.exec(
        select(ReadingPlan)
        .join(Book, Book.id == ReadingPlan.book_id)
        .where(
            Book.id == book_id,
            Book.user_id == user_id,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()


def get_plan_for_book_mode(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> ReadingPlan | None:
    return session.exec(
        select(ReadingPlan)
        .where(
            ReadingPlan.book_id == book_id,
            ReadingPlan.mode == mode,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()


def list_plans_for_book_mode(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> list[ReadingPlan]:
    return list(
        session.exec(
            select(ReadingPlan)
            .where(
                ReadingPlan.book_id == book_id,
                ReadingPlan.mode == mode,
                ReadingPlan.status != PlanStatus.ERROR.value,
            )
            .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
        ).all()
    )

```

### app\repositories\reading_plan_schedule_repo.py

```py
import uuid

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, delete, select

from app.models.db_models import ReadingPlanScheduleSlot


def count_active_learning_books(session: Session, *, user_id: uuid.UUID) -> int:
    rows = session.exec(
        select(ReadingPlanScheduleSlot.book_id)
        .where(
            ReadingPlanScheduleSlot.user_id == user_id,
            ReadingPlanScheduleSlot.is_active.is_(True),
        )
        .distinct()
    ).all()
    return len(rows)


def find_conflicting_slot(
    session: Session,
    *,
    user_id: uuid.UUID,
    weekday: int,
    reminder_time: str,
    exclude_plan_id: uuid.UUID | None = None,
) -> ReadingPlanScheduleSlot | None:
    statement = select(ReadingPlanScheduleSlot).where(
        ReadingPlanScheduleSlot.user_id == user_id,
        ReadingPlanScheduleSlot.weekday == weekday,
        ReadingPlanScheduleSlot.reminder_time == reminder_time,
        ReadingPlanScheduleSlot.is_active.is_(True),
    )
    if exclude_plan_id:
        statement = statement.where(ReadingPlanScheduleSlot.plan_id != exclude_plan_id)
    return session.exec(statement).first()


def list_active_slots(session: Session, *, user_id: uuid.UUID) -> list[ReadingPlanScheduleSlot]:
    return list(
        session.exec(
            select(ReadingPlanScheduleSlot)
            .where(ReadingPlanScheduleSlot.user_id == user_id, ReadingPlanScheduleSlot.is_active.is_(True))
            .order_by(col(ReadingPlanScheduleSlot.weekday), col(ReadingPlanScheduleSlot.reminder_time))
        ).all()
    )


def list_slots_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    active_only: bool = True,
) -> list[ReadingPlanScheduleSlot]:
    statement = select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id)
    if active_only:
        statement = statement.where(ReadingPlanScheduleSlot.is_active.is_(True))
    statement = statement.order_by(col(ReadingPlanScheduleSlot.weekday), col(ReadingPlanScheduleSlot.reminder_time))
    return list(session.exec(statement).all())


def create_slots_for_plan(
    session: Session,
    *,
    slots: list[ReadingPlanScheduleSlot],
) -> list[ReadingPlanScheduleSlot]:
    try:
        for slot in slots:
            session.add(slot)
        session.commit()
        for slot in slots:
            session.refresh(slot)
        return slots
    except IntegrityError:
        session.rollback()
        raise


def delete_slots_for_plan(session: Session, *, plan_id: uuid.UUID) -> int:
    statement = delete(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.plan_id == plan_id)
    result = session.exec(statement)
    return int(result.rowcount or 0)


def set_slots_active(session: Session, *, plan_id: uuid.UUID, is_active: bool) -> int:
    slots = list_slots_for_plan(session, plan_id=plan_id, active_only=False)
    for slot in slots:
        slot.is_active = is_active
        session.add(slot)
    return len(slots)


def replace_slots_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    slots: list[ReadingPlanScheduleSlot],
) -> list[ReadingPlanScheduleSlot]:
    delete_slots_for_plan(session, plan_id=plan_id)
    for slot in slots:
        session.add(slot)
    return slots

```

### app\repositories\reading_plan_session_repo.py

```py
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Session, col, delete, func, select

from app.core.constant import PlanMode, ReadingPlanSessionStatus
from app.models.db_models import ReadingPlanSession, ReadingPlanSessionUnit

FINAL_SESSION_STATUSES = {
    ReadingPlanSessionStatus.COMPLETED.value,
    ReadingPlanSessionStatus.SKIPPED.value,
    ReadingPlanSessionStatus.CANCELLED.value,
}
ACTIVE_SESSION_STATUSES = {
    ReadingPlanSessionStatus.SCHEDULED.value,
    ReadingPlanSessionStatus.DUE.value,
    ReadingPlanSessionStatus.IN_PROGRESS.value,
    ReadingPlanSessionStatus.MISSED.value,
}


@dataclass(frozen=True)
class PlanSessionSummaryCounts:
    total_sessions: int
    completed_sessions: int
    missed_sessions: int


def get_owned_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession).where(
            ReadingPlanSession.id == session_id,
            ReadingPlanSession.user_id == user_id,
        )
    ).first()


def list_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(ReadingPlanSession.plan_id == plan_id)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_sessions_for_book(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode | None = None,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.book_id == book_id,
    )
    if mode:
        statement = statement.where(ReadingPlanSession.mode == mode)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_sessions_for_user_local_date(
    session: Session,
    *,
    user_id: uuid.UUID,
    local_date: str,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.local_date == local_date,
    )
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def list_sessions_for_user_range(
    session: Session,
    *,
    user_id: uuid.UUID,
    from_local_date: str,
    to_local_date: str,
    book_id: uuid.UUID | None = None,
    mode: PlanMode | None = None,
    status: str | None = None,
    include_cancelled: bool = False,
) -> list[ReadingPlanSession]:
    statement = select(ReadingPlanSession).where(
        ReadingPlanSession.user_id == user_id,
        ReadingPlanSession.local_date >= from_local_date,
        ReadingPlanSession.local_date <= to_local_date,
    )
    if book_id:
        statement = statement.where(ReadingPlanSession.book_id == book_id)
    if mode:
        statement = statement.where(ReadingPlanSession.mode == mode)
    if status:
        statement = statement.where(ReadingPlanSession.status == status)
    if not include_cancelled:
        statement = statement.where(ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value)
    statement = statement.order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    return list(session.exec(statement).all())


def get_plan_session_summary_counts(session: Session, *, plan_id: uuid.UUID) -> PlanSessionSummaryCounts:
    rows = session.exec(
        select(ReadingPlanSession.status, func.count(ReadingPlanSession.id))
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value,
        )
        .group_by(ReadingPlanSession.status)
    ).all()
    counts = {status: int(count or 0) for status, count in rows}
    return PlanSessionSummaryCounts(
        total_sessions=sum(counts.values()),
        completed_sessions=counts.get(ReadingPlanSessionStatus.COMPLETED.value, 0),
        missed_sessions=counts.get(ReadingPlanSessionStatus.MISSED.value, 0),
    )


def get_next_session_for_plan(session: Session, *, plan_id: uuid.UUID) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession)
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status.notin_(list(FINAL_SESSION_STATUSES)),
        )
        .order_by(col(ReadingPlanSession.scheduled_at), col(ReadingPlanSession.session_index))
    ).first()


def find_session_schedule_conflict(
    session: Session,
    *,
    user_id: uuid.UUID,
    scheduled_at: datetime,
    exclude_session_id: uuid.UUID,
) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession)
        .where(
            ReadingPlanSession.user_id == user_id,
            ReadingPlanSession.scheduled_at == scheduled_at,
            ReadingPlanSession.id != exclude_session_id,
            ReadingPlanSession.status.in_(list(ACTIVE_SESSION_STATUSES)),
        )
        .order_by(col(ReadingPlanSession.scheduled_at))
    ).first()


def list_due_reminder_sessions(
    session: Session,
    *,
    now: datetime,
    limit: int,
) -> list[ReadingPlanSession]:
    return list(
        session.exec(
            select(ReadingPlanSession)
            .where(ReadingPlanSession.scheduled_at <= now)
            .where(
                ReadingPlanSession.status.in_(
                    [
                        ReadingPlanSessionStatus.SCHEDULED.value,
                        ReadingPlanSessionStatus.DUE.value,
                    ]
                )
            )
            .order_by(col(ReadingPlanSession.scheduled_at))
            .limit(limit)
        ).all()
    )


def get_session_unit_for_learning_unit(
    session: Session,
    *,
    plan_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> ReadingPlanSessionUnit | None:
    return session.exec(
        select(ReadingPlanSessionUnit).where(
            ReadingPlanSessionUnit.plan_id == plan_id,
            ReadingPlanSessionUnit.learning_unit_id == learning_unit_id,
        )
    ).first()


def list_session_units(session: Session, *, session_ids: list[uuid.UUID]) -> list[ReadingPlanSessionUnit]:
    if not session_ids:
        return []
    return list(
        session.exec(
            select(ReadingPlanSessionUnit)
            .where(ReadingPlanSessionUnit.session_id.in_(session_ids))
            .order_by(col(ReadingPlanSessionUnit.session_id), col(ReadingPlanSessionUnit.unit_order))
        ).all()
    )


def count_completed_session_units(session: Session, *, session_id: uuid.UUID) -> int:
    result = session.exec(
        select(func.count(ReadingPlanSessionUnit.id)).where(
            ReadingPlanSessionUnit.session_id == session_id,
            ReadingPlanSessionUnit.status == "completed",
        )
    ).one()
    return int(result or 0)


def cancel_unfinished_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    now: datetime,
) -> int:
    rows = session.exec(
        select(ReadingPlanSession).where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status.notin_(list(FINAL_SESSION_STATUSES)),
        )
    ).all()
    for row in rows:
        row.status = ReadingPlanSessionStatus.CANCELLED.value
        row.updated_at = now
        session.add(row)
    return len(rows)


def mark_overdue_sessions_missed_rows(
    session: Session,
    *,
    user_id: uuid.UUID | None,
    now: datetime,
) -> list[ReadingPlanSession]:
    statement = (
        select(ReadingPlanSession)
        .where(ReadingPlanSession.scheduled_at < now)
        .where(
            ReadingPlanSession.status.in_(
                [
                    ReadingPlanSessionStatus.SCHEDULED.value,
                    ReadingPlanSessionStatus.DUE.value,
                    ReadingPlanSessionStatus.IN_PROGRESS.value,
                ]
            )
        )
        .where(ReadingPlanSession.completed_units < ReadingPlanSession.total_units)
    )
    if user_id:
        statement = statement.where(ReadingPlanSession.user_id == user_id)

    rows = list(session.exec(statement).all())
    for row in rows:
        row.status = ReadingPlanSessionStatus.MISSED.value
        row.missed_at = row.missed_at or now
        row.updated_at = now
        session.add(row)
    return rows


def list_missed_sessions_pending_notification(
    session: Session,
    *,
    now: datetime,
    limit: int,
) -> list[ReadingPlanSession]:
    return list(
        session.exec(
            select(ReadingPlanSession)
            .where(ReadingPlanSession.status == ReadingPlanSessionStatus.MISSED.value)
            .where(ReadingPlanSession.missed_at.is_not(None))
            .where(ReadingPlanSession.missed_at <= now)
            .where(ReadingPlanSession.missed_notified_at.is_(None))
            .order_by(col(ReadingPlanSession.missed_at))
            .limit(limit)
        ).all()
    )


def mark_overdue_sessions_missed(
    session: Session,
    *,
    user_id: uuid.UUID | None,
    now: datetime,
) -> int:
    statement = (
        select(ReadingPlanSession)
        .where(ReadingPlanSession.scheduled_at < now)
        .where(
            ReadingPlanSession.status.in_(
                [
                    ReadingPlanSessionStatus.SCHEDULED.value,
                    ReadingPlanSessionStatus.DUE.value,
                    ReadingPlanSessionStatus.IN_PROGRESS.value,
                ]
            )
        )
        .where(ReadingPlanSession.completed_units < ReadingPlanSession.total_units)
    )
    if user_id:
        statement = statement.where(ReadingPlanSession.user_id == user_id)

    rows = session.exec(statement).all()
    for row in rows:
        row.status = ReadingPlanSessionStatus.MISSED.value
        row.missed_at = row.missed_at or now
        row.updated_at = now
        session.add(row)
    return len(rows)


def delete_sessions_for_plan(session: Session, *, plan_id: uuid.UUID) -> None:
    """Xóa toàn bộ các buổi học và chi tiết buổi học của kế hoạch học tập."""
    session.execute(
        delete(ReadingPlanSessionUnit)
        .where(ReadingPlanSessionUnit.plan_id == plan_id)
    )
    session.execute(
        delete(ReadingPlanSession)
        .where(ReadingPlanSession.plan_id == plan_id)
    )

```

### app\repositories\spaced_review_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, func, select

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem


def create_review_item_once(session: Session, item: SpacedReviewItem) -> SpacedReviewItem | None:
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except IntegrityError:
        session.rollback()
        return None


def get_due_review_items(session: Session, *, now: datetime, limit: int = 100) -> list[SpacedReviewItem]:
    return list(
        session.exec(select(SpacedReviewItem).where(SpacedReviewItem.status == ReviewItemStatus.PENDING).where(SpacedReviewItem.due_at <= now).order_by(SpacedReviewItem.due_at).limit(limit)).all()
    )


def mark_review_item_due(session: Session, review_item: SpacedReviewItem) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.DUE
    review_item.notified_at = datetime.now(timezone.utc)
    review_item.updated_at = datetime.now(timezone.utc)
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def defer_review_item(session: Session, review_item: SpacedReviewItem, due_at: datetime) -> SpacedReviewItem:
    review_item.due_at = due_at
    review_item.updated_at = datetime.now(timezone.utc)
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def has_active_review_chain_for_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> bool:
    return (
        session.exec(
            select(SpacedReviewItem.id)
            .where(
                SpacedReviewItem.user_id == user_id,
                SpacedReviewItem.learning_unit_id == learning_unit_id,
                SpacedReviewItem.status != ReviewItemStatus.CANCELLED,
            )
            .limit(1)
        ).first()
        is not None
    )


def cancel_unanchored_review_items_for_unit(
    session: Session,
    *,
    user_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
) -> int:
    rows = session.exec(
        select(SpacedReviewItem).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.learning_unit_id == learning_unit_id,
            SpacedReviewItem.source_unit_progress_id.is_(None),
            SpacedReviewItem.status != ReviewItemStatus.CANCELLED,
        )
    ).all()
    now = datetime.now(timezone.utc)
    for row in rows:
        row.status = ReviewItemStatus.CANCELLED
        row.updated_at = now
        session.add(row)
    session.commit()
    return len(rows)


def get_review_item_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    review_item_id: uuid.UUID,
) -> SpacedReviewItem | None:
    return session.exec(
        select(SpacedReviewItem).where(
            SpacedReviewItem.id == review_item_id,
            SpacedReviewItem.user_id == user_id,
        )
    ).first()


def list_review_items_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    now: datetime,
    status_filter: str = "due",
    book_id: uuid.UUID | None = None,
    mode: PlanMode | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[SpacedReviewItem]:
    statement = select(SpacedReviewItem).where(SpacedReviewItem.user_id == user_id)
    if book_id:
        statement = statement.where(SpacedReviewItem.book_id == book_id)
    if mode:
        statement = statement.where(SpacedReviewItem.mode == mode)

    if status_filter == "due":
        statement = statement.where(
            SpacedReviewItem.status.in_([ReviewItemStatus.DUE, ReviewItemStatus.PENDING]),
            SpacedReviewItem.due_at <= now,
        )
    elif status_filter == "upcoming":
        statement = statement.where(
            SpacedReviewItem.status == ReviewItemStatus.PENDING,
            SpacedReviewItem.due_at > now,
        )
    elif status_filter == "completed":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.COMPLETED)
    elif status_filter == "skipped":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.SKIPPED)
    elif status_filter != "all":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus(status_filter))

    if status_filter == "all":
        statement = statement.where(SpacedReviewItem.status != ReviewItemStatus.CANCELLED)

    return list(session.exec(statement.order_by(SpacedReviewItem.due_at).offset(offset).limit(limit)).all())


def count_review_items_for_user(
    session: Session,
    *,
    user_id: uuid.UUID,
    now: datetime,
    status_filter: str,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> int:
    statement = select(func.count(SpacedReviewItem.id)).where(
        SpacedReviewItem.user_id == user_id,
        SpacedReviewItem.book_id == book_id,
        SpacedReviewItem.mode == mode,
    )

    if status_filter == "due":
        statement = statement.where(
            SpacedReviewItem.status.in_([ReviewItemStatus.DUE, ReviewItemStatus.PENDING]),
            SpacedReviewItem.due_at <= now,
        )
    elif status_filter == "upcoming":
        statement = statement.where(
            SpacedReviewItem.status == ReviewItemStatus.PENDING,
            SpacedReviewItem.due_at > now,
        )
    elif status_filter == "completed":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.COMPLETED)
    elif status_filter == "skipped":
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus.SKIPPED)
    elif status_filter == "all":
        statement = statement.where(SpacedReviewItem.status != ReviewItemStatus.CANCELLED)
    else:
        statement = statement.where(SpacedReviewItem.status == ReviewItemStatus(status_filter))

    result = session.exec(statement).one()
    return int(result or 0)


def mark_review_item_completed(session: Session, review_item: SpacedReviewItem, *, completed_at: datetime) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.COMPLETED
    review_item.completed_at = completed_at
    review_item.last_reviewed_at = completed_at
    review_item.updated_at = completed_at
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def mark_review_item_skipped(session: Session, review_item: SpacedReviewItem, *, skipped_at: datetime) -> SpacedReviewItem:
    review_item.status = ReviewItemStatus.SKIPPED
    review_item.last_reviewed_at = skipped_at
    review_item.updated_at = skipped_at
    session.add(review_item)
    session.commit()
    session.refresh(review_item)
    return review_item


def delete_spaced_review_items(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> None:
    """Xóa toàn bộ các thẻ ôn tập ngắt quãng của user đối với sách và mode nhất định."""
    session.execute(
        delete(SpacedReviewItem)
        .where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    )

```

### app\repositories\study_context_document_link_repo.py

```py
import uuid

from sqlmodel import Session, select

from app.models.db_models import StudyContextDocumentLink


def create_new_context_document(
    session: Session, link: StudyContextDocumentLink
) -> StudyContextDocumentLink:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_context_documents(session: Session, context_id: uuid.UUID) -> list[StudyContextDocumentLink]:
    return session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == context_id)
    ).all()


def delete_study_context_document(session: Session, context_id: uuid.UUID, book_id: uuid.UUID) -> None:
    link = session.exec(
        select(StudyContextDocumentLink).where(
            StudyContextDocumentLink.context_id == context_id, StudyContextDocumentLink.book_id == book_id
        )
    ).first()
    if link:
        session.delete(link)
        session.commit()

```

### app\repositories\study_context_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import StudyContext


def get_study_context(session: Session, context_id: uuid.UUID) -> StudyContext | None:
    return session.get(StudyContext, context_id)


def get_study_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return session.exec(select(StudyContext).where(StudyContext.user_id == user_id)).all()


def create_study_context(session: Session, study_context: StudyContext) -> StudyContext:
    session.add(study_context)
    session.commit()
    session.refresh(study_context)
    return study_context


def update_study_context(
    session: Session, context_id: uuid.UUID, title: str | None = None
) -> StudyContext | None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        if title is not None:
            study_context.title = title
        study_context.updated_at = datetime.now(timezone.utc)
        session.add(study_context)
        session.commit()
        session.refresh(study_context)
        return study_context
    return None


def delete_study_context(session: Session, context_id: uuid.UUID) -> None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        session.delete(study_context)
        session.commit()

```

### app\repositories\study_context_thread_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.exceptions import DirectBookContextConflictError
from app.models.db_models import ChatMessage, ChatThread, DirectBookContext, StudyContext, StudyContextDocumentLink


def get_chat_threads_for_context(session: Session, context_id: uuid.UUID) -> list[ChatThread]:
    threads = session.exec(select(ChatThread).where(
        ChatThread.context_id == context_id)).all()
    return threads


def get_chat_history_by_thread_id(session: Session, thread_id: uuid.UUID) -> list[ChatMessage]:
    messages = session.exec(select(ChatMessage).where(
        ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()
    return messages


def update_thread_by_id_repo(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def get_or_create_thread_for_book_repo(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str) -> tuple[uuid.UUID, uuid.UUID]:
    # Get existing thread for the book
    direct_ctx = session.exec(select(DirectBookContext).where(
        DirectBookContext.book_id == book_id, DirectBookContext.user_id == user_id)).first()

    if direct_ctx:
        return direct_ctx.context_id, direct_ctx.primary_thread_id

    try:

        # Create new context
        new_context = StudyContext(
            user_id=user_id,
            title=title,
            is_auto_generated=True,
        )

        session.add(new_context)
        session.flush()  # To get new_context.id populated

        # Link context with book
        new_study_context_book_link = StudyContextDocumentLink(
            context_id=new_context.id,
            book_id=book_id,
        )
        session.add(new_study_context_book_link)

        # Create new thread

        new_thread = ChatThread(
            context_id=new_context.id,
            title=title,
        )

        session.add(new_thread)
        session.flush()  # To get new_thread.id populated

        # Create new DirectBookContext
        new_direct_ctx = DirectBookContext(
            user_id=user_id,
            book_id=book_id,
            context_id=new_context.id,
            primary_thread_id=new_thread.id,
        )

        session.add(new_direct_ctx)
        session.commit()

        # Final: Return new context_id and thread_id
        return new_context.id, new_thread.id

    except IntegrityError:
        session.rollback()
        raise DirectBookContextConflictError() from None


def create_new_thread(session: Session, thread: ChatThread) -> ChatThread:
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def update_thread_title(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def delete_thread(session: Session, thread_id: uuid.UUID) -> None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        session.delete(thread)
        session.commit()

```

### app\repositories\user_notification_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.db_models import UserNotification


def create_user_notification_once(session: Session, notification: UserNotification) -> UserNotification | None:
    try:
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification
    except IntegrityError:
        session.rollback()
        return None


def list_user_notifications(
    session: Session,
    *,
    user_id: uuid.UUID,
    limit: int,
    unread_only: bool = False,
) -> list[UserNotification]:
    statement = select(UserNotification).where(UserNotification.user_id == user_id)
    if unread_only:
        statement = statement.where(UserNotification.read_at.is_(None))
    return list(session.exec(statement.order_by(UserNotification.created_at.desc()).limit(limit)).all())


def count_unread_notifications(session: Session, *, user_id: uuid.UUID) -> int:
    count = session.exec(
        select(func.count(UserNotification.id)).where(
            UserNotification.user_id == user_id,
            UserNotification.read_at.is_(None),
        )
    ).one()
    return int(count or 0)


def get_user_notification(session: Session, *, user_id: uuid.UUID, notification_id: uuid.UUID) -> UserNotification | None:
    return session.exec(
        select(UserNotification).where(
            UserNotification.id == notification_id,
            UserNotification.user_id == user_id,
        )
    ).first()


def mark_notification_read(session: Session, notification: UserNotification, *, read_at: datetime | None = None) -> UserNotification:
    notification.read_at = read_at or datetime.now(timezone.utc)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


def mark_all_notifications_read(session: Session, *, user_id: uuid.UUID, read_at: datetime | None = None) -> int:
    current_time = read_at or datetime.now(timezone.utc)
    notifications = list(
        session.exec(
            select(UserNotification).where(
                UserNotification.user_id == user_id,
                UserNotification.read_at.is_(None),
            )
        ).all()
    )
    for notification in notifications:
        notification.read_at = current_time
        session.add(notification)
    session.commit()
    return len(notifications)

```

### app\schemas\admin.py

```py
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType


class AdminMeResponse(BaseModel):
    user_id: uuid.UUID
    email: str | None = None
    role: str
    is_active: bool


class AdminDashboardResponse(BaseModel):
    user_count: int
    book_count: int
    job_count: int
    books_by_status: dict[str, int] = Field(default_factory=dict)
    jobs_by_status: dict[str, int] = Field(default_factory=dict)
    failed_jobs_last_24h: int = 0
    estimated_input_tokens_last_30d: int = 0
    estimated_audio_seconds_last_30d: int = 0


class AdminUserListItem(BaseModel):
    user_id: uuid.UUID
    email: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    account_created_at: datetime | None = None
    last_sign_in_at: datetime | None = None
    book_count: int = 0
    job_count: int = 0
    notification_count: int = 0
    last_activity_at: datetime | None = None



class AdminUsersResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AdminUserListItem]


class AdminBookListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    author: str | None = None
    document_type: str | None = None
    status: str | None = None
    total_sections: int | None = None
    total_units: int | None = None
    error_message: str | None = None
    is_shared: bool = False
    parent_shared_id: uuid.UUID | None = None
    has_full_mode: bool = False
    has_pareto_mode: bool = False
    user_email: str | None = None
    user_display_name: str | None = None
    user_avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime


class AdminBooksResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AdminBookListItem]


class AdminJobListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    estimated_input_tokens: int | None = None
    estimated_audio_seconds: int | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class AdminJobsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AdminJobListItem]


class AdminBookOwnerInfo(BaseModel):
    user_id: uuid.UUID
    email: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    account_created_at: datetime | None = None
    last_sign_in_at: datetime | None = None


class AdminBookSectionListItem(BaseModel):
    id: uuid.UUID
    section_index: int
    title: str
    level: int
    path: str
    text_char_count: int
    page_start: int | None = None
    page_end: int | None = None
    modes: list[str] = []
    chunk_count: int = 0
    has_text: bool = False


class AdminSectionChunkItem(BaseModel):
    id: int
    chunk_index: int
    content: str
    search_text: str
    embedding_model: str
    embedding_version: str
    char_count: int
    token_count: int | None = None
    has_embedding: bool = False


class AdminBookSectionDetailResponse(BaseModel):
    id: uuid.UUID
    section_index: int
    title: str
    level: int
    path: str
    text_content: str | None = None
    text_char_count: int
    page_start: int | None = None
    page_end: int | None = None
    chunks: list[AdminSectionChunkItem] = []


class AdminBookDetailResponse(AdminBookListItem):
    latest_job: AdminJobListItem | None = None
    learning_units_by_status: dict[str, int] = Field(default_factory=dict)
    segment_count: int = 0
    owner_info: AdminBookOwnerInfo | None = None


class AdminRetryJobResponse(BaseModel):
    job: AdminJobListItem
    message: str


class AdminAuditLogItem(BaseModel):
    id: uuid.UUID
    admin_user_id: uuid.UUID
    action: str
    target_type: str | None = None
    target_id: uuid.UUID | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime


class AdminAuditLogsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AdminAuditLogItem]


class AdminExportChunkItem(BaseModel):
    chunk_index: int
    content: str
    embedding_model: str
    embedding_version: str
    token_count: int | None = None
    has_embedding: bool = False


class AdminExportSectionItem(BaseModel):
    section_index: int
    title: str
    level: int
    path: str
    page_start: int | None = None
    page_end: int | None = None
    modes: list[str] = []
    chunks: list[AdminExportChunkItem] = []


class AdminBookExportResponse(BaseModel):
    book_id: uuid.UUID
    title: str
    author: str | None = None
    document_type: str | None = None
    sections: list[AdminExportSectionItem] = []

```

### app\schemas\audiobook.py

```py
from pydantic import BaseModel, Field


class BookCreateRequest(BaseModel):
    """DTO cho input khi tạo mới sách thủ công."""

    title: str = Field(min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)


class BookUpdateRequest(BaseModel):
    """DTO cho input khi cập nhật metadata sách."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)

```

### app\schemas\learning_progress.py

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constant import BookLearningStatus, LearningProgressStatus, PlanMode


class LearningUnitProgressUpdateRequest(BaseModel):
    mode: PlanMode
    segment_id: int | None = None
    segment_index: int = Field(ge=0)
    position_ms: int = Field(ge=0)
    listened_ms: int = Field(default=0, ge=0)
    total_duration_ms: int | None = Field(default=None, ge=0)
    progress_percent: int | None = Field(default=None, ge=0, le=100)
    force_persist: bool = False


class ManualLearningUnitCompleteRequest(BaseModel):
    mode: PlanMode


class LearningUnitProgressResponse(BaseModel):
    learning_unit_id: uuid.UUID
    mode: PlanMode
    segment_id: int | None = None
    segment_index: int
    position_ms: int
    progress_percent: int
    max_progress_percent: int
    status: LearningProgressStatus
    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    completed_at: datetime | None = None


class BookLearningSummaryResponse(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    learning_status: BookLearningStatus
    is_completed: bool
    can_resume: bool
    can_review: bool
    book_progress_percent: int
    completed_units: int
    playable_units: int
    last_learning_unit_id: uuid.UUID | None = None
    last_segment_id: int | None = None
    last_segment_index: int | None = None
    position_ms: int | None = None
    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    completed_at: datetime | None = None
    due_reviews_count: int = 0
    upcoming_reviews_count: int = 0


class BookLearningProgressResponse(BookLearningSummaryResponse):
    units: list[LearningUnitProgressResponse]

```

### app\schemas\notification.py

```py
import re
import uuid
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constant import NotificationType

HHMM_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def _validate_hhmm(value: str) -> str:
    if not HHMM_PATTERN.match(value):
        raise ValueError("Time must use HH:MM 24-hour format.")
    return value


class NotificationSettingsRequest(BaseModel):
    timezone: str = "Asia/Ho_Chi_Minh"
    reminders_enabled: bool = True
    spaced_review_enabled: bool = True
    reminder_time: str = "20:00"
    quiet_hours_start: str = "22:00"
    quiet_hours_end: str = "07:00"
    daily_cap: int = Field(default=3, ge=0, le=10)

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Invalid IANA timezone.") from exc
        return value

    @field_validator("reminder_time", "quiet_hours_start", "quiet_hours_end")
    @classmethod
    def validate_time(cls, value: str) -> str:
        return _validate_hhmm(value)


class NotificationSettingsResponse(NotificationSettingsRequest):
    user_id: uuid.UUID


class UserNotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: NotificationType
    title: str
    body: str
    action_type: str | None = None
    action_payload: dict[str, Any] | None = None
    read_at: datetime | None = None
    created_at: datetime


class NotificationListResponse(BaseModel):
    items: list[UserNotificationResponse]
    unread_count: int


class MarkNotificationReadResponse(BaseModel):
    id: uuid.UUID
    read_at: datetime


class MarkAllNotificationsReadResponse(BaseModel):
    updated_count: int
    read_at: datetime


class DeviceTokenRegisterRequest(BaseModel):
    device_token: str = Field(..., min_length=1, description="Firebase registration token")


class DeviceTokenResponse(BaseModel):
    device_token: str
    user_id: uuid.UUID
    created_at: datetime

```

### app\schemas\plan.py

```py
import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.core.constant import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số learning unit mỗi buổi học
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]; request-only compatibility field
    reminder_time: str | None = None  # VD: "20:00", nếu None sẽ lấy từ user settings
    activate: bool = False  # False: chỉ cấu hình/generate, True: active lịch ngay


class SwitchModeRequest(BaseModel):
    mode: PlanMode


class PlanUpdateRequest(BaseModel):
    pace: int | None = None
    schedule_config: list[str] | None = None
    reminder_time: str | None = None  # HH:MM format


class ReadingPlanSlotResponse(BaseModel):
    id: uuid.UUID
    weekday: int
    weekday_label: str
    reminder_time: str
    timezone: str
    is_active: bool


class ReadingPlanUserSlotResponse(ReadingPlanSlotResponse):
    plan_id: uuid.UUID
    book_id: uuid.UUID


class ReadingPlanSessionUnitResponse(BaseModel):
    id: uuid.UUID
    learning_unit_id: uuid.UUID
    unit_title: str = ""
    unit_order: int
    status: str
    completed_at: datetime | None = None


class ReadingPlanSessionResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    book_id: uuid.UUID
    mode: PlanMode
    session_index: int
    scheduled_at: datetime
    local_date: str
    reminder_time: str
    timezone: str
    status: str
    completed_units: int
    total_units: int
    is_overdue: bool
    started_at: datetime | None = None
    completed_at: datetime | None = None
    missed_at: datetime | None = None
    skipped_at: datetime | None = None
    units: list[ReadingPlanSessionUnitResponse] = Field(default_factory=list)


class ReadingPlanSessionListResponse(BaseModel):
    book_id: uuid.UUID | None = None
    local_date: str | None = None
    timezone: str | None = None
    total: int
    items: list[ReadingPlanSessionResponse] = Field(default_factory=list)


class ReadingPlanSessionRangeResponse(ReadingPlanSessionListResponse):
    from_date: date
    to_date: date
    summary: dict[str, int] = Field(default_factory=dict)


class ReadingPlanSessionSkipRequest(BaseModel):
    reason: str | None = None


class ReadingPlanSessionRescheduleRequest(BaseModel):
    local_date: date
    reminder_time: str
    timezone: str | None = None


class ReadingPlanSessionActionResponse(BaseModel):
    message: str
    session: ReadingPlanSessionResponse


class ReadingPlanSessionSummaryResponse(BaseModel):
    total_sessions: int = 0
    completed_sessions: int = 0
    missed_sessions: int = 0
    next_session: ReadingPlanSessionResponse | None = None


class ReadingPlanResponse(BaseModel):
    plan_id: uuid.UUID
    book_id: uuid.UUID
    mode: PlanMode
    pace: int
    schedule_config: list[str] = Field(default_factory=list)
    reminder_time: str
    status: str
    plan_status: str
    active_slots: list[ReadingPlanSlotResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    paused_at: datetime | None = None
    completed_at: datetime | None = None
    session_summary: ReadingPlanSessionSummaryResponse | None = None


class ReadingPlanUpdateResponse(ReadingPlanResponse):
    message: str

```

### app\schemas\processing_job.py

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType


class ProcessingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    estimated_input_tokens: int | None = None
    estimated_audio_seconds: int | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ProcessingJobSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    estimated_input_tokens: int | None = None
    estimated_audio_seconds: int | None = None
    error_message: str | None = None

```

### app\schemas\responses\audiobook_res.py

```py
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.constant import DocumentType
from app.schemas.learning_progress import BookLearningSummaryResponse


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    author: Optional[str] = None
    total_sections: Optional[int] = None
    total_units: Optional[int] = None
    status: Optional[str] = None
    learning_status: Optional[str] = None
    book_progress_percent: Optional[int] = None
    completed_at: Optional[datetime] = None
    document_type: Optional[DocumentType] = None
    file_url: Optional[str] = None
    is_shared: Optional[bool] = False
    parent_shared_id: Optional[uuid.UUID] = None
    has_full_mode: Optional[bool] = False
    has_pareto_mode: Optional[bool] = False
    created_at: datetime
    updated_at: datetime


class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    segment_index: int
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    duration_ms: Optional[int] = None


class LearningUnitDetailResponse(BaseModel):
    id: uuid.UUID
    title: str
    status: Optional[str] = None
    unit_index: int
    unit_type: str
    source_text_char_count: int = 0
    estimated_audio_seconds: int = 0
    main_segment_count: int = 0
    review_text: str = ""
    review_audio_url: str = ""
    planner_reason: Optional[str] = None
    segments: list[SegmentResponse] = Field(default_factory=list)


class BookDetailResponse(BaseModel):
    book_id: uuid.UUID
    book_status: Optional[str] = None
    mode: str
    total_sections: Optional[int] = None
    total_units: int = 0
    learning_summary: Optional[BookLearningSummaryResponse] = None
    units: list[LearningUnitDetailResponse] = Field(default_factory=list)


class SwitchModeResponse(BaseModel):
    message: str
    needs_generation: bool
    job_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    progress_percent: Optional[int] = None

```

### app\schemas\responses\study_context_res.py

```py
"""
app/schemas/responses/study_context_res.py
===========================================
Response DTOs cho module Study Context.

Chỉ expose các trường Flutter FE thực sự cần — không lộ user_id,
không kéo theo lazy-load relationships.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudyContextResponse(BaseModel):
    """DTO cho StudyContext — ẩn user_id (internal field)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    is_auto_generated: bool = False
    created_at: datetime
    updated_at: datetime


class ChatThreadResponse(BaseModel):
    """DTO cho ChatThread — không kéo theo relationship messages."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    context_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageResponse(BaseModel):
    """DTO cho ChatMessage — không kéo theo relationship thread."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thread_id: uuid.UUID
    is_user: bool
    text: str
    source: str
    timestamp: datetime


class ContextDocumentResponse(BaseModel):
    """DTO cho StudyContextDocumentLink."""

    model_config = ConfigDict(from_attributes=True)

    context_id: uuid.UUID
    book_id: uuid.UUID

```

### app\schemas\responses\__init__.py

```py
# Response DTO schemas — import từ đây cho gọn
from app.schemas.responses.audiobook_res import (
    BookDetailResponse,
    BookResponse,
    SwitchModeResponse,
)
from app.schemas.responses.study_context_res import (
    ChatMessageResponse,
    ChatThreadResponse,
    ContextDocumentResponse,
    StudyContextResponse,
)

__all__ = [
    # Audiobook
    "BookResponse",
    "BookDetailResponse",
    "SwitchModeResponse",
    # Study Context
    "StudyContextResponse",
    "ChatThreadResponse",
    "ChatMessageResponse",
    "ContextDocumentResponse",
]

```

### app\schemas\review.py

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constant import PlanMode, ReviewItemStatus


class ReviewItemResponse(BaseModel):
    review_item_id: uuid.UUID
    book_id: uuid.UUID
    book_title: str | None = None
    learning_unit_id: uuid.UUID | None = None
    learning_unit_title: str | None = None
    mode: PlanMode
    status: ReviewItemStatus
    due_at: datetime
    interval_days: int
    sequence_index: int
    review_text: str = ""
    review_audio_url: str | None = None
    anchor_completed_at: datetime | None = None
    last_reviewed_at: datetime | None = None
    completed_at: datetime | None = None
    notified_at: datetime | None = None


class ReviewListResponse(BaseModel):
    items: list[ReviewItemResponse] = Field(default_factory=list)
    total: int


class ReviewActionResponse(BaseModel):
    review_item_id: uuid.UUID
    status: ReviewItemStatus
    completed_at: datetime | None = None

```

### app\schemas\study_context.py

```py
import uuid

from pydantic import BaseModel, Field


class StudyContextInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class StudyContextUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class StudyContextDocumentInput(BaseModel):
    book_id: uuid.UUID


class ChatThreadInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class ChatThreadUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)

```

### app\schemas\user.py

```py
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserTokenPayload(BaseModel):
    """
    Schema định nghĩa payload chứa trong JWT token của Supabase trả về
    """
    sub: UUID
    email: Optional[str] = None
    role: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None

```

### app\services\admin_service.py

```py
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


```

### app\services\agent_grounding\contracts.py

```py
from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import Enum


class GroundingIntent(str, Enum):
    BOOK_METADATA_TITLE = "book_metadata.title"
    BOOK_METADATA_AUTHOR = "book_metadata.author"
    BOOK_METADATA_DOCUMENT_TYPE = "book_metadata.document_type"
    BOOK_METADATA_SECTION_COUNT = "book_metadata.section_count"
    BOOK_METADATA_ROOT_SECTION_COUNT = "book_metadata.root_section_count"
    BOOK_METADATA_STATUS = "book_metadata.status"
    BOOK_SECTION_SUMMARY = "book_section.summary"
    BOOK_SECTION_CONTENT = "book_section.content"
    BOOK_SEMANTIC_QUESTION = "book_semantic_question"
    EXTERNAL_CURRENT_INFO = "external_current_info"
    CLARIFICATION_REQUIRED = "clarification_required"


class GroundingRoute(str, Enum):
    BOOK_METADATA = "book_metadata"
    BOOK_SECTION = "book_section"
    BOOK_RAG = "book_rag"
    WEB_POLICY = "web_policy"
    CLARIFICATION = "clarification"


class ResolutionQuality(str, Enum):
    EXACT = "exact"
    UNIQUE = "unique"
    AMBIGUOUS = "ambiguous"
    NOT_FOUND = "not_found"


@dataclass(frozen=True)
class NormalizedQuery:
    original: str
    normalized: str
    accent_folded: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class GroundingBook:
    id: uuid.UUID
    title: str
    author: str | None
    document_type: str | None
    total_sections: int | None
    status: str | None
    root_section_count: int


@dataclass(frozen=True)
class GroundingSection:
    id: uuid.UUID
    book_id: uuid.UUID
    parent_id: uuid.UUID | None
    section_index: int
    title: str
    level: int
    path: str
    text_char_count: int


@dataclass(frozen=True)
class GroundingSectionText:
    id: uuid.UUID
    book_id: uuid.UUID
    section_index: int
    title: str
    path: str
    text_content: str | None


@dataclass(frozen=True)
class GroundingScope:
    allowed_book_ids: tuple[uuid.UUID, ...]
    books: tuple[GroundingBook, ...]
    sections: tuple[GroundingSection, ...]


@dataclass(frozen=True)
class SectionReference:
    marker_present: bool = False
    explicit_path: str | None = None
    explicit_ordinal: int | None = None
    title_hint: str | None = None
    explicit: bool = True

    @property
    def has_target(self) -> bool:
        return self.explicit_path is not None or self.explicit_ordinal is not None or bool(self.title_hint)


@dataclass(frozen=True)
class BookResolution:
    quality: ResolutionQuality
    reason_code: str
    book: GroundingBook | None = None
    candidates: tuple[GroundingBook, ...] = field(default_factory=tuple)
    clarification: str | None = None


@dataclass(frozen=True)
class SectionResolution:
    quality: ResolutionQuality
    reason_code: str
    book: GroundingBook | None = None
    section: GroundingSection | None = None
    candidates: tuple[GroundingSection, ...] = field(default_factory=tuple)
    clarification: str | None = None


@dataclass(frozen=True)
class SectionContext:
    text: str
    section_ids: tuple[uuid.UUID, ...]
    has_content: bool
    truncated: bool


@dataclass(frozen=True)
class GroundingDecision:
    intent: GroundingIntent
    route: GroundingRoute
    quality: ResolutionQuality
    reason_code: str
    resolved_book_ids: tuple[uuid.UUID, ...] = field(default_factory=tuple)
    resolved_section_ids: tuple[uuid.UUID, ...] = field(default_factory=tuple)
    clarification: str | None = None


@dataclass(frozen=True)
class GroundingResult:
    decision: GroundingDecision
    deterministic_answer: str | None = None
    section_context: str | None = None
    section_context_truncated: bool = False


SectionTextLoader = Callable[[uuid.UUID, tuple[uuid.UUID, ...]], Awaitable[tuple[GroundingSectionText, ...]]]


```

### app\services\agent_grounding\grounding_router.py

```py
from __future__ import annotations

import time

from app.services.agent_grounding.contracts import (
    GroundingDecision,
    GroundingIntent,
    GroundingResult,
    GroundingRoute,
    GroundingScope,
    ResolutionQuality,
    SectionTextLoader,
)
from app.services.agent_grounding.intent_router import classify_intent
from app.services.agent_grounding.query_normalizer import normalize_query
from app.services.agent_grounding.response_renderer import render_metadata_answer
from app.services.agent_grounding.section_context_builder import build_section_context, descendant_section_ids
from app.services.agent_grounding.section_reference_parser import parse_section_reference
from app.services.agent_grounding.section_resolver import resolve_metadata_book, resolve_section
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer


class GroundingRouter:
    def __init__(
        self,
        scope: GroundingScope,
        section_text_loader: SectionTextLoader,
        *,
        section_context_max_chars: int,
    ) -> None:
        self.scope = scope
        self.section_text_loader = section_text_loader
        self.section_context_max_chars = section_context_max_chars

    async def resolve(
        self,
        query: str,
        *,
        input_mode: AgentInputMode = AgentInputMode.TEXT,
        tracer: AgentTurnTracer | None = None,
    ) -> GroundingResult:
        started = time.perf_counter()
        normalized = normalize_query(query)

        # 1. Gọi bộ phân loại ý định ngữ nghĩa bất đồng bộ
        intent = await classify_intent(normalized)
        reference = parse_section_reference(normalized)

        # 2. Luật chặn (Guard Rule): Nếu phân loại là mục lục/tóm tắt chương nhưng không có đề mục cụ thể
        # thì tự động hạ cấp xuống CLARIFICATION_REQUIRED để tránh lỗi định tuyến
        if intent in (GroundingIntent.BOOK_SECTION_SUMMARY, GroundingIntent.BOOK_SECTION_CONTENT):
            if not reference.has_target:
                intent = GroundingIntent.CLARIFICATION_REQUIRED

        result = None
        if intent == GroundingIntent.BOOK_SEMANTIC_QUESTION:
            result = GroundingResult(
                GroundingDecision(
                    GroundingIntent.BOOK_SEMANTIC_QUESTION,
                    GroundingRoute.BOOK_RAG,
                    ResolutionQuality.NOT_FOUND,
                    "semantic_rag_fallback",
                )
            )
        elif intent == GroundingIntent.CLARIFICATION_REQUIRED:
            result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
        elif intent == GroundingIntent.EXTERNAL_CURRENT_INFO:
            result = GroundingResult(
                GroundingDecision(
                    GroundingIntent.EXTERNAL_CURRENT_INFO,
                    GroundingRoute.WEB_POLICY,
                    ResolutionQuality.EXACT,
                    "clear_external_current_info",
                )
            )
        elif intent in (GroundingIntent.BOOK_SECTION_SUMMARY, GroundingIntent.BOOK_SECTION_CONTENT):
            result = await self._resolve_section(normalized, reference, intent)
            if result.decision.route == GroundingRoute.CLARIFICATION:
                is_explicit = reference.explicit_path is not None or reference.explicit_ordinal is not None
                if not is_explicit:
                    result = None
        else:
            # Các nhóm Metadata
            result = self._resolve_metadata(normalized, intent)

        # Fallback phòng thủ cuối cùng
        if result is None:
            result = GroundingResult(
                GroundingDecision(
                    GroundingIntent.BOOK_SEMANTIC_QUESTION,
                    GroundingRoute.BOOK_RAG,
                    ResolutionQuality.NOT_FOUND,
                    "semantic_rag_fallback",
                )
            )

        if tracer is not None:
            self._record_trace(tracer, input_mode, result, int((time.perf_counter() - started) * 1000))
        return result

    def _resolve_metadata(self, query, intent: GroundingIntent) -> GroundingResult:
        resolution = resolve_metadata_book(self.scope, query)
        if resolution.book is None:
            return self._clarification(resolution.reason_code, resolution.clarification or "Bạn muốn hỏi sách nào?")
        decision = GroundingDecision(
            intent,
            GroundingRoute.BOOK_METADATA,
            resolution.quality,
            resolution.reason_code,
            resolved_book_ids=(resolution.book.id,),
        )
        return GroundingResult(decision, deterministic_answer=render_metadata_answer(resolution.book, intent))

    async def _resolve_section(self, query, reference, intent: GroundingIntent) -> GroundingResult:
        resolution = resolve_section(self.scope, query, reference)
        if resolution.book is None or resolution.section is None:
            return self._clarification(resolution.reason_code, resolution.clarification or "Bạn muốn hỏi đề mục nào?")

        section_ids = descendant_section_ids(self.scope, resolution.section.id)
        rows = await self.section_text_loader(resolution.book.id, section_ids)
        context = build_section_context(
            resolution.book,
            resolution.section,
            rows,
            max_chars=self.section_context_max_chars,
        )
        decision = GroundingDecision(
            intent,
            GroundingRoute.BOOK_SECTION,
            resolution.quality,
            resolution.reason_code,
            resolved_book_ids=(resolution.book.id,),
            resolved_section_ids=context.section_ids or (resolution.section.id,),
        )
        if not context.has_content:
            answer = f'Tôi đã tìm thấy mục "{resolution.section.title}", nhưng nội dung mục này chưa được trích xuất.'
            return GroundingResult(decision, deterministic_answer=answer)
        return GroundingResult(decision, section_context=context.text, section_context_truncated=context.truncated)

    @staticmethod
    def _clarification(reason_code: str, clarification: str) -> GroundingResult:
        return GroundingResult(
            GroundingDecision(
                GroundingIntent.CLARIFICATION_REQUIRED,
                GroundingRoute.CLARIFICATION,
                ResolutionQuality.AMBIGUOUS,
                reason_code,
                clarification=clarification,
            )
        )

    @staticmethod
    def _record_trace(tracer: AgentTurnTracer, input_mode: AgentInputMode, result: GroundingResult, elapsed_ms: int) -> None:
        decision = result.decision
        tracer.record_grounding_decision(
            input_mode,
            intent=decision.intent.value,
            route=decision.route.value,
            reason_code=decision.reason_code,
            resolved_book_ids=[str(value) for value in decision.resolved_book_ids],
            resolved_section_ids=[str(value) for value in decision.resolved_section_ids],
        )
        tracer.record_latency(input_mode, "grounding_total", elapsed_ms)
        source_by_route = {
            GroundingRoute.BOOK_METADATA: AgentAnswerSource.BOOK_METADATA,
            GroundingRoute.BOOK_SECTION: AgentAnswerSource.BOOK_SECTION,
            GroundingRoute.CLARIFICATION: AgentAnswerSource.CLARIFICATION,
            GroundingRoute.WEB_POLICY: AgentAnswerSource.POLICY,
        }
        source = source_by_route.get(decision.route)
        if source is not None:
            tracer.record_answer_source(input_mode, source)

```

### app\services\agent_grounding\hybrid_retrieval.py

```py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.services.agent_grounding.query_normalizer import normalize_query, normalized_key, tokenize

_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,}(?:[-_/][A-Z0-9]{2,})*\b")
_QUOTED_RE = re.compile(r"[\"'“”‘’]([^\"'“”‘’]{2,})[\"'“”‘’]")

from app.core.stopwords import STOPWORDS


@dataclass(frozen=True)
class HybridRetrievalConfig:
    min_final_score: float
    max_context_chunks: int
    max_chunks_per_section: int
    validate_evidence_enabled: bool = True


@dataclass
class RetrievalCandidate:
    id: str
    book_id: str
    section_id: str
    section_path: str = ""
    section_title: str = ""
    chunk_index: int = 0
    content: str = ""
    vector_score: float | None = None
    lexical_score: float | None = None
    final_score: float = 0.0
    sources: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class EvidenceValidationResult:
    valid: bool
    reason_code: str
    missing_token_count: int = 0


@dataclass(frozen=True)
class HybridRetrievalResult:
    found: bool
    chunks: list[dict[str, Any]]
    method: str
    reason_code: str
    candidate_count: int
    top_candidate_id: str | None = None
    top_vector_score: float | None = None
    top_lexical_score: float | None = None
    top_final_score: float | None = None
    missing_token_count: int = 0


def _clamp_score(value: float | int | None) -> float:
    if value is None:
        return 0.0
    return max(0.0, min(float(value), 1.0))


def _candidate_key(item: dict[str, Any]) -> str:
    item_id = item.get("id")
    if item_id is not None:
        return str(item_id)
    return f"{item.get('section_id', '')}:{item.get('chunk_index', '')}"


def _to_candidate(item: dict[str, Any], source: str) -> RetrievalCandidate:
    vector_score = item.get("similarity") if source == "vector" else item.get("vector_score")
    lexical_score = item.get("lexical_score") if source == "lexical" else item.get("lexical_score")
    candidate = RetrievalCandidate(
        id=_candidate_key(item),
        book_id=str(item.get("book_id") or ""),
        section_id=str(item.get("section_id") or ""),
        section_path=str(item.get("section_path") or ""),
        section_title=str(item.get("section_title") or ""),
        chunk_index=int(item.get("chunk_index") or 0),
        content=str(item.get("content") or ""),
        vector_score=_clamp_score(vector_score) if vector_score is not None else None,
        lexical_score=_clamp_score(lexical_score) if lexical_score is not None else None,
        sources={source},
    )
    return candidate


def merge_candidates(
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
) -> list[RetrievalCandidate]:
    merged: dict[str, RetrievalCandidate] = {}
    for source, payload in (("vector", vector_payload), ("lexical", lexical_payload)):
        for item in payload:
            if not isinstance(item, dict):
                continue
            key = _candidate_key(item)
            candidate = merged.get(key)
            next_candidate = _to_candidate(item, source)
            if candidate is None:
                merged[key] = next_candidate
                continue

            candidate.sources.add(source)
            candidate.vector_score = max(
                _clamp_score(candidate.vector_score),
                _clamp_score(next_candidate.vector_score),
            ) or None
            candidate.lexical_score = max(
                _clamp_score(candidate.lexical_score),
                _clamp_score(next_candidate.lexical_score),
            ) or None
            candidate.section_path = candidate.section_path or next_candidate.section_path
            candidate.section_title = candidate.section_title or next_candidate.section_title
            candidate.content = candidate.content or next_candidate.content
            candidate.book_id = candidate.book_id or next_candidate.book_id
            candidate.section_id = candidate.section_id or next_candidate.section_id
    return list(merged.values())


def _token_overlap(query_tokens: set[str], text: str) -> bool:
    if not query_tokens:
        return False
    text_tokens = set(tokenize(normalized_key(text)))
    return bool(query_tokens & text_tokens)


def rerank_candidates(
    query: str,
    candidates: list[RetrievalCandidate],
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
    config: HybridRetrievalConfig,
    k: int = 60,
) -> list[RetrievalCandidate]:
    
    # 1. Xác định thứ hạng (1-indexed) của từng ứng viên trong luồng Vector Search
    vector_ranks = {_candidate_key(item): idx + 1 for idx, item in enumerate(vector_payload)}
    
    # 2. Xác định thứ hạng (1-indexed) của từng ứng viên trong luồng Lexical Search
    lexical_ranks = {_candidate_key(item): idx + 1 for idx, item in enumerate(lexical_payload)}
    
    # 3. Tính điểm RRF cho từng ứng viên theo công thức chuẩn quốc tế
    for candidate in candidates:
        c_id = candidate.id
        term_v = 1.0 / (k + vector_ranks[c_id]) if c_id in vector_ranks else 0.0
        term_l = 1.0 / (k + lexical_ranks[c_id]) if c_id in lexical_ranks else 0.0
        candidate.final_score = term_v + term_l
        
    return sorted(
        candidates,
        key=lambda item: (
            item.final_score,
            _clamp_score(item.lexical_score),
            _clamp_score(item.vector_score),
            -item.chunk_index,
        ),
        reverse=True,
    )


def select_context_candidates(
    candidates: list[RetrievalCandidate],
    config: HybridRetrievalConfig,
) -> list[RetrievalCandidate]:
    selected: list[RetrievalCandidate] = []
    per_section: dict[str, int] = {}
    max_total = max(1, config.max_context_chunks)
    max_per_section = max(1, config.max_chunks_per_section)
    for candidate in candidates:
        section_key = candidate.section_id or candidate.section_path or candidate.id
        if per_section.get(section_key, 0) >= max_per_section:
            continue
        selected.append(candidate)
        per_section[section_key] = per_section.get(section_key, 0) + 1
        if len(selected) >= max_total:
            break
    return selected


def _important_query_tokens(query: str) -> set[str]:
    normalized = normalize_query(query)
    important = {
        token
        for token in normalized.tokens
        if (len(token) >= 5 or any(char.isdigit() for char in token))
        and token not in STOPWORDS
    }
    for acronym in _ACRONYM_RE.findall(query):
        important.update(tokenize(normalized_key(acronym)))
    for quoted in _QUOTED_RE.findall(query):
        important.update(token for token in tokenize(normalized_key(quoted)) if token not in STOPWORDS)
    return important


def validate_evidence(
    query: str,
    selected_candidates: list[RetrievalCandidate],
    config: HybridRetrievalConfig,
) -> EvidenceValidationResult:
    if not selected_candidates:
        return EvidenceValidationResult(valid=False, reason_code="no_candidates")

    if not config.validate_evidence_enabled:
        return EvidenceValidationResult(valid=True, reason_code="valid")

    top_vector_score = selected_candidates[0].vector_score
    if top_vector_score is not None and top_vector_score < config.min_final_score:
        return EvidenceValidationResult(valid=False, reason_code="low_confidence")

    important_tokens = _important_query_tokens(query)
    if important_tokens:
        evidence_text = normalized_key(
            " ".join(
                f"{candidate.section_path} {candidate.section_title} {candidate.content}"
                for candidate in selected_candidates[:2]
            )
        )
        evidence_tokens = set(tokenize(evidence_text))
        missing_tokens = important_tokens - evidence_tokens
        if missing_tokens and len(missing_tokens) == len(important_tokens):
            return EvidenceValidationResult(
                valid=False,
                reason_code="missing_named_entity",
                missing_token_count=len(missing_tokens),
            )

    return EvidenceValidationResult(valid=True, reason_code="valid")


def _candidate_to_payload(candidate: RetrievalCandidate) -> dict[str, Any]:
    return {
        "id": candidate.id,
        "book_id": candidate.book_id,
        "section_id": candidate.section_id,
        "section_path": candidate.section_path,
        "section_title": candidate.section_title,
        "chunk_index": candidate.chunk_index,
        "content": candidate.content,
        "similarity": candidate.final_score,
        "vector_score": candidate.vector_score,
        "lexical_score": candidate.lexical_score,
        "final_score": candidate.final_score,
        "retrieval_method": "hybrid",
        "retrieval_sources": sorted(candidate.sources),
    }


def build_hybrid_retrieval_result(
    *,
    query: str,
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
    config: HybridRetrievalConfig,
) -> HybridRetrievalResult:
    candidates = merge_candidates(vector_payload, lexical_payload)
    ranked = rerank_candidates(query, candidates, vector_payload, lexical_payload, config)
    selected = select_context_candidates(ranked, config)
    validation = validate_evidence(query, selected, config)
    top_candidate = selected[0] if selected else None
    if not validation.valid:
        return HybridRetrievalResult(
            found=False,
            chunks=[],
            method="hybrid",
            reason_code=validation.reason_code,
            candidate_count=len(candidates),
            top_candidate_id=top_candidate.id if top_candidate else None,
            top_vector_score=top_candidate.vector_score if top_candidate else None,
            top_lexical_score=top_candidate.lexical_score if top_candidate else None,
            top_final_score=top_candidate.final_score if top_candidate else None,
            missing_token_count=validation.missing_token_count,
        )
    return HybridRetrievalResult(
        found=True,
        chunks=[_candidate_to_payload(candidate) for candidate in selected],
        method="hybrid",
        reason_code=validation.reason_code,
        candidate_count=len(candidates),
        top_candidate_id=top_candidate.id if top_candidate else None,
        top_vector_score=top_candidate.vector_score if top_candidate else None,
        top_lexical_score=top_candidate.lexical_score if top_candidate else None,
        top_final_score=top_candidate.final_score if top_candidate else None,
        missing_token_count=validation.missing_token_count,
    )

```

### app\services\agent_grounding\intent_router.py

```py
from __future__ import annotations

import asyncio
import torch
from transformers import AutoTokenizer, AutoModel
from app.core.config import settings
from app.services.agent_grounding.contracts import GroundingIntent, NormalizedQuery

# Định nghĩa các câu mẫu đặc trưng đại diện cho từng lớp Ý định (Intent Class)
PROTOTYPES = {
    GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT: [
        "sách có bao nhiêu chương chính",
        "quyển sách này gồm bao nhiêu chương",
        "sách có mấy chương",
        "sách gồm mấy phần",
        "tổng số chương chính",
        "how many chapters",
        "how many main sections"
    ],
    GroundingIntent.BOOK_METADATA_AUTHOR: [
        "ai là tác giả cuốn sách này",
        "tác giả quyển sách này là ai",
        "ai viết tác phẩm này",
        "sách này được soạn bởi ai",
        "author của cuốn sách này",
        "who wrote this book",
        "written by"
    ],
    GroundingIntent.BOOK_METADATA_TITLE: [
        "tên sách là gì",
        "tựa đề quyển sách này",
        "đang đọc quyển sách nào",
        "tên của quyển sách đang học",
        "quyển sách này tên là gì",
        "book title"
    ],
    GroundingIntent.BOOK_SECTION_SUMMARY: [
        "tóm tắt chương 1",
        "đại ý của chương hai",
        "tổng quan chương 3",
        "kể tóm lược phần 4",
        "ý chương bốn là gì",
        "ý chính của chương này",
        "ý nghĩa của chương",
        "đại ý chương",
        "summarize",
        "summary of chapter"
    ],
    GroundingIntent.BOOK_SECTION_CONTENT: [
        "nội dung chương 1 là gì",
        "giải thích chương 2",
        "đọc nội dung phần ba",
        "trình bày chi tiết mục 1.1",
        "nội dung phần",
        "what is in section"
    ],
    GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE: [
        "định dạng tài liệu này là gì",
        "đây là loại file gì",
        "đây là tài liệu pdf hay word",
        "loại tài liệu hiện tại",
        "document type",
        "file format"
    ],
    GroundingIntent.BOOK_METADATA_STATUS: [
        "sách đã xử lý xong chưa",
        "trạng thái xử lý của sách",
        "sách đã được nạp thành công chưa",
        "tiến trình nạp sách thế nào",
        "sach da ingest thanh cong chua"
    ],
    GroundingIntent.BOOK_METADATA_SECTION_COUNT: [
        "bao nhiêu đề mục",
        "quyển này có bao nhiêu mục tất cả",
        "tổng số mục trong sách",
        "how many sections",
        "section count"
    ],
    GroundingIntent.EXTERNAL_CURRENT_INFO: [
        "giá thị trường hôm nay là bao nhiêu",
        "tin tức mới nhất hôm nay",
        "thời tiết hôm nay thế nào",
        "giá vàng hiện nay",
        "thời tiết hiện tại",
        "tin tức thời sự bây giờ",
        "current market price today",
        "latest news today",
        "thời tiết hôm nay ra sao",
        "tin hot ngày hôm nay",
        "tìm các tác phẩm tương tự",
        "các tác phẩm cùng thể loại",
        "similar books to this one"
    ]
}

AUTHOR_CONTENT_VERBS = ("giải thích", "trình bày", "cho rằng", "nói gì", "quan điểm", "nghĩ gì")
AUTHOR_IDENTITY_KEYWORDS = ("ai viết", "who wrote", "written by", "tên của tác giả", "tác giả là ai")

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

class SemanticIntentClassifier:
    def __init__(self) -> None:
        self.model_name = settings.AGENT_INTENT_CLASSIFIER_MODEL or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.tokenizer = None
        self.model = None
        self.proto_embeddings = {}
        self._lock = asyncio.Lock()
        self._initialized = False

    def initialize(self) -> None:
        """
        Nạp tokenizer, weights và tính toán trước vector nhúng của các câu mẫu.
        Phương thức này chạy đồng bộ (blocking CPU) nên cần được bao bọc khi gọi từ async loop.
        """
        if self._initialized:
            return
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()
        
        with torch.no_grad():
            for intent, phrases in PROTOTYPES.items():
                inputs = self.tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs, inputs['attention_mask'])
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                self.proto_embeddings[intent] = embeddings
                
        self._initialized = True

    async def initialize_async(self) -> None:
        """
        Khởi tạo an toàn bất đồng bộ. Đẩy tác vụ nạp model nặng sang Executor Thread
        để không chặn Event Loop chính của LiveKit.
        """
        if self._initialized:
            return
        async with self._lock:
            if not self._initialized:
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, self.initialize)

    async def classify(self, query_text: str, threshold: float | None = None) -> GroundingIntent:
        """
        Tính toán cosine similarity của câu hỏi với các mẫu.
        Nếu điểm số cao nhất dưới threshold, mặc định trả về RAG (BOOK_SEMANTIC_QUESTION).
        """
        resolved_threshold = threshold if threshold is not None else settings.AGENT_INTENT_CLASSIFIER_THRESHOLD
        await self.initialize_async()
        
        text = query_text.strip().lower()
        if not text:
            return GroundingIntent.BOOK_SEMANTIC_QUESTION

        with torch.no_grad():
            inputs = self.tokenizer([text], padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            
            best_intent = GroundingIntent.BOOK_SEMANTIC_QUESTION
            best_score = -1.0
            
            for intent, proto_embs in self.proto_embeddings.items():
                # Nhân ma trận tính khoảng cách Cosine nhanh trên Pytorch
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent
                    
            if best_score >= resolved_threshold:
                # Kiểm duyệt biên: Nếu hỏi nội dung tác giả viết (RAG) thay vì danh tính tác giả (Metadata)
                if best_intent == GroundingIntent.BOOK_METADATA_AUTHOR:
                    has_content_verb = any(v in text for v in AUTHOR_CONTENT_VERBS)
                    has_identity_keyword = any(k in text for k in AUTHOR_IDENTITY_KEYWORDS)
                    if has_content_verb and not has_identity_keyword:
                        return GroundingIntent.BOOK_SEMANTIC_QUESTION
                return best_intent
                
            return GroundingIntent.BOOK_SEMANTIC_QUESTION

# Đối tượng Singleton dùng chung trong suốt phiên hoạt động của module
_classifier = SemanticIntentClassifier()

async def classify_intent(query: NormalizedQuery) -> GroundingIntent:
    """
    Hàm giao tiếp hướng ngoại tương thích với các module gọi ngoài.
    """
    return await _classifier.classify(query.normalized)

```

### app\services\agent_grounding\query_normalizer.py

```py
from __future__ import annotations

import re
import unicodedata

from app.services.agent_grounding.contracts import NormalizedQuery

TOKEN_PATTERN = re.compile(r"\d+(?:\.\d+)+|[^\W_]+|\d+", re.UNICODE)
WHITESPACE_PATTERN = re.compile(r"\s+")


def fold_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(character for character in decomposed if not unicodedata.combining(character))
# EX: "Ví dụ" => "Vi du"

def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "").strip().casefold()
    return WHITESPACE_PATTERN.sub(" ", normalized)
# EX: " hOÀnG   vŨ ß " => "hoàng vũ ss"


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(TOKEN_PATTERN.findall(text))
# EX: "hoang vu dep trai" => ("hoang", "vu", "dep", "trai")

def normalize_query(text: str) -> NormalizedQuery:
    original = (text or "").strip()
    normalized = normalize_text(original)
    accent_folded = fold_accents(normalized)
    return NormalizedQuery(
        original=original, # Origine
        normalized=normalized, # Chuẩn hóa, Khớp từ có dấu
        accent_folded=accent_folded, # Khớp không dấu
        tokens=tokenize(accent_folded), # Từng từ, độc lập từ => Full text search
    )


def normalized_key(text: str) -> str:
    return " ".join(tokenize(fold_accents(normalize_text(text))))


def _contains_token_sequence(tokens: tuple[str, ...], phrase_tokens: tuple[str, ...]) -> bool:
    if not phrase_tokens or len(phrase_tokens) > len(tokens):
        return False
    width = len(phrase_tokens)
    return any(tokens[index : index + width] == phrase_tokens for index in range(len(tokens) - width + 1))


def contains_phrase(query: NormalizedQuery, phrase: str) -> bool:
    return _contains_token_sequence(query.tokens, tokenize(fold_accents(normalize_text(phrase))))


def contains_any_phrase(query: NormalizedQuery, phrases: tuple[str, ...] | list[str] | set[str]) -> bool:
    return any(contains_phrase(query, phrase) for phrase in phrases)


```

### app\services\agent_grounding\reranker.py

```py
from app.core.logger import log
from app.core.config import settings
from typing import Any
import httpx
import asyncio

async def rerank_candidates(
    query: str,
    candidates: list[dict[str, Any]],
    *,
    model: str | None = None,
    top_n: int | None = None
) -> list[dict[str, Any]]:
    """
    Sử dụng Cohere Multilingual Rerank API v2 để xếp hạng lại (Rerank) các chunks ứng viên.
    
    Args:
        query: Câu hỏi hoặc truy vấn của người dùng.
        candidates: Danh sách các chunk ứng viên dạng dictionary từ Hybrid Retrieval.
        model: Model rerank sử dụng (mặc định lấy từ settings).
        top_n: Số lượng kết quả tối đa muốn giữ lại (mặc định lấy từ settings).
        
    Returns:
        Danh sách các chunk đã được cập nhật score và sắp xếp theo thứ tự giảm dần.
        Nếu API lỗi hoặc không cấu hình API Key, tự động fallback trả về danh sách gốc.
    """
    if not settings.COHERE_API_KEY:
        log.warning("Reranker: Không tìm thấy COHERE_API_KEY. Bỏ qua Rerank (Fallback mode).")
        return candidates
    
    if not candidates:
        return []

    limit = settings.AGENT_RERANKER_CANDIDATES_LIMIT
    input_candidates = candidates[:limit]

    rerank_model = model or settings.AGENT_RERANKER_MODEL
    rerank_top_n = top_n or settings.AGENT_RERANKER_TOP_N

    # Sử dụng Cohere Rerank API v2 theo đặc tả mới nhất
    url = "https://api.cohere.com/v2/rerank"
    headers = {
        "Authorization": f"Bearer {settings.COHERE_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    
    payload = {
        "model": rerank_model,
        "query": query,
        "documents": [c.get("content", "") for c in input_candidates],
        "top_n": min(rerank_top_n, len(input_candidates))
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=8.0)
            
            if response.status_code != 200:
                log.error(f"Reranker: Cohere API v2 trả về mã lỗi {response.status_code}: {response.text}")
                return candidates  # Fallback
                
            results = response.json().get("results", [])
            
            reranked_candidates = []
            for item in results:
                idx = item["index"]
                relevance_score = float(item["relevance_score"])
                
                candidate = input_candidates[idx].copy()
                candidate["similarity"] = round(relevance_score, 4)
                candidate["final_score"] = round(relevance_score, 4)
                candidate["retrieval_method"] = "cohere-rerank-v2"
                
                reranked_candidates.append(candidate)
                
            log.info(f"Reranker: Đã Rerank thành công {len(reranked_candidates)} chunks bằng Cohere v2 API.")
            return reranked_candidates

    except httpx.HTTPError as http_err:
        log.error(f"Reranker: Lỗi kết nối HTTP tới Cohere API v2: {http_err}")
    except asyncio.TimeoutError:
        log.error("Reranker: Gọi Cohere API v2 bị quá hạn (Timeout).")
    except Exception as e:
        log.error(f"Reranker: Lỗi không xác định khi thực hiện rerank: {e}")
        
    return candidates
```

### app\services\agent_grounding\response_renderer.py

```py
from __future__ import annotations

from app.services.agent_grounding.contracts import GroundingBook, GroundingIntent, GroundingResult, GroundingRoute

STATUS_LABELS = {
    "draft": "đã tải lên và chưa tạo kế hoạch học",
    "processing": "đang được xử lý",
    "partial_ready": "đã có thể nghe một phần",
    "ready": "đã xử lý xong",
    "error": "đang gặp lỗi xử lý",
}


def render_metadata_answer(book: GroundingBook, intent: GroundingIntent) -> str:
    if intent == GroundingIntent.BOOK_METADATA_AUTHOR:
        return f'Tác giả của "{book.title}" là {book.author}.' if book.author else f'Tôi chưa có thông tin tác giả của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_TITLE:
        return f'Tên sách là "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE:
        return f'"{book.title}" là tài liệu {book.document_type.upper()}.' if book.document_type else f'Tôi chưa có thông tin định dạng của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_SECTION_COUNT:
        return f'"{book.title}" có {book.total_sections} đề mục trong cấu trúc tài liệu.' if book.total_sections is not None else f'Tôi chưa có tổng số đề mục của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT:
        return f'"{book.title}" có {book.root_section_count} phần chính.'
    if intent == GroundingIntent.BOOK_METADATA_STATUS:
        status = STATUS_LABELS.get((book.status or "").casefold())
        return f'"{book.title}" {status}.' if status else f'Tôi chưa xác định được trạng thái xử lý của "{book.title}".'
    raise ValueError(f"Unsupported metadata intent: {intent}")


def format_grounding_tool_result(result: GroundingResult) -> str:
    if result.decision.route == GroundingRoute.BOOK_METADATA:
        return f"BOOK_METADATA_FOUND:\n{result.deterministic_answer or ''}".strip()
    if result.decision.route == GroundingRoute.BOOK_SECTION:
        if result.section_context:
            suffix = "\nThe context was truncated; state that limitation." if result.section_context_truncated else ""
            return (
                "BOOK_SECTION_FOUND:\n"
                f"{result.section_context}\n"
                "Answer only from this section context. Do not use model memory or request web search."
                f"{suffix}"
            )
        return f"BOOK_SECTION_UNAVAILABLE:\n{result.deterministic_answer or 'Nội dung section chưa được trích xuất.'}"
    if result.decision.route == GroundingRoute.CLARIFICATION:
        return f"CLARIFICATION_REQUIRED:\n{result.decision.clarification or 'Bạn vui lòng nói rõ câu hỏi.'}"
    if result.decision.route == GroundingRoute.WEB_POLICY:
        return "EXTERNAL_INFO_REQUIRED: This question needs current or external information. Follow the existing web-search permission policy."
    return "BOOK_RAG_REQUIRED"


```

### app\services\agent_grounding\section_context_builder.py

```py
from __future__ import annotations

import re
import uuid

from app.services.agent_grounding.contracts import GroundingBook, GroundingScope, GroundingSection, GroundingSectionText, SectionContext
from app.services.agent_grounding.query_normalizer import normalize_text

WHITESPACE_PATTERN = re.compile(r"\s+")


def descendant_section_ids(scope: GroundingScope, root_id: uuid.UUID) -> tuple[uuid.UUID, ...]:
    children: dict[uuid.UUID | None, list[GroundingSection]] = {}
    by_id = {section.id: section for section in scope.sections}
    root = by_id.get(root_id)
    if root is None:
        return ()

    for section in sorted(scope.sections, key=lambda item: item.section_index):
        if section.book_id == root.book_id:
            children.setdefault(section.parent_id, []).append(section)

    result: list[uuid.UUID] = []

    def walk(section: GroundingSection) -> None:
        result.append(section.id)
        for child in children.get(section.id, []):
            walk(child)

    walk(root)
    return tuple(result)


def _dedupe_rows(rows: tuple[GroundingSectionText, ...]) -> tuple[GroundingSectionText, ...]:
    seen: set[str] = set()
    result: list[GroundingSectionText] = []
    for row in sorted(rows, key=lambda item: item.section_index):
        text = WHITESPACE_PATTERN.sub(" ", normalize_text(row.text_content or ""))
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(row)
    return tuple(result)


def build_section_context(
    book: GroundingBook,
    target: GroundingSection,
    rows: tuple[GroundingSectionText, ...],
    *,
    max_chars: int,
) -> SectionContext:
    max_chars = max(8000, max_chars)
    header = f'BOOK_SECTION_CONTEXT\nBook: "{book.title}"\nTarget section: {target.path} - {target.title}\n\n'
    unique_rows = _dedupe_rows(rows)
    if not unique_rows:
        message = f'{header}The section exists, but no source text was extracted for "{target.title}".'
        return SectionContext(message[:max_chars], tuple(row.id for row in rows), False, len(message) > max_chars)

    parts = [header]
    remaining = max_chars - len(header)
    truncated = False
    for index, row in enumerate(unique_rows):
        if remaining <= 0:
            truncated = True
            break
        section_header = f"[{row.path} {row.title}]\n"
        remaining_rows = len(unique_rows) - index
        fair_share = max(200, remaining // max(remaining_rows, 1))
        text = (row.text_content or "").strip()
        allowed_text_chars = max(0, min(len(text), fair_share - len(section_header) - 2, remaining - len(section_header) - 2))
        if allowed_text_chars <= 0:
            truncated = True
            continue
        content = text[:allowed_text_chars].rstrip()
        if len(content) < len(text):
            content = f"{content}\n...[truncated]"
            truncated = True
        block = f"{section_header}{content}\n\n"
        if len(block) > remaining:
            block = block[:remaining]
            truncated = True
        parts.append(block)
        remaining -= len(block)

    text = "".join(parts)[:max_chars]
    all_source_ids = tuple(row.id for row in sorted(rows, key=lambda item: item.section_index))
    return SectionContext(text, all_source_ids, True, truncated or len(text) >= max_chars)

```

### app\services\agent_grounding\section_reference_parser.py

```py
from __future__ import annotations

import re

from app.services.agent_grounding.contracts import NormalizedQuery, SectionReference
from app.services.agent_grounding.query_normalizer import fold_accents, normalize_text

SECTION_MARKERS = {"chuong", "chapter", "phan", "part", "muc", "section"}
GENERIC_SECTION_SUFFIX = {
    "cua",
    "quyen",
    "sach",
    "nay",
    "do",
    "gi",
    "la",
    "trong",
    "the",
    "this",
    "book",
    "please",
}
PATH_PATTERN = re.compile(r"^\d+(?:\.\d+)+$")
ROMAN_PATTERN = re.compile(r"^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$", re.IGNORECASE)
QUOTED_TEXT_PATTERN = re.compile(r'["“”\']([^"“”\']{2,160})["“”\']')

VI_UNITS = {
    "khong": 0,
    "mot": 1,
    "hai": 2,
    "ba": 3,
    "bon": 4,
    "tu": 4,
    "nam": 5,
    "lam": 5,
    "sau": 6,
    "bay": 7,
    "tam": 8,
    "chin": 9,
}
EN_UNITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
EN_TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


def _parse_roman(value: str) -> int | None:
    candidate = value.strip().lower()
    if not candidate or not ROMAN_PATTERN.fullmatch(candidate):
        return None
    values = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    result = 0
    previous = 0
    for character in reversed(candidate):
        current = values[character]
        result += -current if current < previous else current
        previous = max(previous, current)
    return result or None


def _parse_english_number(tokens: list[str]) -> int | None:
    if not tokens or any(token not in EN_UNITS and token not in EN_TENS and token not in {"and", "hundred", "thousand"} for token in tokens):
        return None
    total = 0
    current = 0
    consumed_number = False
    for token in tokens:
        if token == "and":
            continue
        if token in EN_UNITS:
            current += EN_UNITS[token]
            consumed_number = True
        elif token in EN_TENS:
            current += EN_TENS[token]
            consumed_number = True
        elif token == "hundred":
            current = max(current, 1) * 100
            consumed_number = True
        elif token == "thousand":
            total += max(current, 1) * 1000
            current = 0
            consumed_number = True
    value = total + current
    return value if consumed_number and value > 0 else None


def _parse_vi_under_hundred(tokens: list[str]) -> int | None:
    tokens = [token for token in tokens if token not in {"le", "linh"}]
    if not tokens:
        return 0
    if len(tokens) == 1:
        return 10 if tokens[0] == "muoi" else VI_UNITS.get(tokens[0])
    if tokens[0] == "muoi" and len(tokens) == 2 and tokens[1] in VI_UNITS:
        return 10 + VI_UNITS[tokens[1]]
    if len(tokens) in {2, 3} and tokens[0] in VI_UNITS and tokens[1] == "muoi":
        return VI_UNITS[tokens[0]] * 10 + (VI_UNITS.get(tokens[2], 0) if len(tokens) == 3 else 0)
    return None


def _parse_vietnamese_number(tokens: list[str]) -> int | None:
    allowed = set(VI_UNITS) | {"muoi", "tram", "nghin", "le", "linh"}
    if not tokens or any(token not in allowed for token in tokens):
        return None

    total = 0
    remaining = tokens
    if "nghin" in remaining:
        index = remaining.index("nghin")
        thousands = _parse_vietnamese_number(remaining[:index]) if index else 1
        if thousands is None:
            return None
        total += thousands * 1000
        remaining = remaining[index + 1 :]

    if "tram" in remaining:
        index = remaining.index("tram")
        hundreds = VI_UNITS.get(remaining[index - 1], 1) if index else 1
        if index > 1:
            return None
        total += hundreds * 100
        remaining = remaining[index + 1 :]

    under_hundred = _parse_vi_under_hundred(remaining)
    if under_hundred is None:
        return None
    value = total + under_hundred
    return value if value > 0 else None


def parse_positive_integer_phrase(value: str) -> int | None:
    normalized = fold_accents(normalize_text(value)).replace("-", " ")
    if normalized.isdigit():
        parsed = int(normalized)
        return parsed if parsed > 0 else None
    roman = _parse_roman(normalized)
    if roman is not None:
        return roman
    tokens = normalized.split()
    return _parse_vietnamese_number(tokens) or _parse_english_number(tokens)


def _number_prefix(tokens: tuple[str, ...]) -> tuple[int | None, int]:
    for width in range(min(6, len(tokens)), 0, -1):
        value = parse_positive_integer_phrase(" ".join(tokens[:width]))
        if value is not None:
            return value, width
    return None, 0


def _quoted_title(original: str) -> str | None:
    match = QUOTED_TEXT_PATTERN.search(original)
    return match.group(1).strip() if match else None


def parse_section_reference(query: NormalizedQuery) -> SectionReference:
    quoted_title = _quoted_title(query.original)
    for index, token in enumerate(query.tokens):
        if token not in SECTION_MARKERS:
            continue

        if token == "phan" and index + 1 < len(query.tokens) and query.tokens[index + 1] == "tram":
            continue

        remaining = query.tokens[index + 1 :]
        if not remaining:
            return SectionReference(marker_present=True, title_hint=quoted_title)

        first = remaining[0]
        if PATH_PATTERN.fullmatch(first):
            return SectionReference(marker_present=True, explicit_path=first, title_hint=quoted_title)
        if first.isdigit():
            value = int(first)
            return SectionReference(marker_present=True, explicit_ordinal=value if value > 0 else None, title_hint=quoted_title)

        ordinal, width = _number_prefix(remaining)
        if ordinal is not None:
            return SectionReference(marker_present=True, explicit_ordinal=ordinal, title_hint=quoted_title)

        if quoted_title:
            return SectionReference(marker_present=True, title_hint=quoted_title)

        title_tokens = [item for item in remaining if item not in GENERIC_SECTION_SUFFIX]
        title_hint = " ".join(title_tokens).strip() or None
        return SectionReference(marker_present=True, title_hint=title_hint)

    return SectionReference(marker_present=False, title_hint=quoted_title, explicit=quoted_title is not None)


```

### app\services\agent_grounding\section_resolver.py

```py
from __future__ import annotations

from app.services.agent_grounding.contracts import (
    BookResolution,
    GroundingBook,
    GroundingScope,
    GroundingSection,
    NormalizedQuery,
    ResolutionQuality,
    SectionReference,
    SectionResolution,
)
from app.services.agent_grounding.query_normalizer import normalized_key
from app.services.agent_grounding.section_reference_parser import parse_section_reference


def _query_contains_key(query: NormalizedQuery, key: str) -> bool:
    query_key = " ".join(query.tokens)
    return f" {key} " in f" {query_key} "


def _named_books(scope: GroundingScope, query: NormalizedQuery) -> tuple[GroundingBook, ...]:
    return tuple(book for book in scope.books if normalized_key(book.title) and _query_contains_key(query, normalized_key(book.title)))


def resolve_metadata_book(scope: GroundingScope, query: NormalizedQuery) -> BookResolution:
    if not scope.books:
        return BookResolution(
            ResolutionQuality.NOT_FOUND,
            "no_allowed_books",
            clarification="Tôi chưa tìm thấy sách nào trong ngữ cảnh học tập hiện tại.",
        )

    named = _named_books(scope, query)
    if len(named) == 1:
        return BookResolution(ResolutionQuality.EXACT, "exact_book_title", book=named[0])
    if len(named) > 1:
        return BookResolution(
            ResolutionQuality.AMBIGUOUS,
            "multiple_named_books",
            candidates=named,
            clarification="Tôi tìm thấy nhiều sách phù hợp. Bạn muốn hỏi sách nào?",
        )
    if len(scope.books) == 1:
        return BookResolution(ResolutionQuality.UNIQUE, "single_book_scope", book=scope.books[0])

    if scope.allowed_book_ids:
        primary_id = scope.allowed_book_ids[0]
        primary_book = next((b for b in scope.books if b.id == primary_id), None)
        if primary_book is not None:
            return BookResolution(ResolutionQuality.UNIQUE, "primary_book_fallback", book=primary_book)

    return BookResolution(
        ResolutionQuality.AMBIGUOUS,
        "multiple_books_require_selection",
        candidates=scope.books,
        clarification="Ngữ cảnh hiện có nhiều sách. Bạn muốn hỏi thông tin của sách nào?",
    )


def _sections_for_book(scope: GroundingScope, book_id) -> tuple[GroundingSection, ...]:
    return tuple(sorted((section for section in scope.sections if section.book_id == book_id), key=lambda item: item.section_index))


def _ordinal_candidates(sections: tuple[GroundingSection, ...], ordinal: int) -> tuple[GroundingSection, ...]:
    roots = tuple(section for section in sections if section.parent_id is None)
    path_matches = tuple(section for section in roots if section.path == str(ordinal))
    if path_matches:
        return path_matches

    title_matches: list[GroundingSection] = []
    for section in roots:
        title_key = normalized_key(section.title)
        parsed = parse_section_reference(
            NormalizedQuery(
                original=section.title,
                normalized=section.title.casefold(),
                accent_folded=title_key,
                tokens=tuple(title_key.split()),
            )
        )
        if parsed.explicit_ordinal == ordinal:
            title_matches.append(section)
    if title_matches:
        return tuple(title_matches)
    return (roots[ordinal - 1],) if 0 < ordinal <= len(roots) else ()


def _title_candidates(sections: tuple[GroundingSection, ...], title_hint: str) -> tuple[GroundingSection, ...]:
    hint = normalized_key(title_hint)
    exact = tuple(section for section in sections if normalized_key(section.title) == hint)
    if exact or len(hint.split()) < 2:
        return exact
    return tuple(
        section
        for section in sections
        if f" {hint} " in f" {normalized_key(section.title)} " or f" {normalized_key(section.title)} " in f" {hint} "
    )


def _reference_candidates(sections: tuple[GroundingSection, ...], reference: SectionReference) -> tuple[GroundingSection, ...]:
    if reference.explicit_path:
        return tuple(section for section in sections if section.path == reference.explicit_path)
    if reference.explicit_ordinal is not None:
        return _ordinal_candidates(sections, reference.explicit_ordinal)
    if reference.title_hint:
        return _title_candidates(sections, reference.title_hint)
    return ()


def _clarification_for_candidates(candidates: tuple[GroundingSection, ...]) -> str:
    if len(candidates) == 2:
        return f'Tôi tìm thấy hai mục phù hợp: mục {candidates[0].path} và mục {candidates[1].path}. Bạn muốn hỏi mục nào?'
    return "Tôi tìm thấy nhiều đề mục phù hợp. Bạn vui lòng nói rõ số mục hoặc đường dẫn mục lục."


def _primary_book_with_reference(scope: GroundingScope, reference: SectionReference) -> GroundingBook | None:
    if not scope.allowed_book_ids:
        return None

    primary_id = scope.allowed_book_ids[0]
    primary_book = next((book for book in scope.books if book.id == primary_id), None)
    if primary_book is None:
        return None

    candidates = _reference_candidates(_sections_for_book(scope, primary_book.id), reference)
    return primary_book if candidates else None


def _candidate_books_for_reference(
    scope: GroundingScope,
    query: NormalizedQuery,
    reference: SectionReference,
) -> tuple[GroundingBook, ...]:
    named_books = _named_books(scope, query)
    if named_books:
        return named_books

    if not scope.books:
        return ()

    primary_book = _primary_book_with_reference(scope, reference)
    if primary_book is not None:
        return (primary_book,)

    return scope.books


def _section_matches(
    scope: GroundingScope,
    candidate_books: tuple[GroundingBook, ...],
    reference: SectionReference,
) -> list[tuple[GroundingBook, GroundingSection]]:
    matches: list[tuple[GroundingBook, GroundingSection]] = []
    for book in candidate_books:
        sections = _sections_for_book(scope, book.id)
        for section in _reference_candidates(sections, reference):
            matches.append((book, section))
    return matches


def _section_resolution_from_matches(
    matches: list[tuple[GroundingBook, GroundingSection]],
    reference: SectionReference,
) -> SectionResolution | None:
    if len(matches) == 1:
        book, section = matches[0]
        reason = "exact_section_path" if reference.explicit_path or reference.explicit_ordinal is not None else "exact_section_title"
        return SectionResolution(ResolutionQuality.EXACT, reason, book=book, section=section)

    if len(matches) > 1:
        candidates = tuple(section for _, section in matches)
        return SectionResolution(
            ResolutionQuality.AMBIGUOUS,
            "multiple_section_matches",
            candidates=candidates,
            clarification=_clarification_for_candidates(candidates),
        )

    return None


def resolve_section(scope: GroundingScope, query: NormalizedQuery, reference: SectionReference) -> SectionResolution:
    if not reference.has_target:
        return SectionResolution(
            ResolutionQuality.NOT_FOUND,
            "missing_section_reference",
            clarification="Bạn muốn hỏi chương hoặc đề mục nào?",
        )

    candidate_books = _candidate_books_for_reference(scope, query, reference)
    if not candidate_books:
        return SectionResolution(
            ResolutionQuality.NOT_FOUND,
            "no_allowed_books",
            clarification="Tôi chưa tìm thấy sách nào trong ngữ cảnh học tập hiện tại.",
        )

    resolution = _section_resolution_from_matches(
        _section_matches(scope, candidate_books, reference),
        reference,
    )
    if resolution is not None:
        return resolution

    return SectionResolution(
        ResolutionQuality.NOT_FOUND,
        "section_not_found",
        clarification="Tôi không tìm thấy chương hoặc đề mục đó trong sách hiện tại. Bạn vui lòng kiểm tra lại số hoặc tên mục.",
    )

```

### app\services\agent_grounding\__init__.py

```py
"""Shared deterministic grounding policy for text and realtime voice."""

from app.services.agent_grounding.contracts import (
    GroundingDecision,
    GroundingIntent,
    GroundingResult,
    GroundingRoute,
    GroundingScope,
)
from app.services.agent_grounding.grounding_router import GroundingRouter

__all__ = [
    "GroundingDecision",
    "GroundingIntent",
    "GroundingResult",
    "GroundingRoute",
    "GroundingRouter",
    "GroundingScope",
]


```

### app\services\agent_observability\contracts.py

```py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentInputMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"


class AgentAnswerSource(str, Enum):
    UNKNOWN = "unknown"
    BOOK_METADATA = "book_metadata"
    BOOK_SECTION = "book_section"
    BOOK_RAG = "book_rag"
    WEB = "web"
    CLARIFICATION = "clarification"
    POLICY = "policy"
    ERROR = "error"


@dataclass
class AgentTurnTrace:
    trace_id: str
    thread_id: str | None
    room_name: str | None
    input_mode: AgentInputMode
    started_at: datetime
    started_monotonic: float = field(repr=False)
    completed_at: datetime | None = None
    completed_monotonic: float | None = field(default=None, repr=False)
    transcript_final_seen: bool = False
    transcript_char_count: int = 0
    detected_language: str | None = None
    detected_intent: str | None = None
    grounding_route: str | None = None
    grounding_reason_code: str | None = None
    resolved_book_ids: list[str] = field(default_factory=list)
    resolved_section_ids: list[str] = field(default_factory=list)
    retrieval_method: str | None = None
    retrieval_result_count: int = 0
    retrieval_chunk_ids: list[str] = field(default_factory=list)
    retrieval_learning_unit_ids: list[str] = field(default_factory=list)
    retrieval_section_ids: list[str] = field(default_factory=list)
    retrieval_scores: list[float] = field(default_factory=list)
    tool_names: list[str] = field(default_factory=list)
    query_guard_reason_code: str | None = None
    query_guard_mode: str | None = None
    query_guard_overlap_ratio: float | None = None
    query_guard_important_overlap_ratio: float | None = None
    answer_source: AgentAnswerSource = AgentAnswerSource.UNKNOWN
    assistant_char_count: int = 0
    stage_latency_ms: dict[str, int] = field(default_factory=dict)
    error_code: str | None = None
    tool_reply_watchdog_scheduled: bool | None = None
    tool_reply_watchdog_fired: bool | None = None
    tool_reply_watchdog_tool_names: list[str] = field(default_factory=list)
    tool_reply_watchdog_reason: str | None = None
    tool_result_to_speech_ms: int | None = None
    forced_reply_reason: str | None = None
    correlation_quality: str = "session_active_turn"

```

### app\services\agent_observability\llm_as_a_judge.py

```py
from __future__ import annotations

import uuid

from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.core.config import settings
from app.db.database import engine
from app.models.db_models import BookSectionKnowledge


class LLMJudgeScore(BaseModel):
    faithfulness: float = Field(
        ...,
        description="Điểm trung thực của câu trả lời sinh ra so với phần ngữ cảnh được truy xuất (từ 0.0 đến 1.0). "
                    "Điểm 1.0 nghĩa là toàn bộ thông tin trong câu trả lời đều được hỗ trợ bởi ngữ cảnh. "
                    "Điểm 0.0 nghĩa là câu trả lời chứa các khẳng định sai lệch hoàn toàn so với ngữ cảnh."
    )
    answer_relevance: float = Field(
        ...,
        description="Điểm độ liên quan của câu trả lời đối với câu hỏi gốc của người học (từ 0.0 đến 1.0). "
                    "Điểm 1.0 nghĩa là câu trả lời đi thẳng vào trọng tâm câu hỏi và giải đáp chính xác. "
                    "Điểm 0.0 nghĩa là câu trả lời hoàn toàn lạc đề hoặc không liên quan gì đến câu hỏi."
    )
    verdict: bool = Field(
        ...,
        description="True nếu câu trả lời đạt yêu cầu chất lượng (Faithfulness >= 0.8 và Answer Relevance >= 0.8), "
                    "ngược lại nhận giá trị False nếu bị ảo giác thông tin hoặc trả lời không đúng trọng tâm."
    )
    reasoning: str = Field(
        ...,
        description="Lập luận chi tiết bằng tiếng Việt giải thích cho điểm số trên, chỉ rõ các luận điểm đúng hoặc sai lệch."
    )


def get_retrieved_context(chunk_ids: list[str]) -> str:
    """
    Truy vấn nội dung văn bản gốc của các đoạn tri thức RAG từ PostgreSQL dựa trên danh sách chunk_ids.
    """
    if not chunk_ids:
        return ""

    # Chuyển đổi chuỗi ID sang dạng integer để truy vấn
    ids = []
    for cid in chunk_ids:
        try:
            ids.append(int(cid))
        except (ValueError, TypeError):
            continue

    if not ids:
        return ""

    with Session(engine) as db_session:
        statement = select(BookSectionKnowledge).where(BookSectionKnowledge.id.in_(ids))
        chunks = db_session.exec(statement).all()
        # Sắp xếp các đoạn văn bản theo thứ tự xuất hiện ban đầu của chunk_ids nhận được từ trace
        chunk_map = {c.id: c.content for c in chunks}
        ordered_contents = [chunk_map[idx] for idx in ids if idx in chunk_map]
        return "\n\n".join(ordered_contents)


async def judge_answer(
    query: str,
    context: str,
    answer: str,
    *,
    model: str = "gpt-4o-mini",
) -> LLMJudgeScore:
    """
    Gọi API OpenAI để đóng vai trò làm trọng tài (LLM-as-a-Judge) chấm điểm
    độ trung thực (faithfulness) và độ liên quan (answer_relevance) của câu trả lời.
    """
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    system_prompt = (
        "Bạn là một chuyên gia kiểm định chất lượng học liệu số trong hệ thống trợ lý học tập TRIAM.\n"
        "Nhiệm vụ của bạn là đánh giá chất lượng câu trả lời của trợ lý ảo dựa trên câu hỏi của người học "
        "và phần ngữ cảnh sách (context) đã được truy xuất.\n"
        "Bạn cần phân tích kỹ lường xem câu trả lời có bám sát ngữ cảnh không (Faithfulness) "
        "và có trả lời trực tiếp câu hỏi không (Answer Relevance).\n"
        "Hãy cực kỳ nghiêm khắc với hiện tượng ảo giác (hallucination) — bất kỳ tuyên bố nào không có bằng chứng "
        "rõ ràng trong ngữ cảnh đều phải bị trừ điểm trung thực nặng."
    )

    user_prompt = (
        f"--- CÂU HỎI NGƯỜI HỌC ---\n{query}\n\n"
        f"--- NGỮ CẢNH TRÍ THỨC TRUY XUẤT ---\n{context}\n\n"
        f"--- CÂU TRẢ LỜI CỦA TRỢ LÝ ---\n{answer}\n"
    )

    # Sử dụng tính năng Structured Outputs của OpenAI SDK
    completion = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=LLMJudgeScore,
        temperature=0.0
    )

    return completion.choices[0].message.parsed

```

### app\services\agent_observability\model_eval_report.py

```py
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

MODEL_CONFIG_KEYS = (
    "AGENT_MODEL_PROFILE",
    "VOICE_AGENT_TEXT_LLM_MODEL",
    "OPENAI_STREAM_MODEL_NAME",
    "OPENAI_REALTIME_TRANSCRIPTION_MODEL",
    "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL",
)
RUNTIME_CONFIG_KEYS = (
    "BOOK_SECTION_EMBEDDING_VERSION",
    "BOOK_SECTION_RAG_MATCH_THRESHOLD",
    "BOOK_SECTION_RAG_MATCH_COUNT",
    "AGENT_RERANKER_ENABLED",
    "AGENT_RERANKER_MODEL",
    "AGENT_RERANKER_TOP_N",
    "AGENT_HYBRID_MIN_FINAL_SCORE",
    "AGENT_HYBRID_MAX_CONTEXT_CHUNKS",
)
REPORT_CONFIG_KEYS = MODEL_CONFIG_KEYS + RUNTIME_CONFIG_KEYS
MODEL_ENV_ALLOWLIST = set(MODEL_CONFIG_KEYS) - {"AGENT_MODEL_PROFILE"}
BOOK_SOURCES = {"book_metadata", "book_section", "book_rag"}
SNAPSHOT_COMPARE_KEYS = (
    "database_label",
    "book_id",
    "book_sections_count",
    "book_section_knowledge_count",
    "embedding_model",
    "embedding_version",
    "outline_hash",
    "app_git_sha",
)


def _trace_section_ids(trace: dict[str, Any] | None) -> set[str]:
    if not trace:
        return set()
    return set(trace.get("resolved_section_ids") or []) | set(trace.get("retrieval_section_ids") or [])


def _section_failure_is_trace_coverage(
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> bool:
    return (
        not _trace_section_ids(trace)
        and checks.get("expected_intent") is True
        and checks.get("expected_answer_source") is True
        and checks.get("must_include") is not False
        and checks.get("must_not_include") is not False
    )


def _content_failure_is_fixture_review(
    checks: dict[str, bool | None],
    actual_source: Any,
) -> bool:
    return (
        checks.get("expected_intent") is True
        and checks.get("expected_answer_source") is True
        and checks.get("expected_section") in (True, None)
        and actual_source in {"book_metadata", "book_section"}
    )


def _input_and_web_failures(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    *,
    actual_source: Any,
) -> list[str]:
    failures: list[str] = []
    expected_source = case.get("expected_answer_source")
    if checks.get("trace_available") is False:
        failures.append("TRACE_COVERAGE")
    if checks.get("voice_transcript_meaning") is False:
        failures.append("INPUT_STT")
    if checks.get("web_not_used_without_permission") is False:
        failures.append("WEB_PERMISSION")
    if checks.get("expected_answer_source") is False and expected_source in BOOK_SOURCES and actual_source in {"policy", "web"}:
        failures.append("WEB_PERMISSION")
    return failures


def _routing_failures(
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    if checks.get("expected_intent") is False:
        failures.append("ROUTING_INTENT")
    if checks.get("expected_section") is False:
        failures.append("TRACE_COVERAGE" if _section_failure_is_trace_coverage(checks, trace) else "ROUTING_SECTION")
    return failures


def _content_failures(
    checks: dict[str, bool | None],
    *,
    actual_source: Any,
    retrieval_count: int,
) -> list[str]:
    if checks.get("must_include") is not False and checks.get("must_not_include") is not False:
        return []
    if _content_failure_is_fixture_review(checks, actual_source):
        return ["EVAL_FIXTURE_MISMATCH"]
    return ["RETRIEVAL_RELEVANCE" if retrieval_count else "RETRIEVAL_COVERAGE"]


def _voice_tool_bypass_failures(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    if trace is None:
        return []
    if case.get("input_mode") != "voice":
        return []
    if case.get("expected_answer_source") not in BOOK_SOURCES:
        return []
    if checks.get("voice_transcript_meaning") is False:
        return []
    if checks.get("must_include") is False or checks.get("must_not_include") is False:
        return []

    actual_source = str(trace.get("answer_source") or "unknown").casefold()
    tool_names = trace.get("tool_names") or []
    if actual_source in {"unknown", "none", ""} and not tool_names:
        return ["VOICE_TOOL_BYPASS"]
    return []


def percentile(values: list[int], quantile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return round(ordered[lower] + (ordered[upper] - ordered[lower]) * fraction)


def latency_summary(values: list[int]) -> dict[str, int | None]:
    return {
        "samples": len(values),
        "p50_ms": percentile(values, 0.50),
        "p95_ms": percentile(values, 0.95),
        "max_ms": max(values) if values else None,
    }


def classify_failure_codes(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    actual_source = trace.get("answer_source") if trace else None
    retrieval_count = int(trace.get("retrieval_result_count") or 0) if trace else 0

    failures.extend(_input_and_web_failures(case, checks, actual_source=actual_source))
    failures.extend(_voice_tool_bypass_failures(case, checks, trace))
    if "VOICE_TOOL_BYPASS" not in failures:
        failures.extend(_routing_failures(checks, trace))
        if checks.get("expected_answer_source") is False and "WEB_PERMISSION" not in failures:
            failures.append("CONTEXT_VALIDATION")
        failures.extend(_content_failures(checks, actual_source=actual_source, retrieval_count=retrieval_count))
    if checks.get("llm_verdict") is False:
        failures.append("LLM_JUDGE")

    return list(dict.fromkeys(failures)) or ["UNKNOWN"]


def classify_exception_failure_codes(
    *,
    input_mode: str,
    error_type: str,
    error_message: str,
) -> list[str]:
    normalized = f"{error_type} {error_message}".casefold()
    if input_mode == "voice" and "transcript role=user" in normalized:
        return ["NO_USER_TRANSCRIPT"]
    if "timeout" in normalized or "timed out" in normalized:
        return ["INPUT_TIMEOUT"]
    if "voice fixture" in normalized or "wav" in normalized:
        return ["INPUT_AUDIO_FIXTURE"]
    return ["UNKNOWN"]


def build_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    check_names = {
        "content_accuracy": ("must_include", "must_not_include"),
        "intent_accuracy": ("expected_intent",),
        "answer_source_accuracy": ("expected_answer_source",),
        "section_resolution_accuracy": ("expected_section",),
        "web_policy_safety_rate": ("web_not_used_without_permission",),
        "voice_meaning_preservation_rate": ("voice_transcript_meaning",),
        "llm_judge_accuracy": ("llm_verdict",),
    }
    accuracy: dict[str, dict[str, int | float]] = {}
    for metric_name, names in check_names.items():
        values: list[bool] = []
        for result in results:
            checks = result.get("checks") or {}
            selected = [checks.get(name) for name in names if checks.get(name) is not None]
            if selected:
                values.append(all(selected))
        passed = sum(values)
        accuracy[metric_name] = {
            "passed": passed,
            "evaluated": len(values),
            "rate": round(passed / len(values), 4) if values else 0.0,
        }

    latency: dict[str, dict[str, dict[str, int | None]]] = {}
    for mode in ("text", "voice"):
        mode_results = [result for result in results if result.get("input_mode") == mode]
        turn_values = [
            int(result["trace"]["stage_latency_ms"]["turn_total"])
            for result in mode_results
            if result.get("trace") and result["trace"].get("stage_latency_ms", {}).get("turn_total") is not None
        ]
        retrieval_values = [
            int(result["trace"]["stage_latency_ms"]["retrieval"])
            for result in mode_results
            if result.get("trace") and result["trace"].get("stage_latency_ms", {}).get("retrieval") is not None
        ]
        if mode_results:
            latency[mode] = {
                "turn_total": latency_summary(turn_values),
                "retrieval": latency_summary(retrieval_values),
            }

    failure_counts = Counter(code for result in results for code in result.get("failure_codes", []))
    warning_counts = Counter(code for result in results for code in result.get("warnings", []))
    web_permission_violations = failure_counts.get("WEB_PERMISSION", 0)
    return {
        "strict_case_pass_rate": round(sum(result.get("status") == "passed" for result in results) / len(results), 4) if results else 0.0,
        "accuracy": accuracy,
        "latency": latency,
        "failure_counts": dict(sorted(failure_counts.items())),
        "warning_counts": dict(sorted(warning_counts.items())),
        "web_permission_violations": web_permission_violations,
    }


def summarize_results(results: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(results),
        "passed": sum(result.get("status") == "passed" for result in results),
        "failed": sum(result.get("status") == "failed" for result in results),
    }


def safe_model_config_from_settings(settings_obj: Any) -> dict[str, str]:
    return {
        key: str(getattr(settings_obj, key, ""))
        for key in REPORT_CONFIG_KEYS
    }


def validate_candidate_matrix(candidates: list[dict[str, Any]]) -> None:
    seen_names: set[str] = set()
    for candidate in candidates:
        name = str(candidate.get("name") or "").strip()
        if not name:
            raise ValueError("Candidate matrix item is missing name.")
        if name in seen_names:
            raise ValueError(f"Duplicate candidate name: {name}")
        seen_names.add(name)

        env = candidate.get("env")
        if not isinstance(env, dict):
            raise ValueError(f"Candidate {name} env must be an object.")

        disallowed = sorted(set(env) - MODEL_ENV_ALLOWLIST)
        if disallowed:
            raise ValueError(f"Candidate {name} uses disallowed env keys: {', '.join(disallowed)}")

        if name != "baseline" and len(env) > 1 and not candidate.get("combined_experiment"):
            unique_values = {key: value for key, value in env.items() if value not in (None, "", "<candidate-model>", "<candidate-realtime-model>")}
            if len(unique_values) > 1:
                raise ValueError(f"Candidate {name} changes multiple model surfaces without combined_experiment=true.")


def load_candidate_matrix(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Candidate matrix must be a list.")
    validate_candidate_matrix(payload)
    return payload


def find_candidate(candidates: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for candidate in candidates:
        if candidate.get("name") == name:
            return candidate
    raise ValueError(f"Candidate not found: {name}")


def _safe_outline_items(outline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": str(item.get("id") or ""),
            "path": str(item.get("path") or ""),
            "title": str(item.get("title") or ""),
        }
        for item in outline
    ]


def build_snapshot_metadata(
    *,
    book: dict[str, Any],
    outline: list[dict[str, Any]],
    app_git_sha: str,
    database_label: str,
    embedding_model: str,
    embedding_version: str,
    book_section_knowledge_count: int | None = None,
) -> dict[str, Any]:
    safe_outline = _safe_outline_items(outline)
    outline_hash = hashlib.sha256(json.dumps(safe_outline, ensure_ascii=True, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "book_id": str(book.get("id") or ""),
        "thread_id": None,
        "book_sections_count": len(outline),
        "book_section_knowledge_count": book_section_knowledge_count,
        "embedding_model": embedding_model,
        "embedding_version": embedding_version,
        "outline_hash": outline_hash,
        "app_git_sha": app_git_sha,
        "database_label": database_label,
    }


def snapshots_compatible(baseline: dict[str, Any], candidate: dict[str, Any]) -> tuple[bool, list[str]]:
    mismatches: list[str] = []
    for key in SNAPSHOT_COMPARE_KEYS:
        left = baseline.get(key)
        right = candidate.get(key)
        if left in (None, "", "unknown") or right in (None, "", "unknown"):
            continue
        if left != right:
            mismatches.append(key)
    return not mismatches, mismatches


def _metric_rate(report: dict[str, Any], metric_name: str) -> float:
    return float(report.get("metrics", {}).get("accuracy", {}).get(metric_name, {}).get("rate", 0.0))


def compare_reports(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    max_chat_p95_regression_ratio: float = 0.30,
    max_voice_p95_regression_ratio: float = 0.25,
) -> dict[str, Any]:
    compatible, snapshot_mismatches = snapshots_compatible(baseline.get("snapshot") or {}, candidate.get("snapshot") or {})
    hard_gate_failures: list[str] = []
    warnings: list[str] = []

    if not compatible:
        hard_gate_failures.append("SNAPSHOT_MISMATCH")

    if int(candidate.get("metrics", {}).get("web_permission_violations") or 0) > 0:
        hard_gate_failures.append("WEB_PERMISSION_VIOLATION")

    if _metric_rate(candidate, "answer_source_accuracy") < _metric_rate(baseline, "answer_source_accuracy"):
        hard_gate_failures.append("SOURCE_ACCURACY_REGRESSION")

    if _metric_rate(candidate, "content_accuracy") < _metric_rate(baseline, "content_accuracy"):
        hard_gate_failures.append("CONTENT_ACCURACY_REGRESSION")

    latency_warnings = _compare_latency_regression(
        baseline,
        candidate,
        max_chat_p95_regression_ratio=max_chat_p95_regression_ratio,
        max_voice_p95_regression_ratio=max_voice_p95_regression_ratio,
    )
    warnings.extend(latency_warnings)

    recommendation = "go" if not hard_gate_failures else "no-go"
    return {
        "recommendation": recommendation,
        "hard_gate_failures": hard_gate_failures,
        "warnings": warnings,
        "snapshot_mismatches": snapshot_mismatches,
        "baseline_candidate": baseline.get("candidate"),
        "candidate": candidate.get("candidate"),
        "metric_deltas": {
            name: round(_metric_rate(candidate, name) - _metric_rate(baseline, name), 4)
            for name in ("content_accuracy", "answer_source_accuracy", "intent_accuracy", "voice_meaning_preservation_rate")
        },
    }


def _compare_latency_regression(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    max_chat_p95_regression_ratio: float,
    max_voice_p95_regression_ratio: float,
) -> list[str]:
    warnings: list[str] = []
    thresholds = {
        "text": max_chat_p95_regression_ratio,
        "voice": max_voice_p95_regression_ratio,
    }
    for mode, threshold in thresholds.items():
        base_p95 = baseline.get("metrics", {}).get("latency", {}).get(mode, {}).get("turn_total", {}).get("p95_ms")
        cand_p95 = candidate.get("metrics", {}).get("latency", {}).get(mode, {}).get("turn_total", {}).get("p95_ms")
        if not base_p95 or not cand_p95:
            continue
        if cand_p95 > base_p95 * (1 + threshold):
            warnings.append(f"{mode.upper()}_P95_LATENCY_REGRESSION")
    return warnings


def write_eval_reports(output_dir: Path, report: dict[str, Any], *, prefix: str = "phase10_7_eval") -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate_name = str(report.get("candidate") or "unknown").replace(" ", "_")
    json_path = output_dir / f"{prefix}_{timestamp}_{candidate_name}.json"
    md_path = output_dir / f"{prefix}_{timestamp}_{candidate_name}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 10 Agent Model Evaluation Run",
        "",
        f"- Candidate: `{report.get('candidate')}`",
        f"- Environment: `{report.get('environment')}`",
        f"- Book: `{report.get('ground_truth', {}).get('title')}`",
        f"- Cases: `{report.get('summary', {}).get('total')}`",
        f"- Passed: `{report.get('summary', {}).get('passed')}`",
        f"- Failed: `{report.get('summary', {}).get('failed')}`",
        f"- DB message delta: `{report.get('db_message_delta')}`",
        "",
    ]
    voice_isolation = report.get("voice_isolation")
    if isinstance(voice_isolation, dict):
        lines.extend(
            [
                "## Voice Isolation",
                "",
                f"- Enabled: `{voice_isolation.get('enabled')}`",
                f"- Strategy: `{voice_isolation.get('strategy')}`",
                f"- Isolation Quality: `{voice_isolation.get('quality')}`",
                f"- Eval Threads: `{voice_isolation.get('thread_count')}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Model Config",
            "",
            "| Key | Value |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{key}` | `{value}` |" for key, value in (report.get("model_config") or {}).items())
    lines.extend(
        [
            "",
            "## Snapshot",
            "",
            "| Key | Value |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{key}` | `{value}` |" for key, value in (report.get("snapshot") or {}).items())
    lines.extend(
        [
            "",
            "## Accuracy",
            "",
            "| Metric | Passed | Evaluated | Rate |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    lines.extend(
        f"| {name} | {metric['passed']} | {metric['evaluated']} | {metric['rate']:.1%} |"
        for name, metric in report.get("metrics", {}).get("accuracy", {}).items()
    )
    lines.extend(
        [
            "",
            "## Failures",
            "",
            "| Failure code | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(f"| {code} | {count} |" for code, count in report.get("metrics", {}).get("failure_counts", {}).items())
    warning_counts = report.get("metrics", {}).get("warning_counts", {})
    if warning_counts:
        lines.extend(
            [
                "",
                "## Warnings",
                "",
                "| Warning code | Count |",
                "| --- | ---: |",
            ]
        )
        lines.extend(f"| {code} | {count} |" for code, count in warning_counts.items())
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Mode | Status |",
            "| --- | --- | --- |",
        ]
    )
    lines.extend(f"| {result['id']} | {result['input_mode']} | {result['status']} |" for result in report.get("results", []))
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path

```

### app\services\agent_observability\turn_trace.py

```py
from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from app.core.logger import log
from app.services.agent_observability.contracts import AgentAnswerSource, AgentInputMode, AgentTurnTrace

TraceEmitter = Callable[[str, dict[str, Any]], None]


def _default_emitter(event: str, payload: dict[str, Any]) -> None:
    log.info(f"AGENT_TRACE {event} | {json.dumps(payload, ensure_ascii=True, sort_keys=True)}")


def _string_values(items: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for item in items:
        value = item.get(key)
        if value is not None:
            values.append(str(value))
    return list(dict.fromkeys(values))


class AgentTurnTracer:
    """Session-scoped, best-effort trace collector that never stores raw content."""

    def __init__(
        self,
        *,
        enabled: bool,
        thread_id: str | None,
        room_name: str | None,
        score_precision: int = 4,
        late_transcript_window_seconds: float = 15.0,
        emitter: TraceEmitter | None = None,
    ) -> None:
        self.enabled = enabled
        self.thread_id = thread_id
        self.room_name = room_name
        self.score_precision = max(0, score_precision)
        self.late_transcript_window_seconds = max(0.0, late_transcript_window_seconds)
        self._emitter = emitter or _default_emitter
        self._active: dict[AgentInputMode, AgentTurnTrace] = {}
        self._last_completed: dict[AgentInputMode, AgentTurnTrace] = {}

    def begin_turn(self, input_mode: AgentInputMode) -> str | None:
        if not self.enabled:
            return None

        if input_mode in self._active:
            self.complete_turn(input_mode, error_code="superseded_by_new_turn")

        trace = AgentTurnTrace(
            trace_id=str(uuid.uuid4()),
            thread_id=self.thread_id,
            room_name=self.room_name,
            input_mode=input_mode,
            started_at=datetime.now(timezone.utc),
            started_monotonic=time.monotonic(),
        )
        self._active[input_mode] = trace
        self._emit_safe("turn_started", self._summary(trace))
        return trace.trace_id

    def ensure_turn(self, input_mode: AgentInputMode) -> str | None:
        trace = self._active.get(input_mode)
        if trace:
            return trace.trace_id
        return self.begin_turn(input_mode)

    def has_active_turn(self, input_mode: AgentInputMode) -> bool:
        return input_mode in self._active

    def record_transcript(
        self,
        input_mode: AgentInputMode,
        *,
        char_count: int,
        language: str | None = None,
        final: bool = True,
    ) -> None:
        if not self.enabled or not final:
            return

        trace = self._active.get(input_mode)
        late_update = False
        if trace is None:
            candidate = self._last_completed.get(input_mode)
            if candidate and not candidate.transcript_final_seen and candidate.completed_monotonic is not None:
                late_update = time.monotonic() - candidate.completed_monotonic <= self.late_transcript_window_seconds
                if late_update:
                    trace = candidate

        if trace is None:
            self.ensure_turn(input_mode)
            trace = self._active.get(input_mode)
        if trace is None:
            return

        trace.transcript_final_seen = True
        trace.transcript_char_count = max(0, char_count)
        trace.detected_language = language
        if late_update:
            trace.correlation_quality = "late_transcript_last_completed_turn"
            self._emit_safe("late_transcript", self._summary(trace))

    def record_tool(self, input_mode: AgentInputMode, tool_name: str) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None and tool_name not in trace.tool_names:
            trace.tool_names.append(tool_name)

    def record_retrieval(
        self,
        input_mode: AgentInputMode,
        payload: Any,
        *,
        elapsed_ms: int,
        method: str = "vector",
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return

        items = [item for item in payload if isinstance(item, dict)] if isinstance(payload, list) else []
        trace.retrieval_method = method
        trace.retrieval_result_count = len(items)
        trace.retrieval_chunk_ids = _string_values(items, "id")
        trace.retrieval_learning_unit_ids = _string_values(items, "learning_unit_id")
        trace.retrieval_section_ids = _string_values(items, "section_id")
        trace.retrieval_scores = [
            round(float(item["similarity"]), self.score_precision)
            for item in items
            if isinstance(item.get("similarity"), int | float)
        ]
        trace.stage_latency_ms["retrieval"] = max(0, elapsed_ms)
        self._emit_safe("retrieval_completed", self._summary(trace))

    def record_grounding_decision(
        self,
        input_mode: AgentInputMode,
        *,
        intent: str,
        route: str,
        reason_code: str,
        resolved_book_ids: list[str],
        resolved_section_ids: list[str],
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.detected_intent = intent
        trace.grounding_route = route
        trace.grounding_reason_code = reason_code
        trace.resolved_book_ids = list(dict.fromkeys(resolved_book_ids))
        trace.resolved_section_ids = list(dict.fromkeys(resolved_section_ids))
        self._emit_safe("grounding_resolved", self._summary(trace))

    def record_latency(self, input_mode: AgentInputMode, stage: str, elapsed_ms: int) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.stage_latency_ms[stage] = max(0, elapsed_ms)

    def record_query_guard(
        self,
        input_mode: AgentInputMode,
        *,
        reason_code: str,
        guard_mode: str,
        overlap_ratio: float | None = None,
        important_overlap_ratio: float | None = None,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.query_guard_reason_code = reason_code
        trace.query_guard_mode = guard_mode
        trace.query_guard_overlap_ratio = (
            round(overlap_ratio, self.score_precision) if overlap_ratio is not None else None
        )
        trace.query_guard_important_overlap_ratio = (
            round(important_overlap_ratio, self.score_precision)
            if important_overlap_ratio is not None
            else None
        )

    def record_answer_source(self, input_mode: AgentInputMode, source: AgentAnswerSource) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.answer_source = source

    def record_assistant(self, input_mode: AgentInputMode, *, char_count: int) -> None:
        trace = self._active.get(input_mode)
        if trace is not None:
            trace.assistant_char_count = max(0, char_count)

    def record_error(self, input_mode: AgentInputMode, error_code: str) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is not None:
            trace.error_code = error_code
            trace.answer_source = AgentAnswerSource.ERROR

    def record_tool_reply_watchdog_scheduled(
        self,
        input_mode: AgentInputMode,
        *,
        tool_name: str,
        grace_ms: int,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_scheduled = True
        if tool_name not in trace.tool_reply_watchdog_tool_names:
            trace.tool_reply_watchdog_tool_names.append(tool_name)
        trace.stage_latency_ms["tool_reply_watchdog_grace"] = grace_ms
        self._emit_safe("watchdog_scheduled", self._summary(trace))

    def record_tool_reply_watchdog_fired(
        self,
        input_mode: AgentInputMode,
        *,
        tool_name: str,
        elapsed_ms: int | None,
        reason: str,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_fired = True
        trace.tool_reply_watchdog_reason = reason
        trace.forced_reply_reason = reason
        if elapsed_ms is not None:
            trace.tool_result_to_speech_ms = elapsed_ms
        self._emit_safe("watchdog_fired", self._summary(trace))

    def record_tool_reply_watchdog_bypassed(
        self,
        input_mode: AgentInputMode,
        *,
        reason: str,
        tool_name: str,
    ) -> None:
        trace = self._get_or_begin(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_fired = False
        trace.tool_reply_watchdog_reason = reason
        self._emit_safe("watchdog_bypassed", self._summary(trace))

    def record_tool_reply_watchdog_cancelled(
        self,
        input_mode: AgentInputMode,
        *,
        reason: str,
    ) -> None:
        trace = self._active.get(input_mode)
        if trace is None:
            return
        trace.tool_reply_watchdog_reason = f"cancelled_{reason}"
        self._emit_safe("watchdog_cancelled", self._summary(trace))

    def record_tool_reply_speech_created(
        self,
        input_mode: AgentInputMode,
        *,
        source: str | None = None,
        elapsed_ms: int | None = None,
    ) -> None:
        trace = self._active.get(input_mode)
        if trace is None:
            return
        if elapsed_ms is not None:
            trace.tool_result_to_speech_ms = elapsed_ms
        self._emit_safe("speech_created", self._summary(trace))

    def complete_turn(self, input_mode: AgentInputMode, *, error_code: str | None = None) -> dict[str, Any] | None:
        if not self.enabled:
            return None

        trace = self._active.pop(input_mode, None)
        if trace is None:
            return None

        trace.completed_at = datetime.now(timezone.utc)
        trace.completed_monotonic = time.monotonic()
        trace.stage_latency_ms["turn_total"] = max(0, int((trace.completed_monotonic - trace.started_monotonic) * 1000))
        if error_code:
            trace.error_code = error_code
        self._last_completed[input_mode] = trace
        summary = self._summary(trace)
        self._emit_safe("turn_completed", summary)
        return summary

    def _get_or_begin(self, input_mode: AgentInputMode) -> AgentTurnTrace | None:
        if not self.enabled:
            return None
        if input_mode not in self._active:
            self.begin_turn(input_mode)
        return self._active.get(input_mode)

    def _emit_safe(self, event: str, payload: dict[str, Any]) -> None:
        try:
            self._emitter(event, payload)
        except Exception as exc:
            log.warning(f"Agent trace emit failed | event={event} | error_type={type(exc).__name__}")

    @staticmethod
    def _summary(trace: AgentTurnTrace) -> dict[str, Any]:
        return {
            "trace_id": trace.trace_id,
            "thread_id": trace.thread_id,
            "room_name": trace.room_name,
            "input_mode": trace.input_mode.value,
            "started_at": trace.started_at.isoformat(),
            "completed_at": trace.completed_at.isoformat() if trace.completed_at else None,
            "transcript_final_seen": trace.transcript_final_seen,
            "transcript_char_count": trace.transcript_char_count,
            "detected_language": trace.detected_language,
            "detected_intent": trace.detected_intent,
            "grounding_route": trace.grounding_route,
            "grounding_reason_code": trace.grounding_reason_code,
            "resolved_book_ids": trace.resolved_book_ids,
            "resolved_section_ids": trace.resolved_section_ids,
            "retrieval_method": trace.retrieval_method,
            "retrieval_result_count": trace.retrieval_result_count,
            "retrieval_chunk_ids": trace.retrieval_chunk_ids,
            "retrieval_learning_unit_ids": trace.retrieval_learning_unit_ids,
            "retrieval_section_ids": trace.retrieval_section_ids,
            "retrieval_scores": trace.retrieval_scores,
            "tool_names": trace.tool_names,
            "query_guard_reason_code": trace.query_guard_reason_code,
            "query_guard_mode": trace.query_guard_mode,
            "query_guard_overlap_ratio": trace.query_guard_overlap_ratio,
            "query_guard_important_overlap_ratio": trace.query_guard_important_overlap_ratio,
            "answer_source": trace.answer_source.value,
            "assistant_char_count": trace.assistant_char_count,
            "stage_latency_ms": trace.stage_latency_ms,
            "error_code": trace.error_code,
            "tool_reply_watchdog_scheduled": trace.tool_reply_watchdog_scheduled,
            "tool_reply_watchdog_fired": trace.tool_reply_watchdog_fired,
            "tool_reply_watchdog_tool_names": trace.tool_reply_watchdog_tool_names,
            "tool_reply_watchdog_reason": trace.tool_reply_watchdog_reason,
            "tool_result_to_speech_ms": trace.tool_result_to_speech_ms,
            "forced_reply_reason": trace.forced_reply_reason,
            "correlation_quality": trace.correlation_quality,
        }

```

### app\services\agent_observability\__init__.py

```py
from app.services.agent_observability.contracts import AgentAnswerSource, AgentInputMode, AgentTurnTrace
from app.services.agent_observability.turn_trace import AgentTurnTracer

__all__ = [
    "AgentAnswerSource",
    "AgentInputMode",
    "AgentTurnTrace",
    "AgentTurnTracer",
]

```

### app\services\agent_policy\contracts.py

```py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.services.agent_observability import AgentAnswerSource, AgentInputMode


class AgentPolicyAction(str, Enum):
    DIRECT_ANSWER = "direct_answer"
    ANSWER_WITH_SECTION_CONTEXT = "answer_with_section_context"
    ANSWER_WITH_RAG_CONTEXT = "answer_with_rag_context"
    ASK_CLARIFICATION = "ask_clarification"
    ASK_WEB_PERMISSION = "ask_web_permission"
    WEB_DISABLED = "web_disabled"
    ERROR = "error"


@dataclass(frozen=True)
class AgentPolicyRequest:
    query: str
    input_mode: AgentInputMode
    document_ids: list[str]
    allow_web_permission: bool


@dataclass(frozen=True)
class AgentPolicyResult:
    action: AgentPolicyAction
    answer_source: AgentAnswerSource
    reason_code: str
    message_key: str | None = None
    message_params: dict[str, str] = field(default_factory=dict)
    user_message: str | None = None
    tool_marker: str | None = None
    llm_system_context: str | None = None
    resolved_book_ids: tuple[str, ...] = field(default_factory=tuple)
    resolved_section_ids: tuple[str, ...] = field(default_factory=tuple)
    retrieval_chunk_ids: tuple[str, ...] = field(default_factory=tuple)
    retrieval_result_count: int = 0

```

### app\services\agent_policy\renderers.py

```py
from __future__ import annotations

from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyResult

SECTION_TEXT_ANSWER_INSTRUCTIONS = """
Answer the user's question in Vietnamese using only SECTION_CONTEXT below.
Do not use model memory, other chapters, or web search.
For a summary or "what happens" question, cover the major events or ideas across
the beginning, middle, and ending of the entire available section context.
Do not stop after describing only the opening excerpt.
Keep the answer factual and concise, normally 3-5 sentences.
If the context says it was truncated, state that the answer is based on the available excerpt.

SECTION_CONTEXT:
{section_context}
""".strip()

RAG_TEXT_ANSWER_INSTRUCTIONS = """
Answer the user's question in Vietnamese using only BOOK_CONTEXT below.
Do not use model memory, other chapters, or web search.
Keep the answer factual and concise, normally 2-4 sentences.
If the context is weak or incomplete, say that the book context is not enough.

BOOK_CONTEXT:
{book_context}
""".strip()

MESSAGE_TEMPLATES = {
    "ask_clarification": "{clarification}",
    "book_context_error": "Không thể tìm kiếm dữ liệu trong sách lúc này.",
    "book_context_not_found": "Mình chưa tìm thấy thông tin phù hợp trong sách cho câu hỏi này.",
    "section_unavailable": "{message}",
    "web_disabled": "Câu hỏi này cần thông tin ngoài sách, nhưng tìm kiếm internet hiện đang tắt.",
}


def build_section_text_context(section_context: str) -> str:
    return SECTION_TEXT_ANSWER_INSTRUCTIONS.format(section_context=section_context)


def build_rag_text_context(book_context: str) -> str:
    return RAG_TEXT_ANSWER_INSTRUCTIONS.format(book_context=book_context)


def render_text_direct_message(result: AgentPolicyResult) -> str:
    if result.user_message:
        return result.user_message
    if result.message_key:
        template = MESSAGE_TEMPLATES.get(result.message_key)
        if template:
            return template.format(**result.message_params)
    return "Mình chưa có đủ thông tin để trả lời chắc chắn."


def render_voice_tool_result(result: AgentPolicyResult) -> str:
    if result.tool_marker:
        return result.tool_marker

    message = render_text_direct_message(result)
    if result.action == AgentPolicyAction.DIRECT_ANSWER:
        return f"BOOK_METADATA_FOUND:\n{message}"
    if result.action == AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT and result.llm_system_context:
        return (
            "BOOK_SECTION_FOUND:\n"
            f"{result.llm_system_context}\n"
            "Answer only from this section context. Do not use model memory or request web search."
        )
    if result.action == AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT and result.llm_system_context:
        return f"BOOK_CONTEXT_FOUND:\n{result.llm_system_context}"
    if result.action == AgentPolicyAction.ASK_CLARIFICATION:
        return f"CLARIFICATION_REQUIRED:\n{message}"
    if result.action == AgentPolicyAction.ASK_WEB_PERMISSION:
        return f"BOOK_CONTEXT_NOT_FOUND: {message}"
    if result.action == AgentPolicyAction.WEB_DISABLED:
        return f"BOOK_CONTEXT_NOT_FOUND: {message}"
    if result.action == AgentPolicyAction.ERROR:
        return f"BOOK_CONTEXT_ERROR: {message}"
    return message

```

### app\services\agent_policy\shared_policy.py

```py
from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from app.core.logger import log
from app.services.agent_grounding import GroundingResult, GroundingRoute, GroundingRouter
from app.services.agent_grounding.response_renderer import format_grounding_tool_result
from app.services.agent_observability import AgentAnswerSource, AgentTurnTracer
from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyRequest, AgentPolicyResult
from app.services.agent_policy.renderers import build_rag_text_context, build_section_text_context
from app.services.voice_agent.contracts import VoiceRagResult
from app.services.voice_agent.rag_context import format_rag_context, search_voice_book_context

SearchBookContext = Callable[..., Awaitable[VoiceRagResult]]


class SharedAgentPolicy:
    """Session-scoped policy for text and voice book-grounded decisions.

    This object intentionally holds session-specific state references such as
    tracer and document_ids, so it must never be created as a process-global
    singleton.
    """

    def __init__(
        self,
        *,
        document_ids: list[str],
        grounding_router: GroundingRouter | None,
        tracer: AgentTurnTracer,
        search_book_context: SearchBookContext = search_voice_book_context,
    ) -> None:
        self.document_ids = document_ids
        self.grounding_router = grounding_router
        self.tracer = tracer
        self.search_book_context = search_book_context

    async def resolve(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        started = time.perf_counter()
        try:
            result = await self._resolve(request)
            return result
        finally:
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            resolved = locals().get("result")
            if isinstance(resolved, AgentPolicyResult):
                log.info(
                    "Agent shared policy resolved | "
                    f"mode={request.input_mode.value} | "
                    f"action={resolved.action.value} | "
                    f"source={resolved.answer_source.value} | "
                    f"reason={resolved.reason_code} | "
                    f"books={len(resolved.resolved_book_ids)} | "
                    f"sections={len(resolved.resolved_section_ids)} | "
                    f"retrieval_count={resolved.retrieval_result_count} | "
                    f"latency_ms={elapsed_ms}"
                )

    async def _resolve(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        if self.grounding_router is not None:
            grounding_result = await self.grounding_router.resolve(
                request.query,
                input_mode=request.input_mode,
                tracer=self.tracer,
            )
            if grounding_result.decision.route != GroundingRoute.BOOK_RAG:
                return self._from_grounding_result(grounding_result, request)

        return await self._resolve_rag(request)

    def _from_grounding_result(
        self,
        grounding_result: GroundingResult,
        request: AgentPolicyRequest,
    ) -> AgentPolicyResult:
        decision = grounding_result.decision
        resolved_book_ids = tuple(str(value) for value in decision.resolved_book_ids)
        resolved_section_ids = tuple(str(value) for value in decision.resolved_section_ids)
        tool_marker = format_grounding_tool_result(grounding_result)

        if decision.route == GroundingRoute.BOOK_METADATA:
            return AgentPolicyResult(
                action=AgentPolicyAction.DIRECT_ANSWER,
                answer_source=AgentAnswerSource.BOOK_METADATA,
                reason_code=decision.reason_code,
                user_message=grounding_result.deterministic_answer,
                tool_marker=tool_marker,
                resolved_book_ids=resolved_book_ids,
            )

        if decision.route == GroundingRoute.CLARIFICATION:
            return AgentPolicyResult(
                action=AgentPolicyAction.ASK_CLARIFICATION,
                answer_source=AgentAnswerSource.CLARIFICATION,
                reason_code=decision.reason_code,
                message_key="ask_clarification",
                message_params={"clarification": decision.clarification or "Bạn vui lòng nói rõ câu hỏi."},
                tool_marker=tool_marker,
            )

        if decision.route == GroundingRoute.BOOK_SECTION:
            if grounding_result.section_context:
                return AgentPolicyResult(
                    action=AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT,
                    answer_source=AgentAnswerSource.BOOK_SECTION,
                    reason_code=decision.reason_code,
                    tool_marker=tool_marker,
                    llm_system_context=build_section_text_context(grounding_result.section_context),
                    resolved_book_ids=resolved_book_ids,
                    resolved_section_ids=resolved_section_ids,
                )
            return AgentPolicyResult(
                action=AgentPolicyAction.DIRECT_ANSWER,
                answer_source=AgentAnswerSource.BOOK_SECTION,
                reason_code=decision.reason_code,
                message_key="section_unavailable",
                message_params={"message": grounding_result.deterministic_answer or "Nội dung section chưa được trích xuất."},
                user_message=grounding_result.deterministic_answer,
                tool_marker=tool_marker,
                resolved_book_ids=resolved_book_ids,
                resolved_section_ids=resolved_section_ids,
            )

        if decision.route == GroundingRoute.WEB_POLICY:
            if request.allow_web_permission:
                return AgentPolicyResult(
                    action=AgentPolicyAction.ASK_WEB_PERMISSION,
                    answer_source=AgentAnswerSource.POLICY,
                    reason_code=decision.reason_code,
                    tool_marker=tool_marker,
                    resolved_book_ids=resolved_book_ids,
                )
            return self._web_disabled(decision.reason_code)

        return self._error("unsupported_grounding_route")

    async def _resolve_rag(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        try:
            rag_result = await self.search_book_context(
                request.query,
                request.document_ids,
                tracer=self.tracer,
                input_mode=request.input_mode,
            )
        except Exception as exc:
            self.tracer.record_error(request.input_mode, "book_rag_search_error")
            log.warning(
                "Shared policy RAG search failed | "
                f"mode={request.input_mode.value} | "
                f"document_count={len(request.document_ids)} | "
                f"error_type={type(exc).__name__}"
            )
            return self._error("book_rag_search_error")

        if rag_result.found:
            self.tracer.record_answer_source(request.input_mode, AgentAnswerSource.BOOK_RAG)
            tool_marker = format_rag_context(rag_result)
            return AgentPolicyResult(
                action=AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT,
                answer_source=AgentAnswerSource.BOOK_RAG,
                reason_code="rag_context_found",
                tool_marker=tool_marker,
                llm_system_context=build_rag_text_context(tool_marker),
                retrieval_chunk_ids=_chunk_ids(rag_result),
                retrieval_result_count=len(rag_result.chunks),
            )

        if request.allow_web_permission:
            self.tracer.record_answer_source(request.input_mode, AgentAnswerSource.POLICY)
            return AgentPolicyResult(
                action=AgentPolicyAction.ASK_WEB_PERMISSION,
                answer_source=AgentAnswerSource.POLICY,
                reason_code="rag_context_not_found",
                message_key="book_context_not_found",
                tool_marker=format_rag_context(rag_result),
            )

        return self._web_disabled("rag_context_not_found")

    @staticmethod
    def _web_disabled(reason_code: str) -> AgentPolicyResult:
        return AgentPolicyResult(
            action=AgentPolicyAction.WEB_DISABLED,
            answer_source=AgentAnswerSource.POLICY,
            reason_code=reason_code,
            message_key="web_disabled",
        )

    @staticmethod
    def _error(reason_code: str) -> AgentPolicyResult:
        return AgentPolicyResult(
            action=AgentPolicyAction.ERROR,
            answer_source=AgentAnswerSource.ERROR,
            reason_code=reason_code,
            message_key="book_context_error",
        )


def _chunk_ids(result: VoiceRagResult) -> tuple[str, ...]:
    values: list[str] = []
    for item in result.chunks:
        chunk_id = item.get("id")
        if chunk_id is not None:
            values.append(str(chunk_id))
    return tuple(dict.fromkeys(values))

```

### app\services\agent_policy\__init__.py

```py
"""Shared policy layer for book-grounded text and realtime voice agents."""

from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyRequest, AgentPolicyResult
from app.services.agent_policy.renderers import render_text_direct_message, render_voice_tool_result
from app.services.agent_policy.shared_policy import SharedAgentPolicy

__all__ = [
    "AgentPolicyAction",
    "AgentPolicyRequest",
    "AgentPolicyResult",
    "SharedAgentPolicy",
    "render_text_direct_message",
    "render_voice_tool_result",
]

```

### app\services\agent_voice_gpt_realtime.py

```py
import asyncio
import json
import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    AgentStateChangedEvent,
    ConversationItemAddedEvent,
    FunctionToolsExecutedEvent,
    JobContext,
    JobExecutorType,
    SpeechCreatedEvent,
    UserStateChangedEvent,
    WorkerOptions,
    function_tool,
    room_io,
)
from livekit.agents import (
    llm as agents_llm,
)
from livekit.agents.llm import ChatMessage as LLMMessage
from livekit.agents.voice import io as voice_io
from livekit.plugins import noise_cancellation
from livekit.plugins.openai import LLM as OpenAILLM
from livekit.plugins.openai.realtime import RealtimeModel
from openai.types.realtime import AudioTranscription

from app.core.config import settings
from app.core.logger import log
from app.repositories.agent_grounding_repo import load_grounding_scope, load_scoped_section_texts
from app.services.agent_grounding import GroundingResult, GroundingRoute, GroundingRouter
from app.services.agent_grounding.response_renderer import format_grounding_tool_result
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer
from app.services.agent_policy import AgentPolicyAction, AgentPolicyRequest, SharedAgentPolicy, render_text_direct_message, render_voice_tool_result
from app.services.voice_agent.contracts import LK_CHAT_TOPIC, LK_CONTROL_TOPIC, VoiceJobMetadata
from app.services.voice_agent.query_guard import VoiceQueryGuardConfig, VoiceQueryGuardResult, guard_voice_book_query
from app.services.voice_agent.rag_context import format_rag_context, search_voice_book_context, trim_text
from app.services.voice_agent.tool_reply_watchdog import VoiceToolReplyWatchdog, VoiceToolReplyWatchdogConfig
from app.services.voice_agent.transcript_store import VoiceTranscriptStore, normalize_transcript_text
from app.services.voice_agent.transcription_prompt import build_realtime_transcription_prompt
from app.services.voice_agent.turn_state import VoiceTurnState
from app.services.voice_agent.web_permission_intent_classifier import normalize_intent_text
from app.services.voice_agent.web_permission_policy import WebSearchPermissionPolicy
from app.services.web_search_service import search_web as web_search

# FIX 1: Ép API Key vào biến môi trường để LiveKit SDK tự động nhận diện ngầm
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

CLARIFICATION_MARKER = "CLARIFICATION_REQUIRED:"
ASSISTANT_CLARIFICATION_MARKERS = (
    "ban muon",
    "y ban la",
    "dung khong",
    "phai khong",
    "ban dang hoi",
    "do you mean",
    "which chapter",
    "which section",
)


VOICE_AGENT_INSTRUCTIONS = """
You are TRIAM, a Vietnamese audiobook study assistant.

Core rules:
- Answer in Vietnamese only.
- Keep replies natural and short: 2-3 sentences.
- You are encouraged to use Markdown formatting (including headings, bold text, bullet/numbered lists, and tables) in your transcript text to make the on-screen display rich and structured. However, speak in a natural, conversational manner.
- If audio is unclear, partial, noisy, silent, or unintelligible, ask the user to repeat in Vietnamese.
- If the user asks a general/conceptual book question or requests a character/concept summary without specifying a chapter, do not ask them to specify a chapter. Answer directly using the provided context (e.g. from BOOK_CONTEXT_FOUND).

ASR spelling and homophone correction rules:
- The user's voice inputs are transcribed using Speech-to-Text (ASR) and may contain spelling mistakes, missing diacritics, or homophone errors (e.g., "sạch co máy chương" instead of "sách có mấy chương", "câu hỏi bi thảm" instead of "hậu quả bi thảm").
- You must dynamically map acoustically similar speech to the correct terms from the "Ngữ cảnh học tập hiện tại" or the recent conversation history.
- When calling functions like `search_book_knowledge`, always use the corrected spelling of the query (e.g., pass "sách có mấy chương" instead of "sạch co máy chương", and "hậu quả bi thảm" instead of "câu hỏi bi thảm").

Tool rules:
- For any question about book content, concepts, chapters, learning topics, or study context, ALWAYS call `search_book_knowledge` first.
- Treat `BOOK_METADATA_FOUND` as authoritative database metadata.
- Treat `BOOK_SECTION_FOUND` as the only source for the requested section.
- If the tool returns `CLARIFICATION_REQUIRED`, read the clarification and stop.
- If the tool returns `WEB_PERMISSION_REPLY_DETECTED`, continue the pending web-search permission flow; do not answer from book memory.
- If the tool returns `BOOK_SECTION_UNAVAILABLE` or `BOOK_CONTEXT_ERROR`, read the message and stop.
- Never request web search for `CLARIFICATION_REQUIRED` or a resolved book section.
- If the tool returns `EXTERNAL_INFO_REQUIRED` or `BOOK_CONTEXT_NOT_FOUND`, call `ask_web_search_permission` exactly once.
- Read the returned question, then stop and wait for the user.
- Do not call `search_book_knowledge` again in the same turn after a clarification, unavailable-section, context-error, or web-permission marker.
- Do not ask web-search permission in your own words. Always use `ask_web_search_permission` so the backend can track the pending request.
- After the user clearly agrees, call `execute_web_search` once for the pending query and answer from the result.
- NEVER call `execute_web_search` before the user grants permission.
- If `execute_web_search` returns a permission error, call `ask_web_search_permission` once and stop.
- If `execute_web_search` returns `WEB_SEARCH_PERMISSION_DENIED`, acknowledge the refusal and continue without web search.
- After `execute_web_search` returns a real web result, answer immediately from that result.
- Do not say you are still searching after a web result has been returned.
- Do not answer external or out-of-book facts from memory when web permission is required.
""".strip()


TEXT_AGENTIC_SYSTEM_INSTRUCTIONS = """
System facts:
- Current server time: {now_str}
- Use this server time for date/time questions.

Tool rules:
- For book-content questions, call `search_book_knowledge_text` first.
- Treat `BOOK_METADATA_FOUND` and `BOOK_SECTION_FOUND` as authoritative.
- If a tool returns `CLARIFICATION_REQUIRED`, ask that clarification and stop.
- If a tool returns `BOOK_SECTION_UNAVAILABLE` or `BOOK_CONTEXT_ERROR`, read the message and stop.
- If a tool returns `WEB_PERMISSION_REPLY_DETECTED`, continue the pending web-search permission flow; do not treat it as a new book question.
- If a tool returns `EXTERNAL_INFO_REQUIRED`, call `ask_web_search_permission_text`.
- For prices, news, recent events, or out-of-book facts, call `ask_web_search_permission_text` before any web search.
- If `search_book_knowledge_text` returns `BOOK_CONTEXT_NOT_FOUND`, call `ask_web_search_permission_text`.
- Call `execute_web_search_text` only after the user granted permission in the previous turn.
- If a tool returns `WEB_SEARCH_PERMISSION_REQUIRED` or `WEB_SEARCH_PERMISSION_UNCLEAR`, ask permission and stop.
- If a tool returns `WEB_SEARCH_PERMISSION_DENIED`, do not search the web.
- Do not call `search_book_knowledge_text` again in the same turn after a clarification, unavailable-section, context-error, or web-permission marker.
- Answer in Vietnamese only, keeping the response structured and focused. You are encouraged to use rich Markdown formatting (such as headings #/##, bold text **, lists, and tables) to present your answers beautifully and clearly on the UI.
- If the user asks a general/conceptual book question or requests a character/concept summary without specifying a chapter, do not ask them to specify a chapter. Answer directly using the provided context.
""".strip()

SECTION_TEXT_ANSWER_INSTRUCTIONS = """
Answer the user's question in Vietnamese using only SECTION_CONTEXT below.
Do not use model memory, other chapters, or web search.
For a summary or "what happens" question, cover the major events or ideas across
the beginning, middle, and ending of the entire available section context.
Do not stop after describing only the opening excerpt.
Keep the answer factual and concise, normally 3-5 sentences.
If the context says it was truncated, state that the answer is based on the available excerpt.

SECTION_CONTEXT:
{section_context}
""".strip()


WEB_GRANTED_REPLY_INSTRUCTIONS = """
The user just granted permission to search the web for the previous question.
Approved query: {query}

Web result:
{web_result}

Answer in Vietnamese only, briefly.
You are encouraged to use Markdown formatting (such as bold text, headings, bullet/numbered lists, and tables) to structure your explanation clearly based on the web results.
If the web result is weak or incomplete, say so.
""".strip()


GREETING_INSTRUCTIONS = (
    "Speak exactly the following greeting in Vietnamese: "
    '"Chào bạn, tôi là TRIAM đây. Bạn muốn thảo luận về chương sách nào hôm nay?" '
    "Under no circumstances should you call any tools (including search_book_knowledge) "
    "or attempt to answer any historical queries from previous turns. Just output the "
    "greeting text and finish this turn immediately."
)


def _get_job_executor_type() -> JobExecutorType:
    executor_type = settings.LIVEKIT_AGENT_JOB_EXECUTOR_TYPE.strip().lower()
    if executor_type == JobExecutorType.PROCESS.value:
        return JobExecutorType.PROCESS
    if executor_type == JobExecutorType.THREAD.value:
        return JobExecutorType.THREAD

    log.warning(f"Invalid LIVEKIT_AGENT_JOB_EXECUTOR_TYPE={settings.LIVEKIT_AGENT_JOB_EXECUTOR_TYPE!r}; falling back to thread")
    return JobExecutorType.THREAD


def _calculate_agent_load(server: Any) -> float:
    max_jobs = max(settings.LIVEKIT_AGENT_MAX_CONCURRENT_JOBS, 1)
    active_jobs = len(getattr(server, "active_jobs", []) or [])
    return min(active_jobs / max_jobs, 1.0)


def _coerce_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _parse_job_metadata(raw_metadata: str | None, room_name: str) -> VoiceJobMetadata:
    try:
        payload = json.loads(raw_metadata or "{}")
    except (json.JSONDecodeError, TypeError):
        payload = {}

    thread_id = str(payload.get("thread_id") or "")
    document_ids = _coerce_string_list(payload.get("document_ids"))
    book_id = str(payload.get("book_id") or "")

    if book_id and not document_ids:
        document_ids = [book_id]

    if room_name == "console":
        if not thread_id:
            thread_id = settings.VOICE_AGENT_CONSOLE_THREAD_ID
        if not document_ids and settings.VOICE_AGENT_CONSOLE_BOOK_ID:
            document_ids = [settings.VOICE_AGENT_CONSOLE_BOOK_ID]

    return VoiceJobMetadata(thread_id=thread_id, document_ids=document_ids)


def _extract_conversation_item_text(item: LLMMessage) -> str:
    text_content = getattr(item, "text_content", None)
    if isinstance(text_content, str) and text_content.strip():
        return normalize_transcript_text(text_content)

    content = getattr(item, "content", getattr(item, "text", ""))
    if isinstance(content, list):
        text_parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif hasattr(part, "text"):
                text_parts.append(str(part.text))
        return normalize_transcript_text(" ".join(text_parts))

    return normalize_transcript_text(str(content or ""))


class ChatTextOutput(voice_io.TextOutput):
    def __init__(
        self,
        room: rtc.Room,
        topic: str = LK_CHAT_TOPIC,
    ) -> None:
        super().__init__(label="ChatTextOutput", next_in_chain=None)
        self._room = room
        self._topic = topic
        self._buffer: list[str] = []
        self._flush_task: asyncio.Task[None] | None = None

    async def capture_text(self, text: str) -> None:
        if not text:
            return

        self._buffer.append(text)

    def flush(self) -> None:
        if not self._buffer:
            return

        message = "".join(self._buffer)
        self._buffer.clear()
        log.info(f"Text output flushed | chars={len(message)} | topic={self._topic}")

        async def _publish(topic: str, payload: str) -> None:
            if not self._room.isconnected():
                return
            try:
                await self._room.local_participant.publish_data(
                    payload,
                    reliable=True,
                    topic=topic,
                )
            except Exception as exc:
                log.info(f"Text output publish failed: {exc}")

        # Flush is sync; schedule async publish.
        self._flush_task = asyncio.create_task(_publish(self._topic, message))


class TriamAssistant(Agent):
    def __init__(
        self,
        document_ids: list[str],
        web_search_policy: WebSearchPermissionPolicy,
        tracer: AgentTurnTracer,
        grounding_router: GroundingRouter | None = None,
        voice_turn_state: VoiceTurnState | None = None,
        shared_policy: SharedAgentPolicy | None = None,
    ) -> None:
        books_str = ""
        if grounding_router and grounding_router.scope.books:
            books_list = []
            for b in grounding_router.scope.books:
                book_desc = f"- Sách: '{b.title}'"
                if b.author:
                    book_desc += f" của tác giả {b.author}"
                books_list.append(book_desc)
            books_str = "\n\nNgữ cảnh học tập hiện tại:\n" + "\n".join(books_list)

            # Trích xuất và nạp danh sách chương cấp 1 động từ GroundingScope để LLM làm điểm tựa sửa lỗi
            headings_list = []
            for s in grounding_router.scope.sections:
                if s.level == 1:  # Chỉ lấy tiêu đề chương chính để tránh quá tải prompt
                    headings_list.append(f"  + Chương {s.path}: {s.title}")
            if headings_list:
                books_str += "\n\nDanh sách các chương trong sách:\n" + "\n".join(headings_list)

        super().__init__(instructions=VOICE_AGENT_INSTRUCTIONS + books_str)
        self.document_ids = document_ids
        self.web_search_policy = web_search_policy
        self.tracer = tracer
        self.grounding_router = grounding_router
        self.voice_turn_state = voice_turn_state or VoiceTurnState()
        self.shared_policy = shared_policy
        self._web_search_lock = asyncio.Lock()
        self._cached_web_query: str | None = None
        self._cached_web_result: str | None = None
        self._cached_web_at: datetime | None = None

    def _voice_query_guard_config(self) -> VoiceQueryGuardConfig:
        return VoiceQueryGuardConfig(
            min_chars=settings.VOICE_AGENT_QUERY_GUARD_MIN_CHARS,
            min_tokens=settings.VOICE_AGENT_QUERY_GUARD_MIN_TOKENS,
            clarification_confirmation_max_tokens=settings.VOICE_AGENT_CLARIFICATION_CONFIRMATION_MAX_TOKENS,
            clarification_min_query_prompt_overlap=settings.VOICE_AGENT_CLARIFICATION_MIN_QUERY_PROMPT_OVERLAP,
        )

    @staticmethod
    def _extract_clarification_message(tool_result: str) -> str | None:
        if not tool_result.startswith(CLARIFICATION_MARKER):
            return None
        return tool_result.removeprefix(CLARIFICATION_MARKER).strip() or "Bạn vui lòng nói rõ câu hỏi."

    def _set_pending_clarification(
        self,
        *,
        prompt_text: str,
        reason_code: str,
        candidate_query: str | None = None,
        source: str = "query_guard",
    ) -> None:
        if not settings.VOICE_AGENT_CLARIFICATION_STATE_ENABLED:
            return
        self.voice_turn_state.set_pending_clarification(
            prompt_text=prompt_text,
            reason_code=reason_code,
            candidate_query=candidate_query,
            source=source,
        )

    def _remember_clarification_marker(
        self,
        tool_result: str,
        *,
        reason_code: str,
        candidate_query: str | None = None,
        source: str,
    ) -> bool:
        clarification = self._extract_clarification_message(tool_result)
        if clarification is None:
            return False
        self._set_pending_clarification(
            prompt_text=clarification,
            reason_code=reason_code,
            candidate_query=candidate_query,
            source=source,
        )
        return True

    @staticmethod
    def _looks_like_assistant_clarification(text: str) -> bool:
        normalized = normalize_intent_text(text)
        if len(normalized.split()) > 24:
            return False
        if "?" not in text and not any(marker in normalized for marker in ASSISTANT_CLARIFICATION_MARKERS):
            return False
        return any(marker in normalized for marker in ASSISTANT_CLARIFICATION_MARKERS)

    def _get_cached_web_result(self, query: str) -> str | None:
        if not self._cached_web_query or not self._cached_web_result or not self._cached_web_at:
            return None
        if datetime.now(timezone.utc) - self._cached_web_at > timedelta(seconds=settings.VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS):
            return None
        if normalize_intent_text(self._cached_web_query) != normalize_intent_text(query):
            return None
        return self._cached_web_result

    def _remember_web_result(self, query: str, result: str) -> None:
        self._cached_web_query = query
        self._cached_web_result = result
        self._cached_web_at = datetime.now(timezone.utc)

    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"],
    ) -> str:
        """
        Tìm kiếm kiến thức, nội dung, khái niệm trong các quyển sách thuộc Study Context hiện tại.
        PHẢI gọi tool này trước tiên cho bất kỳ câu hỏi nào liên quan đến:
        - Nội dung, chương, đoạn văn trong sách
        - Khái niệm, định nghĩa, giải thích thuật ngữ
        - Tóm tắt, phân tích nội dung sách
        - Câu hỏi kiến thức mà User đang học từ sách
        Hệ thống tự động giới hạn tìm kiếm trong tài liệu User đã chọn.
        """
        self.tracer.record_tool(AgentInputMode.VOICE, "search_book_knowledge")
        return await self.resolve_book_query(query, AgentInputMode.VOICE)

    def _remember_or_clear_voice_clarification(
        self,
        tool_result: str,
        *,
        reason_code: str,
        source: str,
    ) -> None:
        if not self._remember_clarification_marker(tool_result, reason_code=reason_code, source=source):
            self.voice_turn_state.clear_pending_clarification()

    def _current_pending_clarification(self):
        if not settings.VOICE_AGENT_CLARIFICATION_STATE_ENABLED:
            return None
        return self.voice_turn_state.recent_pending_clarification(settings.VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS)

    def _record_query_guard_result(
        self,
        input_mode: AgentInputMode,
        guard_started: float,
        guard_result: VoiceQueryGuardResult,
    ) -> None:
        self.tracer.record_latency(
            input_mode,
            "query_guard",
            int((time.perf_counter() - guard_started) * 1000),
        )
        self.tracer.record_query_guard(
            input_mode,
            reason_code=guard_result.reason_code,
            guard_mode=guard_result.guard_mode,
            overlap_ratio=guard_result.overlap_ratio,
            important_overlap_ratio=guard_result.important_overlap_ratio,
        )

    def _run_voice_query_guard_once(
        self,
        query: str,
        input_mode: AgentInputMode,
        transcript,
        *,
        pending_clarification=None,
    ) -> VoiceQueryGuardResult:
        guard_started = time.perf_counter()
        guard_result = guard_voice_book_query(
            query,
            transcript,
            config=self._voice_query_guard_config(),
            pending_clarification=pending_clarification,
        )
        self._record_query_guard_result(input_mode, guard_started, guard_result)
        return guard_result

    def _log_voice_query_guard_blocked(self, query: str, guard_result: VoiceQueryGuardResult) -> None:
        if not settings.VOICE_AGENT_QUERY_GUARD_LOG_DETAILS:
            return
        log.info(
            "Voice query guard blocked | "
            f"reason={guard_result.reason_code} | "
            f"mode={guard_result.guard_mode} | "
            f"query_chars={len(query)} | "
            f"tokens={guard_result.token_count} | "
            f"important_tokens={guard_result.important_token_count} | "
            f"overlap={guard_result.overlap_ratio} | "
            f"important_overlap={guard_result.important_overlap_ratio} | "
            f"transcript_source={guard_result.transcript_source}"
        )

    def _voice_query_guard_blocked_result(
        self,
        query: str,
        input_mode: AgentInputMode,
        guard_result: VoiceQueryGuardResult,
    ) -> str:
        self.tracer.record_answer_source(input_mode, AgentAnswerSource.CLARIFICATION)
        self._log_voice_query_guard_blocked(query, guard_result)
        if guard_result.reason_code == "permission_reply":
            return (
                "WEB_PERMISSION_REPLY_DETECTED: This user turn looks like a reply to a pending "
                "web-search permission request, not a new book question. Follow the existing "
                "web-search permission flow for the pending query."
            )

        clear_reasons = {"clarification_denied", "clarification_query_mismatch"}
        if guard_result.reason_code in clear_reasons:
            self.voice_turn_state.clear_pending_clarification()

        marker = f"{CLARIFICATION_MARKER}\n{guard_result.clarification or 'Bạn vui lòng nói rõ câu hỏi.'}"
        remember_block_reasons = {*clear_reasons, "permission_reply"}
        if guard_result.reason_code not in remember_block_reasons:
            self._remember_clarification_marker(marker, reason_code=guard_result.reason_code, source="query_guard")
        return marker

    def _voice_query_guard_block(self, query: str, input_mode: AgentInputMode) -> str | None:
        if input_mode != AgentInputMode.VOICE or not settings.VOICE_AGENT_QUERY_GUARD_ENABLED:
            return None

        transcript = self.voice_turn_state.recent_transcript(settings.VOICE_AGENT_QUERY_GUARD_TRANSCRIPT_TTL_SECONDS)
        guard_result = self._run_voice_query_guard_once(
            query,
            input_mode,
            transcript,
            pending_clarification=self._current_pending_clarification(),
        )
        if guard_result.reason_code == "valid_clarification_confirmation":
            self.voice_turn_state.clear_pending_clarification()
        if guard_result.valid:
            return None

        if guard_result.reason_code == "clarification_new_question":
            self.voice_turn_state.clear_pending_clarification()
            guard_result = self._run_voice_query_guard_once(query, input_mode, transcript)
            if guard_result.valid:
                return None

        return self._voice_query_guard_blocked_result(query, input_mode, guard_result)

    async def _resolve_shared_policy(self, query: str, input_mode: AgentInputMode) -> str | None:
        if not settings.AGENT_SHARED_POLICY_ENABLED or self.shared_policy is None:
            return None
        policy_result = await self.shared_policy.resolve(
            AgentPolicyRequest(
                query=query,
                input_mode=input_mode,
                document_ids=self.document_ids,
                allow_web_permission=self.web_search_policy.enabled,
            )
        )
        tool_result = render_voice_tool_result(policy_result)
        if input_mode == AgentInputMode.VOICE:
            self._remember_or_clear_voice_clarification(
                tool_result,
                reason_code=policy_result.reason_code,
                source="shared_policy",
            )
        return tool_result

    async def _resolve_grounding_route(self, query: str, input_mode: AgentInputMode) -> str | None:
        if self.grounding_router is None:
            return None
        grounding_result = await self.grounding_router.resolve(query, input_mode=input_mode, tracer=self.tracer)
        if grounding_result.decision.route == GroundingRoute.BOOK_RAG:
            return None

        tool_result = format_grounding_tool_result(grounding_result)
        if input_mode == AgentInputMode.VOICE:
            self._remember_or_clear_voice_clarification(
                tool_result,
                reason_code=grounding_result.decision.reason_code,
                source="grounding_router",
            )
        return tool_result

    async def _resolve_rag_context(self, query: str, input_mode: AgentInputMode) -> str:
        try:
            result = await search_voice_book_context(
                query,
                self.document_ids,
                tracer=self.tracer,
                input_mode=input_mode,
            )
            if result.found:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.BOOK_RAG)
            if input_mode == AgentInputMode.VOICE:
                self.voice_turn_state.clear_pending_clarification()
            return format_rag_context(result)
        except Exception as exc:
            self.tracer.record_error(input_mode, "book_rag_search_error")
            log.warning(f"Book RAG search failed | input_mode={input_mode.value} | document_count={len(self.document_ids)} | error_type={type(exc).__name__}")
            if input_mode == AgentInputMode.VOICE:
                self.voice_turn_state.clear_pending_clarification()
            return "BOOK_CONTEXT_ERROR: Không thể tìm kiếm dữ liệu trong sách lúc này."

    async def _resolve_book_query_inner(self, query: str, input_mode: AgentInputMode) -> str:
        guard_block = self._voice_query_guard_block(query, input_mode)
        if guard_block is not None:
            return guard_block

        policy_result = await self._resolve_shared_policy(query, input_mode)
        if policy_result is not None:
            return policy_result

        grounding_result = await self._resolve_grounding_route(query, input_mode)
        if grounding_result is not None:
            return grounding_result

        return await self._resolve_rag_context(query, input_mode)

    async def resolve_book_query(self, query: str, input_mode: AgentInputMode) -> str:
        tool_started = time.perf_counter()
        try:
            return await self._resolve_book_query_inner(query, input_mode)
        finally:
            self.tracer.record_latency(input_mode, "tool_total", int((time.perf_counter() - tool_started) * 1000))

    @function_tool
    async def execute_web_search(
        self,
        query: Annotated[str, "Nội dung cần tìm kiếm trên internet"],
    ) -> str:
        """
        [VOICE - Pha 2] Chỉ gọi tool này SAU KHI user đã xác nhận đồng ý ở turn hội thoại trước.
        THỰC HIỆN tìm kiếm thực sự trên internet và trả về kết quả.
        TRAO ĐỔI VUI: Nếu chưa có turn hỏi xin phép trước → không gọi tool này.
        """
        return await self._execute_web_search_for_mode(query, AgentInputMode.VOICE)

    async def _execute_web_search_for_mode(self, query: str, input_mode: AgentInputMode) -> str:
        self.tracer.record_tool(input_mode, "execute_web_search")
        async with self._web_search_lock:
            cached_result = self._get_cached_web_result(query)
            if cached_result is not None:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.WEB)
                log.info(f"Voice web search cached result reused | query_chars={len(query)}")
                return cached_result

            allowed, reason = await self.web_search_policy.resolve_before_web_search(query)
            if not allowed:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.POLICY)
                log.info(f"Voice web search blocked | reason={reason}")
                return reason

            log.info(f"Voice web search executing | query_chars={len(query)}")
            started = time.perf_counter()
            try:
                result = await web_search(query)
                self._remember_web_result(query, result)
                log.info(f"Voice web search completed | query_chars={len(query)} | result_chars={len(result or '')}")
                self.tracer.record_latency(input_mode, "web_search", int((time.perf_counter() - started) * 1000))
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.WEB)
                return result
            except Exception:
                self.tracer.record_latency(input_mode, "web_search", int((time.perf_counter() - started) * 1000))
                self.tracer.record_error(input_mode, "web_search_error")
                raise
            finally:
                self.web_search_policy.mark_search_consumed()

    @function_tool
    async def ask_web_search_permission(
        self,
        query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"],
    ) -> str:
        """
        [VOICE - Pha 1] Gọi tool này khi search_book_knowledge không có đủ thông tin liên quan.
        Tool này KHÔNG tìm web ngay. Nó chỉ trả về mẫu câu hỏi xác nhận để AI đọc lên cho user nghe.
        Sau khi AI đọc câu hỏi này, AI kết thúc turn và đợi user trả lời ở turn tiếp theo.
        Nếu user đồng ý (bất kỳ cách nào) → AI tự quyết định gọi 'execute_web_search'.
        Nếu user từ chối → AI không gọi tool và trả lời phù hợp.
        """
        self.tracer.record_tool(AgentInputMode.VOICE, "ask_web_search_permission")
        self.tracer.record_answer_source(AgentInputMode.VOICE, AgentAnswerSource.POLICY)
        log.info(f"Voice web search permission requested | query_chars={len(query)}")
        return self.web_search_policy.request_permission(query)


def _tool_reply_watchdog_config() -> VoiceToolReplyWatchdogConfig:
    return VoiceToolReplyWatchdogConfig(
        enabled=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED,
        grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS,
        thinking_grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS,
        monitored_tools={item.strip() for item in settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_TOOLS.split(",") if item.strip()},
        allow_error_outputs=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS,
        force_tool_choice_none=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE,
    )


async def entrypoint(ctx: JobContext):  # noqa: C901
    await ctx.connect()

    job_meta = _parse_job_metadata(ctx.job.metadata, ctx.room.name)
    thread_id = job_meta.thread_id
    document_ids = job_meta.document_ids

    if not document_ids:
        if ctx.room.name == "console":
            log.warning("Voice console started without VOICE_AGENT_CONSOLE_BOOK_ID; limited STT-only run. Full local console testing requires a book ID.")
        else:
            log.info("No document_ids found in LiveKit metadata; closing voice job.")
            return

    if ctx.room.name == "console" and not thread_id:
        log.warning("Voice console started without VOICE_AGENT_CONSOLE_THREAD_ID; chat persistence is disabled for this run.")

    log.info(f"Voice session scope ready | document_count={len(document_ids)} | room={ctx.room.name}")
    log.info(f"Bat dau phien doc sach cho Thread ID: {thread_id}")

    thread_uuid: uuid.UUID | None = None
    if thread_id:
        try:
            thread_uuid = uuid.UUID(thread_id)
        except ValueError:
            log.info(f"Invalid thread_id UUID; skipping DB persistence: {thread_id}")
            thread_uuid = None

    def _is_model_not_found(exc: Exception) -> bool:
        msg = str(exc)
        return "NOT_FOUND" in msg or "404" in msg or "model" in msg.lower() and "not" in msg.lower() and "found" in msg.lower()

    model_candidates = [settings.OPENAI_STREAM_MODEL_NAME, "gpt-realtime-1.5"]
    # de-dupe while preserving order
    seen_models: set[str] = set()
    model_candidates = [m for m in model_candidates if not (m in seen_models or seen_models.add(m))]
    log.info(
        "Agent model profile active | "
        f"profile={settings.AGENT_MODEL_PROFILE} | "
        f"text_model={settings.VOICE_AGENT_TEXT_LLM_MODEL} | "
        f"realtime_model={settings.OPENAI_STREAM_MODEL_NAME} | "
        f"transcription_model={settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL} | "
        f"classifier_model={settings.VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL}"
    )

    web_search_policy = WebSearchPermissionPolicy(
        enabled=settings.VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT,
        grant_ttl_seconds=settings.VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS,
        implicit_grant_window_seconds=settings.VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS,
    )
    tracer = AgentTurnTracer(
        enabled=settings.AGENT_TRACE_ENABLED,
        thread_id=str(thread_uuid) if thread_uuid else None,
        room_name=ctx.room.name,
        score_precision=settings.AGENT_TRACE_SCORE_PRECISION,
        late_transcript_window_seconds=settings.AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS,
    )

    grounding_scope = None
    grounding_router: GroundingRouter | None = None
    if settings.AGENT_GROUNDING_ROUTER_ENABLED:
        try:
            grounding_started = time.perf_counter()
            grounding_scope = await asyncio.to_thread(load_grounding_scope, document_ids)

            async def _load_section_texts(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
                return await asyncio.to_thread(
                    load_scoped_section_texts,
                    book_id,
                    section_ids,
                    grounding_scope.allowed_book_ids,
                )

            grounding_router = GroundingRouter(
                grounding_scope,
                _load_section_texts,
                section_context_max_chars=settings.AGENT_SECTION_CONTEXT_MAX_CHARS,
            )
            log.info(f"Grounding router ready | books={len(grounding_scope.books)} | sections={len(grounding_scope.sections)} | load_ms={int((time.perf_counter() - grounding_started) * 1000)}")

            # Pre-warm local embedding classifiers in the background
            from app.services.voice_agent.web_permission_intent_classifier import _initialize_permission_prototypes_async
            asyncio.create_task(_initialize_permission_prototypes_async())
        except Exception:
            log.exception("Failed to initialize grounding router")
            grounding_scope = None
            grounding_router = None

    voice_turn_state = VoiceTurnState()
    shared_policy = SharedAgentPolicy(
        document_ids=document_ids,
        grounding_router=grounding_router,
        tracer=tracer,
    )
    agent_instance = TriamAssistant(
        document_ids=document_ids,
        web_search_policy=web_search_policy,
        tracer=tracer,
        grounding_router=grounding_router,
        voice_turn_state=voice_turn_state,
        shared_policy=shared_policy,
    )
    chat_llm = OpenAILLM(model=settings.VOICE_AGENT_TEXT_LLM_MODEL, temperature=0.7)
    transcript_store = VoiceTranscriptStore(
        room=ctx.room,
        thread_id=thread_uuid,
        dedupe_window_seconds=settings.VOICE_AGENT_DEDUPE_WINDOW_SECONDS,
    )

    session: AgentSession
    text_turn_lock = asyncio.Lock()

    def _truncate_session_history() -> None:
        if hasattr(session, "history") and session.history is not None:
            session.history.truncate(max_items=settings.VOICE_AGENT_HISTORY_LIMIT)

    def _record_web_permission_reply(text: str) -> None:
        web_search_policy.record_user_reply(text)

    async def _observe_web_permission_reply(text: str):
        decision = await web_search_policy.observe_user_reply(text)
        if decision.granted_query:
            log.info(f"Web search permission granted | query_chars={len(decision.granted_query)}")
        elif decision.denied:
            log.info("Web search permission denied")
        elif decision.unclear:
            log.info("Web search permission unclear")
        elif decision.new_question:
            log.info("Web search permission cleared because user asked a new question")
        return decision

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent

    async def _chat_naive_rag(user_text: str) -> str:
        """Chế độ RAG Naive (toggle TẮT): luôn search sách, không dùng tool web."""
        log.info("[Text Chat] Chế độ Naive RAG (web search TẮT)")
        tracer.record_tool(AgentInputMode.TEXT, "search_book_knowledge_text")
        rag_result = await search_voice_book_context(
            user_text,
            document_ids,
            tracer=tracer,
            input_mode=AgentInputMode.TEXT,
        )
        temp_ctx = session.history.copy()
        if rag_result.found:
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.BOOK_RAG)
            temp_ctx.add_message(
                role="system",
                content=f"Thông tin trích xuất từ sách (dùng để trả lời):\n{format_rag_context(rag_result)}",
            )
        else:
            temp_ctx.add_message(
                role="system",
                content=("Không tìm thấy thông tin phù hợp trong sách cho câu hỏi này. Hãy nói ngắn gọn rằng nội dung hiện không có trong sách, không tự bịa thông tin ngoài sách."),
            )
        response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
        return response.text

    async def _chat_from_grounding_result(result: GroundingResult, user_text: str) -> str:
        route = result.decision.route
        if route == GroundingRoute.BOOK_METADATA:
            return result.deterministic_answer or "Tôi chưa có thông tin metadata phù hợp."
        if route == GroundingRoute.CLARIFICATION:
            return result.decision.clarification or "Bạn vui lòng nói rõ câu hỏi."
        if route == GroundingRoute.BOOK_SECTION:
            if result.deterministic_answer:
                return result.deterministic_answer
            temp_ctx = session.history.copy()
            temp_ctx.add_message(
                role="system",
                content=SECTION_TEXT_ANSWER_INSTRUCTIONS.format(section_context=result.section_context or ""),
            )
            response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
            return response.text
        if route == GroundingRoute.WEB_POLICY:
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
            if web_search_policy.enabled:
                return web_search_policy.request_permission(user_text)
            return "Câu hỏi này cần thông tin ngoài sách, nhưng tìm kiếm internet hiện đang tắt."
        raise ValueError(f"Unsupported direct grounding route: {route}")

    async def _try_chat_grounding_route(user_text: str) -> tuple[bool, str]:
        if grounding_router is None:
            return False, ""
        result = await grounding_router.resolve(
            user_text,
            input_mode=AgentInputMode.TEXT,
            tracer=tracer,
        )
        if result.decision.route == GroundingRoute.BOOK_RAG:
            return False, ""
        return True, await _chat_from_grounding_result(result, user_text)

    async def _chat_with_shared_policy(user_text: str) -> str:
        log.info("[Text Chat] Shared agent policy")
        policy_result = await shared_policy.resolve(
            AgentPolicyRequest(
                query=user_text,
                input_mode=AgentInputMode.TEXT,
                document_ids=document_ids,
                allow_web_permission=web_search_policy.enabled,
            )
        )

        if policy_result.action in {
            AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT,
            AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT,
        }:
            temp_ctx = session.history.copy()
            temp_ctx.add_message(
                role="system",
                content=policy_result.llm_system_context or "",
            )
            response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
            return response.text

        if policy_result.action == AgentPolicyAction.ASK_WEB_PERMISSION:
            tracer.record_tool(AgentInputMode.TEXT, "ask_web_search_permission_text")
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
            return web_search_policy.request_permission(user_text) if web_search_policy.enabled else render_text_direct_message(policy_result)

        return render_text_direct_message(policy_result)

    async def _chat_with_agentic_loop(user_text: str) -> str:
        """
        Chế độ Agentic (toggle BẬT): gpt-4o-mini tự quyết định dùng tool nào.
        Dùng LLMStream.collect() + llm.execute_function_call() theo chuẩn SDK.
        LLM tự phán xét RAG có đủ không, nếu không tự gọi search_web.
        """
        log.info("[Text Chat] Chế độ Agentic Loop (web search BẬT)")

        # Tạo standalone async functions để tránh trực tiếp dùng agent_instance.tools.
        # ToolContext.__init__ nội bộ gọi find_function_tools(self) → crash khi agent
        # chưa có activity context. Ta wrap thủ công bằng @function_tool decorator.
        async def search_book_knowledge_text(query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"]) -> str:
            """Tìm kiếm kiến thức trong sách thuộc Study Context hiện tại."""
            tracer.record_tool(AgentInputMode.TEXT, "search_book_knowledge_text")
            if settings.AGENT_SHARED_POLICY_ENABLED:
                policy_result = await shared_policy.resolve(
                    AgentPolicyRequest(
                        query=query,
                        input_mode=AgentInputMode.TEXT,
                        document_ids=document_ids,
                        allow_web_permission=web_search_policy.enabled,
                    )
                )
                return render_voice_tool_result(policy_result)
            return await agent_instance.resolve_book_query(query, AgentInputMode.TEXT)

        async def ask_web_search_permission_text(query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"]) -> str:
            """Xin phép user trước khi tìm kiếm internet."""
            tracer.record_tool(AgentInputMode.TEXT, "ask_web_search_permission_text")
            tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
            return web_search_policy.request_permission(query)

        async def execute_web_search_text(query: Annotated[str, "Nội dung cần tìm kiếm trên internet"]) -> str:
            """Tìm kiếm thông tin trên internet sau khi user đã đồng ý."""
            return await agent_instance._execute_web_search_for_mode(query, AgentInputMode.TEXT)

        book_fn_tool = function_tool(search_book_knowledge_text)
        ask_web_permission_tool = function_tool(ask_web_search_permission_text)
        web_fn_tool = function_tool(execute_web_search_text)
        standalone_tools = [book_fn_tool, ask_web_permission_tool, web_fn_tool]

        # Tạo ToolContext thủ công để tránh gọi __init__ (nó gọi find_function_tools(self))
        tool_ctx = agents_llm.ToolContext.__new__(agents_llm.ToolContext)
        tool_ctx._tools = standalone_tools
        tool_ctx._fnc_tools_map = {t.info.name: t for t in standalone_tools}
        tool_ctx._provider_tools = []
        tool_ctx._tool_sets = []

        ctx_copy = session.history.copy()
        # Inject ngày giờ thực từ server và quy tắc dùng tool.
        # Lý do inject datetime: Tavily có thể trả về trang cũ được cache → ngày sai.
        # Ngày/giờ là fact của server, không cần web search.
        now_str = datetime.now(timezone.utc).astimezone().strftime("%A, %d/%m/%Y %H:%M (UTC+7)")
        ctx_copy.add_message(
            role="system",
            content=TEXT_AGENTIC_SYSTEM_INSTRUCTIONS.format(now_str=now_str),
        )

        MAX_STEPS = 4  # Giới hạn vòng lặp tool call, tránh loop vô tận
        for step in range(MAX_STEPS):
            response = await chat_llm.chat(
                chat_ctx=ctx_copy,
                tools=standalone_tools,
            ).collect()

            # Nếu không có tool call → LLM đã có câu trả lời cuối
            if not response.tool_calls:
                log.info(f"[Agentic] Hoàn thành sau {step + 1} bước. Reply: {len(response.text)} chars")
                return response.text

            # Thực thi tool calls theo đúng chuẩn SDK
            log.info(f"[Agentic] Bước {step + 1}: thực thi {len(response.tool_calls)} tool call(s)")
            for tc in response.tool_calls:
                tracer.record_tool(AgentInputMode.TEXT, str(getattr(tc, "name", "unknown_tool")))
                result = await agents_llm.execute_function_call(tc, tool_ctx)
                ctx_copy.insert(result.fnc_call)
                if result.fnc_call_out:
                    ctx_copy.insert(result.fnc_call_out)

        # Hết MAX_STEPS, trả về text của lần gọi cuối cùng
        log.warning("[Agentic] Đạt giới hạn MAX_STEPS, trả về text hiện tại")
        return response.text

    async def _chat_with_granted_web_search(query: str) -> str:
        log.info(f"[Text Chat] Web search granted by user | query_chars={len(query)}")
        web_result = await agent_instance._execute_web_search_for_mode(query, AgentInputMode.TEXT)
        temp_ctx = session.history.copy()
        temp_ctx.add_message(
            role="system",
            content=WEB_GRANTED_REPLY_INSTRUCTIONS.format(query=query, web_result=web_result),
        )
        response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
        return response.text

    async def _publish_assistant_reply(full_reply: str) -> None:
        full_reply = full_reply.strip()
        if not full_reply:
            return

        await transcript_store.save_and_publish_assistant(full_reply)
        try:
            await ctx.room.local_participant.publish_data(
                full_reply.encode("utf-8"),
                reliable=True,
                topic=LK_CHAT_TOPIC,
            )
        except Exception as exc:
            log.info(f"Data output publish failed: {exc}")

        session.history.add_message(role="assistant", content=full_reply)
        _truncate_session_history()

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        normalized_text = normalize_transcript_text(text)
        if not normalized_text:
            return

        async with text_turn_lock:
            tracer.begin_turn(AgentInputMode.TEXT)
            tracer.record_transcript(
                AgentInputMode.TEXT,
                char_count=len(normalized_text),
                language="text",
            )
            log.info(f"Data input received | participant={participant_id or 'unknown'} | chars={len(normalized_text)} | thread_id={thread_uuid}")
            if settings.VOICE_AGENT_LOG_TRANSCRIPT_TEXT:
                log.debug(f"Data input preview: {trim_text(normalized_text, 160)}")

            # Save DB and update transcript immediately (await to guarantee insertion order)
            await transcript_store.save_and_publish_user(normalized_text)
            permission_decision = await _observe_web_permission_reply(normalized_text)

            # Interrupt if livekit is currently speaking
            await session.interrupt()

            # Put input into shared memory
            session.history.add_message(role="user", content=normalized_text)
            _truncate_session_history()

            try:
                if permission_decision.granted_query:
                    full_reply = await _chat_with_granted_web_search(permission_decision.granted_query)
                elif permission_decision.denied:
                    tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.POLICY)
                    full_reply = "Được, tôi sẽ không tìm trên internet. Mình tiếp tục trao đổi dựa trên nội dung sách nhé."
                elif permission_decision.unclear:
                    tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.CLARIFICATION)
                    full_reply = "Tôi chưa rõ ý ông. Bạn muốn tôi tìm thêm trên internet cho câu vừa rồi không?"
                else:
                    started = time.perf_counter()
                    if settings.AGENT_SHARED_POLICY_ENABLED:
                        full_reply = await _chat_with_shared_policy(normalized_text)
                    else:
                        handled_by_grounding, full_reply = await _try_chat_grounding_route(normalized_text)
                        if not handled_by_grounding:
                            full_reply = await _chat_with_agentic_loop(normalized_text) if web_search_policy.enabled else await _chat_naive_rag(normalized_text)
                    tracer.record_latency(AgentInputMode.TEXT, "answer_pipeline", int((time.perf_counter() - started) * 1000))

                full_reply = full_reply.strip()
                log.info(f"LLM Reply completed. Length: {len(full_reply)}")

                if full_reply:
                    await _publish_assistant_reply(full_reply)
                    tracer.record_assistant(AgentInputMode.TEXT, char_count=len(full_reply))
                tracer.complete_turn(AgentInputMode.TEXT)
            except Exception as e:
                tracer.record_error(AgentInputMode.TEXT, type(e).__name__)
                tracer.complete_turn(AgentInputMode.TEXT, error_code=type(e).__name__)
                log.error(f"Error in handle_data_input: {e}")

    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input received | participant={participant_id} | chars={len(ev.text or '')}")
        # call handle_data_input to process the text input
        await handle_data_input(ev.text, participant_id)

    def on_data_received(packet: rtc.DataPacket) -> None:
        try:
            raw = packet.data.decode("utf-8")
        except Exception as exc:
            log.info(f"Data input decode failed: {exc}")
            return

        # --- Kênh điều khiển: bật/tắt web search ---
        if packet.topic == LK_CONTROL_TOPIC:
            try:
                payload = json.loads(raw)
                if payload.get("type") == "toggle_web_search":
                    web_search_policy.set_enabled(bool(payload.get("enabled", False)))
                    if payload.get("allowed"):
                        web_search_policy.pre_grant_for_eval()
                    else:
                        web_search_policy.clear()
                    log.info(f"Web search toggle: {'BẬT' if web_search_policy.enabled else 'TẮT'} | allowed={payload.get('allowed')}")
            except json.JSONDecodeError:
                log.info("lk.control: payload không phải JSON hợp lệ")
            return

        # --- Kênh chat thông thường ---
        if packet.topic == LK_CHAT_TOPIC:
            participant_id = packet.participant.identity if packet.participant else None
            asyncio.create_task(handle_data_input(raw, participant_id))

    ctx.room.on("data_received", on_data_received)

    session: AgentSession | None = None
    empty_room_cleanup_task: asyncio.Task[None] | None = None

    def _remote_participant_identities(exclude_identity: str | None = None) -> list[str]:
        return [participant.identity for participant in ctx.room.remote_participants.values() if participant.identity != exclude_identity]

    async def _close_empty_room_after_grace() -> None:
        try:
            await asyncio.sleep(settings.LIVEKIT_AGENT_EMPTY_ROOM_GRACE_SECONDS)
            remaining = _remote_participant_identities()
            if remaining:
                log.info(f"Empty-room cleanup skipped | remaining_remote_participants={len(remaining)}")
                return

            log.info("No remote participants after grace period. Closing agent session and room.")
            if session is not None:
                await session.aclose()
            if ctx.room.isconnected():
                await ctx.room.disconnect()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            log.warning(f"Empty-room cleanup failed | error_type={type(exc).__name__}")

    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        nonlocal empty_room_cleanup_task
        if empty_room_cleanup_task and not empty_room_cleanup_task.done():
            empty_room_cleanup_task.cancel()
            log.info(f"Empty-room cleanup cancelled | participant={participant.identity}")

    @ctx.room.on("participant_disconnected")
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        nonlocal empty_room_cleanup_task
        log.info(f"Participant disconnected: {participant.identity}")
        active_remotes = _remote_participant_identities(exclude_identity=participant.identity)
        log.info(f"Active remote participants remaining: {len(active_remotes)}")
        if active_remotes:
            return
        if empty_room_cleanup_task and not empty_room_cleanup_task.done():
            return
        log.info(f"No remote participants left. Scheduling agent cleanup after {settings.LIVEKIT_AGENT_EMPTY_ROOM_GRACE_SECONDS}s grace period.")
        empty_room_cleanup_task = asyncio.create_task(_close_empty_room_after_grace())

    async def _cancel_empty_room_cleanup() -> None:
        if empty_room_cleanup_task and not empty_room_cleanup_task.done():
            empty_room_cleanup_task.cancel()
            try:
                await empty_room_cleanup_task
            except asyncio.CancelledError:
                pass

    ctx.add_shutdown_callback(_cancel_empty_room_cleanup)

    def _handle_user_input_transcribed(ev: Any) -> None:
        is_final = bool(getattr(ev, "is_final", False))
        transcript = str(getattr(ev, "transcript", "") or "").strip()
        language = getattr(ev, "language", None)
        log.info(f"user_input_transcribed received | final={is_final} | chars={len(transcript)} | thread_id={thread_uuid}")
        if settings.VOICE_AGENT_LOG_TRANSCRIPT_TEXT and transcript:
            log.debug(f"user_input_transcribed preview: {trim_text(transcript, 160)}")
        if is_final and transcript:
            voice_turn_state.record_final_transcript(
                transcript,
                str(language) if language else None,
            )
            tracer.record_transcript(
                AgentInputMode.VOICE,
                char_count=len(transcript),
                language=str(language) if language else None,
            )
            _record_web_permission_reply(transcript)

    def _handle_conversation_item_added(ev: ConversationItemAddedEvent) -> None:
        item = ev.item
        if not isinstance(item, LLMMessage):
            return

        text = _extract_conversation_item_text(item)
        if not text:
            return

        if item.role == "user":
            tracer.ensure_turn(AgentInputMode.VOICE)
            log.info(f"User voice speech saved | text='{text}' | thread_id={thread_uuid}")
            voice_turn_state.record_committed_user_text(text)
            _record_web_permission_reply(text)
            asyncio.create_task(transcript_store.save_and_publish_user(text))
        elif item.role == "assistant":
            tracer.record_assistant(AgentInputMode.VOICE, char_count=len(text))
            tracer.complete_turn(AgentInputMode.VOICE)
            log.info(f"Assistant voice speech saved | text='{text}' | thread_id={thread_uuid}")
            asyncio.create_task(transcript_store.save_and_publish_assistant(text))
            if settings.VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED and agent_instance._looks_like_assistant_clarification(text):
                voice_turn_state.set_pending_clarification(
                    prompt_text=text,
                    reason_code="assistant_confirmation",
                    source="assistant_message",
                )

    def _handle_function_tools_executed(
        ev: FunctionToolsExecutedEvent,
        watchdog: VoiceToolReplyWatchdog,
    ) -> None:
        if tracer.has_active_turn(AgentInputMode.VOICE):
            for function_call in ev.function_calls:
                tracer.record_tool(
                    AgentInputMode.VOICE,
                    str(getattr(function_call, "name", "unknown_tool")),
                )
        watchdog.schedule_after_tools_executed(ev)

    def _attach_session_handlers(sess: AgentSession, watchdog: VoiceToolReplyWatchdog) -> None:
        @sess.on("user_input_transcribed")  # type: ignore[arg-type]
        def on_user_input_transcribed(ev):
            watchdog.record_user_transcribed()
            _handle_user_input_transcribed(ev)

        @sess.on("conversation_item_added")  # type: ignore[arg-type]
        def on_conversation_item_added(ev: ConversationItemAddedEvent):
            _handle_conversation_item_added(ev)

        @sess.on("function_tools_executed")  # type: ignore[arg-type]
        def on_function_tools_executed(ev: FunctionToolsExecutedEvent):
            _handle_function_tools_executed(ev, watchdog)

        @sess.on("speech_created")  # type: ignore[arg-type]
        def on_speech_created(ev: SpeechCreatedEvent):
            watchdog.record_speech_created(source=str(getattr(ev, "source", "")))

        @sess.on("agent_state_changed")  # type: ignore[arg-type]
        def on_agent_state_changed(ev: AgentStateChangedEvent):
            watchdog.record_agent_state_changed(new_state=str(getattr(ev, "new_state", "")))

        @sess.on("user_state_changed")  # type: ignore[arg-type]
        def on_user_state_changed(ev: UserStateChangedEvent):
            watchdog.record_user_state_changed(new_state=str(getattr(ev, "new_state", "")))

        @sess.on("close")  # type: ignore[arg-type]
        def on_close(_ev):
            watchdog.close()

    transcription_prompt_result = build_realtime_transcription_prompt(
        base_prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
        grounding_scope=grounding_scope,
        enabled=settings.OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED,
        max_chars=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS,
        max_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS,
        max_section_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS,
    )

    log.info(
        "Realtime transcription prompt ready | "
        f"dynamic={transcription_prompt_result.dynamic_enabled} | "
        f"terms={transcription_prompt_result.term_count} | "
        f"chars={transcription_prompt_result.prompt_chars}"
    )

    # Start session with fallback when a configured model is unavailable.
    last_start_exc: Exception | None = None
    for model_name in model_candidates:
        try:
            log.info(f"Starting realtime session with model: {model_name}, voice: {settings.OPENAI_REALTIME_VOICE}")
            model = RealtimeModel(
                model=model_name,
                voice=settings.OPENAI_REALTIME_VOICE,
                modalities=["audio"],
                input_audio_transcription=AudioTranscription(
                    model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
                    language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
                    prompt=transcription_prompt_result.prompt,
                ),
                input_audio_noise_reduction=settings.OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION,
            )
            session = AgentSession(
                llm=model,
                turn_handling={
                    "interruption": {
                        "enabled": True,
                        "min_duration": settings.VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS,
                        "min_words": settings.VOICE_AGENT_INTERRUPTION_MIN_WORDS,
                        "resume_false_interruption": True,
                        "false_interruption_timeout": settings.VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS,
                        "discard_audio_if_uninterruptible": True,
                    },
                    "preemptive_generation": {
                        "enabled": settings.VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED,
                    },
                },
            )
            tool_reply_watchdog = VoiceToolReplyWatchdog(
                session=session,
                tracer=tracer,
                config=_tool_reply_watchdog_config(),
            )
            _attach_session_handlers(session, tool_reply_watchdog)

            await session.start(
                room=ctx.room,
                agent=agent_instance,
                room_options=room_io.RoomOptions(
                    audio_input=room_io.AudioInputOptions(
                        noise_cancellation=lambda _: noise_cancellation.BVC(),
                    ),
                    text_input=room_io.TextInputOptions(  # type: ignore[call-arg]
                        text_input_cb=handle_text_input
                    ),
                    text_output=room_io.TextOutputOptions(
                        sync_transcription=False,
                        next_in_chain=ChatTextOutput(
                            ctx.room,
                            topic=LK_CHAT_TOPIC,
                        ),
                    ),
                    close_on_disconnect=True,
                    delete_room_on_close=True,
                ),
            )

            break
        except Exception as exc:
            last_start_exc = exc
            if _is_model_not_found(exc) and model_name != model_candidates[-1]:
                log.info(f"Realtime model not available ({model_name}); trying fallback")
                continue
            raise

    if last_start_exc is not None and not ctx.room.isconnected():
        # Defensive: in case we failed before connecting properly.
        raise last_start_exc

    try:
        history_msgs = await transcript_store.load_recent_history(settings.VOICE_AGENT_HISTORY_LIMIT)
        # type: ignore[attr-defined]
        if hasattr(session, "history") and session.history is not None:
            for msg in history_msgs:
                # type: ignore[attr-defined]
                session.history.add_message(role="user" if msg.is_user else "assistant", content=msg.text)
            _truncate_session_history()
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")

    await session.generate_reply(
        instructions=GREETING_INSTRUCTIONS,
    )


if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=_calculate_agent_load,
            load_threshold=settings.LIVEKIT_AGENT_LOAD_THRESHOLD,
            job_executor_type=_get_job_executor_type(),
            num_idle_processes=settings.LIVEKIT_AGENT_NUM_IDLE_PROCESSES,
            initialize_process_timeout=settings.LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT,
            shutdown_process_timeout=settings.LIVEKIT_AGENT_SHUTDOWN_PROCESS_TIMEOUT,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )

```

### app\services\async_limiter.py

```py
import asyncio
import threading
import weakref

_limiters_by_loop: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, dict[str, asyncio.Semaphore]] = weakref.WeakKeyDictionary()
_limiters_lock = threading.Lock()


def get_loop_semaphore(name: str, limit: int) -> asyncio.Semaphore:
    """Return a semaphore scoped to the current event loop.

    Celery runs each async book job through ``asyncio.run()``, which creates a
    fresh event loop per task. A module-level asyncio.Semaphore can become bound
    to the first loop and fail on later tasks, so limiters must be loop-local.
    """
    loop = asyncio.get_running_loop()
    with _limiters_lock:
        loop_limiters = _limiters_by_loop.setdefault(loop, {})
        semaphore = loop_limiters.get(name)
        if semaphore is None:
            semaphore = asyncio.Semaphore(max(1, limit))
            loop_limiters[name] = semaphore
        return semaphore

```

### app\services\audiobook_service.py

```py
import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.constant import BookStatus, PlanMode, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import BookNotFoundError, BookStatusConflictError, ExternalServiceError, NoReadingPlanError, ReadingPlanNotFoundError, ReadingPlanScheduleConflictError
from app.models.db_models import Book, LearningUnit, LearningUnitSegment, ProcessingJob, ReadingPlan, ReadingPlanScheduleSlot, BookLearningState, ReadingPlanSession, SpacedReviewItem
from app.repositories import audiobook_repo
from app.repositories.book_read_repo import BookListProjection, get_book_library_projection, list_book_library_projections
from app.repositories.book_section_repo import BookSectionOutlineRow, list_book_section_outline_rows, list_book_sections
from app.repositories.learning_unit_repo import (
    count_unit_segments_by_book_and_mode,
    create_learning_units,
    list_learning_units,
    list_unit_segments,
)
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
from app.repositories.reading_plan_repo import get_current_plan_for_owned_book
from app.repositories.reading_plan_schedule_repo import list_active_slots, list_slots_for_plan, replace_slots_for_plan, set_slots_active
from app.repositories.learning_progress_repo import delete_book_progress
from app.repositories.book_learning_state_repo import reset_book_learning_state
from app.repositories.reading_plan_session_repo import delete_sessions_for_plan
from app.repositories.spaced_review_repo import delete_spaced_review_items
from app.repositories.notification_outbox_repo import delete_pending_outbox_by_keys
from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest
from app.services.learning_progress_service import build_book_learning_summary_from_state
from app.services.learning_unit_planner_service import plan_learning_units_async
from app.services.reading_plan_schedule_service import WEEKDAY_LABELS, WEEKDAY_SHORT_LABELS, build_slots_for_plan, validate_plan_schedule_for_activation, validate_plan_schedule_shape
from app.services.reading_plan_session_service import (
    build_plan_session_summary,
    cancel_future_sessions_for_plan,
    ensure_future_sessions_for_plan,
    mark_due_sessions_missed,
    sync_existing_session_units_from_progress,
)
from app.tasks.book_tasks import switch_mode_task


def _book_to_response_dict(projection: BookListProjection, modes_map: dict[uuid.UUID, set[str]] | None = None) -> dict:
    book = projection.book
    book_data = book.model_dump()
    learning_status = None
    book_progress_percent = None
    completed_at = None
    if projection.learning_state:
        learning_status = projection.learning_state.status
        book_progress_percent = projection.learning_state.book_progress_percent
        completed_at = projection.learning_state.completed_at

    book_modes = (modes_map or {}).get(book.id, set())
    return {
        **book_data,
        "learning_status": learning_status,
        "book_progress_percent": book_progress_percent,
        "completed_at": completed_at,
        "has_full_mode": "full" in book_modes,
        "has_pareto_mode": "pareto" in book_modes,
    }


def list_books(session: Session, user_id: uuid.UUID) -> list[dict]:
    projections = list_book_library_projections(session, user_id=user_id)
    book_ids = [p.book.id for p in projections]
    modes_map = {}
    if book_ids:
        rows = session.exec(select(LearningUnit.book_id, LearningUnit.mode).where(LearningUnit.book_id.in_(book_ids)).group_by(LearningUnit.book_id, LearningUnit.mode)).all()
        for b_id, mode in rows:
            modes_map.setdefault(b_id, set()).add(mode.value)
    return [_book_to_response_dict(p, modes_map) for p in projections]


def get_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    projection = get_book_library_projection(session, user_id=user_id, book_id=book_id)
    if not projection:
        raise BookNotFoundError()
    rows = session.exec(select(LearningUnit.mode).where(LearningUnit.book_id == book_id).group_by(LearningUnit.mode)).all()
    book_modes = {mode.value for mode in rows}
    return _book_to_response_dict(projection, {book_id: book_modes})


def list_shared_library(session: Session) -> list[dict]:
    """
    Lấy danh sách sách mẫu được chia sẻ công khai kèm thông tin các chế độ học đã bóc tách xong.
    """
    books = session.exec(select(Book).where(Book.is_shared == True, Book.status == "ready")).all()

    book_ids = [b.id for b in books]
    modes_map = {}
    if book_ids:
        rows = session.exec(select(LearningUnit.book_id, LearningUnit.mode).where(LearningUnit.book_id.in_(book_ids)).group_by(LearningUnit.book_id, LearningUnit.mode)).all()
        for b_id, mode in rows:
            modes_map.setdefault(b_id, set()).add(mode.value)

    items = []
    for b in books:
        book_modes = modes_map.get(b.id, set())
        items.append(
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "total_sections": b.total_sections,
                "total_units": b.total_units,
                "status": b.status,
                "learning_status": None,
                "book_progress_percent": 0,
                "completed_at": None,
                "document_type": b.document_type,
                "file_url": b.file_url,
                "is_shared": b.is_shared,
                "parent_shared_id": b.parent_shared_id,
                "has_full_mode": "full" in book_modes,
                "has_pareto_mode": "pareto" in book_modes,
                "created_at": b.created_at,
                "updated_at": b.updated_at,
            }
        )
    return items


def create_new_book(session: Session, user_id: uuid.UUID, payload: BookCreateRequest) -> Book:
    book = Book(
        user_id=user_id,
        title=payload.title,
        author=payload.author,
    )
    return audiobook_repo.create_book(session, book)


def update_book_by_id(session: Session, book_data: BookUpdateRequest, book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    return audiobook_repo.update_book_by_id(session, book_data, book_id, user_id)


async def delete_book_and_assets(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> None:
    await audiobook_repo.delete_book_storage(session, book_id, user_id)


def _active_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> ReadingPlan:
    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
    if not plan:
        raise NoReadingPlanError()
    return plan


def _slot_to_dict(slot: ReadingPlanScheduleSlot) -> dict:
    return {
        "id": slot.id,
        "weekday": slot.weekday,
        "weekday_label": WEEKDAY_LABELS.get(slot.weekday, str(slot.weekday)),
        "reminder_time": slot.reminder_time,
        "timezone": slot.timezone,
        "is_active": slot.is_active,
    }


def _user_slot_to_dict(slot: ReadingPlanScheduleSlot) -> dict:
    return {
        **_slot_to_dict(slot),
        "plan_id": slot.plan_id,
        "book_id": slot.book_id,
    }


def _slots_to_schedule_config(slots: list[ReadingPlanScheduleSlot]) -> list[str]:
    return [WEEKDAY_SHORT_LABELS.get(slot.weekday, str(slot.weekday)) for slot in slots]


def _reading_plan_to_dict(session: Session, plan: ReadingPlan) -> dict:
    all_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    active_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
    return {
        "plan_id": plan.id,
        "book_id": plan.book_id,
        "mode": PlanMode(plan.mode),
        "pace": plan.pace,
        "schedule_config": _slots_to_schedule_config(all_slots),
        "reminder_time": plan.reminder_time,
        "status": plan.status,
        "plan_status": plan.status,
        "active_slots": [_slot_to_dict(slot) for slot in active_slots],
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
        "started_at": plan.started_at,
        "paused_at": plan.paused_at,
        "completed_at": plan.completed_at,
        "session_summary": build_plan_session_summary(session, plan_id=plan.id),
    }


def get_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
    if not plan:
        raise ReadingPlanNotFoundError()
    mark_due_sessions_missed(session, user_id=user_id)
    session.commit()
    return _reading_plan_to_dict(session, plan)


def list_reading_plan_slots(session: Session, user_id: uuid.UUID) -> list[dict]:
    return [_user_slot_to_dict(slot) for slot in list_active_slots(session, user_id=user_id)]


def _segments_by_unit(segments: list[LearningUnitSegment]) -> dict[uuid.UUID, list[dict]]:
    result: dict[uuid.UUID, list[dict]] = {}
    for segment in segments:
        result.setdefault(segment.learning_unit_id, []).append(segment.model_dump())
    return result


def _unit_to_dict(unit: LearningUnit, segments: list[dict] | None = None) -> dict:
    return {
        "id": str(unit.id),
        "title": unit.title,
        "status": unit.status,
        "unit_index": unit.unit_index,
        "unit_type": unit.unit_type,
        "source_text_char_count": unit.source_text_char_count,
        "estimated_audio_seconds": unit.estimated_audio_seconds,
        "main_segment_count": unit.main_segment_count,
        "review_text": unit.review_text or "",
        "review_audio_url": unit.review_audio_url or "",
        "planner_reason": unit.planner_reason,
        "segments": segments or [],
    }


def get_book_details(session: Session, book_id: uuid.UUID, user_id: uuid.UUID, *, mode: str | None = None) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    plan = _active_plan(session, book_id, user_id)
    active_mode = PlanMode(mode) if mode else PlanMode(plan.mode)
    learning_summary = build_book_learning_summary_from_state(session, user_id=user_id, book_id=book_id, mode=active_mode)
    units = list_learning_units(session, book_id, active_mode)
    segments_map = _segments_by_unit(list_unit_segments(session, [unit.id for unit in units]))

    return {
        "book_id": book.id,
        "book_status": book.status,
        "mode": active_mode.value,
        "total_sections": book.total_sections,
        "total_units": len(units),
        "learning_summary": learning_summary,
        "units": [_unit_to_dict(unit, segments_map.get(unit.id, [])) for unit in units],
    }


def get_book_outline(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    sections = list_book_section_outline_rows(session, book_id)
    by_parent: dict[uuid.UUID | None, list[BookSectionOutlineRow]] = {}
    for section in sections:
        by_parent.setdefault(section.parent_id, []).append(section)

    def walk(parent_id: uuid.UUID | None = None) -> list[dict]:
        return [
            {
                "id": str(section.id),
                "title": section.title,
                "level": section.level,
                "path": section.path,
                "page_start": section.page_start,
                "page_end": section.page_end,
                "text_char_count": section.text_char_count,
                "children": walk(section.id),
            }
            for section in by_parent.get(parent_id, [])
        ]

    return {
        "book_id": str(book_id),
        "total_sections": len(sections),
        "outline_tree": walk(),
    }


def get_book_learning_units(session: Session, book_id: uuid.UUID, user_id: uuid.UUID, mode: str) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    mode_value = PlanMode(mode)
    units = list_learning_units(session, book_id, mode_value)
    return {
        "book_id": str(book_id),
        "mode": mode_value.value,
        "total_units": len(units),
        "units": [_unit_to_dict(unit) for unit in units],
    }


async def _ensure_learning_units_for_mode(session: Session, *, book: Book, user_id: uuid.UUID, mode: PlanMode) -> list[LearningUnit]:
    existing = list_learning_units(session, book.id, mode)
    if existing:
        return existing

    sections = list_book_sections(session, book.id)
    planned_units = await plan_learning_units_async(sections, mode)
    if not planned_units:
        raise NoReadingPlanError()
    units = create_learning_units(session, user_id=user_id, book_id=book.id, mode=mode, planned_units=planned_units)
    book.total_units = len(units)
    session.add(book)
    session.commit()
    return units


async def switch_book_mode(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    payload_mode: str,
) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    requested_mode = PlanMode(payload_mode)

    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
    if not plan:
        raise ReadingPlanNotFoundError()

    units = await _ensure_learning_units_for_mode(session, book=book, user_id=user_id, mode=requested_mode)
    total_segments = count_unit_segments_by_book_and_mode(session, book_id, requested_mode)
    needs_generation = total_segments == 0

    plan.mode = requested_mode
    session.add(plan)
    session.commit()

    if needs_generation:
        job = _create_switch_mode_job(session, book, user_id, requested_mode, total_units=len(units))
        _enqueue_switch_mode_job(session, book_id, requested_mode.value, job)
        return {
            "message": f"Đã chuyển sang mode {requested_mode.value}. Hệ thống đang sinh audio trong background.",
            "needs_generation": True,
            "job_id": job.id,
            "status": job.status,
            "progress_percent": job.progress_percent,
        }

    return {
        "message": f"Đã chuyển sang mode {requested_mode.value}. Audio đã có sẵn.",
        "needs_generation": False,
        "job_id": None,
        "status": None,
        "progress_percent": None,
    }


def _create_switch_mode_job(session: Session, book: Book, user_id: uuid.UUID, mode: PlanMode, *, total_units: int) -> ProcessingJob:
    job = ProcessingJob(
        user_id=user_id,
        book_id=book.id,
        job_type=ProcessingJobType.SWITCH_MODE,
        status=ProcessingJobStatus.QUEUED,
        mode=mode,
        total_units=total_units,
        done_units=0,
        progress_percent=0,
        current_step=f"Đang chờ sinh audio mode {mode.value}.",
    )
    return create_processing_job(session, job)


def _enqueue_switch_mode_job(session: Session, book_id: uuid.UUID, mode: str, job: ProcessingJob) -> None:
    try:
        switch_mode_task.apply_async(
            args=[str(book_id), mode, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step=f"Không thể đưa tác vụ switch mode {mode} vào hàng đợi.",
            error_message=str(e),
        )
        raise ExternalServiceError("Không thể đưa tác vụ đổi mode vào hàng đợi xử lý. Vui lòng thử lại sau.") from e


def pause_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id, user_id)
    plan.status = PlanStatus.INACTIVE.value
    plan.paused_at = datetime.now(timezone.utc)
    session.add(plan)
    set_slots_active(session, plan_id=plan.id, is_active=False)
    cancel_future_sessions_for_plan(session, plan_id=plan.id)
    session.commit()
    return {"message": "Đã tạm dừng kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}


def resume_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id, user_id)

    if plan.status == PlanStatus.ACTIVE.value:
        return {"message": "Kế hoạch học tập đang hoạt động.", **_reading_plan_to_dict(session, plan)}
    if plan.status == PlanStatus.COMPLETED.value:
        raise BookStatusConflictError("Sách đã hoàn thành. Hãy dùng chức năng ôn tập hoặc học lại nếu muốn bắt đầu vòng mới.")

    if book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
        raise BookStatusConflictError("Tài liệu chưa sẵn sàng để bắt đầu học. Vui lòng chờ hệ thống xử lý thêm.")

    existing_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    if not existing_slots:
        raise ReadingPlanScheduleConflictError("Kế hoạch học tập chưa có lịch học. Vui lòng cập nhật lịch học trước khi tiếp tục.")

    slots = validate_plan_schedule_for_activation(
        session,
        user_id=user_id,
        schedule_config=_slots_to_schedule_config(existing_slots),
        reminder_time=plan.reminder_time,
        exclude_plan_id=plan.id,
    )

    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = plan.started_at or datetime.now(timezone.utc)
    plan.paused_at = None
    session.add(plan)
    replace_slots_for_plan(
        session,
        plan_id=plan.id,
        slots=build_slots_for_plan(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan.id,
            slots=slots,
            is_active=True,
        ),
    )

    try:
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)
        sync_existing_session_units_from_progress(session, plan=plan, user_id=user_id)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from exc
    return {"message": "Đã tiếp tục kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}


def update_reading_plan(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    pace: int | None = None,
    schedule_config: list[str] | None = None,
    reminder_time: str | None = None,
) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    plan = _active_plan(session, book_id, user_id)

    new_pace = pace if pace is not None else plan.pace
    existing_slots = list_slots_for_plan(session, plan_id=plan.id, active_only=False)
    new_schedule_config = schedule_config if schedule_config is not None else _slots_to_schedule_config(existing_slots)
    new_reminder_time = reminder_time if reminder_time is not None else plan.reminder_time

    if plan.status == PlanStatus.ACTIVE.value:
        slots = validate_plan_schedule_for_activation(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
            exclude_plan_id=plan.id,
        )

        replace_slots_for_plan(
            session,
            plan_id=plan.id,
            slots=build_slots_for_plan(
                user_id=user_id,
                book_id=book_id,
                plan_id=plan.id,
                slots=slots,
                is_active=True,
            ),
        )
    else:
        slots = validate_plan_schedule_shape(
            session,
            user_id=user_id,
            schedule_config=new_schedule_config,
            reminder_time=new_reminder_time,
        )
        replace_slots_for_plan(
            session,
            plan_id=plan.id,
            slots=build_slots_for_plan(
                user_id=user_id,
                book_id=book_id,
                plan_id=plan.id,
                slots=slots,
                is_active=False,
            ),
        )

    plan.pace = new_pace
    plan.reminder_time = new_reminder_time
    session.add(plan)
    try:
        if plan.status == PlanStatus.ACTIVE.value:
            ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)
            sync_existing_session_units_from_progress(session, plan=plan, user_id=user_id)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from exc

    return {
        "message": "Đã cập nhật kế hoạch học tập.",
        **_reading_plan_to_dict(session, plan),
    }


def select_shared_book_to_user(session: Session, *, shared_book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    """
    Nhân bản toàn bộ metadata của một sách hệ thống (shared) cho một User cụ thể.
    Sử dụng PostgreSQL Stored Procedure (clone_shared_book) để tối ưu hóa hiệu năng tối đa.
    """

    # 1. Kiểm tra sách gốc có tồn tại và được chia sẻ không
    shared_book = session.get(Book, shared_book_id)
    if not shared_book or not shared_book.is_shared:
        raise ValueError("Sách hệ thống không tồn tại hoặc chưa được chia sẻ công khai.")

    # 2. Kiểm tra xem user đã chọn sách này trước đây chưa
    existing = session.exec(select(Book).where(Book.parent_shared_id == shared_book_id, Book.user_id == user_id)).first()
    if existing:
        return existing

    # 3. Gọi PostgreSQL Stored Function để nhân bản cực nhanh
    new_book_id = uuid.uuid4()
    session.execute(text("SELECT clone_shared_book(:shared_book_id, :new_user_id, :new_book_id)"), {"shared_book_id": shared_book_id, "new_user_id": user_id, "new_book_id": new_book_id})
    session.commit()

    # 4. Trả về đối tượng Book vừa được clone thành công
    cloned_book = session.get(Book, new_book_id)
    if not cloned_book:
        raise ValueError("Lỗi nhân bản sách từ thư viện.")
    return cloned_book


def reset_reading_plan(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """
    Đặt lại toàn bộ tiến độ học tập và lịch biểu của cuốn sách từ đầu cho chế độ học hiện tại.
    """
    # 1. Xác thực sách và kế hoạch học tập hiện có
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    plan = _active_plan(session, book_id, user_id)
    now = datetime.now(timezone.utc)
    mode = PlanMode(plan.mode)

    # 2. Thu thập danh sách ID của các buổi học (sessions) cũ
    sessions = session.exec(
        select(ReadingPlanSession.id).where(ReadingPlanSession.plan_id == plan.id)
    ).all()
    session_ids = [str(sid) for sid in sessions]

    # 3. Thu thập danh sách ID của các thẻ ôn tập (spaced review items) cũ
    review_items = session.exec(
        select(SpacedReviewItem.id).where(
            SpacedReviewItem.user_id == user_id,
            SpacedReviewItem.book_id == book_id,
            SpacedReviewItem.mode == mode,
        )
    ).all()
    review_ids = [str(rid) for rid in review_items]

    # 4. Tạo danh sách các idempotency_key tương ứng trong hàng đợi thông báo để xóa
    keys_to_delete = []
    for sid in session_ids:
        keys_to_delete.append(f"plan-session-reminder:{sid}")
        keys_to_delete.append(f"plan-session-missed:{sid}")
    for rid in review_ids:
        keys_to_delete.append(f"spaced-review:{rid}")

    # 5. Gọi các Repo xóa sạch dữ liệu tiến trình & lịch học
    delete_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    reset_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_spaced_review_items(session, user_id=user_id, book_id=book_id, mode=mode)
    delete_sessions_for_plan(session, plan_id=plan.id)

    # 6. Hủy toàn bộ các thông báo đẩy PENDING còn sót lại trong Outbox
    delete_pending_outbox_by_keys(session, keys=keys_to_delete)

    # Commit trung gian để đồng bộ xóa CSDL tránh xung đột khóa ngoại
    session.flush()

    # 7. Đặt lại trạng thái kế hoạch học tập ban đầu
    plan.status = PlanStatus.ACTIVE.value
    plan.started_at = now
    plan.paused_at = None
    plan.completed_at = None
    plan.updated_at = now
    session.add(plan)
    session.flush()

    # 8. Tự động xếp lịch mới bắt đầu từ Bài học thứ nhất
    ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)

    session.commit()
    return {
        "message": "Đã đặt lại kế hoạch học tập từ đầu thành công.",
        **_reading_plan_to_dict(session, plan)
    }

```

### app\services\book_section_chunker.py

```py
import hashlib
import re
import uuid
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.agent_grounding.query_normalizer import normalized_key

_WHITESPACE_RE = re.compile(r"[ \t\r\f\v]+")


@dataclass(frozen=True)
class SectionChunk:
    section_id: uuid.UUID
    section_title: str
    section_path: str
    chunk_index: int
    content: str
    embedding_text: str
    content_hash: str
    char_count: int



def normalize_section_text(text: str | None) -> str:
    """
    Bộ chuẩn hóa nâng cấp đa ngôn ngữ (Xử lý tối ưu lỗi PDF tiếng Việt và sở hữu cách tiếng Anh)
    """
    if not text:
        return ""

    # 1. Đồng nhất xuống dòng
    text = text.replace("\r\n", "\n")

    # 2. Xóa ký tự rác (cid:xxx)
    text = re.sub(r"\(cid:\d+\)", "•", text)

    # 3. SỬA LỖI ĐẶC THÙ TIẾNG ANH: Vá các khoảng trắng bị lỗi bẻ đôi do sở hữu cách hoặc viết tắt
    # Đổi "george s " -> "george's ", "tha s " -> "that's " (hoặc tha's theo ngôn ngữ gốc của truyện)
    text = re.sub(r"\b(\w+)\s+s\b", r"\1's", text)   # Sửa george s -> george's, curley s -> curley's
    text = re.sub(r"\b(\w+)\s+ll\b", r"\1'll", text)  # Sửa you ll -> you'll
    text = re.sub(r"\b(\w+)\s+d\b", r"\1'd", text)    # Sửa you d -> you'd
    text = re.sub(r"\b(\w+)\s+t\b", r"\1't", text)    # Sửa didn t -> didn't, don t -> don't
    text = re.sub(r"\b(\w+)\s+re\b", r"\1're", text)  # Sửa you re -> you're
    text = re.sub(r"\b(\w+)\s+ve\b", r"\1've", text)  # Sửa you ve -> you've

    # 4. Tách Paragraph bằng dấu xuống dòng kép
    paragraphs = text.split("\n\n")
    normalized_paragraphs = []

    for paragraph in paragraphs:
        p_clean = paragraph.strip()
        if not p_clean:
            continue

        # 5. Xóa bỏ toàn bộ dấu xuống dòng đơn lẻ nằm giữa các câu liền mạch
        p_sub = re.sub(r"(?<![•\-\*\d\.])\n(?!\s*[•\-\*\d\.])", " ", p_clean)

        # 6. Gom khoảng trắng thừa
        p_sub = re.sub(r"[ \t]+", " ", p_sub)

        normalized_paragraphs.append(p_sub.strip())

    return "\n\n".join(normalized_paragraphs)


def build_section_search_text(*, section_path: str, section_title: str, content: str) -> str:
    return normalized_key(f"{section_path} {section_title} {content}")


def build_section_chunks(
    *,
    book_title: str,
    author: str | None,
    section_id: uuid.UUID,
    section_title: str,
    section_path: str,
    text: str | None,
    chunk_size_chars: int,
    chunk_overlap_chars: int,
    embedding_version: str,
) -> list[SectionChunk]:
    normalized_text = normalize_section_text(text)
    if not normalized_text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max(1, chunk_size_chars),
        chunk_overlap=max(0, min(chunk_overlap_chars, chunk_size_chars - 1)),
        separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""],
    )
    raw_chunks = [chunk.strip() for chunk in splitter.split_text(normalized_text) if chunk.strip()]

    chunks: list[SectionChunk] = []
    for index, chunk in enumerate(raw_chunks):
        content = f"[{section_path}]\n{chunk}"
        embedding_parts = [
            f"Book: {book_title}",
            f"Section path: {section_path}",
            f"Section title: {section_title}",
        ]
        if author:
            embedding_parts.insert(1, f"Author: {author}")
        embedding_text = "\n".join(embedding_parts) + f"\nContent:\n{chunk}"
        content_hash = hashlib.sha256(
            f"{embedding_version}\0{section_id}\0{index}\0{content}".encode("utf-8")
        ).hexdigest()
        chunks.append(
            SectionChunk(
                section_id=section_id,
                section_title=section_title,
                section_path=section_path,
                chunk_index=index,
                content=content,
                embedding_text=embedding_text,
                content_hash=content_hash,
                char_count=len(content),
            )
        )
    return chunks

```

### app\services\book_section_knowledge_indexer.py

```py
import uuid
from dataclasses import dataclass
from typing import Protocol

from openai import AsyncOpenAI
from sqlmodel import Session, col, select

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import Book, BookSection, BookSectionKnowledge
from app.repositories.book_section_knowledge_repo import (
    bulk_create_section_knowledge,
    delete_section_knowledge,
    list_section_hashes,
    list_section_knowledge_rows_for_search_text,
    update_section_knowledge_search_text,
)
from app.services.book_section_chunker import SectionChunk, build_section_chunks, build_section_search_text


class SectionEmbeddingProvider(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...


class OpenAISectionEmbeddingProvider:
    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = await self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]


@dataclass(frozen=True)
class BookSectionIndexResult:
    book_id: uuid.UUID
    total_sections: int
    indexed_sections: int
    skipped_sections: int
    chunks_created: int


@dataclass(frozen=True)
class BookSectionSearchTextBackfillResult:
    book_id: uuid.UUID
    updated_rows: int


def _build_records(
    *,
    book_id: uuid.UUID,
    chunks: list[SectionChunk],
    embeddings: list[list[float]],
) -> list[BookSectionKnowledge]:
    return [
        BookSectionKnowledge(
            book_id=book_id,
            section_id=chunk.section_id,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            search_text=build_section_search_text(
                section_path=chunk.section_path,
                section_title=chunk.section_title,
                content=chunk.content,
            ),
            content_hash=chunk.content_hash,
            embedding_model=settings.BOOK_SECTION_EMBEDDING_MODEL,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
            char_count=chunk.char_count,
            embedding=embeddings[index],
        )
        for index, chunk in enumerate(chunks)
    ]


def _section_chunks(book: Book, section: BookSection) -> list[SectionChunk]:
    return build_section_chunks(
        book_title=book.title,
        author=book.author,
        section_id=section.id,
        section_title=section.title,
        section_path=section.path,
        text=section.text_content,
        chunk_size_chars=settings.BOOK_SECTION_CHUNK_SIZE_CHARS,
        chunk_overlap_chars=settings.BOOK_SECTION_CHUNK_OVERLAP_CHARS,
        embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
    )


async def index_book_sections(
    session: Session,
    *,
    book_id: uuid.UUID,
    embedder: SectionEmbeddingProvider | None = None,
) -> BookSectionIndexResult:
    book = session.get(Book, book_id)
    if not book:
        raise ValueError(f"Book not found: {book_id}")

    sections = list(
        session.exec(
            select(BookSection)
            .where(
                BookSection.book_id == book_id,
                BookSection.text_content.is_not(None),
                BookSection.text_char_count > 0,
            )
            .order_by(col(BookSection.section_index))
        ).all()
    )
    if not sections:
        return BookSectionIndexResult(book_id=book_id, total_sections=0, indexed_sections=0, skipped_sections=0, chunks_created=0)

    provider = embedder or OpenAISectionEmbeddingProvider(
        api_key=settings.OPENAI_API_KEY,
        model=settings.BOOK_SECTION_EMBEDDING_MODEL,
    )

    indexed_sections = 0
    skipped_sections = 0
    chunks_created = 0
    batch_size = max(1, settings.BOOK_SECTION_EMBEDDING_BATCH_SIZE)

    for section in sections:
        chunks = _section_chunks(book, section)
        if not chunks:
            skipped_sections += 1
            continue

        current_hashes = list_section_hashes(
            session,
            section_id=section.id,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
        )
        next_hashes = [chunk.content_hash for chunk in chunks]
        if current_hashes == next_hashes:
            skipped_sections += 1
            continue

        delete_section_knowledge(
            session,
            section_id=section.id,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
        )
        for start in range(0, len(chunks), batch_size):
            chunk_batch = chunks[start:start + batch_size]
            embeddings = await provider.embed_texts([chunk.embedding_text for chunk in chunk_batch])
            records = _build_records(book_id=book_id, chunks=chunk_batch, embeddings=embeddings)
            bulk_create_section_knowledge(session, records)
            chunks_created += len(records)

        session.commit()
        indexed_sections += 1

    log.info(
        "BookSectionKnowledge index done | "
        f"book_id={book_id} | sections={len(sections)} | indexed={indexed_sections} | "
        f"skipped={skipped_sections} | chunks_created={chunks_created} | "
        f"version={settings.BOOK_SECTION_EMBEDDING_VERSION}"
    )
    return BookSectionIndexResult(
        book_id=book_id,
        total_sections=len(sections),
        indexed_sections=indexed_sections,
        skipped_sections=skipped_sections,
        chunks_created=chunks_created,
    )


def backfill_book_section_search_text(session: Session, *, book_id: uuid.UUID) -> BookSectionSearchTextBackfillResult:
    rows = list_section_knowledge_rows_for_search_text(session, book_id=book_id)
    updated_rows = 0
    for row in rows:
        next_search_text = build_section_search_text(
            section_path=row.section_path,
            section_title=row.section_title,
            content=row.content,
        )
        if row.search_text == next_search_text:
            continue
        update_section_knowledge_search_text(session, knowledge_id=row.id, search_text=next_search_text)
        updated_rows += 1
    session.commit()
    log.info(f"BookSectionKnowledge search_text backfill done | book_id={book_id} | updated_rows={updated_rows}")
    return BookSectionSearchTextBackfillResult(book_id=book_id, updated_rows=updated_rows)

```

### app\services\chapter_chunking_service.py

```py
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.services.token_budget_service import estimate_tokens


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    estimated_tokens: int


def split_text_for_llm(text: str) -> list[TextChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.LLM_CHUNK_TARGET_TOKENS,
        chunk_overlap=settings.LLM_CHUNK_OVERLAP_TOKENS,
        length_function=estimate_tokens,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
    )
    parts = [part.strip() for part in splitter.split_text(text or "") if part.strip()]
    return [
        TextChunk(
            index=index,
            text=part,
            estimated_tokens=estimate_tokens(part),
        )
        for index, part in enumerate(parts)
    ]

```

### app\services\document_parser_service.py

```py
from __future__ import annotations

from urllib.parse import unquote, urlparse

from app.core.exceptions import UnsupportedFileTypeError
from app.services.document_structure_types import ParsedDocument
from app.services.docx_service import parse_docx_structure
from app.services.epub_service import parse_epub_structure
from app.services.pdf_service import parse_pdf_structure

SUPPORTED_DOCUMENT_TYPES = {"pdf", "epub", "docx"}


def normalize_document_type(document_type: str | None) -> str:
    normalized = (document_type or "").strip().lower().lstrip(".")
    if normalized not in SUPPORTED_DOCUMENT_TYPES:
        raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({document_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")
    return normalized


def infer_document_type_from_url(file_url: str | None) -> str:
    if not file_url:
        return "pdf"

    path = unquote(urlparse(file_url).path).lower()
    for document_type in SUPPORTED_DOCUMENT_TYPES:
        if path.endswith(f".{document_type}"):
            return document_type

    return "pdf"


async def parse_document_structure(file_obj, document_type: str) -> ParsedDocument:
    normalized_type = normalize_document_type(document_type)

    if normalized_type == "pdf":
        return await parse_pdf_structure(file_obj)

    if normalized_type == "epub":
        return await parse_epub_structure(file_obj)

    if normalized_type == "docx":
        return await parse_docx_structure(file_obj)

    raise UnsupportedFileTypeError()

```

### app\services\document_structure_service.py

```py
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from app.core.exceptions import DocumentExtractionError
from app.services.document_structure_types import ParsedDocument, ParsedSection, flatten_sections, section_subtree_text


@dataclass(frozen=True)
class StructureStats:
    total_sections: int
    max_depth: int
    sections_with_text: int


def document_structure_stats(parsed: ParsedDocument) -> StructureStats:
    flattened = flatten_sections(parsed.sections)
    return StructureStats(
        total_sections=len(flattened),
        max_depth=parsed.max_depth,
        sections_with_text=sum(1 for section in flattened if section_subtree_text(section)),
    )


def validate_document_structure(parsed: ParsedDocument) -> None:
    stats = document_structure_stats(parsed)

    if stats.total_sections == 0:
        raise DocumentExtractionError("Tài liệu không có cấu trúc mục lục hợp lệ.")

    if stats.max_depth > 6:
        raise DocumentExtractionError("Cấu trúc mục lục quá sâu, hiện chưa hỗ trợ tài liệu này.")

    if stats.total_sections > 300:
        raise DocumentExtractionError("Tài liệu có quá nhiều đề mục, hiện chưa hỗ trợ xử lý tự động.")

    if stats.sections_with_text == 0:
        raise DocumentExtractionError("Tài liệu có mục lục nhưng không trích xuất được nội dung text.")


def detect_structure_warnings(parsed: ParsedDocument) -> list[str]:
    flattened = flatten_sections(parsed.sections)
    warnings: list[str] = []

    if not flattened:
        return warnings

    levels = Counter(section.level for section in flattened)
    if len(levels) == 1 and len(flattened) >= 20:
        warnings.append("Tài liệu có outline phẳng với nhiều đề mục. TRIAM sẽ tự gom các đề mục liên quan thành bài nghe.")

    short_sections = sum(1 for section in flattened if 0 < len(section_subtree_text(section)) < 500)
    if short_sections / max(1, len(flattened)) >= 0.5:
        warnings.append("Nhiều đề mục khá ngắn. Hệ thống sẽ gộp các mục nhỏ để tránh tạo audio quá vụn.")

    return warnings


def build_outline_preview(parsed: ParsedDocument, *, max_nodes: int = 120) -> list[dict[str, Any]]:
    remaining = max_nodes

    def walk(sections: list[ParsedSection]) -> list[dict[str, Any]]:
        nonlocal remaining
        result: list[dict[str, Any]] = []
        for section in sections:
            if remaining <= 0:
                break
            remaining -= 1
            children = walk(section.children)
            result.append(
                {
                    "title": section.title,
                    "level": section.level,
                    "path": section.path,
                    "page_start": section.page_start,
                    "page_end": section.page_end,
                    "text_char_count": len(section_subtree_text(section)),
                    "children": children,
                }
            )
        return result

    return walk(parsed.sections)

```

### app\services\document_structure_types.py

```py
from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class ParsedSection:
    title: str
    level: int
    order_index: int
    path: str
    text: str = ""
    page_start: int | None = None
    page_end: int | None = None
    source_href: str | None = None
    source_anchor: str | None = None
    top: float | None = None
    children: list["ParsedSection"] = field(default_factory=list)

    @property
    def text_char_count(self) -> int:
        return len(self.text or "")


@dataclass(frozen=True)
class ParsedDocument:
    document_type: str
    sections: list[ParsedSection]

    @property
    def total_sections(self) -> int:
        return len(flatten_sections(self.sections))

    @property
    def max_depth(self) -> int:
        return max_section_depth(self.sections)


def flatten_sections(sections: list[ParsedSection]) -> list[ParsedSection]:
    flattened: list[ParsedSection] = []

    def walk(items: list[ParsedSection]) -> None:
        for section in items:
            flattened.append(section)
            walk(section.children)

    walk(sections)
    return flattened


def max_section_depth(sections: list[ParsedSection]) -> int:
    if not sections:
        return 0

    def depth(section: ParsedSection) -> int:
        if not section.children:
            return section.level
        return max(depth(child) for child in section.children)

    return max(depth(section) for section in sections)


def section_subtree_text(section: ParsedSection) -> str:
    parts: list[str] = []

    def walk(item: ParsedSection) -> None:
        if item.text.strip():
            parts.append(item.text.strip())
        for child in item.children:
            walk(child)

    walk(section)
    return "\n\n".join(parts).strip()


def has_extractable_text(sections: list[ParsedSection]) -> bool:
    return any(section_subtree_text(section) for section in sections)


def with_reindexed_paths(sections: list[ParsedSection]) -> list[ParsedSection]:
    def walk(items: list[ParsedSection], parent_path: str = "") -> list[ParsedSection]:
        updated: list[ParsedSection] = []
        for index, section in enumerate(items, start=1):
            path = f"{parent_path}.{index}" if parent_path else str(index)
            updated.append(
                replace(
                    section,
                    order_index=index - 1,
                    path=path,
                    children=walk(section.children, path),
                )
            )
        return updated

    return walk(sections)

```

### app\services\docx_service.py

```py
from __future__ import annotations

from dataclasses import dataclass, field

from docx import Document
from docx.oxml.ns import qn

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError
from app.services.document_structure_types import ParsedDocument, ParsedSection

HEADING_STYLE_NAMES = {
    "heading 1",
    "heading 2",
    "heading 3",
}


@dataclass
class _SectionBuilder:
    title: str
    level: int
    order_index: int
    path: str
    parts: list[str] = field(default_factory=list)
    children: list["_SectionBuilder"] = field(default_factory=list)

    def to_parsed(self) -> ParsedSection:
        return ParsedSection(
            title=self.title,
            level=self.level,
            order_index=self.order_index,
            path=self.path,
            text="\n".join(self.parts).strip(),
            page_start=None,
            page_end=None,
            children=[child.to_parsed() for child in self.children],
        )


def _has_outline_level(paragraph) -> bool:
    if paragraph.style is None or paragraph.style.element is None:
        return False

    p_pr = paragraph.style.element.find(qn("w:pPr"))
    if p_pr is None:
        return False

    return p_pr.find(qn("w:outlineLvl")) is not None


def _outline_level(paragraph) -> int | None:
    if paragraph.style is None or paragraph.style.element is None:
        return None

    p_pr = paragraph.style.element.find(qn("w:pPr"))
    if p_pr is None:
        return None

    outline = p_pr.find(qn("w:outlineLvl"))
    if outline is None:
        return None

    value = outline.get(qn("w:val"))
    if value is None:
        return None

    try:
        return int(value) + 1
    except ValueError:
        return None


def _heading_level(paragraph) -> int | None:
    style_name = (paragraph.style.name or "").strip().lower() if paragraph.style else ""
    if style_name.startswith("heading "):
        suffix = style_name.removeprefix("heading ").strip()
        if suffix.isdigit():
            return max(1, min(6, int(suffix)))

    outline_level = _outline_level(paragraph)
    if outline_level is not None:
        return max(1, min(6, outline_level))

    return None


def _is_heading(paragraph) -> bool:
    style_name = (paragraph.style.name or "").strip().lower() if paragraph.style else ""
    return style_name in HEADING_STYLE_NAMES or style_name.startswith("heading ") or _has_outline_level(paragraph)


def parse_docx_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)

    try:
        document = Document(file_obj)
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc DOCX: {exc}") from exc

    roots: list[_SectionBuilder] = []
    stack: list[_SectionBuilder] = []
    sibling_counts: dict[str, int] = {"": 0}

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        if _is_heading(paragraph):
            level = _heading_level(paragraph) or 1
            while stack and stack[-1].level >= level:
                stack.pop()

            parent = stack[-1] if stack else None
            parent_path = parent.path if parent else ""
            sibling_counts[parent_path] = sibling_counts.get(parent_path, 0) + 1
            order_index = sibling_counts[parent_path] - 1
            path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
            builder = _SectionBuilder(title=text, level=level, order_index=order_index, path=path)

            if parent:
                parent.children.append(builder)
            else:
                roots.append(builder)

            stack.append(builder)
            continue

        if stack:
            stack[-1].parts.append(text)

    if not roots:
        raise DocumentOutlineRequiredError("DOCX không có Heading/mục lục hợp lệ. Vui lòng dùng Heading 1/Heading 2 cho tên chương.")

    return ParsedDocument(document_type="docx", sections=[root.to_parsed() for root in roots])


async def parse_docx_structure(file_obj) -> ParsedDocument:
    import asyncio
    import io
    file_bytes = file_obj.read()
    return await asyncio.to_thread(parse_docx_structure_sync, io.BytesIO(file_bytes))

```

### app\services\epub_service.py

```py
from __future__ import annotations

from io import BytesIO

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError
from app.services.document_structure_types import ParsedDocument, ParsedSection, has_extractable_text


def _html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup(["script", "style", "nav"]):
        tag.decompose()

    lines = [line.strip() for line in soup.get_text("\n").splitlines() if line.strip()]
    return "\n".join(lines)


def _split_href(href: str | None) -> tuple[str | None, str | None]:
    if not href:
        return None, None
    source_href, _, source_anchor = href.partition("#")
    return source_href or None, source_anchor or None


def _epub_toc_tree(toc_items, documents_by_href: dict[str, bytes], level: int = 1, parent_path: str = "") -> list[ParsedSection]:
    sections: list[ParsedSection] = []
    for item in toc_items:
        if isinstance(item, tuple):
            parent, children = item
            title = str(getattr(parent, "title", "") or "").strip()
            href = getattr(parent, "href", None)
            source_href, source_anchor = _split_href(href)
            if title and source_href:
                order_index = len(sections)
                path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
                content = documents_by_href.get(source_href)
                sections.append(
                    ParsedSection(
                        title=title,
                        level=level,
                        order_index=order_index,
                        path=path,
                        text=_html_to_text(content) if content else "",
                        page_start=None,
                        page_end=None,
                        source_href=source_href,
                        source_anchor=source_anchor,
                        children=_epub_toc_tree(children, documents_by_href, level + 1, path),
                    )
                )
            else:
                sections.extend(_epub_toc_tree(children, documents_by_href, level, parent_path))
            continue

        title = str(getattr(item, "title", "") or "").strip()
        href = getattr(item, "href", None)
        source_href, source_anchor = _split_href(href)
        if title and source_href:
            order_index = len(sections)
            path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
            content = documents_by_href.get(source_href)
            sections.append(
                ParsedSection(
                    title=title,
                    level=level,
                    order_index=order_index,
                    path=path,
                    text=_html_to_text(content) if content else "",
                    page_start=None,
                    page_end=None,
                    source_href=source_href,
                    source_anchor=source_anchor,
                )
            )

    return sections


def parse_epub_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)

    try:
        book = epub.read_epub(BytesIO(file_obj.read()))
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc EPUB: {exc}") from exc

    documents_by_href = {item.get_name(): item.get_content() for item in book.get_items_of_type(ITEM_DOCUMENT)}
    sections = _epub_toc_tree(book.toc, documents_by_href)
    if not sections:
        raise DocumentOutlineRequiredError("EPUB không có mục lục điều hướng hợp lệ. Vui lòng upload EPUB có TOC chuẩn.")

    if not has_extractable_text(sections):
        raise DocumentExtractionError("EPUB có mục lục nhưng không trích xuất được text. File có thể bị lỗi hoặc không phải text-based EPUB.")

    return ParsedDocument(document_type="epub", sections=sections)


async def parse_epub_structure(file_obj) -> ParsedDocument:
    import asyncio
    import io
    file_bytes = file_obj.read()
    return await asyncio.to_thread(parse_epub_structure_sync, io.BytesIO(file_bytes))

```

### app\services\fcm_service.py

```py
import json
import os
import uuid
from datetime import datetime, timezone
from hashlib import sha256

import firebase_admin
from firebase_admin import credentials, messaging
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import UserDeviceToken

_firebase_initialized = False


def _token_fingerprint(device_token: str) -> str:
    return sha256(device_token.encode("utf-8")).hexdigest()[:12]


def _stringify_fcm_data(data: dict[str, str] | None) -> dict[str, str]:
    if not data:
        return {}
    return {str(key): str(value) for key, value in data.items()}


def _delete_device_tokens(session: Session, device_tokens: list[str]) -> None:
    if not device_tokens:
        return
    db_tokens = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token.in_(device_tokens))).all()
    for token_record in db_tokens:
        session.delete(token_record)
    session.commit()
    log.info(f"Đã xóa {len(device_tokens)} token không khả dụng khỏi DB.")


def _collect_invalid_tokens(response: messaging.BatchResponse, device_tokens: list[str]) -> list[str]:
    tokens_to_delete: list[str] = []
    for idx, resp in enumerate(response.responses):
        if resp.success:
            continue

        exc = resp.exception
        token = device_tokens[idx]
        token_hash = _token_fingerprint(token)
        if isinstance(exc, (messaging.UnregisteredError, messaging.SenderIdMismatchError)):
            log.info(f"FCM token không khả dụng ({type(exc).__name__}), token_hash={token_hash}")
            tokens_to_delete.append(token)
        else:
            log.warning(f"Lỗi gửi push cho token_hash={token_hash}: {exc}")
    return tokens_to_delete


def init_firebase() -> bool:
    """
    Khởi tạo Firebase Admin SDK một cách an toàn.
    """
    global _firebase_initialized
    if _firebase_initialized or firebase_admin._apps:
        _firebase_initialized = True
        return True

    try:
        if settings.FIREBASE_CREDENTIALS_JSON:
            log.info("Khởi tạo Firebase Admin SDK từ chuỗi JSON môi trường...")
            cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
        elif settings.FIREBASE_CREDENTIALS_FILE:
            file_path = settings.FIREBASE_CREDENTIALS_FILE
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            if os.path.exists(file_path):
                log.info(f"Khởi tạo Firebase Admin SDK từ file: {file_path}")
                cred = credentials.Certificate(file_path)
                firebase_admin.initialize_app(cred)
                _firebase_initialized = True
            else:
                log.warning(f"File key Firebase không tồn tại tại: {file_path}. Push notification chạy giả lập.")
        else:
            log.warning("Firebase credentials chưa được cấu hình. Push notification chạy giả lập.")
    except Exception as e:
        log.error(f"Khởi tạo Firebase lỗi: {e}. Push notification chạy giả lập.")

    return _firebase_initialized


def send_fcm_notification(
    session: Session,
    *,
    user_id: uuid.UUID,
    title: str,
    body: str,
    data: dict[str, str] | None = None,
) -> None:
    """
    Gửi thông báo Push qua FCM đến tất cả thiết bị của user_id.
    Tự động dọn dẹp các token bị báo lỗi Unregistered/SenderIdMismatch.
    """
    device_tokens = list(session.exec(select(UserDeviceToken.device_token).where(UserDeviceToken.user_id == user_id)).all())

    if not device_tokens:
        log.debug(f"User {user_id} không có device token đăng ký. Bỏ qua gửi push.")
        return

    initialized = init_firebase()
    if not initialized:
        log.warning(f"[MOCK PUSH] Gửi đến user {user_id} ({len(device_tokens)} thiết bị) | Title: '{title}' | Body: '{body}' | Data: {data}")
        return

    log.info(f"Đang gửi push notification cho user {user_id} tới {len(device_tokens)} thiết bị...")
    string_data = _stringify_fcm_data(data)
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=string_data if string_data else None,
        tokens=list(device_tokens),
    )

    try:
        response = messaging.send_each_for_multicast(message)
        log.info(f"FCM multicast done | success={response.success_count} | failure={response.failure_count}")

        if response.failure_count > 0:
            _delete_device_tokens(session, _collect_invalid_tokens(response, device_tokens))
    except Exception as e:
        log.error(f"Gửi multicast FCM gặp lỗi hệ thống: {e}")


def register_user_device_token(session: Session, user_id: uuid.UUID, device_token: str) -> UserDeviceToken:
    """
    Đăng ký hoặc cập nhật device token cho user.
    Nếu token đã được đăng ký bởi user khác, sẽ chuyển quyền sở hữu sang user hiện tại.
    """
    existing = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token == device_token)).first()

    if existing:
        if existing.user_id == user_id:
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing
        else:
            log.info(f"Chuyển device_token từ user {existing.user_id} sang user {user_id}")
            existing.user_id = user_id
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

    new_token = UserDeviceToken(user_id=user_id, device_token=device_token)
    session.add(new_token)
    session.commit()
    session.refresh(new_token)
    return new_token


def unregister_user_device_token(session: Session, user_id: uuid.UUID, device_token: str) -> bool:
    """
    Hủy đăng ký device token của user.
    """
    token_record = session.exec(select(UserDeviceToken).where(UserDeviceToken.user_id == user_id, UserDeviceToken.device_token == device_token)).first()

    if not token_record:
        return False

    session.delete(token_record)
    session.commit()
    return True

```

### app\services\health_service.py

```py
from typing import Any

from redis import Redis
from sqlalchemy import text
from sqlmodel import Session

from app.core.config import settings
from app.db.database import engine

DOCUMENT_QUEUE_NAME = "document"


def _exception_name(exc: Exception) -> str:
    return type(exc).__name__


def get_background_health() -> dict[str, Any]:
    health: dict[str, Any] = {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
        "document_queue_length": None,
    }

    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1")).one()
    except Exception as exc:
        health["status"] = "degraded"
        health["database"] = "error"
        health["database_error"] = _exception_name(exc)

    redis_client: Redis | None = None
    try:
        redis_client = Redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)
        redis_client.ping()
        health["document_queue_length"] = redis_client.llen(DOCUMENT_QUEUE_NAME)
    except Exception as exc:
        health["status"] = "degraded"
        health["redis"] = "error"
        health["redis_error"] = _exception_name(exc)
    finally:
        if redis_client:
            redis_client.close()

    return health

```

### app\services\learning_progress_service.py

```py
import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookLearningStatus, LearningProgressStatus, PlanMode, PlanStatus
from app.core.exceptions import BadRequestError, BookNotFoundError, NoPlayableAudioError
from app.models.db_models import Book, BookLearningState, LearningUnit, LearningUnitProgress, LearningUnitSegment
from app.repositories.book_learning_state_repo import get_book_learning_state, upsert_book_learning_state
from app.repositories.learning_progress_repo import get_latest_activity, get_progress, list_book_progress, list_playable_unit_ids, save_progress
from app.repositories.reading_plan_repo import get_plan_for_book_mode
from app.repositories.reading_plan_schedule_repo import set_slots_active
from app.repositories.spaced_review_repo import count_review_items_for_user
from app.schemas.learning_progress import (
    BookLearningProgressResponse,
    BookLearningSummaryResponse,
    LearningUnitProgressResponse,
    LearningUnitProgressUpdateRequest,
)
from app.services.reading_plan_session_service import cancel_future_sessions_for_plan, sync_reading_plan_session_unit_completion
from app.services.spaced_review_service import create_spaced_reviews_after_unit_completion


def _load_owned_book(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID) -> Book:
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    return book


def _load_learning_unit(session: Session, *, book_id: uuid.UUID, learning_unit_id: uuid.UUID, mode: PlanMode) -> LearningUnit:
    unit = session.exec(
        select(LearningUnit).where(
            LearningUnit.id == learning_unit_id,
            LearningUnit.book_id == book_id,
            LearningUnit.mode == mode,
        )
    ).first()
    if not unit:
        raise BadRequestError("Bài học không thuộc sách/mode này.")
    return unit


def _segments_for_unit(session: Session, *, learning_unit_id: uuid.UUID) -> list[LearningUnitSegment]:
    return list(
        session.exec(
            select(LearningUnitSegment)
            .where(LearningUnitSegment.learning_unit_id == learning_unit_id)
            .order_by(LearningUnitSegment.segment_index)
        ).all()
    )


def _resolve_segment(
    segments: list[LearningUnitSegment],
    *,
    segment_id: int | None,
    segment_index: int,
) -> LearningUnitSegment:
    if not segments:
        raise NoPlayableAudioError("Bài học này chưa có audio để ghi nhận tiến độ.")

    if segment_id is not None:
        for segment in segments:
            if segment.id == segment_id:
                return segment
        raise BadRequestError("Segment không thuộc bài học này.")

    for segment in segments:
        if segment.segment_index == segment_index:
            return segment
    raise BadRequestError("Segment index không thuộc bài học này.")


def _compute_progress_percent(
    *,
    segments: list[LearningUnitSegment],
    segment_index: int,
    position_ms: int,
    fallback_percent: int | None,
    fallback_total_duration_ms: int | None,
) -> tuple[int, int]:
    durations = [segment.duration_ms or 0 for segment in segments]
    total_duration = sum(durations) or int(fallback_total_duration_ms or 0)
    if sum(durations) > 0:
        before = sum(durations[:segment_index])
        current = min(sum(durations), before + max(0, position_ms))
        return max(0, min(100, int(current * 100 / sum(durations)))), sum(durations)
    return max(0, min(100, int(fallback_percent or 0))), total_duration


def _to_unit_response(progress: LearningUnitProgress) -> LearningUnitProgressResponse:
    return LearningUnitProgressResponse(
        learning_unit_id=progress.learning_unit_id,
        mode=progress.mode,
        segment_id=progress.current_segment_id,
        segment_index=progress.last_segment_index,
        position_ms=progress.position_ms,
        progress_percent=progress.progress_percent,
        max_progress_percent=progress.max_progress_percent,
        status=progress.status,
        started_at=progress.started_at,
        last_activity_at=progress.last_activity_at,
        completed_at=progress.completed_at,
    )


def _create_reviews_after_completion_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book: Book,
    unit: LearningUnit,
    progress: LearningUnitProgress,
) -> None:
    if not progress.completed_at:
        return
    create_spaced_reviews_after_unit_completion(
        session,
        user_id=user_id,
        book_id=book.id,
        learning_unit_id=unit.id,
        mode=unit.mode,
        review_text=unit.review_text or "",
        completed_at=progress.completed_at,
        source_unit_progress_id=progress.id,
    )


def _should_persist_progress(
    existing: LearningUnitProgress | None,
    *,
    now: datetime,
    segment: LearningUnitSegment,
    progress_percent: int,
    force_persist: bool,
) -> bool:
    if existing is None:
        return True
    if force_persist:
        return True
    if existing.completed_at is None and progress_percent >= settings.LEARNING_COMPLETION_THRESHOLD_PERCENT:
        return True
    if existing.current_segment_id != segment.id or existing.last_segment_index != segment.segment_index:
        return True
    if progress_percent - existing.max_progress_percent >= settings.LEARNING_PROGRESS_MIN_DELTA_PERCENT:
        return True

    last_saved_at = existing.last_activity_at or existing.updated_at
    return bool(last_saved_at and now - last_saved_at >= timedelta(seconds=settings.LEARNING_PROGRESS_STALE_SECONDS))


def _complete_reading_plan_if_needed(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
    completed_at: datetime,
) -> None:
    plan = get_plan_for_book_mode(session, book_id=book_id, mode=mode)
    if not plan or plan.status == PlanStatus.COMPLETED.value:
        return

    plan.status = PlanStatus.COMPLETED.value
    plan.completed_at = plan.completed_at or completed_at
    plan.updated_at = datetime.now(timezone.utc)
    session.add(plan)
    set_slots_active(session, plan_id=plan.id, is_active=False)
    cancel_future_sessions_for_plan(session, plan_id=plan.id, now=completed_at)
    session.commit()


def sync_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningState:
    playable_ids = list_playable_unit_ids(session, book_id=book_id, mode=mode)
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    progress_by_unit = {progress.learning_unit_id: progress for progress in progress_rows}
    existing_state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)

    playable_count = len(playable_ids)
    total_percent = 0
    completed_count = 0
    started_at_candidates: list[datetime] = []
    latest_activity_candidates: list[datetime] = []
    completed_at_candidates: list[datetime] = []

    for learning_unit_id in playable_ids:
        progress = progress_by_unit.get(learning_unit_id)
        if not progress:
            continue
        total_percent += progress.max_progress_percent
        completed_count += int(progress.status == LearningProgressStatus.COMPLETED)
        if progress.started_at:
            started_at_candidates.append(progress.started_at)
        if progress.last_activity_at:
            latest_activity_candidates.append(progress.last_activity_at)
        if progress.completed_at:
            completed_at_candidates.append(progress.completed_at)

    latest = get_latest_activity(session, user_id=user_id, book_id=book_id, mode=mode)
    if playable_count and completed_count >= playable_count:
        learning_status = BookLearningStatus.COMPLETED
    elif progress_rows:
        learning_status = BookLearningStatus.IN_PROGRESS
    else:
        learning_status = BookLearningStatus.NOT_STARTED

    completed_at = None
    if learning_status == BookLearningStatus.COMPLETED:
        completed_at = existing_state.completed_at if existing_state and existing_state.completed_at else max(completed_at_candidates, default=datetime.now(timezone.utc))

    state = upsert_book_learning_state(
        session,
        user_id=user_id,
        book_id=book_id,
        mode=mode,
        status=learning_status.value,
        book_progress_percent=int(total_percent / playable_count) if playable_count else 0,
        completed_units=completed_count,
        playable_units=playable_count,
        last_learning_unit_id=latest.learning_unit_id if latest else None,
        last_segment_id=latest.current_segment_id if latest else None,
        last_segment_index=latest.last_segment_index if latest else None,
        position_ms=latest.position_ms if latest else 0,
        started_at=min(started_at_candidates, default=None),
        last_activity_at=max(latest_activity_candidates, default=None),
        completed_at=completed_at,
    )
    if learning_status == BookLearningStatus.COMPLETED and completed_at:
        _complete_reading_plan_if_needed(session, book_id=book_id, mode=mode, completed_at=completed_at)
    return state


def build_book_learning_summary(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningSummaryResponse:
    state = sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    return build_book_learning_summary_from_state(
        session,
        user_id=user_id,
        book_id=book_id,
        mode=mode,
        state=state,
    )


def build_book_learning_summary_from_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    state: BookLearningState | None = None,
    include_review_counts: bool = True,
) -> BookLearningSummaryResponse:
    state = state or get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    due_reviews_count = 0
    upcoming_reviews_count = 0
    if include_review_counts:
        now = datetime.now(timezone.utc)
        due_reviews_count = count_review_items_for_user(
            session,
            user_id=user_id,
            now=now,
            status_filter="due",
            book_id=book_id,
            mode=mode,
        )
        upcoming_reviews_count = count_review_items_for_user(
            session,
            user_id=user_id,
            now=now,
            status_filter="upcoming",
            book_id=book_id,
            mode=mode,
        )
    if state is None:
        learning_status = BookLearningStatus.NOT_STARTED
        return BookLearningSummaryResponse(
            book_id=book_id,
            mode=mode,
            learning_status=learning_status,
            is_completed=False,
            can_resume=False,
            can_review=due_reviews_count > 0 or upcoming_reviews_count > 0,
            book_progress_percent=0,
            completed_units=0,
            playable_units=0,
            last_learning_unit_id=None,
            last_segment_id=None,
            last_segment_index=None,
            position_ms=None,
            started_at=None,
            last_activity_at=None,
            completed_at=None,
            due_reviews_count=due_reviews_count,
            upcoming_reviews_count=upcoming_reviews_count,
        )

    learning_status = BookLearningStatus(state.status)
    return BookLearningSummaryResponse(
        book_id=book_id,
        mode=mode,
        learning_status=learning_status,
        is_completed=learning_status == BookLearningStatus.COMPLETED,
        can_resume=learning_status == BookLearningStatus.IN_PROGRESS,
        can_review=state.completed_units > 0 or due_reviews_count > 0 or upcoming_reviews_count > 0,
        book_progress_percent=state.book_progress_percent,
        completed_units=state.completed_units,
        playable_units=state.playable_units,
        last_learning_unit_id=state.last_learning_unit_id,
        last_segment_id=state.last_segment_id,
        last_segment_index=state.last_segment_index,
        position_ms=state.position_ms if state.last_learning_unit_id else None,
        started_at=state.started_at,
        last_activity_at=state.last_activity_at,
        completed_at=state.completed_at,
        due_reviews_count=due_reviews_count,
        upcoming_reviews_count=upcoming_reviews_count,
    )


def update_learning_unit_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    payload: LearningUnitProgressUpdateRequest,
) -> LearningUnitProgressResponse:
    mode = PlanMode(payload.mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    unit = _load_learning_unit(session, book_id=book_id, learning_unit_id=learning_unit_id, mode=mode)
    segments = _segments_for_unit(session, learning_unit_id=learning_unit_id)
    segment = _resolve_segment(segments, segment_id=payload.segment_id, segment_index=payload.segment_index)
    progress_percent, total_duration_ms = _compute_progress_percent(
        segments=segments,
        segment_index=segment.segment_index,
        position_ms=payload.position_ms,
        fallback_percent=payload.progress_percent,
        fallback_total_duration_ms=payload.total_duration_ms,
    )

    now = datetime.now(timezone.utc)
    progress = get_progress(session, user_id=user_id, learning_unit_id=learning_unit_id)
    if not _should_persist_progress(
        progress,
        now=now,
        segment=segment,
        progress_percent=progress_percent,
        force_persist=payload.force_persist,
    ):
        return _to_unit_response(progress)

    first_completion = False
    if not progress:
        progress = LearningUnitProgress(
            user_id=user_id,
            book_id=book_id,
            learning_unit_id=learning_unit_id,
            mode=mode,
            started_at=now,
        )

    progress.current_segment_id = segment.id
    progress.last_segment_index = segment.segment_index
    progress.position_ms = payload.position_ms
    progress.listened_ms = max(progress.listened_ms, payload.listened_ms)
    progress.total_duration_ms = total_duration_ms
    progress.progress_percent = progress_percent
    progress.max_progress_percent = max(progress.max_progress_percent, progress_percent)
    progress.last_activity_at = now
    progress.updated_at = now

    if progress.completed_at is None and progress.max_progress_percent >= settings.LEARNING_COMPLETION_THRESHOLD_PERCENT:
        progress.status = LearningProgressStatus.COMPLETED
        progress.completed_at = now
        first_completion = True
    elif progress.completed_at is not None:
        progress.status = LearningProgressStatus.COMPLETED
    else:
        progress.status = LearningProgressStatus.IN_PROGRESS

    saved = save_progress(session, progress)
    if first_completion:
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, unit=unit, progress=saved)
    sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    sync_reading_plan_session_unit_completion(
        session,
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode,
        progress_status=saved.status,
        completed_at=saved.completed_at,
        now=saved.last_activity_at,
    )
    return _to_unit_response(saved)


def complete_learning_unit_manually(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode,
) -> LearningUnitProgressResponse:
    mode_value = PlanMode(mode)
    book = _load_owned_book(session, user_id=user_id, book_id=book_id)
    unit = _load_learning_unit(session, book_id=book_id, learning_unit_id=learning_unit_id, mode=mode_value)
    segments = _segments_for_unit(session, learning_unit_id=learning_unit_id)
    if not segments:
        raise NoPlayableAudioError("Bài học này chưa có audio để hoàn thành.")

    now = datetime.now(timezone.utc)
    last_segment = segments[-1]
    total_duration_ms = sum(segment.duration_ms or 0 for segment in segments)
    progress = get_progress(session, user_id=user_id, learning_unit_id=learning_unit_id)
    first_completion = False
    if not progress:
        progress = LearningUnitProgress(
            user_id=user_id,
            book_id=book_id,
            learning_unit_id=learning_unit_id,
            mode=mode_value,
            started_at=now,
        )

    if progress.completed_at is None:
        progress.completed_at = now
        first_completion = True

    progress.current_segment_id = last_segment.id
    progress.last_segment_index = last_segment.segment_index
    progress.position_ms = last_segment.duration_ms or 0
    progress.total_duration_ms = total_duration_ms
    progress.progress_percent = 100
    progress.max_progress_percent = 100
    progress.status = LearningProgressStatus.COMPLETED
    progress.last_activity_at = now
    progress.updated_at = now
    saved = save_progress(session, progress)
    if first_completion:
        _create_reviews_after_completion_once(session, user_id=user_id, book=book, unit=unit, progress=saved)
    sync_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode_value)
    sync_reading_plan_session_unit_completion(
        session,
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode_value,
        progress_status=saved.status,
        completed_at=saved.completed_at,
        now=saved.last_activity_at,
    )
    return _to_unit_response(saved)


def get_book_learning_progress(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> BookLearningProgressResponse:
    mode_value = PlanMode(mode)
    _load_owned_book(session, user_id=user_id, book_id=book_id)
    playable_ids = list_playable_unit_ids(session, book_id=book_id, mode=mode_value)
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode_value)
    progress_by_unit = {progress.learning_unit_id: progress for progress in progress_rows}

    units: list[LearningUnitProgressResponse] = []
    for learning_unit_id in playable_ids:
        progress = progress_by_unit.get(learning_unit_id)
        if progress:
            units.append(_to_unit_response(progress))
        else:
            units.append(
                LearningUnitProgressResponse(
                    learning_unit_id=learning_unit_id,
                    mode=mode_value,
                    segment_id=None,
                    segment_index=0,
                    position_ms=0,
                    progress_percent=0,
                    max_progress_percent=0,
                    status=LearningProgressStatus.NOT_STARTED,
                    started_at=None,
                    last_activity_at=None,
                    completed_at=None,
                )
            )

    summary = build_book_learning_summary(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return BookLearningProgressResponse(
        **summary.model_dump(),
        units=units,
    )

```

### app\services\learning_unit_planner_service.py

```py
from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.core.config import settings
from app.core.constant import PlanMode
from app.models.db_models import BookSection
from app.services.token_budget_service import estimate_text_budget

FULL_UNIT_TARGET_TOKENS = 5000
FULL_UNIT_MAX_TOKENS = 12000
MIN_UNIT_TOKENS = 300


@dataclass(frozen=True)
class PlannedLearningUnit:
    title: str
    unit_type: str
    source_section_ids: list[uuid.UUID]
    source_text: str
    source_text_char_count: int
    estimated_tokens: int
    estimated_audio_seconds: int
    planner_reason: str | None = None


def _children_by_parent(sections: list[BookSection]) -> dict[uuid.UUID | None, list[BookSection]]:
    children: dict[uuid.UUID | None, list[BookSection]] = {}
    for section in sorted(sections, key=lambda item: item.section_index):
        children.setdefault(section.parent_id, []).append(section)
    return children


def _subtree_sections(root: BookSection, children: dict[uuid.UUID | None, list[BookSection]]) -> list[BookSection]:
    result = [root]
    for child in children.get(root.id, []):
        result.extend(_subtree_sections(child, children))
    return result


def _sections_text(sections: list[BookSection]) -> str:
    parts = [section.text_content.strip() for section in sections if section.text_content and section.text_content.strip()]
    return "\n\n".join(parts).strip()


def _make_unit(title: str, unit_type: str, source_sections: list[BookSection], reason: str | None = None) -> PlannedLearningUnit | None:
    ordered = sorted(source_sections, key=lambda item: item.section_index)
    source_text = _sections_text(ordered)
    if not source_text:
        return None
    budget = estimate_text_budget(source_text)
    return PlannedLearningUnit(
        title=title.strip() or "Bài học",
        unit_type=unit_type,
        source_section_ids=[section.id for section in ordered],
        source_text=source_text,
        source_text_char_count=budget.char_count,
        estimated_tokens=budget.estimated_tokens,
        estimated_audio_seconds=budget.estimated_audio_seconds,
        planner_reason=reason,
    )


def _format_split_title(title: str, part_number: int, total_parts: int) -> str:
    base_title = title.strip() or "Bài học"
    if total_parts <= 1:
        return base_title
    return f"{base_title} - Phần {part_number}/{total_parts}"


def _split_large_group(
    title: str,
    source_sections: list[BookSection],
    unit_type: str,
    *,
    max_tokens: int = FULL_UNIT_MAX_TOKENS,
) -> list[PlannedLearningUnit]:
    chunks: list[list[BookSection]] = []
    current: list[BookSection] = []
    current_tokens = 0

    for section in sorted(source_sections, key=lambda item: item.section_index):
        section_text = section.text_content or ""
        section_tokens = estimate_text_budget(section_text).estimated_tokens if section_text.strip() else 0
        if current and current_tokens > 0 and current_tokens + section_tokens > max_tokens:
            chunks.append(current)
            current = []
            current_tokens = 0
        current.append(section)
        current_tokens += section_tokens

    if current:
        chunks.append(current)

    units: list[PlannedLearningUnit] = []
    total_parts = len(chunks)
    for index, chunk in enumerate(chunks, start=1):
        split_title = _format_split_title(title, index, total_parts)
        reason = (
            "Tách từ nhóm lớn để không vượt giới hạn xử lý."
            if total_parts <= 1
            else f"Tách từ nhóm lớn thành phần {index}/{total_parts} để không vượt giới hạn xử lý."
        )
        unit = _make_unit(split_title, unit_type, chunk, reason)
        if unit:
            units.append(unit)

    return units


def _merge_tiny_units(units: list[PlannedLearningUnit]) -> list[PlannedLearningUnit]:
    merged: list[PlannedLearningUnit] = []
    buffer: list[PlannedLearningUnit] = []

    def flush() -> None:
        if not buffer:
            return
        if len(buffer) == 1:
            merged.append(buffer[0])
        else:
            title = " - ".join(unit.title for unit in buffer[:2])
            source_ids = [section_id for unit in buffer for section_id in unit.source_section_ids]
            source_text = "\n\n".join(unit.source_text for unit in buffer)
            budget = estimate_text_budget(source_text)
            merged.append(
                PlannedLearningUnit(
                    title=title,
                    unit_type="full_group",
                    source_section_ids=source_ids,
                    source_text=source_text,
                    source_text_char_count=budget.char_count,
                    estimated_tokens=budget.estimated_tokens,
                    estimated_audio_seconds=budget.estimated_audio_seconds,
                    planner_reason="Gộp các đề mục ngắn liền kề để tránh audio quá vụn.",
                )
            )
        buffer.clear()

    for unit in units:
        if unit.estimated_tokens < MIN_UNIT_TOKENS:
            buffer.append(unit)
            if sum(item.estimated_tokens for item in buffer) >= MIN_UNIT_TOKENS:
                flush()
            continue
        flush()
        merged.append(unit)
    flush()
    return merged


def _learning_roots(sections: list[BookSection]) -> list[BookSection]:
    children = _children_by_parent(sections)
    roots = children.get(None, [])
    if 1 <= len(roots) <= 60:
        return roots
    return []


def _plan_full_from_roots(roots: list[BookSection], children: dict[uuid.UUID | None, list[BookSection]]) -> list[PlannedLearningUnit]:
    units: list[PlannedLearningUnit] = []
    for root in roots:
        subtree = _subtree_sections(root, children)
        unit = _make_unit(root.title, "full_chapter", subtree, "Full mode giữ đầy đủ nội dung trong cụm mục gốc.")
        if not unit:
            continue
        if unit.estimated_tokens > FULL_UNIT_MAX_TOKENS:
            units.extend(_split_large_group(root.title, subtree, "full_group", max_tokens=FULL_UNIT_MAX_TOKENS))
        else:
            units.append(unit)
    return units


def _plan_full_from_flat_sections(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    units: list[PlannedLearningUnit] = []
    current: list[BookSection] = []
    current_tokens = 0
    for section in sorted(sections, key=lambda item: item.section_index):
        section_tokens = estimate_text_budget(section.text_content or "").estimated_tokens
        if current and current_tokens + section_tokens > FULL_UNIT_TARGET_TOKENS:
            unit = _make_unit(current[0].title, "full_group", current, "Gộp outline phẳng thành bài nghe theo kích thước hợp lý.")
            if unit:
                units.append(unit)
            current = []
            current_tokens = 0
        current.append(section)
        current_tokens += section_tokens
    if current:
        unit = _make_unit(current[0].title, "full_group", current, "Gộp outline phẳng thành bài nghe theo kích thước hợp lý.")
        if unit:
            units.append(unit)
    return units


def plan_full_learning_units(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    if not sections:
        return []

    children = _children_by_parent(sections)
    roots = _learning_roots(sections)
    units = _plan_full_from_roots(roots, children) if roots else _plan_full_from_flat_sections(sections)

    return _merge_tiny_units(units)


async def plan_learning_units_async(sections: list[BookSection], mode: PlanMode | str) -> list[PlannedLearningUnit]:
    mode_value = PlanMode(mode)
    if mode_value == PlanMode.FULL:
        return plan_full_learning_units(sections)

    from app.services.pareto_planner_service import plan_pareto_learning_units
    return await plan_pareto_learning_units(sections)

```

### app\services\live_service.py

```py
import json
import uuid

from livekit import api
from sqlmodel import Session, select

from app.core.config import settings
from app.core.exceptions import BookNotFoundError, ThreadNotFoundError
from app.models.db_models import Book, ChatThread, StudyContext, StudyContextDocumentLink


def _build_livekit_token(room_name: str, metadata: dict) -> dict:
    """
    Helper dùng chung: Tạo AccessToken LiveKit với room config và trả về JWT + room_name.
    """
    agent_dispatch = api.RoomAgentDispatch(
        agent_name=settings.LIVEKIT_AGENT_NAME,
        metadata=json.dumps(metadata),
    )
    room_config = api.RoomConfiguration(
        agents=[agent_dispatch],
        empty_timeout=settings.LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS,
        departure_timeout=settings.LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS,
    )

    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": room_name}


def get_token_for_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """Tạo LiveKit token cho session đọc sách đơn lẻ sau khi kiểm tra ownership."""
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()

    book_id_value = str(book_id)
    session_room_name = f"triam_{book_id_value[:8]}_{uuid.uuid4().hex[:6]}"
    return _build_livekit_token(session_room_name, {"book_id": book_id_value})


def get_token_for_thread(session: Session, thread_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    """Tạo LiveKit token cho session gắn với Study Context thread sau khi kiểm tra ownership."""
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()
    context = session.get(StudyContext, thread.context_id)
    if not context or context.user_id != user_id:
        raise ThreadNotFoundError()

    # Lấy danh sách document_ids từ context
    links = session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == thread.context_id)
    ).all()
    document_ids = [str(link.book_id) for link in links]

    session_room_name = f"triam_{str(thread_id)[:8]}_{uuid.uuid4().hex[:6]}"
    metadata = {
        "thread_id": str(thread_id),
        "context_id": str(thread.context_id),
        "document_ids": document_ids,
    }
    return _build_livekit_token(session_room_name, metadata)

```

### app\services\llm_service.py

```py
import json
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.core.config import settings
from app.core.constant import PlanMode
from app.core.exceptions import LearningUnitTooLargeError, LLMResponseFormatError
from app.core.logger import log as logger
from app.services.async_limiter import get_loop_semaphore
from app.services.chapter_chunking_service import split_text_for_llm
from app.services.token_budget_service import estimate_text_budget, exceeds_hard_limit, should_chunk
from app.services.tts_script_quality_service import inspect_tts_script_quality, sanitize_tts_script_list, sanitize_tts_script_text

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0
)


@dataclass(frozen=True)
class NormalizedUnit:
    main_scripts: list[str]
    review_script: str


class NormalizedUnitPayload(BaseModel):
    main_scripts: list[str] = Field(min_length=1, description="Các đoạn kịch bản nói nối tiếp nhau.")
    review_script: str = Field(min_length=1, description="Nội dung tóm tắt để người học ôn tập.")

    @field_validator("main_scripts")
    @classmethod
    def validate_main_scripts(cls, value: list[str]) -> list[str]:
        scripts = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        if not scripts:
            raise ValueError("main_scripts must contain at least one non-empty string")
        return scripts

    @field_validator("review_script")
    @classmethod
    def validate_review_script(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("review_script must be non-empty")
        return stripped


COMMON_TTS_REWRITE_RULES = """
You are TRIAM's audiobook editor. Convert raw textbook text into clean Vietnamese spoken scripts for Text-to-Speech.

Global rules:
- Preserve the source meaning. Do not invent facts, scores, definitions, citations, or claims.
- Write natural Vietnamese speech for listeners, not visual text for readers.
- Every string value must be plain spoken text. Never output Markdown, headings, bullets, tables, inline code marks, visual emphasis, citation markers, page numbers, headers, or footers.
- Convert visual emphasis into normal speech. For example, a visually highlighted concept should become ordinary words in the sentence, with no symbols.
- Repair PDF/DOCX extraction noise: broken lines, repeated headers, footers, page numbers, table separators, and stray formatting symbols.
- Convert numbers, years, percentages, currencies, and common symbols into Vietnamese spoken form when this improves listening.
- First-use terminology rule: for any acronym, initialism, symbol, benchmark, method name, or domain-specific abbreviation, briefly explain it the first time it appears in the same learning unit.
- Prefer the source's own parenthetical explanation or expansion when available.
- If the exact expansion is uncertain, explain the term's role neutrally instead of guessing.
- After a term has been explained once in the same learning unit, you may use the short form to keep audio concise.
- The review script may be heard separately later, so explain essential abbreviations again there.
- Split main_scripts into coherent spoken paragraphs of about 3-5 sentences or one complete idea each. Do not prefix them with labels such as "Segment", "Part", or "Next".
- Ensure the scripts sound continuous when played in order.

Return only a valid JSON object:
{
  "main_scripts": ["spoken paragraph 1", "spoken paragraph 2"],
  "review_script": "spoken review summary"
}
"""

SYSTEM_PROMPT_REWRITE_FULL = (
    COMMON_TTS_REWRITE_RULES
    + """

Mode: FULL.
- Keep the learning unit's content complete and faithful.
- Do not over-summarize. Preserve definitions, arguments, conditions, examples that explain the concept, and important transitions.
- You may make dense textbook prose easier to hear, but keep the author's logic and scope.
- review_script: 100-150 Vietnamese words, summarizing 3-5 core ideas in spoken form.

Input: raw textbook text.
Output: valid JSON only.
"""
)

SYSTEM_PROMPT_REWRITE_PARETO = (
    COMMON_TTS_REWRITE_RULES
    + """

Mode: PARETO.
- Select the smallest set of ideas that gives the learner the highest understanding value.
- Keep definitions, central claims, formulas, rules, methods, causal relationships, and important comparison criteria.
- Remove side stories, long examples, repeated evidence, and low-value details unless they are needed to understand a retained idea.
- Do not keep a dense list of names, benchmarks, acronyms, or scores only because they appear in the source. Group them into a broader spoken idea when the exact items are not essential.
- If a benchmark, acronym, score, or technical name is retained because it is important, explain it at first use using the global first-use terminology rule.
- review_script: about 100 Vietnamese words, focused on the most useful recall points.

Input: raw textbook text.
Output: valid JSON only.
"""
)


# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------


def _prompt_for_mode(mode: str) -> str:
    if mode.lower() == PlanMode.PARETO.value:
        return SYSTEM_PROMPT_REWRITE_PARETO
    return SYSTEM_PROMPT_REWRITE_FULL


def _validate_normalized_payload(payload: dict) -> NormalizedUnit:
    try:
        parsed = NormalizedUnitPayload.model_validate(payload)
    except ValidationError as exc:
        raise LLMResponseFormatError("LLM response không khớp schema JSON yêu cầu.") from exc
    return NormalizedUnit(
        main_scripts=parsed.main_scripts,
        review_script=parsed.review_script,
    )


def _extract_json_object(content: str) -> dict:
    raw = content.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(raw[start : end + 1])


def _coerce_normalized_response(parsed_payload: NormalizedUnitPayload | None, content: str | None) -> NormalizedUnit:
    if parsed_payload is not None:
        return NormalizedUnit(
            main_scripts=parsed_payload.main_scripts,
            review_script=parsed_payload.review_script,
        )

    if not content:
        raise LLMResponseFormatError("LLM response rỗng.")

    try:
        parsed_data = _extract_json_object(content)
    except json.JSONDecodeError as exc:
        raise LLMResponseFormatError("LLM response không phải JSON hợp lệ.") from exc
    return _validate_normalized_payload(parsed_data)


def _sanitize_normalized_unit(unit: NormalizedUnit) -> NormalizedUnit:
    return NormalizedUnit(
        main_scripts=sanitize_tts_script_list(unit.main_scripts),
        review_script=sanitize_tts_script_text(unit.review_script),
    )


def _log_tts_quality_report(unit: NormalizedUnit, *, mode: str, request_context: str, request_chars: int) -> None:
    report = inspect_tts_script_quality([*unit.main_scripts, unit.review_script])
    if not report.has_warnings:
        return

    log_message = (
        "LLM normalize quality warnings | "
        f"mode={mode} | context={request_context} | chars={request_chars} | "
        f"markdown_artifacts={report.markdown_artifacts} | "
        f"unexplained_acronyms={list(report.unexplained_acronyms)}"
    )
    if report.markdown_artifacts:
        logger.warning(log_message)
    else:
        logger.info(log_message)


async def _call_normalize_llm(text: str, mode: str, *, context_hint: str | None = None) -> NormalizedUnit:
    mode_prompt = _prompt_for_mode(mode)
    user_content = text if not context_hint else f"{context_hint}\n\n--- INPUT ---\n{text}"
    request_chars = len(user_content)
    request_context = "chunk" if context_hint else "single"

    last_format_error: Exception | None = None
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        async with get_loop_semaphore("llm_normalize", settings.LLM_NORMALIZE_CONCURRENCY):
            logger.info(f"LLM normalize start | mode={mode} | context={request_context} | chars={request_chars} | attempt={attempt}/{max_attempts}")
            try:
                response = await client.beta.chat.completions.parse(
                    model=settings.GEMINI_MODEL_LLM,
                    messages=[
                        {"role": "system", "content": mode_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.2,
                    response_format=NormalizedUnitPayload,
                )
                message = response.choices[0].message
                normalized = _coerce_normalized_response(message.parsed, message.content)
                _log_tts_quality_report(normalized, mode=mode, request_context=request_context, request_chars=request_chars)
                normalized = _sanitize_normalized_unit(normalized)
                logger.info(f"LLM normalize done | mode={mode} | context={request_context} | scripts={len(normalized.main_scripts)} | review_chars={len(normalized.review_script)}")
                return normalized
            except LLMResponseFormatError as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize returned invalid structured output | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")
            except (ValidationError, ValueError, json.JSONDecodeError) as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize schema validation failed | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")

    raise LLMResponseFormatError("LLM response không phải JSON hợp lệ sau khi thử lại.") from last_format_error


async def normalize_text_for_speech(raw_text: str, mode: str, *, unit_title: str | None = None, chapter_title: str | None = None) -> dict:
    """
    Gửi text thô cho Gemini để biên tập và cấu trúc lại thành TTS script.

    Returns:
        {"main_scripts": [...], "review_script": "..."}

    Raises:
        Exception: Nếu LLM call thất bại hoặc response không parse được —
                   caller (learning_unit_tts_worker) chịu trách nhiệm rollback unit.
    """
    title = unit_title or chapter_title
    budget = estimate_text_budget(raw_text)
    logger.info(
        f"Normalize preflight | mode={mode} | title={title or '(unknown)'} | "
        f"chars={budget.char_count} | estimated_tokens={budget.estimated_tokens} | "
        f"estimated_audio_seconds={budget.estimated_audio_seconds}"
    )
    if exceeds_hard_limit(budget):
        raise LearningUnitTooLargeError(f"Bài học quá lớn: khoảng {budget.estimated_tokens} tokens, vượt giới hạn {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens.")

    if not should_chunk(budget):
        logger.info(f"Normalize strategy | mode={mode} | strategy=single_call | title={title or '(unknown)'}")
        normalized = await _call_normalize_llm(raw_text, mode)
        return {
            "main_scripts": normalized.main_scripts,
            "review_script": normalized.review_script,
        }

    chunks = split_text_for_llm(raw_text)
    logger.info(f"Normalize long unit with {len(chunks)} chunks | mode={mode} | title={title or '(unknown)'} | estimated_tokens={budget.estimated_tokens}")

    all_scripts: list[str] = []
    review_parts: list[str] = []
    previous_tail = ""

    for chunk in chunks:
        logger.info(f"Normalize chunk start | mode={mode} | title={title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | estimated_tokens={chunk.estimated_tokens}")
        context_hint = (
            f"Bài học: {title or 'Không rõ'}.\n"
            f"Đây là phần {chunk.index + 1}/{len(chunks)} của cùng một bài học.\n"
            "Giữ mạch văn nối tiếp với phần trước. Không tự nhắc 'phần' hoặc 'chunk' trong câu trả lời.\n"
            f"Đoạn cuối phần trước để nối ngữ cảnh: {previous_tail[-600:]}"
        )
        normalized = await _call_normalize_llm(chunk.text, mode, context_hint=context_hint)
        all_scripts.extend(normalized.main_scripts)
        if normalized.review_script:
            review_parts.append(normalized.review_script)
        previous_tail = chunk.text[-1000:]
        logger.info(f"Normalize chunk done | mode={mode} | title={title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | cumulative_scripts={len(all_scripts)}")

    return {
        "main_scripts": all_scripts,
        "review_script": " ".join(review_parts).strip(),
    }

```

### app\services\notification_copy_service.py

```py
from app.core.constant import NotificationType


def build_notification_copy(notification_type: NotificationType, payload: dict) -> tuple[str, str]:
    match notification_type:
        case NotificationType.PLAN_REMINDER:
            if payload.get("subtype") == "missed_session":
                return (
                    "Bạn đã lỡ một buổi học",
                    f"Có thể học bù {payload.get('book_title', 'sách của bạn')} khi bạn rảnh.",
                )
            return (
                "Đến giờ học rồi",
                f"Tiếp tục nghe {payload.get('book_title', 'sách của bạn')} nhé.",
            )
        case NotificationType.CONTENT_READY:
            subtype = payload.get("subtype")
            book_title = payload.get("book_title", "sách của bạn")
            if subtype == "first_playable":
                return (
                    "Có thể bắt đầu nghe rồi",
                    f"{book_title} đã có nội dung đầu tiên sẵn sàng.",
                )
            if subtype == "book_ready":
                return (
                    "Sách đã sẵn sàng",
                    f"{book_title} đã được xử lý xong.",
                )
            return (
                "Nội dung đã sẵn sàng",
                payload.get("message", "Bạn đã có nội dung mới để nghe trong TRIAM."),
            )
        case NotificationType.SPACED_REVIEW_DUE:
            unit_title = payload.get("unit_title") or "một bài học đã học"
            return (
                "Đến lúc ôn lại rồi",
                f"Ôn nhanh: {unit_title}.",
            )
    return ("TRIAM", "Bạn có một thông báo mới.")

```

### app\services\notification_event_service.py

```py
import json
import uuid
from datetime import datetime

from sqlalchemy.orm.exc import ObjectDeletedError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import (
    BookStatus,
    LearningProgressStatus,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
    PlanMode,
    ReadingPlanSessionStatus,
    ReviewItemStatus,
)
from app.core.logger import log
from app.models.db_models import (
    Book,
    LearningUnit,
    LearningUnitProgress,
    NotificationOutbox,
    ReadingPlanSession,
    SpacedReviewItem,
    UserNotification,
)
from app.repositories.learning_progress_repo import has_playable_uncompleted_unit, has_studied_book_between
from app.repositories.notification_outbox_repo import (
    count_outbox_for_user_between,
    create_outbox_once,
    get_outbox_by_idempotency_key,
    mark_outbox_sent,
)
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.reading_plan_session_repo import list_due_reminder_sessions, list_missed_sessions_pending_notification
from app.repositories.spaced_review_repo import defer_review_item, get_due_review_items, mark_review_item_due
from app.repositories.user_notification_repo import create_user_notification_once
from app.services.fcm_service import send_fcm_notification
from app.services.notification_copy_service import build_notification_copy
from app.services.reminder_schedule_service import (
    local_day_bounds_utc,
    shift_out_of_quiet_hours,
    to_local,
)


def _daily_cap_available(session: Session, *, user_id: uuid.UUID, due_at: datetime, user_settings) -> bool:
    if user_settings.daily_cap <= 0:
        return False

    local_due = to_local(due_at, user_settings.timezone)
    start_utc, end_utc = local_day_bounds_utc(local_due.date(), user_settings.timezone)
    existing_count = count_outbox_for_user_between(
        session,
        user_id=user_id,
        start_utc=start_utc,
        end_utc=end_utc,
    )
    return existing_count < user_settings.daily_cap


def _adjust_due_time(session: Session, *, user_id: uuid.UUID, due_at: datetime) -> datetime | None:
    user_settings = get_or_create_notification_settings(session, user_id)
    shifted_due_at = shift_out_of_quiet_hours(
        due_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if not _daily_cap_available(session, user_id=user_id, due_at=shifted_due_at, user_settings=user_settings):
        return None
    return shifted_due_at


def create_content_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    learning_unit_id: uuid.UUID,
    unit_title: str,
    mode: PlanMode | str,
    due_at: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=due_at)
    if adjusted_due_at is None:
        log.info(
            f"Skip content-ready notification because daily cap is reached | "
            f"user_id={user_id} | learning_unit_id={learning_unit_id}"
        )
        return None

    payload = {
        "book_id": str(book_id),
        "book_title": book_title,
        "learning_unit_id": str(learning_unit_id),
        "unit_title": unit_title,
        "mode": mode_value,
        "message": f"{unit_title} đã sẵn sàng để nghe.",
        "action_type": "open_learning_unit",
        "action_payload": {
            "book_id": str(book_id),
            "learning_unit_id": str(learning_unit_id),
            "mode": mode_value,
        },
    }
    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:{user_id}:{learning_unit_id}:{mode_value}",
        ),
    )


def create_first_playable_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    mode: PlanMode | str,
    now: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=now)
    if adjusted_due_at is None:
        return None

    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload={
                "subtype": "first_playable",
                "book_id": str(book_id),
                "book_title": book_title,
                "mode": mode_value,
                "action_type": "open_book",
                "action_payload": {
                    "book_id": str(book_id),
                    "mode": mode_value,
                },
            },
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:first-playable:{user_id}:{book_id}:{mode_value}",
        ),
    )


def create_book_ready_outbox_once(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    mode: PlanMode | str,
    now: datetime,
) -> NotificationOutbox | None:
    mode_value = PlanMode(mode).value
    adjusted_due_at = _adjust_due_time(session, user_id=user_id, due_at=now)
    if adjusted_due_at is None:
        return None

    return create_outbox_once(
        session,
        NotificationOutbox(
            user_id=user_id,
            type=NotificationType.CONTENT_READY,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload={
                "subtype": "book_ready",
                "book_id": str(book_id),
                "book_title": book_title,
                "mode": mode_value,
                "action_type": "open_book",
                "action_payload": {
                    "book_id": str(book_id),
                    "mode": mode_value,
                },
            },
            due_at=adjusted_due_at,
            idempotency_key=f"content-ready:book-ready:{user_id}:{book_id}:{mode_value}",
        ),
    )


def _build_review_outbox(session: Session, review_item: SpacedReviewItem, *, now: datetime) -> NotificationOutbox | None:
    user_settings = get_or_create_notification_settings(session, review_item.user_id)
    if not user_settings.spaced_review_enabled:
        return None

    progress = None
    if review_item.source_unit_progress_id:
        progress = session.get(LearningUnitProgress, review_item.source_unit_progress_id)
    if not progress and review_item.learning_unit_id:
        progress = session.exec(
            select(LearningUnitProgress).where(
                LearningUnitProgress.user_id == review_item.user_id,
                LearningUnitProgress.learning_unit_id == review_item.learning_unit_id,
                LearningUnitProgress.mode == review_item.mode,
                LearningUnitProgress.status == LearningProgressStatus.COMPLETED,
            )
        ).first()
    if not progress or progress.status != LearningProgressStatus.COMPLETED:
        review_item.status = ReviewItemStatus.CANCELLED
        review_item.updated_at = now
        session.add(review_item)
        session.commit()
        return None

    due_at = shift_out_of_quiet_hours(
        review_item.due_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if due_at > now:
        defer_review_item(session, review_item, due_at)
        return None
    if not _daily_cap_available(session, user_id=review_item.user_id, due_at=due_at, user_settings=user_settings):
        return None

    unit = session.get(LearningUnit, review_item.learning_unit_id) if review_item.learning_unit_id else None
    book = session.get(Book, review_item.book_id)
    idempotency_key = f"spaced-review:{review_item.id}"
    payload = {
        "book_id": str(review_item.book_id),
        "book_title": book.title if book else "sách của bạn",
        "learning_unit_id": str(review_item.learning_unit_id) if review_item.learning_unit_id else None,
        "unit_title": unit.title if unit else "một bài học đã học",
        "review_item_id": str(review_item.id),
        "mode": review_item.mode.value,
        "interval_days": review_item.interval_days,
        "action_type": "open_review",
        "action_payload": {
            "book_id": str(review_item.book_id),
            "learning_unit_id": str(review_item.learning_unit_id) if review_item.learning_unit_id else None,
            "review_item_id": str(review_item.id),
            "mode": review_item.mode.value,
        },
    }
    outbox = create_outbox_once(
        session,
        NotificationOutbox(
            user_id=review_item.user_id,
            type=NotificationType.SPACED_REVIEW_DUE,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=due_at,
            idempotency_key=idempotency_key,
        ),
    )
    if outbox or get_outbox_by_idempotency_key(session, idempotency_key):
        mark_review_item_due(session, review_item)
    return outbox


def create_due_review_outbox_rows(session: Session, *, now: datetime) -> int:
    created_count = 0
    for review_item in get_due_review_items(session, now=now, limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE * 2):
        try:
            if _build_review_outbox(session, review_item, now=now):
                created_count += 1
        except ObjectDeletedError:
            session.rollback()
            log.warning(f"Review item was deleted concurrently during scan | review_item_id={getattr(review_item, 'id', 'unknown')}")
            continue
    return created_count


def _build_plan_session_reminder_outbox(
    session: Session,
    plan_session: ReadingPlanSession,
    book: Book,
    *,
    now: datetime,
) -> NotificationOutbox | None:
    user_settings = get_or_create_notification_settings(session, plan_session.user_id)
    if not user_settings.reminders_enabled:
        return None
    if not has_playable_uncompleted_unit(session, user_id=plan_session.user_id, book_id=book.id, mode=plan_session.mode):
        return None

    local_scheduled = to_local(plan_session.scheduled_at, plan_session.timezone)
    start_utc, end_utc = local_day_bounds_utc(local_scheduled.date(), plan_session.timezone)
    if has_studied_book_between(
        session,
        user_id=plan_session.user_id,
        book_id=book.id,
        mode=plan_session.mode,
        start_utc=start_utc,
        end_utc=end_utc,
    ):
        return None

    due_at = shift_out_of_quiet_hours(
        plan_session.scheduled_at,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if due_at > now:
        return None
    if not _daily_cap_available(session, user_id=plan_session.user_id, due_at=due_at, user_settings=user_settings):
        return None

    payload = {
        "book_id": str(book.id),
        "book_title": book.title,
        "plan_id": str(plan_session.plan_id),
        "session_id": str(plan_session.id),
        "session_index": plan_session.session_index,
        "mode": plan_session.mode.value,
        "local_date": plan_session.local_date,
        "action_type": "open_plan_session",
        "action_payload": {
            "book_id": str(book.id),
            "plan_id": str(plan_session.plan_id),
            "session_id": str(plan_session.id),
            "mode": plan_session.mode.value,
        },
    }
    idempotency_key = f"plan-session:{plan_session.user_id}:{plan_session.id}:{plan_session.local_date}"
    outbox = create_outbox_once(
        session,
        NotificationOutbox(
            user_id=plan_session.user_id,
            type=NotificationType.PLAN_REMINDER,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=due_at,
            idempotency_key=idempotency_key,
        ),
    )
    if outbox or get_outbox_by_idempotency_key(session, idempotency_key):
        plan_session.status = ReadingPlanSessionStatus.DUE.value
        plan_session.updated_at = now
        session.add(plan_session)
        session.commit()
    return outbox


def _create_due_plan_session_reminder_outbox_rows(session: Session, *, now: datetime) -> int:
    created_count = 0
    sessions = list_due_reminder_sessions(
        session,
        now=now,
        limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE * 2,
    )
    for plan_session in sessions:
        try:
            book = session.get(Book, plan_session.book_id)
            if not book or book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
                continue
            if _build_plan_session_reminder_outbox(session, plan_session, book, now=now):
                created_count += 1
        except ObjectDeletedError:
            session.rollback()
            log.warning(f"Reading plan session was deleted concurrently during scan | session_id={plan_session.id}")
            continue
    return created_count


def _build_missed_plan_session_outbox(
    session: Session,
    plan_session: ReadingPlanSession,
    book: Book,
    *,
    now: datetime,
) -> NotificationOutbox | None:
    user_settings = get_or_create_notification_settings(session, plan_session.user_id)
    if not user_settings.reminders_enabled:
        plan_session.missed_notified_at = plan_session.missed_notified_at or now
        plan_session.updated_at = now
        session.add(plan_session)
        session.commit()
        return None

    if has_studied_book_between(
        session,
        user_id=plan_session.user_id,
        book_id=book.id,
        mode=plan_session.mode,
        start_utc=plan_session.scheduled_at,
        end_utc=now,
    ):
        plan_session.missed_notified_at = plan_session.missed_notified_at or now
        plan_session.updated_at = now
        session.add(plan_session)
        session.commit()
        return None

    reminder_key = f"plan-session:{plan_session.user_id}:{plan_session.id}:{plan_session.local_date}"
    if get_outbox_by_idempotency_key(session, reminder_key):
        plan_session.missed_notified_at = plan_session.missed_notified_at or now
        plan_session.updated_at = now
        session.add(plan_session)
        session.commit()
        return None

    due_at = shift_out_of_quiet_hours(
        now,
        user_settings.timezone,
        user_settings.quiet_hours_start,
        user_settings.quiet_hours_end,
    )
    if not _daily_cap_available(session, user_id=plan_session.user_id, due_at=due_at, user_settings=user_settings):
        return None

    payload = {
        "subtype": "missed_session",
        "book_id": str(book.id),
        "book_title": book.title,
        "plan_id": str(plan_session.plan_id),
        "session_id": str(plan_session.id),
        "session_index": plan_session.session_index,
        "mode": plan_session.mode.value,
        "local_date": plan_session.local_date,
        "action_type": "open_plan_session",
        "action_payload": {
            "book_id": str(book.id),
            "plan_id": str(plan_session.plan_id),
            "session_id": str(plan_session.id),
            "mode": plan_session.mode.value,
        },
    }
    idempotency_key = f"missed-session:{plan_session.user_id}:{plan_session.id}"
    outbox = create_outbox_once(
        session,
        NotificationOutbox(
            user_id=plan_session.user_id,
            type=NotificationType.PLAN_REMINDER,
            channel=NotificationChannel.ALL,
            status=NotificationStatus.PENDING,
            payload=payload,
            due_at=due_at,
            idempotency_key=idempotency_key,
        ),
    )
    if outbox or get_outbox_by_idempotency_key(session, idempotency_key):
        plan_session.missed_notified_at = plan_session.missed_notified_at or now
        plan_session.updated_at = now
        session.add(plan_session)
        session.commit()
    return outbox


def create_missed_plan_session_outbox_rows(session: Session, *, now: datetime) -> int:
    created_count = 0
    sessions = list_missed_sessions_pending_notification(
        session,
        now=now,
        limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE * 2,
    )
    for plan_session in sessions:
        try:
            book = session.get(Book, plan_session.book_id)
            if not book or book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
                plan_session.missed_notified_at = plan_session.missed_notified_at or now
                plan_session.updated_at = now
                session.add(plan_session)
                session.commit()
                continue
            if _build_missed_plan_session_outbox(session, plan_session, book, now=now):
                created_count += 1
        except ObjectDeletedError:
            session.rollback()
            log.warning(f"Reading plan session was deleted concurrently during missed scan | session_id={plan_session.id}")
            continue
    return created_count


def create_due_plan_reminder_outbox_rows(session: Session, *, now: datetime) -> int:
    return _create_due_plan_session_reminder_outbox_rows(session, now=now) + create_missed_plan_session_outbox_rows(session, now=now)


def deliver_outbox_notification(session: Session, outbox: NotificationOutbox, *, now: datetime) -> None:
    title, body = build_notification_copy(outbox.type, outbox.payload)

    # 1. In-app Delivery
    if outbox.channel in (NotificationChannel.IN_APP, NotificationChannel.ALL):
        notification = UserNotification(
            user_id=outbox.user_id,
            outbox_id=outbox.id,
            type=outbox.type,
            title=title,
            body=body,
            action_type=outbox.payload.get("action_type"),
            action_payload=outbox.payload.get("action_payload"),
        )
        create_user_notification_once(session, notification)

    # 2. Push/FCM Delivery
    if outbox.channel in (NotificationChannel.PUSH, NotificationChannel.ALL):
        fcm_data = {}
        if outbox.payload.get("action_type"):
            fcm_data["action_type"] = outbox.payload["action_type"]
        if outbox.payload.get("action_payload"):
            fcm_data["action_payload"] = json.dumps(outbox.payload["action_payload"])

        fcm_data["outbox_id"] = str(outbox.id)
        fcm_data["notification_type"] = outbox.type.value

        send_fcm_notification(session, user_id=outbox.user_id, title=title, body=body, data=fcm_data)

    mark_outbox_sent(session, outbox, now=now)

```

### app\services\notification_service.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import NotificationNotFoundError
from app.repositories.notification_settings_repo import get_or_create_notification_settings, update_notification_settings
from app.repositories.user_notification_repo import (
    count_unread_notifications,
    get_user_notification,
    list_user_notifications,
    mark_all_notifications_read,
    mark_notification_read,
)
from app.schemas.notification import NotificationSettingsRequest

MAX_NOTIFICATION_LIST_LIMIT = 100
DEFAULT_NOTIFICATION_LIST_LIMIT = 30


def get_settings(session: Session, user_id: uuid.UUID):
    return get_or_create_notification_settings(session, user_id)


def update_settings(session: Session, user_id: uuid.UUID, payload: NotificationSettingsRequest):
    return update_notification_settings(
        session,
        user_id,
        timezone_name=payload.timezone,
        reminders_enabled=payload.reminders_enabled,
        spaced_review_enabled=payload.spaced_review_enabled,
        reminder_time=payload.reminder_time,
        quiet_hours_start=payload.quiet_hours_start,
        quiet_hours_end=payload.quiet_hours_end,
        daily_cap=payload.daily_cap,
    )


def list_notifications(
    session: Session,
    user_id: uuid.UUID,
    *,
    limit: int = DEFAULT_NOTIFICATION_LIST_LIMIT,
    unread_only: bool = False,
) -> dict:
    safe_limit = max(1, min(limit, MAX_NOTIFICATION_LIST_LIMIT))
    items = list_user_notifications(session, user_id=user_id, limit=safe_limit, unread_only=unread_only)
    unread_count = count_unread_notifications(session, user_id=user_id)
    return {"items": items, "unread_count": unread_count}


def read_notification(session: Session, user_id: uuid.UUID, notification_id: uuid.UUID) -> dict:
    notification = get_user_notification(session, user_id=user_id, notification_id=notification_id)
    if not notification:
        raise NotificationNotFoundError()

    read_at = datetime.now(timezone.utc)
    saved = mark_notification_read(session, notification, read_at=read_at)
    return {"id": saved.id, "read_at": saved.read_at}


def read_all_notifications(session: Session, user_id: uuid.UUID) -> dict:
    read_at = datetime.now(timezone.utc)
    updated_count = mark_all_notifications_read(session, user_id=user_id, read_at=read_at)
    return {"updated_count": updated_count, "read_at": read_at}

```

### app\services\pareto_planner_service.py

```py
from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import BookSection, BookSectionKnowledge
from app.services.async_limiter import get_loop_semaphore
from app.services.learning_unit_planner_service import PlannedLearningUnit
from app.services.pareto_signal_service import (
    extract_pareto_signal_hints,
    get_or_create_anchor_embeddings,
)
from app.services.token_budget_service import estimate_text_budget

client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0
)

PARETO_PLANNER_SYSTEM_PROMPT = """
You are TRIAM's Pareto learning planner.
Your job is not to summarize the book.
Your job is to select and group the vital few source sections that give the learner the highest understanding value.

Rules:
- Return only valid JSON matching the requested schema.
- Section titles may be Vietnamese, English, or mixed-language.
- Use the original document language when naming learning units unless the source title is unclear.
- Treat signal_hints as helpful hints, not strict rules.
- Prefer structurally important sections even when there are no obvious keywords.
- Select 3 to 8 learning units unless the document is very small.
- Prefer foundational definitions, principles, formulas, methods, procedures, and representative examples.
- Merge small related sections into one coherent learning unit.
- Preserve the source order inside each unit.
- Do not invent section ids.
- Do not create audio script content.
- Do not include sections that are only decorative, repetitive, or minor examples unless they are necessary to understand a core idea.
- Each unit must explain why it was selected.
""".strip()


@dataclass(frozen=True)
class SectionCard:
    section_id: uuid.UUID
    title: str
    path: str
    level: int
    parent_path: str | None
    section_index: int
    text_char_count: int
    estimated_tokens: int
    child_count: int
    signal_hints: list[str]
    excerpt: str

    def to_prompt_dict(self) -> dict:
        return {
            "id": str(self.section_id),
            "title": self.title,
            "path": self.path,
            "level": self.level,
            "parent_path": self.parent_path,
            "estimated_tokens": self.estimated_tokens,
            "child_count": self.child_count,
            "signal_hints": self.signal_hints,
            "excerpt": self.excerpt,
        }


class ParetoPlannedUnitPayload(BaseModel):
    title: str = Field(min_length=3)
    source_section_ids: list[str] = Field(min_length=1)
    unit_type: str = Field(min_length=3)
    importance_score: int = Field(ge=1, le=5)
    learning_objective: str = Field(min_length=10)
    planner_reason: str = Field(min_length=10)

    @field_validator("source_section_ids")
    @classmethod
    def validate_source_section_ids(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for item in value:
            try:
                cleaned.append(str(uuid.UUID(str(item))))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid section id: {item}") from exc
        return cleaned


class ParetoPlannerPayload(BaseModel):
    units: list[ParetoPlannedUnitPayload] = Field(min_length=1)


def _children_by_parent(sections: list[BookSection]) -> dict[uuid.UUID | None, list[BookSection]]:
    children: dict[uuid.UUID | None, list[BookSection]] = {}
    for section in sorted(sections, key=lambda item: item.section_index):
        children.setdefault(section.parent_id, []).append(section)
    return children


def _excerpt(text: str | None) -> str:
    normalized = " ".join((text or "").split())
    limit = max(100, settings.PARETO_SECTION_EXCERPT_CHARS)
    return normalized[:limit]


def build_section_cards(sections: list[BookSection], anchor_vectors: dict[str, list[float]] | None = None) -> list[SectionCard]:
    by_id = {section.id: section for section in sections}
    children = _children_by_parent(sections)
    cards: list[SectionCard] = []

    # 1. Truy vấn một lần duy nhất tất cả embeddings có sẵn của cuốn sách trong database
    embeddings_map = {}
    if sections:
        book_id = sections[0].book_id
        with Session(engine) as session:
            rows = session.exec(
                select(BookSectionKnowledge.section_id, BookSectionKnowledge.embedding)
                .where(
                    BookSectionKnowledge.book_id == book_id,
                    BookSectionKnowledge.embedding_version == settings.BOOK_SECTION_EMBEDDING_VERSION
                )
            ).all()
            embeddings_map = {row[0]: row[1] for row in rows if row[1] is not None}

    # 2. Xây dựng danh sách SectionCard
    for section in sorted(sections, key=lambda item: item.section_index):
        text = section.text_content or ""
        excerpt = _excerpt(text)
        budget = estimate_text_budget(text)
        parent = by_id.get(section.parent_id) if section.parent_id else None
        
        # Tìm vector của section hiện tại
        embedding = embeddings_map.get(section.id)
        
        cards.append(
            SectionCard(
                section_id=section.id,
                title=section.title,
                path=section.path,
                level=section.level,
                parent_path=parent.path if parent else None,
                section_index=section.section_index,
                text_char_count=section.text_char_count,
                estimated_tokens=budget.estimated_tokens,
                child_count=len(children.get(section.id, [])),
                signal_hints=extract_pareto_signal_hints(
                    embedding=embedding, anchor_vectors=anchor_vectors
                ),
                excerpt=excerpt,
            )
        )

    return cards[: max(1, settings.PARETO_PLANNER_MAX_SECTION_CARDS)]


def _prompt_user_content(cards: list[SectionCard]) -> str:
    total_tokens = sum(card.estimated_tokens for card in cards)
    payload = {
        "mode": "pareto",
        "target_coverage_ratio": settings.PARETO_TARGET_COVERAGE_RATIO,
        "target_tokens": int(total_tokens * settings.PARETO_TARGET_COVERAGE_RATIO),
        "min_units": settings.PARETO_PLANNER_MIN_UNITS,
        "max_units": settings.PARETO_PLANNER_MAX_UNITS,
        "section_cards": [card.to_prompt_dict() for card in cards],
    }
    return json.dumps(payload, ensure_ascii=False)


def _coerce_planner_response(parsed_payload: ParetoPlannerPayload | None, content: str | None) -> ParetoPlannerPayload:
    if parsed_payload is not None:
        return parsed_payload
    if not content:
        raise ValueError("Empty Pareto planner response")
    return ParetoPlannerPayload.model_validate(json.loads(content))


async def _call_pareto_llm(cards: list[SectionCard]) -> ParetoPlannerPayload:
    async with get_loop_semaphore("pareto_planner", 1):
        response = await client.beta.chat.completions.parse(
            model=settings.PARETO_PLANNER_MODEL,
            messages=[
                {"role": "system", "content": PARETO_PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": _prompt_user_content(cards)},
            ],
            temperature=0.1,
            response_format=ParetoPlannerPayload,
        )
    message = response.choices[0].message
    return _coerce_planner_response(message.parsed, message.content)


def _sections_by_id(sections: list[BookSection]) -> dict[uuid.UUID, BookSection]:
    return {section.id: section for section in sections}


def _make_planned_unit_from_payload(
    payload: ParetoPlannedUnitPayload,
    *,
    sections_by_id: dict[uuid.UUID, BookSection],
) -> PlannedLearningUnit | None:
    source_sections: list[BookSection] = []
    seen: set[uuid.UUID] = set()
    for raw_id in payload.source_section_ids:
        section_id = uuid.UUID(raw_id)
        if section_id in seen:
            continue
        section = sections_by_id.get(section_id)
        if not section:
            continue
        source_sections.append(section)
        seen.add(section_id)

    source_sections.sort(key=lambda item: item.section_index)
    source_text_parts = [section.text_content.strip() for section in source_sections if section.text_content and section.text_content.strip()]
    source_text = "\n\n".join(source_text_parts).strip()
    if not source_text:
        return None

    budget = estimate_text_budget(source_text)
    reason = (
        f"{payload.planner_reason.strip()} "
        f"Mục tiêu học: {payload.learning_objective.strip()} "
        f"Điểm quan trọng: {payload.importance_score}/5."
    )
    return PlannedLearningUnit(
        title=payload.title.strip(),
        unit_type=payload.unit_type.strip() or "pareto_core",
        source_section_ids=[section.id for section in source_sections],
        source_text=source_text,
        source_text_char_count=budget.char_count,
        estimated_tokens=budget.estimated_tokens,
        estimated_audio_seconds=budget.estimated_audio_seconds,
        planner_reason=reason,
    )


def _trim_to_target(units: list[PlannedLearningUnit], *, total_source_tokens: int) -> list[PlannedLearningUnit]:
    if len(units) <= settings.PARETO_PLANNER_MIN_UNITS:
        return units

    target_tokens = max(1, int(total_source_tokens * settings.PARETO_TARGET_COVERAGE_RATIO))
    selected: list[PlannedLearningUnit] = []
    selected_tokens = 0

    for unit in units[: settings.PARETO_PLANNER_MAX_UNITS]:
        selected.append(unit)
        selected_tokens += unit.estimated_tokens
        if len(selected) >= settings.PARETO_PLANNER_MIN_UNITS and selected_tokens >= target_tokens:
            break

    return selected


def _validate_planner_payload(payload: ParetoPlannerPayload, sections: list[BookSection]) -> list[PlannedLearningUnit]:
    sections_by_id = _sections_by_id(sections)
    total_source_tokens = sum(estimate_text_budget(section.text_content or "").estimated_tokens for section in sections)
    units: list[PlannedLearningUnit] = []
    for unit_payload in payload.units:
        unit = _make_planned_unit_from_payload(unit_payload, sections_by_id=sections_by_id)
        if unit:
            units.append(unit)

    units.sort(key=lambda unit: min(sections_by_id[section_id].section_index for section_id in unit.source_section_ids))
    return _trim_to_target(units, total_source_tokens=total_source_tokens)


async def plan_pareto_learning_units(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    if not sections:
        return []

    # 1. Tải các Vector Neo bất đồng bộ từ OpenAI (Cache in-memory)
    anchor_vectors = await get_or_create_anchor_embeddings()

    # 2. Tạo section cards truyền kèm anchor_vectors
    cards = build_section_cards(sections, anchor_vectors)

    # 3. Gọi trực tiếp LLM để lập kế hoạch, nếu lỗi sẽ Fail-fast ném lỗi lên API
    log.info(f"Pareto planner start | sections={len(sections)} | cards={len(cards)}")
    
    payload = await asyncio.wait_for(
        _call_pareto_llm(cards), 
        timeout=settings.PARETO_PLANNER_TIMEOUT_SECONDS
    )
    
    planned_units = _validate_planner_payload(payload, sections)
    if not planned_units:
        raise ValueError("Pareto planner returned no valid learning units")
        
    log.info(f"Pareto planner result | source=llm | units={len(planned_units)}")
    return planned_units

```

### app\services\pareto_signal_service.py

```py
from __future__ import annotations

import numpy as np
from openai import AsyncOpenAI

from app.core.config import settings

# 1. Định nghĩa bộ neo ngữ nghĩa mô tả mẫu (Label Enrichment)
ENRICHED_ANCHORS: dict[str, str] = {
    "core_concept": (
        "Khái niệm nền tảng, tổng quan lý thuyết, giới thiệu tổng thể, định nghĩa cơ bản. "
        "Foundational core concepts, basic overview, theoretical background, introduction to the topic."
    ),
    "definition": (
        "Định nghĩa thuật ngữ, giải thích ý nghĩa từ ngữ, phát biểu định nghĩa khoa học. "
        "Scientific definition of terms, formal explanation of meaning, vocabulary terminology."
    ),
    "theorem": (
        "Định lý toán học, bổ đề, hệ quả, định luật khoa học, quy luật tự nhiên đã được chứng minh. "
        "Mathematical theorems, logic lemmas, scientific laws, corollaries, axioms."
    ),
    "formula": (
        "Công thức toán học, biểu thức số học, phương trình đại số, hệ thức tính toán giá trị. "
        "Mathematical formulas, equations, arithmetic expressions, calculation rules."
    ),
    "method": (
        "Phương pháp giải quyết, thuật toán máy tính, kỹ thuật thực hiện, giải pháp công nghệ. "
        "Problem-solving methods, computer algorithms, techniques, solutions."
    ),
    "procedure": (
        "Quy trình thực hiện, các bước tiến hành, hướng dẫn từng bước, kịch bản nghiệp vụ. "
        "Step-by-step procedures, execution workflows, guide tutorials, sequential processes."
    ),
    "reasoning": (
        "Suy luận logic, chứng minh toán học, lập luận phản bác, lý luận khoa học chặt chẽ. "
        "Logical reasoning, mathematical proofs, arguments, deductive inference."
    ),
    "example": (
        "Ví dụ thực tế, minh họa cụ thể, bài tập vận dụng mẫu, tình huống nghiên cứu điển hình. "
        "Practical examples, concrete illustrations, sample exercises, case studies."
    )
}

# 2. Siêu dữ liệu cấu hình các tín hiệu trọng tâm (Weights & Unit Types)
PARETO_SIGNAL_METADATA: dict[str, dict[str, str | float]] = {
    "core_concept": {"unit_type": "pareto_core", "weight": 1.0},
    "definition": {"unit_type": "pareto_core", "weight": 1.0},
    "principle": {"unit_type": "pareto_core", "weight": 0.95},
    "method": {"unit_type": "pareto_method", "weight": 0.9},
    "procedure": {"unit_type": "pareto_method", "weight": 0.85},
    "rule": {"unit_type": "pareto_rule", "weight": 0.9},
    "formula": {"unit_type": "pareto_formula", "weight": 0.9},
    "theorem": {"unit_type": "pareto_rule", "weight": 0.9},
    "reasoning": {"unit_type": "pareto_core", "weight": 0.85},
    "example": {"unit_type": "pareto_example", "weight": 0.4},
}

_ANCHOR_VECTORS_CACHE: dict[str, list[float]] = {}


async def get_or_create_anchor_embeddings() -> dict[str, list[float]]:
    """Tải và lưu trữ vector neo vào RAM bằng OpenAI embeddings API."""
    global _ANCHOR_VECTORS_CACHE
    if _ANCHOR_VECTORS_CACHE:
        return _ANCHOR_VECTORS_CACHE

    # Sử dụng OpenAI API key chính thức để lấy embeddings cho text-embedding-3-small
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    keys = list(ENRICHED_ANCHORS.keys())
    texts = list(ENRICHED_ANCHORS.values())

    response = await client.embeddings.create(
        model=settings.BOOK_SECTION_EMBEDDING_MODEL,
        input=texts
    )
    for idx, key in enumerate(keys):
        _ANCHOR_VECTORS_CACHE[key] = response.data[idx].embedding

    return _ANCHOR_VECTORS_CACHE


def extract_pareto_signal_hints(
    embedding: list[float] | None = None,
    anchor_vectors: dict[str, list[float]] | None = None,
    threshold: float = 0.20,
) -> list[str]:
    """
    Phân loại tín hiệu dựa trên tích vô hướng vector NumPy (Cosine Similarity).
    Chỉ trả về 1 nhãn duy nhất có độ khớp cao nhất đạt ngưỡng (Arg-max).
    Dùng ngưỡng 0.20 theo kiểm nghiệm thực nghiệm tối ưu của OpenAI text-embedding-3-small.
    """
    if embedding is None or not anchor_vectors:
        return []

    similarities = {}
    v_sec = np.array(embedding)
    for key, anchor in anchor_vectors.items():
        sim = float(np.dot(v_sec, np.array(anchor)))
        if sim >= threshold:
            similarities[key] = sim
            
    if similarities:
        best_key = max(similarities, key=similarities.get)
        return [best_key]
    return []


def infer_unit_type_from_signals(hints: list[str]) -> str:
    for hint in hints:
        meta = PARETO_SIGNAL_METADATA.get(hint)
        if meta:
            return str(meta["unit_type"])
    return "pareto_focus"

```

### app\services\pdf_service.py

```py
import pdfplumber
from pypdf import PdfReader

from app.core.exceptions import DocumentOutlineRequiredError, PdfExtractionError
from app.core.logger import log
from app.services.document_structure_types import ParsedDocument, ParsedSection, flatten_sections, has_extractable_text


def _read_pdf_outline_tree(file_obj) -> list[ParsedSection]:
    file_obj.seek(0)
    try:
        reader = PdfReader(file_obj)
        if not reader.outline:
            return []

        def _walk(outline_items, level: int, parent_path: str = "") -> list[ParsedSection]:
            sections: list[ParsedSection] = []
            for item in outline_items:
                if isinstance(item, list):
                    if sections:
                        parent = sections[-1]
                        sections[-1] = ParsedSection(
                            title=parent.title,
                            level=parent.level,
                            order_index=parent.order_index,
                            path=parent.path,
                            text=parent.text,
                            page_start=parent.page_start,
                            page_end=parent.page_end,
                            top=parent.top,
                            children=_walk(item, level + 1, parent.path),
                        )
                    continue

                try:
                    page_index = reader.get_destination_page_number(item)
                    title = str(getattr(item, "title", "") or "").strip()
                    top = getattr(item, "top", None)
                    if top is not None:
                        top = float(top)
                    if title:
                        order_index = len(sections)
                        path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
                        sections.append(
                            ParsedSection(
                                title=title,
                                level=level,
                                order_index=order_index,
                                path=path,
                                page_start=int(page_index) + 1,
                                top=top,
                            )
                        )
                except Exception as exc:
                    log.warning(f"Bỏ qua outline item lỗi: {exc}")
            return sections

        return _walk(reader.outline, level=1)
    except Exception as exc:
        log.warning(f"Lỗi đọc PDF outline: {exc}")
        return []


def _replace_section_text(section: ParsedSection, text_by_path: dict[str, tuple[str, int | None]]) -> ParsedSection:
    text, page_end = text_by_path.get(section.path, ("", section.page_end))
    return ParsedSection(
        title=section.title,
        level=section.level,
        order_index=section.order_index,
        path=section.path,
        text=text,
        page_start=section.page_start,
        page_end=page_end,
        source_href=section.source_href,
        source_anchor=section.source_anchor,
        top=section.top,
        children=[_replace_section_text(child, text_by_path) for child in section.children],
    )


def _pdf_outline_sort_key(pair: tuple[int, ParsedSection]) -> tuple[int, float]:
    _, section = pair
    page = section.page_start or 1
    top = section.top
    if top is None:
        top = float("inf")
    return (page, -top)


def _crop_text(page, y_start: float, y_end: float) -> str:
    page_height = float(page.height)
    y_start = max(0.0, min(y_start, page_height))
    y_end = max(0.0, min(y_end, page_height))
    if y_start >= y_end:
        return ""
    return page.crop((0, y_start, page.width, y_end)).extract_text() or ""


def _y_from_outline_top(page, outline_top: float | None, *, default: float) -> float:
    if outline_top is None:
        return default
    return float(page.height) - outline_top


def _extract_same_page_section_text(page, start_top: float | None, end_top: float | None) -> str:
    page_height = float(page.height)
    y_start = _y_from_outline_top(page, start_top, default=0.0)
    y_end = _y_from_outline_top(page, end_top, default=page_height)
    return _crop_text(page, y_start, y_end)


def _extract_first_page_section_text(page, start_top: float | None) -> str:
    y_start = _y_from_outline_top(page, start_top, default=0.0)
    return _crop_text(page, y_start, float(page.height))


def _extract_last_page_section_text(page, end_top: float | None) -> str:
    y_end = _y_from_outline_top(page, end_top, default=float(page.height))
    return _crop_text(page, 0.0, y_end)


def _append_non_empty(parts: list[str], text: str) -> None:
    if text.strip():
        parts.append(text)


def _extract_multi_page_section_text(pdf, p_start: int, p_end: int, start_top: float | None, end_top: float | None) -> str:
    parts: list[str] = []
    _append_non_empty(parts, _extract_first_page_section_text(pdf.pages[p_start - 1], start_top))

    for page_number in range(p_start + 1, p_end):
        _append_non_empty(parts, pdf.pages[page_number - 1].extract_text() or "")

    if p_end <= len(pdf.pages):
        _append_non_empty(parts, _extract_last_page_section_text(pdf.pages[p_end - 1], end_top))

    return "\n".join(parts).strip()


def _extract_section_text_from_pdf(pdf, current_section: ParsedSection, next_section: ParsedSection | None) -> tuple[str, int]:
    total_pages = len(pdf.pages)
    start_page = current_section.page_start or 1
    start_top = current_section.top
    end_page = (next_section.page_start or (total_pages + 1)) if next_section else total_pages + 1
    end_top = next_section.top if next_section else 0.0

    p_start = max(1, min(start_page, total_pages))
    p_end = max(1, min(end_page, total_pages + 1))

    if p_start == p_end:
        text = _extract_same_page_section_text(pdf.pages[p_start - 1], start_top, end_top)
    else:
        text = _extract_multi_page_section_text(pdf, p_start, p_end, start_top, end_top)

    section_page_end = min(total_pages, max(start_page, end_page - 1))
    return text, section_page_end


def parse_pdf_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    outline_tree = _read_pdf_outline_tree(file_obj)
    outline_items = flatten_sections(outline_tree)

    if not outline_items or len(outline_items) <= 1:
        raise DocumentOutlineRequiredError(
            "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
        )

    file_obj.seek(0)
    text_by_path: dict[str, tuple[str, int | None]] = {}

    try:
        with pdfplumber.open(file_obj) as pdf:
            ordered_items = sorted(
                enumerate(outline_items),
                key=_pdf_outline_sort_key,
            )

            for i, (_, current_section) in enumerate(ordered_items):
                next_section = ordered_items[i + 1][1] if i < len(ordered_items) - 1 else None
                chapter_text, section_page_end = _extract_section_text_from_pdf(pdf, current_section, next_section)
                text_by_path[current_section.path] = (chapter_text, section_page_end)

    except DocumentOutlineRequiredError:
        raise
    except Exception as exc:
        raise PdfExtractionError(f"Không thể đọc nội dung PDF: {exc}") from exc

    sections = [_replace_section_text(section, text_by_path) for section in outline_tree]
    if not has_extractable_text(sections):
        raise PdfExtractionError(
            "PDF có outline nhưng không trích xuất được text. File có thể là scan ảnh hoặc bị lỗi."
        )

    return ParsedDocument(document_type="pdf", sections=sections)


async def parse_pdf_structure(file_obj) -> ParsedDocument:
    import asyncio
    import io
    file_bytes = file_obj.read()
    return await asyncio.to_thread(parse_pdf_structure_sync, io.BytesIO(file_bytes))

```

### app\services\processing_job_service.py

```py
import uuid

from sqlmodel import Session

from app.core.exceptions import ProcessingJobNotFoundError
from app.repositories.processing_job_repo import get_latest_processing_job_for_book, get_processing_job_by_id_and_user


def get_job_status(session: Session, user_id: uuid.UUID, job_id: uuid.UUID):
    job = get_processing_job_by_id_and_user(session, job_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job


def get_book_processing_status(session: Session, user_id: uuid.UUID, book_id: uuid.UUID):
    job = get_latest_processing_job_for_book(session, book_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job

```

### app\services\rag_service.py

```py
from app.services.agent_grounding.reranker import rerank_candidates
import asyncio
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import log
from app.core.supabase import supabase
from app.services.agent_grounding.hybrid_retrieval import (
    HybridRetrievalConfig,
    build_hybrid_retrieval_result,
)
from app.services.agent_grounding.query_normalizer import normalized_key

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

BOOK_CONTEXT_NOT_FOUND_MESSAGE = "Không tìm thấy thông tin cụ thể trong sách."


def _execute_supabase_rpc(name: str, payload: dict[str, Any]):
    return supabase.rpc(name, payload).execute()


def _normalize_section_ids(section_ids: list[str] | None) -> list[str] | None:
    if not section_ids:
        return None
    return section_ids


def _round_score(value: float | int | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)


async def _embed_query(query: str, *, model: str) -> list[float]:
    res = await ai_client.embeddings.create(model=model, input=[query])
    query_vector = res.data[0].embedding
    return query_vector

# FALLBACK
async def search_book_section_knowledge(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
    match_count: int | None = None,
) -> list[dict[str, Any]] | str:
    query_vector = await _embed_query(query, model=settings.BOOK_SECTION_EMBEDDING_MODEL)
    result = await asyncio.to_thread(
        _execute_supabase_rpc,
        "match_book_section_knowledge",
        {
            "query_embedding": query_vector,
            "match_threshold": settings.BOOK_SECTION_RAG_MATCH_THRESHOLD,
            "match_count": match_count or settings.BOOK_SECTION_RAG_MATCH_COUNT,
            "filter_book_ids": document_ids,
            "filter_section_ids": _normalize_section_ids(section_ids),
        },
    )

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


async def search_book_section_knowledge_lexical(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
    match_count: int | None = None,
) -> list[dict[str, Any]] | str:
    result = await asyncio.to_thread(
        _execute_supabase_rpc,
        "match_book_section_knowledge_lexical",
        {
            "query_text": query,
            "normalized_query_text": normalized_key(query),
            "match_count": match_count or settings.AGENT_HYBRID_LEXICAL_CANDIDATES,
            "filter_book_ids": document_ids,
            "filter_section_ids": _normalize_section_ids(section_ids),
        },
    )

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


def _as_payload_list(payload: list[dict[str, Any]] | str) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def _hybrid_config() -> HybridRetrievalConfig:
    max_chunks = settings.AGENT_HYBRID_MAX_CONTEXT_CHUNKS
    if settings.AGENT_RERANKER_ENABLED:
        max_chunks = settings.AGENT_RERANKER_CANDIDATES_LIMIT

    return HybridRetrievalConfig(
        min_final_score=settings.AGENT_HYBRID_MIN_FINAL_SCORE,
        max_context_chunks=max_chunks,
        max_chunks_per_section=settings.AGENT_HYBRID_MAX_CHUNKS_PER_SECTION,
        validate_evidence_enabled=settings.AGENT_HYBRID_VALIDATE_EVIDENCE_ENABLED,
    )


async def search_book_hybrid_knowledge(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
) -> list[dict[str, Any]] | str:

    cadidates_limit = settings.AGENT_RERANKER_CANDIDATES_LIMIT

    vector_task = search_book_section_knowledge(
        query,
        document_ids,
        section_ids=section_ids,
        match_count=cadidates_limit,
    )
    lexical_task = search_book_section_knowledge_lexical(
        query,
        document_ids,
        section_ids=section_ids,
        match_count=cadidates_limit,
    )

    vector_result, lexical_result = await asyncio.gather(vector_task, lexical_task, return_exceptions=True)

    if isinstance(vector_result, Exception):
        log.error(f"RAG Tối ưu hóa: Nhánh Vector Search bị lỗi: {vector_result}")
        vector_result = BOOK_CONTEXT_NOT_FOUND_MESSAGE

    if isinstance(lexical_result, Exception):
        log.error(f"RAG Tối ưu hóa: Nhánh Lexical Search bị lỗi: {lexical_result}")
        lexical_result = BOOK_CONTEXT_NOT_FOUND_MESSAGE

    # Build hybrid with Base Reranker
    hybrid_result = build_hybrid_retrieval_result(
        query=query,
        vector_payload=_as_payload_list(vector_result),
        lexical_payload=_as_payload_list(lexical_result),
        config=_hybrid_config(),
    )
    if not hybrid_result.found:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE
    
    # Rerank with Cohere
    final_chunks = hybrid_result.chunks
    if settings.AGENT_RERANKER_ENABLED:
        log.info(f"Reranker start: {len(final_chunks)} candidates with Cohere Reranker for query='{query}'")
        for idx, chunk in enumerate(final_chunks):
            content_full = str(chunk.get("content") or "").replace("\n", " ")
            log.info(f"  [Pre-Rerank Rank {idx + 1}] ID: {chunk.get('id')} | Score: {_round_score(chunk.get('final_score') or chunk.get('similarity'))} | Content: {content_full}")
        
        final_chunks = await rerank_candidates(query, final_chunks)
        final_chunks = final_chunks[:settings.AGENT_RERANKER_TOP_N]

    log.info(
        "Hybrid section RAG done | "
        f"found={hybrid_result.found} | "
        f"candidates={hybrid_result.candidate_count} | "
        f"final_chunks_count={len(final_chunks)} | "
        f"top_id={final_chunks[0].get('id') if final_chunks else None} | "
        f"top_final_score={_round_score(final_chunks[0].get('final_score')) if final_chunks else None}"
    )

    for idx, chunk in enumerate(final_chunks):
        content_full = str(chunk.get("content") or "").replace("\n", " ")
        section_path = chunk.get("section_path") or chunk.get("section_title") or "unknown"
        log.info(f"  [Post-Rerank Rank {idx + 1}] ID: {chunk.get('id')} | Section: {section_path} | Score: {_round_score(chunk.get('final_score') or chunk.get('similarity'))} | Content: {content_full}")

    if not final_chunks:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE
    
    return final_chunks


async def search_book_knowledge(query: str, document_ids: list[str]) -> list[dict[str, Any]] | str:
    """Tìm kiếm kiến thức sách bằng Hybrid RAG pipeline (vector + lexical + rerank)."""
    return await search_book_hybrid_knowledge(query, document_ids)

```

### app\services\reading_plan_schedule_service.py

```py
import uuid
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.core.config import settings
from app.core.exceptions import ActiveLearningBookLimitExceededError, ReadingPlanScheduleConflictError
from app.models.db_models import ReadingPlanScheduleSlot
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.reading_plan_schedule_repo import count_active_learning_books, create_slots_for_plan, find_conflicting_slot
from app.services.reminder_schedule_service import WEEKDAY_ALIASES, parse_hhmm

WEEKDAY_LABELS = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

WEEKDAY_SHORT_LABELS = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun",
}

WEEKDAY_VI_LABELS = {
    0: "Thứ hai",
    1: "Thứ ba",
    2: "Thứ tư",
    3: "Thứ năm",
    4: "Thứ sáu",
    5: "Thứ bảy",
    6: "Chủ nhật",
}


@dataclass(frozen=True)
class ScheduleSlotInput:
    weekday: int
    reminder_time: str
    timezone: str


def _weekday_from_value(value: object) -> int:
    weekday = WEEKDAY_ALIASES.get(str(value).strip().lower())
    if weekday is None:
        raise ReadingPlanScheduleConflictError(f"Ngày học không hợp lệ: {value}")
    return weekday


def normalize_schedule_config(
    schedule_config: object,
    *,
    reminder_time: str,
    timezone_name: str,
) -> list[ScheduleSlotInput]:
    if not isinstance(schedule_config, list) or not schedule_config:
        raise ReadingPlanScheduleConflictError("Vui lòng chọn ít nhất một ngày học.")

    try:
        parse_hhmm(reminder_time)
    except (TypeError, ValueError) as exc:
        raise ReadingPlanScheduleConflictError(f"Giờ học không hợp lệ: {reminder_time}. Vui lòng dùng định dạng HH:MM.") from exc
    weekdays = sorted({_weekday_from_value(day) for day in schedule_config})
    return [ScheduleSlotInput(weekday=weekday, reminder_time=reminder_time, timezone=timezone_name) for weekday in weekdays]


def validate_active_learning_capacity(session: Session, *, user_id: uuid.UUID) -> None:
    if count_active_learning_books(session, user_id=user_id) >= settings.MAX_ACTIVE_LEARNING_BOOKS_PER_USER:
        raise ActiveLearningBookLimitExceededError()


def validate_schedule_slots_available(
    session: Session,
    *,
    user_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
    exclude_plan_id: uuid.UUID | None = None,
) -> None:
    for slot in slots:
        conflict = find_conflicting_slot(
            session,
            user_id=user_id,
            weekday=slot.weekday,
            reminder_time=slot.reminder_time,
            exclude_plan_id=exclude_plan_id,
        )
        if conflict:
            weekday_label = WEEKDAY_VI_LABELS.get(slot.weekday, f"ngày {slot.weekday}")
            raise ReadingPlanScheduleConflictError(
                f"Lịch học bị trùng vào {weekday_label} lúc {slot.reminder_time}. Hãy chọn ngày hoặc giờ khác."
            )


def build_slots_for_plan(
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    plan_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
    is_active: bool = True,
) -> list[ReadingPlanScheduleSlot]:
    return [
        ReadingPlanScheduleSlot(
            user_id=user_id,
            book_id=book_id,
            plan_id=plan_id,
            weekday=slot.weekday,
            reminder_time=slot.reminder_time,
            timezone=slot.timezone,
            is_active=is_active,
        )
        for slot in slots
    ]


def validate_plan_schedule_shape(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
) -> list[ScheduleSlotInput]:
    user_settings = get_or_create_notification_settings(session, user_id)
    resolved_reminder_time = reminder_time or user_settings.reminder_time
    return normalize_schedule_config(
        schedule_config,
        reminder_time=resolved_reminder_time,
        timezone_name=user_settings.timezone,
    )


def validate_plan_schedule_for_activation(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
    exclude_plan_id: uuid.UUID | None = None,
) -> list[ScheduleSlotInput]:
    slots = validate_plan_schedule_shape(
        session,
        user_id=user_id,
        schedule_config=schedule_config,
        reminder_time=reminder_time,
    )
    if exclude_plan_id is None:
        validate_active_learning_capacity(session, user_id=user_id)
    validate_schedule_slots_available(session, user_id=user_id, slots=slots, exclude_plan_id=exclude_plan_id)
    return slots


def validate_plan_schedule_for_create(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
    exclude_plan_id: uuid.UUID | None = None,
) -> list[ScheduleSlotInput]:
    return validate_plan_schedule_for_activation(
        session,
        user_id=user_id,
        schedule_config=schedule_config,
        reminder_time=reminder_time,
        exclude_plan_id=exclude_plan_id,
    )


def create_schedule_slots_for_plan(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    plan_id: uuid.UUID,
    slots: list[ScheduleSlotInput],
) -> list[ReadingPlanScheduleSlot]:
    try:
        return create_slots_for_plan(
            session,
            slots=build_slots_for_plan(user_id=user_id, book_id=book_id, plan_id=plan_id, slots=slots),
        )
    except IntegrityError as exc:
        raise ReadingPlanScheduleConflictError() from exc

```

### app\services\reading_plan_session_service.py

```py
import uuid
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, PlanMode, PlanStatus, ReadingPlanSessionStatus, ReadingPlanSessionUnitStatus
from app.core.exceptions import BadRequestError, BookNotFoundError, ReadingPlanScheduleConflictError, ReadingPlanSessionNotFoundError, ReadingPlanSessionStatusConflictError
from app.models.db_models import (
    Book,
    LearningUnit,
    ReadingPlan,
    ReadingPlanScheduleSlot,
    ReadingPlanSession,
    ReadingPlanSessionUnit,
)
from app.repositories.learning_progress_repo import list_book_progress
from app.repositories.learning_unit_repo import list_learning_units
from app.repositories.notification_settings_repo import get_or_create_notification_settings
from app.repositories.reading_plan_repo import list_plans_for_book_mode
from app.repositories.reading_plan_schedule_repo import list_slots_for_plan
from app.repositories.reading_plan_session_repo import (
    FINAL_SESSION_STATUSES,
    cancel_unfinished_sessions_for_plan,
    find_session_schedule_conflict,
    get_next_session_for_plan,
    get_owned_session,
    get_plan_session_summary_counts,
    get_session_unit_for_learning_unit,
    list_session_units,
    list_sessions_for_book,
    list_sessions_for_plan,
    list_sessions_for_user_local_date,
    list_sessions_for_user_range,
    mark_overdue_sessions_missed,
    mark_overdue_sessions_missed_rows,
)
from app.services.reminder_schedule_service import ensure_aware_utc, parse_hhmm, to_local

MAX_SESSION_RANGE_DAYS = 120


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _chunk_units(units: list[LearningUnit], pace: int) -> list[list[LearningUnit]]:
    safe_pace = max(1, int(pace or 1))
    return [units[index : index + safe_pace] for index in range(0, len(units), safe_pace)]


def _next_session_datetimes(
    *,
    slots: list[ReadingPlanScheduleSlot],
    now: datetime,
    count: int,
    lookahead_days: int = 370,
) -> list[datetime]:
    if count <= 0 or not slots:
        return []

    now = ensure_aware_utc(now)
    candidates: list[datetime] = []
    for slot in sorted(slots, key=lambda value: (value.weekday, value.reminder_time)):
        slot_time = parse_hhmm(slot.reminder_time)
        tz = ZoneInfo(slot.timezone)
        local_now = now.astimezone(tz)
        for offset in range(lookahead_days):
            local_day = local_now.date() + timedelta(days=offset)
            if local_day.weekday() != slot.weekday:
                continue
            local_dt = datetime.combine(local_day, slot_time, tzinfo=tz)
            scheduled_at = local_dt.astimezone(timezone.utc)
            if scheduled_at >= now:
                candidates.append(scheduled_at)

    unique_candidates = sorted(set(candidates))
    return unique_candidates[:count]


def _completed_unit_ids(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, mode: PlanMode) -> set[uuid.UUID]:
    progress_rows = list_book_progress(session, user_id=user_id, book_id=book_id, mode=mode)
    return {row.learning_unit_id for row in progress_rows if row.status == LearningProgressStatus.COMPLETED}


def _remaining_units_for_plan(session: Session, *, plan: ReadingPlan, user_id: uuid.UUID) -> list[LearningUnit]:
    mode = PlanMode(plan.mode)
    units = list_learning_units(session, plan.book_id, mode)
    completed_ids = _completed_unit_ids(session, user_id=user_id, book_id=plan.book_id, mode=mode)
    return [unit for unit in units if unit.id not in completed_ids]


def _session_local_date(scheduled_at: datetime, timezone_name: str) -> str:
    return ensure_aware_utc(scheduled_at).astimezone(ZoneInfo(timezone_name)).date().isoformat()


def ensure_future_sessions_for_plan(
    session: Session,
    *,
    plan: ReadingPlan,
    user_id: uuid.UUID,
    now: datetime | None = None,
    replace_unfinished: bool = False,
) -> int:
    now = ensure_aware_utc(now or _now_utc())
    if plan.status == PlanStatus.COMPLETED.value:
        return 0

    if replace_unfinished:
        cancel_unfinished_sessions_for_plan(session, plan_id=plan.id, now=now)
    else:
        existing = [
            row
            for row in list_sessions_for_plan(session, plan_id=plan.id)
            if row.status not in FINAL_SESSION_STATUSES
        ]
        if existing:
            return 0

    slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
    if not slots:
        return 0

    remaining_units = _remaining_units_for_plan(session, plan=plan, user_id=user_id)
    unit_groups = _chunk_units(remaining_units, plan.pace)
    scheduled_times = _next_session_datetimes(slots=slots, now=now, count=len(unit_groups))
    created = 0

    for index, (scheduled_at, unit_group) in enumerate(zip(scheduled_times, unit_groups, strict=False)):
        slot = min(slots, key=lambda value: abs((scheduled_at.astimezone(ZoneInfo(value.timezone)).weekday() - value.weekday) % 7))
        plan_session = ReadingPlanSession(
            user_id=user_id,
            plan_id=plan.id,
            book_id=plan.book_id,
            mode=PlanMode(plan.mode),
            session_index=index,
            scheduled_at=scheduled_at,
            local_date=_session_local_date(scheduled_at, slot.timezone),
            reminder_time=slot.reminder_time,
            timezone=slot.timezone,
            status=ReadingPlanSessionStatus.SCHEDULED.value,
            completed_units=0,
            total_units=len(unit_group),
        )
        session.add(plan_session)
        session.flush()

        for unit_order, unit in enumerate(unit_group):
            session.add(
                ReadingPlanSessionUnit(
                    session_id=plan_session.id,
                    plan_id=plan.id,
                    book_id=plan.book_id,
                    learning_unit_id=unit.id,
                    unit_order=unit_order,
                    status=ReadingPlanSessionUnitStatus.PENDING.value,
                )
            )
        created += 1

    return created


def cancel_future_sessions_for_plan(
    session: Session,
    *,
    plan_id: uuid.UUID,
    now: datetime | None = None,
) -> int:
    return cancel_unfinished_sessions_for_plan(session, plan_id=plan_id, now=ensure_aware_utc(now or _now_utc()))


def mark_due_sessions_missed(
    session: Session,
    *,
    user_id: uuid.UUID | None = None,
    now: datetime | None = None,
) -> int:
    return mark_overdue_sessions_missed(session, user_id=user_id, now=ensure_aware_utc(now or _now_utc()))


def mark_due_sessions_missed_rows(
    session: Session,
    *,
    user_id: uuid.UUID | None = None,
    now: datetime | None = None,
) -> list[ReadingPlanSession]:
    return mark_overdue_sessions_missed_rows(session, user_id=user_id, now=ensure_aware_utc(now or _now_utc()))


def _recalculate_parent_session(session: Session, plan_session: ReadingPlanSession, *, now: datetime) -> ReadingPlanSession:
    units = list_session_units(session, session_ids=[plan_session.id])
    completed_count = sum(1 for unit in units if unit.status == ReadingPlanSessionUnitStatus.COMPLETED.value)
    active_count = sum(
        1
        for unit in units
        if unit.status
        in (
            ReadingPlanSessionUnitStatus.IN_PROGRESS.value,
            ReadingPlanSessionUnitStatus.COMPLETED.value,
        )
    )

    plan_session.completed_units = completed_count
    plan_session.total_units = len(units)
    plan_session.updated_at = now

    if len(units) > 0 and completed_count >= len(units):
        plan_session.status = ReadingPlanSessionStatus.COMPLETED.value
        plan_session.completed_at = plan_session.completed_at or now
    elif active_count > 0:
        plan_session.status = ReadingPlanSessionStatus.IN_PROGRESS.value
        plan_session.started_at = plan_session.started_at or now
    elif plan_session.scheduled_at <= now and plan_session.status == ReadingPlanSessionStatus.SCHEDULED.value:
        plan_session.status = ReadingPlanSessionStatus.DUE.value

    session.add(plan_session)
    return plan_session


def sync_reading_plan_session_unit_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode,
    progress_status: LearningProgressStatus,
    completed_at: datetime | None = None,
    now: datetime | None = None,
    commit: bool = True,
) -> None:
    now = ensure_aware_utc(now or _now_utc())
    plans = list_plans_for_book_mode(session, book_id=book_id, mode=mode)
    changed = False
    for plan in plans:
        session_unit = get_session_unit_for_learning_unit(session, plan_id=plan.id, learning_unit_id=learning_unit_id)
        if not session_unit:
            continue

        if progress_status == LearningProgressStatus.COMPLETED:
            session_unit.status = ReadingPlanSessionUnitStatus.COMPLETED.value
            session_unit.completed_at = session_unit.completed_at or completed_at or now
        elif progress_status == LearningProgressStatus.IN_PROGRESS and session_unit.status == ReadingPlanSessionUnitStatus.PENDING.value:
            session_unit.status = ReadingPlanSessionUnitStatus.IN_PROGRESS.value
        else:
            continue

        session_unit.updated_at = now
        session.add(session_unit)
        parent = session.get(ReadingPlanSession, session_unit.session_id)
        if parent:
            _recalculate_parent_session(session, parent, now=now)
        changed = True

    if changed and commit:
        session.commit()


def _learning_unit_title_map(session: Session, unit_ids: list[uuid.UUID]) -> dict[uuid.UUID, str]:
    if not unit_ids:
        return {}
    rows = session.exec(select(LearningUnit.id, LearningUnit.title).where(LearningUnit.id.in_(unit_ids))).all()
    return dict(rows)


def sessions_to_response(session: Session, sessions: list[ReadingPlanSession]) -> list[dict]:
    units = list_session_units(session, session_ids=[item.id for item in sessions])
    units_by_session: dict[uuid.UUID, list[ReadingPlanSessionUnit]] = {}
    for unit in units:
        units_by_session.setdefault(unit.session_id, []).append(unit)

    titles = _learning_unit_title_map(session, [unit.learning_unit_id for unit in units])
    now = _now_utc()
    result: list[dict] = []
    for item in sessions:
        item_units = units_by_session.get(item.id, [])
        result.append(
            {
                "id": item.id,
                "plan_id": item.plan_id,
                "book_id": item.book_id,
                "mode": item.mode,
                "session_index": item.session_index,
                "scheduled_at": item.scheduled_at,
                "local_date": item.local_date,
                "reminder_time": item.reminder_time,
                "timezone": item.timezone,
                "status": item.status,
                "completed_units": item.completed_units,
                "total_units": item.total_units,
                "is_overdue": item.status not in FINAL_SESSION_STATUSES and item.scheduled_at < now,
                "started_at": item.started_at,
                "completed_at": item.completed_at,
                "missed_at": item.missed_at,
                "skipped_at": item.skipped_at,
                "units": [
                    {
                        "id": unit.id,
                        "learning_unit_id": unit.learning_unit_id,
                        "unit_title": titles.get(unit.learning_unit_id, ""),
                        "unit_order": unit.unit_order,
                        "status": unit.status,
                        "completed_at": unit.completed_at,
                    }
                    for unit in item_units
                ],
            }
        )
    return result


def build_plan_session_summary(session: Session, *, plan_id: uuid.UUID) -> dict:
    counts = get_plan_session_summary_counts(session, plan_id=plan_id)
    next_session = get_next_session_for_plan(session, plan_id=plan_id)
    return {
        "total_sessions": counts.total_sessions,
        "completed_sessions": counts.completed_sessions,
        "missed_sessions": counts.missed_sessions,
        "next_session": sessions_to_response(session, [next_session])[0] if next_session else None,
    }


def list_book_reading_plan_sessions(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode | str | None = None,
) -> dict:
    now = _now_utc()
    mode_value = PlanMode(mode) if mode else None
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()
    sessions = list_sessions_for_book(session, user_id=user_id, book_id=book_id, mode=mode_value)
    return {
        "book_id": book_id,
        "total": len(sessions),
        "items": sessions_to_response(session, sessions),
    }


def list_today_reading_plan_sessions(
    session: Session,
    *,
    user_id: uuid.UUID,
    local_date: date | None = None,
) -> dict:
    now = _now_utc()
    user_settings = get_or_create_notification_settings(session, user_id)
    resolved_date = local_date or to_local(now, user_settings.timezone).date()
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()
    sessions = list_sessions_for_user_local_date(session, user_id=user_id, local_date=resolved_date.isoformat())
    return {
        "local_date": resolved_date.isoformat(),
        "timezone": user_settings.timezone,
        "total": len(sessions),
        "items": sessions_to_response(session, sessions),
    }


def _resolve_status_filter(status: str | None) -> str | None:
    if status is None:
        return None
    try:
        return ReadingPlanSessionStatus(status).value
    except ValueError as exc:
        raise BadRequestError("Trạng thái buổi học không hợp lệ.") from exc


def _resolve_mode_filter(mode: PlanMode | str | None) -> PlanMode | None:
    if mode is None:
        return None
    try:
        return PlanMode(mode)
    except ValueError as exc:
        raise BadRequestError("Mode kế hoạch học không hợp lệ.") from exc


def _resolve_timezone_name(timezone_name: str | None, fallback: str) -> str:
    resolved = timezone_name or fallback or "Asia/Ho_Chi_Minh"
    try:
        ZoneInfo(resolved)
    except ZoneInfoNotFoundError as exc:
        raise BadRequestError("Timezone không hợp lệ.") from exc
    return resolved


def _scheduled_at_from_local(*, local_date: date, reminder_time: str, timezone_name: str) -> datetime:
    try:
        local_time = parse_hhmm(reminder_time)
    except ValueError as exc:
        raise BadRequestError("Giờ nhắc học phải đúng định dạng HH:MM.") from exc
    tz = ZoneInfo(timezone_name)
    return datetime.combine(local_date, local_time, tzinfo=tz).astimezone(timezone.utc)


def _session_summary_counts(sessions: list[ReadingPlanSession]) -> dict[str, int]:
    return {status.value: sum(1 for item in sessions if item.status == status.value) for status in ReadingPlanSessionStatus}


def list_reading_plan_sessions_range(
    session: Session,
    *,
    user_id: uuid.UUID,
    from_date: date | None = None,
    to_date: date | None = None,
    book_id: uuid.UUID | None = None,
    mode: PlanMode | str | None = None,
    status: str | None = None,
) -> dict:
    now = _now_utc()
    user_settings = get_or_create_notification_settings(session, user_id)
    local_today = to_local(now, user_settings.timezone).date()
    resolved_from = from_date or local_today - timedelta(days=7)
    resolved_to = to_date or local_today + timedelta(days=30)
    if resolved_from > resolved_to:
        raise BadRequestError("from_date không được lớn hơn to_date.")
    if (resolved_to - resolved_from).days > MAX_SESSION_RANGE_DAYS:
        raise BadRequestError(f"Khoảng thời gian không được vượt quá {MAX_SESSION_RANGE_DAYS} ngày.")

    if book_id:
        book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
        if not book:
            raise BookNotFoundError()

    mode_value = _resolve_mode_filter(mode)
    status_value = _resolve_status_filter(status)
    mark_due_sessions_missed(session, user_id=user_id, now=now)
    session.commit()

    sessions = list_sessions_for_user_range(
        session,
        user_id=user_id,
        from_local_date=resolved_from.isoformat(),
        to_local_date=resolved_to.isoformat(),
        book_id=book_id,
        mode=mode_value,
        status=status_value,
    )
    return {
        "book_id": book_id,
        "timezone": user_settings.timezone,
        "from_date": resolved_from,
        "to_date": resolved_to,
        "total": len(sessions),
        "summary": _session_summary_counts(sessions),
        "items": sessions_to_response(session, sessions),
    }


def _ensure_session_can_change(plan_session: ReadingPlanSession, *, action: str) -> None:
    if plan_session.status in FINAL_SESSION_STATUSES:
        raise ReadingPlanSessionStatusConflictError(f"Buổi học đã ở trạng thái cuối, không thể {action}.")


def skip_reading_plan_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    reason: str | None = None,
) -> dict:
    now = _now_utc()
    plan_session = get_owned_session(session, user_id=user_id, session_id=session_id)
    if not plan_session:
        raise ReadingPlanSessionNotFoundError()
    _ensure_session_can_change(plan_session, action="bỏ qua")

    plan_session.status = ReadingPlanSessionStatus.SKIPPED.value
    plan_session.skipped_at = plan_session.skipped_at or now
    plan_session.updated_at = now
    session.add(plan_session)

    units = list_session_units(session, session_ids=[plan_session.id])
    for unit in units:
        if unit.status in (ReadingPlanSessionUnitStatus.PENDING.value, ReadingPlanSessionUnitStatus.IN_PROGRESS.value):
            unit.status = ReadingPlanSessionUnitStatus.SKIPPED.value
            unit.updated_at = now
            session.add(unit)

    session.commit()
    session.refresh(plan_session)
    return {
        "message": "Đã bỏ qua buổi học.",
        "session": sessions_to_response(session, [plan_session])[0],
    }


def reschedule_reading_plan_session(
    session: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    local_date: date,
    reminder_time: str,
    timezone_name: str | None = None,
) -> dict:
    now = _now_utc()
    plan_session = get_owned_session(session, user_id=user_id, session_id=session_id)
    if not plan_session:
        raise ReadingPlanSessionNotFoundError()
    _ensure_session_can_change(plan_session, action="dời lịch")

    resolved_timezone = _resolve_timezone_name(timezone_name, plan_session.timezone)
    scheduled_at = _scheduled_at_from_local(
        local_date=local_date,
        reminder_time=reminder_time,
        timezone_name=resolved_timezone,
    )
    conflict = find_session_schedule_conflict(
        session,
        user_id=user_id,
        scheduled_at=scheduled_at,
        exclude_session_id=plan_session.id,
    )
    if conflict:
        conflict_book = session.get(Book, conflict.book_id)
        conflict_title = conflict_book.title if conflict_book else "một sách khác"
        raise ReadingPlanScheduleConflictError(
            f'Lịch học bị trùng với sách "{conflict_title}" vào {reminder_time} ngày {local_date.isoformat()}.'
        )

    units = list_session_units(session, session_ids=[plan_session.id])
    has_started_unit = any(unit.status in (ReadingPlanSessionUnitStatus.IN_PROGRESS.value, ReadingPlanSessionUnitStatus.COMPLETED.value) for unit in units)
    plan_session.scheduled_at = scheduled_at
    plan_session.local_date = local_date.isoformat()
    plan_session.reminder_time = reminder_time
    plan_session.timezone = resolved_timezone
    plan_session.updated_at = now
    if has_started_unit or plan_session.started_at:
        plan_session.status = ReadingPlanSessionStatus.IN_PROGRESS.value
        plan_session.started_at = plan_session.started_at or now
        if scheduled_at > now:
            plan_session.missed_at = None
    elif scheduled_at > now:
        plan_session.status = ReadingPlanSessionStatus.SCHEDULED.value
        plan_session.missed_at = None
    else:
        plan_session.status = ReadingPlanSessionStatus.MISSED.value
        plan_session.missed_at = plan_session.missed_at or now

    session.add(plan_session)
    session.commit()
    session.refresh(plan_session)
    return {
        "message": "Đã dời lịch buổi học.",
        "session": sessions_to_response(session, [plan_session])[0],
    }


def sync_existing_session_units_from_progress(session: Session, *, plan: ReadingPlan, user_id: uuid.UUID) -> None:
    progress_rows = list_book_progress(session, user_id=user_id, book_id=plan.book_id, mode=PlanMode(plan.mode))
    for progress in progress_rows:
        sync_reading_plan_session_unit_completion(
            session,
            user_id=user_id,
            book_id=plan.book_id,
            learning_unit_id=progress.learning_unit_id,
            mode=PlanMode(plan.mode),
            progress_status=progress.status,
            completed_at=progress.completed_at,
            now=progress.completed_at or progress.last_activity_at or _now_utc(),
            commit=False,
        )

```

### app\services\reminder_schedule_service.py

```py
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

WEEKDAY_ALIASES = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def parse_hhmm(value: str) -> time:
    parts = value.split(":", 1)
    if len(parts) != 2:
        raise ValueError("Time must use HH:MM format.")
    hour, minute = int(parts[0]), int(parts[1])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("Time must use HH:MM 24-hour format.")
    return time(hour=hour, minute=minute)


def to_local(now_utc: datetime, timezone_name: str) -> datetime:
    return ensure_aware_utc(now_utc).astimezone(ZoneInfo(timezone_name))


def is_quiet_time(local_dt: datetime, quiet_start: str, quiet_end: str) -> bool:
    start = parse_hhmm(quiet_start)
    end = parse_hhmm(quiet_end)
    current = local_dt.time()
    if start <= end:
        return start <= current < end
    return current >= start or current < end


def shift_out_of_quiet_hours(due_at_utc: datetime, timezone_name: str, quiet_start: str, quiet_end: str) -> datetime:
    local_due = to_local(due_at_utc, timezone_name)
    if not is_quiet_time(local_due, quiet_start, quiet_end):
        return ensure_aware_utc(due_at_utc)

    end_time = parse_hhmm(quiet_end)
    start_time = parse_hhmm(quiet_start)
    if start_time <= end_time:
        shifted_local = local_due.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)
    elif local_due.time() < end_time:
        shifted_local = local_due.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)
    else:
        next_day = local_due.date() + timedelta(days=1)
        shifted_local = datetime.combine(next_day, end_time, tzinfo=local_due.tzinfo)
    return shifted_local.astimezone(timezone.utc)


def local_day_bounds_utc(local_day: date, timezone_name: str) -> tuple[datetime, datetime]:
    tz = ZoneInfo(timezone_name)
    start_local = datetime.combine(local_day, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def reminder_due_at_for_today(
    *,
    now_utc: datetime,
    timezone_name: str,
    reminder_time: str,
) -> datetime:
    local_now = to_local(now_utc, timezone_name)
    reminder_local_time = parse_hhmm(reminder_time)
    reminder_local = datetime.combine(local_now.date(), reminder_local_time, tzinfo=local_now.tzinfo)
    return reminder_local.astimezone(timezone.utc)

```

### app\services\review_service.py

```py
import uuid
from datetime import datetime, timezone, timedelta

from sqlmodel import Session

from app.core.constant import PlanMode, ReviewItemStatus
from app.core.exceptions import BadRequestError, ReviewItemNotFoundError
from app.models.db_models import Book, LearningUnit, SpacedReviewItem
from app.repositories.spaced_review_repo import (
    create_review_item_once,
    get_review_item_for_user,
    list_review_items_for_user,
    mark_review_item_completed,
    mark_review_item_skipped,
)
from app.schemas.review import ReviewActionResponse, ReviewItemResponse, ReviewListResponse
from app.services.spaced_review_service import SPACED_REVIEW_INTERVALS


def _to_review_item_response(session: Session, item: SpacedReviewItem) -> ReviewItemResponse:
    book = session.get(Book, item.book_id)
    unit = session.get(LearningUnit, item.learning_unit_id) if item.learning_unit_id else None
    return ReviewItemResponse(
        review_item_id=item.id,
        book_id=item.book_id,
        book_title=book.title if book else None,
        learning_unit_id=item.learning_unit_id,
        learning_unit_title=unit.title if unit else None,
        mode=item.mode,
        status=item.status,
        due_at=item.due_at,
        interval_days=item.interval_days,
        sequence_index=item.sequence_index,
        review_text=item.review_text_snapshot or (unit.review_text if unit else "") or "",
        review_audio_url=unit.review_audio_url if unit else None,
        anchor_completed_at=item.anchor_completed_at,
        last_reviewed_at=item.last_reviewed_at,
        completed_at=item.completed_at,
        notified_at=item.notified_at,
    )


def list_review_items(
    session: Session,
    *,
    user_id: uuid.UUID,
    status: str = "due",
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> ReviewListResponse:
    allowed_statuses = {"due", "upcoming", "completed", "skipped", "all"}
    if status not in allowed_statuses:
        raise BadRequestError("Trạng thái ôn tập không hợp lệ.")
    try:
        mode_value = PlanMode(mode) if mode else None
    except ValueError as exc:
        raise BadRequestError("Mode ôn tập không hợp lệ.") from exc
    now = datetime.now(timezone.utc)
    items = list_review_items_for_user(
        session,
        user_id=user_id,
        now=now,
        status_filter=status,
        book_id=book_id,
        mode=mode_value,
        limit=limit,
        offset=offset,
    )
    return ReviewListResponse(items=[_to_review_item_response(session, item) for item in items], total=len(items))


def get_review_item_detail(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewItemResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    return _to_review_item_response(session, item)


def _create_next_review_cycle_if_applicable(
    session: Session,
    current_item: SpacedReviewItem,
    now: datetime,
) -> SpacedReviewItem | None:
    next_index = current_item.sequence_index + 1
    if next_index >= len(SPACED_REVIEW_INTERVALS):
        return None

    next_interval_days = SPACED_REVIEW_INTERVALS[next_index]
    
    next_item = SpacedReviewItem(
        user_id=current_item.user_id,
        book_id=current_item.book_id,
        learning_unit_id=current_item.learning_unit_id,
        mode=current_item.mode,
        interval_days=next_interval_days,
        sequence_index=next_index,
        due_at=now + timedelta(days=next_interval_days),
        status=ReviewItemStatus.PENDING,
        review_text_snapshot=current_item.review_text_snapshot,
        anchor_completed_at=current_item.anchor_completed_at,
        source_unit_progress_id=current_item.source_unit_progress_id,
    )
    
    return create_review_item_once(session, next_item)


def complete_review_item(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewActionResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    now = datetime.now(timezone.utc)
    saved = mark_review_item_completed(session, item, completed_at=now)
    _create_next_review_cycle_if_applicable(session, saved, now)
    return ReviewActionResponse(review_item_id=saved.id, status=saved.status, completed_at=saved.completed_at)


def skip_review_item(session: Session, *, user_id: uuid.UUID, review_item_id: uuid.UUID) -> ReviewActionResponse:
    item = get_review_item_for_user(session, user_id=user_id, review_item_id=review_item_id)
    if not item:
        raise ReviewItemNotFoundError()
    now = datetime.now(timezone.utc)
    saved = mark_review_item_skipped(session, item, skipped_at=now)
    _create_next_review_cycle_if_applicable(session, saved, now)
    return ReviewActionResponse(review_item_id=saved.id, status=saved.status, completed_at=saved.completed_at)

```

### app\services\spaced_review_service.py

```py
import uuid
from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.constant import PlanMode, ReviewItemStatus
from app.models.db_models import SpacedReviewItem
from app.repositories.spaced_review_repo import (
    cancel_unanchored_review_items_for_unit,
    create_review_item_once,
    has_active_review_chain_for_unit,
)

SPACED_REVIEW_INTERVALS = [1, 3, 7, 14, 30]


def create_spaced_reviews_after_unit_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    mode: PlanMode | str,
    review_text: str,
    completed_at: datetime,
    source_unit_progress_id: uuid.UUID,
) -> list[SpacedReviewItem]:
    clean_review_text = review_text.strip()
    if not clean_review_text:
        return []

    cancel_unanchored_review_items_for_unit(session, user_id=user_id, learning_unit_id=learning_unit_id)
    if has_active_review_chain_for_unit(session, user_id=user_id, learning_unit_id=learning_unit_id):
        return []

    mode_value = PlanMode(mode)
    first_interval_days = SPACED_REVIEW_INTERVALS[0]
    
    item = SpacedReviewItem(
        user_id=user_id,
        book_id=book_id,
        learning_unit_id=learning_unit_id,
        mode=mode_value,
        interval_days=first_interval_days,
        sequence_index=0,
        due_at=completed_at + timedelta(days=first_interval_days),
        status=ReviewItemStatus.PENDING,
        review_text_snapshot=clean_review_text,
        anchor_completed_at=completed_at,
        source_unit_progress_id=source_unit_progress_id,
    )
    created_item = create_review_item_once(session, item)
    return [created_item] if created_item else []


```

### app\services\storage_service.py

```py
"""
app/services/storage_service.py
=================================
Utility service để upload file lên Supabase Storage.

Trước đây là app/helper/upload2supabase.py.
Di chuyển vào services/ để thống nhất cấu trúc dự án.
"""

import asyncio

import aiofiles

from app.core.logger import log as logger
from app.core.supabase import supabase


async def upload_file_to_supabase(
    local_path: str,
    storage_path: str,
    bucket: str,
    content_type: str,
    max_retries: int = 3,
    upsert: bool = True,
) -> str:
    """
    Upload file lên Supabase Storage và trả về public URL.

    Args:
        local_path: Đường dẫn file local cần upload.
        storage_path: Đường dẫn đích trong bucket.
        bucket: Tên bucket Supabase (vd: "raw_books", "audios").
        content_type: MIME type của file.
        max_retries: Số lần retry nếu upload thất bại (default 3).
        upsert: Ghi đè nếu file đã tồn tại (default True — cần cho switch-mode).

    Returns:
        Public URL của file sau khi upload thành công.
    """
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            await asyncio.to_thread(
                supabase.storage.from_(bucket).upload,
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
            )
            return supabase.storage.from_(bucket).get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2**attempt
                logger.warning(f"Upload failed (attempt {attempt + 1}/{max_retries}), retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise

```

### app\services\study_context_service.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import BadRequestError, BookNotFoundError, StudyContextNotFoundError, ThreadNotFoundError
from app.models.db_models import ChatMessage, ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.audiobook_repo import get_book_by_id
from app.repositories.study_context_document_link_repo import create_new_context_document
from app.repositories.study_context_repo import create_study_context, get_study_context, get_study_contexts
from app.repositories.study_context_thread_repo import (
    create_new_thread,
    delete_thread,
    get_chat_history_by_thread_id,
    get_chat_threads_for_context,
    get_or_create_thread_for_book_repo,
    update_thread_by_id_repo,
)
from app.schemas.study_context import ChatThreadInput, StudyContextDocumentInput, StudyContextInput, StudyContextUpdate


def _get_owned_context(session: Session, context_id: uuid.UUID, user_id: uuid.UUID) -> StudyContext:
    """Helper: Lấy context và kiểm tra ownership. Raise nếu không tìm thấy hoặc không thuộc user."""
    context = get_study_context(session, context_id)
    if not context or context.user_id != user_id:
        raise StudyContextNotFoundError()
    return context


def _get_owned_thread(session: Session, thread_id: uuid.UUID, user_id: uuid.UUID) -> ChatThread:
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()
    _get_owned_context(session, thread.context_id, user_id)
    return thread


def get_documents_in_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list[dict]:
    """Lấy danh sách các tài liệu trong context sau khi kiểm tra quyền sở hữu."""
    context = _get_owned_context(session, context_id, user_id)
    from app.services.audiobook_service import _book_to_response_dict

    return [_book_to_response_dict(session, book) for book in context.books]


def list_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return get_study_contexts(session, user_id)


def create_context(session: Session, user_id: uuid.UUID, payload: StudyContextInput) -> StudyContext:
    """Tạo mới một StudyContext cho user."""
    context = StudyContext(
        user_id=user_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_study_context(session, context)


def update_thread_by_id(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID, title: str) -> ChatThread:
    _get_owned_thread(session, thread_id, user_id)
    updated = update_thread_by_id_repo(session, thread_id, title)
    if not updated:
        raise ThreadNotFoundError("Không thể cập nhật thread.")
    return updated


def delete_thread_by_id(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> None:
    _get_owned_thread(session, thread_id, user_id)
    delete_thread(session, thread_id)


def get_thread_messages(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> list[ChatMessage]:
    thread = _get_owned_thread(session, thread_id, user_id)
    return get_chat_history_by_thread_id(session, thread.id)


def get_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> StudyContext:
    """Lấy context và kiểm tra ownership. Dùng cho router GET."""
    return _get_owned_context(session, context_id, user_id)


def update_context_title(session: Session, user_id: uuid.UUID, context_id: uuid.UUID, payload: StudyContextUpdate) -> StudyContext:
    """Validate ownership rồi cập nhật title."""
    from app.repositories.study_context_repo import update_study_context

    if payload.title is None:
        raise BadRequestError("Thiếu title để cập nhật Study Context.")
    _get_owned_context(session, context_id, user_id)
    updated = update_study_context(session, context_id, payload.title)
    if not updated:
        raise StudyContextNotFoundError()
    return updated


def delete_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> None:
    """Validate ownership rồi xóa context."""
    from app.repositories.study_context_repo import delete_study_context

    _get_owned_context(session, context_id, user_id)
    delete_study_context(session, context_id)


def add_document_to_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: StudyContextDocumentInput,
) -> StudyContextDocumentLink:
    """Validate book và context, sau đó tạo link giữa context và document."""
    book = get_book_by_id(session, payload.book_id)
    if not book or book.user_id != user_id:
        raise BookNotFoundError()

    _get_owned_context(session, context_id, user_id)

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


def delete_document_from_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    book_id: uuid.UUID,
) -> None:
    """Validate ownership rồi xóa document link."""
    from app.repositories.study_context_document_link_repo import delete_study_context_document

    _get_owned_context(session, context_id, user_id)
    delete_study_context_document(session, context_id, book_id)


def get_threads_for_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list:
    """Validate ownership rồi trả về danh sách threads."""
    _get_owned_context(session, context_id, user_id)
    return get_chat_threads_for_context(session, context_id)


def create_thread(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: ChatThreadInput,
) -> ChatThread:
    """Validate context ownership rồi tạo mới ChatThread."""
    _get_owned_context(session, context_id, user_id)

    context = _get_owned_context(session, context_id, user_id)
    if context.is_auto_generated:
        raise BadRequestError("Không thể tạo thêm thread cho Direct Book Context.")

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)


def get_or_create_thread_for_book(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str):
    book = get_book_by_id(session, book_id)
    if not book or book.user_id != user_id:
        raise BookNotFoundError()
    ctx_id, thread_id = get_or_create_thread_for_book_repo(session, user_id, book_id, title=title)
    return {"context_id": str(ctx_id), "thread_id": str(thread_id), "is_auto_generated": True}

```

### app\services\token_budget_service.py

```py
from dataclasses import dataclass

import tiktoken

from app.core.config import settings


@dataclass(frozen=True)
class TextBudget:
    char_count: int
    estimated_tokens: int
    estimated_audio_seconds: int


_encoding = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return len(_encoding.encode(text))


def estimate_audio_seconds(text: str) -> int:
    """
    Conservative Vietnamese speech estimate.

    130 words/minute avoids underestimating long audio generation cost.
    """
    words = len(text.split())
    if words == 0:
        return 0
    return int(words / 130 * 60)


def estimate_text_budget(text: str) -> TextBudget:
    return TextBudget(
        char_count=len(text or ""),
        estimated_tokens=estimate_tokens(text),
        estimated_audio_seconds=estimate_audio_seconds(text),
    )


def exceeds_hard_limit(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT


def should_chunk(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_SOFT_TOKEN_LIMIT

```

### app\services\tts_script_quality_service.py

```py
import re
from dataclasses import dataclass

_STAGE_TAG_RE = re.compile(r"\[(?:[A-Za-zÀ-ỹ_ -]{2,40})\]")
_HEADING_RE = re.compile(r"(?m)^\s*#{1,6}\s*")
_BULLET_RE = re.compile(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+")
_BLOCKQUOTE_RE = re.compile(r"(?m)^\s*>\s?")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_CITATION_RE = re.compile(r"(?<!\w)\[\d{1,4}\](?!\w)")
_HTML_TAG_RE = re.compile(r"</?[^>]+>")
_SPACE_BEFORE_PUNCTUATION_RE = re.compile(r"\s+([.,;:!?])")
_MULTISPACE_RE = re.compile(r"\s+")
_MARKDOWN_ARTIFACT_RE = re.compile(r"(\*\*|__|`{1,3}|~~|^\s*#{1,6}\s+|^\s*(?:[-*+]|\d+[.)])\s+)", re.MULTILINE)
_ACRONYM_RE = re.compile(
    r"(?<![\w])(?:[A-Z]{2,}-[A-Za-z0-9]+|[A-Z][A-Z0-9]{2,}(?:[-/.][A-Z0-9]{1,})*)(?![\w])"
)


@dataclass(frozen=True)
class TTSQualityReport:
    markdown_artifacts: int
    unexplained_acronyms: tuple[str, ...]

    @property
    def has_warnings(self) -> bool:
        return self.markdown_artifacts > 0 or bool(self.unexplained_acronyms)


def sanitize_tts_script_text(text: str) -> str:
    """Remove visual markup that should never reach an audio renderer."""
    cleaned = text or ""
    cleaned = _IMAGE_RE.sub(r"\1", cleaned)
    cleaned = _LINK_RE.sub(r"\1", cleaned)
    cleaned = _STAGE_TAG_RE.sub("", cleaned)
    cleaned = _HEADING_RE.sub("", cleaned)
    cleaned = _BULLET_RE.sub("", cleaned)
    cleaned = _BLOCKQUOTE_RE.sub("", cleaned)
    cleaned = _CITATION_RE.sub("", cleaned)
    cleaned = _HTML_TAG_RE.sub("", cleaned)
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("__", "")
    cleaned = cleaned.replace("~~", "")
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("|", ", ")
    cleaned = cleaned.replace("•", ". ")
    cleaned = _MULTISPACE_RE.sub(" ", cleaned)
    cleaned = _SPACE_BEFORE_PUNCTUATION_RE.sub(r"\1", cleaned)
    return cleaned.strip()


def sanitize_tts_script_list(scripts: list[str]) -> list[str]:
    return [cleaned for script in scripts if (cleaned := sanitize_tts_script_text(script))]


def has_markdown_artifacts(text: str) -> bool:
    return bool(_MARKDOWN_ARTIFACT_RE.search(text or ""))


def _looks_explained(context: str, acronym: str) -> bool:
    lower_context = context.lower()
    lower_acronym = acronym.lower()
    explanation_markers = (
        f"gọi tắt là {lower_acronym}",
        f"viết tắt là {lower_acronym}",
        f"tức là {lower_acronym}",
        f"{lower_acronym}, một ",
        f"{lower_acronym}, là ",
        f"{lower_acronym} là ",
        f"{lower_acronym}, bộ ",
        f"{lower_acronym}, bài ",
        f"{lower_acronym}, phương pháp ",
        f"{lower_acronym}, kỹ thuật ",
    )
    if any(marker in lower_context for marker in explanation_markers):
        return True

    acronym_pos = context.find(acronym)
    if acronym_pos == -1:
        return False

    before = context[max(0, acronym_pos - 100) : acronym_pos]
    after = context[acronym_pos + len(acronym) : acronym_pos + len(acronym) + 120]
    if "(" in before and ")" in after:
        return True
    if before.rstrip().endswith((" -", " –", " —")) or after.lstrip().startswith(("- ", "– ", "— ")):
        return True
    return False


def find_unexplained_acronyms(texts: list[str], *, max_items: int = 8) -> tuple[str, ...]:
    combined = " ".join(texts)
    seen: set[str] = set()
    warnings: list[str] = []
    for match in _ACRONYM_RE.finditer(combined):
        acronym = match.group(0).strip(".,;:!?")
        if acronym in seen or len(acronym) < 3:
            continue
        seen.add(acronym)
        window = combined[max(0, match.start() - 140) : match.end() + 160]
        if not _looks_explained(window, acronym):
            warnings.append(acronym)
            if len(warnings) >= max_items:
                break
    return tuple(warnings)


def inspect_tts_script_quality(texts: list[str]) -> TTSQualityReport:
    raw_text = " ".join(texts)
    return TTSQualityReport(
        markdown_artifacts=len(_MARKDOWN_ARTIFACT_RE.findall(raw_text)),
        unexplained_acronyms=find_unexplained_acronyms(texts),
    )

```

### app\services\tts_service.py

```py
import asyncio
from pathlib import Path

import edge_tts

from app.core.config import settings
from app.core.exceptions import ExternalServiceError, TTSInputTooShortError
from app.core.logger import log
from app.services.async_limiter import get_loop_semaphore
from app.services.tts_script_quality_service import sanitize_tts_script_text

SUPPORTED_TTS_PROVIDERS = {"edge", "google", "gg"}
_google_tts_client = None


def _clean_text_for_tts(text: str) -> str:
    return sanitize_tts_script_text(text)


def _utf8_size(text: str) -> int:
    return len(text.encode("utf-8"))


def _validate_tts_text(text: str) -> None:
    if len(text) < settings.TTS_MIN_TEXT_CHARS:
        raise TTSInputTooShortError(f"Nội dung quá ngắn để tạo audio ({len(text)} ký tự).")


def _selected_tts_provider() -> str:
    provider = settings.TTS_PROVIDER.strip().lower()
    if provider not in SUPPORTED_TTS_PROVIDERS:
        raise ExternalServiceError(f"TTS_PROVIDER không hợp lệ: {settings.TTS_PROVIDER}")
    return "google" if provider == "gg" else provider


def _validate_provider_config(provider: str, text: str) -> None:
    if provider != "google":
        return
    if not settings.TTS_GOOGLE_API_KEY:
        raise ExternalServiceError("Thiếu TTS_GOOGLE_API_KEY để gọi Google Text-to-Speech.")
    byte_count = _utf8_size(text)
    if byte_count > settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST:
        raise ExternalServiceError(
            "Google TTS input quá dài cho một request "
            f"({byte_count} bytes > {settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST} bytes)."
        )


def _get_google_tts_client():
    global _google_tts_client

    if _google_tts_client is not None:
        return _google_tts_client

    try:
        from google.api_core.client_options import ClientOptions
        from google.cloud import texttospeech
    except ImportError as exc:
        raise ExternalServiceError("Thiếu dependency google-cloud-texttospeech.") from exc

    if not settings.TTS_GOOGLE_API_KEY:
        raise ExternalServiceError("Thiếu TTS_GOOGLE_API_KEY để gọi Google Text-to-Speech.")

    options = ClientOptions(api_key=settings.TTS_GOOGLE_API_KEY)
    _google_tts_client = texttospeech.TextToSpeechClient(client_options=options)
    return _google_tts_client


def _measure_mp3_duration_ms(filename: str) -> int:
    from mutagen.mp3 import MP3

    try:
        audio = MP3(filename)
        return int(audio.info.length * 1000)
    except Exception:
        return 0


def _retry_wait_seconds(attempt: int) -> int:
    return settings.TTS_RETRY_BASE_SECONDS * (2**attempt)


def _safe_tts_error(exc: Exception) -> str:
    message = str(exc)
    if settings.TTS_GOOGLE_API_KEY:
        message = message.replace(settings.TTS_GOOGLE_API_KEY, "[REDACTED]")
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


async def _generate_audio_file_edge(text: str, filename: str, voice_name: str) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text,
        voice_name,
        receive_timeout=settings.TTS_RECEIVE_TIMEOUT_SECONDS,
    )
    await communicate.save(filename)


def _generate_audio_file_google_sync(text: str, filename: str, voice_name: str) -> int:
    from google.cloud import texttospeech

    _validate_provider_config("google", text)
    client = _get_google_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=settings.GOOGLE_TTS_LANGUAGE_CODE,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    Path(filename).write_bytes(response.audio_content)
    return len(response.audio_content)


async def generate_audio_file_edge(text: str, filename: str, voice: str = settings.EDGE_TTS_VOICE):
    cleaned = _clean_text_for_tts(text)
    _validate_tts_text(cleaned)
    await _generate_audio_file_edge(cleaned, filename, voice)
    log.info("Edge TTS file generated | chars={} | bytes={} | voice={}", len(cleaned), _utf8_size(cleaned), voice)


async def generate_audio_and_get_duration(
    text: str,
    filename: str,
    voice: str | None = None,
    max_retries: int = 6,
) -> int:
    cleaned = _clean_text_for_tts(text)
    _validate_tts_text(cleaned)
    provider = _selected_tts_provider()
    _validate_provider_config(provider, cleaned)
    target_voice = voice or (settings.GOOGLE_TTS_VOICE if provider == "google" else settings.EDGE_TTS_VOICE)

    async with get_loop_semaphore("tts_generation", settings.TTS_GENERATION_CONCURRENCY):
        for attempt in range(max_retries):
            try:
                if provider == "google":
                    audio_bytes = await asyncio.to_thread(
                        _generate_audio_file_google_sync,
                        cleaned,
                        filename,
                        target_voice,
                    )
                    if settings.GOOGLE_TTS_ENABLE_COST_LOG:
                        log.info(
                            "Google TTS generated | chars={} | bytes={} | audio_bytes={} | voice={}",
                            len(cleaned),
                            _utf8_size(cleaned),
                            audio_bytes,
                            target_voice,
                        )
                else:
                    await _generate_audio_file_edge(cleaned, filename, target_voice)
                    log.info(
                        "Edge TTS generated | chars={} | bytes={} | voice={}",
                        len(cleaned),
                        _utf8_size(cleaned),
                        target_voice,
                    )

                return _measure_mp3_duration_ms(filename)

            except Exception as exc:
                if attempt < max_retries - 1:
                    wait = _retry_wait_seconds(attempt)
                    log.warning(
                        "TTS attempt failed | provider={} | attempt={}/{} | chars={} | wait_seconds={} | error={}",
                        provider,
                        attempt + 1,
                        max_retries,
                        len(cleaned),
                        wait,
                        _safe_tts_error(exc),
                    )
                    await asyncio.sleep(wait)
                else:
                    log.error(
                        "TTS failed | provider={} | attempts={} | chars={} | voice={} | error={}",
                        provider,
                        max_retries,
                        len(cleaned),
                        target_voice,
                        _safe_tts_error(exc),
                    )
                    raise
    return 0  # unreachable

```

### app\services\upload_service.py

```py
import os
import uuid
from typing import Optional

import aiofiles
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, DocumentType, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import (
    AppException,
    BookNotFoundError,
    BookStatusConflictError,
    DatabaseError,
    DocumentExtractionError,
    ExternalServiceError,
    FileTooLargeError,
    ReadingPlanScheduleConflictError,
    UnsupportedFileTypeError,
)
from app.core.logger import log as logger
from app.models.db_models import Book, LearningUnit, ProcessingJob, ReadingPlan
from app.repositories.audiobook_repo import update_book_status
from app.repositories.book_section_repo import create_book_sections, list_book_sections
from app.repositories.learning_unit_repo import create_learning_units
from app.repositories.processing_job_repo import update_processing_job
from app.repositories.reading_plan_schedule_repo import list_slots_for_plan
from app.schemas.plan import PlanInput
from app.services.document_parser_service import parse_document_structure
from app.services.document_structure_service import build_outline_preview, detect_structure_warnings, validate_document_structure
from app.services.document_structure_types import flatten_sections
from app.services.learning_unit_planner_service import plan_learning_units_async
from app.services.reading_plan_schedule_service import WEEKDAY_LABELS, WEEKDAY_SHORT_LABELS, build_slots_for_plan, validate_plan_schedule_for_activation, validate_plan_schedule_shape
from app.services.reading_plan_session_service import build_plan_session_summary, ensure_future_sessions_for_plan
from app.services.storage_service import upload_file_to_supabase
from app.tasks.book_tasks import index_book_sections_task, process_book_task

# HELPER FUNCTION: Detect document type based on MIME type or file extension


def _detect_document_type(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if filename.endswith(".pdf") or content_type == "application/pdf":
        return DocumentType.PDF.value
    if filename.endswith(".epub") or content_type == "application/epub+zip":
        return DocumentType.EPUB.value
    if filename.endswith(".docx") or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return DocumentType.DOCX.value

    raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")


async def _planned_units_for_book(session: Session, book_id: uuid.UUID, mode) -> list:
    sections = list_book_sections(session, book_id)
    if not sections:
        return []

    planned_units = await plan_learning_units_async(sections, mode)
    if not planned_units:
        raise DocumentExtractionError("Không tạo được bài học từ cấu trúc tài liệu.")
    return planned_units


def _enqueue_section_indexing(book_id: uuid.UUID) -> None:
    if not settings.BOOK_SECTION_INDEXING_ENABLED:
        return
    try:
        index_book_sections_task.apply_async(args=[str(book_id)], queue="document")
    except Exception as exc:
        logger.warning(f"BookSectionKnowledge indexing enqueue failed | book_id={book_id} | reason={type(exc).__name__}")


def _slot_response(slot) -> dict:
    return {
        "id": str(slot.id),
        "weekday": slot.weekday,
        "weekday_label": WEEKDAY_LABELS.get(slot.weekday, str(slot.weekday)),
        "reminder_time": slot.reminder_time,
        "timezone": slot.timezone,
        "is_active": slot.is_active,
    }


async def _create_plan_and_job_async(
    session: Session,
    *,
    book: Book,
    payload: PlanInput,
    user_id: uuid.UUID,
    slots: list,
    resolved_reminder_time: str,
    plan_status: PlanStatus,
) -> tuple[Optional[ProcessingJob], list, ReadingPlan]:

    # Kiểm tra xem các bài học (LearningUnits) cho chế độ này đã được clone/tạo sẵn chưa
    existing_units = session.exec(select(LearningUnit).where(LearningUnit.book_id == payload.book_id, LearningUnit.mode == payload.mode)).all()

    plan = ReadingPlan(
        book_id=payload.book_id,
        mode=payload.mode,
        pace=payload.pace,
        status=plan_status.value,
        reminder_time=resolved_reminder_time,
    )
    session.add(plan)
    session.flush()

    for slot in build_slots_for_plan(
        user_id=user_id,
        book_id=payload.book_id,
        plan_id=plan.id,
        slots=slots,
        is_active=plan_status == PlanStatus.ACTIVE,
    ):
        session.add(slot)

    planned_units = []
    # Nếu CHƯA có bài học nào (Sách gốc tự upload), tiến hành lập kế hoạch học phần mới
    if not existing_units:
        planned_units = await _planned_units_for_book(session, payload.book_id, payload.mode)
        if planned_units:
            created_units = create_learning_units(
                session,
                user_id=user_id,
                book_id=payload.book_id,
                mode=payload.mode,
                planned_units=planned_units,
            )
            # Cập nhật thông minh tránh ghi đè số lượng lớn hơn của FULL mode
            book.total_units = max(book.total_units or 0, len(created_units))
    else:
        # Have book clone, save it don't change it. Update total_units
        book.total_units = max(book.total_units or 0, len(existing_units))

    if plan.status == PlanStatus.ACTIVE.value:
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)

    job = None
    # Chỉ tạo Job xử lý nền và chạy Celery nếu CHƯA có bài học sẵn
    if not existing_units:
        job = ProcessingJob(
            user_id=user_id,
            book_id=payload.book_id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.QUEUED,
            mode=payload.mode,
            total_units=len(planned_units) if planned_units else book.total_units or 0,
            done_units=0,
            progress_percent=0,
            current_step="Đang chờ xử lý sách.",
        )
        session.add(job)
        book.status = BookStatus.PROCESSING

    session.add(book)  # Đảm bảo luôn lưu thay đổi của book (bao gồm cả total_units ở nhánh else)
    return job, planned_units, plan


# Dispatcher function to extract document structure based on document type
async def _extract_structure_by_type(tmp_filename: str, document_type: str):
    with open(tmp_filename, "rb") as f:
        return await parse_document_structure(f, document_type)


async def handle_upload_document(session: Session, file: UploadFile, user_id: uuid.UUID) -> dict:
    """
    Bước 1: Validate file, extract outline từ tài liệu, upload lên Supabase Storage,
    lưu Book + BookSection vào DB, trả về outline tree cho Flutter.
    """
    # 1. Validate MIME Type hoặc đuôi file
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()
    document_type = _detect_document_type(file)

    if not is_valid_type:
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError()

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)

    parsed_document = None
    file_url = ""
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract deterministic outline tree từ tài liệu
        parsed_document = await _extract_structure_by_type(tmp_filename, document_type)
        validate_document_structure(parsed_document)
        flat_sections = flatten_sections(parsed_document.sections)
        if not flat_sections:
            raise DocumentExtractionError()

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.{document_type}"
        content_type = (
            file.content_type
            or {
                "pdf": "application/pdf",
                "epub": "application/epub+zip",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }[document_type]
        )

        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type=content_type,
        )
        logger.info(f"☁️  {document_type.upper()} uploaded to Storage: {storage_path}")

    finally:
        # Dọn rác: Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    if not parsed_document:
        raise DocumentExtractionError()

    flat_sections = flatten_sections(parsed_document.sections)
    warnings = detect_structure_warnings(parsed_document)

    # 5. Lưu DB: Book (DRAFT) + BookSection tree
    title = (file.filename or "unknown").rsplit(".", 1)[0]
    try:
        book = Book(
            id=book_id,
            user_id=user_id,
            title=title,
            total_sections=len(flat_sections),
            total_units=0,
            status=BookStatus.DRAFT,
            file_url=file_url,
            document_type=document_type,
        )

        session.add(book)
        session.flush()
        create_book_sections(session, book_id, parsed_document)
        session.commit()
        logger.info(f"📘 Created DRAFT book {book_id} | {len(flat_sections)} sections | file_url saved")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    _enqueue_section_indexing(book_id)

    outline_tree = build_outline_preview(parsed_document)
    return {
        "book_id": str(book_id),
        "total_sections": len(flat_sections),
        "max_depth": parsed_document.max_depth,
        "outline_tree": outline_tree,
        "warnings": warnings,
        "document_type": document_type,
    }


async def handle_generate_plan(session: Session, payload: PlanInput, user_id: uuid.UUID) -> dict:
    """
    Bước 2: Validate trạng thái sách, tạo ReadingPlan, tạo progress job,
    kick-off background processing.
    """
    # 1. Validate book tồn tại và đang ở trạng thái DRAFT hoặc là sách clone READY
    book = session.exec(select(Book).where(Book.id == payload.book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()
    if book.status not in (BookStatus.DRAFT,) and book.parent_shared_id is None:
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    if payload.activate:
        slots = validate_plan_schedule_for_activation(
            session,
            user_id=user_id,
            schedule_config=payload.schedule_config,
            reminder_time=payload.reminder_time,
        )
        plan_status = PlanStatus.ACTIVE
        slots_to_create = slots
    else:
        slots = validate_plan_schedule_shape(
            session,
            user_id=user_id,
            schedule_config=payload.schedule_config,
            reminder_time=payload.reminder_time,
        )
        plan_status = PlanStatus.INACTIVE
        slots_to_create = slots
    resolved_reminder_time = slots[0].reminder_time

    # 2. Lưu ReadingPlan + schedule slots + learning units + progress job
    try:
        job, planned_units, plan = await _create_plan_and_job_async(
            session,
            book=book,
            payload=payload,
            user_id=user_id,
            slots=slots_to_create,
            resolved_reminder_time=resolved_reminder_time,
            plan_status=plan_status,
        )
        session.commit()
        if job:
            session.refresh(job)
        session.refresh(plan)

        job_id_str = str(job.id) if job else "N/A"
        logger.info(f"📋 ReadingPlan created for book {payload.book_id} | mode={payload.mode.value} | job={job_id_str}")
    except IntegrityError as e:
        session.rollback()
        raise ReadingPlanScheduleConflictError() from e
    except AppException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    if job:
        try:
            process_book_task.apply_async(
                args=[str(payload.book_id), payload.mode.value, str(job.id)],
                queue="document",
            )
        except Exception as e:
            update_processing_job(
                session,
                job.id,
                status=ProcessingJobStatus.ERROR,
                current_step="Không thể đưa sách vào hàng đợi xử lý.",
                error_message=str(e),
            )
            update_book_status(session, payload.book_id, BookStatus.ERROR, "Không thể đưa sách vào hàng đợi xử lý.")
            raise ExternalServiceError("Không thể đưa sách vào hàng đợi xử lý. Vui lòng thử lại sau.") from e

    return {
        "message": "Kế hoạch học tập đã được tạo! " + ("Chúng tôi đang xử lý sách của bạn." if job else "Sách đã sẵn sàng để học."),
        "book_id": str(payload.book_id),
        "plan_id": str(plan.id),
        "job_id": str(job.id) if job else None,
        "mode": payload.mode.value,
        "plan_status": plan.status,
        "pace": plan.pace,
        "schedule_config": [
            WEEKDAY_SHORT_LABELS.get(slot.weekday, str(slot.weekday))
            for slot in list_slots_for_plan(session, plan_id=plan.id, active_only=False)
        ],
        "reminder_time": plan.reminder_time,
        "status": job.status if job else "ready",
        "progress_percent": job.progress_percent if job else 100,
        "active_slots": [_slot_response(slot) for slot in list_slots_for_plan(session, plan_id=plan.id, active_only=True)] if plan.status == PlanStatus.ACTIVE.value else [],
        "session_summary": build_plan_session_summary(session, plan_id=plan.id),
        "planned_units": [
            {
                "unit_index": index,
                "title": unit.title,
                "unit_type": unit.unit_type,
                "source_section_count": len(unit.source_section_ids),
                "estimated_audio_seconds": unit.estimated_audio_seconds,
            }
            for index, unit in enumerate(planned_units)
        ],
    }

```

### app\services\voice_agent\contracts.py

```py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

LK_CHAT_TOPIC = "lk.chat"
LK_CONTROL_TOPIC = "lk.control"
LK_TRANSCRIPT_TOPIC = "lk.transcript"

TranscriptRole = Literal["user", "assistant"]
WebPermissionIntent = Literal["grant", "deny", "unclear", "new_question"]


@dataclass(frozen=True)
class VoiceJobMetadata:
    thread_id: str
    document_ids: list[str]


@dataclass(frozen=True)
class VoiceRagResult:
    found: bool
    chunks: list[dict[str, Any]]
    message: str


@dataclass(frozen=True)
class WebSearchPermissionDecision:
    granted_query: str | None = None
    denied: bool = False
    unclear: bool = False
    new_question: str | None = None


@dataclass(frozen=True)
class WebPermissionIntentResult:
    intent: WebPermissionIntent
    confidence: float
    reason: str = ""
    source: str = "classifier"


@dataclass
class WebSearchPermissionState:
    enabled: bool = False
    pending_query: str | None = None
    pending_request_id: str | None = None
    last_user_reply: str | None = None
    last_user_reply_at: datetime | None = None
    granted_query: str | None = None
    granted_request_id: str | None = None
    granted_at: datetime | None = None

```

### app\services\voice_agent\query_guard.py

```py
from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.agent_grounding.contracts import GroundingIntent
from app.services.agent_grounding.query_normalizer import normalize_query, normalized_key, tokenize
from app.services.agent_grounding.section_reference_parser import parse_section_reference
from app.services.voice_agent.turn_state import PendingVoiceClarification, VoiceTranscriptSnapshot
from app.services.voice_agent.voice_intent_classifier import VoiceReplyIntentResult, classify_voice_reply_intent_fast_path
from app.services.voice_agent.web_permission_intent_classifier import classify_web_permission_intent_fast_path

_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,}(?:[-_/][A-Z0-9]{2,})*\b")
_QUOTED_RE = re.compile(r"[\"'“”‘’]([^\"'“”‘’]{2,})[\"'“”‘’]")

_STOPWORDS = {
    "a",
    "about",
    "an",
    "and",
    "anh",
    "ạ",
    "ban",
    "book",
    "can",
    "cho",
    "co",
    "could",
    "cua",
    "cuon",
    "de",
    "duoc",
    "em",
    "giup",
    "hay",
    "ho",
    "i",
    "is",
    "la",
    "lai",
    "me",
    "minh",
    "nay",
    "noi",
    "please",
    "quyen",
    "sach",
    "the",
    "this",
    "toi",
    "trong",
    "ve",
    "vui",
    "with",
    "you",
}

_ACK_ONLY_CLARIFICATION = "Bạn muốn hỏi nội dung nào trong sách?"
_MISSING_SECTION_CLARIFICATION = "Bạn muốn hỏi chương hoặc đề mục nào?"
_MISMATCH_CLARIFICATION = "Mình nghe chưa chắc câu hỏi. Bạn nói lại ngắn gọn giúp mình nhé."


GENERIC_CLARIFICATION_REASON_CODES = frozenset(
    {
        "too_short_or_ack_only",
    }
)


@dataclass(frozen=True)
class VoiceQueryGuardConfig:
    min_chars: int = 6
    min_tokens: int = 2
    clarification_confirmation_max_tokens: int = 4
    clarification_min_query_prompt_overlap: float = 0.45


@dataclass(frozen=True)
class VoiceQueryGuardResult:
    valid: bool
    reason_code: str
    clarification: str | None = None
    token_count: int = 0
    important_token_count: int = 0
    overlap_ratio: float | None = None
    important_overlap_ratio: float | None = None
    transcript_source: str | None = None
    guard_mode: str = "normal"
    pending_reason_code: str | None = None


def _content_tokens(text: str) -> set[str]:
    return {token for token in tokenize(normalized_key(text)) if token not in _STOPWORDS}


def _important_tokens(text: str) -> set[str]:
    normalized = normalize_query(text)
    important = {token for token in normalized.tokens if token not in _STOPWORDS and (len(token) >= 4 or any(character.isdigit() for character in token))}
    for acronym in _ACRONYM_RE.findall(text):
        important.update(tokenize(normalized_key(acronym)))
    for quoted in _QUOTED_RE.findall(text):
        important.update(token for token in tokenize(normalized_key(quoted)) if token not in _STOPWORDS)
    return important


def _ratio(matched_count: int, denominator_count: int) -> float:
    return matched_count / max(1, denominator_count)


def _invalid(
    reason_code: str,
    clarification: str,
    *,
    token_count: int,
    important_token_count: int,
    overlap_ratio: float | None = None,
    important_overlap_ratio: float | None = None,
    transcript_source: str | None = None,
    guard_mode: str = "normal",
    pending_reason_code: str | None = None,
) -> VoiceQueryGuardResult:
    return VoiceQueryGuardResult(
        valid=False,
        reason_code=reason_code,
        clarification=clarification,
        token_count=token_count,
        important_token_count=important_token_count,
        overlap_ratio=overlap_ratio,
        important_overlap_ratio=important_overlap_ratio,
        transcript_source=transcript_source,
        guard_mode=guard_mode,
        pending_reason_code=pending_reason_code,
    )


def _query_matches_pending_clarification(
    query: str,
    pending: PendingVoiceClarification,
    *,
    min_ratio: float,
) -> bool:
    query_tokens = _content_tokens(query)
    if not query_tokens:
        return False
    query_targets = _section_reference_targets(query)

    candidates = []
    if pending.candidate_query:
        candidates.append(pending.candidate_query)
    candidates.append(pending.prompt_text)

    for candidate in candidates:
        candidate_tokens = _content_tokens(candidate)
        if not candidate_tokens:
            continue
        candidate_targets = _section_reference_targets(candidate)
        if query_targets and candidate_targets and query_targets.isdisjoint(candidate_targets):
            continue
        overlap_ratio = _ratio(len(query_tokens & candidate_tokens), len(query_tokens))
        if overlap_ratio >= min_ratio:
            return True

    return False


def _section_reference_targets(text: str) -> set[str]:
    reference = parse_section_reference(normalize_query(text))
    targets: set[str] = set()
    if reference.explicit_path:
        targets.add(reference.explicit_path)
    if reference.explicit_ordinal is not None:
        targets.add(str(reference.explicit_ordinal))
    return targets


def _valid_clarification_confirmation(
    base_result: VoiceQueryGuardResult,
    transcript: VoiceTranscriptSnapshot,
    pending: PendingVoiceClarification,
) -> VoiceQueryGuardResult:
    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid_clarification_confirmation",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        overlap_ratio=1.0,
        important_overlap_ratio=1.0,
        transcript_source=transcript.source,
        guard_mode="clarification_confirmed",
        pending_reason_code=pending.reason_code,
    )


def _pending_clarification_reply_result(
    query: str,
    transcript: VoiceTranscriptSnapshot,
    base_result: VoiceQueryGuardResult,
    pending: PendingVoiceClarification,
    *,
    config: VoiceQueryGuardConfig,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult | None:
    resolved_reply = reply_intent or classify_voice_reply_intent_fast_path(
        transcript.text,
        max_grant_tokens=config.clarification_confirmation_max_tokens,
    )
    if resolved_reply is None:
        # TRIAM_FIX_ROOT_CAUSE: Since we removed semantic QUESTION_HINTS from the fast-path classifier,
        # a new question might return resolved_reply = None if it doesn't contain an explicit '?'.
        # In this case, we check if the new query matches the pending clarification.
        # If it does, we treat it as a confirmation (grant).
        if _query_matches_pending_clarification(
            query,
            pending,
            min_ratio=config.clarification_min_query_prompt_overlap,
        ):
            return _valid_clarification_confirmation(base_result, transcript, pending)
        # If it does not match, it is a new question.
        return VoiceQueryGuardResult(
            valid=False,
            reason_code="clarification_new_question",
            clarification=None,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_new_question",
            pending_reason_code=pending.reason_code,
        )

    if resolved_reply.intent == "grant":
        is_generic_mismatch = pending.reason_code in GENERIC_CLARIFICATION_REASON_CODES
        if is_generic_mismatch or _query_matches_pending_clarification(
            query,
            pending,
            min_ratio=config.clarification_min_query_prompt_overlap,
        ):
            return _valid_clarification_confirmation(base_result, transcript, pending)
        return _invalid(
            "clarification_query_mismatch",
            _MISMATCH_CLARIFICATION,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_pending",
            pending_reason_code=pending.reason_code,
        )

    if resolved_reply.intent == "deny":
        return _invalid(
            "clarification_denied",
            "Được, bạn muốn hỏi nội dung nào khác?",
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_pending",
            pending_reason_code=pending.reason_code,
        )

    if resolved_reply.intent == "new_question":
        return VoiceQueryGuardResult(
            valid=False,
            reason_code="clarification_new_question",
            clarification=None,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_new_question",
            pending_reason_code=pending.reason_code,
        )

    return _invalid(
        "clarification_reply_unclear",
        "Bạn xác nhận hay muốn hỏi câu khác?",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        transcript_source=transcript.source,
        guard_mode="clarification_pending",
        pending_reason_code=pending.reason_code,
    )


def assess_voice_query(query: str, *, config: VoiceQueryGuardConfig | None = None) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    normalized = normalize_query(query)
    content_tokens = _content_tokens(query)
    important_tokens = _important_tokens(query)
    token_count = len(content_tokens)
    important_token_count = len(important_tokens)

    permission_result = classify_web_permission_intent_fast_path(query)
    if permission_result is not None and permission_result.intent != "new_question":
        return _invalid(
            "permission_reply",
            "Đây có vẻ là câu trả lời cho yêu cầu tìm web trước đó.",
            token_count=token_count,
            important_token_count=important_token_count,
        )

    if len(normalized.normalized) < resolved_config.min_chars or token_count < resolved_config.min_tokens:
        return _invalid(
            "too_short_or_ack_only",
            _ACK_ONLY_CLARIFICATION,
            token_count=token_count,
            important_token_count=important_token_count,
        )

    reference = parse_section_reference(normalized)

    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid",
        token_count=token_count,
        important_token_count=important_token_count,
    )


def compare_query_with_transcript(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
    pending_clarification: PendingVoiceClarification | None = None,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    base_result = assess_voice_query(query, config=resolved_config)
    if not base_result.valid:
        return base_result
    if transcript is None:
        return base_result

    resolved_reply = reply_intent or classify_voice_reply_intent_fast_path(
        transcript.text,
        max_grant_tokens=resolved_config.clarification_confirmation_max_tokens,
    )

    if pending_clarification is not None:
        pending_result = _pending_clarification_reply_result(
            query,
            transcript,
            base_result,
            pending_clarification,
            config=resolved_config,
            reply_intent=resolved_reply,
        )
        if pending_result is not None:
            return pending_result
    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid_transcript_snapshot_available",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        transcript_source=transcript.source,
        guard_mode="transcript_snapshot",
    )


def guard_voice_book_query(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
    pending_clarification: PendingVoiceClarification | None = None,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult:
    return compare_query_with_transcript(
        query,
        transcript,
        config=config,
        pending_clarification=pending_clarification,
        reply_intent=reply_intent,
    )

```

### app\services\voice_agent\rag_context.py

```py
import time
from typing import Any, Awaitable, Callable

from app.core.config import settings
from app.services.agent_observability import AgentInputMode, AgentTurnTracer
from app.services.rag_service import search_book_knowledge
from app.services.voice_agent.contracts import VoiceRagResult

RawRagSearch = Callable[[str, list[str]], Awaitable[Any]]


def trim_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return f"{text[:max_chars].rstrip()}\n...[truncated]"


def normalize_rag_payload(payload: Any) -> VoiceRagResult:
    if not isinstance(payload, list) or not payload:
        return VoiceRagResult(
            found=False,
            chunks=[],
            message="Không tìm thấy thông tin phù hợp trong sách.",
        )

    chunks = [item for item in payload if isinstance(item, dict)]
    if not chunks:
        return VoiceRagResult(
            found=False,
            chunks=[],
            message="Không tìm thấy thông tin phù hợp trong sách.",
        )

    return VoiceRagResult(found=True, chunks=chunks, message="")


def infer_retrieval_method(payload: Any) -> str:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict) and item.get("retrieval_method"):
                return str(item["retrieval_method"])
    return "vector"


async def search_voice_book_context(
    query: str,
    document_ids: list[str],
    *,
    search_fn: RawRagSearch = search_book_knowledge,
    tracer: AgentTurnTracer | None = None,
    input_mode: AgentInputMode = AgentInputMode.VOICE,
) -> VoiceRagResult:
    started = time.perf_counter()
    try:
        payload = await search_fn(query, document_ids)
    except Exception:
        if tracer is not None:
            tracer.record_latency(input_mode, "retrieval", int((time.perf_counter() - started) * 1000))
            tracer.record_error(input_mode, "retrieval_error")
        raise

    if tracer is not None:
        tracer.record_retrieval(
            input_mode,
            payload,
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            method=infer_retrieval_method(payload),
        )
    return normalize_rag_payload(payload)


def format_rag_context(result: VoiceRagResult, *, max_chars: int | None = None) -> str:
    if not result.found:
        return f"BOOK_CONTEXT_NOT_FOUND: {result.message}"

    remaining_chars = settings.VOICE_AGENT_RAG_MAX_CHARS if max_chars is None else max_chars
    formatted_chunks: list[str] = []
    for index, item in enumerate(result.chunks):
        if remaining_chars <= 0:
            break

        unit_id = str(item.get("learning_unit_id") or "")
        section_id = str(item.get("section_id") or "")
        section_path = str(item.get("section_path") or item.get("section_title") or "")
        chunk_index = item.get("chunk_index", "N/A")
        content = trim_text(str(item.get("content", "")), remaining_chars)
        if not content:
            continue

        if section_id:
            source_label = f"Section: {section_path or 'unknown'}"
            source_id = f", Section ID: ...{section_id[-6:]}"
        else:
            source_label = f"Unit ID: ...{unit_id[-6:]}"
            source_id = ""
        formatted_chunks.append(f"--- Source {index + 1} ({source_label}{source_id}, Chunk: {chunk_index}) ---\n{content}")
        remaining_chars -= len(content)

    if not formatted_chunks:
        return f"BOOK_CONTEXT_NOT_FOUND: {result.message or 'Không tìm thấy thông tin phù hợp trong sách.'}"

    return "BOOK_CONTEXT_FOUND:\n" + "\n\n".join(formatted_chunks)


```

### app\services\voice_agent\tool_reply_watchdog.py

```py
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any

from app.core.logger import log
from app.services.agent_observability import AgentInputMode, AgentTurnTracer


@dataclass(frozen=True)
class VoiceToolReplyWatchdogConfig:
    enabled: bool
    grace_seconds: float
    thinking_grace_seconds: float
    monitored_tools: set[str]
    allow_error_outputs: bool = False
    force_tool_choice_none: bool = True


class VoiceToolReplyWatchdog:
    def __init__(
        self,
        *,
        session: Any,
        tracer: AgentTurnTracer,
        config: VoiceToolReplyWatchdogConfig,
    ) -> None:
        self.session = session
        self.tracer = tracer
        self.config = config
        self._watch_tasks: dict[str, asyncio.Task[None]] = {}
        self._watch_tool_names: dict[str, str] = {}
        self._speech_generation_counter = 0
        self._last_tool_completed_monotonic: float | None = None

    def close(self) -> None:
        self.cancel_all("session_close")

    def cancel_all(self, reason: str) -> None:
        if not self._watch_tasks:
            return

        for task in self._watch_tasks.values():
            if not task.done():
                task.cancel()
        self._watch_tasks.clear()
        self._watch_tool_names.clear()
        self.tracer.record_tool_reply_watchdog_cancelled(
            AgentInputMode.VOICE,
            reason=reason,
        )

    def record_speech_created(self, *, source: str | None = None) -> None:
        self._speech_generation_counter += 1
        elapsed_ms = self._elapsed_since_tool_completed_ms()
        self.cancel_all("speech_created")
        self.tracer.record_tool_reply_speech_created(
            AgentInputMode.VOICE,
            source=source,
            elapsed_ms=elapsed_ms,
        )

    def record_agent_state_changed(self, *, new_state: str) -> None:
        state_lower = new_state.lower()
        if state_lower == "speaking":
            self._speech_generation_counter += 1
            self.cancel_all("agent_speaking")
        elif state_lower == "thinking":
            self._extend_grace_for_thinking()

    def _extend_grace_for_thinking(self) -> None:
        active_event_ids = [eid for eid, task in self._watch_tasks.items() if not task.done()]
        if not active_event_ids:
            return

        self._speech_generation_counter += 1
        generation_marker = self._speech_generation_counter

        for event_id in active_event_ids:
            task = self._watch_tasks.get(event_id)
            if task and not task.done():
                task.cancel()

            tool_name = self._watch_tool_names.get(event_id, "unknown")
            log.info(f"Voice tool reply watchdog: agent entered thinking. Extending grace for {tool_name}.")
            self.tracer.record_tool_reply_watchdog_scheduled(
                AgentInputMode.VOICE,
                tool_name=tool_name,
                grace_ms=int(self.config.thinking_grace_seconds * 1000),
            )
            self._watch_tasks[event_id] = asyncio.create_task(
                self._watch_and_force_reply(
                    event_id=event_id,
                    tool_name=tool_name,
                    generation_marker=generation_marker,
                    grace_seconds=self.config.thinking_grace_seconds,
                )
            )

    def record_user_state_changed(self, *, new_state: str) -> None:
        if new_state == "speaking":
            self.cancel_all("user_started_speaking")

    def record_user_transcribed(self) -> None:
        self.cancel_all("user_input_transcribed")

    def schedule_after_tools_executed(self, ev: Any) -> None:
        if not self.config.enabled:
            return
        for call, output in _zipped_tool_outputs(ev):
            tool_name = str(getattr(call, "name", ""))
            if not self._should_watch(tool_name, output):
                continue
            event_id = _tool_event_id(call)
            self._schedule_one(event_id, tool_name)

    def _should_watch(self, tool_name: str, output: Any) -> bool:
        if tool_name not in self.config.monitored_tools:
            return False
        if output is not None and getattr(output, "is_error", False):
            return self.config.allow_error_outputs
        return True

    def _schedule_one(self, event_id: str, tool_name: str) -> None:
        existing = self._watch_tasks.pop(event_id, None)
        if existing and not existing.done():
            existing.cancel()
        self._watch_tool_names[event_id] = tool_name
        self._last_tool_completed_monotonic = time.monotonic()
        generation_marker = self._speech_generation_counter
        self.tracer.record_tool_reply_watchdog_scheduled(
            AgentInputMode.VOICE,
            tool_name=tool_name,
            grace_ms=int(self.config.grace_seconds * 1000),
        )
        self._watch_tasks[event_id] = asyncio.create_task(
            self._watch_and_force_reply(
                event_id=event_id,
                tool_name=tool_name,
                generation_marker=generation_marker,
                grace_seconds=self.config.grace_seconds,
            )
        )

    async def _watch_and_force_reply(
        self,
        *,
        event_id: str,
        tool_name: str,
        generation_marker: int,
        grace_seconds: float,
    ) -> None:
        try:
            await asyncio.sleep(grace_seconds)
            if generation_marker != self._speech_generation_counter:
                self.tracer.record_tool_reply_watchdog_bypassed(
                    AgentInputMode.VOICE,
                    reason="speech_created_before_grace",
                    tool_name=tool_name,
                )
                return

            elapsed_ms = self._elapsed_since_tool_completed_ms()
            self.tracer.record_tool_reply_watchdog_fired(
                AgentInputMode.VOICE,
                tool_name=tool_name,
                elapsed_ms=elapsed_ms,
                reason="no_speech_after_tool",
            )
            self._speech_generation_counter += 1
            self._generate_reply_after_tool()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.tracer.record_error(AgentInputMode.VOICE, "tool_reply_watchdog_error")
            log.warning(
                "Voice tool reply watchdog failed | "
                f"tool={tool_name} | error_type={type(exc).__name__}"
            )
        finally:
            current_task = asyncio.current_task()
            if self._watch_tasks.get(event_id) is current_task:
                self._watch_tasks.pop(event_id, None)
                self._watch_tool_names.pop(event_id, None)

    def _generate_reply_after_tool(self) -> None:
        if not hasattr(self.session, "room") or not self.session.room.isconnected():
            log.info("[Watchdog] Session room is disconnected. Aborting force reply.")
            return

        kwargs: dict[str, Any] = {
            "allow_interruptions": True,
            # "instructions": POST_TOOL_REPLY_INSTRUCTIONS,
        }
        if self.config.force_tool_choice_none:
            kwargs["tool_choice"] = "none"
        self.session.generate_reply(**kwargs)

    def _elapsed_since_tool_completed_ms(self) -> int | None:
        if self._last_tool_completed_monotonic is None:
            return None
        return max(0, int((time.monotonic() - self._last_tool_completed_monotonic) * 1000))


def _zipped_tool_outputs(ev: Any) -> list[tuple[Any, Any]]:
    if hasattr(ev, "zipped"):
        return list(ev.zipped())
    calls = list(getattr(ev, "function_calls", []) or [])
    outputs = list(getattr(ev, "function_call_outputs", []) or [])
    return list(zip(calls, outputs or [None] * len(calls), strict=False))


def _tool_event_id(call: Any) -> str:
    return str(
        getattr(call, "call_id", None)
        or getattr(call, "id", None)
        or f"{getattr(call, 'name', 'unknown')}:{getattr(call, 'created_at', '')}"
    )


POST_TOOL_REPLY_INSTRUCTIONS = """
Answer the user now using the most recent tool result already present in the conversation.
Do not call any tools.
Do not ask for web permission again.
Do not say you are still searching.
Reply in Vietnamese, naturally and briefly, in 1-2 short sentences.
"""

```

### app\services\voice_agent\transcription_prompt.py

```py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from app.services.agent_grounding.contracts import GroundingScope

_WHITESPACE_RE = re.compile(r"\s+")
_SECTION_NUMBER_RE = re.compile(r"^\s*(chapter|chương|part|phần|section|mục)\s+\d+", re.IGNORECASE)


@dataclass(frozen=True)
class TranscriptionPromptBuildResult:
    prompt: str
    term_count: int
    prompt_chars: int
    dynamic_enabled: bool


def _normalize_term(value: object) -> str:
    text = str(value or "").strip()
    text = _WHITESPACE_RE.sub(" ", text)
    text = text.strip(" -–—|,.;:")
    return text


def _add_unique(terms: list[str], seen: set[str], value: object, *, max_len: int = 80) -> None:
    term = _normalize_term(value)
    if not term:
        return

    if len(term) > max_len:
        term = term[:max_len].rstrip()

    key = term.casefold()
    if key in seen:
        return

    seen.add(key)
    terms.append(term)


def _split_path_terms(path: str | None) -> list[str]:
    if not path:
        return []

    raw = _normalize_term(path)
    if not raw:
        return []

    parts = re.split(r"\s*(?:>|/|\\|»|›)\s*", raw)
    result: list[str] = []

    for part in parts:
        part = _normalize_term(part)
        if part:
            result.append(part)

    if raw and raw not in result:
        result.append(raw)

    return result


def _base_domain_terms() -> tuple[str, ...]:
    return (
        "Tri Âm",
        "TRIAM",
        "chương",
        "sách",
        "tóm tắt",
        "nội dung chính",
        "nhân vật",
        "tác giả",
        "mục lục",
        "bài học",
        "đề mục",
        "định lý",
        "phương pháp",
        "khái niệm",
        "ví dụ",
        "giải thích",
        "so sánh",
        "tìm web",
        "tìm trên internet",
        "tra cứu web",
        "đồng ý",
        "không đồng ý",
        "có",
        "không",
        "tiếp tục",
        "dừng lại",
        "GPT",
        "Gemini",
        "OpenAI",
        "RAG",
    )


def _add_scope_terms(
    terms: list[str],
    seen: set[str],
    grounding_scope: GroundingScope,
    *,
    max_section_terms: int,
) -> None:
    for book in grounding_scope.books:
        _add_unique(terms, seen, book.title)
        _add_unique(terms, seen, book.author)
        if book.document_type:
            _add_unique(terms, seen, str(book.document_type))

    section_added = 0
    for section in grounding_scope.sections:
        if section_added >= max_section_terms:
            break
        section_added += _add_section_terms(terms, seen, section.title, section.path, max_section_terms - section_added)


def _add_section_terms(terms: list[str], seen: set[str], title: str, path: str, remaining: int) -> int:
    added = 0
    if remaining <= 0:
        return added

    if _normalize_term(title):
        _add_unique(terms, seen, title)
        added += 1

    for path_term in _split_path_terms(path):
        if added >= remaining:
            break
        _add_unique(terms, seen, path_term)
        added += 1

    return added


def _collect_dynamic_terms(
    grounding_scope: GroundingScope | None,
    *,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None,
) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()

    for term in _base_domain_terms():
        _add_unique(terms, seen, term)

    if extra_terms:
        for term in extra_terms:
            _add_unique(terms, seen, term)

    if grounding_scope is not None:
        _add_scope_terms(terms, seen, grounding_scope, max_section_terms=max_section_terms)

    return terms[: max(0, max_terms)]


def _build_prompt(base: str, terms: list[str], *, max_chars: int) -> str:
    # Xây dựng câu thoại giả định (Mock Conversation) giúp Whisper học văn phong và thuật ngữ tốt hơn
    mock_dialogue = ""
    if terms:
        mock_dialogue = " Chào bạn! Hôm nay chúng ta sẽ cùng thảo luận về các thuật ngữ " + ", ".join(terms[:12]) + " nhé. Bạn muốn hỏi gì?"
    
    prompt = (
        base
        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
        + mock_dialogue
    ).strip()
    return _trim_prompt(prompt, max_chars=max_chars)


def _trim_prompt(prompt: str, *, max_chars: int) -> str:
    if max_chars <= 0 or len(prompt) <= max_chars:
        return prompt

    trimmed = prompt[:max_chars].rstrip()
    return trimmed if trimmed.endswith(".") else trimmed + "."


def build_realtime_transcription_prompt(
    *,
    base_prompt: str,
    grounding_scope: GroundingScope | None,
    enabled: bool,
    max_chars: int,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None = None,
) -> TranscriptionPromptBuildResult:
    base = _normalize_term(base_prompt)

    if not enabled:
        return TranscriptionPromptBuildResult(
            prompt=base,
            term_count=0,
            prompt_chars=len(base),
            dynamic_enabled=False,
        )

    terms = _collect_dynamic_terms(
        grounding_scope,
        max_terms=max_terms,
        max_section_terms=max_section_terms,
        extra_terms=extra_terms,
    )
    prompt = _build_prompt(base, terms, max_chars=max_chars)

    return TranscriptionPromptBuildResult(
        prompt=prompt,
        term_count=len(terms),
        prompt_chars=len(prompt),
        dynamic_enabled=True,
    )

```

### app\services\voice_agent\transcript_store.py

```py
import asyncio
import json
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, cast

from sqlmodel import Session, select

from app.core.logger import log
from app.models.db_models import ChatMessage
from app.services.voice_agent.contracts import LK_TRANSCRIPT_TOPIC, TranscriptRole

MessageSaver = Callable[[str, bool], uuid.UUID | None]
HistoryLoader = Callable[[int], list[ChatMessage]]


def normalize_transcript_text(text: str) -> str:
    if not text:
        return ""
    lines = text.splitlines()
    normalized_lines = [" ".join(line.split()) for line in lines]
    return "\n".join(normalized_lines)


class VoiceTranscriptStore:
    def __init__(
        self,
        *,
        room: Any,
        thread_id: uuid.UUID | None,
        dedupe_window_seconds: int,
        save_message_sync: MessageSaver | None = None,
        load_history_sync: HistoryLoader | None = None,
        db_engine: Any = None,
    ) -> None:
        self._room = room
        self._thread_id = thread_id
        self._seen_user_texts: dict[str, datetime] = {}
        self._dedupe_window_seconds = max(dedupe_window_seconds, 1)
        self._save_message_sync = save_message_sync or self._save_message_to_db
        self._load_history_sync = load_history_sync or self._load_history_from_db
        self._engine = db_engine

    def _get_engine(self) -> Any:
        if self._engine is None:
            from sqlalchemy.pool import NullPool
            from sqlmodel import create_engine

            from app.core.config import settings
            self._engine = create_engine(
                settings.DATABASE_URL,
                echo=False,
                poolclass=NullPool,
            )
        return self._engine

    async def publish_transcript(
        self,
        role: TranscriptRole,
        text: str,
        *,
        message_id: uuid.UUID | None = None,
    ) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized or not self._room.isconnected():
            return

        transcript_id = message_id or uuid.uuid4()
        payload = {
            "v": 1,
            "type": "transcript",
            "role": role,
            "text": normalized,
            "id": str(transcript_id),
            "message_id": str(message_id) if message_id else None,
            "thread_id": str(self._thread_id) if self._thread_id else None,
            "source": "livekit",
            "status": "committed",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        try:
            await self._room.local_participant.publish_data(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                reliable=True,
                topic=LK_TRANSCRIPT_TOPIC,
            )
        except Exception as exc:
            log.info(f"Transcript publish failed: {exc}")

    async def save_and_publish_user(self, text: str) -> bool:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return False

        now = datetime.now(timezone.utc)
        last_seen = self._seen_user_texts.get(normalized)
        if last_seen and (now - last_seen).total_seconds() < self._dedupe_window_seconds:
            return False
        self._seen_user_texts[normalized] = now

        message_id = await self._save_message_for_transcript(normalized, True)
        await self.publish_transcript("user", normalized, message_id=message_id)
        return True

    async def save_and_publish_assistant(self, text: str) -> bool:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return False

        message_id = await self._save_message_for_transcript(normalized, False)
        await self.publish_transcript("assistant", normalized, message_id=message_id)
        return True

    async def load_recent_history(self, limit: int) -> list[ChatMessage]:
        return await asyncio.to_thread(self._load_history_sync, limit)

    async def _save_message_for_transcript(self, text: str, is_user: bool) -> uuid.UUID | None:
        try:
            return await asyncio.to_thread(self._save_message_sync, text, is_user)
        except Exception as exc:
            self._log_transcript_save_failure(text=text, is_user=is_user, exc=exc)
            return None

    def _save_message_to_db(self, text: str, is_user: bool) -> uuid.UUID | None:
        if not self._thread_id:
            return None
        try:
            with Session(self._get_engine()) as db:
                new_msg = ChatMessage(
                    thread_id=self._thread_id,
                    is_user=is_user,
                    text=text,
                    source="livekit",
                    timestamp=datetime.now(timezone.utc),
                )
                db.add(new_msg)
                db.commit()
                db.refresh(new_msg)
                return new_msg.id
        except Exception as exc:
            self._log_transcript_save_failure(text=text, is_user=is_user, exc=exc)
            return None

    def _log_transcript_save_failure(self, *, text: str, is_user: bool, exc: Exception) -> None:
        role = "user" if is_user else "assistant"
        log.info(
            "Transcript DB save failed | "
            f"thread_id={self._thread_id} | role={role} | "
            f"text_len={len(text)} | error_type={type(exc).__name__}"
        )

    def _load_history_from_db(self, limit: int) -> list[ChatMessage]:
        if not self._thread_id:
            return []
        with Session(self._get_engine()) as db:
            messages = db.exec(
                select(ChatMessage)
                .where(ChatMessage.thread_id == self._thread_id)
                .order_by(cast(Any, ChatMessage.timestamp).desc())
                .limit(limit)
            ).all()
            return list(reversed(messages))


```

### app\services\voice_agent\turn_state.py

```py
from __future__ import annotations

import time
from dataclasses import dataclass

from app.services.voice_agent.transcript_store import normalize_transcript_text


@dataclass(frozen=True)
class VoiceTranscriptSnapshot:
    text: str
    created_monotonic: float
    language: str | None = None
    source: str = "final_transcript"


@dataclass(frozen=True)
class PendingVoiceClarification:
    prompt_text: str
    candidate_query: str | None
    reason_code: str
    created_monotonic: float
    source: str = "query_guard"


class VoiceTurnState:
    def __init__(self, *, clock=time.monotonic) -> None:
        self._clock = clock
        self._final_transcript: VoiceTranscriptSnapshot | None = None
        self._committed_user_text: VoiceTranscriptSnapshot | None = None
        self._pending_clarification: PendingVoiceClarification | None = None

    def record_final_transcript(self, text: str, language: str | None = None) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return
        self._final_transcript = VoiceTranscriptSnapshot(
            text=normalized,
            created_monotonic=self._clock(),
            language=language,
            source="final_transcript",
        )

    def record_committed_user_text(self, text: str, language: str | None = None) -> None:
        normalized = normalize_transcript_text(text)
        if not normalized:
            return
        self._committed_user_text = VoiceTranscriptSnapshot(
            text=normalized,
            created_monotonic=self._clock(),
            language=language,
            source="committed_user_item",
        )

    def recent_transcript(self, ttl_seconds: float) -> VoiceTranscriptSnapshot | None:
        candidates = [item for item in (self._committed_user_text, self._final_transcript) if item is not None]
        if not candidates:
            return None
        newest = max(candidates, key=lambda item: item.created_monotonic)
        if self._clock() - newest.created_monotonic > max(0.0, ttl_seconds):
            return None
        return newest

    def set_pending_clarification(
        self,
        *,
        prompt_text: str,
        reason_code: str,
        candidate_query: str | None = None,
        source: str = "query_guard",
    ) -> None:
        normalized_prompt = normalize_transcript_text(prompt_text)
        normalized_query = normalize_transcript_text(candidate_query or "")
        if not normalized_prompt:
            return
        self._pending_clarification = PendingVoiceClarification(
            prompt_text=normalized_prompt,
            candidate_query=normalized_query or None,
            reason_code=reason_code,
            created_monotonic=self._clock(),
            source=source,
        )

    def recent_pending_clarification(self, ttl_seconds: float) -> PendingVoiceClarification | None:
        pending = self._pending_clarification
        if pending is None:
            return None
        if self._clock() - pending.created_monotonic > max(0.0, ttl_seconds):
            self._pending_clarification = None
            return None
        return pending

    def clear_pending_clarification(self) -> None:
        self._pending_clarification = None

```

### app\services\voice_agent\voice_intent_classifier.py

```py
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

VoiceReplyIntent = Literal["grant", "deny", "unclear", "new_question"]

POSITIVE_ACTION_PHRASES = (
    "dong y",
    "dung roi",
    "dung do",
    "chinh xac",
    "phai roi",
    "tim di",
    "tim kiem di",
    "search di",
    "lam di",
    "cu lam",
    "cu tim",
    "tiep di",
    "thu xem",
    "go ahead",
    "do it",
    "search it",
    "cho phep",
    "cho phep di",
    "cho phep lam",
    "duoc phep",
    "tim tren mang",
    "tim tren web",
    "tim google",
    "tim internet",
    "dong y tim",
    "dong y luon",
    "chap nhan",
    "dong y nha",
    "duoc chu",
    "co chu",
    "tim giup",
    "tim ho",
    "tim di ban",
    "u tim",
)
POSITIVE_SHORT_REPLIES = (
    "co",
    "uh",
    "um",
    "ok",
    "oke",
    "okay",
    "yes",
    "yep",
    "yup",
    "yub",
    "sure",
    "duoc",
    "duoc roi",
    "dung",
    "dung roi",
    "phai",
    "phai roi",
    "cho phep",
    "vang",
    "da vang",
    "da",
    "u",
    "ua",
)
NEGATIVE_PHRASES = (
    "khong phai",
    "khong can",
    "khong dau",
    "khong duoc",
    "khong muon",
    "khong thich",
    "khong",
    "khoi",
    "dung lam",
    "dung tim",
    "dung search",
    "thoi",
    "bo qua",
    "skip",
    "cancel",
    "stop",
    "nope",
    "nah",
    "no",
    "dont",
    "do not",
)

CONTEXT_SENSITIVE_NEGATIONS = {"khong", "no"}
CONTEXT_SENSITIVE_CONFIRMATIONS = {"co", "duoc", "dung", "phai", "uh", "um", "u", "da", "ua"}


@dataclass(frozen=True)
class VoiceReplyIntentResult:
    intent: VoiceReplyIntent
    confidence: float
    reason: str = ""
    source: str = "fast_path"


def normalize_voice_intent_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", (text or "").casefold())
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    without_marks = without_marks.replace("đ", "d")
    without_marks = re.sub(r"[^a-z0-9]+", " ", without_marks)
    return " ".join(without_marks.split())


def phrase_in_text(phrase: str, text: str) -> bool:
    return f" {phrase} " in f" {text} "


def looks_like_new_question(original_text: str, normalized_text: str) -> bool:
    return "?" in original_text


def classify_voice_reply_intent_fast_path(text: str, *, max_grant_tokens: int = 4) -> VoiceReplyIntentResult | None:
    normalized = normalize_voice_intent_text(text)
    if not normalized:
        return None

    token_count = len(normalized.split())
    # Constrain fast path positive/negative matching to short replies only
    if token_count > max(4, max_grant_tokens):
        if looks_like_new_question(text, normalized):
            return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark detected", "fast_path")
        return None

    # 1. Check negative phrases first
    for phrase in NEGATIVE_PHRASES:
        if phrase in CONTEXT_SENSITIVE_NEGATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")

    # 2. Check positive action phrases
    if any(phrase_in_text(phrase, normalized) for phrase in POSITIVE_ACTION_PHRASES):
        return VoiceReplyIntentResult("grant", 0.96, "Matched positive action fast path", "fast_path")

    # 3. Check positive short replies
    for phrase in POSITIVE_SHORT_REPLIES:
        if phrase in CONTEXT_SENSITIVE_CONFIRMATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")

    # 4. Check if it looks like a new question only if it does not match positive/negative phrases
    if looks_like_new_question(text, normalized):
        return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark detected", "fast_path")

    return None
```

### app\services\voice_agent\web_permission_intent_classifier.py

```py
from __future__ import annotations

import os
import torch
import asyncio
from typing import Any

from app.core.logger import log
from app.services.voice_agent.contracts import WebPermissionIntent, WebPermissionIntentResult
from app.services.voice_agent.voice_intent_classifier import (
    classify_voice_reply_intent_fast_path,
    normalize_voice_intent_text,
    looks_like_new_question,
)
# Re-use the singleton model loader from intent_router to avoid double RAM allocation
from app.services.agent_grounding.intent_router import _classifier, mean_pooling

# Expose normalize_intent_text for policy layer
normalize_intent_text = normalize_voice_intent_text

L12_WEB_PERMISSION_PROTOTYPES = {
    "grant": [
        "đồng ý cho tìm kiếm", "ừ tìm trên internet đi", "cho phép tra cứu google",
        "tìm giúp mình trên mạng", "search hộ mình thông tin này", "đồng ý nha",
        "được chứ tìm đi", "yes search it", "go ahead and search", "nhất trí tìm đi"
    ],
    "deny": [
        "không cần tìm đâu", "đừng tra cứu internet", "thôi khỏi cần",
        "bỏ qua đi bạn", "không muốn tìm trên web", "đừng tìm kiếm",
        "no don't search", "cancel web search", "thôi bỏ qua đi"
    ],
    "unclear": [
        "chưa biết nữa", "để tính sau đi", "tùy bạn thôi", "cái đó khó nói",
        "sao cũng được", "maybe later", "chưa chắc nữa", "để mình suy nghĩ tí"
    ]
}

_proto_embeddings: dict[str, torch.Tensor] = {}
_lock = asyncio.Lock()
_initialized = False

def _initialize_permission_prototypes() -> None:
    global _proto_embeddings, _initialized
    if _initialized:
        return
        
    # Ensure the intent router model is initialized
    _classifier.initialize()
    tokenizer = _classifier.tokenizer
    model = _classifier.model

    with torch.no_grad():
        for intent, phrases in L12_WEB_PERMISSION_PROTOTYPES.items():
            inputs = tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            embeddings = mean_pooling(outputs, inputs['attention_mask'])
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            _proto_embeddings[intent] = embeddings
            
    _initialized = True

async def _initialize_permission_prototypes_async() -> None:
    global _initialized
    if _initialized:
        return
    async with _lock:
        if not _initialized:
            # First ensure the intent router model is initialized async/sync
            await _classifier.initialize_async()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, _initialize_permission_prototypes)

def classify_web_permission_intent_fast_path(user_reply: str) -> WebPermissionIntentResult | None:
    normalized = normalize_voice_intent_text(user_reply)
    if not normalized:
        return None

    # Layer 1 (Fast-Path): Only apply to very short replies <= 2 words
    token_count = len(normalized.split())
    if token_count <= 2:
        result = classify_voice_reply_intent_fast_path(user_reply)
        if result is not None:
            return WebPermissionIntentResult(
                intent=result.intent,
                confidence=result.confidence,
                reason=result.reason,
                source=result.source,
            )
    return None

async def classify_web_permission_intent(
    *,
    pending_query: str,
    user_reply: str,
    use_llm: bool | None = None, # Left for backward compatibility, unused
    model: str | None = None, # Left for backward compatibility, unused
    timeout_seconds: float | None = None, # Left for backward compatibility, unused
    confidence_threshold: float | None = None,
) -> WebPermissionIntentResult:
    """
    Classifies the user reply regarding web search permission using a local multilingual L12 model.
    """
    # 1. Run Fast-path Layer 1:
    fast_result = classify_web_permission_intent_fast_path(user_reply)
    if fast_result is not None:
        return fast_result

    # Layer 2: Local Embedding
    # 2. Run Local Embedding Cosine Similarity Layer 2
    normalized = normalize_voice_intent_text(user_reply)

    # Fast-check if query looks like a new question (e.g. contains question marks or keywords)
    if looks_like_new_question(user_reply, normalized):
        return WebPermissionIntentResult(
            intent="new_question",
            confidence=1.0,
            reason="looks_like_new_question",
            source="local_embedding",
        )

    try:
        # Load prototypes asynchronously to prevent event loop blocking
        await _initialize_permission_prototypes_async()
        
        tokenizer = _classifier.tokenizer
        model_obj = _classifier.model

        with torch.no_grad():
            inputs = tokenizer([user_reply.strip().lower()], padding=True, truncation=True, return_tensors="pt")
            outputs = model_obj(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)

            best_intent: WebPermissionIntent = "unclear"
            best_score = -1.0

            for intent, proto_embs in _proto_embeddings.items():
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent  # type: ignore[assignment]

            # Use threshold from arguments or default
            from app.core.config import settings
            # We default to 0.55 for web permission classification as evaluated
            resolved_threshold = confidence_threshold or 0.55

            if best_score < resolved_threshold:
                log.info(f"Web permission cosine score {best_score:.2f} below threshold {resolved_threshold} | Fallback to new_question")
                return WebPermissionIntentResult(
                    intent="new_question",
                    confidence=best_score,
                    reason="Below similarity threshold",
                    source="local_embedding",
                )

            return WebPermissionIntentResult(
                intent=best_intent,
                confidence=best_score,
                reason="Classified by local L12 Cosine",
                source="local_embedding",
            )
            
    except Exception as exc:
        log.error(f"Web permission local classifier failed: {exc} | Fallback to unclear")
        return WebPermissionIntentResult(
            intent="unclear",
            confidence=0.0,
            reason=f"Classifier error: {exc}",
            source="local_embedding",
        )

```

### app\services\voice_agent\web_permission_policy.py

```py
from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone

from app.core.logger import log
from app.services.voice_agent.contracts import (
    WebPermissionIntentResult,
    WebSearchPermissionDecision,
    WebSearchPermissionState,
)
from app.services.voice_agent.web_permission_intent_classifier import (
    classify_web_permission_intent,
    normalize_intent_text,
)

IntentClassifier = Callable[..., Awaitable[WebPermissionIntentResult]]


def _normalize_query(text: str) -> str:
    return " ".join((text or "").split())


def _word_set(text: str) -> set[str]:
    return {word for word in normalize_intent_text(text).split() if len(word) >= 2}


def _query_matches(granted_query: str, query: str) -> bool:
    left = normalize_intent_text(granted_query)
    right = normalize_intent_text(query)
    if not left or not right:
        return False
    if left in right or right in left:
        return True

    left_words = _word_set(left)
    right_words = _word_set(right)
    if not left_words or not right_words:
        return False

    overlap = len(left_words & right_words)
    return overlap / max(min(len(left_words), len(right_words)), 1) >= 0.5


class WebSearchPermissionPolicy:
    def __init__(
        self,
        *,
        enabled: bool = False,
        grant_ttl_seconds: int = 180,
        implicit_grant_window_seconds: int = 20,
        intent_classifier: IntentClassifier | None = None,
    ) -> None:
        self.state = WebSearchPermissionState(enabled=enabled)
        self._grant_ttl = timedelta(seconds=max(grant_ttl_seconds, 1))
        self._implicit_grant_window = timedelta(seconds=max(implicit_grant_window_seconds, 1))
        self._intent_classifier = intent_classifier or classify_web_permission_intent

    @property
    def enabled(self) -> bool:
        return self.state.enabled

    @property
    def has_pending_permission(self) -> bool:
        return bool(self.state.pending_query)

    def set_enabled(self, enabled: bool) -> None:
        self.state.enabled = enabled
        if not enabled:
            self.clear()

    def clear(self) -> None:
        self.state.pending_query = None
        self.state.pending_request_id = None
        self.state.last_user_reply = None
        self.state.last_user_reply_at = None
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None

    def request_permission(self, query: str) -> str:
        normalized_query = _normalize_query(query)
        if not self.state.enabled:
            self.clear()
            return "Thông tin này không có trong sách. Tính năng tìm kiếm internet hiện đang tắt."

        self.state.pending_query = normalized_query
        self.state.pending_request_id = str(uuid.uuid4())
        self.state.last_user_reply = None
        self.state.last_user_reply_at = None
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None
        log.info(
            "Voice web permission requested | "
            f"request_id={self.state.pending_request_id} | query_chars={len(normalized_query)}"
        )
        return f"Thông tin về '{normalized_query}' không có trong sách. Bạn có muốn tôi tìm kiếm thêm trên internet không?"

    def record_user_reply(self, text: str) -> None:
        normalized_reply = _normalize_query(text)
        if normalized_reply:
            self.state.last_user_reply = normalized_reply
            self.state.last_user_reply_at = datetime.now(timezone.utc)

    def _last_reply_is_recent(self) -> bool:
        if not self.state.last_user_reply or not self.state.last_user_reply_at:
            return False
        return datetime.now(timezone.utc) - self.state.last_user_reply_at <= self._implicit_grant_window

    async def _classify_reply(
        self,
        *,
        pending_query: str,
        user_reply: str,
        request_id: str | None,
        implicit: bool = False,
    ) -> WebPermissionIntentResult:
        result = await self._intent_classifier(
            pending_query=pending_query,
            user_reply=user_reply,
        )
        mode = "implicit" if implicit else "pending"
        log.info(
            "Voice web permission intent classified | "
            f"mode={mode} | request_id={request_id} | intent={result.intent} | "
            f"confidence={result.confidence:.2f} | source={result.source}"
        )
        return result

    async def observe_user_reply(self, text: str) -> WebSearchPermissionDecision:
        self.record_user_reply(text)
        return await self.resolve_pending_reply()

    async def resolve_pending_reply(self) -> WebSearchPermissionDecision:
        if not self.state.pending_query or not self.state.last_user_reply:
            return WebSearchPermissionDecision()

        pending_query = self.state.pending_query
        request_id = self.state.pending_request_id
        user_reply = self.state.last_user_reply
        result = await self._classify_reply(
            pending_query=pending_query,
            user_reply=user_reply,
            request_id=request_id,
        )

        if result.intent == "grant":
            self.state.pending_query = None
            self.state.pending_request_id = None
            self.state.last_user_reply = None
            self.state.last_user_reply_at = None
            self.state.granted_query = pending_query
            self.state.granted_request_id = request_id
            self.state.granted_at = datetime.now(timezone.utc)
            return WebSearchPermissionDecision(granted_query=pending_query)

        if result.intent == "deny":
            self.clear()
            return WebSearchPermissionDecision(denied=True)

        if result.intent == "new_question":
            self.clear()
            return WebSearchPermissionDecision(new_question=user_reply)

        return WebSearchPermissionDecision(unclear=True)

    def pre_grant_for_eval(self) -> None:
        self.state.granted_query = "eval_pre_granted"
        self.state.granted_at = datetime.now(timezone.utc)

    def can_execute(self, query: str) -> tuple[bool, str]:
        if not self.state.enabled:
            return False, "Tính năng tìm kiếm internet hiện đang tắt."

        if not self.state.granted_query or not self.state.granted_at:
            return False, "WEB_SEARCH_PERMISSION_REQUIRED: Hãy xin phép user trước khi tìm kiếm internet."

        if self.state.granted_query == "eval_pre_granted":
            return True, ""

        if datetime.now(timezone.utc) - self.state.granted_at > self._grant_ttl:
            self.clear()
            return False, "WEB_SEARCH_PERMISSION_EXPIRED: Quyền tìm kiếm đã hết hạn. Hãy xin phép lại."

        if not _query_matches(self.state.granted_query, query):
            return False, "WEB_SEARCH_PERMISSION_QUERY_MISMATCH: Query khác với nội dung user đã đồng ý."

        return True, ""

    async def _resolve_pending_before_search(self, query: str) -> tuple[bool, str]:
        decision = await self.resolve_pending_reply()
        if decision.granted_query:
            return self.can_execute(query)
        if decision.denied:
            return False, "WEB_SEARCH_PERMISSION_DENIED: User đã từ chối tìm kiếm internet."
        if decision.unclear:
            return False, "WEB_SEARCH_PERMISSION_UNCLEAR: Hãy hỏi lại user để xác nhận rõ hơn."
        if decision.new_question:
            return False, "WEB_SEARCH_PERMISSION_NEW_QUESTION: User đã hỏi câu mới thay vì xác nhận."
        return False, "WEB_SEARCH_PERMISSION_REQUIRED: Hãy xin phép user trước khi tìm kiếm internet."

    async def _resolve_implicit_before_search(self, query: str) -> tuple[bool, str]:
        result = await self._classify_reply(
            pending_query=query,
            user_reply=self.state.last_user_reply or "",
            request_id=None,
            implicit=True,
        )
        if result.intent == "grant":
            self.state.last_user_reply = None
            self.state.last_user_reply_at = None
            self.state.granted_query = _normalize_query(query)
            self.state.granted_request_id = None
            self.state.granted_at = datetime.now(timezone.utc)
            return self.can_execute(query)
        if result.intent == "deny":
            self.clear()
            return False, "WEB_SEARCH_PERMISSION_DENIED: User đã từ chối tìm kiếm internet."
        if result.intent == "unclear":
            return False, "WEB_SEARCH_PERMISSION_UNCLEAR: Hãy hỏi lại user để xác nhận rõ hơn."
        return False, "WEB_SEARCH_PERMISSION_NEW_QUESTION: User đã hỏi câu mới thay vì xác nhận."

    def _can_try_implicit_grant(self, reason: str) -> bool:
        return (
            reason.startswith("WEB_SEARCH_PERMISSION_REQUIRED")
            and not self.state.pending_query
            and bool(self.state.last_user_reply)
            and self._last_reply_is_recent()
        )

    async def resolve_before_web_search(self, query: str) -> tuple[bool, str]:
        allowed, reason = self.can_execute(query)
        if allowed:
            return True, ""

        if (
            reason.startswith("WEB_SEARCH_PERMISSION_REQUIRED")
            and self.state.pending_query
            and self.state.last_user_reply
        ):
            return await self._resolve_pending_before_search(query)

        if self._can_try_implicit_grant(reason):
            return await self._resolve_implicit_before_search(query)

        return False, reason

    def mark_search_consumed(self) -> None:
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None

```

### app\services\voice_agent\__init__.py

```py
"""Voice agent helpers for TRIAM realtime sessions."""


```

### app\services\web_search_service.py

```py
from tavily import AsyncTavilyClient

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.core.logger import log

# Singleton async client
_tavily_client: AsyncTavilyClient | None = None


def get_tavily_client() -> AsyncTavilyClient:
    global _tavily_client
    if _tavily_client is None:
        if not settings.TAVILY_API_KEY:
            raise ExternalServiceError("Thiếu TAVILY_API_KEY trong cấu hình.")
        _tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
    return _tavily_client


async def search_web(query: str, max_results: int = 3) -> str:
    """
    Tìm kiếm web bằng Tavily AsyncClient (Tối ưu cho LLM Agents).
    Trả về chuỗi văn bản đã được format để tiết kiệm token cho AI.
    """
    log.info(f"Web Search (Tavily): {query}")

    try:
        client = get_tavily_client()
        response = await client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
        )

        results = response.get("results", [])
        if not results:
            return "Không tìm thấy thông tin trên internet cho câu hỏi này."

        formatted_results = [
            f"- {item.get('title', '')}: {item.get('content', '')}"
            for item in results
        ]
        return "\n".join(formatted_results)

    except Exception as e:
        log.error(f"Lỗi khi search web: {str(e)}")
        return "Đã xảy ra lỗi hệ thống khi kết nối internet."

```

### app\services\workers\book_pipeline.py

```py
import asyncio
import math
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.constant import BookStatus, PlanMode, ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import Book, LearningUnit, ProcessingJob
from app.repositories.audiobook_repo import update_book_status
from app.repositories.learning_unit_repo import get_learning_unit_source_text_map, list_learning_units
from app.repositories.processing_job_repo import update_processing_job
from app.services.notification_event_service import create_book_ready_outbox_once, create_first_playable_ready_outbox_once
from app.services.token_budget_service import TextBudget, estimate_text_budget
from app.services.workers.learning_unit_worker import process_learning_unit


@dataclass(frozen=True)
class UnitWorkItem:
    unit: LearningUnit
    raw_text: str
    budget: TextBudget


@dataclass(frozen=True)
class BookProcessingInput:
    book: Book
    units: list[LearningUnit]
    source_text_by_unit: dict[uuid.UUID, str]


def _update_job(
    job_id: uuid.UUID | None,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    estimated_input_tokens: int | None = None,
    estimated_audio_seconds: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> None:
    if not job_id:
        return
    with Session(engine) as session:
        update_processing_job(
            session,
            job_id,
            status=status,
            progress_percent=progress_percent,
            current_step=current_step,
            total_units=total_units,
            done_units=done_units,
            failed_units=failed_units,
            estimated_input_tokens=estimated_input_tokens,
            estimated_audio_seconds=estimated_audio_seconds,
            error_message=error_message,
            started_at=started_at,
            finished_at=finished_at,
        )


def _set_book_status(book_id: uuid.UUID, status: BookStatus, *, current_job_id: uuid.UUID | None = None, error_message: str | None = None) -> None:
    with Session(engine) as session:
        # Nếu worker muốn đặt trạng thái READY cho sách
        if status == BookStatus.READY:
            # Kiểm tra xem còn tiến trình (Job) xử lý nào khác cho sách đang chạy không (loại trừ job hiện tại)
            query = select(ProcessingJob).where(ProcessingJob.book_id == book_id, ProcessingJob.status.in_([ProcessingJobStatus.QUEUED, ProcessingJobStatus.PROCESSING]))
            if current_job_id:
                query = query.where(ProcessingJob.id != current_job_id)

            active_jobs = session.exec(query).all()

            # Nếu còn ít nhất 1 job khác đang chạy (ví dụ chế độ còn lại đang gen)
            if active_jobs:
                logger.info(f"Sách {book_id} vẫn còn {len(active_jobs)} job khác đang xử lý. Giữ trạng thái ở mức PARTIAL_READY.")
                update_book_status(session, book_id, BookStatus.PARTIAL_READY, error_message)
                return

        # Thiết lập bình thường nếu không vướng job chạy song song
        update_book_status(session, book_id, status, error_message)


def _fail_job(
    job_id: uuid.UUID | None,
    current_step: str,
    error_message: str,
    *,
    progress_percent: int | None = None,
    total_units: int | None = None,
) -> None:
    _update_job(
        job_id,
        status=ProcessingJobStatus.ERROR,
        progress_percent=progress_percent,
        current_step=current_step,
        total_units=total_units,
        error_message=error_message,
        finished_at=datetime.now(timezone.utc),
    )


def _job_is_ready(job_id: uuid.UUID | None) -> bool:
    if not job_id:
        return False
    with Session(engine) as session:
        job = session.get(ProcessingJob, job_id)
        return bool(job and job.status == ProcessingJobStatus.READY)


def _load_book_processing_input(book_id: uuid.UUID, mode: PlanMode, job_id: uuid.UUID | None) -> BookProcessingInput | None:
    with Session(engine) as session:
        book = session.get(Book, book_id)
        units = list_learning_units(session, book_id, mode)
        source_text_by_unit = get_learning_unit_source_text_map(session, book_id, mode)

    if not book:
        _fail_job(job_id, "Không tìm thấy sách.", f"Book {book_id} not found")
        logger.error(f"Book {book_id} not found")
        return None

    if not units:
        message = "Sách chưa có bài học nào để xử lý. Hãy tạo kế hoạch học trước."
        _set_book_status(book_id, BookStatus.ERROR, message)
        _fail_job(job_id, message, message, progress_percent=0, total_units=0)
        return None

    if not source_text_by_unit:
        message = "Không tìm thấy nội dung nguồn của các bài học."
        _set_book_status(book_id, BookStatus.ERROR, message)
        _fail_job(job_id, message, message, progress_percent=0, total_units=len(units))
        return None

    return BookProcessingInput(book=book, units=list(units), source_text_by_unit=source_text_by_unit)


def _create_first_playable_notification_safely(book: Book, mode: str) -> None:
    try:
        with Session(engine) as session:
            created = create_first_playable_ready_outbox_once(
                session,
                user_id=book.user_id,
                book_id=book.id,
                book_title=book.title,
                mode=mode,
                now=datetime.now(timezone.utc),
            )
            logger.info(f"Content-ready first-playable event | book_id={book.id} | mode={mode} | created={bool(created)}")
    except Exception as exc:
        logger.warning(f"Content-ready first-playable event failed | book_id={book.id} | mode={mode} | error={exc}")


def _create_book_ready_notification_safely(book_id: uuid.UUID, mode: str) -> None:
    try:
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if not book:
                return
            created = create_book_ready_outbox_once(
                session,
                user_id=book.user_id,
                book_id=book.id,
                book_title=book.title,
                mode=mode,
                now=datetime.now(timezone.utc),
            )
            logger.info(f"Content-ready book-ready event | book_id={book.id} | mode={mode} | created={bool(created)}")
    except Exception as exc:
        logger.warning(f"Content-ready book-ready event failed | book_id={book_id} | mode={mode} | error={exc}")


def _build_work_items(units: list[LearningUnit], source_text_by_unit: dict[uuid.UUID, str]) -> list[UnitWorkItem]:
    work_items: list[UnitWorkItem] = []
    for unit in units:
        raw_text = source_text_by_unit.get(unit.id, "")
        if not raw_text.strip():
            logger.warning(f"Learning unit {unit.unit_index + 1} '{unit.title}' không có text, bỏ qua.")
            continue
        work_items.append(UnitWorkItem(unit=unit, raw_text=raw_text, budget=estimate_text_budget(raw_text)))
    return work_items


def _hard_limit_error(work_items: list[UnitWorkItem]) -> str | None:
    too_large = [item for item in work_items if item.budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT]
    if too_large:
        first = too_large[0]
        return (
            f"Có {len(too_large)} bài học vượt giới hạn xử lý. "
            f"Bài đầu tiên vượt giới hạn: '{first.unit.title}' khoảng {first.budget.estimated_tokens} tokens, "
            f"giới hạn là {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens."
        )

    total_audio_seconds = sum(item.budget.estimated_audio_seconds for item in work_items)
    if total_audio_seconds > settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK:
        return f"Tài liệu dự kiến khoảng {math.ceil(total_audio_seconds / 60)} phút audio, vượt giới hạn {math.ceil(settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK / 60)} phút cho mỗi sách."

    return None


def _total_estimates(work_items: list[UnitWorkItem]) -> tuple[int, int]:
    return (
        sum(item.budget.estimated_tokens for item in work_items),
        sum(item.budget.estimated_audio_seconds for item in work_items),
    )


async def _track_progress(
    tasks: list[asyncio.Task],
    job_id: uuid.UUID | None,
    total_units: int,
    book_id: uuid.UUID,
    step_template: str,
    completed_offset: int = 0,
) -> None:
    completed = completed_offset
    partial_threshold = min(total_units, max(1, settings.FIRST_PLAYABLE_UNITS))

    try:
        for task in asyncio.as_completed(tasks):
            await task
            completed += 1
            progress = int(completed * 100 / total_units)
            is_partial = completed >= partial_threshold and completed < total_units
            job_status = ProcessingJobStatus.PARTIAL_READY if is_partial else ProcessingJobStatus.PROCESSING

            if is_partial:
                await asyncio.to_thread(_set_book_status, book_id, BookStatus.PARTIAL_READY)

            await asyncio.to_thread(
                _update_job,
                job_id,
                status=job_status,
                progress_percent=progress,
                current_step=step_template.format(completed=completed, total=total_units),
                done_units=completed,
            )
    except Exception:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.to_thread(_update_job, job_id, done_units=completed, failed_units=max(1, total_units - completed))
        raise


async def _run_unit_pipeline(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None) -> None:
    if await asyncio.to_thread(_job_is_ready, job_id):
        logger.info(f"Skip book processing because job is already READY | book_id={book_id} | job_id={job_id}")
        return

    mode_value = PlanMode(mode)
    processing_input = await asyncio.to_thread(_load_book_processing_input, book_id, mode_value, job_id)
    if not processing_input:
        return

    book = processing_input.book
    work_items = _build_work_items(processing_input.units, processing_input.source_text_by_unit)
    total_units = len(work_items)
    if total_units == 0:
        error_message = "Không có bài học nào có nội dung để xử lý."
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=error_message)
        await asyncio.to_thread(_fail_job, job_id, error_message, error_message, progress_percent=0, total_units=0)
        return

    hard_limit_error = _hard_limit_error(work_items)
    estimated_input_tokens, estimated_audio_seconds = _total_estimates(work_items)
    if hard_limit_error:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=hard_limit_error)
        await asyncio.to_thread(_fail_job, job_id, "Tài liệu vượt giới hạn xử lý.", hard_limit_error, progress_percent=0, total_units=total_units)
        return

    await asyncio.to_thread(
        _update_job,
        job_id,
        status=ProcessingJobStatus.PROCESSING,
        progress_percent=0,
        current_step="Đã tạo các bài học, đang xử lý audio.",
        total_units=total_units,
        done_units=0,
        estimated_input_tokens=estimated_input_tokens,
        estimated_audio_seconds=estimated_audio_seconds,
        started_at=datetime.now(timezone.utc),
    )

    first_count = min(total_units, max(1, settings.FIRST_PLAYABLE_UNITS))
    completed = 0
    for item in work_items[:first_count]:
        await process_learning_unit(
            book.user_id,
            book_id,
            book.title,
            item.unit,
            item.raw_text,
            job_id,
            item.budget.char_count,
            item.budget.estimated_tokens,
            item.budget.estimated_audio_seconds,
        )
        completed += 1
        progress = int(completed * 100 / total_units)
        if completed < total_units:
            await asyncio.to_thread(_set_book_status, book_id=book_id, status=BookStatus.PARTIAL_READY, current_job_id=job_id)
            await asyncio.to_thread(
                _update_job,
                job_id,
                status=ProcessingJobStatus.PARTIAL_READY,
                progress_percent=progress,
                current_step="Đã có bài học đầu tiên có thể nghe. Phần còn lại đang được xử lý.",
                done_units=completed,
            )
    _create_first_playable_notification_safely(book, mode_value.value)

    remaining_items = work_items[first_count:]
    if remaining_items:
        tasks = [
            asyncio.create_task(
                process_learning_unit(
                    book.user_id,
                    book_id,
                    book.title,
                    item.unit,
                    item.raw_text,
                    job_id,
                    item.budget.char_count,
                    item.budget.estimated_tokens,
                    item.budget.estimated_audio_seconds,
                )
            )
            for item in remaining_items
        ]
        await _track_progress(tasks, job_id, total_units, book_id, "Đã xử lý {completed}/{total} bài học.", completed_offset=completed)

    await asyncio.to_thread(_set_book_status, book_id=book_id, status=BookStatus.READY, current_job_id=job_id)
    _create_book_ready_notification_safely(book_id, mode_value.value)
    await asyncio.to_thread(
        _update_job,
        job_id,
        status=ProcessingJobStatus.READY,
        progress_percent=100,
        current_step="Sách đã xử lý xong.",
        done_units=total_units,
        finished_at=datetime.now(timezone.utc),
    )
    logger.info(f"Book {book_id} READY | processed_units={total_units} | mode={mode_value.value}")


async def run_background_processing(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None = None) -> None:
    try:
        await _run_unit_pipeline(book_id, mode, job_id)
    except Exception as exc:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=str(exc))
        await asyncio.to_thread(_fail_job, job_id, "Xử lý sách thất bại.", str(exc))
        logger.error(f"LỖI XỬ LÝ SÁCH {book_id}: {exc}")


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str, job_id: uuid.UUID | None = None) -> None:
    try:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.PROCESSING)
        await _run_unit_pipeline(book_id, new_mode, job_id)
    except Exception as exc:
        await asyncio.to_thread(_set_book_status, book_id, BookStatus.ERROR, error_message=str(exc))
        await asyncio.to_thread(_fail_job, job_id, f"Sinh audio mode {new_mode} thất bại.", str(exc))
        logger.error(f"LỖI SWITCH MODE SÁCH {book_id}: {exc}")

```

### app\services\workers\learning_unit_tts_worker.py

```py
import asyncio
import os
import uuid
from dataclasses import dataclass

from sqlmodel import Session

from app.core.exceptions import NoPlayableAudioError
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import LearningUnitSegment
from app.repositories.learning_unit_repo import bulk_create_unit_segments, delete_unit_segments, update_learning_unit_review
from app.services.llm_service import normalize_text_for_speech
from app.services.storage_service import upload_file_to_supabase
from app.services.tts_service import generate_audio_and_get_duration


@dataclass(frozen=True)
class LearningUnitTTSResult:
    main_segment_count: int
    review_audio_created: bool
    review_text: str
    generated_audio_seconds: int = 0

# --- Helper for processing single segment ---
async def _process_single_script_task(
    index: int,
    script: str,
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    unit_index: int,
    mode: str,
    total_scripts: int,
) -> LearningUnitSegment | None:
    """
    Process single segment: Generate audio, upload to cloud storage, and clean up temporary files.
    """
    local_file = f"uploads/{uuid.uuid4()}.mp3"
    os.makedirs("uploads", exist_ok=True)
    try:
        logger.info(f"TTS segment start | unit={unit_index + 1} | mode={mode} | segment={index + 1}/{total_scripts} | chars={len(script)}")
        # 1. Generate audio file
        duration_ms = await generate_audio_and_get_duration(script, local_file)

        # 2. Upload file to cloud storage
        storage_path = f"{book_id}/unit_{unit_index + 1}/{mode}/part_{index + 1}.mp3"
        audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")

        logger.info(f"TTS segment done | unit={unit_index + 1} | mode={mode} | segment={index + 1}/{total_scripts} | duration_ms={duration_ms}")

        # Return segment object
        return LearningUnitSegment(
            learning_unit_id=learning_unit_id,
            segment_index=index,
            audio_url=audio_url,
            duration_ms=duration_ms,
            text_content=script,
        )
    except Exception as seg_err:
        logger.warning(f"Segment {index + 1} unit {unit_index + 1} TTS failed ({len(script)} chars): {seg_err}")
        return None
    finally:
        # Ensure temporary files are deleted immediately after this small task ends
        if os.path.exists(local_file):
            os.remove(local_file)


# --- Main function
async def _generate_unit_main_segments(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    unit_index: int,
    mode: str,
    main_scripts: list[str],
) -> list[LearningUnitSegment]:
    total_scripts = len(main_scripts)
    logger.info(f"TTS main segments start | unit={unit_index + 1} | mode={mode} | total_scripts={total_scripts}")

    # 1. Create a list of coroutine tasks (not yet awaited)
    tasks = [
        _process_single_script_task(
            index=i,
            script=script,
            book_id=book_id,
            learning_unit_id=learning_unit_id,
            unit_index=unit_index,
            mode=mode,
            total_scripts=total_scripts,
        )
        for i, script in enumerate(main_scripts)
    ]

    # 2. Run all tasks in parallel
    # I/O network tasks (upload) and API (TTS) will interleave, running extremely fast
    results = await asyncio.gather(*tasks)

    # 3. Filter out None results (failed segments) and preserve order
    segments = [seg for seg in results if seg is not None]

    # 4. Sort segments in the original index order to ensure correct playback order
    segments.sort(key=lambda x: x.segment_index)

    logger.info(f"TTS main segments done | unit={unit_index + 1} | mode={mode} | created_segments={len(segments)}/{total_scripts}")
    return segments

# async def _generate_unit_main_segments(
#     book_id: uuid.UUID,
#     learning_unit_id: uuid.UUID,
#     unit_index: int,
#     mode: str,
#     main_scripts: list[str],
# ) -> list[LearningUnitSegment]:
#     segments: list[LearningUnitSegment] = []
#     total_scripts = len(main_scripts)
#     logger.info(f"TTS main segments start | unit={unit_index + 1} | mode={mode} | total_scripts={total_scripts}")
#     for i, script in enumerate(main_scripts):
#         local_file = f"uploads/{uuid.uuid4()}.mp3"
#         os.makedirs("uploads", exist_ok=True)
#         try:
#             logger.info(
#                 f"TTS segment start | unit={unit_index + 1} | mode={mode} | "
#                 f"segment={i + 1}/{total_scripts} | chars={len(script)}"
#             )
#             duration_ms = await generate_audio_and_get_duration(script, local_file)
#             storage_path = f"{book_id}/unit_{unit_index + 1}/{mode}/part_{i + 1}.mp3"
#             audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
#             segments.append(
#                 LearningUnitSegment(
#                     learning_unit_id=learning_unit_id,
#                     segment_index=i,
#                     audio_url=audio_url,
#                     duration_ms=duration_ms,
#                     text_content=script,
#                 )
#             )
#             logger.info(
#                 f"TTS segment done | unit={unit_index + 1} | mode={mode} | "
#                 f"segment={i + 1}/{total_scripts} | duration_ms={duration_ms}"
#             )
#         except Exception as seg_err:
#             logger.warning(f"Segment {i + 1} unit {unit_index + 1} TTS failed ({len(script)} chars): {seg_err}")
#         finally:
#             if os.path.exists(local_file):
#                 os.remove(local_file)
#     logger.info(
#         f"TTS main segments done | unit={unit_index + 1} | mode={mode} | "
#         f"created_segments={len(segments)}/{total_scripts}"
#     )
#     return segments


async def _generate_unit_review_audio(
    book_id: uuid.UUID,
    unit_index: int,
    mode: str,
    review_text: str,
) -> str | None:
    if not review_text.strip():
        return None

    local_review = f"uploads/{uuid.uuid4()}.mp3"
    os.makedirs("uploads", exist_ok=True)
    try:
        logger.info(f"TTS review start | unit={unit_index + 1} | mode={mode} | chars={len(review_text)}")
        await generate_audio_and_get_duration(review_text, local_review)
        storage_path = f"{book_id}/unit_{unit_index + 1}/{mode}/review.mp3"
        review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
        logger.info(f"TTS review done | unit={unit_index + 1} | mode={mode}")
        return review_url
    except Exception as rev_err:
        logger.warning(f"Review audio unit {unit_index + 1} failed, skipped: {rev_err}")
        return None
    finally:
        if os.path.exists(local_review):
            os.remove(local_review)


def _store_unit_tts_result(
    learning_unit_id: uuid.UUID,
    mode: str,
    review_text: str,
    review_url: str | None,
    segments: list[LearningUnitSegment],
) -> None:
    logger.info(
        f"TTS DB store start | learning_unit_id={learning_unit_id} | mode={mode} | "
        f"segments={len(segments)} | review_audio={bool(review_url)}"
    )
    with Session(engine) as session:
        delete_unit_segments(session, learning_unit_id)
        bulk_create_unit_segments(session, segments)
        update_learning_unit_review(session, learning_unit_id, review_text=review_text, review_audio_url=review_url)
    logger.info(f"TTS DB store done | learning_unit_id={learning_unit_id} | mode={mode}")


async def run_learning_unit_tts_pipeline(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    unit_index: int,
    raw_text: str,
    mode: str,
    unit_title: str,
) -> LearningUnitTTSResult:
    logger.info(
        f"TTS pipeline start | unit={unit_index + 1} | mode={mode} | "
        f"title={unit_title} | raw_chars={len(raw_text)}"
    )
    obj_unit = await normalize_text_for_speech(raw_text, mode, unit_title=unit_title)
    main_scripts: list[str] = obj_unit.get("main_scripts", [])
    review_text: str = obj_unit.get("review_script", "")
    logger.info(
        f"TTS pipeline normalized | unit={unit_index + 1} | mode={mode} | "
        f"main_scripts={len(main_scripts)} | review_chars={len(review_text)}"
    )
    if not main_scripts:
        raise NoPlayableAudioError("LLM không tạo main_scripts để phát audio.")

    segments = await _generate_unit_main_segments(book_id, learning_unit_id, unit_index, mode, main_scripts)
    review_url = await _generate_unit_review_audio(book_id, unit_index, mode, review_text)

    if not segments:
        raise NoPlayableAudioError("Không tạo được segment audio nào.")

    total_ms = sum(seg.duration_ms or 0 for seg in segments)
    generated_seconds = int(total_ms / 1000)

    _store_unit_tts_result(learning_unit_id, mode, review_text, review_url, segments)

    return LearningUnitTTSResult(
        main_segment_count=len(segments),
        review_audio_created=bool(review_url),
        review_text=review_text,
        generated_audio_seconds=generated_seconds,
    )

```

### app\services\workers\learning_unit_worker.py

```py
import asyncio
import uuid
from dataclasses import dataclass

from sqlmodel import Session

from app.core.config import settings
from app.core.constant import ProcessingJobStatus
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import LearningUnit
from app.repositories.learning_unit_repo import delete_unit_segments, unit_segments_exist, update_learning_unit_processing
from app.services.async_limiter import get_loop_semaphore
from app.services.workers.learning_unit_tts_worker import run_learning_unit_tts_pipeline


@dataclass(frozen=True)
class LearningUnitProcessingResult:
    learning_unit_id: uuid.UUID
    main_segment_count: int
    skipped: bool = False


async def _cancel_pending_tasks(tasks: list[asyncio.Task]) -> None:
    for task in tasks:
        if not task.done():
            task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


def _cleanup_failed_unit(learning_unit_id: uuid.UUID, unit_index: int, error_message: str) -> None:
    with Session(engine) as session:
        unit = session.get(LearningUnit, learning_unit_id)
        delete_unit_segments(session, learning_unit_id)
        if unit:
            update_learning_unit_processing(session, unit, status=ProcessingJobStatus.ERROR, error_message=error_message)
    logger.info(f"Cleaned failed side effects for learning unit {unit_index + 1}.")


def _pre_check_and_update_unit_db(
    unit_id: uuid.UUID,
    raw_text_char_count: int,
    estimated_tokens: int,
    estimated_audio_seconds: int
) -> tuple[bool, int]:
    with Session(engine) as session:
        current_unit = session.get(LearningUnit, unit_id)
        if current_unit and current_unit.status == ProcessingJobStatus.READY and unit_segments_exist(session, unit_id):
            return True, current_unit.main_segment_count or 0
        if current_unit:
            update_learning_unit_processing(
                session,
                current_unit,
                status=ProcessingJobStatus.PROCESSING,
                raw_text_char_count=raw_text_char_count,
                estimated_tokens=estimated_tokens,
                estimated_audio_seconds=estimated_audio_seconds,
            )
        return False, 0


def _post_update_unit_db(
    unit_id: uuid.UUID,
    main_segment_count: int,
    generated_audio_seconds: int
) -> None:
    with Session(engine) as session:
        current_unit = session.get(LearningUnit, unit_id)
        if current_unit:
            update_learning_unit_processing(
                session,
                current_unit,
                status=ProcessingJobStatus.READY,
                main_segment_count=main_segment_count,
                estimated_audio_seconds=generated_audio_seconds,
            )


async def process_learning_unit(
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    book_title: str,
    unit: LearningUnit,
    raw_text: str,
    job_id: uuid.UUID | None = None,
    raw_text_char_count: int = 0,
    estimated_tokens: int = 0,
    estimated_audio_seconds: int = 0,
) -> LearningUnitProcessingResult:
    async with get_loop_semaphore("learning_unit_processing", settings.LEARNING_UNIT_PROCESSING_CONCURRENCY):
        logger.info(
            f"Learning unit processing start | unit={unit.unit_index + 1} | mode={unit.mode.value} | "
            f"title={unit.title} | chars={raw_text_char_count or len(raw_text)} | "
            f"estimated_tokens={estimated_tokens} | estimated_audio_seconds={estimated_audio_seconds}"
        )

        is_ready, segment_count = await asyncio.to_thread(
            _pre_check_and_update_unit_db,
            unit.id,
            raw_text_char_count,
            estimated_tokens,
            estimated_audio_seconds
        )
        if is_ready:
            logger.info(f"Learning unit {unit.unit_index + 1} already READY, skip.")
            return LearningUnitProcessingResult(
                learning_unit_id=unit.id,
                main_segment_count=segment_count,
                skipped=True,
            )

        pipeline_tasks: list[asyncio.Task] = []
        try:
            pipeline_tasks = [
                asyncio.create_task(
                    run_learning_unit_tts_pipeline(
                        book_id,
                        unit.id,
                        unit.unit_index,
                        raw_text,
                        unit.mode.value,
                        unit.title,
                    )
                )
            ]
            tts_result = (await asyncio.gather(*pipeline_tasks))[0]
            await asyncio.to_thread(
                _post_update_unit_db,
                unit.id,
                tts_result.main_segment_count,
                tts_result.generated_audio_seconds
            )
            logger.info(f"Learning unit {unit.unit_index + 1} READY | segments={tts_result.main_segment_count}")
            return LearningUnitProcessingResult(unit.id, tts_result.main_segment_count)

        except asyncio.CancelledError:
            logger.warning(f"Learning unit {unit.unit_index + 1} bị hủy vì book job thất bại.")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                await asyncio.to_thread(
                    _cleanup_failed_unit,
                    unit.id,
                    unit.unit_index,
                    "Learning unit processing cancelled because the book job failed."
                )
            except Exception as rollback_err:
                logger.error(f"Failed to clean cancelled learning unit {unit.unit_index + 1}: {rollback_err}")
            raise
        except Exception as exc:
            logger.error(f"Learning unit {unit.unit_index + 1} thất bại: {exc}")
            try:
                await _cancel_pending_tasks(pipeline_tasks)
                await asyncio.to_thread(
                    _cleanup_failed_unit,
                    unit.id,
                    unit.unit_index,
                    str(exc)
                )
            except Exception as rollback_err:
                logger.error(f"Failed to clean failed learning unit {unit.unit_index + 1}: {rollback_err}")
            raise

```

### app\services\workers\__init__.py

```py
"""Worker pipeline package cho background processing."""

```

### app\services\__init__.py

```py
# Services module

```

### app\tasks\book_tasks.py

```py
import asyncio
import uuid

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.constant import ProcessingJobStatus
from app.core.logger import log
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

```

### app\tasks\notification_tasks.py

```py
import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.constant import NotificationChannel, NotificationStatus
from app.core.logger import log
from app.db.database import engine
from app.repositories.notification_outbox_repo import (
    claim_due_outbox,
    get_outbox_by_id,
    has_due_outbox,
    mark_outbox_failed,
    mark_outbox_retry,
    recover_stale_outbox,
)
from app.services.notification_event_service import (
    create_due_plan_reminder_outbox_rows,
    create_due_review_outbox_rows,
    create_missed_plan_session_outbox_rows,
    deliver_outbox_notification,
)
from app.services.reading_plan_session_service import mark_due_sessions_missed


@celery_app.task(name="triam.notifications.scan_due")
def scan_due_notifications_task() -> None:
    now = datetime.now(timezone.utc)
    created_count = 0
    recovered_count = 0
    should_deliver = False

    with Session(engine) as session:
        recovered_count = recover_stale_outbox(
            session,
            now=now,
            stale_before=now - timedelta(minutes=settings.NOTIFICATION_STALE_LOCK_MINUTES),
            max_attempts=settings.NOTIFICATION_MAX_ATTEMPTS,
        )
        created_count += create_due_review_outbox_rows(session, now=now)
        created_count += create_due_plan_reminder_outbox_rows(session, now=now)
        mark_due_sessions_missed(session, now=now)
        created_count += create_missed_plan_session_outbox_rows(session, now=now)
        session.commit()
        should_deliver = created_count > 0 or recovered_count > 0 or has_due_outbox(session, now=now)

    log.info(f"Notification scan done | created={created_count} | recovered={recovered_count} | should_deliver={should_deliver}")
    if should_deliver:
        deliver_due_notifications_task.apply_async(queue="notification")


@celery_app.task(name="triam.notifications.deliver_due")
def deliver_due_notifications_task() -> None:
    now = datetime.now(timezone.utc)
    worker_id = f"notification-worker:{uuid.uuid4()}"

    with Session(engine) as session:
        recover_stale_outbox(
            session,
            now=now,
            stale_before=now - timedelta(minutes=settings.NOTIFICATION_STALE_LOCK_MINUTES),
            max_attempts=settings.NOTIFICATION_MAX_ATTEMPTS,
        )
        outbox_ids = claim_due_outbox(
            session,
            now=now,
            limit=settings.NOTIFICATION_DELIVERY_BATCH_SIZE,
            worker_id=worker_id,
        )

    for outbox_id in outbox_ids:
        deliver_one_notification(outbox_id)

    log.info(f"Notification delivery batch done | worker_id={worker_id} | delivered_attempts={len(outbox_ids)}")


def _next_retry_at(attempts: int, now: datetime) -> datetime:
    delay_seconds = min(3600, 60 * (2 ** max(0, attempts - 1)))
    return now + timedelta(seconds=delay_seconds)


def deliver_one_notification(outbox_id: uuid.UUID) -> None:
    now = datetime.now(timezone.utc)
    with Session(engine) as session:
        outbox = get_outbox_by_id(session, outbox_id)
        if not outbox or outbox.status != NotificationStatus.PROCESSING:
            return

        try:
            if outbox.channel not in (NotificationChannel.IN_APP, NotificationChannel.PUSH, NotificationChannel.ALL):
                raise ValueError(f"Unsupported notification channel: {outbox.channel}")
            deliver_outbox_notification(session, outbox, now=now)
        except Exception as exc:
            error_message = str(exc)
            log.warning(f"Notification delivery failed | outbox_id={outbox_id} | attempts={outbox.attempts} | error={error_message}")
            if outbox.attempts >= settings.NOTIFICATION_MAX_ATTEMPTS:
                mark_outbox_failed(session, outbox, error_message=error_message)
            else:
                mark_outbox_retry(
                    session,
                    outbox,
                    next_retry_at=_next_retry_at(outbox.attempts, now),
                    error_message=error_message,
                )

```

### app\tasks\__init__.py

```py
"""Celery task modules for Triam."""

```

### app\__init__.py

```py
# TRIAM Backend Application

```

### pyproject.toml

*(Unsupported file type)*
