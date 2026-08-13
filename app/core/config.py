from typing import Literal, Set

from dotenv import load_dotenv
from pydantic.v1 import Field
from pydantic.v1.env_settings import BaseSettings

load_dotenv(override=True)

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    GEMINI_BASE_URL: str
    GEMINI_API_KEY: str
    DATABASE_URL: str
    # hardening DB pool/config
    DATABASE_ECHO: bool = False
    DATABASE_POOL_MODE: str = "auto"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 280
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_USE_LIFO: bool = True
    DATABASE_APPLICATION_NAME: str = "triam-backend"
    DATABASE_TCP_KEEPALIVES: bool = True
    DATABASE_TCP_KEEPALIVES_IDLE: int = 30
    DATABASE_TCP_KEEPALIVES_INTERVAL: int = 10
    DATABASE_TCP_KEEPALIVES_COUNT: int = 5

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # TTS
    EDGE_TTS_VOICE: str = "en-US-AvaMultilingualNeural"
    TTS_PROVIDER: str = "edge"
    TTS_RECEIVE_TIMEOUT_SECONDS: int = 300
    TTS_RETRY_BASE_SECONDS: int = 3
    TTS_MIN_TEXT_CHARS: int = 10
    TTS_GOOGLE_API_KEY: str | None = None
    GOOGLE_TTS_LANGUAGE_CODE: str = "vi-VN"
    GOOGLE_TTS_VOICE: str = "vi-VN-Chirp3-HD-Iapetus"
    GOOGLE_TTS_MAX_BYTES_PER_REQUEST: int = 4500
    GOOGLE_TTS_ENABLE_COST_LOG: bool = True
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_AGENT_NAME: str = "triam-voice-agent"
    LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS: int = 60
    LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS: int = 20
    LIVEKIT_AGENT_EMPTY_ROOM_GRACE_SECONDS: float = 8.0
    GEMINI_MODEL_LLM: str = "gemini-3.5-flash-lite"
    TOTAL_TOKEN_LIMIT: int = 800_000
    AI_SUMMARY_MAX_RETRIES: int = 2
    AI_SUMMARY_RETRY_DELAY_SECONDS: int = 15
    AI_SUMMARY_AUTO_ENQUEUE_ENABLED: bool = False

    # Realtime voice agent behavior
    OPENAI_STREAM_MODEL_NAME: str = "gpt-realtime-2.1-mini"
    OPENAI_REALTIME_VOICE: str = "cedar"
    OPENAI_REALTIME_REASONING_EFFORT: Literal["minimal", "low", "medium", "high", "xhigh"] = "minimal"
    # Phase 30.0.2: disabled by default so current Realtime session behavior is preserved.
    # When enabled, OpenAI retains recent conversation items once this remote-session
    # token budget is reached; this does not affect text chat or local history.
    VOICE_AGENT_REALTIME_CONTEXT_BUDGET_ENABLED: bool = False
    VOICE_AGENT_REALTIME_CONTEXT_MAX_POST_INSTRUCTIONS_TOKENS: int = Field(
        default=8000,
        ge=4000,
        le=24000,
    )
    VOICE_AGENT_REALTIME_CONTEXT_RETENTION_RATIO: float = Field(
        default=0.75,
        ge=0.50,
        lt=1.00,
    )
    # Text and local console test behavior
    VOICE_AGENT_HISTORY_LIMIT: int = 6
    VOICE_AGENT_RAG_MAX_CHARS: int = 8000

    # Local console fallback only. Production LiveKit rooms must provide
    # thread_id and document_ids through job metadata from the backend token flow.
    VOICE_AGENT_CONSOLE_BOOK_ID: str = "c3f13d07-4494-4995-ba75-30a12589b8fc"
    VOICE_AGENT_CONSOLE_THREAD_ID: str = "883a77ab-e773-4404-aaa2-0b032db13a89"

    # Dynamic Prompt cho OpenAI Realtime Transcription
    # OPENAI_REALTIME_TRANSCRIPTION_MODEL: str = "gpt-4o-transcribe"
    OPENAI_REALTIME_TRANSCRIPTION_MODEL: str = "gpt-live-transcribe"
    OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE: str = "vi"
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT: str = "Vietnamese audio in the TRIAM audiobook study app. Expect terms: Tri Âm, chương, sách, định lý, phương pháp, GPT, Gemini."
    OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS: int = 900
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS: int = 45
    OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS: int = 20
    # Phase 33.1: legacy-SDK-compatible, scoped vocabulary prompt. Disabled
    # by default so the current transcription prompt is preserved until canary.
    VOICE_AGENT_TRANSCRIPTION_CONTEXT_HINTS_ENABLED: bool = True
    VOICE_AGENT_TRANSCRIPTION_LEGACY_PROMPT_TERM_LIMIT: int = Field(default=8, ge=0, le=20)
    OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION: str = "near_field"

    VOICE_AGENT_TEXT_LLM_MODEL: str = "gpt-4o-mini"
    # Enables tool-calling orchestration for messages received on lk.chat only.
    # Voice continues to use the Realtime AgentSession tool loop.
    VOICE_AGENT_TEXT_CHAT_AGENTIC_ENABLED: bool = True
    VOICE_AGENT_TEXT_CHAT_AGENTIC_MAX_STEPS: int = 4
    VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT: bool = True
    VOICE_AGENT_LOG_TRANSCRIPT_TEXT: bool = True
    # Chat text diagnostics are opt-in because they include user/assistant text.
    # They intentionally never include RAG context, history, or tool payloads.
    VOICE_AGENT_LOG_CHAT_TEXT: bool = True
    VOICE_AGENT_LOG_CHAT_TEXT_MAX_CHARS: int = 400
    VOICE_AGENT_DEDUPE_WINDOW_SECONDS: int = 3
    VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS: int = 180

    # Policy websearch
    VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS: int = 20
    VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS: int = 120
    VOICE_AGENT_PERMISSION_CLASSIFIER_ENABLED: bool = True
    VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL: str = "gpt-4o-mini"
    VOICE_AGENT_PERMISSION_CLASSIFIER_TIMEOUT_SECONDS: float = 5.0
    VOICE_AGENT_PERMISSION_CLASSIFIER_CONFIDENCE_THRESHOLD: float = 0.72
    VOICE_AGENT_QUERY_GUARD_ENABLED: bool = True
    VOICE_AGENT_QUERY_GUARD_MIN_CHARS: int = 6
    VOICE_AGENT_QUERY_GUARD_MIN_TOKENS: int = 2

    VOICE_AGENT_QUERY_GUARD_TRANSCRIPT_TTL_SECONDS: float = 15.0
    VOICE_AGENT_QUERY_GUARD_LOG_DETAILS: bool = True
    VOICE_AGENT_CLARIFICATION_STATE_ENABLED: bool = True
    VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS: float = 30.0
    VOICE_AGENT_CLARIFICATION_CONFIRMATION_MAX_TOKENS: int = 4
    VOICE_AGENT_CLARIFICATION_MIN_QUERY_PROMPT_OVERLAP: float = 0.45

    VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED: bool = False
    VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS: float = 0.8
    VOICE_AGENT_INTERRUPTION_MIN_WORDS: int = 2
    VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS: float = 1.5
    VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED: bool = False

    # P0: keep Realtime VAD endpointing, but defer response creation until the
    # provider has emitted the final input transcript.  Disabled for a safe
    # rollout because it changes voice turn timing.
    VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED: bool = True

    # Phase 10.11 Voice Tool Reply Watchdog config
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED: bool = False
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS: float = 8.0
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS: float = 12.0
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_TOOLS: str = "search_book_knowledge,ask_web_search_permission,execute_web_search"
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS: bool = False
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE: bool = True
    VOICE_AGENT_TOOL_REPLY_WATCHDOG_RATE_LIMIT_COOLDOWN_SECONDS: float = 60.0
    VOICE_AGENT_CLOSE_ON_DISCONNECT: bool = False

    # Phase 10.0 safe agent trace. It never logs raw transcript, answer, or source content.
    AGENT_MODEL_PROFILE: str = "baseline"
    AGENT_TRACE_ENABLED: bool = True
    AGENT_TRACE_SCORE_PRECISION: int = 4
    AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS: float = 15.0
    AGENT_GROUNDING_ROUTER_ENABLED: bool = True
    AGENT_SHARED_POLICY_ENABLED: bool = True
    AGENT_INTENT_CLASSIFIER_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    AGENT_INTENT_CLASSIFIER_THRESHOLD: float = 0.60
    AGENT_SECTION_CONTEXT_MAX_CHARS: int = 24000
    # Phase 32: deterministic answers about every document in the active Study Context.
    # Disabled by default so rollout does not alter existing book/RAG routing.
    AGENT_CONTEXT_OVERVIEW_ENABLED: bool = True
    AGENT_CONTEXT_OVERVIEW_MAX_VISIBLE_DOCUMENTS: int = Field(default=6, ge=1, le=12)

    # Phase 10.3 hybrid retrieval. Keep disabled until search_text is backfilled.
    AGENT_HYBRID_MIN_FINAL_SCORE: float = 0.25
    AGENT_HYBRID_LEXICAL_CANDIDATES: int = 20
    AGENT_HYBRID_MAX_CONTEXT_CHUNKS: int = 12
    AGENT_HYBRID_MAX_CHUNKS_PER_SECTION: int = 2
    AGENT_HYBRID_VALIDATE_EVIDENCE_ENABLED: bool = False
    # Reranker
    COHERE_API_KEY: str | None = None
    AGENT_RERANKER_ENABLED: bool = True
    AGENT_RERANKER_MODEL: str = "rerank-multilingual-v3.0"
    AGENT_RERANKER_TOP_N: int = 8  # Maximum cadidates Reranker reuturn
    AGENT_RERANKER_CANDIDATES_LIMIT: int = 20  # Maximum cadidates sent to Cohere
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

    # WOKER WORKING
    ENABLE_CELERY_WORKER: bool = True
    ENABLE_NOTIFICATION_WORKER: bool = True
    ENABLE_CELERY_BEAT: bool = True

    # Runtime process toggles
    ENABLE_VOICE_AGENT: bool = True
    RUN_MIGRATIONS_ON_START: bool = False
    UVICORN_RELOAD: bool = False
    UV_NO_SYNC: bool = True
    BACKEND_PORT: int = 7860 # HUGGINGFACE SPACE

    # LiveKit agent runtime hardening
    LIVEKIT_AGENT_JOB_EXECUTOR_TYPE: str = "thread"
    LIVEKIT_AGENT_NUM_IDLE_PROCESSES: int = 1
    LIVEKIT_AGENT_MAX_CONCURRENT_JOBS: int = 2
    LIVEKIT_AGENT_LOAD_THRESHOLD: float = 0.95
    LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT: float = 60.0
    LIVEKIT_AGENT_SHUTDOWN_PROCESS_TIMEOUT: float = 20.0

    # Generation guardrails
    LLM_INPUT_SOFT_TOKEN_LIMIT: int = 30000
    LLM_INPUT_HARD_TOKEN_LIMIT: int = 150000
    LLM_CHUNK_TARGET_TOKENS: int = 5000
    LLM_CHUNK_OVERLAP_TOKENS: int = 300
    # Full mode config
    FULL_UNIT_TARGET_TOKENS: int = 5000
    FULL_UNIT_MAX_TOKENS: int = 12000
    FULL_MODE_LLM_MODEL: str = "gpt-5.6-luna"
    FULL_MODE_CHUNK_TARGET_TOKENS: int = Field(default=5000, ge=1000)
    FULL_MODE_CHUNK_OVERLAP_TOKENS: int = Field(default=0, ge=0, le=0)
    FULL_MODE_REVIEW_MAX_OUTPUT_TOKENS: int = Field(default=1600, ge=256)
    STORAGE_UPLOAD_CONCURRENCY: int = Field(default=2, ge=1, le=8)
    MIN_UNIT_TOKENS: int = 300
    MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK: int = 10 * 60 * 60
    FIRST_PLAYABLE_UNITS: int = 1

    # Provider concurrency
    LEARNING_UNIT_PROCESSING_CONCURRENCY: int = 2
    LLM_NORMALIZE_CONCURRENCY: int = 1
    TTS_GENERATION_CONCURRENCY: int = 8
    BOOK_SECTION_INDEXING_ENABLED: bool = True
    BOOK_SECTION_EMBEDDING_MODEL: str = "text-embedding-3-small"
    BOOK_SECTION_EMBEDDING_VERSION: str = "section-v1"
    BOOK_SECTION_CHUNK_SIZE_CHARS: int = 3600
    BOOK_SECTION_CHUNK_OVERLAP_CHARS: int = 500
    BOOK_SECTION_EMBEDDING_BATCH_SIZE: int = 64
    BOOK_SECTION_RAG_MATCH_THRESHOLD: float = 0.3
    BOOK_SECTION_RAG_MATCH_COUNT: int = 10

    # Pareto learning unit planner
    PARETO_PLANNER_MODEL: str = "gemini-3.6-flash"
    PARETO_PLANNER_TIMEOUT_SECONDS: float = 90.0
    PARETO_PLANNER_MAX_UNITS: int = 8
    PARETO_PLANNER_MIN_UNITS: int = 3
    PARETO_TARGET_COVERAGE_RATIO: float = 0.40
    PARETO_SECTION_EXCERPT_CHARS: int = 1400
    PARETO_PLANNER_MAX_SECTION_CARDS: int = 120

    # Phase 4.1 notification/reminder workflow
    NOTIFICATION_SCAN_INTERVAL_SECONDS: int = 60
    NOTIFICATION_DELIVERY_BATCH_SIZE: int = 50
    NOTIFICATION_MAX_ATTEMPTS: int = 5
    NOTIFICATION_STALE_LOCK_MINUTES: int = 10
    NOTIFICATION_DEFAULT_TIMEZONE: str = "Asia/Ho_Chi_Minh"
    NOTIFICATION_DEFAULT_REMINDER_TIME: str = "20:00"
    NOTIFICATION_DEFAULT_DAILY_CAP: int = 30
    NOTIFICATION_DEFAULT_QUIET_START: str = "23:00"
    NOTIFICATION_DEFAULT_QUIET_END: str = "06:00"

    # Firebase Cloud Messaging
    FIREBASE_CREDENTIALS_JSON: str | None = None
    FIREBASE_CREDENTIALS_FILE: str | None = None

    # Phase 4.2 production learning loop
    MAX_ACTIVE_LEARNING_BOOKS_PER_USER: int = 14
    LEARNING_COMPLETION_THRESHOLD_PERCENT: int = 80
    LEARNING_PROGRESS_MIN_DELTA_PERCENT: int = 5
    LEARNING_PROGRESS_STALE_SECONDS: int = 30

    # == FOR TEST ==
    PARETO_PLANNER_LLM_ENABLED: bool = True
    PARETO_PLANNER_LLM_MIN_CARDS: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
