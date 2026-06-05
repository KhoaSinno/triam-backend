from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.agent_grounding.contracts import GroundingIntent
from app.services.agent_grounding.intent_router import detect_section_intent
from app.services.agent_grounding.query_normalizer import normalize_query, normalized_key, tokenize
from app.services.agent_grounding.section_reference_parser import parse_section_reference
from app.services.voice_agent.turn_state import VoiceTranscriptSnapshot
from app.services.voice_agent.web_permission_intent_classifier import classify_web_permission_intent_fast_path

_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,}(?:[-_/][A-Z0-9]{2,})*\b")
_QUOTED_RE = re.compile(r"[\"'“”‘’]([^\"'“”‘’]{2,})[\"'“”‘’]")

_STOPWORDS = {
    "a",
    "about",
    "an",
    "and",
    "anh",
    "ạ",
    "ban",
    "book",
    "can",
    "cho",
    "co",
    "could",
    "cua",
    "cuon",
    "de",
    "duoc",
    "em",
    "giup",
    "hay",
    "ho",
    "i",
    "is",
    "la",
    "lai",
    "me",
    "minh",
    "nay",
    "noi",
    "please",
    "quyen",
    "sach",
    "the",
    "this",
    "toi",
    "trong",
    "ve",
    "vui",
    "with",
    "you",
}

_ACK_ONLY_CLARIFICATION = "Bạn muốn hỏi nội dung nào trong sách?"
_MISSING_SECTION_CLARIFICATION = "Bạn muốn hỏi chương hoặc đề mục nào?"
_MISMATCH_CLARIFICATION = "Mình nghe chưa chắc câu hỏi. Bạn nói lại ngắn gọn giúp mình nhé."


@dataclass(frozen=True)
class VoiceQueryGuardConfig:
    min_chars: int = 6
    min_tokens: int = 2
    min_overlap_ratio: float = 0.34
    min_important_overlap_ratio: float = 0.25


@dataclass(frozen=True)
class VoiceQueryGuardResult:
    valid: bool
    reason_code: str
    clarification: str | None = None
    token_count: int = 0
    important_token_count: int = 0
    overlap_ratio: float | None = None
    important_overlap_ratio: float | None = None
    transcript_source: str | None = None


def _content_tokens(text: str) -> set[str]:
    return {token for token in tokenize(normalized_key(text)) if token not in _STOPWORDS}


def _important_tokens(text: str) -> set[str]:
    normalized = normalize_query(text)
    important = {
        token
        for token in normalized.tokens
        if token not in _STOPWORDS and (len(token) >= 4 or any(character.isdigit() for character in token))
    }
    for acronym in _ACRONYM_RE.findall(text):
        important.update(tokenize(normalized_key(acronym)))
    for quoted in _QUOTED_RE.findall(text):
        important.update(token for token in tokenize(normalized_key(quoted)) if token not in _STOPWORDS)
    return important


def _ratio(matched_count: int, denominator_count: int) -> float:
    return matched_count / max(1, denominator_count)


def _invalid(
    reason_code: str,
    clarification: str,
    *,
    token_count: int,
    important_token_count: int,
    overlap_ratio: float | None = None,
    important_overlap_ratio: float | None = None,
    transcript_source: str | None = None,
) -> VoiceQueryGuardResult:
    return VoiceQueryGuardResult(
        valid=False,
        reason_code=reason_code,
        clarification=clarification,
        token_count=token_count,
        important_token_count=important_token_count,
        overlap_ratio=overlap_ratio,
        important_overlap_ratio=important_overlap_ratio,
        transcript_source=transcript_source,
    )


def assess_voice_query(query: str, *, config: VoiceQueryGuardConfig | None = None) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    normalized = normalize_query(query)
    content_tokens = _content_tokens(query)
    important_tokens = _important_tokens(query)
    token_count = len(content_tokens)
    important_token_count = len(important_tokens)

    permission_result = classify_web_permission_intent_fast_path(query)
    if permission_result is not None and permission_result.intent != "new_question":
        return _invalid(
            "permission_reply",
            "Đây có vẻ là câu trả lời cho yêu cầu tìm web trước đó.",
            token_count=token_count,
            important_token_count=important_token_count,
        )

    if len(normalized.normalized) < resolved_config.min_chars or token_count < resolved_config.min_tokens:
        return _invalid(
            "too_short_or_ack_only",
            _ACK_ONLY_CLARIFICATION,
            token_count=token_count,
            important_token_count=important_token_count,
        )

    reference = parse_section_reference(normalized)
    if detect_section_intent(normalized, reference) == GroundingIntent.CLARIFICATION_REQUIRED:
        return _invalid(
            "missing_section_reference",
            _MISSING_SECTION_CLARIFICATION,
            token_count=token_count,
            important_token_count=important_token_count,
        )

    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid",
        token_count=token_count,
        important_token_count=important_token_count,
    )


def compare_query_with_transcript(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    base_result = assess_voice_query(query, config=resolved_config)
    if not base_result.valid:
        return base_result
    if transcript is None:
        return base_result

    query_tokens = _content_tokens(query)
    transcript_tokens = _content_tokens(transcript.text)
    important_query_tokens = _important_tokens(query)
    important_transcript_tokens = _important_tokens(transcript.text)
    overlap_ratio = _ratio(len(query_tokens & transcript_tokens), len(query_tokens))
    important_overlap_ratio = (
        _ratio(len(important_query_tokens & important_transcript_tokens), len(important_query_tokens))
        if important_query_tokens
        else None
    )

    if overlap_ratio < resolved_config.min_overlap_ratio:
        return _invalid(
            "tool_query_transcript_mismatch",
            _MISMATCH_CLARIFICATION,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            overlap_ratio=overlap_ratio,
            important_overlap_ratio=important_overlap_ratio,
            transcript_source=transcript.source,
        )

    if important_overlap_ratio is not None and important_overlap_ratio < resolved_config.min_important_overlap_ratio:
        return _invalid(
            "tool_query_important_token_mismatch",
            _MISMATCH_CLARIFICATION,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            overlap_ratio=overlap_ratio,
            important_overlap_ratio=important_overlap_ratio,
            transcript_source=transcript.source,
        )

    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        overlap_ratio=overlap_ratio,
        important_overlap_ratio=important_overlap_ratio,
        transcript_source=transcript.source,
    )


def guard_voice_book_query(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
) -> VoiceQueryGuardResult:
    return compare_query_with_transcript(query, transcript, config=config)
