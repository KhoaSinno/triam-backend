from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
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


class ReviewAction(str, Enum):
    COMPLETE = "complete"
    SKIP = "skip"
