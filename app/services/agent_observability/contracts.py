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
    grounding_route: str | None = None
    grounding_reason_code: str | None = None
    resolved_book_ids: list[str] = field(default_factory=list)
    resolved_section_ids: list[str] = field(default_factory=list)
    retrieval_method: str | None = None
    retrieval_result_count: int = 0
    retrieval_chunk_ids: list[str] = field(default_factory=list)
    retrieval_learning_unit_ids: list[str] = field(default_factory=list)
    retrieval_section_ids: list[str] = field(default_factory=list)
    retrieval_scores: list[float] = field(default_factory=list)
    rag_candidate_count: int = 0
    rag_context_selected_count: int = 0
    rag_context_char_count: int = 0
    rag_context_budget_mode: str | None = None
    asr_final_status_at_book_tool: str | None = None
    asr_final_before_book_tool_ms: int | None = None
    book_tool_before_asr_final_ms: int | None = None
    transcript_final_monotonic: float | None = field(default=None, repr=False)
    book_tool_started_monotonic: float | None = field(default=None, repr=False)
    tool_names: list[str] = field(default_factory=list)
    query_guard_reason_code: str | None = None
    query_guard_mode: str | None = None
    query_guard_overlap_ratio: float | None = None
    query_guard_important_overlap_ratio: float | None = None
    answer_source: AgentAnswerSource = AgentAnswerSource.UNKNOWN
    assistant_char_count: int = 0
    stage_latency_ms: dict[str, int] = field(default_factory=dict)
    error_code: str | None = None
    tool_reply_watchdog_scheduled: bool | None = None
    tool_reply_watchdog_fired: bool | None = None
    tool_reply_watchdog_tool_names: list[str] = field(default_factory=list)
    tool_reply_watchdog_reason: str | None = None
    tool_result_to_speech_ms: int | None = None
    forced_reply_reason: str | None = None
    correlation_quality: str = "session_active_turn"
