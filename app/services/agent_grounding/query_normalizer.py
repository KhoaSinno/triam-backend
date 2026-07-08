from __future__ import annotations

import re
import unicodedata

from app.services.agent_grounding.contracts import NormalizedQuery

TOKEN_PATTERN = re.compile(r"\d+(?:\.\d+)+|[^\W_]+|\d+", re.UNICODE)
WHITESPACE_PATTERN = re.compile(r"\s+")


def fold_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(character for character in decomposed if not unicodedata.combining(character))
# EX: "Ví dụ" => "Vi du"

def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "").strip().casefold()
    return WHITESPACE_PATTERN.sub(" ", normalized)
# EX: " hOÀnG   vŨ ß " => "hoàng vũ ss"


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(TOKEN_PATTERN.findall(text))
# EX: "hoang vu dep trai" => ("hoang", "vu", "dep", "trai")

def normalize_query(text: str) -> NormalizedQuery:
    original = (text or "").strip()
    normalized = normalize_text(original)
    accent_folded = fold_accents(normalized)
    return NormalizedQuery(
        original=original, # Origine
        normalized=normalized, # Chuẩn hóa, Khớp từ có dấu
        accent_folded=accent_folded, # Khớp không dấu
        tokens=tokenize(accent_folded), # Từng từ, độc lập từ => Full text search
    )


def normalized_key(text: str) -> str:
    return " ".join(tokenize(fold_accents(normalize_text(text))))


def _contains_token_sequence(tokens: tuple[str, ...], phrase_tokens: tuple[str, ...]) -> bool:
    if not phrase_tokens or len(phrase_tokens) > len(tokens):
        return False
    width = len(phrase_tokens)
    return any(tokens[index : index + width] == phrase_tokens for index in range(len(tokens) - width + 1))


def contains_phrase(query: NormalizedQuery, phrase: str) -> bool:
    return _contains_token_sequence(query.tokens, tokenize(fold_accents(normalize_text(phrase))))


def contains_any_phrase(query: NormalizedQuery, phrases: tuple[str, ...] | list[str] | set[str]) -> bool:
    return any(contains_phrase(query, phrase) for phrase in phrases)

