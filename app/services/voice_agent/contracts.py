import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

LK_CHAT_TOPIC = "lk.chat"
LK_CONTROL_TOPIC = "lk.control"
LK_TRANSCRIPT_TOPIC = "lk.transcript"

TranscriptRole = Literal["user", "assistant"]
WebPermissionIntent = Literal["grant", "deny", "unclear", "new_question"]


@dataclass(frozen=True)
class VoiceJobMetadata:
    thread_id: str
    document_ids: list[str]
    context_id: str = ""
    user_id: str = ""


@dataclass(frozen=True)
class VoiceContextResolution:
    """Server-validated study scope used by one live voice session."""

    context_id: uuid.UUID
    thread_id: uuid.UUID
    document_ids: tuple[str, ...]
    context_title: str
    thread_title: str


@dataclass(frozen=True)
class VoiceRagResult:
    found: bool
    chunks: list[dict[str, Any]]
    message: str


@dataclass(frozen=True)
class WebSearchPermissionDecision:
    granted_query: str | None = None
    denied: bool = False
    unclear: bool = False
    new_question: str | None = None


@dataclass(frozen=True)
class WebPermissionIntentResult:
    intent: WebPermissionIntent
    confidence: float
    reason: str = ""
    source: str = "classifier"


@dataclass
class WebSearchPermissionState:
    enabled: bool = False
    pending_query: str | None = None
    pending_request_id: str | None = None
    last_user_reply: str | None = None
    last_user_reply_at: datetime | None = None
    granted_query: str | None = None
    granted_request_id: str | None = None
    granted_at: datetime | None = None
