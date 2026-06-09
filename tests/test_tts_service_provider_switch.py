from pathlib import Path

import pytest

from app.core.exceptions import ExternalServiceError, TTSInputTooShortError
from app.services import tts_service


@pytest.mark.asyncio
async def test_generate_audio_uses_edge_provider(monkeypatch, tmp_path):
    calls: list[tuple[str, str, str]] = []

    async def fake_edge(text: str, filename: str, voice_name: str) -> None:
        calls.append((text, filename, voice_name))
        Path(filename).write_bytes(b"fake edge mp3")

    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "edge")
    monkeypatch.setattr(tts_service.settings, "EDGE_TTS_VOICE", "vi-VN-HoaiMyNeural")
    monkeypatch.setattr(tts_service.settings, "TTS_GENERATION_CONCURRENCY", 1)
    monkeypatch.setattr(tts_service, "_generate_audio_file_edge", fake_edge)
    monkeypatch.setattr(tts_service, "_measure_mp3_duration_ms", lambda filename: 1234)

    output = tmp_path / "edge.mp3"
    duration = await tts_service.generate_audio_and_get_duration("[pause] Đây là đoạn kiểm thử Edge TTS.", str(output))

    assert duration == 1234
    assert calls == [("Đây là đoạn kiểm thử Edge TTS.", str(output), "vi-VN-HoaiMyNeural")]


@pytest.mark.asyncio
async def test_generate_audio_removes_visual_markdown_before_provider(monkeypatch, tmp_path):
    calls: list[str] = []

    async def fake_edge(text: str, filename: str, voice_name: str) -> None:
        calls.append(text)
        Path(filename).write_bytes(b"fake edge mp3")

    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "edge")
    monkeypatch.setattr(tts_service.settings, "EDGE_TTS_VOICE", "vi-VN-HoaiMyNeural")
    monkeypatch.setattr(tts_service.settings, "TTS_GENERATION_CONCURRENCY", 1)
    monkeypatch.setattr(tts_service, "_generate_audio_file_edge", fake_edge)
    monkeypatch.setattr(tts_service, "_measure_mp3_duration_ms", lambda filename: 1234)

    duration = await tts_service.generate_audio_and_get_duration(
        "Trục đầu tiên là **kiến trúc mô hình** và `huấn luyện`.",
        str(tmp_path / "clean.mp3"),
    )

    assert duration == 1234
    assert calls == ["Trục đầu tiên là kiến trúc mô hình và huấn luyện."]


@pytest.mark.asyncio
async def test_generate_audio_uses_google_provider(monkeypatch, tmp_path):
    calls: list[tuple[str, str, str]] = []
    logged: list[tuple[tuple, dict]] = []

    def fake_google(text: str, filename: str, voice_name: str) -> int:
        calls.append((text, filename, voice_name))
        Path(filename).write_bytes(b"fake google mp3")
        return 99

    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "google")
    monkeypatch.setattr(tts_service.settings, "TTS_GOOGLE_API_KEY", "test-google-key")
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_VOICE", "vi-VN-Chirp3-HD-Iapetus")
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_MAX_BYTES_PER_REQUEST", 4500)
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_ENABLE_COST_LOG", True)
    monkeypatch.setattr(tts_service.settings, "TTS_GENERATION_CONCURRENCY", 1)
    monkeypatch.setattr(tts_service, "_generate_audio_file_google_sync", fake_google)
    monkeypatch.setattr(tts_service, "_measure_mp3_duration_ms", lambda filename: 2345)
    monkeypatch.setattr(tts_service.log, "info", lambda *args, **kwargs: logged.append((args, kwargs)))

    sensitive_text = "Xin chào, đây là đoạn kiểm thử Google TTS không được log nguyên văn."
    output = tmp_path / "google.mp3"
    duration = await tts_service.generate_audio_and_get_duration(sensitive_text, str(output))

    assert duration == 2345
    assert calls == [(sensitive_text, str(output), "vi-VN-Chirp3-HD-Iapetus")]
    logged_text = repr(logged)
    assert sensitive_text not in logged_text
    assert "test-google-key" not in logged_text


@pytest.mark.asyncio
async def test_google_alias_gg_maps_to_google(monkeypatch, tmp_path):
    calls: list[str] = []

    def fake_google(text: str, filename: str, voice_name: str) -> int:
        calls.append(voice_name)
        Path(filename).write_bytes(b"fake google mp3")
        return 10

    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "gg")
    monkeypatch.setattr(tts_service.settings, "TTS_GOOGLE_API_KEY", "test-google-key")
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_VOICE", "vi-VN-Chirp3-HD-Iapetus")
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_MAX_BYTES_PER_REQUEST", 4500)
    monkeypatch.setattr(tts_service.settings, "TTS_GENERATION_CONCURRENCY", 1)
    monkeypatch.setattr(tts_service, "_generate_audio_file_google_sync", fake_google)
    monkeypatch.setattr(tts_service, "_measure_mp3_duration_ms", lambda filename: 111)

    duration = await tts_service.generate_audio_and_get_duration("Đây là đoạn kiểm thử alias Google.", str(tmp_path / "gg.mp3"))

    assert duration == 111
    assert calls == ["vi-VN-Chirp3-HD-Iapetus"]


@pytest.mark.asyncio
async def test_invalid_provider_fails_clearly(monkeypatch, tmp_path):
    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "unknown")

    with pytest.raises(ExternalServiceError, match="TTS_PROVIDER"):
        await tts_service.generate_audio_and_get_duration("Đây là đoạn kiểm thử provider lỗi.", str(tmp_path / "bad.mp3"))


@pytest.mark.asyncio
async def test_short_text_fails_before_provider_call(monkeypatch, tmp_path):
    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "edge")
    monkeypatch.setattr(tts_service.settings, "TTS_MIN_TEXT_CHARS", 10)

    with pytest.raises(TTSInputTooShortError):
        await tts_service.generate_audio_and_get_duration("ngắn", str(tmp_path / "short.mp3"))


@pytest.mark.asyncio
async def test_google_missing_api_key_fails_before_provider_call(monkeypatch, tmp_path):
    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "google")
    monkeypatch.setattr(tts_service.settings, "TTS_GOOGLE_API_KEY", None)

    with pytest.raises(ExternalServiceError, match="TTS_GOOGLE_API_KEY"):
        await tts_service.generate_audio_and_get_duration("Đây là đoạn kiểm thử thiếu Google key.", str(tmp_path / "missing.mp3"))


@pytest.mark.asyncio
async def test_google_oversized_input_fails_before_provider_call(monkeypatch, tmp_path):
    monkeypatch.setattr(tts_service.settings, "TTS_PROVIDER", "google")
    monkeypatch.setattr(tts_service.settings, "TTS_GOOGLE_API_KEY", "test-google-key")
    monkeypatch.setattr(tts_service.settings, "GOOGLE_TTS_MAX_BYTES_PER_REQUEST", 20)

    with pytest.raises(ExternalServiceError, match="quá dài"):
        await tts_service.generate_audio_and_get_duration("Đây là đoạn kiểm thử vượt quá giới hạn bytes.", str(tmp_path / "large.mp3"))


def test_safe_tts_error_redacts_google_api_key(monkeypatch):
    monkeypatch.setattr(tts_service.settings, "TTS_GOOGLE_API_KEY", "secret-google-key")

    message = tts_service._safe_tts_error(RuntimeError("failed with secret-google-key"))

    assert "secret-google-key" not in message
    assert "[REDACTED]" in message
