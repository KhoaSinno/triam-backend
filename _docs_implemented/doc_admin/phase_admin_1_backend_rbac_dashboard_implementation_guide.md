# Phase Admin 1 Implementation Guide - Backend Admin RBAC And Operations Dashboard

Date: 2026-06-02  
Status: **Implemented and tested locally**  
Scope: Backend-only admin foundation for Tri Âm Admin Web  
Frontend target: Separate Next.js + TypeScript admin project  
Backend branch used: `dev`  
Audience: Backend developer, admin frontend developer, capstone reviewer

---

## 1. Decisions Confirmed

Em đã chốt các quyết định sau:

1. Admin vẫn login bằng Supabase Auth như user thường.
2. Backend thêm bước kiểm tra role admin cho các route `/api/v1/admin/*`.
3. Role admin dùng bảng DB riêng `admin_users`.
4. Phase Admin 1 làm:
   - `/admin/me`
   - `/admin/dashboard`
   - `/admin/users`
   - `/admin/books`
   - `/admin/jobs`
   - `/admin/audit-logs`
5. Phase Admin 1 chỉ xem dữ liệu và retry job. Chưa khóa user, chưa xóa sách user.
6. System book ingest/publish để Phase Admin 2.
7. Admin action phải có audit log ngay từ Phase Admin 1.

---

## 2. Goal

Tri Âm hiện có actor chính là:

```text
Reader = người dùng app học/nghe sách.
```

Tuy nhiên một hệ thống capstone hoàn chỉnh cần thêm actor vận hành:

```text
Admin = người quản trị nội dung, user, job, chi phí, lỗi hệ thống.
```

Phase Admin 1 tạo nền tảng backend để Admin Web có thể:

- xác nhận người đang login có quyền admin;
- xem dashboard tổng quan;
- xem danh sách user;
- xem danh sách sách;
- xem danh sách job xử lý;
- retry job lỗi;
- xem audit log admin action.

Không làm ở phase này:

- không làm ingest sách hệ thống;
- không làm publish/unpublish system book;
- không xem raw Hugging Face/LiveKit/Redis/Supabase logs;
- không xóa sách user;
- không khóa user;
- không expose service-role key hoặc provider secret.

---

## 3. Architecture Principle

Admin Web không được gọi trực tiếp Redis, Supabase service role, LiveKit secret, Hugging Face token.

Luồng đúng:

```text
Admin Web
  -> Supabase login
  -> gets access_token
  -> calls FastAPI with Bearer token
  -> FastAPI verifies Supabase token
  -> FastAPI checks admin_users
  -> FastAPI returns sanitized admin data
```

```mermaid
flowchart TD
    A[Next.js Admin Web] -->|Supabase Login| B[Supabase Auth]
    B -->|access_token| A
    A -->|Bearer token| C[FastAPI Admin API]
    C --> D[get_current_user]
    D --> E[require_admin_user]
    E -->|check user_id| F[(admin_users)]
    E -->|allowed| G[/api/v1/admin/*]
    G --> H[(Postgres app tables)]
    G --> I[Redis health summary]
    G --> J[Audit log]
```

Rule:

```text
Only FastAPI holds privileged secrets.
Admin Web is an authenticated UI, not an infrastructure client.
```

---

## 4. Branch Strategy

Original recommendation:

```powershell
git checkout dev
git pull
git checkout -b dev-admin
```

Final decision for this project:

```text
Backend continues on branch dev.
Admin Web can still be developed as a separate sibling project.
```

Optional larger-team flow:

```text
dev-admin -> test -> merge dev -> test -> merge main when deploy-ready
```

Admin web should live as a sibling project:

```text
_CAPSTON_PROJECT/
  triam-backend/
  triam-admin-web/
  triam-mobile-flutter/
```

---

## 5. Database Design

### 5.1 `admin_users`

Purpose:

```text
Defines which authenticated Supabase users are allowed to call admin APIs.
```

SQLModel model:

