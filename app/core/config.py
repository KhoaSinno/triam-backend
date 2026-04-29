import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or ""
    PINECONE_ENV = os.getenv("PINECONE_ENV") or ""
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or ""
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL") or ""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
    DATABASE_URL = os.getenv("DATABASE_URL") or ""
    SUPABASE_URL = os.getenv("SUPABASE_URL") or ""
    SUPABASE_KEY = os.getenv("SUPABASE_KEY") or ""
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
    EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-AvaMultilingualNeural") or ""
    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY") or ""
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET") or ""
    LIVEKIT_AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME") or ""
    GEMINI_MODEL_NATIVE_AUDIO = os.getenv("GEMINI_MODEL_NATIVE_AUDIO", "gemini-2.5-flash-native-audio-latest") or ""

    # Upload file
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }


settings = Settings()
