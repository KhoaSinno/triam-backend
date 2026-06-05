from app.services.voice_agent.turn_state import VoiceTurnState


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


def test_recent_transcript_prefers_newest_committed_text() -> None:
    clock = FakeClock()
    state = VoiceTurnState(clock=clock)

    state.record_final_transcript("Tóm tắt chương 4", "vi")
    clock.value = 1.0
    state.record_committed_user_text("Tóm tắt chương bốn", "vi")

    snapshot = state.recent_transcript(ttl_seconds=15)

    assert snapshot is not None
    assert snapshot.text == "Tóm tắt chương bốn"
    assert snapshot.source == "committed_user_item"


def test_recent_transcript_expires_by_ttl() -> None:
    clock = FakeClock()
    state = VoiceTurnState(clock=clock)

    state.record_final_transcript("Tác giả của sách là ai?", "vi")
    clock.value = 20.0

    assert state.recent_transcript(ttl_seconds=15) is None


def test_empty_transcript_is_ignored() -> None:
    state = VoiceTurnState(clock=FakeClock())

    state.record_final_transcript("   ")
    state.record_committed_user_text("")

    assert state.recent_transcript(ttl_seconds=15) is None
