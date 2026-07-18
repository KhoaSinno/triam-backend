import re
import uuid
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constant import NotificationType

HHMM_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def _validate_hhmm(value: str) -> str:
    if not HHMM_PATTERN.match(value):
        raise ValueError("Time must use HH:MM 24-hour format.")
    return value


class NotificationSettingsRequest(BaseModel):
    timezone: str = "Asia/Ho_Chi_Minh"
    reminders_enabled: bool = True
    spaced_review_enabled: bool = True
    reminder_time: str = "20:00"
    quiet_hours_start: str = "23:00"
    quiet_hours_end: str = "06:00"
    daily_cap: int = Field(default=30, ge=0, le=30)

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Invalid IANA timezone.") from exc
        return value

    @field_validator("reminder_time", "quiet_hours_start", "quiet_hours_end")
    @classmethod
    def validate_time(cls, value: str) -> str:
        return _validate_hhmm(value)


class NotificationSettingsResponse(NotificationSettingsRequest):
    user_id: uuid.UUID


class UserNotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: NotificationType
    title: str
    body: str
    action_type: str | None = None
    action_payload: dict[str, Any] | None = None
    read_at: datetime | None = None
    created_at: datetime


class NotificationListResponse(BaseModel):
    items: list[UserNotificationResponse]
    unread_count: int


class MarkNotificationReadResponse(BaseModel):
    id: uuid.UUID
    read_at: datetime


class MarkAllNotificationsReadResponse(BaseModel):
    updated_count: int
    read_at: datetime


class DeviceTokenRegisterRequest(BaseModel):
    device_token: str = Field(..., min_length=1, description="Firebase registration token")


class DeviceTokenResponse(BaseModel):
    device_token: str
    user_id: uuid.UUID
    created_at: datetime
