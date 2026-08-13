from __future__ import annotations

from dataclasses import dataclass

from app.services.agent_grounding.contracts import GroundingBook, GroundingIntent, GroundingScope

CONTEXT_OVERVIEW_INTENTS = frozenset(
    {
        GroundingIntent.CONTEXT_DOCUMENT_COUNT,
        GroundingIntent.CONTEXT_DOCUMENT_LIST,
        GroundingIntent.CONTEXT_OVERVIEW,
    }
)

_STATUS_LABELS = {
    "draft": "đã tải lên và chưa tạo kế hoạch học",
    "processing": "đang được xử lý",
    "partial_ready": "đã có thể nghe một phần",
    "ready": "đã xử lý xong",
    "error": "đang gặp lỗi xử lý",
}


@dataclass(frozen=True)
class ContextOverview:
    books: tuple[GroundingBook, ...]
    max_visible_documents: int

    @property
    def document_count(self) -> int:
        return len(self.books)

    @property
    def visible_books(self) -> tuple[GroundingBook, ...]:
        return self.books[: self.max_visible_documents]

    @property
    def hidden_document_count(self) -> int:
        return max(self.document_count - len(self.visible_books), 0)


def build_context_overview(scope: GroundingScope, *, max_visible_documents: int) -> ContextOverview:
    return ContextOverview(
        books=scope.books,
        max_visible_documents=max(1, max_visible_documents),
    )


def render_context_overview_answer(overview: ContextOverview, intent: GroundingIntent) -> str:
    if intent not in CONTEXT_OVERVIEW_INTENTS:
        raise ValueError(f"Unsupported context overview intent: {intent}")

    if not overview.books:
        return "Ngữ cảnh học tập hiện tại chưa có tài liệu nào."

    if intent == GroundingIntent.CONTEXT_DOCUMENT_COUNT:
        return _render_document_list(overview)

    if intent == GroundingIntent.CONTEXT_DOCUMENT_LIST:
        return _render_document_list(overview)

    return _render_context_overview(overview)


def _render_document_list(overview: ContextOverview) -> str:
    documents = "; ".join(_render_list_item(book) for book in overview.visible_books)
    suffix = _hidden_documents_suffix(overview.hidden_document_count)
    return f"Ngữ cảnh học tập hiện tại có {overview.document_count} tài liệu: {documents}.{suffix}"


def _render_context_overview(overview: ContextOverview) -> str:
    documents = "; ".join(_render_overview_item(book) for book in overview.visible_books)
    suffix = _hidden_documents_suffix(overview.hidden_document_count)
    return f"Ngữ cảnh học tập hiện tại gồm {overview.document_count} tài liệu: {documents}.{suffix}"


def _render_list_item(book: GroundingBook) -> str:
    if book.author:
        return f'"{book.title}" — {book.author}'
    return f'"{book.title}"'


def _render_overview_item(book: GroundingBook) -> str:
    details: list[str] = []
    if book.author:
        details.append(f"tác giả {book.author}")
    if book.document_type:
        details.append(f"loại {book.document_type.upper()}")
    status = _STATUS_LABELS.get((book.status or "").casefold())
    if status:
        details.append(status)
    details.append(f"{book.root_section_count} phần chính")
    return f'"{book.title}" ({", ".join(details)})'


def _hidden_documents_suffix(hidden_document_count: int) -> str:
    if hidden_document_count == 0:
        return ""
    return f" Còn {hidden_document_count} tài liệu khác."
