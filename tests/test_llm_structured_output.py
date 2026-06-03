from types import SimpleNamespace

import pytest

from app.services import llm_service


@pytest.mark.asyncio
async def test_call_normalize_llm_uses_schema_and_retries_invalid_json(monkeypatch):
    calls = []

    async def fake_parse(**kwargs):
        calls.append(kwargs)
        assert kwargs["response_format"] is llm_service.NormalizedUnitPayload

        if len(calls) == 1:
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(parsed=None, content="không phải json"),
                    )
                ]
            )

        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        parsed=llm_service.NormalizedUnitPayload(
                            main_scripts=[" Nội dung nghe đã chuẩn hóa. "],
                            review_script=" Nội dung ôn tập. ",
                        ),
                        content=None,
                    ),
                )
            ]
        )

    monkeypatch.setattr(llm_service.client.beta.chat.completions, "parse", fake_parse)

    result = await llm_service._call_normalize_llm("Nội dung chương.", "pareto")

    assert len(calls) == 2
    assert result.main_scripts == ["Nội dung nghe đã chuẩn hóa."]
    assert result.review_script == "Nội dung ôn tập."


@pytest.mark.asyncio
async def test_call_normalize_llm_sanitizes_tts_scripts(monkeypatch):
    async def fake_parse(**kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        parsed=llm_service.NormalizedUnitPayload(
                            main_scripts=["## Mở đầu\nTrục đầu tiên là **kiến trúc mô hình** và `huấn luyện`."],
                            review_script="Ôn lại **khái niệm chính** [1].",
                        ),
                        content=None,
                    ),
                )
            ]
        )

    monkeypatch.setattr(llm_service.client.beta.chat.completions, "parse", fake_parse)

    result = await llm_service._call_normalize_llm("Nội dung chương.", "full")

    assert result.main_scripts == ["Mở đầu Trục đầu tiên là kiến trúc mô hình và huấn luyện."]
    assert result.review_script == "Ôn lại khái niệm chính."


def test_extract_json_object_accepts_markdown_fenced_json():
    payload = llm_service._extract_json_object(
        """```json
        {"main_scripts":["Một đoạn."],"review_script":"Ôn tập."}
        ```"""
    )

    assert payload == {"main_scripts": ["Một đoạn."], "review_script": "Ôn tập."}
