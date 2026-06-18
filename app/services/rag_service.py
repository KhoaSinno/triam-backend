import asyncio
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import log
from app.core.supabase import supabase
from app.services.agent_grounding.hybrid_retrieval import (
    HybridRetrievalConfig,
    build_hybrid_retrieval_result,
)
from app.services.agent_grounding.query_normalizer import normalized_key

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

BOOK_CONTEXT_NOT_FOUND_MESSAGE = "Không tìm thấy thông tin cụ thể trong sách."


def _execute_supabase_rpc(name: str, payload: dict[str, Any]):
    return supabase.rpc(name, payload).execute()


def _normalize_section_ids(section_ids: list[str] | None) -> list[str] | None:
    if not section_ids:
        return None
    return section_ids


def _round_score(value: float | int | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)


async def _embed_query(query: str, *, model: str) -> list[float]:
    res = await ai_client.embeddings.create(model=model, input=[query])
    query_vector = res.data[0].embedding
    return query_vector


async def search_book_section_knowledge(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
    match_count: int | None = None,
) -> list[dict[str, Any]] | str:
    query_vector = await _embed_query(query, model=settings.BOOK_SECTION_EMBEDDING_MODEL)
    result = await asyncio.to_thread(
        _execute_supabase_rpc,
        "match_book_section_knowledge",
        {
            "query_embedding": query_vector,
            "match_threshold": settings.BOOK_SECTION_RAG_MATCH_THRESHOLD,
            "match_count": match_count or settings.BOOK_SECTION_RAG_MATCH_COUNT,
            "filter_book_ids": document_ids,
            "filter_section_ids": _normalize_section_ids(section_ids),
        },
    )

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


async def search_book_section_knowledge_lexical(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
    match_count: int | None = None,
) -> list[dict[str, Any]] | str:
    result = await asyncio.to_thread(
        _execute_supabase_rpc,
        "match_book_section_knowledge_lexical",
        {
            "query_text": query,
            "normalized_query_text": normalized_key(query),
            "match_count": match_count or settings.AGENT_HYBRID_LEXICAL_CANDIDATES,
            "filter_book_ids": document_ids,
            "filter_section_ids": _normalize_section_ids(section_ids),
        },
    )

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


def _as_payload_list(payload: list[dict[str, Any]] | str) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def _hybrid_config() -> HybridRetrievalConfig:
    return HybridRetrievalConfig(
        vector_weight=settings.AGENT_HYBRID_VECTOR_WEIGHT,
        lexical_weight=settings.AGENT_HYBRID_LEXICAL_WEIGHT,
        title_match_boost=settings.AGENT_HYBRID_TITLE_MATCH_BOOST,
        multi_source_boost=settings.AGENT_HYBRID_MULTI_SOURCE_BOOST,
        min_final_score=settings.AGENT_HYBRID_MIN_FINAL_SCORE,
        max_context_chunks=settings.AGENT_HYBRID_MAX_CONTEXT_CHUNKS,
        max_chunks_per_section=settings.AGENT_HYBRID_MAX_CHUNKS_PER_SECTION,
    )


async def search_book_hybrid_knowledge(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
) -> list[dict[str, Any]] | str:

    vector_task = search_book_section_knowledge(
        query,
        document_ids,
        section_ids=section_ids,
        match_count=settings.AGENT_HYBRID_VECTOR_CANDIDATES,
    )
    lexical_task = search_book_section_knowledge_lexical(
        query,
        document_ids,
        section_ids=section_ids,
        match_count=settings.AGENT_HYBRID_LEXICAL_CANDIDATES,
    )

    vector_result, lexical_result = await asyncio.gather(vector_task, lexical_task, return_exceptions=True)

    if isinstance(vector_result, Exception):
        log.error(f"RAG Tối ưu hóa: Nhánh Vector Search bị lỗi: {vector_result}")
        vector_result = BOOK_CONTEXT_NOT_FOUND_MESSAGE

    if isinstance(lexical_result, Exception):
        log.error(f"RAG Tối ưu hóa: Nhánh Lexical Search bị lỗi: {lexical_result}")
        lexical_result = BOOK_CONTEXT_NOT_FOUND_MESSAGE

    hybrid_result = build_hybrid_retrieval_result(
        query=query,
        vector_payload=_as_payload_list(vector_result),
        lexical_payload=_as_payload_list(lexical_result),
        config=_hybrid_config(),
    )
    log.info(
        "Hybrid section RAG done | "
        f"found={hybrid_result.found} | "
        f"reason={hybrid_result.reason_code} | "
        f"candidates={hybrid_result.candidate_count} | "
        f"chunks={len(hybrid_result.chunks)} | "
        f"top_id={hybrid_result.top_candidate_id} | "
        f"top_vector={_round_score(hybrid_result.top_vector_score)} | "
        f"top_lexical={_round_score(hybrid_result.top_lexical_score)} | "
        f"top_final={_round_score(hybrid_result.top_final_score)} | "
        f"missing_token_count={hybrid_result.missing_token_count}"
    )
    if not hybrid_result.found:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE
    return hybrid_result.chunks


async def search_book_knowledge(query: str, document_ids: list[str]) -> list[dict[str, Any]] | str:
    if settings.AGENT_HYBRID_RAG_ENABLED:
        return await search_book_hybrid_knowledge(query, document_ids)

    return await search_book_section_knowledge(query, document_ids)
