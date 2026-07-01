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


class AdminBookDetailResponse(AdminBookListItem):
    latest_job: AdminJobListItem | None = None
    learning_units_by_status: dict[str, int] = Field(default_factory=dict)
    segment_count: int = 0


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
