import pytest

from app.core.config import settings
from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer
from app.services.agent_policy import AgentPolicyAction, AgentPolicyRequest, AgentPolicyResult
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


class FakeSharedPolicy:
    def __init__(self) -> None:
        self.requests: list[AgentPolicyRequest] = []

    async def resolve(self, request: AgentPolicyRequest) -> AgentPolicyResult:
        self.requests.append(request)
        return AgentPolicyResult(
            action=AgentPolicyAction.DIRECT_ANSWER,
            answer_source=AgentAnswerSource.BOOK_METADATA,
            reason_code="test_policy",
            user_message="Shared policy answer.",
            tool_marker="BOOK_METADATA_FOUND:\nShared policy answer.",
        )


@pytest.mark.asyncio
async def test_voice_guard_does_not_block_by_transcript_overlap(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    state = VoiceTurnState()
    state.record_final_transcript("Tác giả của quyển sách là ai?")
    assistant = _assistant(state)

    async def fake_search(*args, **kwargs):
        return VoiceRagResult(found=False, chunks=[], message="not found")

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fake_search)

    result = await assistant.resolve_book_query("đại ý chương 4", AgentInputMode.VOICE)

    assert result == "BOOK_CONTEXT_NOT_FOUND: not found"


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


@pytest.mark.asyncio
async def test_resolve_book_query_uses_shared_policy_when_enabled(monkeypatch) -> None:
    monkeypatch.setattr(settings, "AGENT_SHARED_POLICY_ENABLED", True)
    fake_policy = FakeSharedPolicy()
    assistant = TriamAssistant(
        document_ids=["book-1"],
        web_search_policy=WebSearchPermissionPolicy(enabled=False),
        tracer=AgentTurnTracer(enabled=False, thread_id=None, room_name="test"),
        shared_policy=fake_policy,  # type: ignore[arg-type]
    )

    result = await assistant.resolve_book_query("Tác giả của sách là ai?", AgentInputMode.TEXT)

    assert result == "BOOK_METADATA_FOUND:\nShared policy answer."
    assert fake_policy.requests[0].input_mode == AgentInputMode.TEXT
    assert fake_policy.requests[0].document_ids == ["book-1"]


@pytest.mark.asyncio
async def test_voice_confirmation_after_pending_clarification_allows_rag_once(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    monkeypatch.setattr(settings, "VOICE_AGENT_CLARIFICATION_STATE_ENABLED", True)
    state = VoiceTurnState()
    state.set_pending_clarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        reason_code="assistant_confirmation",
    )
    state.record_final_transcript("đúng rồi")
    assistant = _assistant(state)
    calls: list[str] = []

    async def fake_search(query, document_ids, **kwargs):
        del document_ids, kwargs
        calls.append(query)
        return VoiceRagResult(
            found=True,
            chunks=[{"id": 1, "content": "Nội dung chương 5.", "chunk_index": 0}],
            message="",
        )

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fake_search)

    result = await assistant.resolve_book_query("tóm tắt chương 5", AgentInputMode.VOICE)

    assert result.startswith("BOOK_CONTEXT_FOUND:")
    assert calls == ["tóm tắt chương 5"]
    assert state.recent_pending_clarification(ttl_seconds=30) is None


@pytest.mark.asyncio
async def test_voice_denial_after_pending_clarification_does_not_call_rag(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    monkeypatch.setattr(settings, "VOICE_AGENT_CLARIFICATION_STATE_ENABLED", True)
    state = VoiceTurnState()
    state.set_pending_clarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        reason_code="assistant_confirmation",
    )
    state.record_final_transcript("không phải")
    assistant = _assistant(state)

    async def fail_if_called(*args, **kwargs):  # pragma: no cover - assertion helper
        raise AssertionError("RAG should not run when user denies clarification")

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fail_if_called)

    result = await assistant.resolve_book_query("tóm tắt chương 5", AgentInputMode.VOICE)

    assert result.startswith("CLARIFICATION_REQUIRED:")
    assert "nội dung nào khác" in result
    assert state.recent_pending_clarification(ttl_seconds=30) is None


@pytest.mark.asyncio
async def test_voice_new_question_after_pending_clarification_reruns_normal_guard(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    monkeypatch.setattr(settings, "VOICE_AGENT_CLARIFICATION_STATE_ENABLED", True)
    state = VoiceTurnState()
    state.set_pending_clarification(
        prompt_text="Bạn muốn tóm tắt chương 5 đúng không?",
        reason_code="assistant_confirmation",
    )
    state.record_final_transcript("tác giả của sách là ai")
    assistant = _assistant(state)
    calls: list[str] = []

    async def fake_search(query, document_ids, **kwargs):
        del document_ids, kwargs
        calls.append(query)
        return VoiceRagResult(found=False, chunks=[], message="not found")

    monkeypatch.setattr("app.services.agent_voice_gpt_realtime.search_voice_book_context", fake_search)

    result = await assistant.resolve_book_query("tác giả của sách là ai", AgentInputMode.VOICE)

    assert result == "BOOK_CONTEXT_NOT_FOUND: not found"
    assert calls == ["tác giả của sách là ai"]
    assert state.recent_pending_clarification(ttl_seconds=30) is None


@pytest.mark.asyncio
async def test_voice_clarification_marker_sets_pending_state(monkeypatch) -> None:
    monkeypatch.setattr(settings, "VOICE_AGENT_QUERY_GUARD_ENABLED", True)
    monkeypatch.setattr(settings, "VOICE_AGENT_CLARIFICATION_STATE_ENABLED", True)
    state = VoiceTurnState()
    state.record_final_transcript("tóm tắt chương")
    assistant = _assistant(state)

    result = await assistant.resolve_book_query("tóm tắt chương", AgentInputMode.VOICE)
    pending = state.recent_pending_clarification(ttl_seconds=30)

    assert result.startswith("CLARIFICATION_REQUIRED:")
    assert pending is not None
    assert pending.reason_code == "missing_section_reference"
