from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

VoiceReplyIntent = Literal["grant", "deny", "unclear", "new_question"]

POSITIVE_ACTION_PHRASES = (
    "dong y",
    "dung roi",
    "dung do",
    "chinh xac",
    "phai roi",
    "tim di",
    "tim kiem di",
    "search di",
    "lam di",
    "cu lam",
    "cu tim",
    "tiep di",
    "thu xem",
    "go ahead",
    "do it",
    "search it",
    "cho phep",
    "cho phep di",
    "cho phep lam",
    "duoc phep",
    "tim tren mang",
    "tim tren web",
    "tim google",
    "tim internet",
    "dong y tim",
    "dong y luon",
    "chap nhan",
    "dong y nha",
    "duoc chu",
    "co chu",
    "tim giup",
    "tim ho",
    "tim di ban",
    "u tim",
)
POSITIVE_SHORT_REPLIES = (
    "co",
    "uh",
    "um",
    "ok",
    "oke",
    "okay",
    "yes",
    "yep",
    "yup",
    "yub",
    "sure",
    "duoc",
    "duoc roi",
    "dung",
    "dung roi",
    "phai",
    "phai roi",
    "cho phep",
    "vang",
    "da vang",
    "da",
    "u",
    "ua",
)
NEGATIVE_PHRASES = (
    "khong phai",
    "khong can",
    "khong dau",
    "khong duoc",
    "khong muon",
    "khong thich",
    "khong",
    "khoi",
    "dung lam",
    "dung tim",
    "dung search",
    "thoi",
    "bo qua",
    "skip",
    "cancel",
    "stop",
    "nope",
    "nah",
    "no",
    "dont",
    "do not",
)

CONTEXT_SENSITIVE_NEGATIONS = {"khong", "no"}
CONTEXT_SENSITIVE_CONFIRMATIONS = {"co", "duoc", "dung", "phai", "uh", "um", "u", "da", "ua"}


@dataclass(frozen=True)
class VoiceReplyIntentResult:
    intent: VoiceReplyIntent
    confidence: float
    reason: str = ""
    source: str = "fast_path"


def normalize_voice_intent_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", (text or "").casefold())
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    without_marks = without_marks.replace("đ", "d")
    without_marks = re.sub(r"[^a-z0-9]+", " ", without_marks)
    return " ".join(without_marks.split())


def phrase_in_text(phrase: str, text: str) -> bool:
    return f" {phrase} " in f" {text} "


def looks_like_new_question(original_text: str, normalized_text: str) -> bool:
    return "?" in original_text


def classify_voice_reply_intent_fast_path(text: str, *, max_grant_tokens: int = 4) -> VoiceReplyIntentResult | None:
    normalized = normalize_voice_intent_text(text)
    if not normalized:
        return None

    token_count = len(normalized.split())
    # Constrain fast path positive/negative matching to short replies only
    if token_count > max(4, max_grant_tokens):
        if looks_like_new_question(text, normalized):
            return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark detected", "fast_path")
        return None

    # 1. Check negative phrases first
    for phrase in NEGATIVE_PHRASES:
        if phrase in CONTEXT_SENSITIVE_NEGATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")

    # 2. Check positive action phrases
    if any(phrase_in_text(phrase, normalized) for phrase in POSITIVE_ACTION_PHRASES):
        return VoiceReplyIntentResult("grant", 0.96, "Matched positive action fast path", "fast_path")

    # 3. Check positive short replies
    for phrase in POSITIVE_SHORT_REPLIES:
        if phrase in CONTEXT_SENSITIVE_CONFIRMATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")

    # 4. Check if it looks like a new question only if it does not match positive/negative phrases
    if looks_like_new_question(text, normalized):
        return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark detected", "fast_path")

    return None