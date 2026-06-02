import uuid

from app.core.constant import PlanMode
from app.models.db_models import BookSection
from app.services import learning_unit_planner_service as planner_service
from app.services.learning_unit_planner_service import plan_learning_units


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


def test_full_planner_groups_children_under_top_level_root():
    book_id = uuid.uuid4()
    root = _section(book_id=book_id, section_index=0, title="LOGIC MỆNH ĐỀ", path="1", level=1)
    child_a = _section(book_id=book_id, section_index=1, title="Khái niệm", path="1.1", level=2, text="A " * 500, parent_id=root.id)
    child_b = _section(book_id=book_id, section_index=2, title="Phân loại", path="1.2", level=2, text="B " * 500, parent_id=root.id)

    units = plan_learning_units([root, child_a, child_b], PlanMode.FULL)

    assert len(units) == 1
    assert units[0].title == "LOGIC MỆNH ĐỀ"
    assert len(units[0].source_section_ids) == 3


def test_full_planner_names_large_split_units_uniquely(monkeypatch):
    monkeypatch.setattr(planner_service, "FULL_UNIT_MAX_TOKENS", 20)
    monkeypatch.setattr(planner_service, "MIN_UNIT_TOKENS", 1)

    book_id = uuid.uuid4()
    root = _section(book_id=book_id, section_index=0, title="PHÉP ĐẾM", path="1", level=1)
    child_a = _section(book_id=book_id, section_index=1, title="Quy tắc cộng", path="1.1", level=2, text="alpha " * 40, parent_id=root.id)
    child_b = _section(book_id=book_id, section_index=2, title="Quy tắc nhân", path="1.2", level=2, text="beta " * 40, parent_id=root.id)
    child_c = _section(book_id=book_id, section_index=3, title="Hoán vị", path="1.3", level=2, text="gamma " * 40, parent_id=root.id)

    units = plan_learning_units([root, child_a, child_b, child_c], PlanMode.FULL)
    titles = [unit.title for unit in units]

    assert len(units) > 1
    assert len(titles) == len(set(titles))
    assert all(title.startswith("PHÉP ĐẾM - Phần ") for title in titles)


def test_pareto_planner_selects_fewer_focus_units_than_full():
    book_id = uuid.uuid4()
    sections = []
    for index in range(10):
        sections.append(
            _section(
                book_id=book_id,
                section_index=index,
                title=f"Mục {index + 1}",
                path=str(index + 1),
                level=1,
                text=("nội dung quan trọng " if index in (2, 5) else "ghi chú ") * (1000 if index in (2, 5) else 100),
            )
        )

    full_units = plan_learning_units(sections, PlanMode.FULL)
    pareto_units = plan_learning_units(sections, PlanMode.PARETO)

    assert pareto_units
    assert len(pareto_units) <= len(full_units)
    assert sum(unit.source_text_char_count for unit in pareto_units) < sum(unit.source_text_char_count for unit in full_units)


def test_pareto_fallback_supports_english_core_signals(monkeypatch):
    monkeypatch.setattr(planner_service.settings, "PARETO_PLANNER_MAX_UNITS", 1)
    monkeypatch.setattr(planner_service.settings, "PARETO_TARGET_COVERAGE_RATIO", 0.9)

    book_id = uuid.uuid4()
    long_note = _section(book_id=book_id, section_index=1, title="Extended Notes", path="1.1", level=1, text="minor note " * 3000)
    core = _section(book_id=book_id, section_index=2, title="Core Concepts", path="1.2", level=1, text="concept " * 100)

    units = plan_learning_units([long_note, core], PlanMode.PARETO)

    assert len(units) == 1
    assert units[0].source_section_ids == [core.id]
    assert units[0].unit_type == "pareto_core"


def test_pareto_fallback_values_structural_importance_without_keywords(monkeypatch):
    monkeypatch.setattr(planner_service.settings, "PARETO_PLANNER_MAX_UNITS", 1)
    monkeypatch.setattr(planner_service.settings, "PARETO_TARGET_COVERAGE_RATIO", 0.9)

    book_id = uuid.uuid4()
    long_note = _section(book_id=book_id, section_index=1, title="Extended Notes", path="1", level=1, text="minor note " * 3000)
    root = _section(book_id=book_id, section_index=2, title="Boolean Algebra", path="2", level=1, text="boolean algebra " * 80)
    children = [
        _section(book_id=book_id, section_index=3, title="AND", path="2.1", level=2, text="and operator " * 80, parent_id=root.id),
        _section(book_id=book_id, section_index=4, title="OR", path="2.2", level=2, text="or operator " * 80, parent_id=root.id),
        _section(book_id=book_id, section_index=5, title="NOT", path="2.3", level=2, text="not operator " * 80, parent_id=root.id),
        _section(book_id=book_id, section_index=6, title="Karnaugh Map", path="2.4", level=2, text="map simplification " * 80, parent_id=root.id),
    ]

    units = plan_learning_units([long_note, root, *children], PlanMode.PARETO)

    assert len(units) == 1
    assert units[0].source_section_ids == [root.id, *[child.id for child in children]]
