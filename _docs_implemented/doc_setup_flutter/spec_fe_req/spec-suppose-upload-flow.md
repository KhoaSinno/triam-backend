# Spec: Deferred Upload Flow & Reading Plan Activation

Lưu ý đây là đề xuất, vui lòng không xem như chân lý nếu có giải pháp tối ưu hơn cho vấn đề được trình bày trong tài liệu này

## Mục Tiêu

Tách luồng upload/cấu hình kế hoạch khỏi hành động start/resume reading plan.

Hiện tại upload flow bị rối vì `POST /api/v1/generate-plan` có vẻ đang làm nhiều việc cùng lúc: tạo/generate learning plan, active reading plan, và validate trùng lịch ngay. User ở bước này chỉ đang upload tài liệu và set kế hoạch ban đầu, chưa thật sự bắt đầu học, nên conflict lịch không nên chặn upload flow.

Mục tiêu mới:

1. Upload tài liệu và tạo outline.
2. Cho user set kế hoạch học, nhưng plan vẫn ở trạng thái `inactive`.
3. Khi tài liệu `partial_ready` hoặc `ready`, app hiện widget **Tài liệu đã sẵn sàng - Bắt đầu học ngay**.
4. User bấm widget thì backend mới start/resume plan và validate conflict.

## Luồng Hiện Tại

Frontend hiện tại:

- `PersonalDocumentsPage._pickAndUpload`
- `POST /api/v1/upload`
- `_UploadToCourseWizard`
- `_submitGeneratePlanAndReport`
- `POST /api/v1/generate-plan`

Vấn đề:

- Upload flow bị chặn bởi `409 schedule_conflict`.
- Conflict xảy ra quá sớm, lúc user mới cấu hình kế hoạch.
- Plan bị trùng lịch nhưng đang không hoạt động thì không nên được tính là active slot.
- Sau upload chỉ cần set kế hoạch và generate nội dung, chưa cần start plan ngay.

## Đối Chiếu Backend Hiện Tại

Đã đối chiếu với backend tại `D:\triam-backend`.

File liên quan:

- `app/api/v1/routers/upload.py`
- `app/schemas/plan.py`
- `app/services/upload_service.py`
- `app/services/audiobook_service.py`
- `app/services/reading_plan_schedule_service.py`
- `app/repositories/reading_plan_schedule_repo.py`
- `app/core/constant.py`
- `app/models/db_models.py`

Backend hiện tại:

- `PlanInput` chưa có field `activate`.
- `PlanStatus` hiện chỉ có:
  - `active`
  - `inactive`
  - `error`
- Chưa có status `paused` riêng. `pause_reading_plan` đang set `plan.status = inactive`.
- `handle_generate_plan` đang gọi `validate_plan_schedule_for_create(...)` trước khi tạo plan.
- `validate_plan_schedule_for_create(...)` đang:
  - normalize schedule
  - validate active learning capacity
  - validate conflict với active slots
- `_create_plan_and_job(...)` đang tạo `ReadingPlan(status=PlanStatus.ACTIVE)`.
- `_create_plan_and_job(...)` đang tạo active `ReadingPlanScheduleSlot` ngay trong generate-plan.
- `GET /reading-plan-slots` đang đọc từ `list_active_slots(...)`, tức chỉ trả slots có `is_active=True`.
- `POST /books/{bookId}/pause` deactivate slots và set plan `inactive`.
- `POST /books/{bookId}/resume` validate conflict, set plan `active`, và tạo lại active slots.

Kết luận: spec này không yêu cầu tạo endpoint mới. Chỉ cần sửa semantic của `POST /generate-plan` và giữ `POST /books/{bookId}/resume` làm điểm bắt đầu học.

## UX Mục Tiêu

### Phase 1: Upload

User upload PDF/EPUB/DOCX.

Backend tạo book/document, extract metadata/outline, trả `book_id`, `document_type`, `total_chapters`, `outline`.

### Phase 2: Configure

User chọn:

- mode: `pareto` hoặc `full`
- pace
- schedule_config
- reminder_time optional

Backend lưu reading plan với `status=inactive`.

Quan trọng:

- Không active lịch học.
- Không validate conflict.
- Không đưa plan vào `/api/v1/reading-plan-slots`.
- Có thể enqueue job generate content/audio.

### Phase 3: Ready CTA

Khi tài liệu có thể học:

