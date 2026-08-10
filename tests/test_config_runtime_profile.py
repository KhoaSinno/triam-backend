from pathlib import Path

import pytest
from pydantic.v1 import ValidationError

from app.core.config import Settings
from app.services import agent_voice_gpt_realtime as voice_agent

REQUIRED_SETTINGS = {
    "OPENAI_API_KEY": "test",
    "TAVILY_API_KEY": "test",
    "GEMINI_BASE_URL": "https://example.test",
    "GEMINI_API_KEY": "test",
    "DATABASE_URL": "sqlite:///test.db",
    "SUPABASE_URL": "https://example.supabase.co",
    "SUPABASE_KEY": "test",
    "SUPABASE_SERVICE_ROLE_KEY": "test",
    "LIVEKIT_API_KEY": "test",
    "LIVEKIT_API_SECRET": "test",
    "LIVEKIT_AGENT_NAME": "triam-test-agent",
}


def build_settings(**overrides):
    return Settings(_env_file=None, **REQUIRED_SETTINGS, **overrides)


def test_console_ids_are_configurable_for_local_full_voice_test():
    clean_settings = build_settings(
        VOICE_AGENT_CONSOLE_BOOK_ID="195d9623-03d0-483a-ac09-52d9137f2471",
        VOICE_AGENT_CONSOLE_THREAD_ID="07be00b9-c6da-4801-8ba2-7558205b92b2",
    )

    assert clean_settings.VOICE_AGENT_CONSOLE_BOOK_ID
    assert clean_settings.VOICE_AGENT_CONSOLE_THREAD_ID


def test_realtime_session_budget_is_disabled_by_default():
    clean_settings = build_settings()

    assert clean_settings.VOICE_AGENT_REALTIME_CONTEXT_BUDGET_ENABLED is False
    assert clean_settings.VOICE_AGENT_REALTIME_CONTEXT_MAX_POST_INSTRUCTIONS_TOKENS == 8000
    assert clean_settings.VOICE_AGENT_REALTIME_CONTEXT_RETENTION_RATIO == 0.75


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("VOICE_AGENT_REALTIME_CONTEXT_MAX_POST_INSTRUCTIONS_TOKENS", 3999),
        ("VOICE_AGENT_REALTIME_CONTEXT_MAX_POST_INSTRUCTIONS_TOKENS", 24001),
        ("VOICE_AGENT_REALTIME_CONTEXT_RETENTION_RATIO", 0.49),
        ("VOICE_AGENT_REALTIME_CONTEXT_RETENTION_RATIO", 1.0),
    ],
)
def test_realtime_session_budget_rejects_invalid_configuration(field, value):
    with pytest.raises(ValidationError):
        build_settings(**{field: value})


def test_dead_runtime_configs_are_removed_from_settings():
    clean_settings = build_settings()

    assert not hasattr(clean_settings, "VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED")
    assert not hasattr(clean_settings, "VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS")
    assert not hasattr(clean_settings, "EMBEDDING_BATCH_SIZE")
    assert not hasattr(clean_settings, "BOOK_SECTION_EMBEDDING_DIMENSION")
    assert not hasattr(clean_settings, "PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS")


def test_text_chat_agentic_mode_is_independent_from_shared_policy():
    clean_settings = build_settings()
    assert clean_settings.VOICE_AGENT_TEXT_CHAT_AGENTIC_ENABLED is False
    assert clean_settings.VOICE_AGENT_TEXT_CHAT_AGENTIC_MAX_STEPS == 4

    assert voice_agent._select_text_chat_orchestration_mode(
        agentic_enabled=True,
        shared_policy_enabled=True,
    ) == "agentic"
    assert voice_agent._select_text_chat_orchestration_mode(
        agentic_enabled=False,
        shared_policy_enabled=True,
    ) == "shared_policy"
    assert voice_agent._select_text_chat_orchestration_mode(
        agentic_enabled=False,
        shared_policy_enabled=False,
    ) == "legacy"


def test_env_example_documents_console_ids_as_placeholders():
    env_example = Path(".env.example").read_text(encoding="utf-8")

    assert "VOICE_AGENT_CONSOLE_BOOK_ID=<local-test-book-id>" in env_example
    assert "VOICE_AGENT_CONSOLE_THREAD_ID=<local-test-thread-id>" in env_example
    assert "c3f13d07-4494-4995-ba75-30a12589b8fc" not in env_example
    assert "07be00b9-c6da-4801-8ba2-7558205b92b2" not in env_example


def test_env_example_drops_dead_runtime_configs():
    env_example = Path(".env.example").read_text(encoding="utf-8")
    env_lines = {line.strip() for line in env_example.splitlines()}

    assert "VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED" not in env_example
    assert "VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS" not in env_example
    assert not any(line.startswith("EMBEDDING_BATCH_SIZE=") for line in env_lines)
    assert "BOOK_SECTION_EMBEDDING_DIMENSION" not in env_example
    assert "PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS" not in env_example


def test_non_console_metadata_does_not_use_console_fallback(monkeypatch):
    monkeypatch.setattr(voice_agent.settings, "VOICE_AGENT_CONSOLE_BOOK_ID", "book-console")
    monkeypatch.setattr(voice_agent.settings, "VOICE_AGENT_CONSOLE_THREAD_ID", "thread-console")

    metadata = voice_agent._parse_job_metadata(None, room_name="production-room")

    assert metadata.document_ids == []
    assert metadata.thread_id == ""


def test_console_metadata_uses_console_fallback(monkeypatch):
    monkeypatch.setattr(voice_agent.settings, "VOICE_AGENT_CONSOLE_BOOK_ID", "book-console")
    monkeypatch.setattr(voice_agent.settings, "VOICE_AGENT_CONSOLE_THREAD_ID", "thread-console")

    metadata = voice_agent._parse_job_metadata(None, room_name="console")

    assert metadata.document_ids == ["book-console"]
    assert metadata.thread_id == "thread-console"
