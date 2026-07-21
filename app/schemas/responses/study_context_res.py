"""
app/schemas/responses/study_context_res.py
===========================================
Response DTOs cho module Study Context.

Chỉ expose các trường Flutter FE thực sự cần — không lộ user_id,
không kéo theo lazy-load relationships.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.responses.audiobook_res import BookResponse


class ContextCapabilityResponse(BaseModel):
    """Metadata quyền hạn thao tác trên UI phía Flutter FE."""
    can_add_documents: bool = False
    can_remove_documents: bool = False
    can_create_threads: bool = True
    can_rename_context: bool = True
    can_delete_context: bool = True
    can_rename_threads: bool = True
    can_delete_threads: bool = True


class StudyContextResponse(BaseModel):
    """DTO cho StudyContext — Nạp sẵn thông tin tài liệu liên kết và cờ quyền hạn."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    is_auto_generated: bool = False
    document_count: int = 0
    documents: List[BookResponse] = Field(default_factory=list)
    capabilities: Optional[ContextCapabilityResponse] = None
    created_at: datetime
    updated_at: datetime


class DirectBookThreadResponse(BaseModel):
    """DTO phản hồi cho Endpoint GET /threads/for-book/{book_id} chuẩn FE Contract."""

    context_id: uuid.UUID
    thread_id: uuid.UUID
    is_auto_generated: bool = True
    book_id: uuid.UUID
    book_title: str
    context_title: str
    thread_title: str


class ChatThreadResponse(BaseModel):
    """DTO cho ChatThread — không kéo theo relationship messages."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    context_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageResponse(BaseModel):
    """DTO cho ChatMessage — không kéo theo relationship thread."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thread_id: uuid.UUID
    is_user: bool
    text: str
    source: str
    timestamp: datetime


class ContextDocumentResponse(BaseModel):
    """DTO cho StudyContextDocumentLink."""

    model_config = ConfigDict(from_attributes=True)

    context_id: uuid.UUID
    book_id: uuid.UUID
