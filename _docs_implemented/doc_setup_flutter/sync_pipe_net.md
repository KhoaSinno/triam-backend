# Tài liệu Cơ bản về ADB cho Developer

## 1. ADB là gì?

**ADB (Android Debug Bridge)** là một công cụ dòng lệnh đa năng cho phép máy tính giao tiếp với thiết bị Android (điện thoại thật hoặc máy ảo). Nó đóng vai trò là "cây cầu" để bạn cài đặt app, gỡ lỗi (debug), và quản lý thiết bị.

ADB hoạt động theo mô hình Client - Server:

- **Client:** Máy tính bạn đang dùng (gửi lệnh).
- **Daemon (adbd):** Chạy ngầm trên điện thoại (nhận và thực thi lệnh).
- **Server:** Chạy ngầm trên máy tính để quản lý việc truyền tin giữa Client và Daemon.

---

## 2. Cách kết nối mạng (ADB Reverse)

Đây là kỹ thuật quan trọng nhất khi bạn muốn điện thoại truy cập vào Backend (API) đang chạy trên máy tính cá nhân thông qua dây cáp USB.

### Tại sao cần `adb reverse`?

Bình thường, điện thoại và máy tính nằm ở hai dải IP khác nhau. Lệnh này sẽ tạo ra một đường dẫn ngược, giúp điện thoại hiểu rằng: _"Khi tôi truy cập vào localhost của chính tôi, thực chất là tôi đang truy cập vào máy tính đang cắm dây"_.

### Các bước thực hiện:

1.  Kết nối điện thoại với máy tính qua USB (Bật **USB Debugging** trong tùy chọn nhà phát triển).
2.  Mở Backend trên máy tính (ví dụ port `8000`).
3.  Chạy lệnh trên máy tính:
    ```bash
    adb reverse tcp:8000 tcp:8000
    ```
4.  Trong code Flutter, gọi API qua địa chỉ: `http://127.0.0.1:8000`.

---

## 3. Các lệnh ADB thông dụng

### 🔹 Quản lý kết nối

| Lệnh               | Ý nghĩa                                      |
| :----------------- | :------------------------------------------- |
| `adb devices`      | Liệt kê danh sách các thiết bị đang kết nối. |
| `adb kill-server`  | Tắt server ADB (dùng khi bị treo/lag).       |
| `adb start-server` | Khởi động lại server ADB.                    |

### 🔹 Điều phối Port (Networking)

| Lệnh                            | Ý nghĩa                                                       |
| :------------------------------ | :------------------------------------------------------------ |
| `adb reverse tcp:8000 tcp:8000` | Kết nối port 8000 của điện thoại về port 8000 máy tính.       |
| `adb reverse --list`            | Xem danh sách các port đang được forward ngược.               |
| `adb reverse --remove tcp:8000` | Hủy bỏ việc chuyển hướng port 8000.                           |
| `adb forward tcp:9000 tcp:9000` | Chuyển hướng từ máy tính sang điện thoại (ngược với reverse). |

### 🔹 Gỡ lỗi và Hệ thống

| Lệnh                  | Ý nghĩa                                         |
| :-------------------- | :---------------------------------------------- |
| `adb logcat`          | Xem log hệ thống của điện thoại (rất chi tiết). |
| `adb install app.apk` | Cài đặt file APK vào điện thoại.                |
| `adb shell`           | Truy cập vào dòng lệnh Linux của điện thoại.    |

---

## 4. Lưu ý quan trọng khi sử dụng

- **Mất kết nối:** Lệnh `adb reverse` sẽ tự động mất hiệu lực khi rút cáp hoặc khởi động lại ADB. Bạn cần chạy lại lệnh khi cắm lại dây.
- **Biến môi trường:** Để gõ được lệnh `adb` ở bất cứ đâu, bạn phải thêm đường dẫn tới thư mục `platform-tools` vào **Environment Variables (Path)** của Windows như chúng ta đã làm.
- **Quyền xác thực:** Khi cắm điện thoại mới vào, hãy luôn để ý màn hình điện thoại để nhấn **"Allow USB Debugging"**.

---

## 5. Mẹo tự động hóa cho Flutter

Để không phải gõ lại lệnh mỗi lần cắm máy, bạn có thể tạo một file `run_backend.bat` (Windows) để vừa bật Backend vừa chạy lệnh ADB:

```batch
@echo off
adb reverse tcp:8000 tcp:8000
echo "ADB Reverse 8000 xong!"
# Lệnh chạy backend của bạn ở đây, ví dụ:
# python manage.py runserver 0.0.0.0:8000
```

Tài liệu này hy vọng giúp bạn làm chủ được công cụ ADB để việc code Flutter trở nên mượt mà hơn! Bạn có muốn mình giải thích thêm về lệnh nào khác trong đống này không?
