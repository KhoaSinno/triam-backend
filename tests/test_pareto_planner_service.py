import uuid

import pytest

from app.models.db_models import BookSection
from app.services import pareto_planner_service
from app.services.pareto_planner_service import (
    ParetoPlannedUnitPayload,
    ParetoPlannerPayload,
    build_section_cards,
    plan_pareto_learning_units,
)


def _section(
    *,
    book_id: uuid.UUID,
    section_index: int,
    title: str,
    path: str,
    level: int,
    text: str = "",
    parent_id: uuid.UUID | None = None,
) -> BookSection:
    return BookSection(
        id=uuid.uuid4(),
        book_id=book_id,
        parent_id=parent_id,
        section_index=section_index,
        title=title,
        level=level,
        path=path,
        text_content=text,
        text_char_count=len(text),
    )


def test_section_cards_do_not_include_full_source_text(monkeypatch):
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_SECTION_EXCERPT_CHARS", 120)
    book_id = uuid.uuid4()
    long_text = "đây là nội dung rất dài " * 80
    section = _section(
        book_id=book_id,
        section_index=1,
        title="Khái niệm nền tảng",
        path="1.1",
        level=2,
        text=long_text,
    )

    cards = build_section_cards([section])

    assert len(cards) == 1
    assert cards[0].excerpt
    assert cards[0].excerpt != long_text
    assert len(cards[0].excerpt) <= 120
    assert "core_concept" in cards[0].keyword_hints


@pytest.mark.asyncio
async def test_llm_structured_output_becomes_pareto_learning_units(monkeypatch):
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_LLM_ENABLED", True)
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_MIN_UNITS", 1)
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_MAX_UNITS", 4)

    book_id = uuid.uuid4()
    root = _section(book_id=book_id, section_index=0, title="Chương 1 Logic", path="1", level=1)
    concept = _section(book_id=book_id, section_index=1, title="Khái niệm mệnh đề", path="1.1", level=2, text="khái niệm " * 200, parent_id=root.id)
    rule = _section(book_id=book_id, section_index=2, title="Quy tắc suy luận", path="1.2", level=2, text="quy tắc " * 200, parent_id=root.id)
    note = _section(book_id=book_id, section_index=3, title="Ghi chú phụ", path="1.3", level=2, text="ghi chú " * 200, parent_id=root.id)

    async def fake_call(cards):
        return ParetoPlannerPayload(
            units=[
                ParetoPlannedUnitPayload(
                    title="Nền tảng logic mệnh đề",
                    source_section_ids=[str(rule.id), str(concept.id)],
                    unit_type="pareto_core",
                    importance_score=5,
                    learning_objective="Nắm khái niệm và quy tắc nền tảng.",
                    planner_reason="Hai mục này là nền tảng để hiểu các phần sau.",
                )
            ]
        )

    monkeypatch.setattr(pareto_planner_service, "_call_pareto_llm", fake_call)

    units = await plan_pareto_learning_units([root, concept, rule, note])

    assert len(units) == 1
    assert units[0].title == "Nền tảng logic mệnh đề"
    assert units[0].unit_type == "pareto_core"
    assert units[0].source_section_ids == [concept.id, rule.id]
    assert "Mục tiêu học" in (units[0].planner_reason or "")


@pytest.mark.asyncio
async def test_invalid_llm_section_ids_fallback_to_deterministic_planner(monkeypatch):
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_LLM_ENABLED", True)
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_MAX_UNITS", 3)

    book_id = uuid.uuid4()
    concept = _section(book_id=book_id, section_index=1, title="Khái niệm quan trọng", path="1.1", level=1, text="khái niệm " * 200)
    method = _section(book_id=book_id, section_index=2, title="Phương pháp chính", path="1.2", level=1, text="phương pháp " * 200)

    async def fake_call(cards):
        return ParetoPlannerPayload(
            units=[
                ParetoPlannedUnitPayload(
                    title="Unit lỗi",
                    source_section_ids=[str(uuid.uuid4())],
                    unit_type="pareto_core",
                    importance_score=5,
                    learning_objective="Mục tiêu học giả lập.",
                    planner_reason="Id không thuộc tài liệu.",
                )
            ]
        )

    monkeypatch.setattr(pareto_planner_service, "_call_pareto_llm", fake_call)

    units = await plan_pareto_learning_units([concept, method])

    assert units
    assert {section_id for unit in units for section_id in unit.source_section_ids}.issubset({concept.id, method.id})


def test_deterministic_fallback_prefers_core_concept_over_long_minor_note(monkeypatch):
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_PLANNER_MAX_UNITS", 1)
    monkeypatch.setattr(pareto_planner_service.settings, "PARETO_TARGET_COVERAGE_RATIO", 0.9)

    from app.services.learning_unit_planner_service import fallback_pareto_learning_units

    book_id = uuid.uuid4()
    long_note = _section(book_id=book_id, section_index=1, title="Ghi chú mở rộng", path="1.1", level=1, text="ghi chú phụ " * 3000)
    core = _section(book_id=book_id, section_index=2, title="Khái niệm nền tảng", path="1.2", level=1, text="khái niệm " * 100)

    units = fallback_pareto_learning_units([long_note, core])

    assert len(units) == 1
    assert units[0].source_section_ids == [core.id]
