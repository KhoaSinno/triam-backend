# Hướng Dẫn Tích Hợp FCM Push Notification Cho Frontend (Flutter)

Tài liệu này hướng dẫn nhà phát triển Frontend (Flutter) cấu hình Firebase và tích hợp các API đăng ký/hủy đăng ký thiết bị di động để nhận thông báo đẩy từ backend.

---

# google-services.json

```json
{
  "project_info": {
    "project_number": "1041946558007",
    "project_id": "triam-notification",
    "storage_bucket": "triam-notification.firebasestorage.app"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:1041946558007:android:de05b8b2271979dc0f49b2",
        "android_client_info": {
          "package_name": "com.capstone.triam"
        }
      },
      "oauth_client": [],
      "api_key": [
        {
          "current_key": "AIzaSyB3b5_47RRNYQGN0JquPX2vdD3blV-fpYc"
        }
      ],
      "services": {
        "appinvite_service": {
          "other_platform_oauth_client": []
        }
      }
    }
  ],
  "configuration_version": "1"
}
```

---

## 1. Những Thứ Bạn (Product Owner/Tech Lead) Cần Cung Cấp Cho Frontend

Để lập trình viên FE có thể làm việc, bạn cần gửi cho họ các thông tin sau:

1. **File cấu hình Firebase Client:**
   - **Android:** File `google-services.json` (tải từ trang quản trị Firebase Console thuộc Project của dự án).
   - **iOS:** File `GoogleService-Info.plist` (tải từ trang quản trị Firebase Console).
2. **URL các API Endpoint:**
   - API Đăng ký Token: `POST /api/v1/notifications/devices`
   - API Hủy Đăng ký Token: `DELETE /api/v1/notifications/devices/{device_token}`

---

## 2. Các Bước Lập Trình Viên Frontend Cần Thực Hiện

### Bước 2.1: Cấu hình Firebase SDK trên Flutter

Thêm các thư viện Firebase cần thiết vào file `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  firebase_core: ^3.0.0 # Hoặc phiên bản mới nhất
  firebase_messaging: ^15.0.0 # Hoặc phiên bản mới nhất
```

- **Android:** Đặt file `google-services.json` vào thư mục `android/app/`. Cập nhật các file `build.gradle` theo hướng dẫn chuẩn của Firebase.
- **iOS:** Đặt file `GoogleService-Info.plist` vào thư mục Xcode Runner và cấu hình APNs Certificates/Keys trên trang Apple Developer để kết nối APNs với Firebase.

---

### Bước 2.2: Lấy FCM Registration Token

Khi ứng dụng khởi tạo (thường ở hàm `main` hoặc màn hình khởi động), thực hiện lấy Token định danh thiết bị:

```dart
import 'package:firebase_messaging/firebase_messaging.dart';

Future<String?> getDeviceToken() async {
  FirebaseMessaging messaging = FirebaseMessaging.instance;

  // 1. Yêu cầu quyền thông báo (bắt buộc trên iOS và Android 13+)
  NotificationSettings settings = await messaging.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );

  if (settings.authorizationStatus == AuthorizationStatus.authorized) {
    // 2. Lấy FCM Token
    String? token = await messaging.getToken();
    print("FCM Token: $token");
    return token;
  } else {
    print("Người dùng từ chối cấp quyền thông báo.");
    return null;
  }
}
```

---

### Bước 2.3: Đăng ký Token với Backend (API Integration)

FE cần gọi API gửi Token lên backend trong **3 trường hợp**:

1. **Ngay sau khi đăng nhập thành công** vào hệ thống.
2. **Khi mở app (App Launch)** nếu người dùng đã có phiên đăng nhập từ trước.
3. **Khi Token thay đổi** (Lắng nghe qua Stream `onTokenRefresh` của Firebase).

#### API Đăng ký:

- **Method:** `POST`
- **Path:** `/api/v1/notifications/devices`
- **Headers:**
  - `Authorization: Bearer <SUPABASE_JWT_TOKEN>`
  - `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "device_token": "chuỗi_fcm_token_lấy_ở_bước_2.2"
  }
  ```

#### Code gợi ý lắng nghe Token thay đổi:

```dart
FirebaseMessaging.instance.onTokenRefresh.listen((newToken) {
  // Gọi API POST /api/v1/notifications/devices để cập nhật Token mới lên Backend
  apiService.registerDeviceToken(newToken);
});
```

---

### Bước 2.4: Hủy đăng ký Token khi Đăng xuất (Logout)

Để tránh trường hợp người dùng đã đăng xuất nhưng điện thoại vẫn nhận được thông báo của tài khoản cũ, FE **bắt buộc** phải gọi API hủy đăng ký thiết bị trước khi xóa token cục bộ và chuyển màn hình về trang đăng nhập.

#### API Hủy Đăng ký:

- **Method:** `DELETE`
- **Path:** `/api/v1/notifications/devices/{device_token}` (Truyền token cần hủy vào URL path)
- **Headers:**
  - `Authorization: Bearer <SUPABASE_JWT_TOKEN>`

---

## 3. Định Dạng Dữ Liệu Thông Báo (FCM Payload)

Khi Backend gửi push notification, nó sẽ tự động gửi kèm các dữ liệu Custom Metadata để FE điều hướng màn hình khi người dùng nhấn vào thông báo.

### Cấu trúc Data Payload Backend gửi sang:

Các dữ liệu nằm trong thẻ `data` của Firebase Message. **Lưu ý: Tất cả các giá trị trong thẻ data đều là kiểu chuỗi (String).**

```json
{
  "outbox_id": "uuid_của_tin_nhắn",
  "notification_type": "spaced_review_due", // hoặc plan_reminder, content_ready
  "action_type": "open_learning_unit", // hoặc open_book, open_review
  "action_payload": "{\"book_id\":\"63339d85...\",\"learning_unit_id\":\"...\",\"mode\":\"full\"}" // Chuỗi JSON String, cần JSON.decode() để đọc
}
```

### Hướng Dẫn Điều Hướng (Deep Linking) cho FE:

FE cần đọc trường `action_type` để quyết định điều hướng màn hình:

1.  **Nếu `action_type == "open_book"`**:
    - Parse `action_payload` lấy `book_id` và `mode`.
    - Mở màn hình chi tiết cuốn sách tương ứng.
2.  **Nếu `action_type == "open_learning_unit"`**:
    - Parse `action_payload` lấy `book_id`, `learning_unit_id` và `mode`.
    - Mở trình phát audiobook học tập và phát ngay bài học đó.
3.  **Nếu `action_type == "open_review"`**:
    - Parse `action_payload` lấy `book_id`, `review_item_id`, `learning_unit_id` và `mode`.
    - Mở màn hình ôn tập (spaced review) cho người dùng.

---

## 4. Xử Lý Khi Nhận Thông Báo

- **Khi App đang chạy nền hoặc tắt hoàn toàn (Background/Terminated):** Điện thoại sẽ tự động hiển thị Banner thông báo mặc định của hệ điều hành. Khi nhấn vào Banner, app sẽ mở ra và Flutter sẽ nhận được thông tin payload thông qua `FirebaseMessaging.instance.getInitialMessage()` hoặc `FirebaseMessaging.onMessageOpenedApp`.
- **Khi App đang mở (Foreground):** Mặc định điện thoại sẽ không hiện banner. FE cần lắng nghe stream `FirebaseMessaging.onMessage.listen((RemoteMessage message) { ... })` để hiển thị một Banner tùy chỉnh ngay trong app hoặc cập nhật UI thông báo.
