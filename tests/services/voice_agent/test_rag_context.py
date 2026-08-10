import pytest

from app.services.agent_observability import AgentInputMode, AgentTurnTracer
from app.services.voice_agent.contracts import VoiceRagResult
from app.services.voice_agent.rag_context import format_rag_context, render_rag_context, search_voice_book_context


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


@pytest.mark.asyncio
async def test_search_voice_book_context_records_safe_retrieval_trace():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    async def fake_search(query: str, document_ids: list[str]):
        return [
            {
                "id": 9,
                "learning_unit_id": "unit-1",
                "similarity": 0.75,
                "content": "private source content",
            }
        ]

    result = await search_voice_book_context(
        "câu hỏi",
        ["book-1"],
        search_fn=fake_search,
        tracer=tracer,
        input_mode=AgentInputMode.TEXT,
    )

    retrieval_payload = next(payload for event, payload in emitted if event == "retrieval_completed")
    assert result.found is True
    assert retrieval_payload["retrieval_chunk_ids"] == ["9"]
    assert retrieval_payload["retrieval_scores"] == [0.75]
    assert "private source content" not in str(retrieval_payload)


def test_format_rag_context_prefers_section_source_when_available():
    result = VoiceRagResult(
        found=True,
        chunks=[
            {
                "section_id": "11111111-1111-1111-1111-abcdef654321",
                "section_path": "Chương 4 > Crooks",
                "chunk_index": 0,
                "content": "Crooks sống một mình trong phòng của mình.",
            }
        ],
        message="",
    )

    context = format_rag_context(result, max_chars=1000)

    assert "BOOK_CONTEXT_FOUND" in context
    assert "Section: Chương 4 > Crooks" in context
    assert "abcdef654321"[-6:] in context
    assert "Crooks sống một mình" in context


def test_render_rag_context_reports_only_selected_content_metrics():
    result = VoiceRagResult(
        found=True,
        chunks=[
            {"learning_unit_id": "unit-1", "chunk_index": 0, "content": "abc"},
            {"learning_unit_id": "unit-2", "chunk_index": 1, "content": "defgh"},
        ],
        message="",
    )

    rendered = render_rag_context(result, max_chars=6)

    assert rendered.selected_count == 2
    # The existing formatter appends its visible truncation marker to the last chunk.
    # Phase 30.0 measures the actual context sent to the model, including that marker.
    assert rendered.content_char_count == len("abc") + len("def\n...[truncated]")
    assert rendered.text.startswith("BOOK_CONTEXT_FOUND")


@pytest.mark.asyncio
async def test_search_voice_book_context_records_hybrid_retrieval_method():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    async def fake_search(query: str, document_ids: list[str]):
        return [
            {
                "id": 10,
                "section_id": "section-1",
                "similarity": 0.82,
                "retrieval_method": "hybrid",
                "content": "private source content",
            }
        ]

    await search_voice_book_context(
        "câu hỏi",
        ["book-1"],
        search_fn=fake_search,
        tracer=tracer,
        input_mode=AgentInputMode.TEXT,
    )

    retrieval_payload = next(payload for event, payload in emitted if event == "retrieval_completed")
    assert retrieval_payload["retrieval_method"] == "hybrid"

