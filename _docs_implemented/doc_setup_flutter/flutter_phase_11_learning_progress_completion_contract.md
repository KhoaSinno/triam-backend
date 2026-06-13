# Flutter Phase 11 Contract - Learning Progress, Completion State, Review Entry

Date: 2026-06-11  
Status: **Backend implemented, FE migration guide**  
Backend phase: `_docs_implemented/phase_11_learning_progress_completion_state_implementation_guide.md`

---

## 1. Mục Tiêu FE Cần Sửa

Từ Phase 11, FE không được suy ra trạng thái học tập chỉ từ:

```text
book.status
reading_plan.status
```

Lý do:

- `book.status` chỉ nói backend xử lý audio/tài liệu tới đâu.
- `reading_plan.status` chỉ nói lịch học đang active/inactive/completed.
- User đã học xong hay chưa phải đọc từ `learning_status`.

Backend đã bổ sung:

```text
learning_status = not_started | in_progress | completed
```

FE nên dùng field này để render Library, Book Detail, CTA tiếp tục học và CTA ôn tập.

---

## 2. API Thay Đổi

### 2.1 GET /api/v1/books

Mỗi book item có thêm field optional:

```json
{
  "id": "uuid",
  "title": "Tên sách",
  "status": "ready",
  "learning_status": "completed",
  "book_progress_percent": 100,
  "completed_at": "2026-06-11T10:20:00Z"
}
```

FE rule:

```text
status                  -> trạng thái xử lý sách/audio
learning_status         -> trạng thái học của user
book_progress_percent   -> progress tổng quan để vẽ progress bar
completed_at            -> thời điểm hoàn thành nếu có
```

### 2.2 GET /api/v1/study-contexts/{context_id}/documents

Trả về danh sách tài liệu thuộc Study Context chỉ định. Từ Phase 11, danh sách sách trả về cũng đã được **làm giàu (enrich) đầy đủ các trường tiến trình** tương tự như `GET /api/v1/books`:

```json
[
  {
    "id": "uuid",
    "title": "Tên sách",
    "status": "ready",
    "learning_status": "completed",
    "book_progress_percent": 100,
    "completed_at": "2026-06-11T10:20:00Z"
  }
]
```

### 2.3 GET /api/v1/books/{book_id}/details?mode=full|pareto

Response có thêm:

```json
{
  "learning_summary": {
    "book_id": "uuid",
    "mode": "full",
    "learning_status": "completed",
    "is_completed": true,
    "can_resume": false,
    "can_review": true,
    "book_progress_percent": 100,
    "completed_units": 12,
    "playable_units": 12,
    "last_learning_unit_id": "uuid",
    "last_segment_id": 123,
    "last_segment_index": 2,
    "position_ms": 45000,
    "started_at": "2026-06-11T09:00:00Z",
    "last_activity_at": "2026-06-11T10:15:00Z",
    "completed_at": "2026-06-11T10:20:00Z",
    "due_reviews_count": 1,
    "upcoming_reviews_count": 4
  }
}
```

### 2.3 GET /api/v1/books/{book_id}/learning-progress?mode=full|pareto

Response vẫn có danh sách unit progress như cũ, nhưng thêm các field tổng quan giống `learning_summary`.

FE dùng endpoint này khi cần màn progress chi tiết hoặc resume audio chính xác.

### 2.4 GET /api/v1/books/{book_id}/reading-plan

Plan có thể trả:

```json
{
  "status": "completed",
  "plan_status": "completed",
  "completed_at": "2026-06-11T10:20:00Z",
  "active_slots": []
}
```

FE không được hiểu `active_slots=[]` là chưa bắt đầu. Hãy đọc `plan_status` và `learning_status`.

### 2.5 Review List APIs

Backend thêm endpoint:

```text
GET /api/v1/reviews?status=due|upcoming|completed|skipped|all&book_id={optional}&mode={optional}
GET /api/v1/books/{book_id}/reviews?status=due|upcoming|completed|skipped|all&mode={optional}
GET /api/v1/reviews/{review_item_id}
```

