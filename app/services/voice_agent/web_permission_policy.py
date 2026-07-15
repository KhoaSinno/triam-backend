from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone

from app.core.logger import log
from app.services.voice_agent.contracts import (
    WebPermissionIntentResult,
    WebSearchPermissionDecision,
    WebSearchPermissionState,
)
from app.services.voice_agent.web_permission_intent_classifier import (
    classify_web_permission_intent,
    normalize_intent_text,
)

IntentClassifier = Callable[..., Awaitable[WebPermissionIntentResult]]


def _normalize_query(text: str) -> str:
    return " ".join((text or "").split())


def _word_set(text: str) -> set[str]:
    return {word for word in normalize_intent_text(text).split() if len(word) >= 2}


def _query_matches(granted_query: str, query: str) -> bool:
    left = normalize_intent_text(granted_query)
    right = normalize_intent_text(query)
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
    def __init__(
        self,
        *,
        enabled: bool = False,
        grant_ttl_seconds: int = 180,
        implicit_grant_window_seconds: int = 20,
        intent_classifier: IntentClassifier | None = None,
    ) -> None:
        self.state = WebSearchPermissionState(enabled=enabled)
        self._grant_ttl = timedelta(seconds=max(grant_ttl_seconds, 1))
        self._implicit_grant_window = timedelta(seconds=max(implicit_grant_window_seconds, 1))
        self._intent_classifier = intent_classifier or classify_web_permission_intent

    @property
    def enabled(self) -> bool:
        return self.state.enabled

    @property
    def has_pending_permission(self) -> bool:
        return bool(self.state.pending_query)

    def set_enabled(self, enabled: bool) -> None:
        self.state.enabled = enabled
        if not enabled:
            self.clear()

    def clear(self) -> None:
        self.state.pending_query = None
        self.state.pending_request_id = None
        self.state.last_user_reply = None
        self.state.last_user_reply_at = None
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None

    def request_permission(self, query: str) -> str:
        normalized_query = _normalize_query(query)
        if not self.state.enabled:
            self.clear()
            return "Thông tin này không có trong sách. Tính năng tìm kiếm internet hiện đang tắt."

        self.state.pending_query = normalized_query
        self.state.pending_request_id = str(uuid.uuid4())
        self.state.last_user_reply = None
        self.state.last_user_reply_at = None
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None
        log.info(
            "Voice web permission requested | "
            f"request_id={self.state.pending_request_id} | query_chars={len(normalized_query)}"
        )
        return f"Thông tin về '{normalized_query}' không có trong sách. Bạn có muốn tôi tìm kiếm thêm trên internet không?"

    def record_user_reply(self, text: str) -> None:
        normalized_reply = _normalize_query(text)
        if normalized_reply:
            self.state.last_user_reply = normalized_reply
            self.state.last_user_reply_at = datetime.now(timezone.utc)

    def _last_reply_is_recent(self) -> bool:
        if not self.state.last_user_reply or not self.state.last_user_reply_at:
            return False
        return datetime.now(timezone.utc) - self.state.last_user_reply_at <= self._implicit_grant_window

    async def _classify_reply(
        self,
        *,
        pending_query: str,
        user_reply: str,
        request_id: str | None,
        implicit: bool = False,
    ) -> WebPermissionIntentResult:
        result = await self._intent_classifier(
            pending_query=pending_query,
            user_reply=user_reply,
        )
        mode = "implicit" if implicit else "pending"
        log.info(
            "Voice web permission intent classified | "
            f"mode={mode} | request_id={request_id} | intent={result.intent} | "
            f"confidence={result.confidence:.2f} | source={result.source}"
        )
        return result

    async def observe_user_reply(self, text: str) -> WebSearchPermissionDecision:
        self.record_user_reply(text)
        return await self.resolve_pending_reply()

    async def resolve_pending_reply(self) -> WebSearchPermissionDecision:
        if not self.state.pending_query or not self.state.last_user_reply:
            return WebSearchPermissionDecision()

        pending_query = self.state.pending_query
        request_id = self.state.pending_request_id
        user_reply = self.state.last_user_reply
        result = await self._classify_reply(
            pending_query=pending_query,
            user_reply=user_reply,
            request_id=request_id,
        )

        if result.intent == "grant":
            self.state.pending_query = None
            self.state.pending_request_id = None
            self.state.last_user_reply = None
            self.state.last_user_reply_at = None
            self.state.granted_query = pending_query
            self.state.granted_request_id = request_id
            self.state.granted_at = datetime.now(timezone.utc)
            return WebSearchPermissionDecision(granted_query=pending_query)

        if result.intent == "deny":
            self.clear()
            return WebSearchPermissionDecision(denied=True)

        if result.intent == "new_question":
            self.clear()
            return WebSearchPermissionDecision(new_question=user_reply)

        return WebSearchPermissionDecision(unclear=True)

    def pre_grant_for_eval(self) -> None:
        self.state.granted_query = "eval_pre_granted"
        self.state.granted_at = datetime.now(timezone.utc)

    def can_execute(self, query: str) -> tuple[bool, str]:
        if not self.state.enabled:
            return False, "Tính năng tìm kiếm internet hiện đang tắt."

        if not self.state.granted_query or not self.state.granted_at:
            return False, "WEB_SEARCH_PERMISSION_REQUIRED: Hãy xin phép user trước khi tìm kiếm internet."

        if self.state.granted_query == "eval_pre_granted":
            return True, ""

        if datetime.now(timezone.utc) - self.state.granted_at > self._grant_ttl:
            self.clear()
            return False, "WEB_SEARCH_PERMISSION_EXPIRED: Quyền tìm kiếm đã hết hạn. Hãy xin phép lại."

        if not _query_matches(self.state.granted_query, query):
            return False, "WEB_SEARCH_PERMISSION_QUERY_MISMATCH: Query khác với nội dung user đã đồng ý."

        return True, ""

    async def _resolve_pending_before_search(self, query: str) -> tuple[bool, str]:
        decision = await self.resolve_pending_reply()
        if decision.granted_query:
            return self.can_execute(query)
        if decision.denied:
            return False, "WEB_SEARCH_PERMISSION_DENIED: User đã từ chối tìm kiếm internet."
        if decision.unclear:
            return False, "WEB_SEARCH_PERMISSION_UNCLEAR: Hãy hỏi lại user để xác nhận rõ hơn."
        if decision.new_question:
            return False, "WEB_SEARCH_PERMISSION_NEW_QUESTION: User đã hỏi câu mới thay vì xác nhận."
        return False, "WEB_SEARCH_PERMISSION_REQUIRED: Hãy xin phép user trước khi tìm kiếm internet."

    async def _resolve_implicit_before_search(self, query: str) -> tuple[bool, str]:
        result = await self._classify_reply(
            pending_query=query,
            user_reply=self.state.last_user_reply or "",
            request_id=None,
            implicit=True,
        )
        if result.intent == "grant":
            self.state.last_user_reply = None
            self.state.last_user_reply_at = None
            self.state.granted_query = _normalize_query(query)
            self.state.granted_request_id = None
            self.state.granted_at = datetime.now(timezone.utc)
            return self.can_execute(query)
        if result.intent == "deny":
            self.clear()
            return False, "WEB_SEARCH_PERMISSION_DENIED: User đã từ chối tìm kiếm internet."
        if result.intent == "unclear":
            return False, "WEB_SEARCH_PERMISSION_UNCLEAR: Hãy hỏi lại user để xác nhận rõ hơn."
        return False, "WEB_SEARCH_PERMISSION_NEW_QUESTION: User đã hỏi câu mới thay vì xác nhận."

    def _can_try_implicit_grant(self, reason: str) -> bool:
        return (
            reason.startswith("WEB_SEARCH_PERMISSION_REQUIRED")
            and not self.state.pending_query
            and bool(self.state.last_user_reply)
            and self._last_reply_is_recent()
        )

    async def resolve_before_web_search(self, query: str) -> tuple[bool, str]:
        allowed, reason = self.can_execute(query)
        if allowed:
            return True, ""

        if (
            reason.startswith("WEB_SEARCH_PERMISSION_REQUIRED")
            and self.state.pending_query
            and self.state.last_user_reply
        ):
            return await self._resolve_pending_before_search(query)

        if self._can_try_implicit_grant(reason):
            return await self._resolve_implicit_before_search(query)

        return False, reason

    def mark_search_consumed(self) -> None:
        self.state.granted_query = None
        self.state.granted_request_id = None
        self.state.granted_at = None