```python
class AdminUser(SQLModel, table=True):
    __tablename__ = "admin_users"

    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), primary_key=True))
    role: str = Field(default="admin", sa_column=Column(Text, nullable=False, server_default="admin"))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, index=True, nullable=False, server_default="true"))
    note: str | None = Field(default=None, sa_column=Column(Text))
    created_by: uuid.UUID | None = Field(default=None, sa_column=Column(UUID(as_uuid=True)))
    revoked_by: uuid.UUID | None = Field(default=None, sa_column=Column(UUID(as_uuid=True)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    revoked_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
```

Recommended indexes:

```text
PK: user_id
index: is_active
```

Why not use only Supabase `app_metadata` now:

- DB table is easier to query from BE.
- Admin can be revoked immediately by setting `is_active=false`.
- No need to wait for JWT refresh.
- Easier to explain in capstone.
- Easier to audit.

Later, if system grows:

```text
admin_users -> user_roles + role_permissions
```

For now, `admin_users` is the right practical design.

### 5.2 `admin_audit_logs`

Purpose:

```text
Records important admin actions.
```

SQLModel model:

```python
class AdminAuditLog(SQLModel, table=True):
    __tablename__ = "admin_audit_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    admin_user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    action: str = Field(sa_column=Column(Text, index=True, nullable=False))
    target_type: str | None = Field(default=None, sa_column=Column(Text, index=True))
    target_id: uuid.UUID | None = Field(default=None, sa_column=Column(UUID(as_uuid=True), index=True))
    metadata: dict[str, Any] | None = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True))
```

Example actions:

```text
admin.login_check
job.retry
book.view_detail
user.view_detail
```

Do not store:

- raw Authorization header;
- provider API key;
- Supabase service role key;
- full raw document text;
- full conversation transcript.

---

## 6. Backend Layer Design

Follow current Tri Âm architecture:

```text
router -> service -> repository -> model/database
```

Recommended files:

```text
app/api/dependencies/admin.py
app/api/v1/routers/admin.py
app/repositories/admin_repo.py
app/services/admin_service.py
app/schemas/admin.py
tests/test_admin_api.py
```

Optional split later:

```text
app/api/v1/routers/admin_dashboard.py
app/api/v1/routers/admin_books.py
app/api/v1/routers/admin_jobs.py
```

For Phase Admin 1, one router file is acceptable if kept clean.

---

## 7. Admin Dependency

### 7.1 Current auth stays unchanged

Existing dependency:

```python
CurrentUser = Annotated[UserTokenPayload, Depends(get_current_user)]
```

Do not modify user routes.

### 7.2 New admin dependency

File:

```text
app/api/dependencies/admin.py
```

Recommended dependency:

```python
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.repositories.admin_repo import get_active_admin_user
from app.schemas.user import UserTokenPayload


def require_admin_user(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> UserTokenPayload:
    admin = get_active_admin_user(session, current_user.sub)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập trang quản trị.",
        )
    return current_user


AdminUserToken = Annotated[UserTokenPayload, Depends(require_admin_user)]
```

Why `403`:

```text
401 = chưa xác thực / token sai.
403 = đã xác thực nhưng không có quyền admin.
```

---

## 8. Admin API Contract

All endpoints require:

```http
Authorization: Bearer <supabase_access_token>
```

Base path:

```text
/api/v1/admin
```

### 8.1 `GET /admin/me`

Purpose:

```text
Admin Web calls this after login to verify admin access.
```

Response:

```json
{
  "user_id": "uuid",
  "email": "admin@example.com",
  "role": "admin",
  "is_active": true
}
```

If user is not admin:

```json
403
{
  "detail": "Bạn không có quyền truy cập trang quản trị."
}
```

### 8.2 `GET /admin/dashboard`

Purpose:

```text
High-level operational snapshot.
```

Recommended response:

```json
{
  "users": {
    "total": 120,
    "active_24h": 14
  },
  "books": {
    "total": 230,
    "ready": 190,
    "processing": 5,
    "error": 3
  },
  "jobs": {
    "queued": 2,
    "processing": 1,
    "partial_ready": 0,
    "ready": 80,
    "error": 4
  },
  "usage": {
    "estimated_input_tokens_30d": 1200000,
    "estimated_audio_seconds_30d": 36000
  },
  "notifications": {
    "due_items_last_scan": 0
  }
}
```

Implementation note:

- Use aggregate queries.
- Do not fetch all rows then count in Python.
- If metrics become slow later, cache or materialize.

