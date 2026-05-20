import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import ProcessingJobStatus
from app.models.db_models import ProcessingJob


def create_processing_job(session: Session, job: ProcessingJob) -> ProcessingJob:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_processing_job_by_id(session: Session, job_id: uuid.UUID) -> ProcessingJob | None:
    return session.get(ProcessingJob, job_id)


def get_processing_job_by_id_and_user(session: Session, job_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(select(ProcessingJob).where(ProcessingJob.id == job_id, ProcessingJob.user_id == user_id)).first()


def get_latest_processing_job_for_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(
        select(ProcessingJob)
        .where(
            ProcessingJob.book_id == book_id,
            ProcessingJob.user_id == user_id,
        )
        .order_by(ProcessingJob.created_at.desc())
    ).first()


def update_processing_job(
    session: Session,
    job_id: uuid.UUID,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> ProcessingJob | None:
    job = session.get(ProcessingJob, job_id)
    if not job:
        return None

    updates = {
        "status": status,
        "current_step": current_step,
        "total_units": total_units,
        "done_units": done_units,
        "failed_units": failed_units,
        "error_message": error_message,
        "started_at": started_at,
        "finished_at": finished_at,
    }
    for field_name, value in updates.items():
        if value is not None:
            setattr(job, field_name, value)

    if progress_percent is not None:
        job.progress_percent = max(0, min(100, progress_percent))

    job.updated_at = datetime.now(timezone.utc)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job
