"""
app/schemas/responses/study_context_res.py
===========================================
Response DTOs cho module Study Context.

Chỉ expose các trường Flutter FE thực sự cần — không lộ user_id,
không kéo theo lazy-load relationships.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudyContextResponse(BaseModel):
    """DTO cho StudyContext — ẩn user_id (internal field)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    is_auto_generated: bool = False
    created_at: datetime
    updated_at: datetime


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
