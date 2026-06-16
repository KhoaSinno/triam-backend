import uuid

import pytest

from app.services.agent_grounding.contracts import (
    GroundingBook,
    GroundingIntent,
    GroundingRoute,
    GroundingScope,
    GroundingSection,
    GroundingSectionText,
)
from app.services.agent_grounding.grounding_router import GroundingRouter
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer

BOOK_ID = uuid.UUID("10000000-0000-0000-0000-000000000001")
SECTION_ID = uuid.UUID("20000000-0000-0000-0000-000000000004")


def _scope() -> GroundingScope:
    book = GroundingBook(BOOK_ID, "Of Mice and Men", "John Steinbeck", "pdf", 6, "ready", 6)
    section = GroundingSection(SECTION_ID, BOOK_ID, None, 3, "Chapter 4", 1, "4", 500)
    return GroundingScope((BOOK_ID,), (book,), (section,))


async def _section_loader(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
    assert book_id == BOOK_ID
    assert section_ids == (SECTION_ID,)
    return (GroundingSectionText(SECTION_ID, BOOK_ID, 3, "Chapter 4", "4", "Crooks talks with Lennie."),)


@pytest.mark.asyncio
async def test_metadata_route_returns_deterministic_answer_without_section_load():
    calls = 0

    async def loader(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
        nonlocal calls
        calls += 1
        return ()

    result = await GroundingRouter(_scope(), loader, section_context_max_chars=4000).resolve("Tác giả của sách là ai?")

    assert result.decision.intent == GroundingIntent.BOOK_METADATA_AUTHOR
    assert result.decision.route == GroundingRoute.BOOK_METADATA
    assert result.deterministic_answer == 'Tác giả của "Of Mice and Men" là John Steinbeck.'
    assert calls == 0


@pytest.mark.asyncio
async def test_explicit_section_route_loads_canonical_section_context():
    result = await GroundingRouter(_scope(), _section_loader, section_context_max_chars=4000).resolve("Tóm tắt chương 4.")

    assert result.decision.intent == GroundingIntent.BOOK_SECTION_SUMMARY
    assert result.decision.route == GroundingRoute.BOOK_SECTION
    assert result.decision.resolved_section_ids == (SECTION_ID,)
    assert "Crooks talks with Lennie" in (result.section_context or "")


@pytest.mark.asyncio
async def test_ambiguous_section_falls_back_to_rag_without_section_load():
    calls = 0

    async def loader(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
        nonlocal calls
        calls += 1
        return ()

    result = await GroundingRouter(_scope(), loader, section_context_max_chars=4000).resolve("Tóm tắt chương.")

    assert result.decision.route == GroundingRoute.BOOK_RAG
    assert result.decision.intent == GroundingIntent.BOOK_SEMANTIC_QUESTION
    assert calls == 0


@pytest.mark.asyncio
async def test_semantic_question_falls_back_to_rag_route():
    result = await GroundingRouter(_scope(), _section_loader, section_context_max_chars=4000).resolve("Crooks cảm thấy như thế nào và vì sao?")

    assert result.decision.route == GroundingRoute.BOOK_RAG
    assert result.decision.intent == GroundingIntent.BOOK_SEMANTIC_QUESTION


@pytest.mark.asyncio
async def test_router_records_safe_grounding_trace():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )
    tracer.begin_turn(AgentInputMode.TEXT)

    await GroundingRouter(_scope(), _section_loader, section_context_max_chars=4000).resolve(
        "Tác giả của sách là ai?",
        input_mode=AgentInputMode.TEXT,
        tracer=tracer,
    )
    summary = tracer.complete_turn(AgentInputMode.TEXT)

    assert summary is not None
    assert summary["detected_intent"] == "book_metadata.author"
    assert summary["grounding_route"] == "book_metadata"
    assert summary["resolved_book_ids"] == [str(BOOK_ID)]
    assert summary["answer_source"] == AgentAnswerSource.BOOK_METADATA.value
    assert "John Steinbeck" not in str(emitted)
