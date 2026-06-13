# Flutter Phase 12 Contract - Calendar Reading Plan Sessions

Date: 2026-06-12  
Status: **Backend implemented, FE migration guide**  
Backend phase: `_docs_implemented/phase_12_calendar_reading_plan_sessions_implementation_guide.md`  
Related FE doc: `_docs_implemented/doc_setup_flutter/flutter_phase_11_learning_progress_completion_contract.md`

---

## 1. Mục Tiêu FE Cần Sửa

Phase 11 đã giúp FE biết:

```text
User đã học tới đâu?
User đã học xong sách chưa?
User có thể tiếp tục học hoặc ôn tập không?
```

Phase 12 bổ sung phần còn thiếu:

```text
Ngày nào, giờ nào, user nên học bài nào?
Buổi học hôm nay là buổi nào?
Một buổi học gồm những learning units nào?
Buổi học đã scheduled, in_progress, completed hay missed?
```

Từ Phase 12, FE không nên tự suy luận lịch học chỉ từ:

```text
schedule_config = ["Mon", "Wed", "Fri"]
reminder_time = "20:00"
```

Vì đó chỉ là **cấu hình lặp lại**. FE cần dùng `reading_plan_sessions` để hiển thị lịch học theo ngày/tháng/năm cụ thể.

---

## 2. Khái Niệm FE Cần Hiểu

### 2.1 ReadingPlan

`ReadingPlan` là cấu hình kế hoạch học của một sách:

```text
mode
pace
schedule_config
reminder_time
status
```

FE dùng để:

- Prefill màn chỉnh lịch.
- Hiển thị kế hoạch đang active/inactive/completed.
- Cho user đổi ngày học, giờ học, tốc độ học.

### 2.2 Active Slots

`active_slots` là lịch lặp lại theo tuần:

```text
Monday 20:00
Wednesday 20:00
Friday 20:00
```

FE dùng để:

- Hiển thị rule lịch học user đã chọn.
- Tránh chọn trùng lịch với sách khác.
- Không dùng để vẽ calendar cụ thể từng ngày.

### 2.3 Reading Plan Sessions

`sessions` là các buổi học cụ thể:

```text
2026-06-12 20:00 học Unit 1, Unit 2
2026-06-15 20:00 học Unit 3
```

FE dùng để:

- Vẽ "Hôm nay học gì".
- Vẽ "Lịch học sắp tới".
- Hiển thị tiến độ từng buổi học.
- Mở đúng learning unit khi user bấm vào một buổi học.

### 2.4 Session Units

Một session có thể chứa nhiều learning units.

Ví dụ:

```text
pace = 2
total learning units = 3

Session 1:
  Unit 1
  Unit 2

Session 2:
  Unit 3
```

FE không nên giả định một session chỉ có một unit.

---

## 3. API Contract

Base URL:

```text
/api/v1
```

Tất cả API bên dưới cần auth token như các API hiện tại.

---

## 4. GET /books/{book_id}/reading-plan

### 4.1 Khi Nào Gọi

FE gọi endpoint này khi:

- Mở màn Book Detail.
- Mở màn chỉnh lịch học.
- Cần biết plan hiện tại của sách.
- Cần lấy `session_summary` nhanh.

### 4.2 Response Mẫu

```json
{
  "plan_id": "be9fc3ec-4a61-4356-8543-8adb4e385672",
  "book_id": "2860204a-62b9-4f4f-91cb-8f6a92b075ff",
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "status": "active",
  "plan_status": "active",
  "active_slots": [
    {
      "id": "7da9c212-d27a-416d-96f2-adf3393041de",
      "weekday": 0,
      "weekday_label": "monday",
      "reminder_time": "20:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "is_active": true
    }
  ],
  "created_at": "2026-06-10T10:48:20.556407Z",
  "updated_at": "2026-06-12T10:18:37.459883Z",
  "started_at": "2026-06-12T10:18:37.459883Z",
  "paused_at": null,
  "completed_at": null,
  "session_summary": {
    "total_sessions": 2,
    "completed_sessions": 0,
    "missed_sessions": 0,
    "next_session": {
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
      "units": []
    }
  }
}
```

### 4.3 FE Mapping

