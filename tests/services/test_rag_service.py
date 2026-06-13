import pytest

from app.core.config import settings
from app.services import rag_service


@pytest.fixture(autouse=True)
def _disable_hybrid_by_default(monkeypatch):
    monkeypatch.setattr(settings, "AGENT_HYBRID_RAG_ENABLED", False)


@pytest.mark.asyncio
async def test_search_book_knowledge_uses_section_rag_when_hybrid_disabled(monkeypatch):
    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return [{"source": "canonical", "content": "canonical content"}]

    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "canonical", "content": "canonical content"}]


@pytest.mark.asyncio
async def test_search_book_knowledge_returns_not_found_without_legacy_fallback(monkeypatch):
    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return rag_service.BOOK_CONTEXT_NOT_FOUND_MESSAGE

    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == rag_service.BOOK_CONTEXT_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_search_book_knowledge_uses_hybrid_when_enabled(monkeypatch):
    async def fake_hybrid(query: str, document_ids: list[str]):
        return [{"source": "hybrid", "retrieval_method": "hybrid", "content": "hybrid content"}]

    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return [{"source": "canonical", "content": "canonical content"}]

    monkeypatch.setattr(settings, "AGENT_HYBRID_RAG_ENABLED", True)
    monkeypatch.setattr(rag_service, "search_book_hybrid_knowledge", fake_hybrid)
    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "hybrid", "retrieval_method": "hybrid", "content": "hybrid content"}]

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
