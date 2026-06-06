from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.services.agent_observability import AgentAnswerSource, AgentInputMode


class AgentPolicyAction(str, Enum):
    DIRECT_ANSWER = "direct_answer"
    ANSWER_WITH_SECTION_CONTEXT = "answer_with_section_context"
    ANSWER_WITH_RAG_CONTEXT = "answer_with_rag_context"
    ASK_CLARIFICATION = "ask_clarification"
    ASK_WEB_PERMISSION = "ask_web_permission"
    WEB_DISABLED = "web_disabled"
    ERROR = "error"


@dataclass(frozen=True)
class AgentPolicyRequest:
    query: str
    input_mode: AgentInputMode
    document_ids: list[str]
    allow_web_permission: bool


@dataclass(frozen=True)
class AgentPolicyResult:
    action: AgentPolicyAction
    answer_source: AgentAnswerSource
    reason_code: str
    message_key: str | None = None
    message_params: dict[str, str] = field(default_factory=dict)
    user_message: str | None = None
    tool_marker: str | None = None
    llm_system_context: str | None = None
    resolved_book_ids: tuple[str, ...] = field(default_factory=tuple)
    resolved_section_ids: tuple[str, ...] = field(default_factory=tuple)
    retrieval_chunk_ids: tuple[str, ...] = field(default_factory=tuple)
    retrieval_result_count: int = 0
