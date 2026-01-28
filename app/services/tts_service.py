from openai import AsyncOpenAI
from app.core.config import settings
import edge_tts
import asyncio # Need to install

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


# Production ready
# async def generate_audio_file(text: str, file_path: str):
#     """
#     Tạo audio và lưu xuống ổ cứng (sau này là upload lên Firebase Storage).
#     """
#     try:
#         response = await client.audio.speech.create(
#             model="tts-1",
#             voice="alloy",
#             input=text
#         )
#         # Lưu file binary xuống đĩa
#         response.stream_to_file(file_path)
#         return True
#     except Exception as e:
#         print(f"Lỗi TTS: {e}")
#         return False


# Create audio file wiht edge tts


async def generate_audio_file_edge(text: str, filename: str, voice: str = "vi-VN-HoaiMyNeural"):
    """
    Tạo file audio từ text bằng Edge TTS và lưu vào file.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"✓ Audio saved to {filename}")
    except Exception as e:
        print(f"Error creating audio file: {e}")

# Example usage:
# asyncio.run(create_audio_file("Xin chào, đây là bài test giọng nói.", "test.mp3"))
