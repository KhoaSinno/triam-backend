import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlmodel import Session, select

from app.core.constant import LearningProgressStatus, NotificationStatus, NotificationType, PlanMode, ReviewItemStatus
from app.db.database import engine
from app.main import app
from app.models.db_models import (
    AdminAuditLog,
    AdminUser,
    Book,
    LearningUnit,
    LearningUnitProgress,
    NotificationOutbox,
    ReadingPlan,
    ReadingPlanSession,
    SpacedReviewItem,
)
from app.repositories.admin_repo import auth_users


def _seed_auth_user(session: Session, user_id: uuid.UUID, *, name: str) -> None:
    session.execute(
        auth_users.insert().values(
            id=user_id,
            email=f"{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}@triam.local",
            created_at=datetime.now(timezone.utc),
            raw_user_meta_data={"name": name},
        )
    )


def _cleanup_user_management_fixture(admin_user_id: uuid.UUID, target_user_id: uuid.UUID) -> None:
    with Session(engine) as session:
        session.execute(delete(AdminAuditLog).where(AdminAuditLog.admin_user_id == admin_user_id))
        session.execute(delete(NotificationOutbox).where(NotificationOutbox.user_id == target_user_id))
        session.execute(delete(SpacedReviewItem).where(SpacedReviewItem.user_id == target_user_id))
        session.execute(delete(LearningUnitProgress).where(LearningUnitProgress.user_id == target_user_id))
        session.execute(delete(ReadingPlanSession).where(ReadingPlanSession.user_id == target_user_id))
        session.execute(delete(ReadingPlan).where(ReadingPlan.book_id.in_(select(Book.id).where(Book.user_id == target_user_id))))
        session.execute(delete(LearningUnit).where(LearningUnit.user_id == target_user_id))
        session.execute(delete(Book).where(Book.user_id == target_user_id))
        session.execute(auth_users.delete().where(auth_users.c.id == target_user_id))
        admin_user = session.get(AdminUser, admin_user_id)
        if admin_user:
            session.delete(admin_user)
        session.commit()


def test_admin_user_status_uses_supabase_update_api(monkeypatch, auth_as):
    admin_user_id = uuid.uuid4()
    target_user_id = uuid.uuid4()
    calls: list[tuple[str, dict[str, str]]] = []

    def fake_update_user_by_id(user_id: str, attributes: dict[str, str]):
        calls.append((user_id, attributes))

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        _seed_auth_user(session, target_user_id, name="Status Target")
        session.commit()

    monkeypatch.setattr("app.core.supabase.supabase.auth.admin.update_user_by_id", fake_update_user_by_id)
    try:
        auth_as(admin_user_id)
        client = TestClient(app)

        ban_response = client.patch(
            f"/api/v1/admin/users/{target_user_id}/status",
            json={"is_active": False, "ban_reason": "Kiểm thử"},
        )
        assert ban_response.status_code == 200
        assert ban_response.json()["is_active"] is False
        assert calls == [(str(target_user_id), {"ban_duration": "876000h"})]

        unban_response = client.patch(
            f"/api/v1/admin/users/{target_user_id}/status",
            json={"is_active": True},
        )
        assert unban_response.status_code == 200
        assert calls[-1] == (str(target_user_id), {"ban_duration": "none"})

        self_ban_response = client.patch(
            f"/api/v1/admin/users/{admin_user_id}/status",
            json={"is_active": False},
        )
        assert self_ban_response.status_code == 400
    finally:
        _cleanup_user_management_fixture(admin_user_id, target_user_id)


def test_admin_notification_is_queued_once(auth_as):
    admin_user_id = uuid.uuid4()
    target_user_id = uuid.uuid4()
    request_body = {
        "title": "Thông báo kiểm thử",
        "body": "Nội dung kiểm thử từ quản trị viên.",
        "idempotency_key": str(uuid.uuid4()),
    }

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        _seed_auth_user(session, target_user_id, name="Notification Target")
        session.commit()

    try:
        auth_as(admin_user_id)
        client = TestClient(app)
        first_response = client.post(f"/api/v1/admin/users/{target_user_id}/notify", json=request_body)
        assert first_response.status_code == 200
        first_body = first_response.json()
        assert first_body["status"] == NotificationStatus.PENDING.value

        duplicate_response = client.post(f"/api/v1/admin/users/{target_user_id}/notify", json=request_body)
        assert duplicate_response.status_code == 200
        assert duplicate_response.json()["outbox_id"] == first_body["outbox_id"]

        with Session(engine) as session:
            outbox = session.get(NotificationOutbox, uuid.UUID(first_body["outbox_id"]))
            assert outbox is not None
            assert outbox.type == NotificationType.ADMIN_ANNOUNCEMENT
            assert outbox.payload["title"] == request_body["title"]
            assert outbox.payload["body"] == request_body["body"]
            audit_log = session.exec(
                select(AdminAuditLog).where(
                    AdminAuditLog.admin_user_id == admin_user_id,
                    AdminAuditLog.action == "user.send_notification",
                )
            ).first()
            assert audit_log is not None
    finally:
        _cleanup_user_management_fixture(admin_user_id, target_user_id)


def test_admin_user_stats_uses_learning_progress_data(auth_as):
    admin_user_id = uuid.uuid4()
    target_user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        session.add(AdminUser(user_id=admin_user_id, role="admin"))
        _seed_auth_user(session, target_user_id, name="Analytics Target")
        book = Book(user_id=target_user_id, title="Analytics book")
        session.add(book)
        session.commit()
        session.refresh(book)

        unit = LearningUnit(
            user_id=target_user_id,
            book_id=book.id,
            mode=PlanMode.FULL,
            unit_index=0,
            title="Bài học 1",
            unit_type="chapter",
            estimated_audio_seconds=999_999,
        )
        session.add(unit)
        session.commit()
        session.refresh(unit)

        session.add(
            LearningUnitProgress(
                user_id=target_user_id,
                book_id=book.id,
                learning_unit_id=unit.id,
                mode=PlanMode.FULL,
                listened_ms=7_200_000,
                status=LearningProgressStatus.COMPLETED,
                last_activity_at=now,
            )
        )
        plan = ReadingPlan(book_id=book.id, mode=PlanMode.FULL, pace=1, status="active")
        session.add(plan)
        session.commit()
        session.refresh(plan)
        session.add(
            ReadingPlanSession(
                user_id=target_user_id,
                plan_id=plan.id,
                book_id=book.id,
                mode=PlanMode.FULL,
                session_index=1,
                scheduled_at=now,
                local_date=now.date().isoformat(),
                reminder_time="20:00",
                status="completed",
            )
        )
        session.add(
            SpacedReviewItem(
                user_id=target_user_id,
                book_id=book.id,
                learning_unit_id=unit.id,
                mode=PlanMode.FULL,
                interval_days=1,
                sequence_index=0,
                due_at=now,
                status=ReviewItemStatus.COMPLETED,
            )
        )
        session.commit()

    try:
        auth_as(admin_user_id)
        response = TestClient(app).get(f"/api/v1/admin/users/{target_user_id}/stats")
        assert response.status_code == 200
        body = response.json()
        assert body["total_listened_ms"] == 7_200_000
        assert body["total_hours_listened"] == 2.0
        assert body["total_units_completed"] == 1
        assert body["total_sessions_completed"] == 1
        assert body["total_reviews_completed"] == 1
        assert body["books_owned_count"] == 1
        assert body["last_active_at"] is not None
    finally:
        _cleanup_user_management_fixture(admin_user_id, target_user_id)
