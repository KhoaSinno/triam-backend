from __future__ import annotations

import asyncio
import json
from typing import Any

from openai import AsyncOpenAI

from app.core.logger import log
from app.services.voice_agent.contracts import WebPermissionIntent, WebPermissionIntentResult
from app.services.voice_agent.voice_intent_classifier import (
    classify_voice_reply_intent_fast_path,
    normalize_voice_intent_text,
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


normalize_intent_text = normalize_voice_intent_text


def classify_web_permission_intent_fast_path(user_reply: str) -> WebPermissionIntentResult | None:
    result = classify_voice_reply_intent_fast_path(user_reply)
    if result is None:
        return None
    return WebPermissionIntentResult(result.intent, result.confidence, result.reason, result.source)


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
