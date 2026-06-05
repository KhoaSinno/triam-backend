import pytest

from app.core.config import settings
from app.services.agent_observability import AgentInputMode, AgentTurnTracer
from app.services.agent_voice_gpt_realtime import TriamAssistant
from app.services.voice_agent.contracts import VoiceRagResult
from app.services.voice_agent.turn_state import VoiceTurnState
from app.services.voice_agent.web_permission_policy import WebSearchPermissionPolicy


def _assistant(state: VoiceTurnState) -> TriamAssistant:
    return TriamAssistant(
        document_ids=["book-1"],
        web_search_policy=WebSearchPermissionPolicy(enabled=False),
        tracer=AgentTurnTracer(enabled=False, thread_id=None, room_name="test"),
        voice_turn_state=state,
    )


@pytest.mark.asyncio
async def test_voice_guard_blocks_mismatched_tool_query_before_rag(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    state = VoiceTurnState()
    state.record_final_transcript("Tác giả của quyển sách là ai?")
    assistant = _assistant(state)

    async def fail_if_called(*args, **kwargs):  # pragma: no cover - assertion helper
        raise AssertionError("RAG should not run when the voice query guard blocks the turn")

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fail_if_called)

    result = await assistant.resolve_book_query("đại ý chương 4", AgentInputMode.VOICE)

    assert result.startswith("CLARIFICATION_REQUIRED:")


@pytest.mark.asyncio
async def test_text_query_is_not_blocked_by_voice_guard(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    state = VoiceTurnState()
    state.record_final_transcript("Tác giả của quyển sách là ai?")
    assistant = _assistant(state)

    async def fake_search(*args, **kwargs):
        return VoiceRagResult(found=False, chunks=[], message="not found")

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fake_search)

    result = await assistant.resolve_book_query("đại ý chương 4", AgentInputMode.TEXT)

    assert result == "BOOK_CONTEXT_NOT_FOUND: not found"
