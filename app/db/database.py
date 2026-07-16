from typing import Any, Generator

from dotenv import load_dotenv
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.core.logger import log

load_dotenv()

DATABASE_POOL_MODES = {"auto", "queue", "null"}


def _normalize_pool_mode(pool_mode: str) -> str:
    mode = (pool_mode or "auto").strip().lower()
    if mode not in DATABASE_POOL_MODES:
        allowed = ", ".join(sorted(DATABASE_POOL_MODES))
        raise ValueError(f"DATABASE_POOL_MODE must be one of: {allowed}")
    return mode


def _is_supabase_pooler(database_url: str) -> bool:
    url = make_url(database_url)
    host = (url.host or "").lower()
    return url.port == 6543 or host.endswith(".pooler.supabase.com")


def should_use_null_pool(database_url: str, pool_mode: str = "auto") -> bool:
    mode = _normalize_pool_mode(pool_mode)
    if mode == "null":
        return True
    if mode == "queue":
        return False
    return _is_supabase_pooler(database_url)


def _connect_args_for(database_url: str) -> dict[str, Any]:
    url = make_url(database_url)
    if url.get_backend_name().startswith("postgresql") and settings.DATABASE_APPLICATION_NAME:
        return {"application_name": settings.DATABASE_APPLICATION_NAME}
    return {}


def create_db_engine(database_url: str | None = None, *, pool_mode: str | None = None) -> Engine:
    database_url = database_url or settings.DATABASE_URL
    pool_mode = pool_mode or settings.DATABASE_POOL_MODE
    common_args: dict[str, Any] = {
        "echo": settings.DATABASE_ECHO,
        "connect_args": _connect_args_for(database_url),
        "pool_pre_ping": settings.DATABASE_POOL_PRE_PING,
    }

    if should_use_null_pool(database_url, pool_mode):
        log.info("Database engine configured with NullPool.")
        return create_engine(database_url, poolclass=NullPool, **common_args)

    log.info(
        "Database engine configured with QueuePool "
        f"size={settings.DATABASE_POOL_SIZE}, overflow={settings.DATABASE_MAX_OVERFLOW}."
    )
    return create_engine(
        database_url,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_recycle=settings.DATABASE_POOL_RECYCLE,
        pool_use_lifo=settings.DATABASE_POOL_USE_LIFO,
        **common_args,
    )


engine = create_db_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def dispose_engine() -> None:
    engine.dispose()
