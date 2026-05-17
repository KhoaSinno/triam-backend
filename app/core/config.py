from typing import Set

from dotenv import load_dotenv
from pydantic.v1.env_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    TAVILY_API_KEY: str
    GEMINI_BASE_URL: str
    GEMINI_API_KEY: str
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    EDGE_TTS_VOICE: str = "en-US-AvaMultilingualNeural"
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_AGENT_NAME: str
    GEMINI_MODEL_NATIVE_AUDIO: str = "gemini-2.5-flash-native-audio-latest"
    GEMINI_MODEL_LLM: str = "gemini-2.5-flash"
    DEEPGRAM_API_KEY: str
    CARTESIA_API_KEY_TTS: str
    ELEVENLABS_API_KEY_TTS: str
    OPENAI_STREAM_MODEL_NAME: str = "gpt-realtime"
    OPENAI_REALTIME_VOICE: str = "cedar"
    OPENAI_REALTIME_TRANSCRIPTION_MODEL: str = "gpt-4o-transcribe"
    OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE: str = "vi"
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT: str = (
        "Cuộc trò chuyện bằng tiếng Việt trong ứng dụng sách nói TRIAM. "
        "Người dùng hỏi về sách, chương, nội dung học tập, phương pháp nghiên cứu, "
        "hình học Euclid và có thể nói các từ như Tri Âm, chương, sách, định lý."
    )

    # Upload file
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES: Set[str] = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
