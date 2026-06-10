import asyncio
from unittest.mock import MagicMock

import pytest

from app.services.agent_observability import AgentInputMode, AgentTurnTracer
from app.services.voice_agent.tool_reply_watchdog import (
    VoiceToolReplyWatchdog,
    VoiceToolReplyWatchdogConfig,
)


class FakeRoom:
    def __init__(self, connected: bool = True) -> None:
        self._connected = connected

    def isconnected(self) -> bool:
        return self._connected


class FakeSession:
    def __init__(self, connected: bool = True) -> None:
        self.room = FakeRoom(connected)
        self.generate_reply = MagicMock()


class FakeCall:
    def __init__(self, name: str, call_id: str) -> None:
        self.name = name
        self.call_id = call_id
        self.id = call_id


class FakeOutput:
    def __init__(self, name: str, call_id: str, is_error: bool = False) -> None:
        self.name = name
        self.call_id = call_id
        self.is_error = is_error


class FakeEvent:
    def __init__(self, calls: list[FakeCall], outputs: list[FakeOutput]) -> None:
        self.function_calls = calls
        self.function_call_outputs = outputs

    def zipped(self) -> list[tuple[FakeCall, FakeOutput]]:
        return list(zip(self.function_calls, self.function_call_outputs, strict=False))


@pytest.fixture
def base_config() -> VoiceToolReplyWatchdogConfig:
    return VoiceToolReplyWatchdogConfig(
        enabled=True,
        grace_seconds=0.05,  # Short grace seconds for faster tests
        thinking_grace_seconds=0.1,  # Short thinking grace for faster tests
        monitored_tools={"execute_web_search", "search_book_knowledge", "ask_web_search_permission"},
        allow_error_outputs=False,
        force_tool_choice_none=True,
    )


@pytest.fixture
def mock_tracer() -> MagicMock:
    return MagicMock(spec=AgentTurnTracer)


@pytest.mark.asyncio
async def test_watchdog_monitored_tool_no_speech(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    # Let the watchdog sleep and trigger
    await asyncio.sleep(0.08)

    session.generate_reply.assert_called_once()
    kwargs = session.generate_reply.call_args[1]
    assert kwargs.get("tool_choice") == "none"
    mock_tracer.record_tool_reply_watchdog_fired.assert_called_once_with(
        AgentInputMode.VOICE,
        tool_name="execute_web_search",
        elapsed_ms=pytest.approx(50, abs=50),
        reason="no_speech_after_tool",
    )
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_speech_before_grace(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    # Agent starts speaking naturally before grace window ends
    await asyncio.sleep(0.01)
    watchdog.record_speech_created(source="agent_speech")

    # Let grace window expire
    await asyncio.sleep(0.06)

    session.generate_reply.assert_not_called()
    mock_tracer.record_tool_reply_watchdog_cancelled.assert_called_once_with(
        AgentInputMode.VOICE,
        reason="speech_created",
    )
    mock_tracer.record_tool_reply_speech_created.assert_called_once_with(
        AgentInputMode.VOICE,
        source="agent_speech",
        elapsed_ms=pytest.approx(10, abs=40),
    )
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_user_starts_speaking(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    # User interrupts before grace window ends
    await asyncio.sleep(0.01)
    watchdog.record_user_state_changed(new_state="speaking")

    # Let grace window expire
    await asyncio.sleep(0.06)

    session.generate_reply.assert_not_called()
    mock_tracer.record_tool_reply_watchdog_cancelled.assert_called_with(
        AgentInputMode.VOICE,
        reason="user_started_speaking",
    )
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_non_monitored_tool(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("some_background_tool", "call_1")
    output = FakeOutput("some_background_tool", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    await asyncio.sleep(0.08)

    session.generate_reply.assert_not_called()
    mock_tracer.record_tool_reply_watchdog_scheduled.assert_not_called()
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_error_output_default(base_config, mock_tracer) -> None:
    session = FakeSession()
    # allow_error_outputs = False
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1", is_error=True)
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    await asyncio.sleep(0.08)

    session.generate_reply.assert_not_called()
    mock_tracer.record_tool_reply_watchdog_scheduled.assert_not_called()
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_duplicate_events(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)
    # Schedule the exact same event
    watchdog.schedule_after_tools_executed(event)

    await asyncio.sleep(0.08)

    # Re-scheduling should cancel the previous and schedule a new one, but only one generate_reply fires
    assert session.generate_reply.call_count == 1
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_generate_reply_raises(base_config, mock_tracer) -> None:
    session = FakeSession()
    session.generate_reply.side_effect = Exception("API error")
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    await asyncio.sleep(0.08)

    mock_tracer.record_error.assert_called_once_with(AgentInputMode.VOICE, "tool_reply_watchdog_error")
    watchdog.close()


@pytest.mark.asyncio
async def test_watchdog_thinking_extends_grace(base_config, mock_tracer) -> None:
    session = FakeSession()
    watchdog = VoiceToolReplyWatchdog(session=session, tracer=mock_tracer, config=base_config)

    call = FakeCall("execute_web_search", "call_1")
    output = FakeOutput("execute_web_search", "call_1")
    event = FakeEvent([call], [output])

    watchdog.schedule_after_tools_executed(event)

    # Transition to "thinking" before grace window ends (0.05s)
    await asyncio.sleep(0.01)
    watchdog.record_agent_state_changed(new_state="thinking")

    # Let original grace window (0.05s) expire
    await asyncio.sleep(0.05)
    # The watchdog should not have fired yet because it was extended to 0.1s
    session.generate_reply.assert_not_called()

    # Let the extended thinking grace expire
    await asyncio.sleep(0.1)
    session.generate_reply.assert_called_once()
    watchdog.close()