### 8.3 `GET /admin/users`

Purpose:

```text
List app users as seen by app data.
```

Because app does not currently mirror all Supabase Auth users into a `users` table, Phase 1 should derive users from app tables:

```text
distinct user_id from books, processing_jobs, notification_settings, learning_unit_progress
```

Recommended query result:

```json
{
  "items": [
    {
      "user_id": "uuid",
      "book_count": 3,
      "active_book_count": 1,
      "job_count": 7,
      "last_activity_at": "2026-06-02T05:00:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

Do not try to list all Supabase Auth users with service role in Phase 1 unless needed. It adds provider dependency and needs stricter secret handling.

### 8.4 `GET /admin/books`

Purpose:

```text
Admin sees all books across all users.
```

Filters:

```text
status
document_type
user_id
q
limit
offset
```

Response item:

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Logic",
  "author": null,
  "document_type": "docx",
  "status": "ready",
  "total_sections": 122,
  "total_units": 4,
  "created_at": "2026-06-02T05:00:00Z",
  "updated_at": "2026-06-02T05:30:00Z"
}
```

Security:

- Do not include signed storage URLs by default.
- Do not include full source text.
- Error message can be truncated.

### 8.5 `GET /admin/books/{book_id}`

Purpose:

```text
Admin detail for a book.
```

Include:

- book metadata;
- latest processing job;
- learning unit counts by mode/status;
- segment count;
- error message truncated.

Do not include:

- full `text_content`;
- raw audio file signed URLs unless explicitly needed.

### 8.6 `GET /admin/jobs`

Purpose:

```text
List processing jobs across all users.
```

Filters:

```text
status
job_type
book_id
user_id
limit
offset
```