Response:

```json
{
  "items": [
    {
      "review_item_id": "uuid",
      "book_id": "uuid",
      "book_title": "Tên sách",
      "learning_unit_id": "uuid",
      "learning_unit_title": "Bài học",
      "mode": "full",
      "status": "pending",
      "due_at": "2026-06-12T10:20:00Z",
      "interval_days": 1,
      "sequence_index": 0,
      "review_text": "Nội dung ôn tập",
      "review_audio_url": "https://...",
      "completed_at": null
    }
  ],
  "total": 1
}
```

Existing endpoints vẫn giữ:

```text
POST /api/v1/reviews/{review_item_id}/complete
POST /api/v1/reviews/{review_item_id}/skip
```

---

## 3. UI/UX Mapping

### 3.1 Library Card

| Backend State | FE Label | Primary CTA |
| --- | --- | --- |
| `book.status=draft` | Chưa tạo kế hoạch | Tạo kế hoạch |
| `book.status=processing` | Đang xử lý | Xem tiến độ |
| `book.status=partial_ready`, `learning_status=null/not_started` | Có thể bắt đầu | Bắt đầu học |
| `book.status=ready`, `learning_status=null/not_started` | Sẵn sàng học | Bắt đầu học |
| `learning_status=in_progress` | Đang học | Tiếp tục |
| `learning_status=completed` | Đã hoàn thành | Ôn tập |
| `book.status=error` | Lỗi xử lý | Thử lại hoặc xoá |

### 3.2 Book Detail CTA

Pseudo:

```dart
if (bookStatus == 'processing') {
  showProcessingProgress();
} else if (learningStatus == 'completed') {
  primary = 'Ôn tập';
  secondary = 'Nghe lại';
} else if (learningStatus == 'in_progress') {
  primary = 'Tiếp tục học';
} else if (bookStatus == 'partial_ready' || bookStatus == 'ready') {
  primary = 'Bắt đầu học';
}
```

### 3.3 Resume Audio

Use:

```text
learning_summary.last_learning_unit_id
learning_summary.last_segment_id
learning_summary.position_ms
```

Nếu `learning_status=completed`, không gọi `POST /books/{book_id}/resume` để restart plan. Backend sẽ trả 409.

### 3.4 Review Button

Book Detail "Ôn tập" flow:

```text
1. GET /api/v1/books/{book_id}/reviews?status=due&mode=currentMode
2. Nếu có item -> mở Review Player/Review Detail item đầu tiên
3. Nếu không có item due -> GET /api/v1/books/{book_id}/reviews?status=upcoming&mode=currentMode
4. Nếu có upcoming -> show lịch ôn sắp tới
5. Nếu không có gì -> show empty state "Chưa có lịch ôn tập"
```

---

## 4. Important Breaking-Avoidance Rules

- Không bỏ field cũ.
- FE cũ vẫn có thể dùng `book.status`, nhưng FE mới nên ưu tiên `learning_status`.
- Không dùng `plan_status=inactive` để render "Bắt đầu học" nếu `learning_status=completed`.
- Không dùng `active_slots=[]` để hiểu plan chưa active.
- Completed book vẫn có thể nghe lại audio, nhưng không auto resume plan học.

---

## 5. Manual FE Test Checklist

1. Upload/generate một sách mới.
2. Khi sách `partial_ready/ready` và `learning_status=not_started`, UI hiện "Bắt đầu học".
3. Nghe một phần, call progress, UI hiện "Tiếp tục".
4. Hoàn thành tất cả learning units, UI hiện "Đã hoàn thành".
5. Book detail không còn hiện CTA "Bắt đầu học lại" như sách mới.
6. Nút "Ôn tập" gọi `/books/{book_id}/reviews`.
7. `POST /books/{book_id}/resume` với sách completed phải được FE tránh gọi; nếu gọi sẽ nhận 409.
