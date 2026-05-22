from typing import Any

from redis import Redis
from sqlalchemy import text
from sqlmodel import Session

from app.core.config import settings
from app.db.database import engine

DOCUMENT_QUEUE_NAME = "document"


def _exception_name(exc: Exception) -> str:
    return type(exc).__name__


def get_background_health() -> dict[str, Any]:
    health: dict[str, Any] = {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
        "document_queue_length": None,
    }

    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1")).one()
    except Exception as exc:
        health["status"] = "degraded"
        health["database"] = "error"
        health["database_error"] = _exception_name(exc)

    redis_client: Redis | None = None
    try:
        redis_client = Redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)
        redis_client.ping()
        health["document_queue_length"] = redis_client.llen(DOCUMENT_QUEUE_NAME)
    except Exception as exc:
        health["status"] = "degraded"
        health["redis"] = "error"
        health["redis_error"] = _exception_name(exc)
    finally:
        if redis_client:
            redis_client.close()

    return health
