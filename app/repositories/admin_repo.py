import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from sqlalchemy import union_all
from sqlmodel import Session, func, select

from app.core.constant import ProcessingJobStatus, ProcessingJobType
from app.models.db_models import AdminAuditLog, AdminUser, Book, LearningUnit, LearningUnitSegment, ProcessingJob, UserNotification


def _key(value: object) -> str:
    if isinstance(value, Enum):
        return value.value
    return str(value or "unknown")


def get_active_admin_user(session: Session, user_id: uuid.UUID) -> AdminUser | None:
    return session.exec(select(AdminUser).where(AdminUser.user_id == user_id, AdminUser.is_active.is_(True))).first()


def create_admin_audit_log(
    session: Session,
    *,
    admin_user_id: uuid.UUID,
    action: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    metadata: dict[str, Any] | None = None,
) -> AdminAuditLog:
    audit_log = AdminAuditLog(
        admin_user_id=admin_user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        metadata_json=metadata,
    )
    session.add(audit_log)
    return audit_log


def get_admin_dashboard(session: Session) -> dict[str, Any]:
    since_24h = datetime.now(timezone.utc) - timedelta(hours=24)
    since_30d = datetime.now(timezone.utc) - timedelta(days=30)

    book_count = int(session.exec(select(func.count(Book.id))).one() or 0)
    job_count = int(session.exec(select(func.count(ProcessingJob.id))).one() or 0)
    user_count = count_admin_users(session)

    books_by_status = {
        _key(status): int(count)
        for status, count in session.exec(select(Book.status, func.count(Book.id)).group_by(Book.status)).all()
    }
    jobs_by_status = {
        _key(status): int(count)
        for status, count in session.exec(select(ProcessingJob.status, func.count(ProcessingJob.id)).group_by(ProcessingJob.status)).all()
    }
    failed_jobs_last_24h = int(
        session.exec(
            select(func.count(ProcessingJob.id)).where(
                ProcessingJob.status == ProcessingJobStatus.ERROR,
                ProcessingJob.updated_at >= since_24h,
            )
        ).one()
        or 0
    )
    usage_row = session.exec(
        select(
            func.coalesce(func.sum(ProcessingJob.estimated_input_tokens), 0),
            func.coalesce(func.sum(ProcessingJob.estimated_audio_seconds), 0),
        ).where(ProcessingJob.created_at >= since_30d)
    ).one()

    return {
        "user_count": user_count,
        "book_count": book_count,
        "job_count": job_count,
        "books_by_status": books_by_status,
        "jobs_by_status": jobs_by_status,
        "failed_jobs_last_24h": failed_jobs_last_24h,
        "estimated_input_tokens_last_30d": int(usage_row[0] or 0),
        "estimated_audio_seconds_last_30d": int(usage_row[1] or 0),
    }


def _admin_user_ids_query():
    return union_all(
        select(Book.user_id),
        select(ProcessingJob.user_id),
        select(UserNotification.user_id),
    ).subquery()


def count_admin_users(session: Session) -> int:
    user_ids = _admin_user_ids_query()
    grouped_users = select(user_ids.c.user_id).group_by(user_ids.c.user_id).subquery()
    return int(session.exec(select(func.count()).select_from(grouped_users)).one() or 0)


def list_admin_users(session: Session, *, limit: int, offset: int) -> tuple[list[dict[str, Any]], int]:
    user_ids_query = _admin_user_ids_query()
    user_ids = list(
        session.exec(
            select(user_ids_query.c.user_id)
            .group_by(user_ids_query.c.user_id)
            .order_by(user_ids_query.c.user_id)
            .offset(offset)
            .limit(limit)
        ).all()
    )
    total = count_admin_users(session)
    if not user_ids:
        return [], total

    book_stats = {
        user_id: {"book_count": int(book_count), "last_book_at": last_book_at}
        for user_id, book_count, last_book_at in session.exec(
            select(Book.user_id, func.count(Book.id), func.max(Book.updated_at)).where(Book.user_id.in_(user_ids)).group_by(Book.user_id)
        ).all()
    }
    job_stats = {
        user_id: {"job_count": int(job_count), "last_job_at": last_job_at}
        for user_id, job_count, last_job_at in session.exec(
            select(ProcessingJob.user_id, func.count(ProcessingJob.id), func.max(ProcessingJob.updated_at))
            .where(ProcessingJob.user_id.in_(user_ids))
            .group_by(ProcessingJob.user_id)
        ).all()
    }
    notification_stats = {
        user_id: {"notification_count": int(notification_count), "last_notification_at": last_notification_at}
        for user_id, notification_count, last_notification_at in session.exec(
            select(UserNotification.user_id, func.count(UserNotification.id), func.max(UserNotification.created_at))
            .where(UserNotification.user_id.in_(user_ids))
            .group_by(UserNotification.user_id)
        ).all()
    }

    items: list[dict[str, Any]] = []
    for user_id in user_ids:
        book_data = book_stats.get(user_id, {})
        job_data = job_stats.get(user_id, {})
        notification_data = notification_stats.get(user_id, {})
        last_activity_candidates = [
            book_data.get("last_book_at"),
            job_data.get("last_job_at"),
            notification_data.get("last_notification_at"),
        ]
        items.append(
            {
                "user_id": user_id,
                "book_count": book_data.get("book_count", 0),
                "job_count": job_data.get("job_count", 0),
                "notification_count": notification_data.get("notification_count", 0),
                "last_activity_at": max([value for value in last_activity_candidates if value], default=None),
            }
        )
    return items, total


