from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from app.core.exceptions import DocumentExtractionError
from app.services.document_structure_types import ParsedDocument, ParsedSection, flatten_sections, section_subtree_text


@dataclass(frozen=True)
class StructureStats:
    total_sections: int
    max_depth: int
    sections_with_text: int


def document_structure_stats(parsed: ParsedDocument) -> StructureStats:
    flattened = flatten_sections(parsed.sections)
    return StructureStats(
        total_sections=len(flattened),
        max_depth=parsed.max_depth,
        sections_with_text=sum(1 for section in flattened if section_subtree_text(section)),
    )


def validate_document_structure(parsed: ParsedDocument) -> None:
    stats = document_structure_stats(parsed)

    if stats.total_sections == 0:
        raise DocumentExtractionError("Tài liệu không có cấu trúc mục lục hợp lệ.")

    if stats.max_depth > 6:
        raise DocumentExtractionError("Cấu trúc mục lục quá sâu, hiện chưa hỗ trợ tài liệu này.")

    if stats.total_sections > 300:
        raise DocumentExtractionError("Tài liệu có quá nhiều đề mục, hiện chưa hỗ trợ xử lý tự động.")

    if stats.sections_with_text == 0:
        raise DocumentExtractionError("Tài liệu có mục lục nhưng không trích xuất được nội dung text.")


def detect_structure_warnings(parsed: ParsedDocument) -> list[str]:
    flattened = flatten_sections(parsed.sections)
    warnings: list[str] = []

    if not flattened:
        return warnings

    levels = Counter(section.level for section in flattened)
    if len(levels) == 1 and len(flattened) >= 20:
        warnings.append("Tài liệu có outline phẳng với nhiều đề mục. TRIAM sẽ tự gom các đề mục liên quan thành bài nghe.")

    short_sections = sum(1 for section in flattened if 0 < len(section_subtree_text(section)) < 500)
    if short_sections / max(1, len(flattened)) >= 0.5:
        warnings.append("Nhiều đề mục khá ngắn. Hệ thống sẽ gộp các mục nhỏ để tránh tạo audio quá vụn.")

    return warnings


def build_outline_preview(parsed: ParsedDocument, *, max_nodes: int = 120) -> list[dict[str, Any]]:
    remaining = max_nodes

    def walk(sections: list[ParsedSection]) -> list[dict[str, Any]]:
        nonlocal remaining
        result: list[dict[str, Any]] = []
        for section in sections:
            if remaining <= 0:
                break
            remaining -= 1
            children = walk(section.children)
            result.append(
                {
                    "title": section.title,
                    "level": section.level,
                    "path": section.path,
                    "page_start": section.page_start,
                    "page_end": section.page_end,
                    "text_char_count": len(section_subtree_text(section)),
                    "children": children,
                }
            )
        return result

    return walk(parsed.sections)
