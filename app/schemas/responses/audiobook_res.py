"""
app/schemas/responses/audiobook_res.py
=======================================
Response DTOs cho module Audiobook.

Chỉ expose các trường Flutter FE thực sự cần — không lộ thông tin nội bộ
(user_id, error_message, db relationships, ...).
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.constant import DocumentType


class BookResponse(BaseModel):
    """DTO cho một cuốn sách — dùng cho GET /books và GET /books/{id}."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    author: Optional[str] = None
    total_chapters: Optional[int] = None
    status: Optional[str] = None
    document_type: Optional[DocumentType] = None
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SegmentResponse(BaseModel):
    """DTO cho một segment audio trong chapter."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    segment_index: int
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    duration_ms: Optional[int] = None
    mode: str


class ChapterDetailResponse(BaseModel):
    """DTO cho một chapter kèm danh sách segments."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    status: Optional[str] = None
    chapter_index: int
    review_text: str = ""
    review_audio_url: str = ""
    chapter_segments: list[SegmentResponse] = Field(default_factory=list)


class BookDetailResponse(BaseModel):
    """DTO cho response của GET /books/{id}/details — sách kèm toàn bộ chapters."""

    model_config = ConfigDict(from_attributes=True)

    book_status: Optional[str] = None
    total_chapters: Optional[int] = None
    chapters: list[ChapterDetailResponse] = Field(default_factory=list)


class SwitchModeResponse(BaseModel):
    """DTO cho response của POST /books/{id}/switch-mode."""

    message: str
    needs_generation: bool
    job_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    progress_percent: Optional[int] = None
