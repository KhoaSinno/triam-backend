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
    DATABASE_ECHO: bool = False
    DATABASE_POOL_MODE: str = "auto"
    DATABASE_POOL_SIZE: int = 3
    DATABASE_MAX_OVERFLOW: int = 2
    DATABASE_POOL_TIMEOUT: int = 5
    DATABASE_POOL_RECYCLE: int = 900
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_USE_LIFO: bool = True
    DATABASE_APPLICATION_NAME: str = "triam-backend"
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
        "Vietnamese audio in the TRIAM audiobook study app. "
        "Expect terms: Tri Âm, chương, sách, định lý, phương pháp, GPT, Gemini."
    )
    VOICE_AGENT_TEXT_LLM_MODEL: str = "gpt-4o-mini"
    VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT: bool = False
    VOICE_AGENT_LOG_TRANSCRIPT_TEXT: bool = False
    VOICE_AGENT_DEDUPE_WINDOW_SECONDS: int = 3
    VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS: int = 180
    VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS: int = 20
    VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS: int = 120
    VOICE_AGENT_PERMISSION_CLASSIFIER_ENABLED: bool = True
    VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL: str = "gpt-4o-mini"
    VOICE_AGENT_PERMISSION_CLASSIFIER_TIMEOUT_SECONDS: float = 1.5
    VOICE_AGENT_PERMISSION_CLASSIFIER_CONFIDENCE_THRESHOLD: float = 0.72
    VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS: float = 0.8
    VOICE_AGENT_INTERRUPTION_MIN_WORDS: int = 2
    VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS: float = 1.5
    VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED: bool = False
    VOICE_AGENT_HISTORY_LIMIT: int = 24
    VOICE_AGENT_RAG_MAX_CHARS: int = 6000
    VOICE_AGENT_CONSOLE_BOOK_ID: str = "1b893d40-e0cc-4ee3-ae5f-a7809834e6dd"
    VOICE_AGENT_CONSOLE_THREAD_ID: str = "5bb8da1d-7326-4d67-b0b3-0b4dd9bb17d7"

    # Upload file
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_MIME_TYPES: Set[str] = {
        "application/pdf",
        "application/epub+zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    LOG_LEVEL: str = "INFO"
    LOG_THIRD_PARTY_LEVEL: str = "WARNING"

    # Celery / Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str | None = None
    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_EAGER_PROPAGATES: bool = False
    CELERY_BROKER_POOL_LIMIT: int = 1
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
    CELERY_DOCUMENT_CONCURRENCY: int = 1
    CELERY_NOTIFICATION_CONCURRENCY: int = 1
    CELERY_LOG_LEVEL: str = "info"
    CELERY_VISIBILITY_TIMEOUT_SECONDS: int = 3600
    CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS: bool = False
    ENABLE_CELERY_WORKER: bool = False
    ENABLE_NOTIFICATION_WORKER: bool = False
    ENABLE_CELERY_BEAT: bool = False

    # Runtime process toggles
    ENABLE_VOICE_AGENT: bool = True
    RUN_MIGRATIONS_ON_START: bool = False
    UVICORN_RELOAD: bool = False
    UV_NO_SYNC: bool = False

    # LiveKit agent runtime hardening
    LIVEKIT_AGENT_JOB_EXECUTOR_TYPE: str = "thread"
    LIVEKIT_AGENT_NUM_IDLE_PROCESSES: int = 1
    LIVEKIT_AGENT_MAX_CONCURRENT_JOBS: int = 2
    LIVEKIT_AGENT_LOAD_THRESHOLD: float = 0.95
    LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT: float = 60.0
    LIVEKIT_AGENT_SHUTDOWN_PROCESS_TIMEOUT: float = 20.0

    # Generation guardrails
    LLM_INPUT_SOFT_TOKEN_LIMIT: int = 12000
    LLM_INPUT_HARD_TOKEN_LIMIT: int = 60000
    LLM_CHUNK_TARGET_TOKENS: int = 5000
    LLM_CHUNK_OVERLAP_TOKENS: int = 300
    MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK: int = 4 * 60 * 60
    FIRST_PLAYABLE_UNITS: int = 1

    # Provider concurrency
    LEARNING_UNIT_PROCESSING_CONCURRENCY: int = 2
    LLM_NORMALIZE_CONCURRENCY: int = 1
    TTS_GENERATION_CONCURRENCY: int = 4
    EMBEDDING_BATCH_SIZE: int = 64

    # Pareto learning unit planner
    PARETO_PLANNER_LLM_ENABLED: bool = True
    PARETO_PLANNER_MODEL: str = "gemini-2.5-flash"
    PARETO_PLANNER_TIMEOUT_SECONDS: float = 8.0
    PARETO_PLANNER_MAX_UNITS: int = 8
    PARETO_PLANNER_MIN_UNITS: int = 3
    PARETO_TARGET_COVERAGE_RATIO: float = 0.25
    PARETO_SECTION_EXCERPT_CHARS: int = 700
    PARETO_PLANNER_MAX_SECTION_CARDS: int = 120

    # Phase 4.1 notification/reminder workflow
    NOTIFICATION_SCAN_INTERVAL_SECONDS: int = 60
    NOTIFICATION_DELIVERY_BATCH_SIZE: int = 50
    NOTIFICATION_MAX_ATTEMPTS: int = 5
    NOTIFICATION_STALE_LOCK_MINUTES: int = 10
    NOTIFICATION_DEFAULT_TIMEZONE: str = "Asia/Ho_Chi_Minh"
    NOTIFICATION_DEFAULT_REMINDER_TIME: str = "20:00"
    NOTIFICATION_DEFAULT_DAILY_CAP: int = 3
    NOTIFICATION_DEFAULT_QUIET_START: str = "22:00"
    NOTIFICATION_DEFAULT_QUIET_END: str = "07:00"

    # Firebase Cloud Messaging
    FIREBASE_CREDENTIALS_JSON: str | None = None
    FIREBASE_CREDENTIALS_FILE: str | None = None

    # Phase 4.2 production learning loop
    MAX_ACTIVE_LEARNING_BOOKS_PER_USER: int = 3
    LEARNING_COMPLETION_THRESHOLD_PERCENT: int = 80
    LEARNING_PROGRESS_MIN_DELTA_PERCENT: int = 5
    LEARNING_PROGRESS_STALE_SECONDS: int = 30
    PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS: int = 24

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
