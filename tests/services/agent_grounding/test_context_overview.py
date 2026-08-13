import uuid

import pytest

from app.services.agent_grounding import grounding_router
from app.services.agent_grounding.context_overview import build_context_overview, render_context_overview_answer
from app.services.agent_grounding.contracts import GroundingBook, GroundingIntent, GroundingRoute, GroundingScope
from app.services.agent_grounding.grounding_router import GroundingRouter

BOOK_A_ID = uuid.UUID("10000000-0000-0000-0000-000000000001")
BOOK_B_ID = uuid.UUID("10000000-0000-0000-0000-000000000002")
BOOK_C_ID = uuid.UUID("10000000-0000-0000-0000-000000000003")


def _scope() -> GroundingScope:
    books = (
        GroundingBook(BOOK_A_ID, "Of Mice and Men", "John Steinbeck", "pdf", 6, "ready", 6),
        GroundingBook(BOOK_B_ID, "The Great Gatsby", "F. Scott Fitzgerald", "epub", 9, "processing", 5),
        GroundingBook(BOOK_C_ID, "Animal Farm", None, None, 4, "draft", 4),
    )
    return GroundingScope(tuple(book.id for book in books), books, ())


def test_context_overview_renders_full_count_and_bounded_list() -> None:
    overview = build_context_overview(_scope(), max_visible_documents=2)

    assert render_context_overview_answer(overview, GroundingIntent.CONTEXT_DOCUMENT_COUNT) == (
        'Ngữ cảnh học tập hiện tại có 3 tài liệu: "Of Mice and Men" — John Steinbeck; '
        '"The Great Gatsby" — F. Scott Fitzgerald. Còn 1 tài liệu khác.'
    )
    assert render_context_overview_answer(overview, GroundingIntent.CONTEXT_DOCUMENT_LIST) == (
        'Ngữ cảnh học tập hiện tại có 3 tài liệu: "Of Mice and Men" — John Steinbeck; "The Great Gatsby" — F. Scott Fitzgerald. Còn 1 tài liệu khác.'
    )


@pytest.mark.asyncio
async def test_context_count_uses_every_book_in_scope_without_rag(monkeypatch) -> None:
    async def classify_context_count(_query):
        return GroundingIntent.CONTEXT_DOCUMENT_COUNT

    calls = 0

    async def loader(*_args):
        nonlocal calls
        calls += 1
        return ()

    monkeypatch.setattr(grounding_router, "classify_intent", classify_context_count)
    result = await GroundingRouter(
        _scope(),
        loader,
        section_context_max_chars=4000,
        context_overview_enabled=True,
    ).resolve("Có bao nhiêu tài liệu trong ngữ cảnh hiện tại?")

    assert result.decision.route == GroundingRoute.CONTEXT_OVERVIEW
    assert result.decision.resolved_book_ids == (BOOK_A_ID, BOOK_B_ID, BOOK_C_ID)
    assert result.deterministic_answer == (
        'Ngữ cảnh học tập hiện tại có 3 tài liệu: "Of Mice and Men" — John Steinbeck; '
        '"The Great Gatsby" — F. Scott Fitzgerald; "Animal Farm".'
    )
    assert calls == 0


@pytest.mark.asyncio
async def test_context_route_is_not_enabled_until_flag_is_on(monkeypatch) -> None:
    async def classify_context_count(_query):
        return GroundingIntent.CONTEXT_DOCUMENT_COUNT

    monkeypatch.setattr(grounding_router, "classify_intent", classify_context_count)
    result = await GroundingRouter(_scope(), _unused_loader, section_context_max_chars=4000).resolve("Có bao nhiêu tài liệu trong ngữ cảnh hiện tại?")

    assert result.decision.route == GroundingRoute.BOOK_RAG
    assert result.decision.intent == GroundingIntent.BOOK_SEMANTIC_QUESTION


async def _unused_loader(*_args):  # pragma: no cover - the context route must not load sections
    raise AssertionError("section loader must not be called")