- `book.status = partial_ready`, hoặc
- `book.status = ready`

Frontend hiện widget:

```text
Tài liệu đã sẵn sàng
Bắt đầu học ngay
```

CTA gọi start/resume endpoint.

### Phase 4: Start/Resume

User bấm CTA.

Backend mới:

- chuyển plan `inactive` sang `active`
- validate conflict với các active plans khác
- trả active slots

## State Model

### book.status

| Status | Ý nghĩa |
| --- | --- |
| `draft` | Upload xong, chưa generate plan |
| `processing` | Đang generate learning units/audio/content |
| `partial_ready` | Đã có nội dung đầu tiên, user có thể bắt đầu học |
| `ready` | Xử lý hoàn tất |
| `error` | Xử lý lỗi |

### reading_plan.status

| Status | Ý nghĩa |
| --- | --- |
| `inactive` | Đã cấu hình, chưa bắt đầu, không tham gia lịch active |
| `active` | Đang hoạt động, tham gia lịch học/reminder |
| `completed` | Đã hoàn tất |
| `error` | Plan lỗi |

Backend hiện tại chưa có `paused`. Để giảm migration, có thể dùng `inactive` cho cả 2 trường hợp:

- plan đã cấu hình nhưng chưa bắt đầu
- plan từng active nhưng user pause

Nếu backend muốn phân biệt rõ hơn sau này, có thể thêm `paused`, nhưng version tối thiểu không bắt buộc.

## Backend Contract

### 1. Upload Document

```http
POST /api/v1/upload
Content-Type: multipart/form-data
field: file
```

Response:

```json
{
  "book_id": "book_123",
  "document_type": "pdf",
  "total_sections": 24,
  "outline_tree": [
    {
      "title": "Chapter 1",
      "page_start": 1,
      "children": []
    }
  ]
}
```

Expected behavior:

- Tạo uploaded book/document.
- Không tạo active reading plan.
- Không validate schedule conflict.

### 2. Generate Plan

```http
POST /api/v1/generate-plan
```

Request:

```json
{
  "book_id": "book_123",
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "activate": false
}
```

Field mới:

- `activate`: optional boolean.
- Default cho hành vi mới của app: `false`.

Behavior khi `activate=false`:

- Tạo hoặc update reading plan.
- Set `reading_plan.status = inactive`.
- Lưu `mode`, `pace`, `schedule_config`, `reminder_time`.
- Start/enqueue generate job nếu cần.
- Set `book.status = processing` nếu generation bắt đầu.
- Chỉ validate shape của schedule: ngày phải hợp lệ, reminder_time phải hợp lệ.
- Không validate active learning capacity.
- Không validate schedule conflict.
- Không tạo `ReadingPlanScheduleSlot` rows, hoặc tuyệt đối không tạo row nào với `is_active=True`.

Behavior khi `activate=true`:

- Validate conflict against active plans.
- Nếu conflict tồn tại, return `409 schedule_conflict`.
- Nếu không conflict, set `reading_plan.status = active`.

Response cho `activate=false`:

```json
{
  "book_id": "book_123",
  "plan_id": "plan_456",
  "plan_status": "inactive",
  "status": "queued",
  "job_id": "job_789",
  "progress_percent": 0,
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": []
}
```

Rules:

- `active_slots` phải rỗng khi `plan_status=inactive`.
- Inactive plans không được reserve schedule slots.
- Nhiều inactive plans được phép trùng cùng day/time.

Backend patch points:

- `app/schemas/plan.py`
  - thêm `activate: bool = False` vào `PlanInput`
- `app/services/upload_service.py`
  - trong `handle_generate_plan`, branch theo `payload.activate`
  - khi `activate=false`, normalize schedule nhưng bỏ conflict/capacity validation
  - khi `activate=false`, truyền empty slots vào `_create_plan_and_job`
  - khi `activate=false`, tạo `ReadingPlan(status=PlanStatus.INACTIVE)`
  - khi `activate=true`, giữ logic conflict validation và active slot creation hiện tại
- `app/services/reading_plan_schedule_service.py`
  - expose hoặc reuse `normalize_schedule_config(...)` cho config-only validation

### 3. Reading Plan Slots

```http
GET /api/v1/reading-plan-slots
```

Response:

