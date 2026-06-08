from __future__ import annotations

from app.services.agent_grounding.contracts import GroundingIntent, NormalizedQuery, SectionReference
from app.services.agent_grounding.query_normalizer import contains_any_phrase

AUTHOR_MARKERS = ("tác giả", "người viết", "ai viết", "author", "who wrote", "written by")
AUTHOR_CONTENT_ACTIONS = ("giải thích", "trình bày", "cho rằng", "nói gì", "quan điểm", "explain", "argue", "describe")
TITLE_MARKERS = (
    "tên sách",
    "tựa sách",
    "tên của quyển sách",
    "book title",
    "title of the book",
    "sách gì",
    "sách nào",
    "quyển sách gì",
    "quyển sách nào",
    "đang học quyển nào",
    "đang học sách nào",
    "đang học sách gì",
    "đang đọc sách nào",
    "đang đọc quyển nào",
)
DOCUMENT_TYPE_MARKERS = ("loại tài liệu", "định dạng tài liệu", "file gì", "document type", "file format")
ROOT_SECTION_COUNT_MARKERS = (
    "bao nhiêu phần chính",
    "bao nhiêu chương chính",
    "bao nhiêu chương",
    "how many main sections",
    "how many chapters",
)
SECTION_COUNT_MARKERS = ("bao nhiêu đề mục", "bao nhiêu mục", "tổng số đề mục", "how many sections", "section count")
STATUS_MARKERS = ("trạng thái sách", "sách xử lý xong chưa", "book status", "processing status")
SUMMARY_MARKERS = (
    "tóm tắt",
    "đại ý",
    "ý chính",
    "ý chương",
    "tổng quan",
    "xảy ra chuyện gì",
    "summarize",
    "summary",
    "main idea",
    "central idea",
    "what happens",
    "overview",
)
SECTION_CONTENT_MARKERS = ("nội dung", "giải thích", "trình bày", "explain", "what is in", "content")
CURRENT_MARKERS = ("hôm nay", "hiện tại", "mới nhất", "gần đây", "today", "current", "latest", "recent")
EXTERNAL_MARKERS = (
    "bitcoin",
    "tiền điện tử",
    "giá",
    "thời tiết",
    "tin tức",
    "internet",
    "web",
    "stock",
    "crypto",
    "weather",
    "news",
    "price",
)
BOOK_MARKERS = ("sách", "quyển sách", "chương", "mục", "đề mục", "book", "chapter", "section")


def detect_metadata_intent(query: NormalizedQuery) -> GroundingIntent | None:
    if contains_any_phrase(query, AUTHOR_MARKERS):
        if not contains_any_phrase(query, AUTHOR_CONTENT_ACTIONS) or contains_any_phrase(query, ("ai viết", "who wrote", "written by")):
            return GroundingIntent.BOOK_METADATA_AUTHOR
    if contains_any_phrase(query, TITLE_MARKERS):
        return GroundingIntent.BOOK_METADATA_TITLE
    if contains_any_phrase(query, DOCUMENT_TYPE_MARKERS):
        return GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE
    if contains_any_phrase(query, ROOT_SECTION_COUNT_MARKERS):
        return GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT
    if contains_any_phrase(query, SECTION_COUNT_MARKERS):
        return GroundingIntent.BOOK_METADATA_SECTION_COUNT
    if contains_any_phrase(query, STATUS_MARKERS):
        return GroundingIntent.BOOK_METADATA_STATUS
    return None


def detect_section_intent(query: NormalizedQuery, reference: SectionReference) -> GroundingIntent | None:
    summary_requested = contains_any_phrase(query, SUMMARY_MARKERS)
    content_requested = contains_any_phrase(query, SECTION_CONTENT_MARKERS)
    if reference.has_target:
        return GroundingIntent.BOOK_SECTION_SUMMARY if summary_requested else GroundingIntent.BOOK_SECTION_CONTENT
    if reference.marker_present and (summary_requested or content_requested or len(query.tokens) <= 5):
        return GroundingIntent.CLARIFICATION_REQUIRED
    return None


def detect_external_current_info(query: NormalizedQuery) -> bool:
    return (
        contains_any_phrase(query, CURRENT_MARKERS)
        and contains_any_phrase(query, EXTERNAL_MARKERS)
        and not contains_any_phrase(query, BOOK_MARKERS)
    )
