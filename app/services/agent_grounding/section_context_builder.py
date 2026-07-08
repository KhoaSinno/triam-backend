from __future__ import annotations

import re
import uuid

from app.services.agent_grounding.contracts import GroundingBook, GroundingScope, GroundingSection, GroundingSectionText, SectionContext
from app.services.agent_grounding.query_normalizer import normalize_text

WHITESPACE_PATTERN = re.compile(r"\s+")


def descendant_section_ids(scope: GroundingScope, root_id: uuid.UUID) -> tuple[uuid.UUID, ...]:
    children: dict[uuid.UUID | None, list[GroundingSection]] = {}
    by_id = {section.id: section for section in scope.sections}
    root = by_id.get(root_id)
    if root is None:
        return ()

    for section in sorted(scope.sections, key=lambda item: item.section_index):
        if section.book_id == root.book_id:
            children.setdefault(section.parent_id, []).append(section)

    result: list[uuid.UUID] = []

    def walk(section: GroundingSection) -> None:
        result.append(section.id)
        for child in children.get(section.id, []):
            walk(child)

    walk(root)
    return tuple(result)


def _dedupe_rows(rows: tuple[GroundingSectionText, ...]) -> tuple[GroundingSectionText, ...]:
    seen: set[str] = set()
    result: list[GroundingSectionText] = []
    for row in sorted(rows, key=lambda item: item.section_index):
        text = WHITESPACE_PATTERN.sub(" ", normalize_text(row.text_content or ""))
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(row)
    return tuple(result)


def build_section_context(
    book: GroundingBook,
    target: GroundingSection,
    rows: tuple[GroundingSectionText, ...],
    *,
    max_chars: int,
) -> SectionContext:
    max_chars = max(8000, max_chars)
    header = f'BOOK_SECTION_CONTEXT\nBook: "{book.title}"\nTarget section: {target.path} - {target.title}\n\n'
    unique_rows = _dedupe_rows(rows)
    if not unique_rows:
        message = f'{header}The section exists, but no source text was extracted for "{target.title}".'
        return SectionContext(message[:max_chars], tuple(row.id for row in rows), False, len(message) > max_chars)

    parts = [header]
    remaining = max_chars - len(header)
    truncated = False
    for index, row in enumerate(unique_rows):
        if remaining <= 0:
            truncated = True
            break
        section_header = f"[{row.path} {row.title}]\n"
        remaining_rows = len(unique_rows) - index
        fair_share = max(200, remaining // max(remaining_rows, 1))
        text = (row.text_content or "").strip()
        allowed_text_chars = max(0, min(len(text), fair_share - len(section_header) - 2, remaining - len(section_header) - 2))
        if allowed_text_chars <= 0:
            truncated = True
            continue
        content = text[:allowed_text_chars].rstrip()
        if len(content) < len(text):
            content = f"{content}\n...[truncated]"
            truncated = True
        block = f"{section_header}{content}\n\n"
        if len(block) > remaining:
            block = block[:remaining]
            truncated = True
        parts.append(block)
        remaining -= len(block)

    text = "".join(parts)[:max_chars]
    all_source_ids = tuple(row.id for row in sorted(rows, key=lambda item: item.section_index))
    return SectionContext(text, all_source_ids, True, truncated or len(text) >= max_chars)
