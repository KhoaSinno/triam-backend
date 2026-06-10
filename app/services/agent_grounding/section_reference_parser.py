from __future__ import annotations

import re

from app.services.agent_grounding.contracts import NormalizedQuery, SectionReference
from app.services.agent_grounding.query_normalizer import fold_accents, normalize_text

SECTION_MARKERS = {"chuong", "chapter", "phan", "part", "muc", "section"}
GENERIC_SECTION_SUFFIX = {
    "cua",
    "quyen",
    "sach",
    "nay",
    "do",
    "gi",
    "la",
    "trong",
    "the",
    "this",
    "book",
    "please",
}
PATH_PATTERN = re.compile(r"^\d+(?:\.\d+)+$")
ROMAN_PATTERN = re.compile(r"^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$", re.IGNORECASE)
QUOTED_TEXT_PATTERN = re.compile(r'["“”\']([^"“”\']{2,160})["“”\']')

VI_UNITS = {
    "khong": 0,
    "mot": 1,
    "hai": 2,
    "ba": 3,
    "bon": 4,
    "tu": 4,
    "nam": 5,
    "lam": 5,
    "sau": 6,
    "bay": 7,
    "tam": 8,
    "chin": 9,
}
EN_UNITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
EN_TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


def _parse_roman(value: str) -> int | None:
    candidate = value.strip().lower()
    if not candidate or not ROMAN_PATTERN.fullmatch(candidate):
        return None
    values = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    result = 0
    previous = 0
    for character in reversed(candidate):
        current = values[character]
        result += -current if current < previous else current
        previous = max(previous, current)
    return result or None


def _parse_english_number(tokens: list[str]) -> int | None:
    if not tokens or any(token not in EN_UNITS and token not in EN_TENS and token not in {"and", "hundred", "thousand"} for token in tokens):
        return None
    total = 0
    current = 0
    consumed_number = False
    for token in tokens:
        if token == "and":
            continue
        if token in EN_UNITS:
            current += EN_UNITS[token]
            consumed_number = True
        elif token in EN_TENS:
            current += EN_TENS[token]
            consumed_number = True
        elif token == "hundred":
            current = max(current, 1) * 100
            consumed_number = True
        elif token == "thousand":
            total += max(current, 1) * 1000
            current = 0
            consumed_number = True
    value = total + current
    return value if consumed_number and value > 0 else None


def _parse_vi_under_hundred(tokens: list[str]) -> int | None:
    tokens = [token for token in tokens if token not in {"le", "linh"}]
    if not tokens:
        return 0
    if len(tokens) == 1:
        return 10 if tokens[0] == "muoi" else VI_UNITS.get(tokens[0])
    if tokens[0] == "muoi" and len(tokens) == 2 and tokens[1] in VI_UNITS:
        return 10 + VI_UNITS[tokens[1]]
    if len(tokens) in {2, 3} and tokens[0] in VI_UNITS and tokens[1] == "muoi":
        return VI_UNITS[tokens[0]] * 10 + (VI_UNITS.get(tokens[2], 0) if len(tokens) == 3 else 0)
    return None


def _parse_vietnamese_number(tokens: list[str]) -> int | None:
    allowed = set(VI_UNITS) | {"muoi", "tram", "nghin", "le", "linh"}
    if not tokens or any(token not in allowed for token in tokens):
        return None

    total = 0
    remaining = tokens
    if "nghin" in remaining:
        index = remaining.index("nghin")
        thousands = _parse_vietnamese_number(remaining[:index]) if index else 1
        if thousands is None:
            return None
        total += thousands * 1000
        remaining = remaining[index + 1 :]

    if "tram" in remaining:
        index = remaining.index("tram")
        hundreds = VI_UNITS.get(remaining[index - 1], 1) if index else 1
        if index > 1:
            return None
        total += hundreds * 100
        remaining = remaining[index + 1 :]

    under_hundred = _parse_vi_under_hundred(remaining)
    if under_hundred is None:
        return None
    value = total + under_hundred
    return value if value > 0 else None


def parse_positive_integer_phrase(value: str) -> int | None:
    normalized = fold_accents(normalize_text(value)).replace("-", " ")
    if normalized.isdigit():
        parsed = int(normalized)
        return parsed if parsed > 0 else None
    roman = _parse_roman(normalized)
    if roman is not None:
        return roman
    tokens = normalized.split()
    return _parse_vietnamese_number(tokens) or _parse_english_number(tokens)


def _number_prefix(tokens: tuple[str, ...]) -> tuple[int | None, int]:
    for width in range(min(6, len(tokens)), 0, -1):
        value = parse_positive_integer_phrase(" ".join(tokens[:width]))
        if value is not None:
            return value, width
    return None, 0


def _quoted_title(original: str) -> str | None:
    match = QUOTED_TEXT_PATTERN.search(original)
    return match.group(1).strip() if match else None


def parse_section_reference(query: NormalizedQuery) -> SectionReference:
    quoted_title = _quoted_title(query.original)
    for index, token in enumerate(query.tokens):
        if token not in SECTION_MARKERS:
            continue

        remaining = query.tokens[index + 1 :]
        if not remaining:
            return SectionReference(marker_present=True, title_hint=quoted_title)

        first = remaining[0]
        if PATH_PATTERN.fullmatch(first):
            return SectionReference(marker_present=True, explicit_path=first, title_hint=quoted_title)
        if first.isdigit():
            value = int(first)
            return SectionReference(marker_present=True, explicit_ordinal=value if value > 0 else None, title_hint=quoted_title)

        ordinal, width = _number_prefix(remaining)
        if ordinal is not None:
            return SectionReference(marker_present=True, explicit_ordinal=ordinal, title_hint=quoted_title)

        if quoted_title:
            return SectionReference(marker_present=True, title_hint=quoted_title)

        title_tokens = [item for item in remaining if item not in GENERIC_SECTION_SUFFIX]
        title_hint = " ".join(title_tokens).strip() or None
        return SectionReference(marker_present=True, title_hint=title_hint)

    return SectionReference(marker_present=False, title_hint=quoted_title, explicit=quoted_title is not None)

