import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import NotificationType
from app.db.database import engine
from app.main import app
from app.models.db_models import NotificationSettings, UserNotification

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def test_notifications_list_and_mark_read():
    notification_id = uuid.uuid4()
    with Session(engine) as session:
        session.add(
            UserNotification(
                id=notification_id,
                user_id=MOCK_USER_ID,
                type=NotificationType.CONTENT_READY,
                title="Nội dung đã sẵn sàng",
                body="Chương test đã sẵn sàng.",
                action_type="open_book",
                action_payload={"book_id": str(uuid.uuid4())},
            )
        )
        session.commit()

    try:
        client = TestClient(app)
        list_response = client.get("/api/v1/notifications?limit=10")
        assert list_response.status_code == 200
        assert list_response.json()["unread_count"] >= 1

        read_response = client.patch(f"/api/v1/notifications/{notification_id}/read")
        assert read_response.status_code == 200
        assert read_response.json()["id"] == str(notification_id)
        assert read_response.json()["read_at"] is not None
    finally:
        with Session(engine) as session:
            notification = session.get(UserNotification, notification_id)
            if notification:
                session.delete(notification)
                session.commit()


def test_notification_settings_get_update_and_restore():
    client = TestClient(app)
    with Session(engine) as session:
        before = session.get(NotificationSettings, MOCK_USER_ID)
        before_values = None
        if before:
            before_values = {
                "timezone": before.timezone,
                "reminders_enabled": before.reminders_enabled,
                "spaced_review_enabled": before.spaced_review_enabled,
                "reminder_time": before.reminder_time,
                "quiet_hours_start": before.quiet_hours_start,
                "quiet_hours_end": before.quiet_hours_end,
                "daily_cap": before.daily_cap,
            }

    try:
        get_response = client.get("/api/v1/notifications/settings")
        assert get_response.status_code == 200
        assert get_response.json()["user_id"] == str(MOCK_USER_ID)

        update_response = client.put(
            "/api/v1/notifications/settings",
            json={
                "timezone": "Asia/Ho_Chi_Minh",
                "reminders_enabled": True,
                "spaced_review_enabled": True,
                "reminder_time": "19:30",
                "quiet_hours_start": "22:00",
                "quiet_hours_end": "07:00",
                "daily_cap": 2,
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["reminder_time"] == "19:30"
        assert update_response.json()["daily_cap"] == 2
    finally:
        with Session(engine) as session:
            current = session.get(NotificationSettings, MOCK_USER_ID)
            if current and before_values:
                for key, value in before_values.items():
                    setattr(current, key, value)
                current.updated_at = datetime.now(timezone.utc)
                session.add(current)
            elif current:
                session.delete(current)
            session.commit()
