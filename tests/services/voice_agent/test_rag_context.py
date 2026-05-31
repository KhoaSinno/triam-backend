import pytest

from app.services.voice_agent.rag_context import format_rag_context, search_voice_book_context


@pytest.mark.asyncio
async def test_search_voice_book_context_normalizes_empty_string_result():
    async def fake_search(query: str, document_ids: list[str]):
        return "Không tìm thấy thông tin cụ thể trong sách."

    result = await search_voice_book_context("câu hỏi", ["book-1"], search_fn=fake_search)

    assert result.found is False
    assert result.chunks == []
    assert "Không tìm thấy" in result.message
    assert format_rag_context(result).startswith("BOOK_CONTEXT_NOT_FOUND")


@pytest.mark.asyncio
async def test_search_voice_book_context_formats_list_result():
    async def fake_search(query: str, document_ids: list[str]):
        return [
            {
                "learning_unit_id": "12345678-1234-1234-1234-abcdef123456",
                "chunk_index": 2,
                "content": "Nội dung quan trọng trong sách.",
            }
        ]

    result = await search_voice_book_context("câu hỏi", ["book-1"], search_fn=fake_search)
    context = format_rag_context(result, max_chars=1000)

    assert result.found is True
    assert len(result.chunks) == 1
    assert context.startswith("BOOK_CONTEXT_FOUND")
    assert "Nội dung quan trọng" in context
    assert "abcdef123456"[-6:] in context

