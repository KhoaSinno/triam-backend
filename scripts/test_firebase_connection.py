import argparse
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(override=True)

from firebase_admin import messaging  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.services.fcm_service import init_firebase  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra kết nối Firebase và gửi test push notification.")
    parser.add_argument("--token", type=str, help="FCM Registration Token từ thiết bị di động (Flutter) để test gửi push thực tế.")
    args = parser.parse_args()

    print("=" * 60)
    print("      KIỂM TRA KẾT NỐI FIREBASE CLOUD MESSAGING (FCM)")
    print("=" * 60)

    print(f"[*] Cấu hình File: {settings.FIREBASE_CREDENTIALS_FILE}")
    print(f"[*] Cấu hình JSON (Hugging Face): {'Đã cấu hình' if settings.FIREBASE_CREDENTIALS_JSON else 'Chưa cấu hình (Chạy chế độ local)'}")

    success = init_firebase()
    if not success:
        print("[!] KHÔNG THỂ KHỞI TẠO FIREBASE SDK. Vui lòng kiểm tra lại đường dẫn file key hoặc chuỗi JSON trong .env.")
        sys.exit(1)

    print("[+] Khởi tạo Firebase Admin SDK thành công!")

    if args.token:
        print(f"\n[*] Đang gửi push notification thực tế tới token: {args.token[:20]}...")
        message = messaging.Message(
            notification=messaging.Notification(
                title="TRIAM Push Test",
                body="Xin chào! Thông báo push từ backend của bạn đã hoạt động thực tế thành công! 🎉",
            ),
            data={
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "test_key": "test_value",
            },
            token=args.token,
        )
        try:
            response = messaging.send(message)
            print(f"[+] Gửi thành công! Message ID: {response}")
            print("[+] Hãy kiểm tra điện thoại của bạn xem có nhận được thông báo không.")
        except Exception as e:
            print(f"[!] Gửi push thất bại: {e}")
    else:
        print("\n[*] Bạn chưa truyền token thiết bị di động (--token).")
        print("[*] Hệ thống sẽ thực hiện gửi thử nghiệm (dry-run) để kiểm tra xác thực với máy chủ Firebase...")

        dummy_token = "f3v8-G7STdK...dummy-format-only-not-real-token"
        message = messaging.Message(
            notification=messaging.Notification(
                title="Dry-run Test",
                body="Test",
            ),
            token=dummy_token,
        )
        try:
            messaging.send(message, dry_run=True)
            print("[+] Dry-run kết nối thành công!")
        except Exception as e:
            error_str = str(e)
            token_validation_error = (
                "Requested entity was not found" in error_str
                or "unregistered" in error_str.lower()
                or "invalid" in error_str.lower()
                or "valid" in error_str.lower()
                or "SenderIdMismatch" in error_str
            )
            if token_validation_error:
                print("[+] KẾT NỐI & XÁC THỰC VỚI FIREBASE THÀNH CÔNG! (Tài khoản Google Service Account hợp lệ)")
                print("[!] Lưu ý: Để nhận được thông báo trên điện thoại di động thực tế, bạn cần truyền đúng token của thiết bị bằng tham số:")
                print("    python scripts/test_firebase_connection.py --token <YOUR_DEVICE_TOKEN>")
            else:
                print(f"[!] Lỗi xác thực hoặc lỗi kết nối mạng với Firebase: {e}")


if __name__ == "__main__":
    main()
