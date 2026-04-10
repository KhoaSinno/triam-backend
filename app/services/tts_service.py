
import asyncio

import edge_tts
from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


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
        print(f"Error in TTS Stream: {e}")


async def stream_text_to_speech_edge(text: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Sử dụng Edge TTS: Hoàn toàn MIỄN PHÍ và chất lượng Neural rất tốt.
    """
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


async def generate_audio_file_edge(text: str, filename: str, voice: str = settings.EDGE_TTS_VOICE):
    """
    Tạo file audio từ text bằng Edge TTS và lưu vào file.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"✓ Audio saved to {filename}")
    except Exception as e:
        print(f"Error creating audio file: {e}")


# -----------------------------------------------------------------------
# Giới hạn concurrent TTS calls.
# Microsoft Edge TTS service đang bị intermittent failure (Apr 2026).
# Ref: https://github.com/rany2/edge-tts/issues/473
# Semaphore(5) giúp giảm áp lực lên server, tăng tỉ lệ thành công.
# -----------------------------------------------------------------------
_tts_sem = asyncio.Semaphore(5)


async def generate_audio_and_get_duration(
    text: str,
    filename: str,
    voice: str = settings.EDGE_TTS_VOICE,
    max_retries: int = 6,
) -> int:
    """
    Tạo file audio bằng Edge TTS và đo thời lượng (milliseconds).

    - Semaphore(5): giới hạn 5 TTS calls đồng thời (tránh overwhelm server)
    - 6 retries với backoff dài: 3s, 6s, 12s, 24s, 48s
    - receive_timeout=300: chờ Microsoft server đủ lâu
    - KHÔNG dùng voice fallback: giữ giọng đọc nhất quán

    Trả về duration_ms.
    """
    from mutagen.mp3 import MP3

    # Clean and Valid text: too short (page numbers, special characters)
    cleaned = text.strip()
    if len(cleaned) < 10:
        raise ValueError(f"Text too short for TTS ({len(cleaned)} chars): '{cleaned}'")

    async with _tts_sem:
        for attempt in range(max_retries):
            try:
                communicate = edge_tts.Communicate(
                    cleaned,
                    voice,
                    receive_timeout=300,
                )
                await communicate.save(filename)

                try:
                    audio = MP3(filename)
                    duration_ms = int(audio.info.length * 1000)
                except Exception:
                    duration_ms = 0

                return duration_ms

            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 3 * (2 ** attempt)  # 3s, 6s, 12s, 24s, 48s
                    print(
                        f"⚠️ TTS attempt {attempt + 1}/{max_retries} failed "
                        f"({len(cleaned)} chars): {e}. Retry in {wait}s..."
                    )
                    await asyncio.sleep(wait)
                else:
                    print(f"❌ TTS failed after {max_retries} attempts ({len(cleaned)} chars): {e}")
                    raise
    return 0  # unreachable
