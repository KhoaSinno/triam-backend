from __future__ import annotations

import os
import torch
import asyncio
from typing import Any

from app.core.logger import log
from app.services.voice_agent.contracts import WebPermissionIntent, WebPermissionIntentResult
from app.services.voice_agent.voice_intent_classifier import (
    POSITIVE_ACTION_PHRASES,
    classify_voice_reply_intent_fast_path,
    normalize_voice_intent_text,
    looks_like_new_question,
)
# Re-use the singleton model loader from intent_router to avoid double RAM allocation
from app.services.agent_grounding.intent_router import _classifier, mean_pooling

# Expose normalize_intent_text for policy layer
normalize_intent_text = normalize_voice_intent_text

L12_WEB_PERMISSION_PROTOTYPES = {
    "grant": [
        "đồng ý cho tìm kiếm", "ừ tìm trên internet đi", "cho phép tra cứu google",
        "tìm giúp mình trên mạng", "search hộ mình thông tin này", "đồng ý nha",
        "được chứ tìm đi", "yes search it", "go ahead and search", "nhất trí tìm đi",
        "cho phép tìm", "bạn tìm đi", "tìm kiếm thông tin đi", "em đi", "ừm đi", "ý đi"
    ],
    "deny": [
        "không cần tìm đâu", "đừng tra cứu internet", "thôi khỏi cần",
        "bỏ qua đi bạn", "không muốn tìm trên web", "đừng tìm kiếm",
        "no don't search", "cancel web search", "thôi bỏ qua đi"
    ],
    "unclear": [
        "chưa biết nữa", "để tính sau đi", "tùy bạn thôi", "cái đó khó nói",
        "sao cũng được", "maybe later", "chưa chắc nữa", "để mình suy nghĩ tí"
    ]
}

_proto_embeddings: dict[str, torch.Tensor] = {}
_lock = asyncio.Lock()
_initialized = False

def _initialize_permission_prototypes() -> None:
    global _proto_embeddings, _initialized
    if _initialized:
        return
        
    # Ensure the intent router model is initialized
    _classifier.initialize()
    tokenizer = _classifier.tokenizer
    model = _classifier.model

    with torch.no_grad():
        for intent, phrases in L12_WEB_PERMISSION_PROTOTYPES.items():
            inputs = tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            embeddings = mean_pooling(outputs, inputs['attention_mask'])
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            _proto_embeddings[intent] = embeddings
            
    _initialized = True

async def _initialize_permission_prototypes_async() -> None:
    global _initialized
    if _initialized:
        return
    async with _lock:
        if not _initialized:
            # First ensure the intent router model is initialized async/sync
            await _classifier.initialize_async()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, _initialize_permission_prototypes)

async def pre_warm_permission_classifier() -> None:
    """
    [Clean Code & Best Practice]
    Khởi tạo pre-warm mô hình L12 ngầm lúc kết nối session.
    """
    try:
        log.info("Pre-warming Web Permission Classifier (L12 Embedding)...")
        await _initialize_permission_prototypes_async()
        log.info("Pre-warming Web Permission Classifier hoan tat!")
    except Exception as exc:
        log.warning(f"Pre-warming Web Permission Classifier gap loi: {exc}")

def classify_web_permission_intent_fast_path(user_reply: str) -> WebPermissionIntentResult | None:
    """
    [Clean Code Wrapper]
    Gọi Fast-Path từ voice_intent_classifier và chuyển đổi kết quả sang WebPermissionIntentResult.
    """
    voice_res = classify_voice_reply_intent_fast_path(user_reply, max_grant_tokens=6)
    if voice_res is None:
        return None
        
    return WebPermissionIntentResult(
        intent=voice_res.intent,  # type: ignore[arg-type]
        confidence=voice_res.confidence,
        reason=voice_res.reason,
        source="fast_path",
    )

def _compute_cosine_similarity_sync(
    user_reply: str,
    threshold: float,
) -> WebPermissionIntentResult:
    """
    Hàm tính toán Cosine Similarity đồng bộ (CPU-bound), chạy trong Executor Thread.
    """
    tokenizer = _classifier.tokenizer
    model_obj = _classifier.model

    if tokenizer is None or model_obj is None or not _proto_embeddings:
        return WebPermissionIntentResult(
            intent="unclear",
            confidence=0.0,
            reason="Model parameters or prototypes not loaded",
            source="local_embedding",
        )

    with torch.no_grad():
        inputs = tokenizer([user_reply.strip().lower()], padding=True, truncation=True, return_tensors="pt")
        outputs = model_obj(**inputs)
        query_emb = mean_pooling(outputs, inputs['attention_mask'])
        query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)

        best_intent: WebPermissionIntent = "unclear"
        best_score = -1.0

        # Thread Safety Fix: Snapshot dictionary để tránh RuntimeError khi iterate trong ThreadPool
        proto_snapshot = dict(_proto_embeddings)
        for intent, proto_embs in proto_snapshot.items():
            sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
            max_sim = torch.max(sims).item()
            if max_sim > best_score:
                best_score = max_sim
                best_intent = intent  # type: ignore[assignment]

        if best_score < threshold:
            log.info(f"Web permission cosine score {best_score:.2f} below threshold {threshold} | Fallback to new_question")
            return WebPermissionIntentResult(
                intent="new_question",
                confidence=best_score,
                reason="Below similarity threshold",
                source="local_embedding",
            )

        return WebPermissionIntentResult(
            intent=best_intent,
            confidence=best_score,
            reason="Classified by local L12 Cosine",
            source="local_embedding",
        )

async def classify_web_permission_intent(
    *,
    pending_query: str,
    user_reply: str,
    use_llm: bool | None = None, # Left for backward compatibility, unused
    model: str | None = None, # Left for backward compatibility, unused
    timeout_seconds: float | None = None, # Left for backward compatibility, unused
    confidence_threshold: float | None = None,
) -> WebPermissionIntentResult:
    """
    Classifies the user reply regarding web search permission using a local multilingual L12 model.
    Fully async & non-blocking execution via Thread Executor.
    """
    # 1. Run Fast-path Layer 1 (< 1ms)
    fast_result = classify_web_permission_intent_fast_path(user_reply)
    if fast_result is not None:
        return fast_result

    # 2. Run Local Embedding Cosine Similarity Layer 2
    normalized = normalize_voice_intent_text(user_reply)

    # Only treat as new_question if it does NOT contain any positive action phrase
    has_positive_phrase = any(phrase in normalized for phrase in POSITIVE_ACTION_PHRASES)
    if looks_like_new_question(user_reply, normalized) and not has_positive_phrase:
        return WebPermissionIntentResult(
            intent="new_question",
            confidence=1.0,
            reason="looks_like_new_question_without_positive_intent",
            source="local_embedding",
        )

    try:
        # Load prototypes asynchronously if not already pre-warmed
        await _initialize_permission_prototypes_async()
        
        resolved_threshold = confidence_threshold or 0.50
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            _compute_cosine_similarity_sync,
            user_reply,
            resolved_threshold,
        )
            
    except Exception as exc:
        log.error(f"Web permission local classifier failed: {exc} | Fallback to unclear")
        return WebPermissionIntentResult(
            intent="unclear",
            confidence=0.0,
            reason=f"Classifier error: {exc}",
            source="local_embedding",
        )
