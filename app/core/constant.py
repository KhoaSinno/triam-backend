from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class BookStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class DocumentType(str, Enum):
    PDF = "pdf"
    EPUB = "epub"
    DOCX = "docx"


class PlanMode(str, Enum):
    FULL = "full"
    PARETO = "pareto"
