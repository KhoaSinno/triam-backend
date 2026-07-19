from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import BookSection, BookSectionKnowledge
from app.services.async_limiter import get_loop_semaphore
from app.services.learning_unit_planner_service import PlannedLearningUnit
from app.services.pareto_signal_service import (
    extract_pareto_signal_hints,
    get_or_create_anchor_embeddings,
)
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
- Select source sections such that the sum of their estimated_tokens is close to or under the requested target_tokens in the user payload.
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


def build_section_cards(sections: list[BookSection], anchor_vectors: dict[str, list[float]] | None = None) -> list[SectionCard]:
    by_id = {section.id: section for section in sections}
    children = _children_by_parent(sections)
    cards: list[SectionCard] = []

    # 1. Truy vấn một lần duy nhất tất cả embeddings có sẵn của cuốn sách trong database
    embeddings_map = {}
    if sections:
        book_id = sections[0].book_id
        with Session(engine) as session:
            rows = session.exec(
                select(BookSectionKnowledge.section_id, BookSectionKnowledge.embedding)
                .where(
                    BookSectionKnowledge.book_id == book_id,
                    BookSectionKnowledge.embedding_version == settings.BOOK_SECTION_EMBEDDING_VERSION
                )
            ).all()
            embeddings_map = {row[0]: row[1] for row in rows if row[1] is not None}

    # 2. Xây dựng danh sách SectionCard
    for section in sorted(sections, key=lambda item: item.section_index):
        text = section.text_content or ""
        excerpt = _excerpt(text)
        budget = estimate_text_budget(text)
        parent = by_id.get(section.parent_id) if section.parent_id else None
        
        # Tìm vector của section hiện tại
        embedding = embeddings_map.get(section.id)
        
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
                signal_hints=extract_pareto_signal_hints(
                    embedding=embedding, anchor_vectors=anchor_vectors
                ),
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
    # 1. Bảo toàn số lượng bài học tối thiểu (3 bài)
    if len(units) <= settings.PARETO_PLANNER_MIN_UNITS:
        return units

    # Tính toán các ngưỡng token mục tiêu
    target_tokens = int(total_source_tokens * settings.PARETO_TARGET_COVERAGE_RATIO)
    total_planned_tokens = sum(u.estimated_tokens for u in units)

    # 2. Nếu tổng token do LLM chọn nằm dưới ngưỡng cho phép (có sai số 15% để tránh cắt tỉa khi vượt nhẹ), giữ nguyên toàn bộ
    allowed_ceiling = int(target_tokens * 1.15)
    if total_planned_tokens <= allowed_ceiling:
        log.info(f"Keep all planned units | total_planned={total_planned_tokens} <= allowed_ceiling={allowed_ceiling} (target={target_tokens})")
        return units

    log.info(f"Start value-based trimming | total_planned={total_planned_tokens} > allowed_ceiling={allowed_ceiling} (target={target_tokens})")

    # 3. Tiến hành cắt tỉa dựa trên giá trị (Value-Based)
    # Lưu lại chỉ số gốc (index) đại diện cho thứ tự xuất hiện gốc trong sách
    indexed_units = [(i, unit) for i, unit in enumerate(units)]
    
    # Hàm trích xuất điểm quan trọng từ planner_reason (ví dụ: "Điểm quan trọng: X/5")
    def get_importance_score(unit: PlannedLearningUnit) -> int:
        try:
            if "Điểm quan trọng: " in unit.planner_reason:
                return int(unit.planner_reason.split("Điểm quan trọng: ")[1].split("/")[0])
        except Exception as exc:
            log.warning(f"Failed to parse importance score from planner_reason: {exc}")
        return 3  # Điểm mặc định trung bình nếu lỗi parse

    # Sắp xếp theo: 
    # Tiêu chí 1: Importance Score giảm dần (ưu tiên bài quan trọng nhất)
    # Tiêu chí 2: Chỉ số index gốc tăng dần (nếu cùng quan trọng, ưu tiên bài xuất hiện trước trong sách)
    indexed_units.sort(key=lambda item: (-get_importance_score(item[1]), item[0]))

    selected_indexed: list[tuple[int, PlannedLearningUnit]] = []
    selected_tokens = 0

    # Gom các bài học tốt nhất theo ngân sách
    for index, unit in indexed_units:
        # Nếu cộng thêm unit này mà vượt quá 40% ngân sách và chúng ta đã đạt số lượng tối thiểu (3 bài),
        # thì dừng lại để không vượt quá ngưỡng 40%.
        if len(selected_indexed) >= settings.PARETO_PLANNER_MIN_UNITS and (selected_tokens + unit.estimated_tokens) > target_tokens:
            break
            
        selected_indexed.append((index, unit))
        selected_tokens += unit.estimated_tokens

    # 4. Trả các bài học đã chọn về thứ tự đọc tự nhiên của sách (sắp xếp lại theo index gốc)
    selected_indexed.sort(key=lambda item: item[0])
    
    final_units = [unit for _, unit in selected_indexed]
    log.info(
        f"Trimming complete | retained_units={len(final_units)} "
        f"| retained_tokens={sum(u.estimated_tokens for u in final_units)}/{total_source_tokens}"
    )
    return final_units


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


async def plan_pareto_learning_units(sections: list[BookSection]) -> list[PlannedLearningUnit]:
    if not sections:
        return []

    # 1. Tải các Vector Neo bất đồng bộ từ OpenAI (Cache in-memory)
    anchor_vectors = await get_or_create_anchor_embeddings()

    # 2. Tạo section cards truyền kèm anchor_vectors
    cards = build_section_cards(sections, anchor_vectors)

    # 3. Gọi trực tiếp LLM để lập kế hoạch, nếu lỗi sẽ Fail-fast ném lỗi lên API
    log.info(f"Pareto planner start | sections={len(sections)} | cards={len(cards)}")
    
    payload = await asyncio.wait_for(
        _call_pareto_llm(cards), 
        timeout=settings.PARETO_PLANNER_TIMEOUT_SECONDS
    )
    
    planned_units = _validate_planner_payload(payload, sections)
    if not planned_units:
        raise ValueError("Pareto planner returned no valid learning units")
        
    log.info(f"Pareto planner result | source=llm | units={len(planned_units)}")
    return planned_units
