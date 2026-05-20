import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import ProcessingJobStatus, ProcessingJobType
from app.db.database import engine
from app.main import app
from app.models.db_models import ProcessingJob

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def test_get_job_status_returns_progress_summary():
    client = TestClient(app)
    with Session(engine) as session:
        job = ProcessingJob(
            user_id=MOCK_USER_ID,
            book_id=None,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.PROCESSING,
            progress_percent=25,
            current_step="Testing progress",
            total_units=4,
            done_units=1,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_id = job.id

    response = client.get(f"/api/v1/jobs/{job_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == str(job_id)
    assert body["progress_percent"] == 25
    assert body["status"] == "processing"
    assert body["job_type"] == "generate_plan"

    with Session(engine) as session:
        saved = session.get(ProcessingJob, job_id)
        if saved:
            session.delete(saved)
            session.commit()
