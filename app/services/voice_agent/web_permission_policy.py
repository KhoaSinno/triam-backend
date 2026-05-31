from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from app.services.voice_agent.contracts import WebSearchPermissionDecision, WebSearchPermissionState

YES_PATTERNS = (
    "có",
    "co",
    "đồng ý",
    "dong y",
    "ok",
    "oke",
    "okay",
    "được",
    "duoc",
    "tìm đi",
    "tim di",
    "search đi",
    "search di",
    "tìm kiếm đi",
    "tim kiem di",
)
NO_PATTERNS = (
    "không",
    "khong",
    "khỏi",
    "khoi",
    "đừng",
    "dung",
    "không cần",
    "khong can",
    "thôi",
    "thoi",
)


def _normalize_text(text: str) -> str:
    return " ".join((text or "").casefold().split())


def _word_set(text: str) -> set[str]:
    return {word for word in re.split(r"\W+", _normalize_text(text)) if len(word) >= 2}


def _looks_like_yes(text: str) -> bool:
    normalized = _normalize_text(text)
    return any(pattern in normalized for pattern in YES_PATTERNS)


def _looks_like_no(text: str) -> bool:
    normalized = _normalize_text(text)
    return any(pattern in normalized for pattern in NO_PATTERNS)


def _query_matches(granted_query: str, query: str) -> bool:
    left = _normalize_text(granted_query)
    right = _normalize_text(query)
    if not left or not right:
        return False
    if left in right or right in left:
        return True

    left_words = _word_set(left)
    right_words = _word_set(right)
    if not left_words or not right_words:
        return False

    overlap = len(left_words & right_words)
    return overlap / max(min(len(left_words), len(right_words)), 1) >= 0.5


class WebSearchPermissionPolicy:
    def __init__(self, *, enabled: bool = False, grant_ttl_seconds: int = 180) -> None:
        self.state = WebSearchPermissionState(enabled=enabled)
        self._grant_ttl = timedelta(seconds=max(grant_ttl_seconds, 1))

    @property
    def enabled(self) -> bool:
        return self.state.enabled

    def set_enabled(self, enabled: bool) -> None:
        self.state.enabled = enabled
        if not enabled:
            self.clear()

    def clear(self) -> None:
        self.state.pending_query = None
        self.state.granted_query = None
        self.state.granted_at = None

    def request_permission(self, query: str) -> str:
        normalized_query = " ".join(query.split())
        if not self.state.enabled:
            self.clear()
            return "Thông tin này không có trong sách. Tính năng tìm kiếm internet hiện đang tắt."

        self.state.pending_query = normalized_query
        self.state.granted_query = None
        self.state.granted_at = None
        return f"Thông tin về '{normalized_query}' không có trong sách. Bạn có muốn tôi tìm kiếm thêm trên internet không?"

    def observe_user_reply(self, text: str) -> WebSearchPermissionDecision:
        if not self.state.pending_query:
            return WebSearchPermissionDecision()

        if _looks_like_no(text):
            self.clear()
            return WebSearchPermissionDecision(denied=True)

        if _looks_like_yes(text):
            granted_query = self.state.pending_query
            self.state.pending_query = None
            self.state.granted_query = granted_query
            self.state.granted_at = datetime.now(timezone.utc)
            return WebSearchPermissionDecision(granted_query=granted_query)

        return WebSearchPermissionDecision()

    def can_execute(self, query: str) -> tuple[bool, str]:
        if not self.state.enabled:
            return False, "Tính năng tìm kiếm internet hiện đang tắt."

        if not self.state.granted_query or not self.state.granted_at:
            return False, "WEB_SEARCH_PERMISSION_REQUIRED: Hãy xin phép user trước khi tìm kiếm internet."

        if datetime.now(timezone.utc) - self.state.granted_at > self._grant_ttl:
            self.clear()
            return False, "WEB_SEARCH_PERMISSION_EXPIRED: Quyền tìm kiếm đã hết hạn. Hãy xin phép lại."

        if not _query_matches(self.state.granted_query, query):
            return False, "WEB_SEARCH_PERMISSION_QUERY_MISMATCH: Query khác với nội dung user đã đồng ý."

        return True, ""

    def mark_search_consumed(self) -> None:
        self.state.granted_query = None
        self.state.granted_at = None

