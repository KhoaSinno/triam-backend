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
    # Candidates are retained only in memory for a future schema-V2 keyword
    # adapter. They must never be written to production logs.
    keyword_candidates: tuple[str, ...] = ()
    prompt_term_count: int = 0
    context_hints_enabled: bool = False


def _normalize_term(value: object) -> str:
    text = str(value or "").strip()
    text = _WHITESPACE_RE.sub(" ", text)
    text = text.strip(" -–—|,.;:")
    return text


def _add_unique(terms: list[str], seen: set[str], value: object, *, max_len: int = 80) -> bool:
    term = _normalize_term(value)
    if not term:
        return False

    if len(term) > max_len:
        term = term[:max_len].rstrip()

    key = term.casefold()
    if key in seen:
        return False

    seen.add(key)
    terms.append(term)
    return True


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


def _collect_legacy_dynamic_terms(
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
    # Xây dựng câu thoại giả định (Mock Conversation) giúp Whisper học văn phong và thuật ngữ tốt hơn
    mock_dialogue = ""
    if terms:
        mock_dialogue = " Chào bạn! Hôm nay chúng ta sẽ cùng thảo luận về các thuật ngữ " + ", ".join(terms[:12]) + " nhé. Bạn muốn hỏi gì?"
    
    prompt = (
        base
        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
        + mock_dialogue
    ).strip()
    return _trim_prompt(prompt, max_chars=max_chars)


def _add_limited_terms(
    terms: list[str],
    seen: set[str],
    values: Iterable[object],
    *,
    limit: int,
) -> None:
    added = 0
    for value in values:
        if added >= max(0, limit):
            break
        if _add_unique(terms, seen, value):
            added += 1


def _prioritized_section_values(grounding_scope: GroundingScope) -> Iterable[str]:
    for section in grounding_scope.sections:
        yield section.title
        yield from _split_path_terms(section.path)


def _collect_prioritized_terms(
    grounding_scope: GroundingScope | None,
    *,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None,
) -> list[str]:
    """Build bounded vocabulary hints in business-value order.

    This path is intentionally separate from the legacy collector so the
    default-off rollout can retain its exact existing prompt behavior.
    """
    terms: list[str] = []
    seen: set[str] = set()

    if grounding_scope is not None:
        _add_limited_terms(
            terms,
            seen,
            (book.title for book in grounding_scope.books),
            limit=8,
        )
        _add_limited_terms(
            terms,
            seen,
            (
                value
                for book in grounding_scope.books
                for value in (book.author, book.document_type)
                if value
            ),
            limit=8,
        )
        _add_limited_terms(
            terms,
            seen,
            _prioritized_section_values(grounding_scope),
            limit=min(12, max(0, max_section_terms)),
        )

    _add_limited_terms(terms, seen, _base_domain_terms(), limit=12)
    if extra_terms:
        _add_limited_terms(terms, seen, extra_terms, limit=4)
    return terms[: max(0, max_terms)]


def _build_prioritized_prompt(
    base: str,
    prompt_terms: list[str],
    *,
    max_chars: int,
) -> str:
    prompt = (
        base
        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
    )
    if prompt_terms:
        prompt += " Expected names may include: " + ", ".join(prompt_terms) + "."
    return _trim_prompt(prompt.strip(), max_chars=max_chars)


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
    context_hints_enabled: bool = False,
    legacy_prompt_term_limit: int = 0,
) -> TranscriptionPromptBuildResult:
    base = _normalize_term(base_prompt)

    if not enabled:
        return TranscriptionPromptBuildResult(
            prompt=base,
            term_count=0,
            prompt_chars=len(base),
            dynamic_enabled=False,
        )

    if not context_hints_enabled:
        terms = _collect_legacy_dynamic_terms(
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

    terms = _collect_prioritized_terms(
        grounding_scope,
        max_terms=max_terms,
        max_section_terms=max_section_terms,
        extra_terms=extra_terms,
    )
    prompt_terms = terms[: max(0, legacy_prompt_term_limit)]
    prompt = _build_prioritized_prompt(base, prompt_terms, max_chars=max_chars)

    return TranscriptionPromptBuildResult(
        prompt=prompt,
        term_count=len(terms),
        prompt_chars=len(prompt),
        dynamic_enabled=True,
        keyword_candidates=tuple(terms),
        prompt_term_count=len(prompt_terms),
        context_hints_enabled=True,
    )
