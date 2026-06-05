import pytest

from app.core.config import settings
from app.services import rag_service


@pytest.mark.asyncio
async def test_search_book_knowledge_uses_legacy_when_canonical_disabled(monkeypatch):
    async def fake_legacy(query: str, document_ids: list[str]):
        return [{"source": "legacy", "content": "legacy content"}]

    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return [{"source": "canonical", "content": "canonical content"}]

    monkeypatch.setattr(settings, "AGENT_CANONICAL_SECTION_RAG_ENABLED", False)
    monkeypatch.setattr(rag_service, "search_learning_unit_knowledge", fake_legacy)
    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "legacy", "content": "legacy content"}]


@pytest.mark.asyncio
async def test_search_book_knowledge_prefers_canonical_when_enabled(monkeypatch):
    async def fake_legacy(query: str, document_ids: list[str]):
        return [{"source": "legacy", "content": "legacy content"}]

    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return [{"source": "canonical", "section_id": "section-1", "content": "canonical content"}]

    monkeypatch.setattr(settings, "AGENT_CANONICAL_SECTION_RAG_ENABLED", True)
    monkeypatch.setattr(settings, "AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY", True)
    monkeypatch.setattr(rag_service, "search_learning_unit_knowledge", fake_legacy)
    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "canonical", "section_id": "section-1", "content": "canonical content"}]


@pytest.mark.asyncio
async def test_search_book_knowledge_falls_back_to_legacy_when_canonical_empty(monkeypatch):
    async def fake_legacy(query: str, document_ids: list[str]):
        return [{"source": "legacy", "content": "legacy content"}]

    async def fake_canonical(query: str, document_ids: list[str], *, section_ids=None):
        return rag_service.BOOK_CONTEXT_NOT_FOUND_MESSAGE

    monkeypatch.setattr(settings, "AGENT_CANONICAL_SECTION_RAG_ENABLED", True)
    monkeypatch.setattr(settings, "AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY", True)
    monkeypatch.setattr(rag_service, "search_learning_unit_knowledge", fake_legacy)
    monkeypatch.setattr(rag_service, "search_book_section_knowledge", fake_canonical)

    result = await rag_service.search_book_knowledge("hỏi", ["book-1"])

    assert result == [{"source": "legacy", "content": "legacy content"}]
