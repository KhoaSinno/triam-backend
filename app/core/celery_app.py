from celery import Celery
from celery.schedules import schedule

from app.core.config import settings

celery_app = Celery(
    "triam",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND or None,
    include=["app.tasks.book_tasks", "app.tasks.notification_tasks"],
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
    task_reject_on_worker_lost=True,
    result_expires=3600,
    broker_pool_limit=settings.CELERY_BROKER_POOL_LIMIT,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    worker_cancel_long_running_tasks_on_connection_loss=settings.CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS,
    broker_connection_retry_on_startup=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    broker_transport_options={
        "visibility_timeout": settings.CELERY_VISIBILITY_TIMEOUT_SECONDS,
        "socket_keepalive": True,
        "health_check_interval": 30,
    },
    task_routes={
        "triam.books.process": {"queue": "document"},
        "triam.books.switch_mode": {"queue": "document"},
        "triam.books.index_sections": {"queue": "document"},
        "triam.books.purge_storage_assets": {"queue": "document"},
        "triam.books.generate_summary": {"queue": "document"},
        "triam.notifications.scan_due": {"queue": "maintenance"},
        "triam.notifications.deliver_due": {"queue": "notification"},
    },
    beat_schedule={
        "scan-due-notifications": {
            "task": "triam.notifications.scan_due",
            "schedule": schedule(run_every=settings.NOTIFICATION_SCAN_INTERVAL_SECONDS),
            "options": {"queue": "maintenance"},
        }
    },
)
