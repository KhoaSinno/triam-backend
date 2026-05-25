from datetime import datetime, timezone

import pytest

from app.core.constant import NotificationType
from app.schemas.notification import NotificationSettingsRequest
from app.services.notification_copy_service import build_notification_copy
from app.services.reminder_schedule_service import is_quiet_time, shift_out_of_quiet_hours, to_local, weekday_is_enabled


def test_notification_copy_is_deterministic():
    title, body = build_notification_copy(NotificationType.SPACED_REVIEW_DUE, {"chapter_title": "Chương 4"})

    assert title == "Đến lúc ôn lại rồi"
    assert "Chương 4" in body


def test_quiet_hours_cross_midnight():
    local_dt = datetime(2026, 5, 24, 23, 30, tzinfo=timezone.utc)

    assert is_quiet_time(local_dt, "22:00", "07:00") is True
    assert is_quiet_time(local_dt.replace(hour=12), "22:00", "07:00") is False


def test_shift_out_of_quiet_hours_cross_midnight():
    due_at = datetime(2026, 5, 24, 16, 30, tzinfo=timezone.utc)  # 23:30 Asia/Ho_Chi_Minh

    shifted = shift_out_of_quiet_hours(due_at, "Asia/Ho_Chi_Minh", "22:00", "07:00")
    shifted_local = to_local(shifted, "Asia/Ho_Chi_Minh")

    assert shifted_local.hour == 7
    assert shifted_local.minute == 0
    assert shifted_local.date().isoformat() == "2026-05-25"


def test_weekday_config_accepts_short_english_days():
    local_dt = datetime(2026, 5, 25, 20, 0, tzinfo=timezone.utc)  # Monday

    assert weekday_is_enabled(["Mon", "Wed"], local_dt) is True
    assert weekday_is_enabled(["Tue", "Thu"], local_dt) is False


def test_notification_settings_validation_rejects_bad_time_and_timezone():
    with pytest.raises(ValueError):
        NotificationSettingsRequest(timezone="Not/AZone")

    with pytest.raises(ValueError):
        NotificationSettingsRequest(reminder_time="25:99")