| Field | Ý nghĩa | FE dùng để |
| --- | --- | --- |
| `pace` | Số learning units mỗi buổi học | Hiển thị/chỉnh tốc độ học |
| `schedule_config` | Ngày học lặp lại theo tuần | Prefill selector thứ |
| `reminder_time` | Giờ nhắc học | Prefill time picker |
| `active_slots` | Các slot đang active | UI rule lịch học |
| `session_summary.total_sessions` | Tổng buổi học cụ thể | Progress kế hoạch |
| `session_summary.next_session` | Buổi học tiếp theo | CTA "Học tiếp hôm nay/sắp tới" |

---

## 5. PUT /books/{book_id}/reading-plan

### 5.1 Khi Nào Gọi

FE gọi khi user chỉnh:

- Tốc độ học mỗi buổi.
- Ngày học trong tuần.
- Giờ nhắc học.

### 5.2 Request Body

Tất cả field đều optional, FE chỉ gửi field thay đổi cũng được.

```json
{
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00"
}
```

### 5.3 Response

Response giống `GET /books/{book_id}/reading-plan`, có thêm:

```json
{
  "message": "Đã cập nhật kế hoạch học tập."
}
```

### 5.4 FE Rule Quan Trọng

Nếu sách đã `ready`, FE **không gọi** `POST /generate-plan` để đổi lịch.

Flow đúng:

```text
Sách draft mới upload:
  POST /generate-plan

Sách đã ready/partial_ready:
  PUT /books/{book_id}/reading-plan
```

Nếu FE gọi `POST /generate-plan` với sách `ready`, backend trả:

```json
{
  "detail": "Sách đang ở trạng thái 'ready', không thể tạo plan mới."
}
```

Đây là đúng business logic, không phải lỗi backend.

---

## 6. GET /books/{book_id}/reading-plan/sessions

### 6.1 Khi Nào Gọi

FE gọi endpoint này khi:

- Mở Book Detail.
- Mở màn lịch học của sách.
- Cần hiển thị toàn bộ session cụ thể của một sách.

### 6.2 Query

```text
GET /api/v1/books/{book_id}/reading-plan/sessions
GET /api/v1/books/{book_id}/reading-plan/sessions?mode=full
GET /api/v1/books/{book_id}/reading-plan/sessions?mode=pareto
```

Nên truyền `mode` nếu màn hiện tại đang ở mode rõ ràng.

### 6.3 Response Mẫu

```json
{
  "book_id": "2860204a-62b9-4f4f-91cb-8f6a92b075ff",
  "local_date": null,
  "timezone": null,
  "total": 2,
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
      "status": "in_progress",
      "completed_units": 0,
      "total_units": 2,
      "is_overdue": false,
      "started_at": "2026-06-12T10:55:53.344263Z",
      "completed_at": null,
      "missed_at": null,
      "skipped_at": null,
      "units": [
        {
          "id": "8e4e9759-4c26-4d78-b296-8f09fb44cb8f",
          "learning_unit_id": "61365576-2b6c-4bcc-bb39-f19beb79c146",
          "unit_title": "Phương pháp luận nghiên cứu",
          "unit_order": 0,
          "status": "in_progress",
          "completed_at": null
        }
      ]
    }
  ]
}
```

### 6.4 Session Status

| Status | Ý nghĩa | FE nên hiển thị |
| --- | --- | --- |
| `scheduled` | Buổi học tương lai, chưa học | Sắp học |
| `due` | Đã tới giờ học, có thể nhắc | Đến giờ học |
| `in_progress` | User đã học ít nhất một unit trong buổi | Đang học |
| `completed` | Tất cả unit trong buổi đã hoàn thành | Đã xong |
| `missed` | Quá giờ nhưng chưa hoàn thành | Đã trễ |
| `skipped` | Bỏ qua thủ công | Đã bỏ qua |
| `cancelled` | Session cũ đã huỷ do update lịch | FE thường không thấy trong endpoint thường |

### 6.5 Unit Status

| Status | Ý nghĩa | FE nên hiển thị |
| --- | --- | --- |
| `pending` | Chưa học unit này | Chưa học |
| `in_progress` | Đang học dở | Đang học |
| `completed` | Đã hoàn thành | Đã xong |
| `skipped` | Bỏ qua | Đã bỏ qua |

---

## 7. GET /reading-plan/sessions/today

### 7.1 Khi Nào Gọi

FE gọi endpoint này cho:

- Home screen.
- Tab "Hôm nay".
- Widget "Hôm nay học gì".

### 7.2 Query

Không truyền gì:

```text
GET /api/v1/reading-plan/sessions/today
```

Backend dùng timezone trong notification settings của user.

Truyền ngày cụ thể:

```text
GET /api/v1/reading-plan/sessions/today?local_date=2026-06-12
```

