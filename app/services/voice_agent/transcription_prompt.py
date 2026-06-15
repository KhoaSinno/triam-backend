from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from app.services.agent_grounding.contracts import GroundingScope

_WHITESPACE_RE = re.compile(r"\s+")
_SECTION_NUMBER_RE = re.compile(r"^\s*(chapter|chương|part|phần|section|mục)\s+\d+", re.IGNORECASE)


@dataclass(frozen=True)
class TranscriptionPromptBuildResult:
    prompt: str
    term_count: int
    prompt_chars: int
    dynamic_enabled: bool


def _normalize_term(value: object) -> str:
    text = str(value or "").strip()
    text = _WHITESPACE_RE.sub(" ", text)
    text = text.strip(" -–—|,.;:")
    return text


def _add_unique(terms: list[str], seen: set[str], value: object, *, max_len: int = 80) -> None:
    term = _normalize_term(value)
    if not term:
        return

    if len(term) > max_len:
        term = term[:max_len].rstrip()

    key = term.casefold()
    if key in seen:
        return

    seen.add(key)
    terms.append(term)


def _split_path_terms(path: str | None) -> list[str]:
    if not path:
        return []

    raw = _normalize_term(path)
    if not raw:
        return []

    parts = re.split(r"\s*(?:>|/|\\|»|›)\s*", raw)
    result: list[str] = []

    for part in parts:
        part = _normalize_term(part)
        if part:
            result.append(part)

    if raw and raw not in result:
        result.append(raw)

    return result


def _base_domain_terms() -> tuple[str, ...]:
    return (
        "Tri Âm",
        "TRIAM",
        "chương",
        "sách",
        "tóm tắt",
        "nội dung chính",
        "nhân vật",
        "tác giả",
        "mục lục",
        "bài học",
        "đề mục",
        "định lý",
        "phương pháp",
        "khái niệm",
        "ví dụ",
        "giải thích",
        "so sánh",
        "tìm web",
        "tìm trên internet",
        "tra cứu web",
        "đồng ý",
        "không đồng ý",
        "có",
        "không",
        "tiếp tục",
        "dừng lại",
        "GPT",
        "Gemini",
        "OpenAI",
        "RAG",
    )


def _add_scope_terms(
    terms: list[str],
    seen: set[str],
    grounding_scope: GroundingScope,
    *,
    max_section_terms: int,
) -> None:
    for book in grounding_scope.books:
        _add_unique(terms, seen, book.title)
        _add_unique(terms, seen, book.author)
        if book.document_type:
            _add_unique(terms, seen, str(book.document_type))

    section_added = 0
    for section in grounding_scope.sections:
        if section_added >= max_section_terms:
            break
        section_added += _add_section_terms(terms, seen, section.title, section.path, max_section_terms - section_added)


def _add_section_terms(terms: list[str], seen: set[str], title: str, path: str, remaining: int) -> int:
    added = 0
    if remaining <= 0:
        return added

    if _normalize_term(title):
        _add_unique(terms, seen, title)
        added += 1

    for path_term in _split_path_terms(path):
        if added >= remaining:
            break
        _add_unique(terms, seen, path_term)
        added += 1

    return added


def _collect_dynamic_terms(
    grounding_scope: GroundingScope | None,
    *,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None,
) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()

    for term in _base_domain_terms():
        _add_unique(terms, seen, term)

    if extra_terms:
        for term in extra_terms:
            _add_unique(terms, seen, term)

    if grounding_scope is not None:
        _add_scope_terms(terms, seen, grounding_scope, max_section_terms=max_section_terms)

    return terms[: max(0, max_terms)]


def _build_prompt(base: str, terms: list[str], *, max_chars: int) -> str:
    dynamic_suffix = " Session-specific expected terms: " + ", ".join(terms) + "." if terms else ""
    prompt = (
        base
        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
        + dynamic_suffix
    ).strip()
    return _trim_prompt(prompt, max_chars=max_chars)


def _trim_prompt(prompt: str, *, max_chars: int) -> str:
    if max_chars <= 0 or len(prompt) <= max_chars:
        return prompt

    trimmed = prompt[:max_chars].rstrip()
    return trimmed if trimmed.endswith(".") else trimmed + "."


def build_realtime_transcription_prompt(
    *,
    base_prompt: str,
    grounding_scope: GroundingScope | None,
    enabled: bool,
    max_chars: int,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None = None,
) -> TranscriptionPromptBuildResult:
    base = _normalize_term(base_prompt)

    if not enabled:
        return TranscriptionPromptBuildResult(
            prompt=base,
            term_count=0,
            prompt_chars=len(base),
            dynamic_enabled=False,
        )

    terms = _collect_dynamic_terms(
        grounding_scope,
        max_terms=max_terms,
        max_section_terms=max_section_terms,
        extra_terms=extra_terms,
    )
    prompt = _build_prompt(base, terms, max_chars=max_chars)

    return TranscriptionPromptBuildResult(
        prompt=prompt,
        term_count=len(terms),
        prompt_chars=len(prompt),
        dynamic_enabled=True,
    )
