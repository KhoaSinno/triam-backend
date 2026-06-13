# Flutter Phase 13 Contract - Calendar Session Actions And Missed Reminders

Date: 2026-06-12  
Status: **Backend implemented, FE migration guide**  
Backend phase: `_docs_implemented/phase_13_calendar_session_actions_and_learning_rounds_implementation_guide.md`  
Related FE docs:

- `_docs_implemented/doc_setup_flutter/flutter_phase_11_learning_progress_completion_contract.md`
- `_docs_implemented/doc_setup_flutter/flutter_phase_12_calendar_reading_plan_contract.md`

---

## 1. Mục Tiêu FE Cần Sửa

Phase 11 trả lời:

```text
User đã học tới đâu?
Sách đã học xong chưa?
Có thể tiếp tục học hay ôn tập không?
```

Phase 12 trả lời:

```text
Ngày nào, giờ nào, user cần học buổi nào?
Một buổi học gồm learning units nào?
```

Phase 13 bổ sung phần thao tác thật trên lịch:

```text
User xem lịch theo tuần/tháng.
User dời một buổi học cụ thể.
User bỏ qua một buổi học cụ thể.
User nhận thông báo khi trễ một buổi học.
```

FE không cần tự regenerate plan khi user chỉ muốn dời một buổi. Backend đã có API thao tác trực tiếp trên `reading_plan_sessions`.

---

## 2. Những Gì Đã Có Sau Phase 13

Backend đã thêm:

```text
GET  /api/v1/reading-plan/sessions
POST /api/v1/reading-plan/sessions/{session_id}/skip
PUT  /api/v1/reading-plan/sessions/{session_id}/schedule
```

Backend cũng đã thêm missed reminder qua notification hiện tại:

```json
{
  "type": "plan_reminder",
  "payload": {
    "subtype": "missed_session",
    "action_type": "open_plan_session"
  }
}
```

Phase 13 **chưa** implement learning round / học lại sách từ đầu. Nếu FE cần nút "Học lại từ đầu", hiện tại chỉ nên để disabled, ẩn, hoặc ghi là tính năng sau.

---

## 3. Khái Niệm FE Cần Hiểu

### 3.1 Reading Plan Session

Một `ReadingPlanSession` là một buổi học cụ thể đã được backend sinh từ ReadingPlan.

Ví dụ:

```text
Thứ sáu, 20:00, ngày 2026-06-12
Học Unit 1 và Unit 2 của sách A
```

### 3.2 Weekly Plan Rule Khác Session Cụ Thể

`schedule_config` và `reminder_time` trong ReadingPlan là rule lặp lại:

```text
Mon/Wed/Fri lúc 20:00
```

`reading_plan_sessions` là lịch cụ thể:

```text
2026-06-12 20:00
2026-06-15 20:00
2026-06-17 20:00
```

Khi user dời một buổi học, FE gọi API reschedule session, không gọi update toàn bộ ReadingPlan.

### 3.3 Skip Khác Complete

Skip nghĩa là:

```text
User bỏ qua buổi học này.
```

Skip không có nghĩa là:

```text
User đã học xong nội dung.
```

Vì vậy khi FE gọi skip:

- Không tăng progress sách.
- Không tạo lịch ôn tập.
- Không đánh dấu learning unit là completed.
- Chỉ đổi trạng thái buổi học thành `skipped`.

### 3.4 Missed Vẫn Có Thể Học Bù

`missed` nghĩa là buổi học đã qua giờ nhưng chưa hoàn thành.

FE vẫn nên cho CTA:

```text
Học bù
Tiếp tục học
Dời lịch
Bỏ qua
```

Không nên khóa session missed.

---

## 4. Data Model FE Cần Có

Nếu FE đã implement Phase 12 thì model `ReadingPlanSession` gần như dùng lại được.

### 4.1 ReadingPlanSession

