# Project Export

## Project Statistics

- Total files: 59

## Folder Structure

```
app
  api
    dependencies
      auth.py
    v1
      routers
        audiobooks.py
        live.py
        study_context.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    config.py
    constant.py
    exceptions.py
    logger.py
    security.py
    supabase.py
    __init__.py
  db
    database.py
    migrations
      env.py
      README
      script.py.mako
      versions
        054450a4d3fc_added_new_logic_context_conversation_.py
        1a04ac7f0a85_add_mode_to_chapter_segments.py
        34b51c319023_optimize_all_db_schema_add_plan_table.py
        78b35db4eddb_add_server_default_to_created_at_and_.py
        7c1f860609e9_added_error_message_to_book.py
        951590abaacf_hotfix_book_ref.py
        960bf5ca365d_udpate_cascade_role.py
  main.py
  models
    db_models.py
  repositories
    audiobook_repo.py
    book_knowledge_repo.py
    chapter_repo.py
    chapter_segment_repo.py
    plan_repo.py
    study_context_document_link_repo.py
    study_context_repo.py
    study_context_thread_repo.py
  schemas
    plan.py
    responses
      audiobook_res.py
      study_context_res.py
      __init__.py
    study_context.py
    user.py
  services
    agent_voice_service.py
    audiobook_service.py
    embed_service.py
    live_service.py
    llm_service.py
    pdf_service.py
    rag_service.py
    storage_service.py
    study_context_service.py
    tts_service.py
    upload_service.py
    workers
      book_pipeline.py
      chapter_worker.py
      tts_worker.py
      __init__.py
    __init__.py
  __init__.py

```

### app\api\dependencies\auth.py

```py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from app.core.supabase import supabase
from app.schemas.user import UserTokenPayload

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserTokenPayload:
    """
    Dependency lấy và verify JWT token từ Header sử dụng Supabase Python SDK.
    Dùng Depends(get_current_user) trong mọi endpoint cần bảo mật.
    """
    token = credentials.credentials
    try:
        # Sử dụng SDK chính thức của Supabase để kiểm tra auth qua server
        # Phương pháp này hỗ trợ chuẩn Asymmetric Keys mới nhất (ES256/RS256) một cách mượt mà nhất.
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise ValueError("Không thể lấy thông tin người dùng")

        user = user_response.user

        return UserTokenPayload(
            sub=UUID(str(user.id)),
            email=user.email,
            role=user.role,
            aud=user.aud,
        )

    except Exception as e:
        # Bắt mọi lỗi decode, hết hạn auth hoặc token rác
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token không hợp lệ hoặc đã hết hạn: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

```

### app\api\v1\routers\audiobooks.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.api.dependencies.auth import get_current_user
from app.db.database import get_session
from app.models.db_models import Book
from app.repositories import audiobook_repo
from app.schemas.plan import SwitchModeRequest
from app.schemas.responses import BookDetailResponse, BookResponse, SwitchModeResponse
from app.schemas.user import UserTokenPayload
from app.services.audiobook_service import get_book_details, switch_book_mode

router = APIRouter()


# @router.get("/books", response_model=list[BookResponse])
# def read_all_books(session: Annotated[Session, Depends(get_session)], current_user: Annotated[UserTokenPayload, Depends(get_current_user)]):
#     print(f"Current user: {current_user.email} (ID: {current_user.sub})")  # Debug log để xem thông tin user
#     return audiobook_repo.get_audiobooks(session)


@router.get("/books", response_model=list[BookResponse])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.get_audiobooks(session)


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.get_book_by_id(session, book_id)


@router.post("/books", response_model=BookResponse)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return audiobook_repo.create_book(session, book)


@router.delete("/book/{book_id}")
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    await audiobook_repo.delete_book_storage(session, book_id)
    return {"message": "Book deleted"}


@router.get("/books/{book_id}/details", response_model=BookDetailResponse)
def get_book_details_endpoint(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_details(session, book_id)


@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, background_tasks, book_id, payload.mode)

```

### app\api\v1\routers\live.py

```py
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.services.live_service import get_token_for_book, get_token_for_thread

router = APIRouter()


@router.get("/live-token/{book_id}")
async def get_token(book_id: str):
    return get_token_for_book(book_id)


