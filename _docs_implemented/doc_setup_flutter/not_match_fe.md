Tôi đã hoàn tất việc rà soát chéo giữa **Tài liệu hướng dẫn API** và **mã nguồn UI thực tế của Frontend (FE) Mobile App** tại `C:\triam-frontend`.

Ngoài tính năng cài đặt thông báo (Notifications Settings) đã báo cáo ở lượt trước, tôi đã phát hiện thêm **3 điểm lệch pha/chưa tích hợp** khác giữa Frontend UI và Backend API.

Dưới đây là báo cáo tổng hợp chi tiết các API chưa được nối lên giao diện hoặc bị lỗi tương tự để bạn nắm được:

---

## 📊 BẢNG TỔNG HỢP CÁC API BỊ LỆCH PHA GIỮA UI & BACKEND

| STT   | API Endpoint (Backend)                              | Tình trạng tích hợp trên FE UI                               | Vị trí file mã nguồn FE tương ứng                                                                                          | Mô tả & Hệ quả                                                                                                                                                                                                                                                                               |
| ----- | --------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | `GET /api/v1/books/{book_id}/content`               | 🔴 **LỖI LỆCH PHA NGHIÊM TRỌNG** (UI gọi nhưng BE thiếu)     | [text_reading_page.dart](file:///C:/triam-frontend/lib/shared/viewer/text_reading_page.dart#L78)                           | Màn hình đọc sách dạng chữ gọi API này để lấy danh sách chương và nội dung text thô. Nhưng Backend chưa định nghĩa route này, mở màn hình đọc sách sẽ bị crash/trắng màn hình.                                                                                                               |
| **2** | `PUT /api/v1/notifications/settings`                | 🟡 **CÓ CODE LOGIC - THIẾU UI** (Chưa nối lên màn hình)      | [notification_repository.dart](file:///C:/triam-frontend/lib/features/notification/data/notification_repository.dart#L288) | Repository đã viết code gọi API cấu hình thông báo (Reminders, Quiet Hours), nhưng trên màn hình `profile_page.dart` hay `notification_page.dart` đều chưa vẽ nút/form để bấm lưu cấu hình này.                                                                                              |
| **3** | `POST /api/v1/agent/chat`                           | 🟡 **CÓ CODE LOGIC - THIẾU UI** (Chưa có màn hình chat HTTP) | [agent_repository.dart](file:///C:/triam-frontend/lib/features/agent/data/agent_repository.dart#L164)                      | Tầng Data đã viết hàm `sendTextViaHttp`, nhưng giao diện Voice Agent (`agent_page.dart` và `agent_conversation_view.dart`) chỉ có Microphone đàm thoại realtime và kênh truyền data của LiveKit, không có ô nhập liệu (TextField) để chat chữ qua HTTP.                                      |
| **4** | `GET /api/v1/books/{book_id}/reading-plan/sessions` | 🟡 **CÓ CODE LOGIC - THIẾU UI** (Chưa tích hợp UI chi tiết)  | [remote_book_repository.dart](file:///C:/triam-frontend/lib/shared/book/data/remote_book_repository.dart#L648)             | Có định nghĩa hàm `getBookReadingPlanSessions` để xem lộ trình học của riêng 1 cuốn sách. Tuy nhiên UI lịch học hiện tại chỉ dùng Calendar tổng (`getCalendarReadingPlanSessions`) hoặc bài học hôm nay (`getTodayReadingPlanSessions`), chưa vẽ màn hình lộ trình chi tiết riêng từng sách. |

---

## 🛠️ ĐỀ XUẤT HƯỚNG XỬ LÝ CHO BẠN:

### 1. Sửa lỗi đọc sách (Sự cố số 1)

Bạn cần bổ sung thêm router `GET /api/v1/books/{book_id}/content` ở file Backend [audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py) để trả về nội dung của các `BookSection` có `parent_id` (hoặc các sections cấp thấp hơn) nhằm cung cấp text cho Mobile App đọc chữ.

### 2. Thiết kế thêm UI Cấu hình Thông báo (Sự cố số 2)

Nối hàm `updateSettings` của `notificationRepository` vào màn hình [profile_page.dart](file:///C:/triam-frontend/lib/features/profile/presentation/pages/profile_page.dart). Ta có thể vẽ thêm một mục con dạng `expandedContent` bên dưới mục **Chế độ tối/Giọng đọc** để người dùng tuỳ chọn giờ giấc nhắc nhở và bật/tắt giờ yên lặng.

### 3. Đối với API Chat HTTP & Lịch học riêng cuốn sách (Sự cố số 3 & 4)

- **Chat HTTP (`/agent/chat`)**: Có thể giữ nguyên không cần xử lý UI vì app hiện tại tập trung hoàn toàn vào đàm thoại giọng nói Realtime (LiveKit), việc chat chữ HTTP có thể là tính năng dự phòng.
- **Lộ trình riêng của sách**: Hiện tại Calendar tổng hợp đã rất đầy đủ. Việc hiển thị lộ trình chi tiết riêng của từng cuốn sách có thể bổ sung sau khi nâng cấp UI ở các phase tiếp theo.

Bạn có cần tôi hỗ trợ viết code để xử lý phần **API Content** ở Backend, hoặc viết code bổ sung UI cho màn hình **Cấu hình Thông báo / Đọc sách** trên Flutter không?
