from dataclasses import dataclass

import tiktoken

from app.core.constant import PlanMode
from app.core.config import settings


@dataclass(frozen=True)
class TextBudget:
    char_count: int
    estimated_tokens: int
    estimated_audio_seconds: int


_encoding = tiktoken.get_encoding("cl100k_base")

PARETO_SPEECH_COMPRESSION_RATIO = 0.20
FULL_SPEECH_COMPRESSION_RATIO = 0.80


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return len(_encoding.encode(text))


def estimate_audio_seconds(text: str, mode: PlanMode | str = PlanMode.FULL) -> int:
    """
    Standard audiobook & TTS narration speech estimate (~150 WPM / 2.5 words per second),
    factoring in LLM normalization speech compression ratios for Pareto vs Full mode.
    """
    words = len(text.split())
    if words == 0:
        return 0
    mode_str = mode.value if isinstance(mode, PlanMode) else str(mode)
    ratio = PARETO_SPEECH_COMPRESSION_RATIO if mode_str == "pareto" else FULL_SPEECH_COMPRESSION_RATIO
    estimated_words = words * ratio
    return max(10, int(estimated_words / 150 * 60))


def extract_unique_book_text(flat_sections: list) -> str:
    """
    Khử trùng lặp nội dung khi gom tổng văn bản của sách từ flat_sections:
    1. Nếu các section có `source_href` (file EPUB), deduplicate theo file HTML duy nhất.
    2. Ngược lại (PDF/DOCX), gom text từ các node lá (leaf nodes) hoặc các block text không trùng lặp.
    """
    seen_hrefs: set[str] = set()
    texts: list[str] = []

    has_href = any(getattr(sec, "source_href", None) for sec in flat_sections)

    if has_href:
        for sec in flat_sections:
            href = getattr(sec, "source_href", None)
            if href:
                if href not in seen_hrefs:
                    seen_hrefs.add(href)
                    t = (getattr(sec, "text", "") or getattr(sec, "content", "") or "").strip()
                    if t:
                        texts.append(t)
            else:
                if not getattr(sec, "children", None):
                    t = (getattr(sec, "text", "") or getattr(sec, "content", "") or "").strip()
                    if t:
                        texts.append(t)
    else:
        for sec in flat_sections:
            if not getattr(sec, "children", None):
                t = (getattr(sec, "text", "") or getattr(sec, "content", "") or "").strip()
                if t:
                    texts.append(t)
            elif (getattr(sec, "text", "") or getattr(sec, "content", "") or "").strip():
                child_texts = [(getattr(c, "text", "") or getattr(c, "content", "") or "").strip() for c in getattr(sec, "children", [])]
                if not any(child_texts):
                    texts.append((getattr(sec, "text", "") or getattr(sec, "content", "") or "").strip())

    return " ".join(texts)


def estimate_text_budget(text: str, mode: PlanMode | str = PlanMode.FULL) -> TextBudget:
    return TextBudget(
        char_count=len(text or ""),
        estimated_tokens=estimate_tokens(text),
        estimated_audio_seconds=estimate_audio_seconds(text, mode=mode),
    )


def exceeds_hard_limit(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_HARD_TOKEN_LIMIT


def should_chunk(text_budget: TextBudget) -> bool:
    return text_budget.estimated_tokens > settings.LLM_INPUT_SOFT_TOKEN_LIMIT


def check_book_preflight_limits(flat_sections: list, mode: PlanMode | str = PlanMode.FULL) -> tuple[bool, int, str | None]:
    """
    Ước tính nhanh tổng số từ và thời lượng Audio của toàn bộ sách từ flat_sections.

    Trả về:
        (is_valid, estimated_audio_seconds, error_message)
    """
    unique_text = extract_unique_book_text(flat_sections)
    words = len(unique_text.split())
    if words == 0:
        return True, 0, None

    estimated_audio_seconds = estimate_audio_seconds(unique_text, mode=mode)
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
