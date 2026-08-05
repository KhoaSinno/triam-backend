import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.constant import BookStatus, DocumentType, PlanMode, ProcessingJobStatus, ProcessingJobType
from app.db.database import engine
from app.main import app
from app.models.db_models import AdminAuditLog, AdminUser, Book, ProcessingJob


def _get_all_admin_user_ids(client: TestClient) -> set[str]:
    user_ids: set[str] = set()
    offset = 0
    limit = 100

    while True:
        response = client.get(f"/api/v1/admin/users?limit={limit}&offset={offset}")
        assert response.status_code == 200
        body = response.json()
        user_ids.update(item["user_id"] for item in body["items"])
        offset += len(body["items"])
        if offset >= body["total"] or not body["items"]:
            return user_ids


def _cleanup(admin_user_id: uuid.UUID, book_ids: list[uuid.UUID], job_ids: list[uuid.UUID], auth_user_ids: list[uuid.UUID] = None) -> None:
    with Session(engine) as session:
        for audit_log in session.exec(select(AdminAuditLog).where(AdminAuditLog.admin_user_id == admin_user_id)).all():
            session.delete(audit_log)
        for job_id in job_ids:
            job = session.get(ProcessingJob, job_id)
            if job:
                session.delete(job)
        for book_id in book_ids:
            book = session.get(Book, book_id)
            if book:
                session.delete(book)
        admin_user = session.get(AdminUser, admin_user_id)
        if admin_user:
            session.delete(admin_user)
        if auth_user_ids:
            from app.repositories.admin_repo import auth_users
            session.execute(auth_users.delete().where(auth_users.c.id.in_(auth_user_ids)))
        session.commit()


def test_admin_route_requires_active_admin_user(auth_as):
    user_id = uuid.uuid4()
    auth_as(user_id)

    response = TestClient(app).get("/api/v1/admin/me")

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin permission required."