```json
[
  {
    "day": "Mon",
    "reminder_time": "20:00",
    "book_id": "book_active",
    "book_title": "Existing Active Book",
    "plan_id": "plan_active"
  }
]
```

Rules:

- Chỉ return `reading_plan.status = active`.
- Exclude `inactive`, `draft`, `completed`, `error`.
- Endpoint này chỉ là hint cho frontend UI. Backend vẫn là canonical source.

### 4. Get Reading Plan

```http
GET /api/v1/books/{bookId}/reading-plan
```

Response:

```json
{
  "book_id": "book_123",
  "plan_id": "plan_456",
  "status": "inactive",
  "plan_status": "inactive",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": []
}
```

Notes:

- Giữ cả `status` và `plan_status` nếu cần compatibility với frontend hiện tại.
- Frontend hiện đang parse cả hai.

### 5. Update Reading Plan

```http
PUT /api/v1/books/{bookId}/reading-plan
```

Request:

```json
{
  "pace": 3,
  "schedule_config": ["Tue", "Thu"],
  "reminder_time": "21:00"
}
```

Rules:

- Nếu plan là `inactive`, update config mà không validate conflict.
- Nếu plan là `active`, validate conflict trước khi save.
- Conflict chỉ so với các plan khác đang `active`.

### 6. Start/Resume Plan

Dùng endpoint hiện có:

```http
POST /api/v1/books/{bookId}/resume
```

Behavior:

- Nếu plan là `inactive`: start plan, set `status=active`.
- Nếu plan đã được pause theo semantic backend hiện tại, nó cũng là `inactive`; resume bằng cách set `status=active`.
- Nếu plan đã `active`: idempotent success.
- Nếu không có plan: return `404`.
- Nếu book chưa `partial_ready` hoặc `ready`: return `409` hoặc `422` với `document_not_ready`.
- Validate conflict tại đây.
- Conflict chỉ check các plan khác đang `active`.

Current backend `resume_reading_plan(...)` đã gần đúng:

- đọc plan theo book
- validate schedule conflict
- set `PlanStatus.ACTIVE`
- tạo active slots

Điều chỉnh cần thêm:

- make active plan resume idempotent, hoặc giữ behavior hiện tại nếu nó đã harmless
- optional: reject resume khi book vẫn `draft`/`processing`
- return payload giàu hơn qua `_reading_plan_to_dict(...)`, không chỉ `{message, plan_id, status}`

Success response:

```json
{
  "book_id": "book_123",
  "plan_id": "plan_456",
  "status": "active",
  "plan_status": "active",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": [
    {
      "day": "Mon",
      "reminder_time": "20:00",
      "book_id": "book_123",
      "book_title": "Uploaded Document",
      "plan_id": "plan_456"
    }
  ],
  "message": "Reading plan started"
}
```

Conflict response:

```http
409 Conflict
```

```json
{
  "error": "schedule_conflict",
  "message": "Lịch học bị trùng với tài liệu đang hoạt động.",
  "conflicts": [
    {
      "day": "Mon",
      "reminder_time": "20:00",
      "book_id": "book_active",
      "book_title": "Existing Active Book",
      "plan_id": "plan_active"
    }
  ]
}
```

Document not ready response:

```http
409 Conflict
```

```json
{
  "error": "document_not_ready",
  "message": "Tài liệu chưa sẵn sàng để bắt đầu học.",
  "book_status": "processing"
}
```

### 7. Pause Plan

```http
POST /api/v1/books/{bookId}/pause
```

Behavior:

- Nếu plan là `active`, set `inactive`.
- Nếu đã `inactive`, idempotent success.
- Inactive plans không được xuất hiện trong active slots.

Response:

```json
{
  "book_id": "book_123",
  "plan_id": "plan_456",
  "status": "inactive",
  "plan_status": "inactive",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": [],
  "message": "Reading plan paused"
}
```

### 8. Processing Status

Endpoint hiện có:

```http
GET /api/v1/books/{bookId}/processing-status
GET /api/v1/jobs/{jobId}
```

Expected statuses:

- `queued`
- `processing`
- `partial_ready`
- `ready`
- `error`
- `cancelled`

Khi status chuyển thành `partial_ready` hoặc `ready`, frontend có thể hiện ready CTA nếu reading plan là `inactive`.

## Frontend Widget Contract

Widget:

```text
Tài liệu đã sẵn sàng
Bắt đầu học ngay
```

