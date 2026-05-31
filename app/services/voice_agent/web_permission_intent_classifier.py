from __future__ import annotations

import asyncio
import json
import re
import unicodedata
from typing import Any

from openai import AsyncOpenAI

from app.core.logger import log
from app.services.voice_agent.contracts import WebPermissionIntent, WebPermissionIntentResult

POSITIVE_ACTION_PHRASES = (
    "dong y",
    "tim di",
    "tim kiem di",
    "search di",
    "lam di",
    "cu lam",
    "cu tim",
    "thu xem",
    "go ahead",
    "do it",
    "search it",
)
POSITIVE_SHORT_REPLIES = (
    "co",
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
)
NEGATIVE_PHRASES = (
    "khong can",
    "khong dau",
    "khong",
    "khoi",
    "dung",
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
    "maybe",
    "up to you",
)
QUESTION_HINTS = (
    " la gi",
    " gi ",
    " nao",
    " tai sao",
    " vi sao",
    " nhu the nao",
    " the nao",
    " co nhung",
    " chuong",
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
    " tell me",
)

CLASSIFIER_SYSTEM_PROMPT = """
Classify whether the user is answering a web-search permission question.
Return only valid JSON:
{"intent":"grant|deny|unclear|new_question","confidence":0.0,"reason":"short"}

Rules:
- grant: user agrees to search the web for the pending query.
- deny: user refuses or asks to skip.
- unclear: ambiguous reply.
- new_question: user asks something else instead of answering.
- Support Vietnamese, English, and mixed replies.
""".strip()


def normalize_intent_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", (text or "").casefold())
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    without_marks = without_marks.replace("đ", "d")
    without_marks = re.sub(r"[^a-z0-9]+", " ", without_marks)
    return " ".join(without_marks.split())


def _phrase_in_text(phrase: str, text: str) -> bool:
    return f" {phrase} " in f" {text} "


def _looks_like_new_question(original_text: str, normalized_text: str) -> bool:
    if "?" in original_text:
        return True
    padded = f" {normalized_text} "
    return any(hint in padded for hint in QUESTION_HINTS)


def classify_web_permission_intent_fast_path(user_reply: str) -> WebPermissionIntentResult | None:
    normalized = normalize_intent_text(user_reply)
    if not normalized:
        return WebPermissionIntentResult("unclear", 1.0, "Empty reply", "fast_path")

    if any(_phrase_in_text(phrase, normalized) for phrase in NEGATIVE_PHRASES):
        return WebPermissionIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")

    if any(_phrase_in_text(phrase, normalized) for phrase in POSITIVE_ACTION_PHRASES):
        return WebPermissionIntentResult("grant", 0.96, "Matched positive action fast path", "fast_path")

    if any(_phrase_in_text(phrase, normalized) for phrase in AMBIGUOUS_PHRASES):
        return WebPermissionIntentResult("unclear", 0.88, "Matched ambiguous fast path", "fast_path")

    if _looks_like_new_question(user_reply, normalized):
        return WebPermissionIntentResult("new_question", 0.88, "Looks like a new question", "fast_path")

    token_count = len(normalized.split())
    if token_count <= 3 and any(_phrase_in_text(phrase, normalized) for phrase in POSITIVE_SHORT_REPLIES):
        return WebPermissionIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")

    return None


def _coerce_intent(value: Any) -> WebPermissionIntent:
    if value in {"grant", "deny", "unclear", "new_question"}:
        return value
    return "unclear"


def _coerce_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0
    return min(max(confidence, 0.0), 1.0)


async def _classify_with_openai(
    *,
    pending_query: str,
    user_reply: str,
    model: str,
    timeout_seconds: float,
) -> WebPermissionIntentResult:
    from app.core.config import settings

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    user_prompt = (
        f"Pending web query:\n{pending_query}\n\n"
        f"User reply:\n{user_reply}\n"
    )

    response = await asyncio.wait_for(
        client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        ),
        timeout=timeout_seconds,
    )
    content = response.choices[0].message.content or "{}"
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        log.info("Web permission classifier returned invalid JSON")
        return WebPermissionIntentResult("unclear", 0.0, "Invalid classifier JSON")

    return WebPermissionIntentResult(
        intent=_coerce_intent(payload.get("intent")),
        confidence=_coerce_confidence(payload.get("confidence")),
        reason=str(payload.get("reason") or "")[:160],
    )


async def classify_web_permission_intent(
    *,
    pending_query: str,
    user_reply: str,
    use_llm: bool | None = None,
    model: str | None = None,
    timeout_seconds: float | None = None,
    confidence_threshold: float | None = None,
) -> WebPermissionIntentResult:
    fast_path_result = classify_web_permission_intent_fast_path(user_reply)
    if fast_path_result is not None:
        return fast_path_result

    from app.core.config import settings

    llm_enabled = settings.VOICE_AGENT_PERMISSION_CLASSIFIER_ENABLED if use_llm is None else use_llm
    if not llm_enabled:
        return WebPermissionIntentResult("unclear", 0.0, "Classifier disabled")

    resolved_model = model or settings.VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL
    resolved_timeout = timeout_seconds or settings.VOICE_AGENT_PERMISSION_CLASSIFIER_TIMEOUT_SECONDS
    threshold = confidence_threshold or settings.VOICE_AGENT_PERMISSION_CLASSIFIER_CONFIDENCE_THRESHOLD

    try:
        result = await _classify_with_openai(
            pending_query=pending_query,
            user_reply=user_reply,
            model=resolved_model,
            timeout_seconds=resolved_timeout,
        )
    except Exception as exc:
        log.info(f"Web permission classifier failed: {type(exc).__name__}")
        return WebPermissionIntentResult("unclear", 0.0, "Classifier failed")

    if result.confidence < threshold:
        return WebPermissionIntentResult(
            "unclear",
            result.confidence,
            f"Low confidence: {result.reason}",
        )

    return result
