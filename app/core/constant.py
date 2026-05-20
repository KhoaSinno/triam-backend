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