@router.get("/live-token/thread/{thread_id}")
async def get_token_thread(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_token_for_thread(session, thread_id)

```

### app\api\v1\routers\study_context.py

```py
import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.repositories.study_context_repo import get_study_contexts
from app.repositories.study_context_thread_repo import get_chat_history_by_thread_id
from app.schemas.responses import ChatMessageResponse, ChatThreadResponse, ContextDocumentResponse, StudyContextResponse
from app.schemas.study_context import (
    ChatThreadInput,
    StudyContextDocumentInput,
    StudyContextInput,
    StudyContextUpdate,
)
from app.services import study_context_service

router = APIRouter()

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


# === Context Management ===


@router.get("/study-contexts", response_model=List[StudyContextResponse])
async def get_study_contexts_api(session: Annotated[Session, Depends(get_session)]):
    return get_study_contexts(session, MOCK_USER_ID)


@router.get("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def get_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_context(session, MOCK_USER_ID, context_id)


@router.post("/study-contexts", response_model=StudyContextResponse)
async def create_study_context_api(payload: StudyContextInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_context(session, MOCK_USER_ID, payload)


@router.patch("/study-contexts/{context_id}", response_model=StudyContextResponse)
async def update_study_context_api(context_id: uuid.UUID, payload: StudyContextUpdate, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.update_context_title(session, MOCK_USER_ID, context_id, payload.title)


@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_context(session, MOCK_USER_ID, context_id)
    return {"message": "Study context deleted successfully"}


@router.post("/study-contexts/{context_id}/documents", response_model=ContextDocumentResponse)
async def add_study_context_document_api(context_id: uuid.UUID, payload: StudyContextDocumentInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.add_document_to_context(session, MOCK_USER_ID, context_id, payload)


@router.delete("/study-contexts/{context_id}/documents/{book_id}")
async def delete_study_context_document_api(context_id: uuid.UUID, book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    study_context_service.delete_document_from_context(session, MOCK_USER_ID, context_id, book_id)
    return {"message": "Context document deleted successfully"}


# === Thread Management ===


@router.get("/study-contexts/{context_id}/threads", response_model=List[ChatThreadResponse])
async def get_chat_threads_api(context_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.get_threads_for_context(session, MOCK_USER_ID, context_id)


@router.post("/study-contexts/{context_id}/threads", response_model=ChatThreadResponse)
async def create_chat_thread_api(context_id: uuid.UUID, payload: ChatThreadInput, session: Annotated[Session, Depends(get_session)]):
    return study_context_service.create_thread(session, MOCK_USER_ID, context_id, payload)


@router.get("/threads/{thread_id}/messages", response_model=List[ChatMessageResponse])
async def get_thread_messages_api(thread_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_chat_history_by_thread_id(session, thread_id)

```

### app\api\v1\routers\upload.py

```py
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.plan import PlanInput
from app.services.upload_service import handle_generate_plan, handle_upload_document

router = APIRouter()


# -----------------------------------------------------------------------
# ENDPOINT 1: POST /upload
# -----------------------------------------------------------------------
@router.post("/upload")
async def upload_document(
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile, File(...)],
):
    """
    Bước 1: Nhận file, extract outline, upload PDF lên Supabase Storage,
    lưu Book + Chapter (DRAFT), trả về outline cho Flutter.
    """
    return await handle_upload_document(session, file)


# -----------------------------------------------------------------------
# ENDPOINT 2: POST /generate-plan
# -----------------------------------------------------------------------
@router.post("/generate-plan")
async def generate_plan(
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
):
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    return await handle_generate_plan(session, background_tasks, payload)

```

### app\api\v1\routers\__init__.py

```py
# API Endpoints module

```

### app\api\v1\__init__.py

```py
# API v1 module

```

### app\api\__init__.py

```py
# API v1 module

```

### app\core\config.py

```py
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

```

### app\core\constant.py

```py
from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class BookStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class PlanMode(str, Enum):
    FULL = "full"
    PARETO = "pareto"

```

### app\core\exceptions.py

```py
"""
app/core/exceptions.py
======================
Domain-specific exception classes cho Triam Backend.

Luồng hoạt động:
    1. Service layer raise DomainError thay vì HTTPException
    2. @app.exception_handler(AppException) trong main.py bắt tất cả và
       tự động map sang HTTP response chuẩn

Lợi ích:
    - Service layer không phụ thuộc FastAPI → dễ unit test độc lập
    - Tất cả error format tập trung một chỗ duy nhất
"""


class AppException(Exception):
    """Base class cho tất cả domain exceptions của ứng dụng."""

    status_code: int = 500
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


# ---------------------------------------------------------------------------
# 404 Not Found
# ---------------------------------------------------------------------------


class BookNotFoundError(AppException):
    status_code = 404
    detail = "Book not found."


class ReadingPlanNotFoundError(AppException):
    status_code = 404
    detail = "Chưa có ReadingPlan cho sách này."


class NoReadingPlanError(AppException):
    """Book tồn tại nhưng user chưa có reading plan."""
    status_code = 400
    detail = "User has no reading plan for this book."


class StudyContextNotFoundError(AppException):
    status_code = 404
    detail = "Study context not found."


class ThreadNotFoundError(AppException):
    status_code = 404
    detail = "Thread not found."


# ---------------------------------------------------------------------------
# 400 Bad Request
# ---------------------------------------------------------------------------


class UnsupportedFileTypeError(AppException):
    status_code = 400
    detail = "Loại file không hỗ trợ. Chỉ chấp nhận PDF, EPUB, DOCX."


class FileTooLargeError(AppException):
    status_code = 400
    detail = "File vượt quá giới hạn 50MB."


# ---------------------------------------------------------------------------
# 409 Conflict
# ---------------------------------------------------------------------------


class BookStatusConflictError(AppException):
    status_code = 409
    detail = "Sách đang ở trạng thái không hợp lệ để thực hiện thao tác này."


# ---------------------------------------------------------------------------
# 422 Unprocessable Entity
# ---------------------------------------------------------------------------


class PdfExtractionError(AppException):
    status_code = 422
    detail = "Không thể trích xuất nội dung từ file. File có thể bị lỗi hoặc là scan ảnh."


# ---------------------------------------------------------------------------
# 500 Internal Server Error
# ---------------------------------------------------------------------------


class DataIntegrityError(AppException):
    """Dữ liệu trong DB bị corrupt hoặc không nhất quán."""
    status_code = 500
    detail = "Data integrity error."


class DatabaseError(AppException):
    """Lỗi khi thực hiện thao tác ghi vào DB."""
    status_code = 500
    detail = "Database operation failed."

```

### app\core\logger.py

```py
import sys
import json
import logging
from pathlib import Path
from loguru import logger

# Định cấu hình đường dẫn thư mục log
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Tùy chỉnh format log hiển thị trên console (có màu sắc)
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def setup_logger():
    # Bỏ cấu hình mặc định
    logger.remove()

    # 1. Cấu hình log ra console (cho môi trường dev)
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level="DEBUG",
        colorize=True,
    )

    # 2. Cấu hình log ra file văn bản chuẩn (để xem local)
    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        rotation="10 MB",     # Cắt file khi đạt 10MB
        retention="7 days",   # Giữ file trong 7 ngày
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8"
    )

    # 3. Cấu hình log dạng JSON (để đẩy lên ELK / Datadog trên Production)
    logger.add(
        LOG_DIR / "app_json_{time:YYYY-MM-DD}.log",
        rotation="50 MB",
        retention="14 days",
        level="INFO",
        serialize=True,       # Ghi log dưới dạng JSON chuẩn
        encoding="utf-8"
    )

    # Chuyển hướng log từ standard logging của Python sang loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Bắt luôn cả log của Uvicorn và FastAPI nếu chúng chạy độc lập
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

    return logger


# Singleton logger instance
log = setup_logger()

```

### app\core\security.py

```py
# Xử lý JWT, Auth (sau này)

```

### app\core\supabase.py

```py
from dotenv import load_dotenv
from supabase import Client, create_client

from app.core.config import settings

load_dotenv()

url: str = settings.SUPABASE_URL
# Use service role key for backend operations (bypasses RLS)
# Fall back to anon key if service role key is not set
key: str = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

```

### app\core\__init__.py

```py
# Core module

```

### app\db\database.py

```py
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

load_dotenv()

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,         # Tắt verbose SQL log trên production
    pool_size=10,       # Connections persistent trong pool
    max_overflow=20,    # Connections tạm thêm khi pool đầy
    pool_timeout=30,    # Giây chờ nếu pool cạn
    pool_recycle=1800,  # Recycle sau 30 phút (tránh stale connections)
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

```

### app\db\migrations\env.py

```py
import app.models.db_models
from app.core.config import settings
from sqlmodel import SQLModel
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Import all db models to make sure they are included in SQLModel.metadata

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# Set sqlalchemy.url from our settings dynamically so we don't have to put it in alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(compare_server_default=True,
                      url=url,
                      target_metadata=target_metadata,
                      literal_binds=True,
                      dialect_opts={"paramstyle": "named"},
                      )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(compare_server_default=True,
                          connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

### app\db\migrations\README

*(Unsupported file type)*

### app\db\migrations\script.py.mako

*(Unsupported file type)*

### app\db\migrations\versions\054450a4d3fc_added_new_logic_context_conversation_.py

```py
"""added new logic context conversation, optimized type/relationship

Revision ID: 054450a4d3fc
Revises: 960bf5ca365d
Create Date: 2026-05-05 08:46:18.296083

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '054450a4d3fc'
down_revision: Union[str, Sequence[str], None] = '960bf5ca365d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('study_contexts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('is_auto_generated', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_contexts_user_id'), 'study_contexts', ['user_id'], unique=False)
    op.create_table('chat_threads',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('context_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['context_id'], ['study_contexts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_threads_context_id'), 'chat_threads', ['context_id'], unique=False)
    op.create_table('study_context_document_links',
    sa.Column('context_id', sa.UUID(), nullable=False),
    sa.Column('book_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['context_id'], ['study_contexts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('context_id', 'book_id')
    )
    op.create_index(op.f('ix_study_context_document_links_book_id'), 'study_context_document_links', ['book_id'], unique=False)
    op.create_index(op.f('ix_study_context_document_links_context_id'), 'study_context_document_links', ['context_id'], unique=False)
    op.create_table('chat_messages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('thread_id', sa.UUID(), nullable=True),
    sa.Column('is_user', sa.Boolean(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['thread_id'], ['chat_threads.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_thread_id'), 'chat_messages', ['thread_id'], unique=False)
    op.create_index(op.f('ix_book_knowledge_book_id'), 'book_knowledge', ['book_id'], unique=False)
    op.create_index(op.f('ix_book_knowledge_chapter_id'), 'book_knowledge', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_chapter_segments_chapter_id'), 'chapter_segments', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_chapters_book_id'), 'chapters', ['book_id'], unique=False)
    op.create_index(op.f('ix_reading_plans_book_id'), 'reading_plans', ['book_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reading_plans_book_id'), table_name='reading_plans')
    op.drop_index(op.f('ix_chapters_book_id'), table_name='chapters')
    op.drop_index(op.f('ix_chapter_segments_chapter_id'), table_name='chapter_segments')
    op.drop_index(op.f('ix_book_knowledge_chapter_id'), table_name='book_knowledge')
    op.drop_index(op.f('ix_book_knowledge_book_id'), table_name='book_knowledge')
    op.drop_index(op.f('ix_chat_messages_thread_id'), table_name='chat_messages')
    op.drop_table('chat_messages')
    op.drop_index(op.f('ix_study_context_document_links_context_id'), table_name='study_context_document_links')
    op.drop_index(op.f('ix_study_context_document_links_book_id'), table_name='study_context_document_links')
    op.drop_table('study_context_document_links')
    op.drop_index(op.f('ix_chat_threads_context_id'), table_name='chat_threads')
    op.drop_table('chat_threads')
    op.drop_index(op.f('ix_study_contexts_user_id'), table_name='study_contexts')
    op.drop_table('study_contexts')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\1a04ac7f0a85_add_mode_to_chapter_segments.py

```py
"""add mode to chapter_segments

Revision ID: 1a04ac7f0a85
Revises: 34b51c319023
Create Date: 2026-04-24 08:38:44.287323

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1a04ac7f0a85'
down_revision: Union[str, Sequence[str], None] = '34b51c319023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chapter_segments', sa.Column('mode', sa.Text(), server_default='full', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapter_segments', 'mode')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\34b51c319023_optimize_all_db_schema_add_plan_table.py

```py
"""optimize all db schema, add plan table

Revision ID: 34b51c319023
Revises: 7c1f860609e9
Create Date: 2026-04-08 15:59:13.882212

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '34b51c319023'
down_revision: Union[str, Sequence[str], None] = '7c1f860609e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reading_plans',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('book_id', sa.Uuid(), nullable=False),
    sa.Column('mode', sa.Text(), nullable=False),
    sa.Column('pace', sa.Integer(), nullable=False),
    sa.Column('schedule_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # 1. Add columns as nullable=True to not break existing rows
    op.add_column('book_knowledge', sa.Column('chapter_id', sa.Uuid(), nullable=True))
    op.add_column('books', sa.Column('user_id', sa.UUID(), nullable=True))

    # Do normal operations
    op.create_foreign_key(None, 'book_knowledge', 'chapters', ['chapter_id'], ['id'])

    # 2. Fix data relationships
    # Xoá các chunk cũ không còn chapter tương ứng để map dữ liệu
    op.execute("""
        DELETE FROM book_knowledge bk
        WHERE NOT EXISTS (
            SELECT 1 FROM chapters c 
            WHERE c.book_id = bk.book_id AND c.chapter_index = bk.chapter_index
        )
    """)
    # Ánh xạ chapter_id bằng cách join với thông tin cũ
    op.execute("""
        UPDATE book_knowledge bk
        SET chapter_id = c.id
        FROM chapters c
        WHERE c.book_id = bk.book_id AND c.chapter_index = bk.chapter_index
    """)

    # Cấp một Dummy UUID cho các sách cũ thiếu user_id (tránh lỗi null)
    op.execute("UPDATE books SET user_id = '00000000-0000-0000-0000-000000000000' WHERE user_id IS NULL")

    # 3. Alter các cột thành NOT NULL sau khi đã có dữ liệu hợp lệ
    op.alter_column('book_knowledge', 'chapter_id', nullable=False)
    op.alter_column('books', 'user_id', nullable=False)

    # Clean up operations
    op.drop_column('book_knowledge', 'chapter_index')
    op.add_column('books', sa.Column('file_url', sa.Text(), nullable=True))
    op.create_index(op.f('ix_books_user_id'), 'books', ['user_id'], unique=False)
    op.drop_column('books', 'gcs_pdf_url')
    op.add_column('chapter_segments', sa.Column('duration_ms', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapter_segments', 'duration_ms')
    op.add_column('books', sa.Column('gcs_pdf_url', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_books_user_id'), table_name='books')
    op.drop_column('books', 'file_url')
    op.drop_column('books', 'user_id')
    op.add_column('book_knowledge', sa.Column('chapter_index', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.drop_column('book_knowledge', 'chapter_id')
    op.drop_table('reading_plans')
    # ### end Alembic commands ###

```

### app\db\migrations\versions\78b35db4eddb_add_server_default_to_created_at_and_.py

```py
"""Add server_default to created_at and updated_at

Revision ID: 78b35db4eddb
Revises: 951590abaacf
Create Date: 2026-05-07 13:20:01.447773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '78b35db4eddb'
down_revision: Union[str, Sequence[str], None] = '951590abaacf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_messages', 'timestamp',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_threads', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('chat_threads', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('reading_plans', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('reading_plans', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('study_contexts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('study_contexts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('study_contexts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('study_contexts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('reading_plans', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('reading_plans', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_threads', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_threads', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('chat_messages', 'timestamp',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None,
               existing_nullable=False)
    # ### end Alembic commands ###

```

### app\db\migrations\versions\7c1f860609e9_added_error_message_to_book.py

```py
"""added error_message to book

Revision ID: 7c1f860609e9
Revises: 
Create Date: 2026-04-07 22:49:48.167966

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7c1f860609e9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audiobook')
    op.alter_column('book_knowledge', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('book_knowledge', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book_knowledge', 'chunk_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book_knowledge', 'content',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_index(op.f('book_knowledge_embedding_idx'), table_name='book_knowledge', postgresql_ops={'embedding': 'vector_cosine_ops'}, postgresql_using='hnsw')
    op.drop_constraint(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(None, 'book_knowledge', 'books', ['book_id'], ['id'])
    op.add_column('books', sa.Column('error_message', sa.Text(), nullable=True))
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)
    op.alter_column('chapter_segments', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(None, 'chapter_segments', 'chapters', ['chapter_id'], ['id'])
    op.alter_column('chapters', 'book_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapters', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chapters', 'title',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_constraint(op.f('chapters_book_id_fkey'), 'chapters', type_='foreignkey')
    op.create_foreign_key(None, 'chapters', 'books', ['book_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chapters', type_='foreignkey')
    op.create_foreign_key(op.f('chapters_book_id_fkey'), 'chapters', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapters', 'title',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('chapters', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapters', 'book_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint(None, 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.drop_column('books', 'error_message')
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_index(op.f('book_knowledge_embedding_idx'), 'book_knowledge', ['embedding'], unique=False, postgresql_ops={'embedding': 'vector_cosine_ops'}, postgresql_using='hnsw')
    op.alter_column('book_knowledge', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('book_knowledge', 'chunk_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book_knowledge', 'chapter_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book_knowledge', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.create_table('audiobook',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('audiobook_pkey'))
    )
    # ### end Alembic commands ###

```

### app\db\migrations\versions\951590abaacf_hotfix_book_ref.py

```py
"""Hotfix: book ref

Revision ID: 951590abaacf
Revises: 054450a4d3fc
Create Date: 2026-05-06 22:08:41.499014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '951590abaacf'
down_revision: Union[str, Sequence[str], None] = '054450a4d3fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.add_column('books', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE books SET updated_at = NOW()")
    op.alter_column('books', 'updated_at', nullable=False)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    planmode_enum = sa.Enum('FULL', 'PARETO', name='planmode')
    planmode_enum.create(op.get_bind(), checkfirst=True)
    
    op.execute("UPDATE chapter_segments SET mode = 'PARETO' WHERE UPPER(mode) = 'PARETO_MODE'")
    op.execute("UPDATE chapter_segments SET mode = 'FULL' WHERE UPPER(mode) = 'FULL_MODE'")
    op.execute("UPDATE chapter_segments SET mode = UPPER(mode)")
    
    op.alter_column('chapter_segments', 'mode', server_default=None)
    
    op.alter_column('chapter_segments', 'mode',
               existing_type=sa.TEXT(),
               type_=planmode_enum,
               existing_nullable=False,
               postgresql_using='UPPER(mode)::planmode')
    op.alter_column('chat_messages', 'thread_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('chat_threads', 'context_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.add_column('reading_plans', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE reading_plans SET updated_at = NOW()")
    op.alter_column('reading_plans', 'updated_at', nullable=False)
    
    op.execute("UPDATE reading_plans SET mode = 'PARETO' WHERE UPPER(mode) = 'PARETO_MODE'")
    op.execute("UPDATE reading_plans SET mode = 'FULL' WHERE UPPER(mode) = 'FULL_MODE'")
    op.execute("UPDATE reading_plans SET mode = UPPER(mode)")
    op.alter_column('reading_plans', 'mode',
               existing_type=sa.TEXT(),
               type_=planmode_enum,
               existing_nullable=False,
               postgresql_using='UPPER(mode)::planmode')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reading_plans', 'mode',
               existing_type=sa.Enum('FULL', 'PARETO', name='planmode'),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.drop_column('reading_plans', 'updated_at')
    op.alter_column('chat_threads', 'context_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chat_messages', 'thread_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'mode',
               existing_type=sa.Enum('FULL', 'PARETO', name='planmode'),
               type_=sa.TEXT(),
               existing_nullable=False,
               existing_server_default=sa.text("'full'::text"))
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_column('books', 'updated_at')
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###

```

### app\db\migrations\versions\960bf5ca365d_udpate_cascade_role.py

```py
"""udpate CASCADE role

Revision ID: 960bf5ca365d
Revises: 1a04ac7f0a85
Create Date: 2026-04-27 19:58:47.509670

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '960bf5ca365d'
down_revision: Union[str, Sequence[str], None] = '1a04ac7f0a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.drop_constraint(op.f('book_knowledge_chapter_id_fkey'), 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(None, 'book_knowledge', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'book_knowledge', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(None, 'chapter_segments', 'chapters', ['chapter_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('chapters_book_id_fkey'), 'chapters', type_='foreignkey')
    op.create_foreign_key(None, 'chapters', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('reading_plans_book_id_fkey'), 'reading_plans', type_='foreignkey')
    op.create_foreign_key(None, 'reading_plans', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading_plans', type_='foreignkey')
    op.create_foreign_key(op.f('reading_plans_book_id_fkey'), 'reading_plans', 'books', ['book_id'], ['id'])
    op.drop_constraint(None, 'chapters', type_='foreignkey')
    op.create_foreign_key(op.f('chapters_book_id_fkey'), 'chapters', 'books', ['book_id'], ['id'])
    op.drop_constraint(None, 'chapter_segments', type_='foreignkey')
    op.create_foreign_key(op.f('chapter_segments_chapter_id_fkey'), 'chapter_segments', 'chapters', ['chapter_id'], ['id'])
    op.alter_column('chapter_segments', 'segment_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chapter_segments', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.drop_constraint(None, 'book_knowledge', type_='foreignkey')
    op.create_foreign_key(op.f('book_knowledge_chapter_id_fkey'), 'book_knowledge', 'chapters', ['chapter_id'], ['id'])
    op.create_foreign_key(op.f('book_knowledge_book_id_fkey'), 'book_knowledge', 'books', ['book_id'], ['id'])
    op.alter_column('book_knowledge', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###

```

### app\main.py

```py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.v1.routers import audiobooks, live, study_context, upload
from app.core.exceptions import AppException
from app.core.logger import log
from app.services.tts_service import stream_text_to_speech_edge


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Chạy khi STARTUP ---
    log.info("Khởi động hệ thống... (TRIAM)")
    # Schema được quản lý bởi Alembic. Chạy: alembic upgrade head
    # Sau từ khóa yield là lúc ứng dụng đang chạy (đang phục vụ người dùng)
    yield
    # --- Chạy khi SHUTDOWN ---
    log.info("Đang dọn dẹp tài nguyên...")


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Global Exception Handler — bắt tất cả AppException và subclass của nó
# ---------------------------------------------------------------------------
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    log.error(f"AppException: {exc.detail} - Status Code: {exc.status_code}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception("Unhandled Exception:")
    return JSONResponse(status_code=500, content={"detail": "Lỗi hệ thống nội bộ."})


# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])
app.include_router(study_context.router, prefix="/api/v1",
                   tags=["Study Context"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech_edge(text), media_type="audio/mpeg")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

### app\models\db_models.py

```py
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, func, DateTime, ForeignKey, Integer, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlmodel import Field, Relationship, SQLModel

from app.core.constant import PlanMode


class StudyContextDocumentLink(SQLModel, table=True):
    __tablename__ = "study_context_document_links"
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, primary_key=True))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, primary_key=True))


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    author: Optional[str] = Field(default=None, sa_column=Column(Text))
    file_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_chapters: Optional[int] = Field(default=None, sa_column=Column(Integer))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    chapters: list["Chapter"] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    reading_plans: list["ReadingPlan"] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    contexts: list["StudyContext"] = Relationship(back_populates="books", link_model=StudyContextDocumentLink)


class ReadingPlan(SQLModel, table=True):
    __tablename__ = "reading_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))
    pace: int = Field(sa_column=Column(Integer, nullable=False))
    schedule_config: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
    status: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    book: Book = Relationship(back_populates="reading_plans")


class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    chapter_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    review_audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    review_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))

    # === RELATIONSHIPS ===
    book: Book = Relationship(back_populates="chapters")
    segments: list["ChapterSegment"] = Relationship(back_populates="chapter", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChapterSegment(SQLModel, table=True):
    __tablename__ = "chapter_segments"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), index=True, nullable=False))
    segment_index: int = Field(sa_column=Column(Integer, nullable=False))
    audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    duration_ms: Optional[int] = Field(default=None, sa_column=Column(Integer))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))

    # === RELATIONSHIPS ===
    chapter: Chapter = Relationship(back_populates="segments")


class BookKnowledge(SQLModel, table=True):
    __tablename__ = "book_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    chapter_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), index=True, nullable=False))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    # TODO: REPALCE 1536 (OpenAI text-embedding-3-small)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))


# === CONTEXT STUDY CONVERSATION===


class StudyContext(SQLModel, table=True):
    __tablename__ = "study_contexts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    is_auto_generated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    books: list[Book] = Relationship(back_populates="contexts", link_model=StudyContextDocumentLink)
    threads: list["ChatThread"] = Relationship(back_populates="context", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatThread(SQLModel, table=True):
    __tablename__ = "chat_threads"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    context_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("study_contexts.id", ondelete="CASCADE"), index=True, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    context: StudyContext = Relationship(back_populates="threads")
    messages: list["ChatMessage"] = Relationship(back_populates="thread", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chat_threads.id", ondelete="CASCADE"), index=True, nullable=False))
    is_user: bool = Field(sa_column=Column(Boolean, nullable=False))
    text: str = Field(sa_column=Column(Text, nullable=False))
    source: str = Field(sa_column=Column(Text, nullable=False))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))

    # === RELATIONSHIPS ===
    thread: ChatThread = Relationship(back_populates="messages")

```

### app\repositories\audiobook_repo.py

```py
import uuid
from typing import Optional

from sqlmodel import Session, select

from app.core.logger import log
from app.core.supabase import supabase
from app.models.db_models import Book


def get_audiobooks(session: Session) -> list[Book]:
    return list(session.exec(select(Book)).all())


def get_book_by_id(session: Session, book_id: uuid.UUID) -> Optional[Book]:
    return session.get(Book, book_id)


def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def update_book_status(session: Session, book_id: uuid.UUID, status: str, error_message: Optional[str] = None) -> None:
    book = session.get(Book, book_id)
    if book:
        book.status = status
        if error_message is not None:
            book.error_message = error_message
        session.add(book)
        session.commit()


def delete_book(session: Session, book_id: uuid.UUID) -> None:
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()


async def delete_book_storage(session: Session, book_id: uuid.UUID):
    """
    Xóa sạch assets trong Storage và bản ghi trong Database.
    """
    str_book_id = str(book_id)
    target_buckets = ["audios", "raw_books"]

    try:
        # 1. Lấy danh sách file từ tất cả bucket liên quan qua RPC (SELECT)
        result = supabase.rpc("get_book_asset_paths", {
                              "bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute()

        # 2. Phân loại và xóa file qua Storage API
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                # Lọc ra danh sách file thuộc bucket hiện tại
                paths = [str(item["name"])
                         for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]

                if paths:
                    # Xóa hàng loạt file trong bucket này (Đúng quy trình API)
                    supabase.storage.from_(bucket).remove(paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # 3. Xóa record trong DB
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch sẽ database cho book: {str_book_id}")

    except Exception as e:
        # Rollback session nếu có lỗi ở tầng DB để tránh mất dữ liệu không đồng bộ
        session.rollback()
        log.exception(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise e

```

### app\repositories\book_knowledge_repo.py

```py
import uuid

from sqlmodel import Session, select

from app.models.db_models import BookKnowledge


def bulk_create_knowledge(session: Session, records: list[BookKnowledge]) -> None:
    """Insert hàng loạt BookKnowledge (vector chunks) vào DB."""
    for record in records:
        session.add(record)
    session.commit()


def delete_knowledge_by_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    """Xóa toàn bộ vector chunks của 1 chapter (dùng khi rollback)."""
    records = session.exec(
        select(BookKnowledge).where(BookKnowledge.chapter_id == chapter_id)
    ).all()
    for record in records:
        session.delete(record)
    session.commit()


```

### app\repositories\chapter_repo.py

```py
import json
import uuid

from fastapi import HTTPException
from sqlmodel import Session, col, select

from app.core.logger import log
from app.models.db_models import Chapter


def get_draft_chapters_by_book(session: Session, book_id: uuid.UUID) -> list[Chapter]:
    """Lấy danh sách chapters có status='DRAFT' theo book_id, sort theo chapter_index."""
    statement = select(Chapter).where(Chapter.book_id ==
                                      book_id).order_by(col(Chapter.chapter_index))
    return list(session.exec(statement).all())


def create_chapter(session: Session, chapter: Chapter) -> Chapter:
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter


def update_chapter_review_audio(session: Session, chapter_id: uuid.UUID, review_audio_url: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_audio = json.loads(
                chapter.review_audio_url) if chapter.review_audio_url else {}
        except (json.JSONDecodeError, TypeError) as e:
            log.error(f"Data integrity error: {e}")
            raise HTTPException(
                status_code=500, detail="Data integrity error") from e

        reviews_audio[mode] = review_audio_url
        chapter.review_audio_url = json.dumps(
            reviews_audio, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def update_chapter_status(session: Session, chapter_id: uuid.UUID, status: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        chapter.status = status
        session.add(chapter)
        session.commit()


def update_chapter_review_text(session: Session, chapter_id: uuid.UUID, review_text: str, mode: str) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        try:
            reviews_text = json.loads(
                chapter.review_text) if chapter.review_text else {}
        except (json.JSONDecodeError, TypeError) as e:
            log.error(f"Data integrity error: {e}")
            raise HTTPException(
                status_code=500, detail="Data integrity error") from e

        reviews_text[mode] = review_text
        chapter.review_text = json.dumps(reviews_text, ensure_ascii=False)
        session.add(chapter)
        session.commit()


def delete_chapter(session: Session, chapter_id: uuid.UUID) -> None:
    chapter = session.get(Chapter, chapter_id)
    if chapter:
        session.delete(chapter)
        session.commit()

```

### app\repositories\chapter_segment_repo.py

```py
import uuid

from sqlmodel import Session, func, select

from app.models.db_models import ChapterSegment


def bulk_create_segments(session: Session, segments: list[ChapterSegment]) -> None:
    """Bulk tạo mới các segments."""
    for segment in segments:
        session.add(segment)
    session.commit()


def check_segments_exist_by_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> bool:
    """Kiểm tra xem đã có segment nào của mode này sinh ra chưa (trong 1 chapter)."""
    return (
        session.exec(
            select(ChapterSegment).where(
                ChapterSegment.chapter_id == chapter_id,
                ChapterSegment.mode == mode,
            )
        ).first()
        is not None
    )


def count_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: str) -> int:
    """
    Đếm tổng số segments của một mode trên toàn bộ sách.
    Dùng để xác định chính xác xem mode đó đã được gen hoàn chỉnh chưa.
    Thay thế check_segments_exist_by_mode khi cần kiểm tra cả sách.
    """
    from app.models.db_models import Chapter  # tránh circular import

    result = session.exec(
        select(func.count(ChapterSegment.id))
        .join(Chapter, ChapterSegment.chapter_id == Chapter.id)  # type: ignore[arg-type]
        .where(Chapter.book_id == book_id)
        .where(ChapterSegment.mode == mode)
    ).one()
    return result or 0


def delete_segments_by_chapter_and_mode(session: Session, chapter_id: uuid.UUID, mode: str) -> None:
    """Xóa tất cả các segments của 1 chapter theo mode (dùng khi gen lại)."""
    segments = session.exec(
        select(ChapterSegment).where(
            ChapterSegment.chapter_id == chapter_id,
            ChapterSegment.mode == mode,
        )
    ).all()
    for s in segments:
        session.delete(s)
    session.commit()

```

### app\repositories\plan_repo.py

```py
import uuid

from sqlmodel import Session, select

from app.core.constant import PlanStatus
from app.models.db_models import ReadingPlan


def check_plan_exist(session: Session, book_id: uuid.UUID) -> bool:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first() is not None


def get_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()


def get_active_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id).where(ReadingPlan.status == PlanStatus.ACTIVE)).first()


def get_all_plan_by_user_id(session: Session, user_id: uuid.UUID) -> list[ReadingPlan]:
    return session.exec(select(ReadingPlan).where(ReadingPlan.user_id == user_id)).all()


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

```

### app\repositories\study_context_document_link_repo.py

```py
import uuid

from sqlmodel import Session, select

from app.models.db_models import StudyContextDocumentLink


def create_new_context_document(
    session: Session, link: StudyContextDocumentLink
) -> StudyContextDocumentLink:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_context_documents(session: Session, context_id: uuid.UUID) -> list[StudyContextDocumentLink]:
    return session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == context_id)
    ).all()


def delete_study_context_document(session: Session, context_id: uuid.UUID, book_id: uuid.UUID) -> None:
    link = session.exec(
        select(StudyContextDocumentLink).where(
            StudyContextDocumentLink.context_id == context_id, StudyContextDocumentLink.book_id == book_id
        )
    ).first()
    if link:
        session.delete(link)
        session.commit()

```

### app\repositories\study_context_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import StudyContext


def get_study_context(session: Session, context_id: uuid.UUID) -> StudyContext | None:
    return session.get(StudyContext, context_id)


def get_study_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return session.exec(select(StudyContext).where(StudyContext.user_id == user_id)).all()


def create_study_context(session: Session, study_context: StudyContext) -> StudyContext:
    session.add(study_context)
    session.commit()
    session.refresh(study_context)
    return study_context


def update_study_context(
    session: Session, context_id: uuid.UUID, title: str | None = None
) -> StudyContext | None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        if title is not None:
            study_context.title = title
        study_context.updated_at = datetime.now(timezone.utc)
        session.add(study_context)
        session.commit()
        session.refresh(study_context)
        return study_context
    return None


def delete_study_context(session: Session, context_id: uuid.UUID) -> None:
    study_context = session.get(StudyContext, context_id)
    if study_context:
        session.delete(study_context)
        session.commit()

```

### app\repositories\study_context_thread_repo.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.db_models import ChatMessage, ChatThread


def get_chat_threads_for_context(session: Session, context_id: uuid.UUID) -> list[ChatThread]:
    threads = session.exec(select(ChatThread).where(ChatThread.context_id == context_id)).all()
    return threads


def get_chat_history_by_thread_id(session: Session, thread_id: uuid.UUID) -> list[ChatMessage]:
    messages = session.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()
    return messages


def create_new_thread(session: Session, thread: ChatThread) -> ChatThread:
    session.add(thread)
    session.commit()
    session.refresh(thread)
    return thread


def update_thread_title(session: Session, thread_id: uuid.UUID, title: str) -> ChatThread | None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        thread.title = title
        thread.updated_at = datetime.now(timezone.utc)
        session.add(thread)
        session.commit()
        session.refresh(thread)
        return thread
    return None


def delete_thread(session: Session, thread_id: uuid.UUID) -> None:
    thread = session.get(ChatThread, thread_id)
    if thread:
        session.delete(thread)
        session.commit()

```

### app\schemas\plan.py

```py
import uuid

from pydantic import BaseModel

from app.models.db_models import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]


class SwitchModeRequest(BaseModel):
    mode: PlanMode

```

### app\schemas\responses\audiobook_res.py

```py
"""
app/schemas/responses/audiobook_res.py
=======================================
Response DTOs cho module Audiobook.

Chỉ expose các trường Flutter FE thực sự cần — không lộ thông tin nội bộ
(user_id, error_message, db relationships, ...).
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookResponse(BaseModel):
    """DTO cho một cuốn sách — dùng cho GET /books và GET /books/{id}."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    author: Optional[str] = None
    total_chapters: Optional[int] = None
    status: Optional[str] = None
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SegmentResponse(BaseModel):
    """DTO cho một segment audio trong chapter."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    segment_index: int
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    duration_ms: Optional[int] = None
    mode: str


class ChapterDetailResponse(BaseModel):
    """DTO cho một chapter kèm danh sách segments."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    status: Optional[str] = None
    chapter_index: int
    review_text: str = ""
    review_audio_url: str = ""
    chapter_segments: list[SegmentResponse] = []


class BookDetailResponse(BaseModel):
    """DTO cho response của GET /books/{id}/details — sách kèm toàn bộ chapters."""

    model_config = ConfigDict(from_attributes=True)

    book_status: Optional[str] = None
    total_chapters: Optional[int] = None
    chapters: list[ChapterDetailResponse] = []


class SwitchModeResponse(BaseModel):
    """DTO cho response của POST /books/{id}/switch-mode."""

    message: str
    needs_generation: bool

```

### app\schemas\responses\study_context_res.py

```py
"""
app/schemas/responses/study_context_res.py
===========================================
Response DTOs cho module Study Context.

Chỉ expose các trường Flutter FE thực sự cần — không lộ user_id,
không kéo theo lazy-load relationships.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudyContextResponse(BaseModel):
    """DTO cho StudyContext — ẩn user_id (internal field)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    is_auto_generated: bool = False
    created_at: datetime
    updated_at: datetime


class ChatThreadResponse(BaseModel):
    """DTO cho ChatThread — không kéo theo relationship messages."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    context_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageResponse(BaseModel):
    """DTO cho ChatMessage — không kéo theo relationship thread."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thread_id: uuid.UUID
    is_user: bool
    text: str
    source: str
    timestamp: datetime


class ContextDocumentResponse(BaseModel):
    """DTO cho StudyContextDocumentLink."""

    model_config = ConfigDict(from_attributes=True)

    context_id: uuid.UUID
    book_id: uuid.UUID

```

### app\schemas\responses\__init__.py

```py
# Response DTO schemas — import từ đây cho gọn
from app.schemas.responses.audiobook_res import (
    BookDetailResponse,
    BookResponse,
    SwitchModeResponse,
)
from app.schemas.responses.study_context_res import (
    ChatMessageResponse,
    ChatThreadResponse,
    ContextDocumentResponse,
    StudyContextResponse,
)

__all__ = [
    # Audiobook
    "BookResponse",
    "BookDetailResponse",
    "SwitchModeResponse",
    # Study Context
    "StudyContextResponse",
    "ChatThreadResponse",
    "ChatMessageResponse",
    "ContextDocumentResponse",
]

```

### app\schemas\study_context.py

```py
import uuid

from pydantic import BaseModel


class StudyContextInput(BaseModel):
    title: str

class StudyContextUpdate(BaseModel):
    title: str | None = None

class StudyContextDocumentInput(BaseModel):
    book_id: uuid.UUID

class ChatThreadInput(BaseModel):
    title: str

class ChatThreadUpdate(BaseModel):
    title: str | None = None

```

### app\schemas\user.py

```py
# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserTokenPayload(BaseModel):
    """
    Schema định nghĩa payload chứa trong JWT token của Supabase trả về
    """
    sub: UUID
    email: Optional[str] = None
    role: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None

```

### app\services\agent_voice_service.py

```py
import asyncio
import json
import uuid
from app.core.logger import log
from datetime import datetime, timezone
from typing import Annotated

from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    function_tool,
    inference,
    room_io,
)
from livekit.agents.llm import ChatMessage as LLMMessage
from livekit.agents.voice import io as voice_io
from livekit.plugins import noise_cancellation, silero, openai, deepgram, google
from sqlmodel import Session, select
from supabase import Client, create_client
from tavily import TavilyClient

from app.core.config import settings
from app.db.database import engine
from app.models.db_models import ChatMessage
from app.services.rag_service import search_book_knowledge

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# Supabase (RAG)
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY,
)


class ChatTextOutput(voice_io.TextOutput):
    def __init__(self, room: rtc.Room, save_cb=None, topic: str = "lk.chat") -> None:
        super().__init__(label="ChatTextOutput", next_in_chain=None)
        self._room = room
        self._topic = topic
        self._buffer: list[str] = []
        self._flush_task: asyncio.Task[None] | None = None
        self._save_cb = save_cb

    async def capture_text(self, text: str) -> None:
        if not text:
            return

        self._buffer.append(text)

    def flush(self) -> None:
        if not self._buffer:
            return

        message = "".join(self._buffer)
        self._buffer.clear()
        preview = message if len(message) <= 120 else f"{message[:120]}..."
        log.info(f"Text output ({len(message)} chars): {preview}")

        if self._save_cb:
            asyncio.create_task(asyncio.to_thread(
                self._save_cb, message, False))

        async def _publish(text: str) -> None:
            if not self._room.isconnected():
                return
            try:
                await self._room.local_participant.publish_data(
                    text,
                    reliable=True,
                    topic=self._topic,
                )
            except Exception as exc:
                log.info(f"Text output publish failed: {exc}")

        # Flush is sync; schedule async publish.
        self._flush_task = asyncio.create_task(_publish(message))


class TriamAssistant(Agent):
    def __init__(self, document_ids: list[str]) -> None:
        super().__init__(
            instructions=(
                "Bạn là trợ lý AI sách nói TRIAM - Trợ lý đọc sách nói thông minh.\n"
                "1. Bạn đang ở trong một 'Study Context' (Ngữ cảnh học tập) chứa các sách mà User đã chọn.\n"
                "2. Khi User hỏi về kiến thức, hoặc nhắc tới 'quyển sách này', TUYỆT ĐỐI PHẢI GỌI hàm 'search_book_knowledge' để tìm kiếm. Truyền thẳng câu hỏi của User vào biến query (không cần hỏi lại tên sách vì hệ thống đã tự động giới hạn vùng tìm kiếm).\n"
                "3. Trả lời cực kỳ NGẮN GỌN (dưới 2-3 câu), tự nhiên rành mạch, đi thẳng vào trọng tâm câu hỏi.\n"
                "4. Tuyệt đối KHÔNG SỬ DỤNG Markdown (không dùng dấu **, *, #, -) và KHÔNG SỬ DỤNG EMOJI trong câu trả lời.\n"
                "5. Chỉ dùng 'search_web' nếu nội dung không có trong sách."
            )
        )
        self.document_ids = document_ids

    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"],
    ) -> str:
        try:
            data = await search_book_knowledge(query, self.document_ids)

            if not data:
                return "RAG don't have data"

            if not isinstance(data, list):
                return "RAG invalid RAG data format"

            formatted_chunks = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    continue
                chapter_id = str(item.get("chapter_id", ""))
                chunk_index = item.get("chunk_index", "N/A")
                content = item.get("content", "")

                chunk_text = f"--- Segment {i + 1} (Chapter ID: ...{chapter_id[-6:]}, Index: {chunk_index}) ---\n{content}"
                formatted_chunks.append(chunk_text)

            context = "\n\n".join(formatted_chunks)
            return f"Book Knowledge: {context}"
        except Exception as e:
            return f"Error: {str(e)}"

    @function_tool
    async def search_web(
        self,
        query: Annotated[str, "Nội dung cần tìm kiếm trên internet"],
    ) -> str:
        import asyncio

        loop = asyncio.get_event_loop()
        search_result = await loop.run_in_executor(
            None,
            lambda: tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=3,
            ),
        )
        result_text = "\n".join(
            [f"- {r['content']}" for r in search_result["results"]])
        return result_text


async def entrypoint(ctx: JobContext):

    await ctx.connect()

    try:
        job_meta = json.loads(ctx.job.metadata or "{}")
        # TODO: Hardcoded to test console => My intention
        book_id = job_meta.get(
            "book_id", "9cda7cbc-c9e4-4325-9fc9-cb74d71e14b3")
        thread_id = job_meta.get(
            "thread_id", "f25f309f-1dbb-4517-90b9-5fbbc88e3070")
        document_ids = job_meta.get("document_ids", [])

        if book_id and not document_ids:
            document_ids = [book_id]

    except (json.JSONDecodeError, AttributeError, TypeError):
        thread_id = ""
        document_ids = []

    if not document_ids:
        log.info("❌ Không tìm thấy document_ids trong metadata! Thoát.")
        return

    log.info(f"✅ Document IDs từ metadata: {document_ids}")
    log.info(f"🏠 Room Name (session): {ctx.room.name}")
    log.info(f"Bat dau phien doc sach cho Thread ID: {thread_id}")

    # session = AgentSession(
    #     stt=inference.STT(
    #         model="deepgram/nova-3",  # Nova-3 is more accurate for Vietnamese than Flux-General
    #         language="vi",
    #         extra_kwargs={"language_hints": ["vi"], "smart_format": True},
    #     ),
    #     llm=inference.LLM(
    #         model="openai/gpt-5.3-chat-latest",
    #     ),
    #     tts=inference.TTS(
    #         model="elevenlabs/eleven_flash_v2_5",
    #         language="vi",
    #         extra_kwargs={
    #             "voice_id": "Lcf7z35dm7QXBoD0f107",  # Custom voice Vietnamese - Linh
    #             "add_timestamps": True,
    #             "voice_settings": {
    #                 "stability": 0.45,  # Giảm để AI nhấn dấu hỏi/ngã chuẩn hơn
    #                 "similarity_boost": 0.8,  # Tăng để giữ đặc trưng giọng người Việt
    #                 "style": 0.1,  # Thêm chút cảm xúc
    #                 "use_speaker_boost": True,
    #             },
    #         },
    #     ),
    #     vad=silero.VAD.load(),
    # )
    session = AgentSession(
        stt=deepgram.STT(
            api_key=settings.DEEPGRAM_API_KEY,
            model="nova-3",
            language="vi",
            smart_format=True,
        ),
        llm=google.LLM(
            api_key=settings.GEMINI_API_KEY,
            model="gemini-2.5-flash",
        ),
        tts=openai.TTS(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-4o-mini-tts",
            voice="nova",
            speed=1.3,
            instructions="Hãy nói với tốc độ nhanh, hào hứng và ngắt nghỉ dứt khoát."
        ),
        vad=silero.VAD.load(),
    )

    def _save_message(text: str, is_user: bool):
        if not thread_id:
            return
        try:
            with Session(engine) as db:
                new_msg = ChatMessage(thread_id=uuid.UUID(
                    thread_id), is_user=is_user, text=text, source="livekit", timestamp=datetime.now(timezone.utc))
                db.add(new_msg)
                db.commit()
        except Exception as e:
            log.info(f"Lỗi khi lưu message: {e}")

    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent,
    # because TextInputEvent may not be supported or reliable in all client implementations. By listening to data packets directly, we can ensure that text input works consistently regardless of the client.
    # THIS IS A TEXT STREAM implement
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input from {participant_id}: {ev.text}")
        asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        await sess.interrupt()
        sess.generate_reply(user_input=ev.text)

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input from {participant_id or 'unknown'}: {text}")
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        await session.interrupt()
        session.generate_reply(user_input=text)

    def on_data_received(packet: rtc.DataPacket) -> None:
        if packet.topic != "lk.chat":
            return
        try:
            text = packet.data.decode("utf-8")
        except Exception as exc:
            log.info(f"Data input decode failed: {exc}")
            return
        participant_id = packet.participant.identity if packet.participant else None
        asyncio.create_task(handle_data_input(text, participant_id))

    ctx.room.on("data_received", on_data_received)

    @session.on("user_speech_committed")
    def on_user_speech(msg: LLMMessage):
        content = getattr(msg, "content", getattr(msg, "text", ""))
        if content:
            asyncio.create_task(asyncio.to_thread(
                _save_message, str(content), True))

    @session.on("agent_speech_committed")
    def on_agent_speech(msg: LLMMessage):
        content = getattr(msg, "content", getattr(msg, "text", ""))
        if content:
            asyncio.create_task(asyncio.to_thread(
                _save_message, str(content), False))

    await session.start(
        room=ctx.room,
        agent=TriamAssistant(document_ids=document_ids),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda _: noise_cancellation.BVC(),
            ),
            text_input=room_io.TextInputOptions(
                text_input_cb=handle_text_input),
            text_output=room_io.TextOutputOptions(
                sync_transcription=False,
                next_in_chain=ChatTextOutput(ctx.room, save_cb=_save_message),
            ),
            close_on_disconnect=True,
        ),
    )

    # Load history
    def _load_history():
        if not thread_id:
            return []
        with Session(engine) as db:
            return db.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp.asc())).all()

    try:
        history_msgs = await asyncio.to_thread(_load_history)
        if hasattr(session, "chat_ctx") and session.chat_ctx:
            for msg in history_msgs:
                session.chat_ctx.append(
                    role="user" if msg.is_user else "assistant", text=msg.text)
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")

    await session.generate_reply(
        instructions=(
            "Chào bạn! Tôi là trợ lý ảo TRIAM. Tôi sẵn sàng hỗ trợ bạn ngay lúc này."),
    )


if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            load_fnc=lambda: 0.0,
            agent_name=settings.LIVEKIT_AGENT_NAME,
        )
    )

```

### app\services\audiobook_service.py

```py
import json
import uuid
from typing import Any

from fastapi import BackgroundTasks
from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.core.exceptions import (
    BookNotFoundError,
    DataIntegrityError,
    NoReadingPlanError,
    ReadingPlanNotFoundError,
)
from app.models.db_models import Book, Chapter, ChapterSegment, ReadingPlan
from app.repositories.chapter_segment_repo import count_segments_by_book_and_mode
from app.services.workers.book_pipeline import run_switch_mode_processing


def _extract_json_content(raw_data: Any, mode: str) -> str:
    """Helper: Trích xuất nội dung theo mode từ chuỗi JSON."""
    if not raw_data:
        return ""
    try:
        data = json.loads(raw_data)
        return data.get(mode, "")
    except (json.JSONDecodeError, TypeError) as e:
        raise DataIntegrityError() from e


def get_book_details(session: Session, book_id: uuid.UUID) -> dict:
    """
    Lấy chi tiết sách kèm chapters và segments theo active mode.
    Tối ưu N+1 bằng cách query TẤT CẢ segments một lần duy nhất.
    """
    book = session.get(Book, book_id)
    if not book:
        raise BookNotFoundError()

    # 1. Lấy ReadingPlan và xác định active mode
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise NoReadingPlanError()

    try:
        active_mode = PlanMode(plan.mode)
    except ValueError as e:
        raise DataIntegrityError() from e

    # 2. Query tất cả chapters và segments một lần — tránh N+1
    chapters = session.exec(
        select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)
    ).all()

    chapter_ids = [c.id for c in chapters]
    all_segments = session.exec(
        select(ChapterSegment)
        .where(ChapterSegment.chapter_id.in_(chapter_ids), ChapterSegment.mode == active_mode)
        .order_by(ChapterSegment.segment_index)
    ).all()

    # 3. Nhóm segments theo chapter_id để truy xuất O(1)
    segments_map: dict = {}
    for s in all_segments:
        segments_map.setdefault(s.chapter_id, []).append(s.model_dump())

    # 4. Gom kết quả
    result = [
        {
            "id": str(chap.id),
            "title": chap.title,
            "status": chap.status,
            "chapter_index": chap.chapter_index,
            "review_text": _extract_json_content(chap.review_text, active_mode),
            "review_audio_url": _extract_json_content(chap.review_audio_url, active_mode),
            "chapter_segments": segments_map.get(chap.id, []),
        }
        for chap in chapters
    ]

    return {"book_status": book.status, "total_chapters": book.total_chapters, "chapters": result}


def switch_book_mode(
    session: Session,
    background_tasks: BackgroundTasks,
    book_id: uuid.UUID,
    payload_mode: str,
) -> dict:
    """
    Đổi mode active trên ReadingPlan và sinh audio mới nếu mode chưa từng được gen.
    """
    book = session.get(Book, book_id)
    if not book:
        raise BookNotFoundError()

    # 1. Lấy ReadingPlan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    if not plan:
        raise ReadingPlanNotFoundError()

    # 2. Nếu switch sang cùng mode đang active → không cần làm gì thêm
    if plan.mode == payload_mode:
        total = count_segments_by_book_and_mode(session, book_id, payload_mode)
        if total > 0:
            return {
                "message": f"Đã ở mode {payload_mode} và audio đã có sẵn ({total} segments).",
                "needs_generation": False,
            }
        else:
            # Đang ở đúng mode nhưng chưa có segments (do gen thất bại trước)
            background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
            return {"message": f"Mode {payload_mode} chưa có audio, đang gen lại.", "needs_generation": True}

    # 3. Cập nhật mode mới vào ReadingPlan
    plan.mode = payload_mode
    session.add(plan)
    session.commit()

    # 4. Kiểm tra xem audio của mode mới đã được sinh ra bao giờ chưa
    total = count_segments_by_book_and_mode(session, book_id, payload_mode)
    needs_generation = total == 0

    # 5. Kích hoạt Background Task sinh audio nếu cần
    if needs_generation:
        background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode)
        return {
            "message": f"Đã chuyển sang mode {payload_mode}. Hệ thống đang sinh audio trong background.",
            "needs_generation": True,
        }

    return {"message": f"Đã chuyển sang mode {payload_mode}. Audio đã có sẵn.", "needs_generation": False}

```

### app\services\embed_service.py

```py
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
from sqlmodel import Session

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import BookKnowledge
from app.repositories.book_knowledge_repo import bulk_create_knowledge

aclient = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""],
)


async def embed_and_save_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
    session: Session,
) -> None:
    """
    Luồng 1 RAG:
    1. Cắt raw_text thành chunks bằng RecursiveCharacterTextSplitter.
    2. Gọi OpenAI Embedding API (batch).
    3. Lưu vào bảng book_knowledge qua SQLModel session.
    """
    chunks = _splitter.split_text(raw_text)
    if not chunks:
        return

    response = await aclient.embeddings.create(
        input=chunks,
        model="text-embedding-3-small",
    )

    records = [
        BookKnowledge(
            book_id=book_id,
            chapter_id=chapter_id,
            chunk_index=i,
            content=chunks[i],
            embedding=embedding_data.embedding,
        )
        for i, embedding_data in enumerate(response.data)
    ]

    bulk_create_knowledge(session, records)
    log.info(f"RAG: Saved {len(records)} vectors for chapter_id={chapter_id}")

```

### app\services\live_service.py

```py
import json
import uuid

from livekit import api
from sqlmodel import Session, select

from app.core.config import settings
from app.core.exceptions import ThreadNotFoundError
from app.models.db_models import ChatThread, StudyContextDocumentLink


def _build_livekit_token(room_name: str, metadata: dict) -> dict:
    """
    Helper dùng chung: Tạo AccessToken LiveKit với room config và trả về JWT + room_name.
    """
    agent_dispatch = api.RoomAgentDispatch(
        agent_name=settings.LIVEKIT_AGENT_NAME,
        metadata=json.dumps(metadata),
    )
    room_config = api.RoomConfiguration(agents=[agent_dispatch])

    token = (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(f"user_{uuid.uuid4().hex[:6]}")
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
        .with_room_config(room_config)
    )

    return {"token": token.to_jwt(), "room_name": room_name}


def get_token_for_book(book_id: str) -> dict:
    """Tạo LiveKit token cho session đọc sách đơn lẻ."""
    session_room_name = f"triam_{book_id[:8]}_{uuid.uuid4().hex[:6]}"
    return _build_livekit_token(session_room_name, {"book_id": book_id})


def get_token_for_thread(session: Session, thread_id: uuid.UUID) -> dict:
    """Tạo LiveKit token cho session gắn với Study Context thread."""
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()

    # Lấy danh sách document_ids từ context
    links = session.exec(
        select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == thread.context_id)
    ).all()
    document_ids = [str(link.book_id) for link in links]

    session_room_name = f"triam_{str(thread_id)[:8]}_{uuid.uuid4().hex[:6]}"
    metadata = {
        "thread_id": str(thread_id),
        "context_id": str(thread.context_id),
        "document_ids": document_ids,
    }
    return _build_livekit_token(session_room_name, metadata)

```

### app\services\llm_service.py

```py
import json

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.constant import PlanMode

from app.core.logger import log as logger

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY,
                     base_url=settings.GEMINI_BASE_URL)

SYSTEM_PROMPT_REWRITE_FULL = """
Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Nội dung tóm tắt để ôn tập..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""

SYSTEM_PROMPT_REWRITE_PARETO = """
Bạn là một Chuyên gia Đọc nhanh & Giáo dục (TRIAM AI) áp dụng nguyên lý Pareto (80/20).
Nhiệm vụ: Chắt lọc 20% nội dung quan trọng nhất (ý chính, công thức, keyword) để mang lại 80% giá trị của văn bản gốc, sau đó chuyển thành kịch bản nói (TTS Script).

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. LƯỢC BỎ: Cắt bỏ hoàn toàn các ví dụ dài dòng, câu chuyện phụ, câu từ lan man "tốt thì biết".
2. TẬP TRUNG CỐT LÕI: Giữ lại định nghĩa, luận điểm chính, keyword (in đậm/in nghiêng trong ý đồ tác giả).
3. VĂN PHONG TTS: Nội dung chắt lọc phải được nối lại thành câu văn nói mượt mà, dễ hiểu, súc tích. Xử lý số liệu, chữ viết tắt như bình thường.
4. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
5. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
6. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
7. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
8. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Tóm tắt cốt lõi để ôn tập nhanh (100 từ)..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""


# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------


async def normalize_text_for_speech(raw_text: str, mode: str) -> dict:
    """
    Gửi text thô cho Gemini để biên tập và cấu trúc lại thành TTS script.

    Returns:
        {"main_scripts": [...], "review_script": "..."}

    Raises:
        Exception: Nếu LLM call thất bại hoặc response không parse được —
                   caller (tts_worker) chịu trách nhiệm rollback chapter.
    """
    if mode.lower() == PlanMode.PARETO or mode.lower() == PlanMode.PARETO.value:
        mode_prompt = SYSTEM_PROMPT_REWRITE_PARETO
    else:
        mode_prompt = SYSTEM_PROMPT_REWRITE_FULL

    response = await client.chat.completions.create(
        model=settings.GEMINI_MODEL_LLM,
        messages=[{"role": "system", "content": mode_prompt},
                  {"role": "user", "content": raw_text}],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()
    parsed_data = json.loads(content)

    logger.debug(
        f"LLM parsed OK — {len(parsed_data.get('main_scripts', []))} scripts, mode={mode}")
    return parsed_data

```

### app\services\pdf_service.py

```py

import pdfplumber
from pypdf import PdfReader

from app.core.logger import log


def get_pdf_outline_structure(file_obj):
    """
    Hàm này cố gắng đọc Mục lục (Bookmarks) từ metadata của PDF.
    Trả về: List [{"title": "Chapter 1", "page_start": 5}, ...] hoặc [] nếu không có.
    """
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        # reader.outline chứa cấu trúc mục lục
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    # Đệ quy nếu có mục lục con (Sub-chapter)
                    _parse_outline(item)
                else:
                    try:
                        # Lấy số trang (pypdf trả về page object, cần lấy index)
                        page_number = reader.get_destination_page_number(item)
                        # pypdf get đúng page number
                        outline_data.append(
                            {"title": item.title, "page_start": page_number})
                    except Exception:
                        pass  # Bỏ qua nếu item bị lỗi link

        _parse_outline(reader.outline)

        # Sắp xếp lại theo số trang để chắc chắn thứ tự đúng
        outline_data.sort(key=lambda x: x["page_start"])
        return outline_data
    except Exception as e:
        log.warning(f"Lỗi đọc Outline: {e}")
        return []


async def extract_chapters_smart(file_obj):
    """
    Hàm xử lý thông minh Dùng Outline (Mục lục ẩn).
    """
    # Lưu ý: Phải reset pointer file về 0 trước khi đọc
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)

    chapters = []

    if not outlines or len(outlines) <= 1:
        raise ValueError(
            "Tài liệu PDF không có Mục lục (Outline) ẩn. Hệ thống hiện chỉ hỗ trợ PDF có Mục lục chuẩn.")

    log.info("Đã tìm thấy Mục lục Metadata (Outline). Sử dụng Level 1.")

    # Mở lại bằng pdfplumber để lấy text (pdfplumber extract text ngon hơn pypdf)
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)

        for i in range(len(outlines)):
            current_chap = outlines[i]
            start_p = current_chap["page_start"] - 1  # index từ 0

            # Xác định trang kết thúc (là trang bắt đầu của chương sau - 1)
            if i < len(outlines) - 1:
                end_p = outlines[i + 1]["page_start"] - 1
            else:
                end_p = total_pages  # Chương cuối thì lấy hết

            # Đảm bảo không vượt quá file
            end_p = min(end_p, total_pages)

            # Gom text từ start_p đến end_p
            chap_text = ""
            for p_idx in range(start_p, end_p):
                text = pdf.pages[p_idx].extract_text()
                if text:
                    chap_text += text + "\n"

            if chap_text.strip():
                chapters.append(
                    {"title": current_chap["title"], "text": chap_text, "page_start": start_p + 1, "page_end": end_p})

    return chapters


async def extract_text_from_pdf(file_obj, max_pages=None):
    """
    Helper function: Extract raw text từ PDF (không chia chương).
    Dùng cho demo endpoints như /process-book-intro.

    Args:
        file_obj: File object của PDF
        max_pages: Số trang tối đa cần extract (None = all pages)

    Returns:
        str: Raw text từ PDF
    """
    file_obj.seek(0)
    extracted_text = ""

    with pdfplumber.open(file_obj) as pdf:
        pages_to_read = len(pdf.pages) if max_pages is None else min(
            max_pages, len(pdf.pages))

        for i in range(pages_to_read):
            text = pdf.pages[i].extract_text()
            if text:
                extracted_text += text + "\n"

    return extracted_text.strip()


def extract_text_by_page_range(pdf_obj, start_page: int, end_page: int):
    """
    Trích xuất text từ trang A đến trang B.
    - pdf_obj: Đối tượng pdfplumber đã mở.
    - start_page: Số trang thực tế (ví dụ: 5).
    - end_page: Số trang thực tế (ví dụ: 10).
    -> Trả về text của trang 5, 6, 7, 8, 9, 10.
    """
    extracted_text = ""

    # Validate: Đảm bảo trang kết thúc không vượt quá tổng số trang
    total_pages = len(pdf_obj.pages)
    if end_page > total_pages:
        end_page = total_pages

    # Vòng lặp lấy text
    # LƯU Ý: Python index bắt đầu từ 0.
    # Nếu muốn lấy trang 5 (start_page), index phải là 4 (start_page - 1).
    # Hàm range(a, b) chạy đến b-1, nên tham số thứ 2 là end_page (tương ứng index end_page-1)

    # Ví dụ: Lấy trang 5 đến 7.
    # start_page=5 -> index=4
    # end_page=7
    # range(4, 7) sẽ chạy qua index: 4 (trang 5), 5 (trang 6), 6 (trang 7). CHUẨN.

    for i in range(start_page - 1, end_page):
        try:
            page = pdf_obj.pages[i]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception as e:
            log.warning(f"Lỗi đọc trang {i + 1}: {e}")

    return extracted_text


def extract_clean_text(page):
    """
    Chỉ lấy phần thân trang, bỏ Header (trên cùng) và Footer (số trang dưới cùng)
    """
    width = page.width
    height = page.height

    # Giả sử Header chiếm 50px trên cùng, Footer chiếm 50px dưới cùng
    # Tọa độ crop: (x0, top, x1, bottom)
    bounding_box = (0, 50, width, height - 50)

    try:
        cropped_page = page.crop(bounding_box)
        return cropped_page.extract_text()
    except ValueError:
        # Fallback nếu trang không crop được (ví dụ trang trắng)
        return page.extract_text()

```

### app\services\rag_service.py

```py
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.supabase import supabase

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def search_book_knowledge(query: str, document_ids: list[str]):
    # 1. Tạo embedding cho câu hỏi của user
    res = await ai_client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC match_book_knowledge đã tạo ở Supabase
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.3,
        "match_count": 10,
        "filter_book_ids": document_ids
    }).execute()

    if not result.data:
        return "Không tìm thấy thông tin cụ thể trong sách."

    return result.data

```

### app\services\storage_service.py

```py
"""
app/services/storage_service.py
=================================
Utility service để upload file lên Supabase Storage.

Trước đây là app/helper/upload2supabase.py.
Di chuyển vào services/ để thống nhất cấu trúc dự án.
"""

import asyncio

import aiofiles

from app.core.supabase import supabase

from app.core.logger import log as logger


async def upload_file_to_supabase(
    local_path: str,
    storage_path: str,
    bucket: str,
    content_type: str,
    max_retries: int = 3,
    upsert: bool = True,
) -> str:
    """
    Upload file lên Supabase Storage và trả về public URL.

    Args:
        local_path: Đường dẫn file local cần upload.
        storage_path: Đường dẫn đích trong bucket.
        bucket: Tên bucket Supabase (vd: "raw_books", "audios").
        content_type: MIME type của file.
        max_retries: Số lần retry nếu upload thất bại (default 3).
        upsert: Ghi đè nếu file đã tồn tại (default True — cần cho switch-mode).

    Returns:
        Public URL của file sau khi upload thành công.
    """
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
            )
            return supabase.storage.from_(bucket).get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2**attempt
                logger.warning(f"Upload failed (attempt {attempt + 1}/{max_retries}), retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise

```

### app\services\study_context_service.py

```py
import uuid
from datetime import datetime, timezone

from sqlmodel import Session

from app.core.exceptions import BookNotFoundError, StudyContextNotFoundError
from app.models.db_models import ChatThread, StudyContext, StudyContextDocumentLink
from app.repositories.audiobook_repo import get_book_by_id
from app.repositories.study_context_document_link_repo import create_new_context_document
from app.repositories.study_context_repo import create_study_context, get_study_context
from app.repositories.study_context_thread_repo import create_new_thread
from app.schemas.study_context import ChatThreadInput, StudyContextDocumentInput, StudyContextInput


def _get_owned_context(session: Session, context_id: uuid.UUID, user_id: uuid.UUID) -> StudyContext:
    """Helper: Lấy context và kiểm tra ownership. Raise nếu không tìm thấy hoặc không thuộc user."""
    context = get_study_context(session, context_id)
    if not context or context.user_id != user_id:
        raise StudyContextNotFoundError()
    return context


def create_context(session: Session, user_id: uuid.UUID, payload: StudyContextInput) -> StudyContext:
    """Tạo mới một StudyContext cho user."""
    context = StudyContext(
        user_id=user_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_study_context(session, context)


def get_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> StudyContext:
    """Lấy context và kiểm tra ownership. Dùng cho router GET."""
    return _get_owned_context(session, context_id, user_id)


def update_context_title(session: Session, user_id: uuid.UUID, context_id: uuid.UUID, title: str) -> StudyContext:
    """Validate ownership rồi cập nhật title."""
    from app.repositories.study_context_repo import update_study_context
    _get_owned_context(session, context_id, user_id)
    updated = update_study_context(session, context_id, title)
    if not updated:
        raise StudyContextNotFoundError()
    return updated


def delete_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> None:
    """Validate ownership rồi xóa context."""
    from app.repositories.study_context_repo import delete_study_context
    _get_owned_context(session, context_id, user_id)
    delete_study_context(session, context_id)


def add_document_to_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: StudyContextDocumentInput,
) -> StudyContextDocumentLink:
    """Validate book và context, sau đó tạo link giữa context và document."""
    book = get_book_by_id(session, payload.book_id)
    if not book:
        raise BookNotFoundError()

    _get_owned_context(session, context_id, user_id)

    link = StudyContextDocumentLink(context_id=context_id, book_id=payload.book_id)
    return create_new_context_document(session, link)


def delete_document_from_context(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    book_id: uuid.UUID,
) -> None:
    """Validate ownership rồi xóa document link."""
    from app.repositories.study_context_document_link_repo import delete_study_context_document
    _get_owned_context(session, context_id, user_id)
    delete_study_context_document(session, context_id, book_id)


def get_threads_for_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> list:
    """Validate ownership rồi trả về danh sách threads."""
    from app.repositories.study_context_thread_repo import get_chat_threads_for_context
    _get_owned_context(session, context_id, user_id)
    return get_chat_threads_for_context(session, context_id)


def create_thread(
    session: Session,
    user_id: uuid.UUID,
    context_id: uuid.UUID,
    payload: ChatThreadInput,
) -> ChatThread:
    """Validate context ownership rồi tạo mới ChatThread."""
    _get_owned_context(session, context_id, user_id)

    thread = ChatThread(
        context_id=context_id,
        title=payload.title,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return create_new_thread(session, thread)

```

### app\services\tts_service.py

```py

import asyncio

import edge_tts
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import log

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
        log.error(f"Error in TTS Stream: {e}")


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
        log.info(f"Audio saved to {filename}")
    except Exception as e:
        log.error(f"Error creating audio file: {e}")


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
        raise ValueError(
            f"Text too short for TTS ({len(cleaned)} chars): '{cleaned}'")

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
                    log.warning(
                        f"TTS attempt {attempt + 1}/{max_retries} failed "
                        f"({len(cleaned)} chars): {e}. Retry in {wait}s..."
                    )
                    await asyncio.sleep(wait)
                else:
                    log.error(
                        f"TTS failed after {max_retries} attempts ({len(cleaned)} chars): {e}")
                    raise
    return 0  # unreachable

```

### app\services\upload_service.py

```py
import os
import uuid

import aiofiles
from fastapi import BackgroundTasks, UploadFile
from sqlmodel import Session

from app.core.config import settings
from app.core.constant import BookStatus, PlanStatus
from app.core.exceptions import (
    BookNotFoundError,
    BookStatusConflictError,
    DatabaseError,
    FileTooLargeError,
    PdfExtractionError,
    UnsupportedFileTypeError,
)
from app.models.db_models import Book, Chapter, ReadingPlan
from app.repositories.audiobook_repo import create_book, update_book_status
from app.repositories.chapter_repo import create_chapter
from app.repositories.plan_repo import create_reading_plan
from app.schemas.plan import PlanInput
from app.services.pdf_service import extract_chapters_smart
from app.services.storage_service import upload_file_to_supabase
from app.services.workers.book_pipeline import run_background_processing

from app.core.logger import log as logger

# TODO: REPLACE WITH JWT DECODE USER LATER
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


async def handle_upload_document(session: Session, file: UploadFile) -> dict:
    """
    Bước 1: Validate file, extract outline từ PDF, upload lên Supabase Storage,
    lưu Book + Chapter (DRAFT) vào DB, trả về outline cho Flutter.
    """
    # 1. Validate MIME Type hoặc đuôi file
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()

    if not is_valid_type:
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise UnsupportedFileTypeError(
                f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX."
            )

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError()

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)

    chapters_data = []
    file_url = ""
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract outline từ PDF
        with open(tmp_filename, "rb") as f:
            chapters_data = await extract_chapters_smart(f)

        if not chapters_data:
            raise PdfExtractionError()

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.pdf"
        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type="application/pdf",
        )
        logger.info(f"☁️  PDF uploaded to Storage: {storage_path}")

    finally:
        # Dọn rác: Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    # 5. Lưu DB: Book (DRAFT) + Chapters (DRAFT)
    title = (file.filename or "unknown").rsplit(".", 1)[0]
    try:
        book = Book(
            id=book_id,
            user_id=MOCK_USER_ID,
            title=title,
            total_chapters=len(chapters_data),
            status=BookStatus.DRAFT,
            file_url=file_url,
        )
        create_book(session, book)

        for i, chap in enumerate(chapters_data):
            chapter = Chapter(
                book_id=book_id,
                chapter_index=i,
                title=chap.get("title", "Empty Chapter"),
                status=BookStatus.DRAFT,
            )
            create_chapter(session, chapter)

        session.commit()
        logger.info(f"📘 Created DRAFT book {book_id} | {len(chapters_data)} chapters | file_url saved")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    # 6. Trả về outline để Flutter hiển thị
    outline = [{"title": c.get("title", f"Chương {i + 1}"), "page_start": c.get("page_start", 0)} for i, c in enumerate(chapters_data)]

    return {
        "book_id": str(book_id),
        "total_chapters": len(chapters_data),
        "outline": outline,
    }


async def handle_generate_plan(session: Session, background_tasks: BackgroundTasks, payload: PlanInput) -> dict:
    """
    Bước 2: Validate trạng thái sách, tạo ReadingPlan, kick-off background processing.
    """
    # 1. Validate book tồn tại và đang ở trạng thái DRAFT
    book = session.get(Book, payload.book_id)
    if not book:
        raise BookNotFoundError()
    if book.status not in (BookStatus.DRAFT):
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    # 2. Lưu ReadingPlan + cập nhật Book status
    try:
        plan = ReadingPlan(
            book_id=payload.book_id,
            mode=payload.mode,
            pace=payload.pace,
            schedule_config=payload.schedule_config,
            status=PlanStatus.ACTIVE,
        )
        create_reading_plan(session, plan)
        update_book_status(session, payload.book_id, BookStatus.PROCESSING)

        logger.info(f"📋 ReadingPlan created for book {payload.book_id} | mode={payload.mode}")
    except Exception as e:
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    # 3. Kick-off background task — trả 200 OK ngay
    background_tasks.add_task(run_background_processing, payload.book_id, payload.mode)

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "mode": payload.mode,
    }

```

### app\services\workers\book_pipeline.py

```py
"""
Pipeline điều phối xử lý toàn bộ sách ở background.

Trách nhiệm:
    - Fetch book data + draft chapters từ DB
    - Download PDF từ Supabase Storage
    - Re-extract text per-chapter
    - Dispatch chapter tasks song song
    - Cập nhật Book status khi hoàn tất hoặc lỗi

Entry points (được gọi từ FastAPI BackgroundTasks):
    - run_background_processing(): Xử lý sách mới (RAG + TTS)
    - run_switch_mode_processing(): Sinh lại audio khi user đổi mode
"""

import asyncio
import io
import uuid

from sqlmodel import Session, select

from app.core.constant import BookStatus
from app.core.supabase import supabase
from app.db.database import engine
from app.models.db_models import Book, Chapter
from app.repositories.audiobook_repo import update_book_status
from app.repositories.chapter_repo import get_draft_chapters_by_book
from app.services.pdf_service import extract_chapters_smart
from app.services.workers.chapter_worker import process_chapter, process_switch_mode_chapter

from app.core.logger import log as logger


async def run_background_processing(book_id: uuid.UUID, mode: str) -> None:
    """
    Điều phối xử lý tất cả chapters song song sau khi user upload sách.

    Flow:
        1. Fetch book + draft chapters từ DB
        2. Download PDF từ Supabase Storage (file_url đã lưu lúc /upload)
        3. Re-extract text per-chapter từ PDF
        4. Chạy process_chapter() song song cho tất cả chapters
        5. Cập nhật Book status → READY hoặc ERROR
    """
    try:
        # ── 1. Fetch book + draft chapters ───────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            draft_chapters = get_draft_chapters_by_book(session, book_id)

        if not book:
            logger.error(f"Book {book_id} not found")
            return

        if not draft_chapters:
            with Session(engine) as session:
                update_book_status(session, book_id, BookStatus.ERROR, "Không có chapter nào để xử lý.")
            return

        if not book.file_url:
            with Session(engine) as session:
                update_book_status(
                    session, book_id, BookStatus.ERROR,
                    "file_url chưa được lưu — PDF chưa upload lên Storage."
                )
            logger.error(f"book.file_url is missing for book {book_id}")
            return

        # ── 2. Download PDF từ Supabase Storage ──────────────────────────────
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF from Storage: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)

        # ── 3. Re-extract chapters text từ PDF ───────────────────────────────
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 4. Dispatch song song — bị giới hạn bởi Semaphore trong chapter_worker ──
        tasks = []
        for draft_chap in draft_chapters:
            raw_text = chapters_map.get(draft_chap.chapter_index, "")
            if not raw_text.strip():
                logger.warning(
                    f"⚠️ Chapter {draft_chap.chapter_index + 1} '{draft_chap.title}' "
                    f"không có text — bỏ qua."
                )
                continue
            tasks.append(
                process_chapter(book_id, draft_chap.id, draft_chap.chapter_index, raw_text, mode)
            )

        await asyncio.gather(*tasks)

        # ── 5. Cập nhật Book status → READY ──────────────────────────────────
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.READY)
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.ERROR, str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str) -> None:
    """
    Sinh lại audio cho tất cả chapters khi user chuyển mode học.

    Bỏ qua RAG — knowledge base không thay đổi theo mode.
    Chỉ xóa segments cũ của mode mới và sinh TTS mới.
    """
    try:
        # ── 1. Fetch book + all chapters ─────────────────────────────────────
        with Session(engine) as session:
            book = session.get(Book, book_id)
            chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id)).all()

        if not book or not book.file_url:
            logger.error(f"Cannot switch mode for book {book_id}: book missing or no file_url")
            return

        # ── 2. Download PDF + extract text ───────────────────────────────────
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF for switch mode: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # ── 3. Dispatch song song ─────────────────────────────────────────────
        tasks = [
            process_switch_mode_chapter(book_id, chap.id, chap.chapter_index, raw_text, new_mode)
            for chap in chapters
            if (raw_text := chapters_map.get(chap.chapter_index, "")) and raw_text.strip()
        ]

        await asyncio.gather(*tasks)
        logger.info(f"🎉 Book {book_id} đã gen xong audio cho mode: {new_mode}.")

    except Exception as e:
        logger.error(f"❌ LỖI SWITCH MODE SÁCH {book_id}: {e}")

```

### app\services\workers\chapter_worker.py

```py
"""
Worker xử lý 1 chapter trong pipeline background.

Trách nhiệm:
    - Điều phối 2 pipeline song song: RAG (embed) + TTS
    - Giới hạn concurrency qua Semaphore (tránh quá tải DB + external API)
    - Xử lý rollback gọn gàng khi chapter thất bại
    - Xử lý switch-mode (chỉ TTS, không RAG)

Concurrency model:
    sem = Semaphore(5) → tối đa 5 chapters xử lý song song cùng lúc.
    Mỗi chapter trong normal path sử dụng tối đa 3 DB sessions:
        - RAG pipeline: 1 session
        - TTS pipeline: 1 session (gom từ 3 sessions cũ)
        - Chapter status update: 1 session
    → 5 chapters × 3 sessions = 15 connections tối đa (pool_size=10 + overflow=20 → an toàn)
"""

import asyncio
import uuid

from sqlmodel import Session

from app.core.constant import BookStatus
from app.db.database import engine
from app.repositories.book_knowledge_repo import delete_knowledge_by_chapter
from app.repositories.chapter_repo import delete_chapter, update_chapter_status
from app.repositories.chapter_segment_repo import delete_segments_by_chapter_and_mode
from app.services.embed_service import embed_and_save_chapter
from app.services.workers.tts_worker import run_tts_pipeline

from app.core.logger import log as logger

# Tối đa 5 chapters xử lý song song — cân bằng giữa tốc độ và tải hệ thống
sem = asyncio.Semaphore(5)


async def _run_rag_pipeline(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
) -> None:
    """Pipeline RAG: cắt chunks → embed → lưu book_knowledge (1 session)."""
    with Session(engine) as session:
        await embed_and_save_chapter(book_id, chapter_id, raw_text, session)


async def process_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """
    Xử lý đầy đủ 1 chapter: chạy RAG + TTS song song, cập nhật status.

    Nếu thất bại: rollback book_knowledge + xóa chapter để đảm bảo
    không còn dữ liệu không nhất quán.
    """
    async with sem:
        try:
            # RAG và TTS chạy song song — mỗi pipeline dùng session riêng
            await asyncio.gather(
                _run_rag_pipeline(book_id, chapter_id, raw_text),
                run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, mode),
            )
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, BookStatus.READY)
            logger.info(f"✅ Chapter {chapter_index + 1} READY")

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} thất bại: {e}")
            # Rollback: xóa book_knowledge TRƯỚC (FK constraint) rồi mới xóa chapter
            try:
                with Session(engine) as session:
                    delete_knowledge_by_chapter(session, chapter_id)
                    delete_chapter(session, chapter_id)
                logger.info(f"🗑️ Rollback chapter {chapter_index + 1} thành công.")
            except Exception as rollback_err:
                logger.error(f"Failed to rollback chapter {chapter_index + 1}: {rollback_err}")
            raise


async def process_switch_mode_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
) -> None:
    """
    Switch mode 1 chapter: xóa segments cũ → chạy TTS mới (bỏ qua RAG).

    Không cần RAG vì knowledge base không thay đổi theo mode.
    """
    async with sem:
        try:
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, new_mode)

            await run_tts_pipeline(book_id, chapter_id, chapter_index, raw_text, new_mode)
            logger.info(f"✅ Chapter {chapter_index + 1} switch mode '{new_mode}' READY")

        except Exception as e:
            logger.error(f"❌ Chapter {chapter_index + 1} switch mode thất bại: {e}")
            raise

```

### app\services\workers\tts_worker.py

```py
"""
app/services/workers/tts_worker.py
====================================
Worker xử lý TTS (Text-to-Speech) cho 1 chapter.

Trách nhiệm:
    1. Gọi LLM rewrite text → main_scripts + review_script
    2. TTS từng segment → upload audio lên Storage
    3. Lưu tất cả kết quả vào DB trong **1 session duy nhất**
       (thay vì 3 sessions riêng biệt như trước → giảm connection overhead)
"""

import os
import uuid

from sqlmodel import Session

from app.db.database import engine
from app.models.db_models import ChapterSegment
from app.repositories.chapter_repo import update_chapter_review_audio, update_chapter_review_text
from app.repositories.chapter_segment_repo import bulk_create_segments
from app.services.llm_service import normalize_text_for_speech
from app.services.storage_service import upload_file_to_supabase
from app.services.tts_service import generate_audio_and_get_duration

from app.core.logger import log as logger


async def run_tts_pipeline(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """
    Pipeline TTS đầy đủ cho 1 chapter:
      LLM rewrite → TTS segments → upload → review audio → lưu DB (1 session).

    Ghi chú về Session:
        Tất cả DB writes (review_text, segments, review_audio) được gom vào
        **1 Session duy nhất** ở cuối pipeline, tránh mở-đóng nhiều connections.
    """
    # ── Step 1: LLM Rewrite ──────────────────────────────────────────────────
    obj_chapter = await normalize_text_for_speech(raw_text, mode)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # ── Step 2: TTS + Upload segments ────────────────────────────────────────
    segments: list[ChapterSegment] = []
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/part_{i + 1}.mp3"
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            segments.append(
                ChapterSegment(
                    chapter_id=chapter_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                    mode=mode,
                )
            )
        except Exception as seg_err:
            text_preview = script[:80] if script else "(empty)"
            logger.warning(
                f"⚠️ Segment {i + 1} chương {chapter_index + 1} lỗi TTS "
                f"({len(script)} chars, text='{text_preview}...'): {seg_err}"
            )
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)

    # ── Step 3: TTS Review audio ─────────────────────────────────────────────
    review_url: str | None = None
    if review_text and review_text.strip():
        local_review = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            await generate_audio_and_get_duration(review_text, local_review)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/review.mp3"
            review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
        except Exception as rev_err:
            logger.warning(f"⚠️ Review audio chương {chapter_index + 1} lỗi, bỏ qua: {rev_err}")
        finally:
            if os.path.exists(local_review):
                os.remove(local_review)

    # ── Step 4: Lưu tất cả vào DB — 1 Session duy nhất ──────────────────────
    with Session(engine) as session:
        if review_text:
            update_chapter_review_text(session, chapter_id, review_text, mode)
        if segments:
            bulk_create_segments(session, segments)
        if review_url:
            update_chapter_review_audio(session, chapter_id, review_url, mode)

```

### app\services\workers\__init__.py

```py
"""Worker pipeline package cho background processing."""

```

### app\services\__init__.py

```py
# Services module

```

### app\__init__.py

```py
# TRIAM Backend Application

```
