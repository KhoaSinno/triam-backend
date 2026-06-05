from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import log
from app.core.supabase import supabase

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

BOOK_CONTEXT_NOT_FOUND_MESSAGE = "Không tìm thấy thông tin cụ thể trong sách."
LEGACY_BOOK_KNOWLEDGE_EMBEDDING_MODEL = "text-embedding-3-small"


async def _embed_query(query: str, *, model: str) -> list[float]:
    res = await ai_client.embeddings.create(model=model, input=[query])
    query_vector = res.data[0].embedding
    return query_vector


async def search_learning_unit_knowledge(query: str, document_ids: list[str]) -> list[dict[str, Any]] | str:
    query_vector = await _embed_query(query, model=LEGACY_BOOK_KNOWLEDGE_EMBEDDING_MODEL)
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.3,
        "match_count": 10,
        "filter_book_ids": document_ids,
    }).execute()

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


async def search_book_section_knowledge(
    query: str,
    document_ids: list[str],
    *,
    section_ids: list[str] | None = None,
) -> list[dict[str, Any]] | str:
    query_vector = await _embed_query(query, model=settings.BOOK_SECTION_EMBEDDING_MODEL)
    result = supabase.rpc(
        "match_book_section_knowledge",
        {
            "query_embedding": query_vector,
            "match_threshold": settings.BOOK_SECTION_RAG_MATCH_THRESHOLD,
            "match_count": settings.BOOK_SECTION_RAG_MATCH_COUNT,
            "filter_book_ids": document_ids,
            "filter_section_ids": section_ids,
        },
    ).execute()

    if not result.data:
        return BOOK_CONTEXT_NOT_FOUND_MESSAGE

    return result.data


async def search_book_knowledge(query: str, document_ids: list[str]) -> list[dict[str, Any]] | str:
    if not settings.AGENT_CANONICAL_SECTION_RAG_ENABLED:
        return await search_learning_unit_knowledge(query, document_ids)

    canonical_result = await search_book_section_knowledge(query, document_ids)
    if isinstance(canonical_result, list) and canonical_result:
        return canonical_result

    if settings.AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY:
        log.info("Canonical section RAG returned no chunks; falling back to legacy learning-unit RAG.")
        return await search_learning_unit_knowledge(query, document_ids)

    return canonical_result
