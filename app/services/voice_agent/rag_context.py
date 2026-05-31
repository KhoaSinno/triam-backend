from typing import Any, Awaitable, Callable

from app.core.config import settings
from app.services.rag_service import search_book_knowledge
from app.services.voice_agent.contracts import VoiceRagResult

RawRagSearch = Callable[[str, list[str]], Awaitable[Any]]


def trim_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return f"{text[:max_chars].rstrip()}\n...[truncated]"


def normalize_rag_payload(payload: Any) -> VoiceRagResult:
    if not isinstance(payload, list) or not payload:
        return VoiceRagResult(
            found=False,
            chunks=[],
            message="Không tìm thấy thông tin phù hợp trong sách.",
        )

    chunks = [item for item in payload if isinstance(item, dict)]
    if not chunks:
        return VoiceRagResult(
            found=False,
            chunks=[],
            message="Không tìm thấy thông tin phù hợp trong sách.",
        )

    return VoiceRagResult(found=True, chunks=chunks, message="")


async def search_voice_book_context(
    query: str,
    document_ids: list[str],
    *,
    search_fn: RawRagSearch = search_book_knowledge,
) -> VoiceRagResult:
    payload = await search_fn(query, document_ids)
    return normalize_rag_payload(payload)


def format_rag_context(result: VoiceRagResult, *, max_chars: int | None = None) -> str:
    if not result.found:
        return f"BOOK_CONTEXT_NOT_FOUND: {result.message}"

    remaining_chars = settings.VOICE_AGENT_RAG_MAX_CHARS if max_chars is None else max_chars
    formatted_chunks: list[str] = []
    for index, item in enumerate(result.chunks):
        if remaining_chars <= 0:
            break

        unit_id = str(item.get("learning_unit_id") or "")
        chunk_index = item.get("chunk_index", "N/A")
        content = trim_text(str(item.get("content", "")), remaining_chars)
        if not content:
            continue

        formatted_chunks.append(
            f"--- Segment {index + 1} (Unit ID: ...{unit_id[-6:]}, Index: {chunk_index}) ---\n{content}"
        )
        remaining_chars -= len(content)

    if not formatted_chunks:
        return f"BOOK_CONTEXT_NOT_FOUND: {result.message or 'Không tìm thấy thông tin phù hợp trong sách.'}"

    return "BOOK_CONTEXT_FOUND:\n" + "\n\n".join(formatted_chunks)

