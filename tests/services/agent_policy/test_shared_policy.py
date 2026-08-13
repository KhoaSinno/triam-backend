import uuid

import pytest

from app.services.agent_grounding.contracts import (
    GroundingBook,
    GroundingDecision,
    GroundingIntent,
    GroundingResult,
    GroundingRoute,
    GroundingScope,
    GroundingSection,
    GroundingSectionText,
    ResolutionQuality,
)
from app.services.agent_grounding.grounding_router import GroundingRouter
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer
from app.services.agent_policy import AgentPolicyAction, AgentPolicyRequest, SharedAgentPolicy, render_voice_tool_result
from app.services.voice_agent.contracts import VoiceRagResult

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


def _request(query: str, *, allow_web: bool = True) -> AgentPolicyRequest:
    return AgentPolicyRequest(
        query=query,
        input_mode=AgentInputMode.TEXT,
        document_ids=[str(BOOK_ID)],
        allow_web_permission=allow_web,
    )


def _policy(search_book_context=None) -> SharedAgentPolicy:
    return SharedAgentPolicy(
        document_ids=[str(BOOK_ID)],
        grounding_router=GroundingRouter(_scope(), _section_loader, section_context_max_chars=4000),
        tracer=AgentTurnTracer(enabled=False, thread_id=None, room_name="test"),
        search_book_context=search_book_context or _unexpected_rag_call,
    )


async def _unexpected_rag_call(*args, **kwargs):  # pragma: no cover - assertion helper
    raise AssertionError("RAG should not run for deterministic routes")


@pytest.mark.asyncio
async def test_metadata_question_returns_direct_answer_without_rag() -> None:
    result = await _policy().resolve(_request("Tác giả của sách là ai?"))

    assert result.action == AgentPolicyAction.DIRECT_ANSWER
    assert result.answer_source == AgentAnswerSource.BOOK_METADATA
    assert result.user_message == 'Tác giả của "Of Mice and Men" là John Steinbeck.'
    assert render_voice_tool_result(result).startswith("BOOK_METADATA_FOUND:")


@pytest.mark.asyncio
async def test_context_overview_returns_shared_direct_answer_without_rag() -> None:
    context_result = GroundingResult(
        GroundingDecision(
            GroundingIntent.CONTEXT_DOCUMENT_COUNT,
            GroundingRoute.CONTEXT_OVERVIEW,
            quality=ResolutionQuality.EXACT,
            reason_code="context_scope_metadata",
            resolved_book_ids=(BOOK_ID,),
        ),
        deterministic_answer="Ngữ cảnh học tập hiện tại có 1 tài liệu.",
    )

    class ContextRouter:
        async def resolve(self, *_args, **_kwargs):
            return context_result

    policy = SharedAgentPolicy(
        document_ids=[str(BOOK_ID)],
        grounding_router=ContextRouter(),
        tracer=AgentTurnTracer(enabled=False, thread_id=None, room_name="test"),
        search_book_context=_unexpected_rag_call,
    )
    result = await policy.resolve(_request("Có bao nhiêu tài liệu trong ngữ cảnh hiện tại?"))

    assert result.action == AgentPolicyAction.DIRECT_ANSWER
    assert result.answer_source == AgentAnswerSource.CONTEXT_METADATA
    assert result.user_message == "Ngữ cảnh học tập hiện tại có 1 tài liệu."
    assert render_voice_tool_result(result).startswith("STUDY_CONTEXT_FOUND:")


@pytest.mark.asyncio
async def test_section_question_returns_section_context_action() -> None:
    result = await _policy().resolve(_request("Tóm tắt chương 4."))

    assert result.action == AgentPolicyAction.ANSWER_WITH_SECTION_CONTEXT
    assert result.answer_source == AgentAnswerSource.BOOK_SECTION
    assert result.resolved_section_ids == (str(SECTION_ID),)
    assert "Crooks talks with Lennie" in (result.llm_system_context or "")
    assert render_voice_tool_result(result).startswith("BOOK_SECTION_FOUND:")


@pytest.mark.asyncio
async def test_missing_section_target_falls_back_to_rag() -> None:
    async def fake_search(*args, **kwargs):
        return VoiceRagResult(
            found=True,
            chunks=[
                {
                    "id": "chunk-1",
                    "content": "Crooks feels isolated.",
                    "section_id": str(SECTION_ID),
                    "section_path": "4",
                    "chunk_index": 0,
                }
            ],
            message="",
        )

    result = await _policy(fake_search).resolve(_request("Tóm tắt chương."))

    assert result.action == AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT
    assert result.answer_source == AgentAnswerSource.BOOK_RAG
    assert render_voice_tool_result(result).startswith("BOOK_CONTEXT_FOUND:")


@pytest.mark.asyncio
async def test_semantic_rag_hit_returns_rag_context_action() -> None:
    async def fake_search(*args, **kwargs):
        return VoiceRagResult(
            found=True,
            chunks=[
                {
                    "id": "chunk-1",
                    "content": "Crooks feels isolated because he is segregated from the other workers.",
                    "section_id": str(SECTION_ID),
                    "section_path": "4",
                    "chunk_index": 0,
                }
            ],
            message="",
        )

    result = await _policy(fake_search).resolve(_request("Crooks cảm thấy như thế nào?"))

    assert result.action == AgentPolicyAction.ANSWER_WITH_RAG_CONTEXT
    assert result.answer_source == AgentAnswerSource.BOOK_RAG
    assert result.retrieval_chunk_ids == ("chunk-1",)
    assert result.retrieval_result_count == 1
    assert render_voice_tool_result(result).startswith("BOOK_CONTEXT_FOUND:")


@pytest.mark.asyncio
async def test_semantic_rag_miss_asks_web_when_enabled() -> None:
    async def fake_search(*args, **kwargs):
        return VoiceRagResult(found=False, chunks=[], message="Không tìm thấy thông tin phù hợp trong sách.")

    result = await _policy(fake_search).resolve(_request("Thông tin này có mới nhất không?", allow_web=True))

    assert result.action == AgentPolicyAction.ASK_WEB_PERMISSION
    assert result.answer_source == AgentAnswerSource.POLICY
    assert render_voice_tool_result(result).startswith("BOOK_CONTEXT_NOT_FOUND:")


@pytest.mark.asyncio
async def test_semantic_rag_miss_reports_web_disabled() -> None:
    async def fake_search(*args, **kwargs):
        return VoiceRagResult(found=False, chunks=[], message="Không tìm thấy thông tin phù hợp trong sách.")

    result = await _policy(fake_search).resolve(_request("Thông tin này có mới nhất không?", allow_web=False))

    assert result.action == AgentPolicyAction.WEB_DISABLED
    assert result.answer_source == AgentAnswerSource.POLICY
    assert "internet hiện đang tắt" in render_voice_tool_result(result)