```dart
class ReadingPlanSession {
  final String id;
  final String planId;
  final String bookId;
  final String mode; // full | pareto
  final int sessionIndex;
  final DateTime scheduledAt; // UTC from backend
  final String localDate; // yyyy-MM-dd in session timezone
  final String reminderTime; // HH:mm
  final String timezone;
  final String status;
  final int completedUnits;
  final int totalUnits;
  final bool isOverdue;
  final DateTime? startedAt;
  final DateTime? completedAt;
  final DateTime? missedAt;
  final DateTime? skippedAt;
  final List<ReadingPlanSessionUnit> units;
}
```

### 4.2 ReadingPlanSessionUnit

```dart
class ReadingPlanSessionUnit {
  final String id;
  final String learningUnitId;
  final String unitTitle;
  final int unitOrder;
  final String status; // pending | in_progress | completed | skipped
  final DateTime? completedAt;
}
```

### 4.3 ReadingPlanSessionRangeResponse

```dart
class ReadingPlanSessionRangeResponse {
  final String? bookId;
  final String? localDate;
  final String? timezone;
  final String fromDate; // yyyy-MM-dd
  final String toDate;   // yyyy-MM-dd
  final int total;
  final Map<String, int> summary;
  final List<ReadingPlanSession> items;
}
```

### 4.4 ReadingPlanSessionActionResponse

```dart
class ReadingPlanSessionActionResponse {
  final String message;
  final ReadingPlanSession session;
}
```

---

## 5. Status Mapping

### 5.1 Session Status

| Backend status | FE label gợi ý | CTA chính |
| --- | --- | --- |
| `scheduled` | Sắp học | Bắt đầu học / Dời lịch / Bỏ qua |
| `due` | Đến giờ học | Học ngay / Dời lịch / Bỏ qua |
| `in_progress` | Đang học | Tiếp tục / Dời lịch |
| `completed` | Đã xong | Xem lại |
| `missed` | Đã trễ | Học bù / Dời lịch / Bỏ qua |
| `skipped` | Đã bỏ qua | Không có CTA chính |
| `cancelled` | Đã huỷ | Không hiển thị mặc định |

### 5.2 Session Unit Status

| Backend status | FE label gợi ý |
| --- | --- |
| `pending` | Chưa học |
| `in_progress` | Đang học |
| `completed` | Đã xong |
| `skipped` | Đã bỏ qua |

---

## 6. API Contract

Base URL:

```text
/api/v1
```

Tất cả API bên dưới cần auth token như các API hiện tại.

---

## 7. GET /reading-plan/sessions

### 7.1 Khi Nào Gọi

FE gọi endpoint này khi:

- Mở màn Calendar.
- Mở tab "Tuần này".
- Mở tab "Tháng này".
- Cần xem toàn bộ lịch học nhiều sách trong một khoảng ngày.

Endpoint này khác với:

```text
GET /books/{book_id}/reading-plan/sessions
```

Endpoint Phase 12 chỉ tốt cho Book Detail của một sách. Endpoint Phase 13 tốt cho calendar toàn app.

### 7.2 Query

```text
GET /api/v1/reading-plan/sessions?from_date=2026-06-01&to_date=2026-06-30
```

Optional:

```text
book_id=uuid
mode=full|pareto
status=scheduled|due|in_progress|completed|missed|skipped
```

Ví dụ:

```text
GET /api/v1/reading-plan/sessions?from_date=2026-06-10&to_date=2026-06-16
GET /api/v1/reading-plan/sessions?from_date=2026-06-01&to_date=2026-06-30&status=missed
GET /api/v1/reading-plan/sessions?from_date=2026-06-01&to_date=2026-06-30&book_id={bookId}
```

Nếu FE không truyền `from_date` và `to_date`, backend dùng khoảng mặc định:

```text
hôm nay - 7 ngày -> hôm nay + 30 ngày
```

FE nên truyền rõ range để UI ổn định.

### 7.3 Response Mẫu

