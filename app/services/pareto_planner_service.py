from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import BookSection
from app.services.async_limiter import get_loop_semaphore
from app.services.learning_unit_planner_service import PlannedLearningUnit, fallback_pareto_learning_units
from app.services.pareto_signal_service import extract_pareto_signal_hints, guess_section_language
from app.services.token_budget_service import estimate_text_budget

client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0
)

PARETO_PLANNER_SYSTEM_PROMPT = """
You are TRIAM's Pareto learning planner.
Your job is not to summarize the book.
Your job is to select and group the vital few source sections that give the learner the highest understanding value.

Rules:
- Return only valid JSON matching the requested schema.
- Section titles may be Vietnamese, English, or mixed-language.
- Use the original document language when naming learning units unless the source title is unclear.
- Treat signal_hints as helpful hints, not strict rules.
- Prefer structurally important sections even when there are no obvious keywords.
- Select 3 to 8 learning units unless the document is very small.
- Prefer foundational definitions, principles, formulas, methods, procedures, and representative examples.
- Merge small related sections into one coherent learning unit.
- Preserve the source order inside each unit.
- Do not invent section ids.
- Do not create audio script content.
- Do not include sections that are only decorative, repetitive, or minor examples unless they are necessary to understand a core idea.
- Each unit must explain why it was selected.
""".strip()


@dataclass(frozen=True)
class SectionCard:
    section_id: uuid.UUID
    title: str
    path: str
    level: int
    parent_path: str | None
    section_index: int
    text_char_count: int
    estimated_tokens: int
    child_count: int
    language: str
    signal_hints: list[str]
    excerpt: str

    def to_prompt_dict(self) -> dict:
        return {
            "id": str(self.section_id),
            "title": self.title,
            "path": self.path,
            "level": self.level,
            "parent_path": self.parent_path,
            "estimated_tokens": self.estimated_tokens,
            "child_count": self.child_count,
            "language": self.language,
            "signal_hints": self.signal_hints,
            "excerpt": self.excerpt,
        }


