from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.agent_grounding.contracts import GroundingIntent
from app.services.agent_grounding.intent_router import detect_section_intent
from app.services.agent_grounding.query_normalizer import normalize_query, normalized_key, tokenize
from app.services.agent_grounding.section_reference_parser import parse_section_reference
from app.services.voice_agent.turn_state import PendingVoiceClarification, VoiceTranscriptSnapshot
from app.services.voice_agent.voice_intent_classifier import VoiceReplyIntentResult, classify_voice_reply_intent_fast_path
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


GENERIC_CLARIFICATION_REASON_CODES = frozenset(
    {
        "tool_query_transcript_mismatch",
        "tool_query_important_token_mismatch",
        "too_short_or_ack_only",
    }
)


@dataclass(frozen=True)
class VoiceQueryGuardConfig:
    min_chars: int = 6
    min_tokens: int = 2
    min_overlap_ratio: float = 0.34
    min_important_overlap_ratio: float = 0.25
    clarification_confirmation_max_tokens: int = 4
    clarification_min_query_prompt_overlap: float = 0.45
    enforce_transcript_overlap: bool = False


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
    guard_mode: str = "normal"
    pending_reason_code: str | None = None


def _content_tokens(text: str) -> set[str]:
    return {token for token in tokenize(normalized_key(text)) if token not in _STOPWORDS}


def _important_tokens(text: str) -> set[str]:
    normalized = normalize_query(text)
    important = {token for token in normalized.tokens if token not in _STOPWORDS and (len(token) >= 4 or any(character.isdigit() for character in token))}
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
    guard_mode: str = "normal",
    pending_reason_code: str | None = None,
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
        guard_mode=guard_mode,
        pending_reason_code=pending_reason_code,
    )


def _query_matches_pending_clarification(
    query: str,
    pending: PendingVoiceClarification,
    *,
    min_ratio: float,
) -> bool:
    query_tokens = _content_tokens(query)
    if not query_tokens:
        return False
    query_targets = _section_reference_targets(query)

    candidates = []
    if pending.candidate_query:
        candidates.append(pending.candidate_query)
    candidates.append(pending.prompt_text)

    for candidate in candidates:
        candidate_tokens = _content_tokens(candidate)
        if not candidate_tokens:
            continue
        candidate_targets = _section_reference_targets(candidate)
        if query_targets and candidate_targets and query_targets.isdisjoint(candidate_targets):
            continue
        overlap_ratio = _ratio(len(query_tokens & candidate_tokens), len(query_tokens))
        if overlap_ratio >= min_ratio:
            return True

    return False


def _section_reference_targets(text: str) -> set[str]:
    reference = parse_section_reference(normalize_query(text))
    targets: set[str] = set()
    if reference.explicit_path:
        targets.add(reference.explicit_path)
    if reference.explicit_ordinal is not None:
        targets.add(str(reference.explicit_ordinal))
    return targets


def _valid_clarification_confirmation(
    base_result: VoiceQueryGuardResult,
    transcript: VoiceTranscriptSnapshot,
    pending: PendingVoiceClarification,
) -> VoiceQueryGuardResult:
    return VoiceQueryGuardResult(
        valid=True,
        reason_code="valid_clarification_confirmation",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        overlap_ratio=1.0,
        important_overlap_ratio=1.0,
        transcript_source=transcript.source,
        guard_mode="clarification_confirmed",
        pending_reason_code=pending.reason_code,
    )


def _pending_clarification_reply_result(
    query: str,
    transcript: VoiceTranscriptSnapshot,
    base_result: VoiceQueryGuardResult,
    pending: PendingVoiceClarification,
    *,
    config: VoiceQueryGuardConfig,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult | None:
    resolved_reply = reply_intent or classify_voice_reply_intent_fast_path(
        transcript.text,
        max_grant_tokens=config.clarification_confirmation_max_tokens,
    )
    if resolved_reply is None:
        return None

    if resolved_reply.intent == "grant":
        is_generic_mismatch = pending.reason_code in GENERIC_CLARIFICATION_REASON_CODES
        if is_generic_mismatch or _query_matches_pending_clarification(
            query,
            pending,
            min_ratio=config.clarification_min_query_prompt_overlap,
        ):
            return _valid_clarification_confirmation(base_result, transcript, pending)
        return _invalid(
            "clarification_query_mismatch",
            _MISMATCH_CLARIFICATION,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_pending",
            pending_reason_code=pending.reason_code,
        )

    if resolved_reply.intent == "deny":
        return _invalid(
            "clarification_denied",
            "Được, bạn muốn hỏi nội dung nào khác?",
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_pending",
            pending_reason_code=pending.reason_code,
        )

    if resolved_reply.intent == "new_question":
        return VoiceQueryGuardResult(
            valid=False,
            reason_code="clarification_new_question",
            clarification=None,
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="clarification_new_question",
            pending_reason_code=pending.reason_code,
        )

    return _invalid(
        "clarification_reply_unclear",
        "Bạn xác nhận hay muốn hỏi câu khác?",
        token_count=base_result.token_count,
        important_token_count=base_result.important_token_count,
        transcript_source=transcript.source,
        guard_mode="clarification_pending",
        pending_reason_code=pending.reason_code,
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
    pending_clarification: PendingVoiceClarification | None = None,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    base_result = assess_voice_query(query, config=resolved_config)
    if not base_result.valid:
        return base_result
    if transcript is None:
        return base_result

    resolved_reply = reply_intent or classify_voice_reply_intent_fast_path(
        transcript.text,
        max_grant_tokens=resolved_config.clarification_confirmation_max_tokens,
    )

    if pending_clarification is not None:
        pending_result = _pending_clarification_reply_result(
            query,
            transcript,
            base_result,
            pending_clarification,
            config=resolved_config,
            reply_intent=resolved_reply,
        )
        if pending_result is not None:
            return pending_result
    # else:
    #     if resolved_reply is not None and resolved_reply.intent == "grant":
    #         return VoiceQueryGuardResult(
    #             valid=True,
    #             reason_code="valid_confirmation_bypass",
    #             token_count=base_result.token_count,
    #             important_token_count=base_result.important_token_count,
    #             overlap_ratio=1.0,
    #             important_overlap_ratio=1.0,
    #             transcript_source=transcript.source,
    #             guard_mode="confirmation_bypass",
    #         )

    if not resolved_config.enforce_transcript_overlap:
        return VoiceQueryGuardResult(
            valid=True,
            reason_code="valid_transcript_overlap_bypassed",
            token_count=base_result.token_count,
            important_token_count=base_result.important_token_count,
            transcript_source=transcript.source,
            guard_mode="transcript_overlap_bypassed",
        )

    query_tokens = _content_tokens(query)
    transcript_tokens = _content_tokens(transcript.text)
    important_query_tokens = _important_tokens(query)
    important_transcript_tokens = _important_tokens(transcript.text)
    overlap_ratio = _ratio(len(query_tokens & transcript_tokens), len(query_tokens))
    important_overlap_ratio = _ratio(len(important_query_tokens & important_transcript_tokens), len(important_query_tokens)) if important_query_tokens else None

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
    pending_clarification: PendingVoiceClarification | None = None,
    reply_intent: VoiceReplyIntentResult | None = None,
) -> VoiceQueryGuardResult:
    return compare_query_with_transcript(
        query,
        transcript,
        config=config,
        pending_clarification=pending_clarification,
        reply_intent=reply_intent,
    )