```json
{
  "book_id": null,
  "local_date": null,
  "timezone": "Asia/Ho_Chi_Minh",
  "from_date": "2026-06-01",
  "to_date": "2026-06-30",
  "total": 2,
  "summary": {
    "scheduled": 1,
    "due": 0,
    "in_progress": 0,
    "completed": 0,
    "missed": 1,
    "skipped": 0,
    "cancelled": 0
  },
  "items": [
    {
      "id": "5bbec9d5-e613-42e2-81f6-d05603f4ee6e",
      "plan_id": "be9fc3ec-4a61-4356-8543-8adb4e385672",
      "book_id": "2860204a-62b9-4f4f-91cb-8f6a92b075ff",
      "mode": "pareto",
      "session_index": 0,
      "scheduled_at": "2026-06-12T13:00:00Z",
      "local_date": "2026-06-12",
      "reminder_time": "20:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "status": "scheduled",
      "completed_units": 0,
      "total_units": 2,
      "is_overdue": false,
      "started_at": null,
      "completed_at": null,
      "missed_at": null,
      "skipped_at": null,
      "units": [
        {
          "id": "8e4e9759-4c26-4d78-b296-8f09fb44cb8f",
          "learning_unit_id": "61365576-2b6c-4bcc-bb39-f19beb79c146",
          "unit_title": "Phương pháp luận nghiên cứu",
          "unit_order": 0,
          "status": "pending",
          "completed_at": null
        }
      ]
    }
  ]
}
```

### 7.4 FE UI Gợi Ý

Calendar screen:

- Group theo `local_date`.
- Mỗi ngày hiển thị số session bằng `items`.
- Dùng `summary` để render filter chips hoặc badges.
- Khi tap một session:
  - Nếu có unit chưa completed -> mở unit đầu tiên chưa completed.
  - Nếu session completed -> cho xem lại danh sách units.

### 7.5 Error Cases

| HTTP | Khi nào | FE xử lý |
| --- | --- | --- |
| 400 | `from_date > to_date` | Show message backend |
| 400 | range quá lớn | Giới hạn lại calendar range |
| 400 | mode/status không hợp lệ | Fix client request |
| 404 | `book_id` không thuộc user | Pop screen hoặc show not found |

---

## 8. POST /reading-plan/sessions/{session_id}/skip

### 8.1 Khi Nào Gọi

FE gọi khi user bấm:

```text
Bỏ qua buổi học
```

Nên show confirm dialog/bottom sheet trước khi gọi.

### 8.2 Request

```http
POST /api/v1/reading-plan/sessions/{session_id}/skip
```

Body optional:

```json
{
  "reason": "busy"
}
```

Hiện tại backend chưa dùng `reason` cho analytics, nhưng FE có thể không gửi hoặc gửi đơn giản.

### 8.3 Response

```json
{
  "message": "Đã bỏ qua buổi học.",
  "session": {
    "id": "5bbec9d5-e613-42e2-81f6-d05603f4ee6e",
    "status": "skipped",
    "skipped_at": "2026-06-12T10:30:00Z",
    "completed_units": 0,
    "total_units": 2,
    "units": [
      {
        "status": "skipped"
      }
    ]
  }
}
```

### 8.4 FE Rule Quan Trọng

Sau khi skip thành công:

- Update session trong local state bằng response.
- Không tự tăng book progress.
- Không tự đánh dấu unit completed.
- Refresh calendar range nếu cần.

### 8.5 Cho Phép Skip Khi

```text
scheduled
due
in_progress
missed
```

### 8.6 Không Cho Skip Khi

```text
completed
skipped
cancelled
```

Backend trả 409 nếu session đã ở trạng thái cuối.

---

## 9. PUT /reading-plan/sessions/{session_id}/schedule

### 9.1 Khi Nào Gọi

FE gọi khi user chỉ muốn dời **một buổi học cụ thể**.

Không dùng endpoint này để đổi toàn bộ lịch học của sách. Đổi toàn bộ lịch học vẫn dùng:

```text
PUT /api/v1/books/{book_id}/reading-plan
```

### 9.2 Request

```http
PUT /api/v1/reading-plan/sessions/{session_id}/schedule
```

Body:

```json
{
  "local_date": "2026-06-16",
  "reminder_time": "21:00"
}
```

Optional:

```json
{
  "local_date": "2026-06-16",
  "reminder_time": "21:00",
  "timezone": "Asia/Ho_Chi_Minh"
}
```

Nếu FE không gửi timezone, backend dùng timezone hiện tại của session.

### 9.3 Response