FE dùng query này khi user chọn ngày trong calendar.

### 7.3 Response

```json
{
  "book_id": null,
  "local_date": "2026-06-12",
  "timezone": "Asia/Ho_Chi_Minh",
  "total": 1,
  "items": []
}
```

`items` có cùng schema với session list của sách.

---

## 8. Generate Plan Flow Sau Phase 12

### 8.1 Sách Mới Upload

Flow chuẩn:

```text
POST /upload
-> book.status = draft

POST /generate-plan
-> tạo ReadingPlan
-> nếu activate=true thì sinh sessions ngay
-> enqueue background processing
```

Request:

```json
{
  "book_id": "new-draft-book-id",
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "activate": true
}
```

### 8.2 `activate=false`

Nếu FE gửi:

```json
{
  "activate": false
}
```

Thì backend tạo plan inactive.

FE nên hiểu:

- Plan có thể đã tồn tại.
- Audio/background processing vẫn chạy theo flow generate.
- Calendar sessions có thể chưa được sinh ngay.
- Muốn kích hoạt lịch học thì gọi:

```text
POST /api/v1/books/{book_id}/resume
```

### 8.3 Sách Đã Ready

Với sách đã `ready` hoặc `partial_ready`, FE không gọi `POST /generate-plan`.

Flow đúng:

```text
GET /books/{book_id}/reading-plan
PUT /books/{book_id}/reading-plan
GET /books/{book_id}/reading-plan/sessions
```

---

## 9. Pause / Resume Plan

### 9.1 Pause

```text
POST /api/v1/books/{book_id}/pause
```

FE dùng khi user muốn tạm dừng học sách.

Expected UI:

- Plan chuyển `inactive`.
- Không hiện lịch học active trong home.
- Không nhắc lịch học sách đó.

### 9.2 Resume

```text
POST /api/v1/books/{book_id}/resume
```

FE dùng khi user muốn tiếp tục lịch học.

Backend sẽ:

- Validate không trùng lịch với sách khác.
- Tạo lại `active_slots`.
- Sinh concrete sessions cho các unit chưa completed.

Nếu sách đã completed, backend trả 409. FE nên tránh gọi resume cho sách đã hoàn thành.

---

## 10. UI/UX Mapping

### 10.1 Book Detail

Book Detail nên có section:

```text
Lịch học
```

Nội dung gợi ý:

- Rule lịch: "Thứ hai, thứ tư, thứ sáu lúc 20:00".
- Tiến độ plan: "0/2 buổi đã hoàn thành".
- Buổi tiếp theo: ngày, giờ, danh sách unit.
- CTA: "Học buổi này" hoặc "Tiếp tục học".

### 10.2 Home Screen

Home nên gọi:

```text
GET /api/v1/reading-plan/sessions/today
```

UI gợi ý:

- Nếu `total=0`: empty state "Hôm nay chưa có lịch học".
- Nếu có sessions:
  - Group theo sách.
  - Hiển thị giờ học local.
  - Hiển thị status session.
  - CTA mở Book Detail hoặc Learning Unit đầu tiên chưa hoàn thành.

### 10.3 Calendar / Schedule Screen

FE có thể dùng:

```text
GET /api/v1/books/{book_id}/reading-plan/sessions
```

UI gợi ý:

- Timeline buổi học.
- Badge status:
  - Sắp học
  - Đang học
  - Đã xong
  - Đã trễ
- List units trong mỗi buổi.

### 10.4 Edit Plan Screen

FE nên prefill từ:

```text
GET /api/v1/books/{book_id}/reading-plan
```

Fields:

- `pace`
- `schedule_config`
- `reminder_time`

Khi save:

```text
PUT /api/v1/books/{book_id}/reading-plan
```

Sau khi save thành công:

```text
GET /api/v1/books/{book_id}/reading-plan/sessions
```

để refresh calendar UI.

---

## 11. Important Edge Cases

### 11.1 Data Cũ Trước Phase 12

Một số sách đã có progress trước khi Phase 12 sinh sessions.

Khi backend regenerate sessions, có thể thấy:

```text
session.started_at < session.scheduled_at
```

Đây không phải lỗi nghiêm trọng. Nó nghĩa là user đã học unit trước khi lịch cụ thể được sinh.

Với sách upload mới sau Phase 12, flow sẽ sạch hơn:

```text
generate-plan activate=true
-> sessions scheduled
-> user học
-> sessions in_progress/completed
```

