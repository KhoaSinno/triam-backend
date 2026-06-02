from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class ParetoSignal:
    key: str
    unit_type: str
    weight: float
    vi_terms: tuple[str, ...]
    en_terms: tuple[str, ...]


PARETO_SIGNALS: tuple[ParetoSignal, ...] = (
    ParetoSignal(
        key="core_concept",
        unit_type="pareto_core",
        weight=1.0,
        vi_terms=("khái niệm", "nền tảng", "cốt lõi", "tổng quan"),
        en_terms=(
            "concept",
            "concepts",
            "core concept",
            "core concepts",
            "fundamental",
            "fundamentals",
            "overview",
            "overviews",
            "introduction",
            "introductions",
        ),
    ),
    ParetoSignal(
        key="definition",
        unit_type="pareto_core",
        weight=1.0,
        vi_terms=("định nghĩa",),
        en_terms=("definition", "define", "defined as"),
    ),
    ParetoSignal(
        key="principle",
        unit_type="pareto_core",
        weight=0.95,
        vi_terms=("nguyên lý", "nguyên tắc"),
        en_terms=("principle", "principles", "law", "laws"),
    ),
    ParetoSignal(
        key="method",
        unit_type="pareto_method",
        weight=0.9,
        vi_terms=("phương pháp", "cách làm", "kỹ thuật"),
        en_terms=("method", "methods", "technique", "techniques", "approach"),
    ),
    ParetoSignal(
        key="procedure",
        unit_type="pareto_method",
        weight=0.85,
        vi_terms=("quy trình", "các bước", "hướng dẫn"),
        en_terms=("procedure", "procedures", "process", "steps", "workflow", "guide", "guides", "tutorial", "tutorials"),
    ),
    ParetoSignal(
        key="rule",
        unit_type="pareto_rule",
        weight=0.9,
        vi_terms=("quy tắc", "luật", "điều kiện"),
        en_terms=("rule", "rules", "condition", "conditions", "criteria"),
    ),
    ParetoSignal(
        key="formula",
        unit_type="pareto_formula",
        weight=0.9,
        vi_terms=("công thức", "biểu thức"),
        en_terms=("formula", "formulas", "equation", "equations", "expression", "expressions", "identity", "identities"),
    ),
    ParetoSignal(
        key="theorem",
        unit_type="pareto_rule",
        weight=0.9,
        vi_terms=("định lý", "bổ đề", "hệ quả"),
        en_terms=("theorem", "theorems", "lemma", "lemmas", "corollary"),
    ),
    ParetoSignal(
        key="reasoning",
        unit_type="pareto_core",
        weight=0.85,
        vi_terms=("suy luận", "lập luận", "chứng minh", "logic"),
        en_terms=("reasoning", "inference", "proof", "argument", "logic"),
    ),
    ParetoSignal(
        key="example",
        unit_type="pareto_example",
        weight=0.4,
        vi_terms=("ví dụ", "minh họa", "bài tập"),
        en_terms=("example", "examples", "case study", "exercise", "exercises", "illustration"),
    ),
)

NOISE_TERMS: tuple[str, ...] = (
    "phụ lục",
    "tài liệu tham khảo",
    "tham khảo",
    "appendix",
    "references",
    "bibliography",
)


def normalize_signal_text(value: str) -> str:
    lowered = value.casefold()
    without_accents = "".join(
        char for char in unicodedata.normalize("NFD", lowered) if unicodedata.category(char) != "Mn"
    )
    normalized = without_accents.replace("đ", "d")
    return re.sub(r"\s+", " ", normalized).strip()


def _contains_term(normalized_text: str, normalized_term: str) -> bool:
    if not normalized_text or not normalized_term:
        return False
    pattern = rf"(?<![a-z0-9]){re.escape(normalized_term)}(?![a-z0-9])"
    return re.search(pattern, normalized_text) is not None


def _matches_any(normalized_text: str, terms: tuple[str, ...]) -> bool:
    return any(_contains_term(normalized_text, normalize_signal_text(term)) for term in terms)


def guess_section_language(title: str, excerpt: str = "") -> str:
    sample = f"{title} {excerpt[:300]}".casefold()
    vi_markers = ("đ", "ă", "â", "ê", "ô", "ơ", "ư", "khái", "định", "phương", "quy tắc")
    en_markers = ("the ", "and ", "of ", "definition", "method", "concept", "principle", "rule")

    vi_score = sum(1 for marker in vi_markers if marker in sample)
    en_score = sum(1 for marker in en_markers if marker in sample)

    if vi_score and en_score:
        return "mixed"
    if vi_score:
        return "vi"
    if en_score:
        return "en"
    return "unknown"


def extract_pareto_signal_hints(title: str, excerpt: str = "") -> list[str]:
    normalized = normalize_signal_text(f"{title} {excerpt[:300]}")
    hints: list[str] = []
    for signal in PARETO_SIGNALS:
        if _matches_any(normalized, signal.vi_terms + signal.en_terms):
            hints.append(signal.key)
    return hints


def infer_unit_type_from_signals(hints: list[str]) -> str:
    for hint in hints:
        for signal in PARETO_SIGNALS:
            if signal.key == hint:
                return signal.unit_type
    return "pareto_focus"


def score_pareto_signals(title: str, excerpt: str = "") -> float:
    title_normalized = normalize_signal_text(title)
    excerpt_normalized = normalize_signal_text(excerpt[:500])
    score = 0.0

    for signal in PARETO_SIGNALS:
        terms = signal.vi_terms + signal.en_terms
        if _matches_any(title_normalized, terms):
            score += signal.weight * 5000
            continue
        if excerpt_normalized and _matches_any(excerpt_normalized, terms):
            score += signal.weight * 1200

    if _matches_any(title_normalized, NOISE_TERMS):
        score -= 2500
    return score
