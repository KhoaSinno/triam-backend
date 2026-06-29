from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.services.agent_grounding.query_normalizer import normalize_query, normalized_key, tokenize

_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,}(?:[-_/][A-Z0-9]{2,})*\b")
_QUOTED_RE = re.compile(r"[\"'“”‘’]([^\"'“”‘’]{2,})[\"'“”‘’]")

from app.core.stopwords import STOPWORDS


@dataclass(frozen=True)
class HybridRetrievalConfig:
    vector_weight: float
    lexical_weight: float
    title_match_boost: float
    multi_source_boost: float
    min_final_score: float
    max_context_chunks: int
    max_chunks_per_section: int
    validate_evidence_enabled: bool = True


@dataclass
class RetrievalCandidate:
    id: str
    book_id: str
    section_id: str
    section_path: str = ""
    section_title: str = ""
    chunk_index: int = 0
    content: str = ""
    vector_score: float | None = None
    lexical_score: float | None = None
    final_score: float = 0.0
    sources: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class EvidenceValidationResult:
    valid: bool
    reason_code: str
    missing_token_count: int = 0


@dataclass(frozen=True)
class HybridRetrievalResult:
    found: bool
    chunks: list[dict[str, Any]]
    method: str
    reason_code: str
    candidate_count: int
    top_candidate_id: str | None = None
    top_vector_score: float | None = None
    top_lexical_score: float | None = None
    top_final_score: float | None = None
    missing_token_count: int = 0


def _clamp_score(value: float | int | None) -> float:
    if value is None:
        return 0.0
    return max(0.0, min(float(value), 1.0))


def _candidate_key(item: dict[str, Any]) -> str:
    item_id = item.get("id")
    if item_id is not None:
        return str(item_id)
    return f"{item.get('section_id', '')}:{item.get('chunk_index', '')}"


def _to_candidate(item: dict[str, Any], source: str) -> RetrievalCandidate:
    vector_score = item.get("similarity") if source == "vector" else item.get("vector_score")
    lexical_score = item.get("lexical_score") if source == "lexical" else item.get("lexical_score")
    candidate = RetrievalCandidate(
        id=_candidate_key(item),
        book_id=str(item.get("book_id") or ""),
        section_id=str(item.get("section_id") or ""),
        section_path=str(item.get("section_path") or ""),
        section_title=str(item.get("section_title") or ""),
        chunk_index=int(item.get("chunk_index") or 0),
        content=str(item.get("content") or ""),
        vector_score=_clamp_score(vector_score) if vector_score is not None else None,
        lexical_score=_clamp_score(lexical_score) if lexical_score is not None else None,
        sources={source},
    )
    return candidate


def merge_candidates(
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
) -> list[RetrievalCandidate]:
    merged: dict[str, RetrievalCandidate] = {}
    for source, payload in (("vector", vector_payload), ("lexical", lexical_payload)):
        for item in payload:
            if not isinstance(item, dict):
                continue
            key = _candidate_key(item)
            candidate = merged.get(key)
            next_candidate = _to_candidate(item, source)
            if candidate is None:
                merged[key] = next_candidate
                continue

            candidate.sources.add(source)
            candidate.vector_score = max(
                _clamp_score(candidate.vector_score),
                _clamp_score(next_candidate.vector_score),
            ) or None
            candidate.lexical_score = max(
                _clamp_score(candidate.lexical_score),
                _clamp_score(next_candidate.lexical_score),
            ) or None
            candidate.section_path = candidate.section_path or next_candidate.section_path
            candidate.section_title = candidate.section_title or next_candidate.section_title
            candidate.content = candidate.content or next_candidate.content
            candidate.book_id = candidate.book_id or next_candidate.book_id
            candidate.section_id = candidate.section_id or next_candidate.section_id
    return list(merged.values())


def _token_overlap(query_tokens: set[str], text: str) -> bool:
    if not query_tokens:
        return False
    text_tokens = set(tokenize(normalized_key(text)))
    return bool(query_tokens & text_tokens)


def rerank_candidates(
    query: str,
    candidates: list[RetrievalCandidate],
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
    config: HybridRetrievalConfig,
    k: int = 60,
) -> list[RetrievalCandidate]:
    
    # 1. Xác định thứ hạng (1-indexed) của từng ứng viên trong luồng Vector Search
    vector_ranks = {_candidate_key(item): idx + 1 for idx, item in enumerate(vector_payload)}
    
    # 2. Xác định thứ hạng (1-indexed) của từng ứng viên trong luồng Lexical Search
    lexical_ranks = {_candidate_key(item): idx + 1 for idx, item in enumerate(lexical_payload)}
    
    # 3. Tính điểm RRF cho từng ứng viên theo công thức chuẩn quốc tế
    for candidate in candidates:
        c_id = candidate.id
        term_v = 1.0 / (k + vector_ranks[c_id]) if c_id in vector_ranks else 0.0
        term_l = 1.0 / (k + lexical_ranks[c_id]) if c_id in lexical_ranks else 0.0
        candidate.final_score = term_v + term_l
        
    return sorted(
        candidates,
        key=lambda item: (
            item.final_score,
            _clamp_score(item.lexical_score),
            _clamp_score(item.vector_score),
            -item.chunk_index,
        ),
        reverse=True,
    )


