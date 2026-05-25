import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.notification import (
    MarkAllNotificationsReadResponse,
    MarkNotificationReadResponse,
    NotificationListResponse,
    NotificationSettingsRequest,
    NotificationSettingsResponse,
)
from app.services.notification_service import get_settings, list_notifications, read_all_notifications, read_notification, update_settings

router = APIRouter()

# TODO: Replace with JWT user later.
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.get("/notifications", response_model=NotificationListResponse)
def get_notifications(
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    unread_only: bool = False,
):
    return list_notifications(session, MOCK_USER_ID, limit=limit, unread_only=unread_only)


@router.patch("/notifications/read-all", response_model=MarkAllNotificationsReadResponse)
def mark_all_read(session: Annotated[Session, Depends(get_session)]):
    return read_all_notifications(session, MOCK_USER_ID)


@router.patch("/notifications/{notification_id}/read", response_model=MarkNotificationReadResponse)
def mark_notification_read(notification_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return read_notification(session, MOCK_USER_ID, notification_id)


@router.get("/notifications/settings", response_model=NotificationSettingsResponse)
def get_notification_settings(session: Annotated[Session, Depends(get_session)]):
    return get_settings(session, MOCK_USER_ID)


@router.put("/notifications/settings", response_model=NotificationSettingsResponse)
def update_notification_settings(payload: NotificationSettingsRequest, session: Annotated[Session, Depends(get_session)]):
    return update_settings(session, MOCK_USER_ID, payload)
