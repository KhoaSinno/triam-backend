import os
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import firebase_admin
from firebase_admin import credentials, messaging
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import UserDeviceToken

_firebase_initialized = False


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
    data: Optional[dict[str, str]] = None,
) -> None:
    """
    Gửi thông báo Push qua FCM đến tất cả thiết bị của user_id.
    Tự động dọn dẹp các token bị báo lỗi Unregistered/SenderIdMismatch.
    """
    # 1. Truy vấn toàn bộ token của người dùng
    device_tokens = session.exec(select(UserDeviceToken.device_token).where(UserDeviceToken.user_id == user_id)).all()

    if not device_tokens:
        log.debug(f"User {user_id} không có device token đăng ký. Bỏ qua gửi push.")
        return

    # 2. Đảm bảo Firebase được khởi tạo
    initialized = init_firebase()
    if not initialized:
        log.warning(f"[MOCK PUSH] Gửi đến user {user_id} ({len(device_tokens)} thiết bị) | Title: '{title}' | Body: '{body}' | Data: {data}")
        return

    # 3. Chuẩn bị gửi multicast
    log.info(f"Đang gửi push notification cho user {user_id} tới {len(device_tokens)} thiết bị...")

    # Ép kiểu dữ liệu data thành string (FCM yêu cầu các giá trị data phải là string)
    string_data = {}
    if data:
        for k, v in data.items():
            string_data[str(k)] = str(v)

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

        # 4. Kiểm tra lỗi và tự động xóa token hỏng
        if response.failure_count > 0:
            tokens_to_delete = []
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    exc = resp.exception
                    # UnregisteredError và SenderIdMismatchError là các lỗi token không còn khả dụng
                    if isinstance(exc, (messaging.UnregisteredError, messaging.SenderIdMismatchError)):
                        bad_token = device_tokens[idx]
                        log.info(f"FCM token không khả dụng ({type(exc).__name__}), chuẩn bị xóa: {bad_token}")
                        tokens_to_delete.append(bad_token)
                    else:
                        log.warning(f"Lỗi gửi push cho token {device_tokens[idx]}: {exc}")

            if tokens_to_delete:
                # Xóa các token lỗi khỏi cơ sở dữ liệu
                db_tokens = session.exec(select(UserDeviceToken).where(UserDeviceToken.device_token.in_(tokens_to_delete))).all()
                for t in db_tokens:
                    session.delete(t)
                session.commit()
                log.info(f"Đã xóa {len(tokens_to_delete)} token không khả dụng khỏi DB.")
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

    new_token = UserDeviceToken(user_id=user_id, device_token=device_token)
    session.add(new_token)
    session.commit()
    session.refresh(new_token)
    return new_token


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
