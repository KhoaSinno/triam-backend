import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-AvaMultilingualNeural")
    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
    LIVEKIT_AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME")
    GEMINI_MODEL_NATIVE_AUDIO = os.getenv("GEMINI_MODEL_NATIVE_AUDIO", "gemini-2.5-flash-native-audio-latest")

    # Upload file
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }


settings = Settings()
