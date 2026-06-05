from __future__ import annotations

from app.services.agent_grounding.contracts import GroundingBook, GroundingIntent, GroundingResult, GroundingRoute

STATUS_LABELS = {
    "draft": "đã tải lên và chưa tạo kế hoạch học",
    "processing": "đang được xử lý",
    "partial_ready": "đã có thể nghe một phần",
    "ready": "đã xử lý xong",
    "error": "đang gặp lỗi xử lý",
}


def render_metadata_answer(book: GroundingBook, intent: GroundingIntent) -> str:
    if intent == GroundingIntent.BOOK_METADATA_AUTHOR:
        return f'Tác giả của "{book.title}" là {book.author}.' if book.author else f'Tôi chưa có thông tin tác giả của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_TITLE:
        return f'Tên sách là "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE:
        return f'"{book.title}" là tài liệu {book.document_type.upper()}.' if book.document_type else f'Tôi chưa có thông tin định dạng của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_SECTION_COUNT:
        return f'"{book.title}" có {book.total_sections} đề mục trong cấu trúc tài liệu.' if book.total_sections is not None else f'Tôi chưa có tổng số đề mục của "{book.title}".'
    if intent == GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT:
        return f'"{book.title}" có {book.root_section_count} phần chính.'
    if intent == GroundingIntent.BOOK_METADATA_STATUS:
        status = STATUS_LABELS.get((book.status or "").casefold())
        return f'"{book.title}" {status}.' if status else f'Tôi chưa xác định được trạng thái xử lý của "{book.title}".'
    raise ValueError(f"Unsupported metadata intent: {intent}")


def format_grounding_tool_result(result: GroundingResult) -> str:
    if result.decision.route == GroundingRoute.BOOK_METADATA:
        return f"BOOK_METADATA_FOUND:\n{result.deterministic_answer or ''}".strip()
    if result.decision.route == GroundingRoute.BOOK_SECTION:
        if result.section_context:
            suffix = "\nThe context was truncated; state that limitation." if result.section_context_truncated else ""
            return (
                "BOOK_SECTION_FOUND:\n"
                f"{result.section_context}\n"
                "Answer only from this section context. Do not use model memory or request web search."
                f"{suffix}"
            )
        return f"BOOK_SECTION_UNAVAILABLE:\n{result.deterministic_answer or 'Nội dung section chưa được trích xuất.'}"
    if result.decision.route == GroundingRoute.CLARIFICATION:
        return f"CLARIFICATION_REQUIRED:\n{result.decision.clarification or 'Bạn vui lòng nói rõ câu hỏi.'}"
    if result.decision.route == GroundingRoute.WEB_POLICY:
        return "EXTERNAL_INFO_REQUIRED: This question needs current or external information. Follow the existing web-search permission policy."
    return "BOOK_RAG_REQUIRED"

