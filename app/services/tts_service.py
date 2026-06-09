import asyncio
from pathlib import Path

import edge_tts
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import ExternalServiceError, TTSInputTooShortError
from app.core.logger import log
from app.services.async_limiter import get_loop_semaphore
from app.services.tts_script_quality_service import sanitize_tts_script_text

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SUPPORTED_TTS_PROVIDERS = {"edge", "google", "gg"}
_google_tts_client = None


async def stream_text_to_speech(text: str, voice: str = "alloy"):
    """
    Hàm này nhận text, gọi OpenAI TTS và trả về stream audio ngay lập tức.
    """
    try:
        async with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text,
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk

    except Exception as e:
        log.error(f"Error in TTS Stream: {e}")


async def stream_text_to_speech_edge(text: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Sử dụng Edge TTS: Hoàn toàn MIỄN PHÍ và chất lượng Neural rất tốt.
    """
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


def _clean_text_for_tts(text: str) -> str:
    return sanitize_tts_script_text(text)


def _utf8_size(text: str) -> int:
    return len(text.encode("utf-8"))


def _validate_tts_text(text: str) -> None:
    if len(text) < settings.TTS_MIN_TEXT_CHARS:
        raise TTSInputTooShortError(f"Nội dung quá ngắn để tạo audio ({len(text)} ký tự).")


def _selected_tts_provider() -> str:
    provider = settings.TTS_PROVIDER.strip().lower()
    if provider not in SUPPORTED_TTS_PROVIDERS:
        raise ExternalServiceError(f"TTS_PROVIDER không hợp lệ: {settings.TTS_PROVIDER}")
    return "google" if provider == "gg" else provider


def _validate_provider_config(provider: str, text: str) -> None:
    if provider != "google":
        return
    if not settings.TTS_GOOGLE_API_KEY:
        raise ExternalServiceError("Thiếu TTS_GOOGLE_API_KEY để gọi Google Text-to-Speech.")
    byte_count = _utf8_size(text)
    if byte_count > settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST:
        raise ExternalServiceError(
            "Google TTS input quá dài cho một request "
            f"({byte_count} bytes > {settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST} bytes)."
        )


def _get_google_tts_client():
    global _google_tts_client

    if _google_tts_client is not None:
        return _google_tts_client

    try:
        from google.api_core.client_options import ClientOptions
        from google.cloud import texttospeech
    except ImportError as exc:
        raise ExternalServiceError("Thiếu dependency google-cloud-texttospeech.") from exc

    if not settings.TTS_GOOGLE_API_KEY:
        raise ExternalServiceError("Thiếu TTS_GOOGLE_API_KEY để gọi Google Text-to-Speech.")

    options = ClientOptions(api_key=settings.TTS_GOOGLE_API_KEY)
    _google_tts_client = texttospeech.TextToSpeechClient(client_options=options)
    return _google_tts_client


def _measure_mp3_duration_ms(filename: str) -> int:
    from mutagen.mp3 import MP3

    try:
        audio = MP3(filename)
        return int(audio.info.length * 1000)
    except Exception:
        return 0


def _retry_wait_seconds(attempt: int) -> int:
    return settings.TTS_RETRY_BASE_SECONDS * (2**attempt)


def _safe_tts_error(exc: Exception) -> str:
    message = str(exc)
    if settings.TTS_GOOGLE_API_KEY:
        message = message.replace(settings.TTS_GOOGLE_API_KEY, "[REDACTED]")
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


async def _generate_audio_file_edge(text: str, filename: str, voice_name: str) -> None:
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text,
        voice_name,
        receive_timeout=settings.TTS_RECEIVE_TIMEOUT_SECONDS,
    )
    await communicate.save(filename)


def _generate_audio_file_google_sync(text: str, filename: str, voice_name: str) -> int:
    from google.cloud import texttospeech

    _validate_provider_config("google", text)
    client = _get_google_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=settings.GOOGLE_TTS_LANGUAGE_CODE,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    Path(filename).write_bytes(response.audio_content)
    return len(response.audio_content)


async def generate_audio_file_edge(text: str, filename: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Tạo file audio từ text bằng Edge TTS và lưu vào file.
    """
    cleaned = _clean_text_for_tts(text)
    _validate_tts_text(cleaned)
    await _generate_audio_file_edge(cleaned, filename, voice)
    log.info("Edge TTS file generated | chars={} | bytes={} | voice={}", len(cleaned), _utf8_size(cleaned), voice)


async def generate_audio_and_get_duration(
    text: str,
    filename: str,
    voice: str | None = None,
    max_retries: int = 6,
) -> int:
    """
    Tạo file audio bằng provider đang cấu hình và đo thời lượng (milliseconds).

    - Semaphore(settings.TTS_GENERATION_CONCURRENCY): giới hạn TTS calls đồng thời
    - Provider: settings.TTS_PROVIDER = edge | google
    - Không tự fallback provider: giữ giọng đọc nhất quán
    - KHÔNG dùng voice fallback: giữ giọng đọc nhất quán

    Trả về duration_ms.
    """
    cleaned = _clean_text_for_tts(text)
    _validate_tts_text(cleaned)
    provider = _selected_tts_provider()
    _validate_provider_config(provider, cleaned)
    target_voice = voice or (settings.GOOGLE_TTS_VOICE if provider == "google" else settings.EDGE_TTS_VOICE)

    async with get_loop_semaphore("tts_generation", settings.TTS_GENERATION_CONCURRENCY):
        for attempt in range(max_retries):
            try:
                if provider == "google":
                    audio_bytes = await asyncio.to_thread(
                        _generate_audio_file_google_sync,
                        cleaned,
                        filename,
                        target_voice,
                    )
                    if settings.GOOGLE_TTS_ENABLE_COST_LOG:
                        log.info(
                            "Google TTS generated | chars={} | bytes={} | audio_bytes={} | voice={}",
                            len(cleaned),
                            _utf8_size(cleaned),
                            audio_bytes,
                            target_voice,
                        )
                else:
                    await _generate_audio_file_edge(cleaned, filename, target_voice)
                    log.info(
                        "Edge TTS generated | chars={} | bytes={} | voice={}",
                        len(cleaned),
                        _utf8_size(cleaned),
                        target_voice,
                    )

                return _measure_mp3_duration_ms(filename)

            except Exception as exc:
                if attempt < max_retries - 1:
                    wait = _retry_wait_seconds(attempt)
                    log.warning(
                        "TTS attempt failed | provider={} | attempt={}/{} | chars={} | wait_seconds={} | error={}",
                        provider,
                        attempt + 1,
                        max_retries,
                        len(cleaned),
                        wait,
                        _safe_tts_error(exc),
                    )
                    await asyncio.sleep(wait)
                else:
                    log.error(
                        "TTS failed | provider={} | attempts={} | chars={} | voice={} | error={}",
                        provider,
                        max_retries,
                        len(cleaned),
                        target_voice,
                        _safe_tts_error(exc),
                    )
                    raise
    return 0  # unreachable
