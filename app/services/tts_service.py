from openai import AsyncOpenAI
from app.core.config import settings
import edge_tts

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def stream_text_to_speech(text: str, voice: str = "alloy"):
    """
    Hàm này nhận text, gọi OpenAI TTS và trả về stream audio ngay lập tức.
    """
    try:
        # Gọi API OpenAI với response_format để stream
        async with client.audio.speech.with_streaming_response.create(
            model="tts-1",  # Model nhanh nhất, độ trễ thấp
            voice=voice,
            input=text
        ) as response:
            # Streaming response (Chunking 4096 bytes để gửi dần xuống client)
            async for chunk in response.iter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk

    except Exception as e:
        print(f"Error in TTS Stream: {e}")
        # Trong thực tế nên log vào file hoặc Sentry

async def stream_text_to_speech_edge(text: str, voice: str = "vi-VN-HoaiMyNeural"):
    """
    Sử dụng Edge TTS: Hoàn toàn MIỄN PHÍ và chất lượng Neural rất tốt.
    """
    communicate = edge_tts.Communicate(text, voice)
    
    # Streaming response
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]