### 11.2 `completed_units = 0` Nhưng Session `in_progress`

Trường hợp hợp lệ:

```text
Unit 1 đang in_progress nhưng chưa completed.
Unit 2 pending.
```

Khi đó:

```text
session.status = in_progress
completed_units = 0
total_units = 2
```

FE không nên hiểu `completed_units=0` là chưa học gì. Hãy đọc cả `status`.

### 11.3 `local_date` Và Timezone

Backend trả:

```text
scheduled_at = UTC
local_date = ngày local theo timezone user
timezone = Asia/Ho_Chi_Minh
```

FE nên hiển thị theo timezone của session hoặc device local. Với user Việt Nam, `2026-06-12T13:00:00Z` là `20:00 Asia/Ho_Chi_Minh`.

### 11.4 Update Plan Regenerates Future Sessions

Khi FE update plan:

- Backend huỷ sessions chưa xong cũ.
- Backend sinh sessions mới cho các unit chưa completed.
- Endpoint thường không trả `cancelled` sessions.

FE chỉ cần refresh sessions sau update.

### 11.5 Conflict 409

Nếu lịch bị trùng sách khác, backend trả 409:

```json
{
  "detail": "Lịch học bị trùng vào Thứ hai lúc 20:00. Hãy chọn ngày hoặc giờ khác."
}
```

FE nên hiển thị message này trực tiếp hoặc mapping sang snackbar/bottom sheet.

---

## 12. FE Implementation Checklist

### 12.1 Data Layer

- Thêm model `ReadingPlanSession`.
- Thêm model `ReadingPlanSessionUnit`.
- Update model `ReadingPlanResponse` để có `session_summary`.
- Update plan repository/service gọi API session mới.

### 12.2 Book Detail

- Gọi `GET /books/{book_id}/reading-plan`.
- Gọi `GET /books/{book_id}/reading-plan/sessions?mode=currentMode`.
- Hiển thị rule lịch học từ `active_slots`.
- Hiển thị session tiếp theo từ `session_summary.next_session`.
- Hiển thị timeline sessions.

### 12.3 Home / Today

- Gọi `GET /reading-plan/sessions/today`.
- Hiển thị các session hôm nay.
- Nếu session `missed`, hiển thị trạng thái trễ nhưng vẫn cho học bù.

### 12.4 Edit Plan

- Prefill `pace`, `schedule_config`, `reminder_time`.
- Save bằng `PUT /books/{book_id}/reading-plan`.
- Sau khi save, refresh sessions.
- Không gọi `POST /generate-plan` với sách đã `ready`.

### 12.5 Generate Plan

- Với sách mới `draft`, FE dùng `POST /generate-plan`.
- Nếu muốn test Phase 12 ngay, dùng `activate=true`.
- Nếu `activate=false`, FE cần gọi `POST /books/{book_id}/resume` sau đó để bật lịch.

---

## 13. Manual Test Checklist Cho FE

1. Upload sách mới.
2. Generate plan với `activate=true`, `pace=2`, `schedule_config=["Mon","Wed","Fri"]`.
3. Poll job tới `partial_ready/ready`.
4. Gọi `GET /books/{book_id}/reading-plan`.
5. Kiểm tra `session_summary.total_sessions`.
6. Gọi `GET /books/{book_id}/reading-plan/sessions`.
7. Kiểm tra mỗi session có đúng số units theo `pace`.
8. Gọi `GET /reading-plan/sessions/today`.
9. Update plan sang giờ/ngày khác.
10. Refresh sessions và xác nhận lịch mới.
11. Nghe một unit, call progress.
12. Xác nhận session chuyển `in_progress`.
13. Hoàn thành tất cả units trong session.
14. Xác nhận session chuyển `completed`.
15. Để một session quá hạn rồi gọi sessions API.
16. Xác nhận session chuyển `missed` nhưng vẫn có thể học bù.

---

## 14. Những Gì Chưa Có Trong Phase 12

Phase 12 chưa có:

- API skip session thủ công.
- API complete session thủ công.
- Notification riêng cho missed session.
- Calendar range endpoint theo tuần/tháng.

Hiện tại FE có thể build UI tốt bằng:

```text
GET /books/{book_id}/reading-plan
GET /books/{book_id}/reading-plan/sessions
GET /reading-plan/sessions/today
PUT /books/{book_id}/reading-plan
POST /books/{book_id}/pause
POST /books/{book_id}/resume
```

Các phần skip/missed notification/range calendar nên để Phase 13 hoặc phase UX polish sau.