def test_admin_can_view_cross_user_books_and_dashboard(auth_as):
    from datetime import datetime, timezone

    from app.repositories.admin_repo import auth_users

    admin_user_id = uuid.uuid4()
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()
    book_ids: list[uuid.UUID] = []
    job_ids: list[uuid.UUID] = []

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        # Seed user_a and user_b in auth.users table
        user_a_email = f"user_a_{uuid.uuid4().hex[:6]}@triam.local"
        user_b_email = f"user_b_{uuid.uuid4().hex[:6]}@triam.local"
        session.execute(
            auth_users.insert().values(
                id=user_a,
                email=user_a_email,
                created_at=datetime.now(timezone.utc),
                raw_user_meta_data={"name": "User A"},
            )
        )
        session.execute(
            auth_users.insert().values(
                id=user_b,
                email=user_b_email,
                created_at=datetime.now(timezone.utc),
                raw_user_meta_data={"name": "User B"},
            )
        )
        book_a = Book(user_id=user_a, title="Admin User A Book", status=BookStatus.DRAFT, document_type=DocumentType.PDF, total_units=1)
        book_b = Book(user_id=user_b, title="Admin User B Book", status=BookStatus.READY, document_type=DocumentType.DOCX, total_units=2)
        session.add(book_a)
        session.add(book_b)
        session.commit()
        session.refresh(book_a)
        session.refresh(book_b)
        book_ids.extend([book_a.id, book_b.id])

        job = ProcessingJob(
            user_id=user_b,
            book_id=book_b.id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.READY,
            mode=PlanMode.FULL,
            progress_percent=100,
            total_units=2,
            done_units=2,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_ids.append(job.id)

    try:
        auth_as(admin_user_id)
        client = TestClient(app)

        me_response = client.get("/api/v1/admin/me")
        assert me_response.status_code == 200
        assert me_response.json()["user_id"] == str(admin_user_id)

        books_response = client.get("/api/v1/admin/books?limit=20")
        assert books_response.status_code == 200
        returned_ids = {item["id"] for item in books_response.json()["items"]}
        assert {str(book_ids[0]), str(book_ids[1])}.issubset(returned_ids)
        assert "file_url" not in books_response.json()["items"][0]

        detail_response = client.get(f"/api/v1/admin/books/{book_ids[1]}")
        assert detail_response.status_code == 200
        assert detail_response.json()["latest_job"]["id"] == str(job_ids[0])

        dashboard_response = client.get("/api/v1/admin/dashboard")
        assert dashboard_response.status_code == 200
        assert dashboard_response.json()["book_count"] >= 2
        assert dashboard_response.json()["job_count"] >= 1

        returned_user_ids = _get_all_admin_user_ids(client)
        assert {str(user_a), str(user_b)}.issubset(returned_user_ids)
    finally:
        _cleanup(admin_user_id, book_ids, job_ids, auth_user_ids=[user_a, user_b])


def test_admin_can_retry_failed_generation_job(monkeypatch, auth_as):
    calls = []

    def fake_apply_async(*, args, queue, **kwargs):
        calls.append({"args": args, "queue": queue})

    monkeypatch.setattr("app.services.admin_service.process_book_task.apply_async", fake_apply_async)

    admin_user_id = uuid.uuid4()
    user_id = uuid.uuid4()
    book_ids: list[uuid.UUID] = []
    job_ids: list[uuid.UUID] = []

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        book = Book(user_id=user_id, title="Retry Admin Book", status=BookStatus.ERROR, document_type=DocumentType.PDF, total_units=3)
        session.add(book)
        session.commit()
        session.refresh(book)
        book_ids.append(book.id)

        job = ProcessingJob(
            user_id=user_id,
            book_id=book.id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.ERROR,
            mode=PlanMode.PARETO,
            progress_percent=40,
            total_units=3,
            done_units=1,
            failed_units=1,
            error_message="LLM response invalid.",
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_ids.append(job.id)

    try:
        auth_as(admin_user_id)
        response = TestClient(app).post(f"/api/v1/admin/jobs/{job_ids[0]}/retry")

        assert response.status_code == 200
        body = response.json()
        assert body["job"]["status"] == "queued"
        assert body["job"]["progress_percent"] == 0
        assert calls == [{"args": [str(book_ids[0]), "pareto", str(job_ids[0])], "queue": "document"}]

        with Session(engine) as session:
            saved_job = session.get(ProcessingJob, job_ids[0])
            assert saved_job is not None
            assert saved_job.status == ProcessingJobStatus.QUEUED
            assert saved_job.error_message is None
            audit_log = session.exec(select(AdminAuditLog).where(AdminAuditLog.admin_user_id == admin_user_id, AdminAuditLog.action == "job.retry")).first()
            assert audit_log is not None
            assert audit_log.target_id == job_ids[0]
    finally:
        _cleanup(admin_user_id, book_ids, job_ids)


def test_admin_retry_rejects_running_job(auth_as):
    admin_user_id = uuid.uuid4()
    user_id = uuid.uuid4()
    job_ids: list[uuid.UUID] = []

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        job = ProcessingJob(
            user_id=user_id,
            book_id=None,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.PROCESSING,
            mode=PlanMode.FULL,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_ids.append(job.id)

    try:
        auth_as(admin_user_id)
        response = TestClient(app).post(f"/api/v1/admin/jobs/{job_ids[0]}/retry")

        assert response.status_code == 409
    finally:
        _cleanup(admin_user_id, [], job_ids)


def test_admin_cancel_and_rollback_job(auth_as):
    admin_user_id = uuid.uuid4()
    user_id = uuid.uuid4()
    job_ids: list[uuid.UUID] = []

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        job = ProcessingJob(
            user_id=user_id,
            book_id=None,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.PROCESSING,
            mode=PlanMode.FULL,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_ids.append(job.id)

    try:
        auth_as(admin_user_id)
        response = TestClient(app).post(f"/api/v1/admin/jobs/{job_ids[0]}/cancel")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "cancelled"

        with Session(engine) as session:
            saved_job = session.get(ProcessingJob, job_ids[0])
            assert saved_job is not None
            assert saved_job.status == ProcessingJobStatus.CANCELLED
    finally:
        _cleanup(admin_user_id, [], job_ids)