Response item:

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "book_id": "uuid",
  "job_type": "GENERATE_PLAN",
  "status": "ERROR",
  "mode": "pareto",
  "progress_percent": 80,
  "done_units": 3,
  "failed_units": 1,
  "current_step": "TTS failed",
  "error_message": "Google TTS input quá dài...",
  "created_at": "2026-06-02T05:00:00Z",
  "updated_at": "2026-06-02T05:30:00Z"
}
```

### 8.7 `POST /admin/jobs/{job_id}/retry`

Purpose:

```text
Admin retries an error/cancelled job.
```

Phase 1 allowed job types:

```text
GENERATE_PLAN
SWITCH_MODE
```

Rules:

- Only retry jobs in `ERROR` or `CANCELLED`.
- Do not retry `READY`.
- Do not retry `PROCESSING`.
- Re-enqueue to correct Celery queue `document`.
- Create audit log:

```text
action = "job.retry"
target_type = "processing_job"
target_id = job_id
```

Important:

Use existing worker task functions and queue design. Do not run long processing inside admin request.

### 8.8 `GET /admin/audit-logs`

Purpose:

```text
Admin sees admin actions.
```

Filters:

```text
admin_user_id
action
target_type
target_id
limit
offset
```

Response:

```json
{
  "items": [
    {
      "id": "uuid",
      "admin_user_id": "uuid",
      "action": "job.retry",
      "target_type": "processing_job",
      "target_id": "uuid",
      "metadata": {
        "old_status": "ERROR",
        "new_status": "QUEUED"
      },
      "created_at": "2026-06-02T05:30:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

---

## 9. Repository Plan

File:

```text
app/repositories/admin_repo.py
```

Functions:

```python
def get_active_admin_user(session: Session, user_id: uuid.UUID) -> AdminUser | None: ...

def create_admin_audit_log(
    session: Session,
    *,
    admin_user_id: uuid.UUID,
    action: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    metadata: dict[str, Any] | None = None,
) -> AdminAuditLog: ...

def get_dashboard_summary(session: Session) -> AdminDashboardSummary: ...
def list_admin_books(session: Session, filters: AdminBookFilters) -> tuple[list[AdminBookRow], int]: ...
def get_admin_book_detail(session: Session, book_id: uuid.UUID) -> AdminBookDetail | None: ...
def list_admin_jobs(session: Session, filters: AdminJobFilters) -> tuple[list[ProcessingJob], int]: ...
def list_admin_audit_logs(session: Session, filters: AdminAuditLogFilters) -> tuple[list[AdminAuditLog], int]: ...
```

Keep repository DB-only:

- no Celery calls;
- no HTTP calls;
- no Supabase Storage;
- no LiveKit.

---

## 10. Service Plan

File:

```text
app/services/admin_service.py
```

Responsibilities:

- call repository functions;
- enforce admin business rules;
- truncate sensitive/error fields if needed;
- retry allowed jobs by enqueuing Celery task;
- create audit logs.

Retry job pseudo-flow:

```text
admin clicks retry
-> service loads job
-> validate job status ERROR/CANCELLED
-> validate job_type
-> reset job status QUEUED/progress fields
-> enqueue Celery task
-> create audit log
-> return job summary
```

Important:

If enqueue fails:

- set job back to `ERROR`;
- store meaningful error;
- return `ExternalServiceError`.

---

## 11. Router Plan

File:

```text
app/api/v1/routers/admin.py
```

Router:

```python
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin_user)],
)
```

But for `GET /admin/me`, still use `AdminUserToken` to return current admin identity.

Then include in app router:

```python
api_router.include_router(admin.router)
```

Check current project router registration before implementation. If there is no central `api_router`, include it in `app/main.py` matching existing pattern.

---

## 12. Schemas

File:

```text
app/schemas/admin.py
```

Recommended DTOs:

```python
class AdminMeResponse(BaseModel): ...
class AdminDashboardResponse(BaseModel): ...
class AdminUserListItem(BaseModel): ...
class AdminBookListItem(BaseModel): ...
class AdminBookDetailResponse(BaseModel): ...
class AdminJobListItem(BaseModel): ...
class AdminAuditLogItem(BaseModel): ...
class PaginatedResponse[T](BaseModel): ...
```

If generic pagination causes Pydantic complexity, use explicit response classes:

```python
class AdminBooksResponse(BaseModel):
    items: list[AdminBookListItem]
    total: int
    limit: int
    offset: int
```

Keep DTOs separate from DB models. Do not expose `Book` or `ProcessingJob` directly for admin endpoints.

---

## 13. Alembic Migration

Create migration:

```powershell
uv run alembic revision --autogenerate -m "admin users and audit logs"
```

Review generated migration carefully.

Expected:

```text
create_table admin_users
create_table admin_audit_logs
create_index admin_users_is_active
create_index admin_audit_logs_created_at
create_index admin_audit_logs_action
create_index admin_audit_logs_target_type
create_index admin_audit_logs_target_id
```

Do not let Alembic accidentally drop/alter unrelated tables.

Apply:

```powershell
uv run alembic upgrade head
```

---

## 14. First Admin Bootstrap

After migration:

1. Login/register an admin account through Supabase Auth.
2. Copy user id from Supabase Auth.
3. Insert into DB:

```sql
insert into admin_users (user_id, role, is_active, note)
values ('<supabase-user-id>', 'admin', true, 'Founder admin');
```

Local dev:

```text
Use dev Supabase project, not production.
```

Production:

```text
Insert only the real admin user id.
Do not use mock admin user.
Do not commit admin user id into code.
```

---

## 15. Security Rules

1. Admin API must require normal auth and admin role.
2. User APIs must not call admin dependency.
3. Admin Web must not receive service role key.
4. Admin API must not return raw provider secrets.
5. Admin API must not return full document text by default.
6. Audit log all admin mutations.
7. Retry job should be a controlled operation, not arbitrary task execution.
8. Avoid raw logs in Phase 1. Use sanitized error summaries.

---

## 16. Tests

Add:

```text
tests/test_admin_api.py
```

Required cases:

```text
GET /admin/me
  - no token -> 401
  - authenticated non-admin -> 403
  - active admin -> 200

GET /admin/dashboard
  - non-admin -> 403
  - admin -> 200

GET /admin/books
  - admin sees books across users
  - response does not include full text_content

GET /admin/jobs
  - admin sees jobs across users

POST /admin/jobs/{job_id}/retry
  - non-admin -> 403
  - admin can retry ERROR job
  - cannot retry READY job
  - creates admin_audit_logs row
```

Use dependency override for `get_current_user` in tests.

Do not call real Supabase Auth in unit tests.

---

## 17. Manual API Test

After implementation and migration:

```powershell
make gat
```

Use admin token:

```powershell
$token = "<admin-access-token>"
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/admin/me" `
  -Headers @{ Authorization = "Bearer $token" }
```

Expected admin:

```json
{
  "user_id": "...",
  "email": "...",
  "role": "admin",
  "is_active": true
}
```

Expected non-admin:

```json
{
  "detail": "Bạn không có quyền truy cập trang quản trị."
}
```

---

## 18. Admin Web Notes

Next.js admin should call:

```text
GET /api/v1/admin/me
```

right after login.

If 403:

```text
Show "Bạn không có quyền truy cập trang quản trị."
Sign out or redirect to normal app.
```

Admin Web env:

```env
NEXT_PUBLIC_API_BASE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

No service-role key in Next.js.

---

## 19. What Comes Next

### Phase Admin 2 - System Book Ingest

Goal:

```text
Admin uploads/publishes books that all readers can use.
```

Likely DB additions:

```text
book_visibility: user_private | system_public
published_at
published_by
category/tags
```

Flow:

```text
Admin upload
-> parse outline
-> preview
-> generate audio
-> publish
-> reader can add system book to study plan
```

### Phase Admin 3 - Operations Monitoring

Goal:

- Redis queue depth summary;
- Celery worker heartbeat;
- provider usage ledger;
- error rate by day;
- TTS/LLM estimated cost.

### Phase Admin 4 - External Observability Integration

Goal:

- Sentry or equivalent error tracking;
- LiveKit log drain/webhooks;
- Hugging Face logs as external link or summarized ingestion;
- provider billing dashboard links.

---

## 20. Done Criteria

Phase Admin 1 is complete when:

- [x] `admin_users` table exists.
- [x] `admin_audit_logs` table exists.
- [x] Admin dependency returns 403 for non-admin.
- [x] User routes still work normally.
- [x] `/api/v1/admin/me` works.
- [x] `/api/v1/admin/dashboard` works.
- [x] `/api/v1/admin/users` works.
- [x] `/api/v1/admin/books` works.
- [x] `/api/v1/admin/jobs` works.
- [x] `/api/v1/admin/jobs/{job_id}/retry` works for allowed jobs.
- [x] `/api/v1/admin/audit-logs` works.
- [x] Retry job creates audit log.
- [x] Tests pass.
- [x] No raw secrets or raw document text returned.

---

## 21. Implementation Result

Implemented files:

```text
app/models/db_models.py
app/db/migrations/versions/2b7c9d1e4f6a_admin_users_and_audit_logs.py
app/api/dependencies/admin.py
app/api/v1/routers/admin.py
app/repositories/admin_repo.py
app/services/admin_service.py
app/schemas/admin.py
tests/test_admin_api.py
.agents/skills/fastapi-sqlmodel-clean-architecture/SKILL.md
```

Registered router:

```text
/api/v1/admin/*
```

Migration applied:

```powershell
uv run alembic upgrade head
uv run alembic current
```

Current head:

```text
2b7c9d1e4f6a
```

Validation run:

```powershell
uv run ruff check app\api\dependencies\admin.py app\api\v1\routers\admin.py app\services\admin_service.py app\repositories\admin_repo.py app\schemas\admin.py app\models\db_models.py app\core\exceptions.py tests\test_admin_api.py
uv run pytest tests\test_admin_api.py -q
uv run pytest tests\test_auth_user_isolation.py tests\test_processing_jobs_api.py tests\test_celery_enqueue.py -q
uv run python -m py_compile app\api\dependencies\admin.py app\api\v1\routers\admin.py app\services\admin_service.py app\repositories\admin_repo.py app\schemas\admin.py
```

Result:

```text
ruff: passed
tests/test_admin_api.py: 4 passed
auth/jobs/celery related tests: 11 passed
py_compile: passed
```

Important production note:

```text
Admin account is not bootstrapped in code.
After deploying migration, insert the real Supabase user_id into admin_users manually.
```

Example:

```sql
insert into admin_users (user_id, role, is_active, note)
values ('<supabase-user-id>', 'admin', true, 'Founder admin');
```
