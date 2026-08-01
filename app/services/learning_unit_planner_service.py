from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.core.config import settings
from app.core.constant import PlanMode
from app.models.db_models import BookSection
from app.services.pareto_planner_service import plan_pareto_learning_units
from app.services.token_budget_service import estimate_text_budget


@dataclass(frozen=True)
class PlannedLearningUnit:
    title: str
    unit_type: str
    source_section_ids: list[uuid.UUID]
    source_text: str
    source_text_char_count: int
    estimated_tokens: int
    estimated_audio_seconds: int
    planner_reason: str | None = None


def _children_by_parent(sections: list[BookSection]) -> dict[uuid.UUID | None, list[BookSection]]:
    children: dict[uuid.UUID | None, list[BookSection]] = {}
    for section in sorted(sections, key=lambda item: item.section_index):
        children.setdefault(section.parent_id, []).append(section)
    return children


def _subtree_sections(root: BookSection, children: dict[uuid.UUID | None, list[BookSection]]) -> list[BookSection]:
    result = [root]
    for child in children.get(root.id, []):
        result.extend(_subtree_sections(child, children))
    return result


def _sections_text(sections: list[BookSection]) -> str:
    parts = [section.text_content.strip() for section in sections if section.text_content and section.text_content.strip()]
    return "\n\n".join(parts).strip()


def _make_unit(title: str, unit_type: str, source_sections: list[BookSection], reason: str | None = None) -> PlannedLearningUnit | None:
    ordered = sorted(source_sections, key=lambda item: item.section_index)
    source_text = _sections_text(ordered)
    if not source_text:
        return None
    budget = estimate_text_budget(source_text)
    return PlannedLearningUnit(
        title=title.strip() or "Bài học",
        unit_type=unit_type,
        source_section_ids=[section.id for section in ordered],
        source_text=source_text,
        source_text_char_count=budget.char_count,
        estimated_tokens=budget.estimated_tokens,
        estimated_audio_seconds=budget.estimated_audio_seconds,
        planner_reason=reason,
    )


def _format_split_title(title: str, part_number: int, total_parts: int) -> str:
    base_title = title.strip() or "Bài học"
    if total_parts <= 1:
        return base_title
    return f"{base_title} - Phần {part_number}/{total_parts}"


def _split_large_group(
    title: str,
    source_sections: list[BookSection],
    unit_type: str,
    *,
    max_tokens: int | None = None,
) -> list[PlannedLearningUnit]:
    limit_tokens = max_tokens if max_tokens is not None else settings.FULL_UNIT_MAX_TOKENS
    chunks: list[list[BookSection]] = []
    current: list[BookSection] = []
    current_tokens = 0

    for section in sorted(source_sections, key=lambda item: item.section_index):
        section_text = section.text_content or ""
        section_tokens = estimate_text_budget(section_text).estimated_tokens if section_text.strip() else 0
        if current and current_tokens > 0 and current_tokens + section_tokens > limit_tokens:
            chunks.append(current)
            current = []
            current_tokens = 0
        current.append(section)
        current_tokens += section_tokens

    if current:
        chunks.append(current)

    units: list[PlannedLearningUnit] = []
    total_parts = len(chunks)
    for index, chunk in enumerate(chunks, start=1):
        split_title = _format_split_title(title, index, total_parts)
        reason = (
            "Tách từ nhóm lớn để không vượt giới hạn xử lý."
            if total_parts <= 1
            else f"Tách từ nhóm lớn thành phần {index}/{total_parts} để không vượt giới hạn xử lý."
        )
        unit = _make_unit(split_title, unit_type, chunk, reason)
        if unit:
            units.append(unit)

    return units


def _merge_tiny_units(units: list[PlannedLearningUnit]) -> list[PlannedLearningUnit]:
    merged: list[PlannedLearningUnit] = []
    buffer: list[PlannedLearningUnit] = []

    def flush() -> None:
        if not buffer:
            return
        if len(buffer) == 1:
            merged.append(buffer[0])
        else:
            title = " - ".join(unit.title for unit in buffer[:2])
            source_ids = [section_id for unit in buffer for section_id in unit.source_section_ids]
            source_text = "\n\n".join(unit.source_text for unit in buffer)
            budget = estimate_text_budget(source_text)
            merged.append(
                PlannedLearningUnit(
                    title=title,
                    unit_type="full_group",
                    source_section_ids=source_ids,
                    source_text=source_text,
                    source_text_char_count=budget.char_count,
                    estimated_tokens=budget.estimated_tokens,
                    estimated_audio_seconds=budget.estimated_audio_seconds,
                    planner_reason="Gộp các đề mục ngắn liền kề để tránh audio quá vụn.",
                )
            )
        buffer.clear()

    for unit in units:
        if unit.estimated_tokens < settings.MIN_UNIT_TOKENS:
            buffer.append(unit)
            if sum(item.estimated_tokens for item in buffer) >= settings.MIN_UNIT_TOKENS:
                flush()
            continue
        flush()
        merged.append(unit)
    flush()
    return merged


def _learning_roots(sections: list[BookSection]) -> list[BookSection]:
    children = _children_by_parent(sections)
    roots = children.get(None, [])
    if 1 <= len(roots) <= 60:
        return roots
    return []


def _plan_full_from_roots(roots: list[BookSection], children: dict[uuid.UUID | None, list[BookSection]]) -> list[PlannedLearningUnit]:
    units: list[PlannedLearningUnit] = []
    for root in roots:
        subtree = _subtree_sections(root, children)
        unit = _make_unit(root.title, "full_chapter", subtree, "Full mode giữ đầy đủ nội dung trong cụm mục gốc.")
        if not unit:
            continue
        if unit.estimated_tokens > settings.FULL_UNIT_MAX_TOKENS:
            units.extend(_split_large_group(root.title, subtree, "full_group", max_tokens=settings.FULL_UNIT_MAX_TOKENS))
        else:
            units.append(unit)
    return units


def _plan_full_from_flat_sections(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    units: list[PlannedLearningUnit] = []
    current: list[BookSection] = []
    current_tokens = 0
    for section in sorted(sections, key=lambda item: item.section_index):
        section_tokens = estimate_text_budget(section.text_content or "").estimated_tokens
        if current and current_tokens + section_tokens > settings.FULL_UNIT_TARGET_TOKENS:
            unit = _make_unit(current[0].title, "full_group", current, "Gộp outline phẳng thành bài nghe theo kích thước hợp lý.")
            if unit:
                units.append(unit)
            current = []
            current_tokens = 0
        current.append(section)
        current_tokens += section_tokens
    if current:
        unit = _make_unit(current[0].title, "full_group", current, "Gộp outline phẳng thành bài nghe theo kích thước hợp lý.")
        if unit:
            units.append(unit)
    return units


def plan_full_learning_units(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    if not sections:
        return []

    children = _children_by_parent(sections)
    roots = _learning_roots(sections)
    units = _plan_full_from_roots(roots, children) if roots else _plan_full_from_flat_sections(sections)

    return _merge_tiny_units(units)


async def plan_learning_units_async(sections: list[BookSection], mode: PlanMode | str) -> list[PlannedLearningUnit]:
    mode_value = PlanMode(mode)
    if mode_value == PlanMode.FULL:
        return plan_full_learning_units(sections)

    return await plan_pareto_learning_units(sections)
