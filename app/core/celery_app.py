from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "triam",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND or None,
    include=["app.tasks.book_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_ignore_result=True,
    task_acks_late=True,
    result_expires=3600,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    broker_connection_retry_on_startup=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    broker_transport_options={
        "visibility_timeout": 3600,
        "socket_keepalive": True,
        "health_check_interval": 30,
    },
    task_routes={
        "triam.books.process": {"queue": "document"},
        "triam.books.switch_mode": {"queue": "document"},
    },
)
