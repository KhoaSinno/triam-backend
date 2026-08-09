import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType, SummaryStatus


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
    is_active: bool = True
    is_admin: bool = False
    banned_until: datetime | None = None
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


class AdminUserStatusUpdatePayload(BaseModel):
    is_active: bool
    ban_reason: str | None = Field(default=None, max_length=255)


class AdminUserStatusUpdateResponse(BaseModel):
    user_id: uuid.UUID
    is_active: bool
    banned_until: datetime | None = None
    message: str


class AdminUserDirectNotifyPayload(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(min_length=1, max_length=500)
    data: dict[str, str] | None = None
    idempotency_key: str = Field(min_length=8, max_length=120)


class AdminUserDirectNotifyResponse(BaseModel):
    user_id: uuid.UUID
    outbox_id: uuid.UUID
    status: str
    message: str


class AdminUserStatsResponse(BaseModel):
    user_id: uuid.UUID
    display_name: str | None = None
    email: str | None = None
    total_listened_ms: int = 0
    total_hours_listened: float = 0.0
    total_sessions_completed: int = 0
    total_units_completed: int = 0
    total_reviews_completed: int = 0
    books_owned_count: int = 0
    created_at: datetime | None = None
    last_active_at: datetime | None = None


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
    file_url: str | None = None
    latest_job: AdminJobListItem | None = None
    learning_units_by_status: dict[str, int] = Field(default_factory=dict)
    segment_count: int = 0
    owner_info: AdminBookOwnerInfo | None = None
    ai_summary: dict[str, Any] | None = None
    ai_summary_status: SummaryStatus = SummaryStatus.PENDING
    ai_summary_error: str | None = None


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


class AdminSegmentItem(BaseModel):
    id: int
    segment_index: int
    audio_url: str | None = None
    text_content: str | None = None
    duration_ms: int | None = None


class AdminLearningUnitSourceItem(BaseModel):
    section_id: uuid.UUID
    section_index: int
    section_title: str
    section_path: str
    page_start: int | None = None
    page_end: int | None = None
    source_order: int


class AdminLearningUnitItem(BaseModel):
    id: uuid.UUID
    unit_index: int
    title: str
    unit_type: str
    mode: str
    status: str
    estimated_audio_seconds: int
    main_segment_count: int
    review_text: str | None = None
    review_audio_url: str | None = None
    planner_reason: str | None = None
    segments: list[AdminSegmentItem] = []
    sources: list[AdminLearningUnitSourceItem] = []


class AdminBookAudioUnitsResponse(BaseModel):
    book_id: uuid.UUID
    mode: str
    total_units: int
    units: list[AdminLearningUnitItem]


class AdminBookUpdateMetadataRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)
    is_shared: bool | None = None


class AdminBookSummaryResponse(BaseModel):
    book_id: uuid.UUID
    status: str
    ai_summary: dict[str, Any] | None = None
    error_message: str | None = None


class AdminBookUploadResponse(BaseModel):
    book_id: uuid.UUID
    job_id: uuid.UUID
    message: str


class AdminCancelJobResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    message: str
    rolled_back: bool = True
