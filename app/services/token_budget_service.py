from dataclasses import dataclass

import tiktoken

from app.core.config import settings


@dataclass(frozen=True)
class TextBudget:
    char_count: int
    estimated_tokens: int
    estimated_audio_seconds: int


_encoding = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return len(_encoding.encode(text))


def estimate_audio_seconds(text: str) -> int:
    """
    Conservative Vietnamese speech estimate.

    130 words/minute avoids underestimating long audio generation cost.
    """
    words = len(text.split())
    if words == 0:
        return 0
    return int(words / 130 * 60)


def estimate_text_budget(text: str) -> TextBudget:
    return TextBudget(
        char_count=len(text or ""),
        estimated_tokens=estimate_tokens(text),
        estimated_audio_seconds=estimate_audio_seconds(text),
    )


def exceeds_hard_limit(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT


def should_chunk(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_SOFT_TOKEN_LIMIT
