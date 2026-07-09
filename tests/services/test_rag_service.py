import pytest

from app.services import rag_service


@pytest.mark.asyncio
async def test_search_book_knowledge_uses_hybrid_rag(monkeypatch):
    """search_book_knowledge luôn gọi hybrid pipeline."""
    async def fake_hybrid(query: str, document_ids: list[str]):
        return [{"source": "hybrid", "retrieval_method": "hybrid", "content": "hybrid content"}]

    monkeypatch.setattr(rag_service, "search_book_hybrid_knowledge", fake_hybrid)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "hybrid", "retrieval_method": "hybrid", "content": "hybrid content"}]


@pytest.mark.asyncio
async def test_search_book_knowledge_returns_not_found_when_hybrid_finds_nothing(monkeypatch):
    """search_book_knowledge trả về thông báo không tìm thấy khi hybrid không có kết quả."""
    async def fake_hybrid(query: str, document_ids: list[str]):
        return rag_service.BOOK_CONTEXT_NOT_FOUND_MESSAGE

    monkeypatch.setattr(rag_service, "search_book_hybrid_knowledge", fake_hybrid)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == rag_service.BOOK_CONTEXT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_search_book_section_knowledge_lexical_calls_rpc_with_normalized_query(monkeypatch):
    captured: dict = {}

    class FakeRpcResult:
        data = [{"id": 1, "lexical_score": 0.5, "content": "Crooks"}]

        def execute(self):
            return self

    class FakeSupabase:
        def rpc(self, name: str, payload: dict):
            captured["name"] = name
            captured["payload"] = payload
            return FakeRpcResult()

    monkeypatch.setattr(rag_service, "supabase", FakeSupabase())

    result = await rag_service.search_book_section_knowledge_lexical(
        "Crooks ở chương nào?",
        ["11111111-1111-1111-1111-111111111111"],
    )

    assert result == [{"id": 1, "lexical_score": 0.5, "content": "Crooks"}]
    assert captured["name"] == "match_book_section_knowledge_lexical"
    assert captured["payload"]["normalized_query_text"] == "crooks o chuong nao"


@pytest.mark.asyncio
async def test_search_book_section_knowledge_lexical_normalizes_empty_section_filter(monkeypatch):
    captured: dict = {}

    class FakeRpcResult:
        data = [{"id": 1, "lexical_score": 0.5, "content": "Crooks"}]

        def execute(self):
            return self

    class FakeSupabase:
        def rpc(self, name: str, payload: dict):
            captured["payload"] = payload
            return FakeRpcResult()

    monkeypatch.setattr(rag_service, "supabase", FakeSupabase())

    await rag_service.search_book_section_knowledge_lexical(
        "Crooks",
        ["11111111-1111-1111-1111-111111111111"],
        section_ids=[],
    )

    assert captured["payload"]["filter_section_ids"] is None
