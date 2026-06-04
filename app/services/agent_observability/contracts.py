from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentInputMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"


class AgentAnswerSource(str, Enum):
    UNKNOWN = "unknown"
    BOOK_METADATA = "book_metadata"
    BOOK_SECTION = "book_section"
    BOOK_RAG = "book_rag"
    WEB = "web"
    CLARIFICATION = "clarification"
    POLICY = "policy"
    ERROR = "error"


@dataclass
class AgentTurnTrace:
    trace_id: str
    thread_id: str | None
    room_name: str | None
    input_mode: AgentInputMode
    started_at: datetime
    started_monotonic: float = field(repr=False)
    completed_at: datetime | None = None
    completed_monotonic: float | None = field(default=None, repr=False)
    transcript_final_seen: bool = False
    transcript_char_count: int = 0
    detected_language: str | None = None
    detected_intent: str | None = None
    resolved_book_ids: list[str] = field(default_factory=list)
    resolved_section_ids: list[str] = field(default_factory=list)
    retrieval_method: str | None = None
    retrieval_result_count: int = 0
    retrieval_chunk_ids: list[str] = field(default_factory=list)
    retrieval_learning_unit_ids: list[str] = field(default_factory=list)
    retrieval_section_ids: list[str] = field(default_factory=list)
    retrieval_scores: list[float] = field(default_factory=list)
    tool_names: list[str] = field(default_factory=list)
    answer_source: AgentAnswerSource = AgentAnswerSource.UNKNOWN
    assistant_char_count: int = 0
    stage_latency_ms: dict[str, int] = field(default_factory=dict)
    error_code: str | None = None
    correlation_quality: str = "session_active_turn"