class ParetoPlannedUnitPayload(BaseModel):
    title: str = Field(min_length=3)
    source_section_ids: list[str] = Field(min_length=1)
    unit_type: str = Field(min_length=3)
    importance_score: int = Field(ge=1, le=5)
    learning_objective: str = Field(min_length=10)
    planner_reason: str = Field(min_length=10)

    @field_validator("source_section_ids")
    @classmethod
    def validate_source_section_ids(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for item in value:
            try:
                cleaned.append(str(uuid.UUID(str(item))))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid section id: {item}") from exc
        return cleaned


class ParetoPlannerPayload(BaseModel):
    units: list[ParetoPlannedUnitPayload] = Field(min_length=1)


def _children_by_parent(sections: list[BookSection]) -> dict[uuid.UUID | None, list[BookSection]]:
    children: dict[uuid.UUID | None, list[BookSection]] = {}
    for section in sorted(sections, key=lambda item: item.section_index):
        children.setdefault(section.parent_id, []).append(section)
    return children


def _excerpt(text: str | None) -> str:
    normalized = " ".join((text or "").split())
    limit = max(100, settings.PARETO_SECTION_EXCERPT_CHARS)
    return normalized[:limit]


def build_section_cards(sections: list[BookSection]) -> list[SectionCard]:
    by_id = {section.id: section for section in sections}
    children = _children_by_parent(sections)
    cards: list[SectionCard] = []

    for section in sorted(sections, key=lambda item: item.section_index):
        text = section.text_content or ""
        excerpt = _excerpt(text)
        budget = estimate_text_budget(text)
        parent = by_id.get(section.parent_id) if section.parent_id else None
        cards.append(
            SectionCard(
                section_id=section.id,
                title=section.title,
                path=section.path,
                level=section.level,
                parent_path=parent.path if parent else None,
                section_index=section.section_index,
                text_char_count=section.text_char_count,
                estimated_tokens=budget.estimated_tokens,
                child_count=len(children.get(section.id, [])),
                language=guess_section_language(section.title, excerpt),
                signal_hints=extract_pareto_signal_hints(section.title, excerpt),
                excerpt=excerpt,
            )
        )

    return cards[: max(1, settings.PARETO_PLANNER_MAX_SECTION_CARDS)]


def _prompt_user_content(cards: list[SectionCard]) -> str:
    total_tokens = sum(card.estimated_tokens for card in cards)
    payload = {
        "mode": "pareto",
        "target_coverage_ratio": settings.PARETO_TARGET_COVERAGE_RATIO,
        "target_tokens": int(total_tokens * settings.PARETO_TARGET_COVERAGE_RATIO),
        "min_units": settings.PARETO_PLANNER_MIN_UNITS,
        "max_units": settings.PARETO_PLANNER_MAX_UNITS,
        "section_cards": [card.to_prompt_dict() for card in cards],
    }
    return json.dumps(payload, ensure_ascii=False)


def _coerce_planner_response(parsed_payload: ParetoPlannerPayload | None, content: str | None) -> ParetoPlannerPayload:
    if parsed_payload is not None:
        return parsed_payload
    if not content:
        raise ValueError("Empty Pareto planner response")
    return ParetoPlannerPayload.model_validate(json.loads(content))


async def _call_pareto_llm(cards: list[SectionCard]) -> ParetoPlannerPayload:
    async with get_loop_semaphore("pareto_planner", 1):
        response = await client.beta.chat.completions.parse(
            model=settings.PARETO_PLANNER_MODEL,
            messages=[
                {"role": "system", "content": PARETO_PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": _prompt_user_content(cards)},
            ],
            temperature=0.1,
            response_format=ParetoPlannerPayload,
        )
    message = response.choices[0].message
    return _coerce_planner_response(message.parsed, message.content)


def _sections_by_id(sections: list[BookSection]) -> dict[uuid.UUID, BookSection]:
    return {section.id: section for section in sections}


def _make_planned_unit_from_payload(
    payload: ParetoPlannedUnitPayload,
    *,
    sections_by_id: dict[uuid.UUID, BookSection],
) -> PlannedLearningUnit | None:
    source_sections: list[BookSection] = []
    seen: set[uuid.UUID] = set()
    for raw_id in payload.source_section_ids:
        section_id = uuid.UUID(raw_id)
        if section_id in seen:
            continue
        section = sections_by_id.get(section_id)
        if not section:
            continue
        source_sections.append(section)
        seen.add(section_id)

    source_sections.sort(key=lambda item: item.section_index)
    source_text_parts = [section.text_content.strip() for section in source_sections if section.text_content and section.text_content.strip()]
    source_text = "\n\n".join(source_text_parts).strip()
    if not source_text:
        return None

    budget = estimate_text_budget(source_text)
    reason = (
        f"{payload.planner_reason.strip()} "
        f"Mục tiêu học: {payload.learning_objective.strip()} "
        f"Điểm quan trọng: {payload.importance_score}/5."
    )
    return PlannedLearningUnit(
        title=payload.title.strip(),
        unit_type=payload.unit_type.strip() or "pareto_core",
        source_section_ids=[section.id for section in source_sections],
        source_text=source_text,
        source_text_char_count=budget.char_count,
        estimated_tokens=budget.estimated_tokens,
        estimated_audio_seconds=budget.estimated_audio_seconds,
        planner_reason=reason,
    )


def _trim_to_target(units: list[PlannedLearningUnit], *, total_source_tokens: int) -> list[PlannedLearningUnit]:
    if len(units) <= settings.PARETO_PLANNER_MIN_UNITS:
        return units

    target_tokens = max(1, int(total_source_tokens * settings.PARETO_TARGET_COVERAGE_RATIO))
    selected: list[PlannedLearningUnit] = []
    selected_tokens = 0

    for unit in units[: settings.PARETO_PLANNER_MAX_UNITS]:
        selected.append(unit)
        selected_tokens += unit.estimated_tokens
        if len(selected) >= settings.PARETO_PLANNER_MIN_UNITS and selected_tokens >= target_tokens:
            break

    return selected


def _validate_planner_payload(payload: ParetoPlannerPayload, sections: list[BookSection]) -> list[PlannedLearningUnit]:
    sections_by_id = _sections_by_id(sections)
    total_source_tokens = sum(estimate_text_budget(section.text_content or "").estimated_tokens for section in sections)
    units: list[PlannedLearningUnit] = []
    for unit_payload in payload.units:
        unit = _make_planned_unit_from_payload(unit_payload, sections_by_id=sections_by_id)
        if unit:
            units.append(unit)

    units.sort(key=lambda unit: min(sections_by_id[section_id].section_index for section_id in unit.source_section_ids))
    return _trim_to_target(units, total_source_tokens=total_source_tokens)


def _should_use_llm_planner(cards: list[SectionCard]) -> tuple[bool, str | None]:
    min_cards = max(1, settings.PARETO_PLANNER_LLM_MIN_CARDS)
    if len(cards) < min_cards:
        return False, "small_outline"
    return True, None


async def plan_pareto_learning_units(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    if not sections:
        return []

    fallback_units = fallback_pareto_learning_units(sections)
    if not settings.PARETO_PLANNER_LLM_ENABLED:
        log.info(f"Pareto planner fallback used | reason=disabled | units={len(fallback_units)}")
        return fallback_units

    cards = build_section_cards(sections)
    should_use_llm, deterministic_reason = _should_use_llm_planner(cards)
    if not should_use_llm:
        log.info(
            "Pareto planner deterministic used | "
            f"reason={deterministic_reason} | sections={len(sections)} | cards={len(cards)} | units={len(fallback_units)}"
        )
        return fallback_units

    try:
        log.info(f"Pareto planner start | sections={len(sections)} | cards={len(cards)} | model={settings.PARETO_PLANNER_MODEL}")
        payload = await asyncio.wait_for(_call_pareto_llm(cards), timeout=settings.PARETO_PLANNER_TIMEOUT_SECONDS)
        planned_units = _validate_planner_payload(payload, sections)
        if not planned_units:
            raise ValueError("Pareto planner returned no valid learning units")
        log.info(f"Pareto planner result | source=llm | units={len(planned_units)}")
        return planned_units
    except (asyncio.TimeoutError, ValidationError, ValueError, json.JSONDecodeError) as exc:
        log.warning(f"Pareto planner fallback used | reason={type(exc).__name__} | units={len(fallback_units)}")
        return fallback_units
    except Exception as exc:
        log.warning(f"Pareto planner fallback used | reason=unexpected:{type(exc).__name__} | units={len(fallback_units)}")
        return fallback_units
