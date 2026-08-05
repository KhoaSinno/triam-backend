import uuid

from app.services.agent_voice_gpt_realtime import _parse_job_metadata
from app.services.voice_agent.context_runtime import ActiveVoiceContext, ActiveVoiceContextState
from app.services.voice_agent.contracts import VoiceContextResolution


def _resolution(*, thread_id: uuid.UUID | None = None) -> VoiceContextResolution:
    return VoiceContextResolution(
        context_id=uuid.uuid4(),
        thread_id=thread_id or uuid.uuid4(),
        document_ids=(str(uuid.uuid4()),),
        context_title="Ngữ cảnh kiểm thử",
        thread_title="Thread kiểm thử",
    )


def test_job_metadata_keeps_user_and_context_scope_for_runtime_switching():
    metadata = _parse_job_metadata(
        '{"thread_id":"thread-1","context_id":"context-1","user_id":"user-1","document_ids":["book-1"]}',
        "room-1",
    )

    assert metadata.thread_id == "thread-1"
    assert metadata.context_id == "context-1"
    assert metadata.user_id == "user-1"
    assert metadata.document_ids == ["book-1"]


def test_active_context_replacement_increments_version_without_mutating_old_snapshot():
    first = _resolution()
    state = ActiveVoiceContextState(ActiveVoiceContext.from_resolution(first))
    old = state.current

    second = _resolution()
    current = state.replace(second)

    assert old.version == 1
    assert old.thread_id == first.thread_id
    assert current.version == 2
    assert current.thread_id == second.thread_id
    assert current.document_ids == second.document_ids