```json
{
  "message": "Đã dời lịch buổi học.",
  "session": {
    "id": "5bbec9d5-e613-42e2-81f6-d05603f4ee6e",
    "scheduled_at": "2026-06-16T14:00:00Z",
    "local_date": "2026-06-16",
    "reminder_time": "21:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "status": "scheduled",
    "units": []
  }
}
```

### 9.4 FE Rule Quan Trọng

Sau khi reschedule thành công:

- Update session trong local state bằng response.
- Không gọi lại `POST /generate-plan`.
- Không gọi `PUT /books/{book_id}/reading-plan` nếu chỉ dời một buổi.
- Refresh calendar range nếu màn đang hiển thị nhiều ngày.

### 9.5 Trạng Thái Sau Khi Dời

Nếu dời sang tương lai:

- Session chưa học -> `scheduled`.
- Session đã học dở -> `in_progress`.

Nếu dời sang thời điểm đã qua:

- Backend có thể trả `missed`.

FE nên render theo `status` backend trả về, không tự suy luận.

### 9.6 Error Cases

| HTTP | Khi nào | FE xử lý |
| --- | --- | --- |
| 400 | `reminder_time` không đúng `HH:MM` | Validate time picker |
| 400 | timezone không hợp lệ | Dùng timezone mặc định |
| 404 | session không tồn tại hoặc không thuộc user | Pop/refresh calendar |
| 409 | session đã completed/skipped/cancelled | Refresh session và disable action |
| 409 | lịch bị trùng session khác | Show message backend |

Conflict response ví dụ:

```json
{
  "detail": "Lịch học bị trùng với sách \"Tên sách\" vào 21:00 ngày 2026-06-16."
}
```

---

## 10. Missed Session Notification

### 10.1 FE Nhận Notification Như Nào

Backend dùng notification type hiện tại:

```text
plan_reminder
```

Nhưng payload có subtype:

```json
{
  "subtype": "missed_session",
  "book_id": "uuid",
  "book_title": "Tên sách",
  "plan_id": "uuid",
  "session_id": "uuid",
  "session_index": 0,
  "mode": "pareto",
  "local_date": "2026-06-12",
  "action_type": "open_plan_session",
  "action_payload": {
    "book_id": "uuid",
    "plan_id": "uuid",
    "session_id": "uuid",
    "mode": "pareto"
  }
}
```

### 10.2 UI Copy Backend Trả

Backend copy hiện tại:

```text
Title: Bạn đã lỡ một buổi học
Body: Có thể học bù {book_title} khi bạn rảnh.
```

### 10.3 FE Routing

Khi user tap notification:

```text
action_type = open_plan_session
```

FE nên:

1. Mở Book Detail hoặc Calendar Session Detail.
2. Fetch session mới nhất nếu cần.
3. Scroll/highlight session theo `session_id`.
4. Nếu session vẫn `missed`, hiển thị CTA "Học bù".

### 10.4 Không Spam

Backend đã chống trùng bằng idempotency. FE không cần tự chống duplicate notification, nhưng nên dùng `id` hoặc `outbox_id` nếu notification list có hỗ trợ để tránh render trùng trong local cache.

---

## 11. UI/UX Mapping Đề Xuất

### 11.1 Calendar Screen

FE nên có màn hoặc tab:

```text
Lịch học
```

Data source:

```text
GET /api/v1/reading-plan/sessions?from_date=...&to_date=...
```

UI:

- Month/week calendar.
- Dot/badge theo ngày có session.
- Filter: Tất cả, Sắp học, Đang học, Trễ, Đã xong.
- Empty state: "Chưa có lịch học trong khoảng này".

### 11.2 Session Card

Session card nên hiển thị:

- Tên sách.
- Giờ local: `reminder_time`.
- Status label.
- `completed_units / total_units`.
- Danh sách unit ngắn, tối đa 2-3 dòng.

CTA theo status:

```dart
switch (session.status) {
  case 'scheduled':
    showStart();
    showReschedule();
    showSkip();
    break;
  case 'due':
    showStart(primary: true);
    showReschedule();
    showSkip();
    break;
  case 'in_progress':
    showContinue(primary: true);
    showReschedule();
    break;
  case 'missed':
    showCatchUp(primary: true);
    showReschedule();
    showSkip();
    break;
  case 'completed':
    showReviewOrReplay();
    break;
  case 'skipped':
    showDisabledState();
    break;
}
```

