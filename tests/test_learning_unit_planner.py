import uuid

from app.core.constant import PlanMode
from app.models.db_models import BookSection
from app.services import learning_unit_planner_service as planner_service
from app.services.learning_unit_planner_service import plan_full_learning_units


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

    units = plan_full_learning_units([root, child_a, child_b])

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

    units = plan_full_learning_units([root, child_a, child_b, child_c])
    titles = [unit.title for unit in units]

    assert len(units) > 1
    assert len(titles) == len(set(titles))
    assert all(title.startswith("PHÉP ĐẾM - Phần ") for title in titles)

