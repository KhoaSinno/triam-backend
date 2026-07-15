# Flutter Phase 23 Contract - Reset Reading Plan API

Date: 2026-07-15  
Status: **Backend implemented, FE migration guide**  
Backend phase: `_docs_implemented/phase_23_reset_reading_plan_implementation_guide.md`  

---

## 1. Mục Tiêu Nghiệp Vụ Của Frontend (FE)

Trong các phase trước, hệ thống đã cung cấp tính năng lập lịch học tuần (`ReadingPlan`) và theo dõi tiến độ chi tiết. Tuy nhiên, khi một cuốn sách đã học xong hoàn toàn (hoặc người dùng muốn học lại từ đầu cuốn sách ở chế độ hiện tại), chúng ta cần một cơ chế **Đặt lại kế hoạch (Reset Plan)** để xóa sạch tiến trình học cũ và tạo một lịch học hoàn toàn mới bắt đầu từ Bài học thứ nhất.

Backend đã hiện thực hóa API `POST /api/v1/books/{book_id}/reset`. Tài liệu này đặc tả cách Frontend tích hợp API này vào giao diện ứng dụng Flutter.

---

## 2. Đặc Tả API Reset Plan

### **POST /api/v1/books/{book_id}/reset**
*   **Mô tả:** Đặt lại toàn bộ tiến độ học tập chi tiết, xóa các thẻ ôn tập ngắt quãng (Spaced Repetition), hủy các thông báo nhắc nhở cũ còn tồn đọng trong outbox, đồng thời xếp lại lịch mới bắt đầu từ Bài học số 1.
*   **Headers:** `Authorization: Bearer <token>`
*   **Path Parameter:**
    *   `book_id` (String - UUID): ID của cuốn sách cần reset kế hoạch học tập.

### **Response Dữ Liệu Trả Về (Success 200 OK)**

API trả về thông tin `ReadingPlanResponse` (kế hoạch học tập sau khi được cập nhật) kèm thông điệp thông báo:

```json
{
  "message": "Đã đặt lại kế hoạch học tập từ đầu thành công.",
  "plan_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
  "book_id": "f3bd6986-7e99-4462-8fbe-56f973a7de22",
  "mode": "pareto",
  "pace": 1,
  "schedule_config": ["T2", "T4", "T6"],
  "reminder_time": "19:00",
  "status": "active",
  "plan_status": "active",
  "active_slots": [
    {
      "id": "e5f6a1b2-c3d4-7a8b-9c0d-1e2f3a4b5c6d",
      "weekday": 1,
      "weekday_label": "Thứ 2",
      "reminder_time": "19:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "is_active": true
    }
  ],
  "created_at": "2026-07-15T10:00:00Z",
  "updated_at": "2026-07-15T11:00:00.123456Z"
}
```

---

## 3. Các Bước Tích Hợp Lên UI/UX Flutter

Frontend cần thực hiện các công việc sau để tích hợp nút **Bắt đầu vòng học mới (Reset Plan)**:

### 3.1 Vị Trí Đặt Nút trên UI
Đặt một nút bấm có nhãn là **"Học lại từ đầu"** hoặc **"Bắt đầu vòng học mới"** (Reset Plan) ở các vị trí phù hợp:
1.  **Màn hình Chi tiết Sách (Book Detail Screen):** Khi trạng thái học của sách là `completed` hoặc `in_progress`.
2.  **Màn hình Cấu hình Lập Lịch (Reading Plan Configuration/Settings):** Bên cạnh các nút tạm dừng, sửa lịch.

### 3.2 Hộp Thoại Xác Nhận (Confirmation Dialog)
Vì hành động Reset sẽ **xóa vĩnh viễn** toàn bộ tiến trình học tập cũ của sách (ở mode hiện tại) và không thể hoàn tác, FE **bắt buộc** phải hiển thị một Dialog cảnh báo trước khi gửi request:

> ⚠️ **Cảnh báo hiển thị trên Dialog:**
> *"Hành động này sẽ xóa toàn bộ lịch sử và tiến độ học tập hiện tại của cuốn sách này ở chế độ đang chọn để bắt đầu lại từ đầu. Bạn có chắc chắn muốn tiếp tục không?"*

### 3.3 Quy Trình Xử Lý State Sau Khi Gọi API Thành Công
Khi nhận được HTTP Status `200` từ API `/api/v1/books/{book_id}/reset`, Flutter Client cần thực hiện cập nhật các Provider/Bloc State sau:

1.  **Cập nhật Tiến độ Sách (Book Progress State):**
    *   Cập nhật phần trăm tiến độ học tập (`book_progress_percent`) của sách về `0%`.
    *   Cập nhật trạng thái tiến độ học (`learning_status`/`status`) về `not_started`.
2.  **Làm mới Lịch học (Refresh Calendar View):**
    *   Gọi lại API danh sách buổi học tuần `GET /api/v1/reading-plan/sessions` để lấy danh sách các buổi học (`sessions`) mới sinh bắt đầu từ bài số 1.
    *   Cập nhật lại lịch hiển thị (Calendar View/Agenda List) của người dùng để tránh hiển thị các buổi học cũ đã bị backend xóa.
3.  **Thông báo thành công (Success Toast/Snackbar):**
    *   Hiển thị thông điệp từ backend: *"Đã đặt lại kế hoạch học tập từ đầu thành công."*

---

## 4. Đặc Tả Model Dart/Flutter

Nếu dự án của bạn đã có lớp `ReadingPlan` từ Phase 12, bạn chỉ cần sử dụng lớp đó. Dưới đây là tham khảo đặc tả Model Dart để map dữ liệu trả về từ API Reset:

```dart
class ReadingPlanResponse {
  final String message;
  final String planId;
  final String bookId;
  final String mode; // 'full' or 'pareto'
  final int pace;
  final List<String> scheduleConfig;
  final String reminderTime;
  final String status;
  final List<ScheduleSlot> activeSlots;
  final DateTime createdAt;
  final DateTime updatedAt;

  ReadingPlanResponse({
    required this.message,
    required this.planId,
    required this.bookId,
    required this.mode,
    required this.pace,
    required this.scheduleConfig,
    required this.reminderTime,
    required this.status,
    required this.activeSlots,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ReadingPlanResponse.fromJson(Map<String, dynamic> json) {
    return ReadingPlanResponse(
      message: json['message'] as String,
      planId: json['plan_id'] as String,
      bookId: json['book_id'] as String,
      mode: json['mode'] as String,
      pace: json['pace'] as int,
      scheduleConfig: List<String>.from(json['schedule_config'] as List),
      reminderTime: json['reminder_time'] as String,
      status: json['status'] as String,
      activeSlots: (json['active_slots'] as List)
          .map((e) => ScheduleSlot.fromJson(e as Map<String, dynamic>))
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}

class ScheduleSlot {
  final String id;
  final int weekday;
  final String weekdayLabel;
  final String reminderTime;
  final String timezone;
  final bool isActive;

  ScheduleSlot({
    required this.id,
    required this.weekday,
    required this.weekdayLabel,
    required this.reminderTime,
    required this.timezone,
    required this.isActive,
  });

  factory ScheduleSlot.fromJson(Map<String, dynamic> json) {
    return ScheduleSlot(
      id: json['id'] as String,
      weekday: json['weekday'] as int,
      weekdayLabel: json['weekday_label'] as String,
      reminderTime: json['reminder_time'] as String,
      timezone: json['timezone'] as String,
      isActive: json['is_active'] as bool,
    );
  }
}
```
