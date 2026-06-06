from __future__ import annotations

from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyResult

SECTION_TEXT_ANSWER_INSTRUCTIONS = """
Answer the user's question in Vietnamese using only SECTION_CONTEXT below.
Do not use model memory, other chapters, or web search.
For a summary or "what happens" question, cover the major events or ideas across
the beginning, middle, and ending of the entire available section context.
Do not stop after describing only the opening excerpt.
Keep the answer factual and concise, normally 3-5 sentences.
If the context says it was truncated, state that the answer is based on the available excerpt.

SECTION_CONTEXT:
{section_context}
""".strip()

RAG_TEXT_ANSWER_INSTRUCTIONS = """
Answer the user's question in Vietnamese using only BOOK_CONTEXT below.
Do not use model memory, other chapters, or web search.
Keep the answer factual and concise, normally 2-4 sentences.
If the context is weak or incomplete, say that the book context is not enough.

BOOK_CONTEXT:
{book_context}
""".strip()

MESSAGE_TEMPLATES = {
    "ask_clarification": "{clarification}",
    "book_context_error": "Không thể tìm kiếm dữ liệu trong sách lúc này.",
    "book_context_not_found": "Mình chưa tìm thấy thông tin phù hợp trong sách cho câu hỏi này.",
    "section_unavailable": "{message}",
    "web_disabled": "Câu hỏi này cần thông tin ngoài sách, nhưng tìm kiếm internet hiện đang tắt.",
}


def build_section_text_context(section_context: str) -> str:
    return SECTION_TEXT_ANSWER_INSTRUCTIONS.format(section_context=section_context)


def build_rag_text_context(book_context: str) -> str:
    return RAG_TEXT_ANSWER_INSTRUCTIONS.format(book_context=book_context)


def render_text_direct_message(result: AgentPolicyResult) -> str:
    if result.user_message:
        return result.user_message
    if result.message_key:
        template = MESSAGE_TEMPLATES.get(result.message_key)
        if template:
            return template.format(**result.message_params)
    return "Mình chưa có đủ thông tin để trả lời chắc chắn."


def render_voice_tool_result(result: AgentPolicyResult) -> str:
    if result.tool_marker:
        return result.tool_marker

    message = render_text_direct_message(result)
    if result.action == AgentPolicyAction.DIRECT_ANSWER:
        return f"BOOK_METADATA_FOUND:\n{message}"
    if result.action == AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT and result.llm_system_context:
        return (
            "BOOK_SECTION_FOUND:\n"
            f"{result.llm_system_context}\n"
            "Answer only from this section context. Do not use model memory or request web search."
        )
    if result.action == AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT and result.llm_system_context:
        return f"BOOK_CONTEXT_FOUND:\n{result.llm_system_context}"
    if result.action == AgentPolicyAction.ASK_CLARIFICATION:
        return f"CLARIFICATION_REQUIRED:\n{message}"
    if result.action == AgentPolicyAction.ASK_WEB_PERMISSION:
        return f"BOOK_CONTEXT_NOT_FOUND: {message}"
    if result.action == AgentPolicyAction.WEB_DISABLED:
        return f"BOOK_CONTEXT_NOT_FOUND: {message}"
    if result.action == AgentPolicyAction.ERROR:
        return f"BOOK_CONTEXT_ERROR: {message}"
    return message
