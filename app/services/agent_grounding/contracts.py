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