### 11.3 Reschedule Bottom Sheet

Fields:

- Date picker.
- Time picker.

Submit:

```text
PUT /reading-plan/sessions/{session_id}/schedule
```

Sau submit:

- Close bottom sheet.
- Update card bằng response.
- Refresh calendar range.
- Nếu 409 conflict, giữ bottom sheet và show message.

### 11.4 Skip Confirm

Trước khi skip, show confirm:

```text
Bỏ qua buổi học này?
Bạn có thể dời lịch nếu vẫn muốn học bù sau.
```

CTA:

- `Dời lịch`
- `Bỏ qua`
- `Huỷ`

Recommendation:

```text
Với session missed, ưu tiên CTA "Dời lịch" hoặc "Học bù" hơn "Bỏ qua".
```

---

## 12. Những Gì FE Không Nên Làm

FE không nên:

- Gọi `POST /generate-plan` để dời một buổi học.
- Gọi `PUT /books/{book_id}/reading-plan` nếu chỉ dời một session.
- Tự đổi session `missed` thành `completed`.
- Tự tăng book progress khi user skip session.
- Tự xoá session khỏi UI sau khi skip; hãy render `skipped` hoặc ẩn theo filter.
- Tự tạo logic "học lại từ đầu" bằng cách reset local state.

---

## 13. Gửi Cho FE Những File Nào

Đúng, nếu FE đang implement nhóm chức năng học tập mới, em nên gửi 3 file:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_11_learning_progress_completion_contract.md
_docs_implemented/doc_setup_flutter/flutter_phase_12_calendar_reading_plan_contract.md
_docs_implemented/doc_setup_flutter/flutter_phase_13_calendar_session_actions_contract.md
```

Thứ tự đọc nên là:

```text
Phase 11 -> Phase 12 -> Phase 13
```

Vì:

- Phase 11 giải thích progress/completion.
- Phase 12 giải thích session calendar.
- Phase 13 giải thích thao tác trên session calendar.

---

## 14. Manual FE Test Checklist

### 14.1 Calendar Range

1. Login.
2. Có ít nhất một sách đã có active reading plan.
3. Gọi:

```text
GET /api/v1/reading-plan/sessions?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD
```

4. Calendar hiển thị sessions theo `local_date`.
5. Filter `status=missed` chỉ hiện session trễ.

### 14.2 Reschedule

1. Chọn một session `scheduled` hoặc `missed`.
2. Mở bottom sheet dời lịch.
3. Chọn ngày/giờ mới.
4. Gọi:

```text
PUT /api/v1/reading-plan/sessions/{session_id}/schedule
```

5. UI cập nhật đúng ngày/giờ mới.
6. Không gọi generate-plan.

### 14.3 Conflict

1. Tạo hai session khác nhau.
2. Dời session A vào cùng ngày/giờ session B.
3. Backend trả 409.
4. FE hiển thị message backend.

### 14.4 Skip

1. Chọn một session `scheduled`, `due`, `in_progress` hoặc `missed`.
2. Confirm skip.
3. Gọi:

```text
POST /api/v1/reading-plan/sessions/{session_id}/skip
```

4. UI đổi status sang `skipped`.
5. Book progress không tăng.

### 14.5 Missed Notification

1. Có session quá hạn.
2. Backend scanner tạo notification.
3. FE nhận notification `plan_reminder` với `payload.subtype=missed_session`.
4. Tap notification mở đúng Book Detail/session.
5. CTA chính là "Học bù" hoặc "Dời lịch".

---

## 15. Scope Sau Phase 13

Chưa implement:

- Learning round / học lại sách từ đầu.
- Complete session thủ công.
- Undo skip.
- Drag-and-drop calendar.

Recommendation:

```text
FE có thể release calendar/session actions với Phase 13.1 hiện tại.
Learning round nên để phase sau hoặc hướng phát triển luận văn.
```
