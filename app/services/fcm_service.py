import json
import os
import uuid
from datetime import datetime, timezone
from hashlib import sha256

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import UserDeviceToken

_firebase_initialized = False


def _token_fingerprint(device_token: str) -> str:
    return sha256(device_token.encode("utf-8")).hexdigest()[:12]


def _stringify_fcm_data(data: dict[str, str] | None) -> dict[str, str]:
    if not data:
        return {}
    return {str(key): str(value) for key, value in data.items()}


def _delete_device_tokens(session: Session, device_tokens: list[str]) -> None:
    if not device_tokens:
        return
    db_tokens = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token.in_(device_tokens))).all()
    for token_record in db_tokens:
        session.delete(token_record)
    session.commit()
    log.info(f"Đã xóa {len(device_tokens)} token không khả dụng khỏi DB.")


def _collect_invalid_tokens(response: messaging.BatchResponse, device_tokens: list[str]) -> list[str]:
    tokens_to_delete: list[str] = []
    for idx, resp in enumerate(response.responses):
        if resp.success:
            continue

        exc = resp.exception
        token = device_tokens[idx]
        token_hash = _token_fingerprint(token)
        if isinstance(exc, (messaging.UnregisteredError, messaging.SenderIdMismatchError)):
            log.info(f"FCM token không khả dụng ({type(exc).__name__}), token_hash={token_hash}")
            tokens_to_delete.append(token)
        else:
            log.warning(f"Lỗi gửi push cho token_hash={token_hash}: {exc}")
    return tokens_to_delete


def init_firebase() -> bool:
    """
    Khởi tạo Firebase Admin SDK một cách an toàn.
    """
    global _firebase_initialized
    if _firebase_initialized or firebase_admin._apps:
        _firebase_initialized = True
        return True

    try:
        if settings.FIREBASE_CREDENTIALS_JSON:
            log.info("Khởi tạo Firebase Admin SDK từ chuỗi JSON môi trường...")
            cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
        elif settings.FIREBASE_CREDENTIALS_FILE:
            file_path = settings.FIREBASE_CREDENTIALS_FILE
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            if os.path.exists(file_path):
                log.info(f"Khởi tạo Firebase Admin SDK từ file: {file_path}")
                cred = credentials.Certificate(file_path)
                firebase_admin.initialize_app(cred)
                _firebase_initialized = True
            else:
                log.warning(f"File key Firebase không tồn tại tại: {file_path}. Push notification chạy giả lập.")
        else:
            log.warning("Firebase credentials chưa được cấu hình. Push notification chạy giả lập.")
    except Exception as e:
        log.error(f"Khởi tạo Firebase lỗi: {e}. Push notification chạy giả lập.")

    return _firebase_initialized


def send_fcm_notification(
    session: Session,
    *,
    user_id: uuid.UUID,
    title: str,
    body: str,
    data: dict[str, str] | None = None,
) -> None:
    """
    Gửi thông báo Push qua FCM đến tất cả thiết bị của user_id.
    Tự động dọn dẹp các token bị báo lỗi Unregistered/SenderIdMismatch.
    """
    device_tokens = list(session.exec(select(UserDeviceToken.device_token).where(UserDeviceToken.user_id == user_id)).all())

    if not device_tokens:
        log.debug(f"User {user_id} không có device token đăng ký. Bỏ qua gửi push.")
        return

    initialized = init_firebase()
    if not initialized:
        log.warning(f"[MOCK PUSH] Gửi đến user {user_id} ({len(device_tokens)} thiết bị) | Title: '{title}' | Body: '{body}' | Data: {data}")
        return

    log.info(f"Đang gửi push notification cho user {user_id} tới {len(device_tokens)} thiết bị...")
    string_data = _stringify_fcm_data(data)
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=string_data if string_data else None,
        tokens=list(device_tokens),
    )

    try:
        response = messaging.send_each_for_multicast(message)
        log.info(f"FCM multicast done | success={response.success_count} | failure={response.failure_count}")

        if response.failure_count > 0:
            _delete_device_tokens(session, _collect_invalid_tokens(response, device_tokens))
    except Exception as e:
        log.error(f"Gửi multicast FCM gặp lỗi hệ thống: {e}")


def register_user_device_token(session: Session, user_id: uuid.UUID, device_token: str) -> UserDeviceToken:
    """
    Đăng ký hoặc cập nhật device token cho user.
    Nếu token đã được đăng ký bởi user khác, sẽ chuyển quyền sở hữu sang user hiện tại.
    """
    existing = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token == device_token)).first()

    if existing:
        if existing.user_id == user_id:
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing
        else:
            log.info(f"Chuyển device_token từ user {existing.user_id} sang user {user_id}")
            existing.user_id = user_id
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

    try:
        new_token = UserDeviceToken(user_id=user_id, device_token=device_token)
        session.add(new_token)
        session.commit()
        session.refresh(new_token)
        return new_token
    except IntegrityError:
        session.rollback()
        # Nếu gặp lỗi UniqueViolation do luồng khác vừa commit trước đó vài mili-giây,
        # ta truy vấn lại và cập nhật sở hữu cho user hiện tại.
        existing = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token == device_token)).first()
        if existing:
            if existing.user_id != user_id:
                log.info(f"Chuyển device_token (sau khi giải quyết tranh chấp) từ user {existing.user_id} sang user {user_id}")
                existing.user_id = user_id
                existing.updated_at = datetime.now(timezone.utc)
                session.add(existing)
                session.commit()
                session.refresh(existing)
            return existing
        raise


def unregister_user_device_token(session: Session, user_id: uuid.UUID, device_token: str) -> bool:
    """
    Hủy đăng ký device token của user.
    """
    token_record = session.exec(select(UserDeviceToken).where(UserDeviceToken.user_id == user_id, UserDeviceToken.device_token == device_token)).first()

    if not token_record:
        return False

    session.delete(token_record)
    session.commit()
    return True
