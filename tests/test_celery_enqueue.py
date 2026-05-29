import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import BookStatus, DocumentType, ProcessingJobStatus, ProcessingJobType
from app.db.database import engine
from app.main import app
from app.models.db_models import Book, BookSection, ProcessingJob

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def _add_section(session: Session, book_id: uuid.UUID, *, title: str = "Unit Source") -> None:
    session.add(
        BookSection(
            book_id=book_id,
            section_index=0,
            title=title,
            level=1,
            path="1",
            text_content="Nội dung đủ để tạo bài học.",
            text_char_count=28,
        )
    )
    session.commit()


def test_generate_plan_enqueues_document_task(monkeypatch):
    calls = []

    def fake_apply_async(*, args, queue):
        calls.append({"args": args, "queue": queue})

    monkeypatch.setattr("app.services.upload_service.process_book_task.apply_async", fake_apply_async)

    with Session(engine) as session:
        book = Book(
            user_id=MOCK_USER_ID,
            title="Celery Enqueue Test",
            total_sections=1,
            status=BookStatus.DRAFT,
            document_type=DocumentType.PDF,
            file_url="https://example.test/storage/v1/object/public/raw_books/test/original.pdf",
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        _add_section(session, book.id)
        book_id = book.id

    response = TestClient(app).post(
        "/api/v1/generate-plan",
        json={"book_id": str(book_id), "mode": "full", "pace": 1, "schedule_config": ["Mon"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["job_id"]
    assert body["status"] == "queued"
    assert calls == [{"args": [str(book_id), "full", body["job_id"]], "queue": "document"}]

    with Session(engine) as session:
        saved = session.get(Book, book_id)
        if saved:
            session.delete(saved)
            session.commit()


def test_switch_mode_enqueues_document_task(monkeypatch):
    calls = []

    def fake_apply_async(*, args, queue):
        calls.append({"args": args, "queue": queue})

    monkeypatch.setattr("app.services.audiobook_service.switch_mode_task.apply_async", fake_apply_async)

    with Session(engine) as session:
        book = Book(
            user_id=MOCK_USER_ID,
            title="Switch Mode Enqueue Test",
            total_sections=1,
            total_units=1,
            status=BookStatus.READY,
            document_type=DocumentType.PDF,
            file_url="https://example.test/storage/v1/object/public/raw_books/test/original.pdf",
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        _add_section(session, book.id)
        book_id = book.id

    plan_response = TestClient(app).post(
        "/api/v1/generate-plan",
        json={"book_id": str(book_id), "mode": "full", "pace": 1, "schedule_config": ["Mon"]},
    )
    assert plan_response.status_code == 409

    from app.core.constant import PlanMode, PlanStatus
    from app.models.db_models import ReadingPlan

    with Session(engine) as session:
        plan = ReadingPlan(book_id=book_id, mode=PlanMode.FULL, pace=1, schedule_config=["Mon"], status=PlanStatus.ACTIVE)
        session.add(plan)
        session.commit()

    response = TestClient(app).post(f"/api/v1/books/{book_id}/switch-mode", json={"mode": "pareto"})

    assert response.status_code == 200
    body = response.json()
    assert body["needs_generation"] is True
    assert body["job_id"]
    assert calls == [{"args": [str(book_id), "pareto", body["job_id"]], "queue": "document"}]

    with Session(engine) as session:
        saved = session.get(Book, book_id)
        if saved:
            session.delete(saved)
            session.commit()


def test_process_book_task_calls_pipeline(monkeypatch):
    calls = []
    book_id = uuid.uuid4()
    job_id = uuid.uuid4()

    async def fake_pipeline(received_book_id, received_mode, received_job_id):
        calls.append((received_book_id, received_mode, received_job_id))

    monkeypatch.setattr("app.tasks.book_tasks.run_background_processing", fake_pipeline)

    from app.tasks.book_tasks import process_book_task

    process_book_task(str(book_id), "full", str(job_id))

    assert calls == [(book_id, "full", job_id)]


def test_process_book_task_skips_ready_job(monkeypatch):
    calls = []
    book_id = uuid.uuid4()

    async def fake_pipeline(received_book_id, received_mode, received_job_id):
        calls.append((received_book_id, received_mode, received_job_id))

    monkeypatch.setattr("app.tasks.book_tasks.run_background_processing", fake_pipeline)

    with Session(engine) as session:
        job = ProcessingJob(
            user_id=MOCK_USER_ID,
            book_id=None,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.READY,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_id = job.id

    from app.tasks.book_tasks import process_book_task

    process_book_task(str(book_id), "full", str(job_id))

    assert calls == []

    with Session(engine) as session:
        saved = session.get(ProcessingJob, job_id)
        if saved:
            session.delete(saved)
            session.commit()


def test_switch_mode_task_calls_pipeline(monkeypatch):
    calls = []
    book_id = uuid.uuid4()
    job_id = uuid.uuid4()

    async def fake_pipeline(received_book_id, received_mode, received_job_id):
        calls.append((received_book_id, received_mode, received_job_id))

    monkeypatch.setattr("app.tasks.book_tasks.run_switch_mode_processing", fake_pipeline)

    from app.tasks.book_tasks import switch_mode_task

    switch_mode_task(str(book_id), "pareto", str(job_id))

    assert calls == [(book_id, "pareto", job_id)]


def test_switch_mode_task_skips_ready_job(monkeypatch):
    calls = []
    book_id = uuid.uuid4()

    async def fake_pipeline(received_book_id, received_mode, received_job_id):
        calls.append((received_book_id, received_mode, received_job_id))

    monkeypatch.setattr("app.tasks.book_tasks.run_switch_mode_processing", fake_pipeline)

    with Session(engine) as session:
        job = ProcessingJob(
            user_id=MOCK_USER_ID,
            book_id=None,
            job_type=ProcessingJobType.SWITCH_MODE,
            status=ProcessingJobStatus.READY,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_id = job.id

    from app.tasks.book_tasks import switch_mode_task

    switch_mode_task(str(book_id), "pareto", str(job_id))

    assert calls == []

    with Session(engine) as session:
        saved = session.get(ProcessingJob, job_id)
        if saved:
            session.delete(saved)
            session.commit()
