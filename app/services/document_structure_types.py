from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class ParsedSection:
    title: str
    level: int
    order_index: int
    path: str
    text: str = ""
    page_start: int | None = None
    page_end: int | None = None
    source_href: str | None = None
    source_anchor: str | None = None
    top: float | None = None
    children: list["ParsedSection"] = field(default_factory=list)

    @property
    def text_char_count(self) -> int:
        return len(self.text or "")


@dataclass(frozen=True)
class ParsedDocument:
    document_type: str
    sections: list[ParsedSection]

    @property
    def total_sections(self) -> int:
        return len(flatten_sections(self.sections))

    @property
    def max_depth(self) -> int:
        return max_section_depth(self.sections)


def flatten_sections(sections: list[ParsedSection]) -> list[ParsedSection]:
    flattened: list[ParsedSection] = []

    def walk(items: list[ParsedSection]) -> None:
        for section in items:
            flattened.append(section)
            walk(section.children)

    walk(sections)
    return flattened


def max_section_depth(sections: list[ParsedSection]) -> int:
    if not sections:
        return 0

    def depth(section: ParsedSection) -> int:
        if not section.children:
            return section.level
        return max(depth(child) for child in section.children)

    return max(depth(section) for section in sections)


def section_subtree_text(section: ParsedSection) -> str:
    parts: list[str] = []

    def walk(item: ParsedSection) -> None:
        if item.text.strip():
            parts.append(item.text.strip())
        for child in item.children:
            walk(child)

    walk(section)
    return "\n\n".join(parts).strip()


def has_extractable_text(sections: list[ParsedSection]) -> bool:
    return any(section_subtree_text(section) for section in sections)


def with_reindexed_paths(sections: list[ParsedSection]) -> list[ParsedSection]:
    def walk(items: list[ParsedSection], parent_path: str = "") -> list[ParsedSection]:
        updated: list[ParsedSection] = []
        for index, section in enumerate(items, start=1):
            path = f"{parent_path}.{index}" if parent_path else str(index)
            updated.append(
                replace(
                    section,
                    order_index=index - 1,
                    path=path,
                    children=walk(section.children, path),
                )
            )
        return updated

    return walk(sections)
