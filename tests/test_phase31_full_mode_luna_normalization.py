import pytest

from app.services.chapter_chunking_service import TextChunk
from app.services.token_budget_service import TextBudget


class FakeLunaClient:
    def __init__(self):
        self.closed = False

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_full_mode_small_unit_uses_luna_once_without_review_synthesis(monkeypatch):
    from app.services import llm_service

    calls: list[tuple[str, str | None]] = []
    luna_client = FakeLunaClient()

    async def fake_luna_normalize(client, text: str, *, context_hint: str | None = None):
        assert client is luna_client
        calls.append((text, context_hint))
        return llm_service.NormalizedUnit(main_scripts=["Nội dung chính."], review_script="Ôn tập bài học.")

    async def fail_synthesis(*args, **kwargs):
        raise AssertionError("Single Full unit must not synthesize a second review")

    monkeypatch.setattr(llm_service, "_call_luna_normalize_llm", fake_luna_normalize)
    monkeypatch.setattr(llm_service, "_synthesize_full_unit_review", fail_synthesis)
    monkeypatch.setattr(llm_service, "_create_luna_client", lambda: luna_client)
    monkeypatch.setattr(
        llm_service,
        "estimate_text_budget",
        lambda text: TextBudget(char_count=len(text), estimated_tokens=5000, estimated_audio_seconds=10),
    )

    result = await llm_service.normalize_text_for_speech("nguồn", "full", unit_title="Chương 1")

    assert result == {"main_scripts": ["Nội dung chính."], "review_script": "Ôn tập bài học."}
    assert calls == [("nguồn", None)]
    assert luna_client.closed is True


@pytest.mark.asyncio
async def test_full_mode_chunked_merges_main_scripts_and_synthesizes_one_review(monkeypatch):
    from app.services import llm_service

    chunks = [
        TextChunk(index=0, text="nguồn một", estimated_tokens=5000),
        TextChunk(index=1, text="nguồn hai", estimated_tokens=5000),
        TextChunk(index=2, text="nguồn ba", estimated_tokens=1000),
    ]
    normalize_calls: list[tuple[str, str | None]] = []
    synthesis_calls: list[tuple[str | None, list[str]]] = []
    luna_client = FakeLunaClient()

    async def fake_luna_normalize(client, text: str, *, context_hint: str | None = None):
        assert client is luna_client
        normalize_calls.append((text, context_hint))
        number = len(normalize_calls)
        return llm_service.NormalizedUnit(
            main_scripts=[f"main {number}a", f"main {number}b"],
            review_script=f"draft {number}",
        )

    async def fake_synthesis(client, title: str | None, drafts: list[str]) -> str:
        assert client is luna_client
        synthesis_calls.append((title, drafts))
        return "review chung"

    monkeypatch.setattr(llm_service, "split_full_mode_text_for_llm", lambda text: chunks)
    monkeypatch.setattr(llm_service, "_call_luna_normalize_llm", fake_luna_normalize)
    monkeypatch.setattr(llm_service, "_synthesize_full_unit_review", fake_synthesis)
    monkeypatch.setattr(llm_service, "_create_luna_client", lambda: luna_client)
    monkeypatch.setattr(
        llm_service,
        "estimate_text_budget",
        lambda text: TextBudget(char_count=len(text), estimated_tokens=11000, estimated_audio_seconds=10),
    )

    result = await llm_service.normalize_text_for_speech("nguồn dài", "full", unit_title="Chương 5 - Phần 1")

    assert result == {
        "main_scripts": ["main 1a", "main 1b", "main 2a", "main 2b", "main 3a", "main 3b"],
        "review_script": "review chung",
    }
    assert [item[0] for item in normalize_calls] == ["nguồn một", "nguồn hai", "nguồn ba"]
    assert normalize_calls[0][1] is not None
    assert "nguồn một" not in normalize_calls[0][1]
    assert normalize_calls[1][1] is not None
    assert "nguồn một" in normalize_calls[1][1]
    assert synthesis_calls == [("Chương 5 - Phần 1", ["draft 1", "draft 2", "draft 3"])]
    assert luna_client.closed is True


@pytest.mark.asyncio
async def test_pareto_keeps_gemini_normalization_path(monkeypatch):
    from app.services import llm_service

    async def fake_gemini_normalize(text: str, mode: str, *, context_hint: str | None = None):
        assert text == "nguồn pareto"
        assert mode == "pareto"
        assert context_hint is None
        return llm_service.NormalizedUnit(main_scripts=["ý chính"], review_script="ôn tập")

    async def fail_luna(*args, **kwargs):
        raise AssertionError("Pareto must not call Luna")

    monkeypatch.setattr(llm_service, "_call_normalize_llm", fake_gemini_normalize)
    monkeypatch.setattr(llm_service, "_call_luna_normalize_llm", fail_luna)
    monkeypatch.setattr(
        llm_service,
        "estimate_text_budget",
        lambda text: TextBudget(char_count=len(text), estimated_tokens=100, estimated_audio_seconds=10),
    )

    result = await llm_service.normalize_text_for_speech("nguồn pareto", "pareto")

    assert result == {"main_scripts": ["ý chính"], "review_script": "ôn tập"}


def test_full_mode_splitter_uses_zero_overlap(monkeypatch):
    from app.core.config import settings
    from app.services.chapter_chunking_service import split_full_mode_text_for_llm

    monkeypatch.setattr(settings, "FULL_MODE_CHUNK_TARGET_TOKENS", 30)
    monkeypatch.setattr(settings, "FULL_MODE_CHUNK_OVERLAP_TOKENS", 0)
    text = "\n\n".join(f"Đoạn {index}. " + "nội dung học tập " * 10 for index in range(12))

    chunks = split_full_mode_text_for_llm(text)

    assert len(chunks) > 1
    assert [chunk.index for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.estimated_tokens <= 30 for chunk in chunks)
    assert all(chunks[index].text not in chunks[index + 1].text for index in range(len(chunks) - 1))
