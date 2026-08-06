import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.constant import DocumentType, PlanMode
from app.schemas.learning_progress import BookLearningSummaryResponse


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    author: Optional[str] = None
    total_sections: Optional[int] = None
    total_units: Optional[int] = None
    status: Optional[str] = None
    ai_summary: Optional[dict] = None
    ai_summary_status: Optional[str] = None
    ai_summary_error: Optional[str] = None
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
    ai_summary: Optional[dict] = None
    ai_summary_status: Optional[str] = None
    ai_summary_error: Optional[str] = None
    learning_summary: Optional[BookLearningSummaryResponse] = None
    units: list[LearningUnitDetailResponse] = Field(default_factory=list)


class BookOutlineNodeResponse(BaseModel):
    id: uuid.UUID
    title: str
    level: int
    path: str
    page_start: int | None = None
    page_end: int | None = None
    children: list["BookOutlineNodeResponse"] = Field(default_factory=list)


class SharedBookPreviewUnitResponse(BaseModel):
    id: uuid.UUID
    title: str
    status: str | None = None
    unit_index: int
    unit_type: str
    estimated_audio_seconds: int = 0
    planner_reason: str | None = None
    has_audio_sample: bool = False


class SharedBookPreviewResponse(BaseModel):
    """Small pre-clone catalog payload: book structure plus one playable sample."""

    book: BookResponse
    mode: PlanMode
    available_modes: list[PlanMode] = Field(default_factory=list)
    total_sections: int = 0
    outline_tree: list[BookOutlineNodeResponse] = Field(default_factory=list)
    total_units: int = 0
    learning_outline: list[SharedBookPreviewUnitResponse] = Field(default_factory=list)
    audio_sample: LearningUnitDetailResponse | None = None


class SwitchModeResponse(BaseModel):
    message: str
    needs_generation: bool
    job_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    progress_percent: Optional[int] = None
