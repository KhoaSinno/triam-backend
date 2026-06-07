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
    "phai",
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
)
NEGATIVE_PHRASES = (
    "khong phai",
    "khong can",
    "khong dau",
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
AMBIGUOUS_PHRASES = (
    "tuy",
    "tuy anh",
    "sao cung duoc",
    "sao cung",
    "cung duoc",
    "khong biet",
    "maybe",
    "up to you",
)
QUESTION_HINTS = (
    " la gi",
    " gi ",
    " nao",
    " ai ",
    " tai sao",
    " vi sao",
    " nhu the nao",
    " the nao",
    " co nhung",
    " chuong",
    " muc",
    " de muc",
    " noi dung",
    " phuong phap",
    " tom tat",
    " giai thich",
    " what",
    " why",
    " how",
    " when",
    " where",
    " which",
    " who",
    " tell me",
)


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
    if "?" in original_text:
        return True
    padded = f" {normalized_text} "
    return any(hint in padded for hint in QUESTION_HINTS)


def classify_voice_reply_intent_fast_path(text: str, *, max_grant_tokens: int = 3) -> VoiceReplyIntentResult | None:
    normalized = normalize_voice_intent_text(text)
    if not normalized:
        return VoiceReplyIntentResult("unclear", 1.0, "Empty reply", "fast_path")

    if any(phrase_in_text(phrase, normalized) for phrase in NEGATIVE_PHRASES):
        return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")

    if any(phrase_in_text(phrase, normalized) for phrase in POSITIVE_ACTION_PHRASES):
        return VoiceReplyIntentResult("grant", 0.96, "Matched positive action fast path", "fast_path")

    if any(phrase_in_text(phrase, normalized) for phrase in AMBIGUOUS_PHRASES):
        return VoiceReplyIntentResult("unclear", 0.88, "Matched ambiguous fast path", "fast_path")

    if looks_like_new_question(text, normalized):
        return VoiceReplyIntentResult("new_question", 0.88, "Looks like a new question", "fast_path")

    token_count = len(normalized.split())
    if token_count <= max(1, max_grant_tokens) and any(
        phrase_in_text(phrase, normalized) for phrase in POSITIVE_SHORT_REPLIES
    ):
        return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")

    return None
