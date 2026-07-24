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


def check_book_preflight_limits(flat_sections: list) -> tuple[bool, int, str | None]:
    """
    Ước tính nhanh tổng số từ và thời lượng Audio của toàn bộ sách từ flat_sections.

    Trả về:
        (is_valid, estimated_audio_seconds, error_message)
    """
    total_text = " ".join([getattr(sec, "content", None) or getattr(sec, "text", "") or "" for sec in flat_sections])
    words = len(total_text.split())
    if words == 0:
        return True, 0, None

    estimated_audio_seconds = estimate_audio_seconds(total_text)
    max_allowed_seconds = settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK

    if estimated_audio_seconds > max_allowed_seconds:
        est_hours = round(estimated_audio_seconds / 3600, 1)
        max_hours = max_allowed_seconds // 3600
        error_msg = (
            f"Tài liệu quá lớn ~ {est_hours} giờ audio toàn bộ sách, "
            f"vượt quá giới hạn tối đa {max_hours} giờ cho mỗi sách. "
            f"Vui lòng tải lên sách có dung lượng phù hợp."
        )
        return False, estimated_audio_seconds, error_msg

    return True, estimated_audio_seconds, None
