from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any

from app.core.logger import log
from app.services.agent_observability import AgentInputMode, AgentTurnTracer


@dataclass(frozen=True)
class VoiceToolReplyWatchdogConfig:
    enabled: bool
    grace_seconds: float
    thinking_grace_seconds: float
    monitored_tools: set[str]
    allow_error_outputs: bool = False
    force_tool_choice_none: bool = True


class VoiceToolReplyWatchdog:
    def __init__(
        self,
        *,
        session: Any,
        room: Any | None = None,
        tracer: AgentTurnTracer,
        config: VoiceToolReplyWatchdogConfig,
    ) -> None:
        self.session = session
        # AgentSession does not reliably expose the LiveKit room. The entrypoint
        # supplies ctx.room; retaining the fallback keeps console tests compatible.
        self.room = room if room is not None else getattr(session, "room", None)
        self.tracer = tracer
        self.config = config
        self._watch_tasks: dict[str, asyncio.Task[None]] = {}
        self._watch_tool_names: dict[str, str] = {}
        self._last_tool_completed_monotonic: float | None = None

    def close(self) -> None:
        self.cancel_all("session_close")

    def cancel_all(self, reason: str) -> None:
        if not self._watch_tasks:
            return

        for task in self._watch_tasks.values():
            if not task.done():
                task.cancel()
        self._watch_tasks.clear()
        self._watch_tool_names.clear()
        self.tracer.record_tool_reply_watchdog_cancelled(
            AgentInputMode.VOICE,
            reason=reason,
        )

    def record_speech_created(self, *, source: str | None = None) -> None:
        elapsed_ms = self._elapsed_since_tool_completed_ms()
        self.tracer.record_tool_reply_speech_created(
            AgentInputMode.VOICE,
            source=source,
            elapsed_ms=elapsed_ms,
        )
        # A SpeechHandle can be interrupted before an assistant item is committed.
        # Keep watching for a completed answer, with a fresh grace window.
        self._reschedule_active_grace(
            grace_seconds=self.config.thinking_grace_seconds,
            reason="speech_created_waiting_for_commit",
        )

    def record_assistant_committed(self) -> None:
        self.cancel_all("assistant_committed")

    def record_agent_state_changed(self, *, new_state: str) -> None:
        state_lower = new_state.lower()
        if state_lower == "thinking":
            self._reschedule_active_grace(
                grace_seconds=self.config.thinking_grace_seconds,
                reason="agent_thinking",
            )

    def _reschedule_active_grace(self, *, grace_seconds: float, reason: str) -> None:
        active_event_ids = [eid for eid, task in self._watch_tasks.items() if not task.done()]
        if not active_event_ids:
            return

        for event_id in active_event_ids:
            task = self._watch_tasks.get(event_id)
            if task and not task.done():
                task.cancel()

            tool_name = self._watch_tool_names.get(event_id, "unknown")
            log.info(
                "Voice tool reply watchdog: extending grace | "
                f"tool={tool_name} | reason={reason}"
            )
            self.tracer.record_tool_reply_watchdog_scheduled(
                AgentInputMode.VOICE,
                tool_name=tool_name,
                grace_ms=int(grace_seconds * 1000),
            )
            self._watch_tasks[event_id] = asyncio.create_task(
                self._watch_and_force_reply(
                    event_id=event_id,
                    tool_name=tool_name,
                    grace_seconds=grace_seconds,
                )
            )

    def record_user_state_changed(self, *, new_state: str) -> None:
        if new_state == "speaking":
            self.cancel_all("user_started_speaking")

    def record_user_transcribed(self) -> None:
        self.cancel_all("user_input_transcribed")

    def schedule_after_tools_executed(self, ev: Any) -> None:
        if not self.config.enabled:
            return
        if getattr(ev, "has_tool_reply", True) is False:
            return
        for call, output in _zipped_tool_outputs(ev):
            tool_name = str(getattr(call, "name", ""))
            if not self._should_watch(tool_name, output):
                continue
            event_id = _tool_event_id(call)
            self._schedule_one(event_id, tool_name)

    def _should_watch(self, tool_name: str, output: Any) -> bool:
        if tool_name not in self.config.monitored_tools:
            return False
        if output is not None and getattr(output, "is_error", False):
            return self.config.allow_error_outputs
        return True

    def _schedule_one(self, event_id: str, tool_name: str) -> None:
        existing = self._watch_tasks.pop(event_id, None)
        if existing and not existing.done():
            existing.cancel()
        self._watch_tool_names[event_id] = tool_name
        self._last_tool_completed_monotonic = time.monotonic()
        self.tracer.record_tool_reply_watchdog_scheduled(
            AgentInputMode.VOICE,
            tool_name=tool_name,
            grace_ms=int(self.config.grace_seconds * 1000),
        )
        self._watch_tasks[event_id] = asyncio.create_task(
            self._watch_and_force_reply(
                event_id=event_id,
                tool_name=tool_name,
                grace_seconds=self.config.grace_seconds,
            )
        )

    async def _watch_and_force_reply(
        self,
        *,
        event_id: str,
        tool_name: str,
        grace_seconds: float,
    ) -> None:
        try:
            await asyncio.sleep(grace_seconds)
            elapsed_ms = self._elapsed_since_tool_completed_ms()
            self.tracer.record_tool_reply_watchdog_fired(
                AgentInputMode.VOICE,
                tool_name=tool_name,
                elapsed_ms=elapsed_ms,
                reason="no_speech_after_tool",
            )
            self._generate_reply_after_tool(tool_name=tool_name)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.tracer.record_error(AgentInputMode.VOICE, "tool_reply_watchdog_error")
            log.warning(
                "Voice tool reply watchdog failed | "
                f"tool={tool_name} | error_type={type(exc).__name__}"
            )
        finally:
            current_task = asyncio.current_task()
            if self._watch_tasks.get(event_id) is current_task:
                self._watch_tasks.pop(event_id, None)
                self._watch_tool_names.pop(event_id, None)

    def _generate_reply_after_tool(self, *, tool_name: str) -> None:
        if self.room is None or not self.room.isconnected():
            log.info(
                "Voice watchdog fallback skipped | "
                f"tool={tool_name} | reason=room_disconnected"
            )
            return

        kwargs: dict[str, Any] = {
            "allow_interruptions": True,
            "instructions": POST_TOOL_REPLY_INSTRUCTIONS,
        }
        if self.config.force_tool_choice_none:
            kwargs["tool_choice"] = "none"
        log.info(
            "Voice watchdog forcing post-tool reply | "
            f"tool={tool_name} | tool_choice={kwargs.get('tool_choice', 'auto')}"
        )
        self.session.generate_reply(**kwargs)

    def _elapsed_since_tool_completed_ms(self) -> int | None:
        if self._last_tool_completed_monotonic is None:
            return None
        return max(0, int((time.monotonic() - self._last_tool_completed_monotonic) * 1000))


def _zipped_tool_outputs(ev: Any) -> list[tuple[Any, Any]]:
    if hasattr(ev, "zipped"):
        return list(ev.zipped())
    calls = list(getattr(ev, "function_calls", []) or [])
    outputs = list(getattr(ev, "function_call_outputs", []) or [])
    return list(zip(calls, outputs or [None] * len(calls), strict=False))


def _tool_event_id(call: Any) -> str:
    return str(
        getattr(call, "call_id", None)
        or getattr(call, "id", None)
        or f"{getattr(call, 'name', 'unknown')}:{getattr(call, 'created_at', '')}"
    )


POST_TOOL_REPLY_INSTRUCTIONS = """
Answer the user now using the most recent tool result already present in the conversation.
Do not call any tools.
Do not ask for web permission again.
Do not say you are still searching.
Reply in Vietnamese, naturally and briefly, in 1-2 short sentences.
"""
