"""Shared policy layer for book-grounded text and realtime voice agents."""

from app.services.agent_policy.contracts import AgentPolicyAction, AgentPolicyRequest, AgentPolicyResult
from app.services.agent_policy.renderers import render_text_direct_message, render_voice_tool_result
from app.services.agent_policy.shared_policy import SharedAgentPolicy

__all__ = [
    "AgentPolicyAction",
    "AgentPolicyRequest",
    "AgentPolicyResult",
    "SharedAgentPolicy",
    "render_text_direct_message",
    "render_voice_tool_result",
]
