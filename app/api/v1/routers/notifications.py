import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.notification import (
    DeviceTokenRegisterRequest,
    DeviceTokenResponse,
    MarkAllNotificationsReadResponse,
    MarkNotificationReadResponse,
    NotificationListResponse,
    NotificationSettingsRequest,
    NotificationSettingsResponse,
)
from app.services.fcm_service import register_user_device_token, unregister_user_device_token
from app.services.notification_service import get_settings, list_notifications, read_all_notifications, read_notification, update_settings
from app.services.sync_event_service import record_event

router = APIRouter()


@router.get("/notifications", response_model=NotificationListResponse)
def get_notifications(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    unread_only: bool = False,
):
    return list_notifications(session, current_user.sub, limit=limit, unread_only=unread_only)


@router.patch("/notifications/read-all", response_model=MarkAllNotificationsReadResponse)
def mark_all_read(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    response = read_all_notifications(session, current_user.sub)
    record_event(session, user_id=current_user.sub, domain="notification", entity_id="all", operation="update")
    session.commit()
    return response


@router.patch("/notifications/{notification_id}/read", response_model=MarkNotificationReadResponse)
def mark_notification_read(notification_id: uuid.UUID, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    response = read_notification(session, current_user.sub, notification_id)
    record_event(session, user_id=current_user.sub, domain="notification", entity_id=notification_id, operation="update")
    session.commit()
    return response


@router.get("/notifications/settings", response_model=NotificationSettingsResponse)
def get_notification_settings(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    return get_settings(session, current_user.sub)


@router.put("/notifications/settings", response_model=NotificationSettingsResponse)
def update_notification_settings(payload: NotificationSettingsRequest, current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    response = update_settings(session, current_user.sub, payload)
    record_event(session, user_id=current_user.sub, domain="notification_settings", entity_id="settings", operation="update")
    session.commit()
    return response


@router.post("/notifications/devices", response_model=DeviceTokenResponse, status_code=201)
def register_device(
    payload: DeviceTokenRegisterRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    return register_user_device_token(session, current_user.sub, payload.device_token)


@router.delete("/notifications/devices/{device_token}")
def unregister_device(
    device_token: str,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    success = unregister_user_device_token(session, current_user.sub, device_token)
    return {"status": "success" if success else "not_found"}