def list_admin_books(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    document_type: str | None = None,
    user_id: uuid.UUID | None = None,
    q: str | None = None,
) -> tuple[list[Book], int]:
    filters = []
    if status:
        filters.append(Book.status == status)
    if document_type:
        filters.append(Book.document_type == document_type)
    if user_id:
        filters.append(Book.user_id == user_id)
    if q:
        filters.append(Book.title.ilike(f"%{q.strip()}%"))

    total = int(session.exec(select(func.count(Book.id)).where(*filters)).one() or 0)
    books = list(session.exec(select(Book).where(*filters).order_by(Book.created_at.desc()).offset(offset).limit(limit)).all())
    return books, total


def get_admin_book_by_id(session: Session, book_id: uuid.UUID) -> Book | None:
    return session.get(Book, book_id)


def get_latest_admin_job_for_book(session: Session, book_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(select(ProcessingJob).where(ProcessingJob.book_id == book_id).order_by(ProcessingJob.created_at.desc())).first()


def count_learning_units_by_status(session: Session, book_id: uuid.UUID) -> dict[str, int]:
    return {
        _key(status): int(count)
        for status, count in session.exec(
            select(LearningUnit.status, func.count(LearningUnit.id)).where(LearningUnit.book_id == book_id).group_by(LearningUnit.status)
        ).all()
    }


def count_learning_unit_segments_for_book(session: Session, book_id: uuid.UUID) -> int:
    return int(
        session.exec(
            select(func.count(LearningUnitSegment.id))
            .join(LearningUnit, LearningUnit.id == LearningUnitSegment.learning_unit_id)
            .where(LearningUnit.book_id == book_id)
        ).one()
        or 0
    )


def list_admin_jobs(
    session: Session,
    *,
    limit: int,
    offset: int,
    status: ProcessingJobStatus | None = None,
    job_type: ProcessingJobType | None = None,
    user_id: uuid.UUID | None = None,
    book_id: uuid.UUID | None = None,
) -> tuple[list[ProcessingJob], int]:
    filters = []
    if status:
        filters.append(ProcessingJob.status == status)
    if job_type:
        filters.append(ProcessingJob.job_type == job_type)
    if user_id:
        filters.append(ProcessingJob.user_id == user_id)
    if book_id:
        filters.append(ProcessingJob.book_id == book_id)

    total = int(session.exec(select(func.count(ProcessingJob.id)).where(*filters)).one() or 0)
    jobs = list(session.exec(select(ProcessingJob).where(*filters).order_by(ProcessingJob.created_at.desc()).offset(offset).limit(limit)).all())
    return jobs, total


def list_admin_audit_logs(
    session: Session,
    *,
    limit: int,
    offset: int,
    action: str | None = None,
    admin_user_id: uuid.UUID | None = None,
) -> tuple[list[AdminAuditLog], int]:
    filters = []
    if action:
        filters.append(AdminAuditLog.action == action)
    if admin_user_id:
        filters.append(AdminAuditLog.admin_user_id == admin_user_id)

    total = int(session.exec(select(func.count(AdminAuditLog.id)).where(*filters)).one() or 0)
    logs = list(session.exec(select(AdminAuditLog).where(*filters).order_by(AdminAuditLog.created_at.desc()).offset(offset).limit(limit)).all())
    return logs, total