def select_context_candidates(
    candidates: list[RetrievalCandidate],
    config: HybridRetrievalConfig,
) -> list[RetrievalCandidate]:
    selected: list[RetrievalCandidate] = []
    per_section: dict[str, int] = {}
    max_total = max(1, config.max_context_chunks)
    max_per_section = max(1, config.max_chunks_per_section)
    for candidate in candidates:
        section_key = candidate.section_id or candidate.section_path or candidate.id
        if per_section.get(section_key, 0) >= max_per_section:
            continue
        selected.append(candidate)
        per_section[section_key] = per_section.get(section_key, 0) + 1
        if len(selected) >= max_total:
            break
    return selected


def _important_query_tokens(query: str) -> set[str]:
    normalized = normalize_query(query)
    important = {
        token
        for token in normalized.tokens
        if (len(token) >= 5 or any(char.isdigit() for char in token))
        and token not in STOPWORDS
    }
    for acronym in _ACRONYM_RE.findall(query):
        important.update(tokenize(normalized_key(acronym)))
    for quoted in _QUOTED_RE.findall(query):
        important.update(token for token in tokenize(normalized_key(quoted)) if token not in STOPWORDS)
    return important


def validate_evidence(
    query: str,
    selected_candidates: list[RetrievalCandidate],
    config: HybridRetrievalConfig,
) -> EvidenceValidationResult:
    if not selected_candidates:
        return EvidenceValidationResult(valid=False, reason_code="no_candidates")

    if not config.validate_evidence_enabled:
        return EvidenceValidationResult(valid=True, reason_code="valid")

    top_vector_score = selected_candidates[0].vector_score
    if top_vector_score is not None and top_vector_score < config.min_final_score:
        return EvidenceValidationResult(valid=False, reason_code="low_confidence")

    important_tokens = _important_query_tokens(query)
    if important_tokens:
        evidence_text = normalized_key(
            " ".join(
                f"{candidate.section_path} {candidate.section_title} {candidate.content}"
                for candidate in selected_candidates[:2]
            )
        )
        evidence_tokens = set(tokenize(evidence_text))
        missing_tokens = important_tokens - evidence_tokens
        if missing_tokens and len(missing_tokens) == len(important_tokens):
            return EvidenceValidationResult(
                valid=False,
                reason_code="missing_named_entity",
                missing_token_count=len(missing_tokens),
            )

    return EvidenceValidationResult(valid=True, reason_code="valid")


def _candidate_to_payload(candidate: RetrievalCandidate) -> dict[str, Any]:
    return {
        "id": candidate.id,
        "book_id": candidate.book_id,
        "section_id": candidate.section_id,
        "section_path": candidate.section_path,
        "section_title": candidate.section_title,
        "chunk_index": candidate.chunk_index,
        "content": candidate.content,
        "similarity": candidate.final_score,
        "vector_score": candidate.vector_score,
        "lexical_score": candidate.lexical_score,
        "final_score": candidate.final_score,
        "retrieval_method": "hybrid",
        "retrieval_sources": sorted(candidate.sources),
    }


def build_hybrid_retrieval_result(
    *,
    query: str,
    vector_payload: list[dict[str, Any]],
    lexical_payload: list[dict[str, Any]],
    config: HybridRetrievalConfig,
) -> HybridRetrievalResult:
    candidates = merge_candidates(vector_payload, lexical_payload)
    ranked = rerank_candidates(query, candidates, vector_payload, lexical_payload, config)
    selected = select_context_candidates(ranked, config)
    validation = validate_evidence(query, selected, config)
    top_candidate = selected[0] if selected else None
    if not validation.valid:
        return HybridRetrievalResult(
            found=False,
            chunks=[],
            method="hybrid",
            reason_code=validation.reason_code,
            candidate_count=len(candidates),
            top_candidate_id=top_candidate.id if top_candidate else None,
            top_vector_score=top_candidate.vector_score if top_candidate else None,
            top_lexical_score=top_candidate.lexical_score if top_candidate else None,
            top_final_score=top_candidate.final_score if top_candidate else None,
            missing_token_count=validation.missing_token_count,
        )
    return HybridRetrievalResult(
        found=True,
        chunks=[_candidate_to_payload(candidate) for candidate in selected],
        method="hybrid",
        reason_code=validation.reason_code,
        candidate_count=len(candidates),
        top_candidate_id=top_candidate.id if top_candidate else None,
        top_vector_score=top_candidate.vector_score if top_candidate else None,
        top_lexical_score=top_candidate.lexical_score if top_candidate else None,
        top_final_score=top_candidate.final_score if top_candidate else None,
        missing_token_count=validation.missing_token_count,
    )