Show khi:

```text
book.status in ["partial_ready", "ready"]
AND reading_plan.status == "inactive"
```

Primary action:

```http
POST /api/v1/books/{bookId}/resume
```

Success behavior:

- Refresh user books / study data.
- Treat already active as success.
- Navigate tới `BookDetailPage` hoặc bắt đầu first playable unit, tùy quyết định UX.

Conflict behavior:

- Show conflict message.
- Offer edit schedule sheet.
- Không mark plan active ở local.

Not ready behavior:

- Giữ widget hidden nếu frontend đã biết `book.status=processing`.
- Nếu backend trả `document_not_ready`, show message nhẹ nhàng để user chờ/thử lại.

## Conflict Rules

Conflict validation chỉ được chạy khi plan trở thành active hoặc đang active:

- `POST /api/v1/generate-plan` với `activate=true`
- `POST /api/v1/books/{bookId}/resume`
- `PUT /api/v1/books/{bookId}/reading-plan` khi current plan là `active`

Conflict validation không được chạy cho:

- `POST /api/v1/upload`
- `POST /api/v1/generate-plan` với `activate=false`
- `PUT /api/v1/books/{bookId}/reading-plan` khi plan là `inactive`
- background processing job updates

## Recommended Status Flow

```text
upload
  -> book.status=draft

generate-plan activate=false
  -> book.status=processing
  -> reading_plan.status=inactive

job partial ready
  -> book.status=partial_ready
  -> reading_plan.status=inactive
  -> frontend shows ready CTA

user clicks "Bắt đầu học ngay"
  -> POST /books/{bookId}/resume
  -> reading_plan.status=active

job complete
  -> book.status=ready
  -> reading_plan.status remains active

pause
  -> reading_plan.status=inactive

resume
  -> reading_plan.status=active
```

## Acceptance Criteria

1. Uploading a document không bao giờ fail vì schedule conflict.
2. Generating a plan với `activate=false` không bao giờ fail vì schedule conflict.
3. Inactive plans được lưu và trả về bởi `GET /books/{bookId}/reading-plan`.
4. Inactive plans không được trả về bởi `GET /reading-plan-slots`.
5. Nhiều inactive plans có thể dùng cùng day/time.
6. `POST /books/{bookId}/resume` validate conflict against active plans.
7. `POST /books/{bookId}/resume` có thể activate một inactive plan.
8. `POST /books/{bookId}/resume` có thể resume một paused plan được đại diện bằng `inactive`.
9. `POST /books/{bookId}/resume` idempotent nếu plan đã active.
10. Frontend có thể xác định widget visibility từ `book.status` và reading plan status.

## Backend Implementation Notes

- Treat `generate-plan` sau upload là configure + process, không phải schedule activation.
- Add `activate` vào request schema.
- Default `activate=false` cho hành vi mới của app.
- Store plan status tách biệt với book processing status.
- Không reserve notification slots cho inactive plans.
- Theo backend hiện tại, "paused" nghĩa là `PlanStatus.INACTIVE`.
- Return stable machine-readable errors:
  - `schedule_conflict`
  - `document_not_ready`
  - `plan_not_found`
- Giữ response fields compatible với Flutter models hiện tại:
  - `book_id`
  - `plan_id`
  - `status`
  - `plan_status`
  - `pace`
  - `schedule_config`
  - `reminder_time`
  - `active_slots`
  - `message`

## Frontend Notes

Flutter hiện đã có các primitive:

- `RemoteBookRepository.generatePlan`
- `RemoteBookRepository.getReadingPlan`
- `RemoteBookRepository.getReadingPlanSlots`
- `RemoteBookRepository.pauseReadingPlan`
- `RemoteBookRepository.resumeReadingPlan`
- `GeneratePlanResult.planStatus`
- `ReadingPlanDetail.status`
- `ReadingPlanActionResult.isActive`
- `ReadingPlanActionResult.isPaused`

Frontend changes cần làm sau khi backend hỗ trợ:

- Gửi `activate=false` từ upload wizard.
- Không còn treat schedule conflict như một lỗi có thể xảy ra trong upload/configure flow.
- Thêm ready CTA widget ở Study và/hoặc Personal Documents.
- Khi CTA press, gọi `resumeReadingPlan(book.id)`.
- Nếu conflict, mở edit schedule sheet thay vì kéo user quay lại upload.
