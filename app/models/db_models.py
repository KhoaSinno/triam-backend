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
    schedule_config: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
    status: str = Field(sa_column=Column(Text, nullable=False))
    reminder_time: str = Field(default="20:00", sa_column=Column(Text, nullable=False, server_default="20:00"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

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


class NotificationSettings(SQLModel, table=True):
    __tablename__ = "notification_settings"

    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), primary_key=True))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False))
    reminders_enabled: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    spaced_review_enabled: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    reminder_time: str = Field(default="20:00", sa_column=Column(Text, nullable=False))
    quiet_hours_start: str = Field(default="22:00", sa_column=Column(Text, nullable=False))
    quiet_hours_end: str = Field(default="07:00", sa_column=Column(Text, nullable=False))
    daily_cap: int = Field(default=3, sa_column=Column(Integer, nullable=False))
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
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )


class BookKnowledge(SQLModel, table=True):
    __tablename__ = "book_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    learning_unit_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    # TODO: REPALCE 1536 (OpenAI text-embedding-3-small)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))

    __table_args__ = (UniqueConstraint("learning_unit_id", "chunk_index", name="uq_book_knowledge_unit_chunk_index"),)


class BookSectionKnowledge(SQLModel, table=True):
    __tablename__ = "book_section_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    section_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("book_sections.id", ondelete="CASCADE"), index=True, nullable=False))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
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
