# Phase 13 Implementation Guide - Calendar Session Actions And Learning Rounds

Date: 2026-06-12  
Status: Phase 13.1 backend implemented, Phase 13.2 optional  
Depends on:

- `_docs_implemented/phase_11_learning_progress_completion_state_implementation_guide.md`
- `_docs_implemented/phase_12_calendar_reading_plan_sessions_implementation_guide.md`
- `_docs_implemented/doc_setup_flutter/flutter_phase_12_calendar_reading_plan_contract.md`

---

## 0. Implementation Result

Implemented on 2026-06-12:

- Added calendar range endpoint:

```text
GET /api/v1/reading-plan/sessions
```

- Added session action endpoints:

```text
POST /api/v1/reading-plan/sessions/{session_id}/skip
PUT /api/v1/reading-plan/sessions/{session_id}/schedule
```

- Added missed-session notification support through existing `PLAN_REMINDER` with:

```json
{
  "subtype": "missed_session",
  "action_type": "open_plan_session"
}
```

- Added `reading_plan_sessions.missed_notified_at`.
- Kept Phase 12 endpoints backward compatible.
- Did not implement Phase 13.2 `BookLearningRound`; it remains optional.

Implemented files:

```text
app/api/v1/routers/reading_plan_sessions.py
app/schemas/plan.py
app/repositories/reading_plan_session_repo.py
app/services/reading_plan_session_service.py
app/services/notification_event_service.py
app/services/notification_copy_service.py
app/tasks/notification_tasks.py
app/models/db_models.py
app/core/exceptions.py
app/main.py
app/db/migrations/versions/a13f1e2d3c4b_phase_13_calendar_session_actions.py
tests/test_phase13_calendar_session_actions.py
```

Verification result:

```text
uv run alembic upgrade head
OK

uv run pytest tests/test_phase13_calendar_session_actions.py -q
4 passed

uv run pytest tests/test_phase12_calendar_plan_sessions.py -q
4 passed

uv run pytest tests/test_notifications_api.py tests/test_notification_outbox_repo.py -q
9 passed

uv run pytest tests/test_phase4_2_learning_loop.py -q
19 passed

uv run ruff check <changed runtime/test files>
All checks passed

uv run python -m py_compile <changed runtime files>
OK
```

---

## 1. Mục Tiêu

Phase 12 đã giải quyết phần cốt lõi:

```text
ReadingPlan -> sinh ra các buổi học cụ thể theo ngày, giờ, timezone.
Learning progress -> đồng bộ trạng thái session.
FE -> biết hôm nay học gì, lịch sắp tới là gì.
```

Phase 13 cần hoàn thiện vòng đời sử dụng thật:

```text
User có thể xem lịch theo tuần/tháng.
User có thể dời một buổi học.
User có thể bỏ qua một buổi học.
Hệ thống có thể nhắc khi user trễ lịch học.
Sách đã học xong có hướng "học lại" đúng, không phá progress cũ.
```

Mục tiêu kỹ thuật:

- Giữ API hiện tại không breaking.
- Không reset dữ liệu học cũ một cách mù.
- Không tạo notification trùng.
- Không để FE tự suy luận trạng thái lịch học.
- Tách router/service/repository sạch theo kiến trúc hiện tại.

---

## 2. Scope Chốt Cho Phase 13

### 2.1 Nên Implement Ngay

Phase 13.1:

- Calendar range endpoint cho FE xem lịch tuần/tháng.
- Skip session thủ công.
- Reschedule session thủ công.
- Missed-session notification.
- Better conflict response khi dời lịch bị trùng.

### 2.2 Nên Thiết Kế Kỹ Trước Khi Code

Phase 13.2:

- Learn again flow cho sách đã completed.
- Learning round để user học lại mà vẫn giữ lịch sử lần học trước.

Lý do tách 13.2:

- Schema hiện tại chỉ có một `LearningUnitProgress` cho mỗi user và learning unit.
- Nếu reset progress trực tiếp, hệ thống sẽ mất lịch sử học cũ.
- Spaced review đang dựa vào completion cũ. Reset bừa có thể làm review sai logic.

Recommendation của anh:

```text
Implement 13.1 trước.
Với "học lại", chỉ implement khi chấp nhận thêm khái niệm learning round.
Không làm quick fix kiểu xoá/reset progress cũ.
```

---

## 3. Business Logic Cần Đúng

### 3.1 Calendar Range

FE cần một API để lấy lịch theo khoảng ngày:

```text
Tuần này học gì?
Tháng này có những buổi nào?
Ngày nào bị trễ?
```

Không nên bắt FE gọi nhiều lần:

```text
GET /reading-plan/sessions/today
GET /books/{book_id}/reading-plan/sessions
```

Vì hai API hiện tại chỉ đủ cho Book Detail và Home Today.

### 3.2 Skip Session

Skip nghĩa là:

```text
User chủ động bỏ qua buổi học này.
```

Skip không có nghĩa là:

```text
User đã học xong nội dung.
```

Vì vậy khi skip:

- Không update `LearningUnitProgress` thành completed.
- Không tạo spaced review.
- Không tăng `book_progress_percent`.
- Không đánh dấu book completed.
- Chỉ chuyển session sang `skipped`.

### 3.3 Reschedule Session

Reschedule nghĩa là:

```text
Giữ nguyên các learning units trong session.
Chỉ đổi ngày, giờ học cụ thể.
```

Không regenerate toàn bộ plan khi user chỉ dời một buổi.

Ví dụ:

```text
Session 3: 2026-06-15 20:00
User đổi sang: 2026-06-16 21:00

=> chỉ update session 3.
=> không động tới sessions khác.
=> không đổi schedule_config weekly rule.
```

### 3.4 Missed Session

Missed nghĩa là:

```text
Buổi học đã qua giờ, user chưa hoàn thành đủ units.
```

Missed vẫn có thể học bù:

```text
missed -> user học tiếp -> completed
```

Do đó:

- Không khóa session missed.
- Không tự skip.
- Không xoá session.
- FE vẫn hiển thị CTA "Học bù" hoặc "Tiếp tục".

### 3.5 Manual Complete Session

Không nên thêm nút "complete session" chung trong Phase 13.

Lý do:

- Nếu user chưa nghe xong unit mà bấm complete session, progress sẽ bị sai.
- Spaced review sẽ được tạo sai thời điểm.
- Book completion sẽ không phản ánh hành vi học thật.

Flow đúng:

```text
User nghe audio
-> FE gửi progress
-> unit đạt threshold
-> backend complete learning unit
-> backend sync session unit
-> nếu toàn bộ unit trong session completed thì session completed
```

Nếu sau này cần nút "Đánh dấu đã học", nên implement như một explicit unit-level action:

```text
POST /books/{book_id}/learning-units/{learning_unit_id}/complete
```

Không complete cả session một cách gián tiếp.

---

## 4. API Contract Đề Xuất

Base URL:

```text
/api/v1
```

Tất cả endpoint cần auth bằng `CurrentUser`.

---

## 5. GET /reading-plan/sessions

### 5.1 Mục Đích

Lấy lịch học theo khoảng ngày cho calendar UI.

### 5.2 Request

```http
GET /api/v1/reading-plan/sessions?from_date=2026-06-01&to_date=2026-06-30
```

Optional query:

```text
book_id=uuid
mode=full|pareto
status=scheduled|due|in_progress|completed|missed|skipped
```

### 5.3 Response

Reuse `ReadingPlanSessionListResponse`, nhưng bổ sung metadata:

```json
{
  "book_id": null,
  "local_date": null,
  "timezone": "Asia/Ho_Chi_Minh",
  "from_date": "2026-06-01",
  "to_date": "2026-06-30",
  "total": 3,
  "items": [
    {
      "id": "session-id",
      "plan_id": "plan-id",
      "book_id": "book-id",
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
  ],
  "summary": {
    "scheduled": 1,
    "due": 0,
    "in_progress": 1,
    "completed": 0,
    "missed": 1,
    "skipped": 0
  }
}
```

### 5.4 Business Rules

- Query theo `user_id = current_user.sub`.
- Convert `from_date` và `to_date` theo timezone user.
- Trước khi trả response, chạy lazy missed evaluation cho user.
- Default range nếu FE không truyền:

```text
today - 7 days -> today + 30 days
```

Nhưng FE nên truyền rõ range để tránh response quá lớn.

### 5.5 Validation

- `from_date > to_date` -> 400.
- Range quá lớn, ví dụ hơn 120 ngày -> 400.
- `book_id` không thuộc user -> 404.
- `status` không hợp lệ -> 400.

---

## 6. POST /reading-plan/sessions/{session_id}/skip

### 6.1 Mục Đích

Cho user bỏ qua một buổi học.

### 6.2 Request

```http
POST /api/v1/reading-plan/sessions/{session_id}/skip
```

Optional body:

```json
{
  "reason": "busy"
}
```

`reason` có thể để phase sau, không bắt buộc.

### 6.3 Response

```json
{
  "message": "Đã bỏ qua buổi học.",
  "session": {
    "id": "session-id",
    "status": "skipped",
    "skipped_at": "2026-06-12T10:30:00Z"
  }
}
```

### 6.4 Business Rules

Cho phép skip nếu session đang:

```text
scheduled
due
in_progress
missed
```

Không cho skip nếu session đang:

```text
completed
skipped
cancelled
```

Nếu skip:

- Set `reading_plan_sessions.status = skipped`.
- Set `skipped_at = now`.
- Set `updated_at = now`.
- Với `reading_plan_session_units`:
  - Unit `pending` hoặc `in_progress` -> `skipped`.
  - Unit `completed` giữ nguyên.
- Không update `LearningUnitProgress`.
- Không tạo review item.

### 6.5 Error Cases

```text
404: session không tồn tại hoặc không thuộc user.
409: session đã completed/skipped/cancelled.
```

---

## 7. PUT /reading-plan/sessions/{session_id}/schedule

### 7.1 Mục Đích

Dời lịch một buổi học cụ thể.

### 7.2 Request

```json
{
  "local_date": "2026-06-16",
  "reminder_time": "21:00"
}
```

Optional:

```json
{
  "timezone": "Asia/Ho_Chi_Minh"
}
```

Nếu FE không gửi timezone, backend dùng:

1. timezone hiện tại của session;
2. nếu session thiếu timezone, dùng `notification_settings.timezone`;
3. fallback cuối cùng: `Asia/Ho_Chi_Minh`.

### 7.3 Response

```json
{
  "message": "Đã dời lịch buổi học.",
  "session": {
    "id": "session-id",
    "scheduled_at": "2026-06-16T14:00:00Z",
    "local_date": "2026-06-16",
    "reminder_time": "21:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "status": "scheduled"
  }
}
```

### 7.4 Business Rules

Cho phép reschedule nếu session đang:

```text
scheduled
due
in_progress
missed
```

Không cho reschedule nếu:

```text
completed
skipped
cancelled
```

Khi reschedule:

- Convert local date/time sang UTC `scheduled_at`.
- Update `local_date`, `reminder_time`, `timezone`.
- Nếu session đang `missed` và giờ mới ở tương lai:
  - set status về `scheduled` nếu chưa started;
  - giữ `in_progress` nếu đã started hoặc có unit in_progress;
  - clear `missed_at`.
- Nếu giờ mới đã đến hoặc đã qua:
  - status có thể là `due` hoặc `missed` theo lazy evaluation.

### 7.5 Conflict Rule

Không cho hai session active của cùng user trùng cùng thời điểm.

Active statuses:

```text
scheduled
due
in_progress
missed
```

Final statuses:

```text
completed
skipped
cancelled
```

Conflict check:

```text
same user_id
same scheduled_at
status not in completed/skipped/cancelled
id != current_session_id
```

Nếu conflict:

```json
{
  "detail": "Lịch học bị trùng với sách \"Tên sách\" vào 21:00 ngày 2026-06-16."
}
```

---

## 8. Missed Session Notification

### 8.1 Mục Đích

Khi user bỏ lỡ một buổi học, hệ thống nên tạo thông báo nhẹ:

```text
Bạn đã lỡ buổi học của sách X. Có thể học bù khi rảnh.
```

Không nên spam nhiều lần cho cùng một session.

### 8.2 Notification Type

Có hai cách.

#### Option A - Thêm NotificationType mới

```python
class NotificationType(str, Enum):
    PLAN_REMINDER = "plan_reminder"
    CONTENT_READY = "content_ready"
    SPACED_REVIEW_DUE = "spaced_review_due"
    MISSED_PLAN_SESSION = "missed_plan_session"
```

Ưu điểm:

- Rõ business.
- FE dễ render icon/message theo loại.
- Dễ đo analytics.

Nhược điểm:

- Cần migration enum Postgres nếu đang dùng native enum.

#### Option B - Reuse PLAN_REMINDER Với Payload Subtype

```json
{
  "type": "plan_reminder",
  "payload": {
    "subtype": "missed_session"
  }
}
```

Ưu điểm:

- Ít migration.
- Ít rủi ro enum.

Nhược điểm:

- Business type kém rõ.
- FE phải đọc payload để phân biệt.

Recommendation:

```text
Chọn Option A nếu migration enum hiện tại ổn.
Chọn Option B nếu muốn deploy ít rủi ro trước deadline.
```

Với capstone production ổn định, anh nghiêng về Option A.

### 8.3 Data Model Bổ Sung

Thêm field vào `ReadingPlanSession`:

```python
missed_notified_at: datetime | None = None
```

Lý do:

- Dễ debug session này đã từng được nhắc trễ chưa.
- Không chỉ dựa vào outbox idempotency.

Migration:

```text
ALTER TABLE reading_plan_sessions
ADD COLUMN missed_notified_at TIMESTAMPTZ NULL;
```

Index không bắt buộc ở Phase 13.

### 8.4 Idempotency Key

```text
missed-session:{user_id}:{session_id}
```

Nếu outbox đã có key này:

- Không tạo thêm.
- Không gửi lại.

### 8.5 Scanner Flow

Current flow:

```text
Celery Beat
-> triam.notifications.scan_due
-> create due reminder/review outbox
-> mark_due_sessions_missed
```

Phase 13 flow:

```text
Celery Beat
-> triam.notifications.scan_due
-> mark overdue sessions missed, return newly missed sessions
-> create missed-session outbox once
-> create due reminder/review outbox
-> deliver due outbox
```

Lưu ý:

- Mark missed trước.
- Chỉ tạo missed notification cho sessions mới chuyển sang missed.
- Không gửi missed notification nếu user đã học book đó trong cùng local day sau lịch học.
- Tôn trọng quiet hours và daily cap hiện tại.

---

## 9. Learn Again Flow

### 9.1 Vấn Đề Hiện Tại

Khi book đã completed, FE có thể muốn hiển thị:

```text
Học lại
Ôn lại
Nghe lại từ đầu
```

Nhưng các hành động này không giống nhau.

### 9.2 Phân Biệt 3 Hành Động

#### Nghe Lại

User nghe lại audio đã có.

Backend không cần reset progress.

```text
Use existing learning units and segments.
Do not create new plan.
Do not reset progress.
```

#### Ôn Lại

User mở review items đã được tạo sau completion.

Backend dùng spaced review hiện tại.

```text
GET review list
POST complete/skip review
```

#### Học Lại

User muốn bắt đầu một vòng học mới, có lịch mới, tiến độ mới.

Đây là case cần thiết kế thêm `learning round`.

### 9.3 Vì Sao Không Reset Progress Cũ

Không nên làm:

```text
DELETE learning_unit_progress
UPDATE book_learning_states SET status='not_started'
```

Vì:

- Mất lịch sử học.
- `spaced_review_items.source_unit_progress_id` có thể trở nên sai nghĩa.
- Completion cũ không còn đáng tin.
- Capstone báo cáo khó giải thích.

### 9.4 Data Model Đề Xuất Cho Learning Round

Thêm bảng:

```python
class BookLearningRound(SQLModel, table=True):
    __tablename__ = "book_learning_rounds"

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    mode: PlanMode
    round_index: int
    status: str  # active, completed, cancelled
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
```

Bổ sung `round_id` vào:

```text
learning_unit_progress
book_learning_states
reading_plans
reading_plan_sessions
reading_plan_session_units
spaced_review_items
```

Update unique constraints:

```text
learning_unit_progress:
  old: unique(user_id, learning_unit_id)
  new: unique(user_id, round_id, learning_unit_id)

book_learning_states:
  old: unique(user_id, book_id, mode)
  new: unique(user_id, book_id, mode, round_id)
```

### 9.5 API Đề Xuất Cho Học Lại

```http
POST /api/v1/books/{book_id}/learning-rounds
```

Request:

```json
{
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "start_date": "2026-06-15"
}
```

Response:

```json
{
  "message": "Đã tạo vòng học mới.",
  "round_id": "round-id",
  "plan_id": "plan-id",
  "book_id": "book-id",
  "mode": "pareto",
  "status": "active"
}
```

### 9.6 Recommendation Cho Phase 13

Nếu deadline gần:

```text
Phase 13.1 chỉ làm calendar actions và missed notification.
Learn again chỉ document, chưa code.
FE dùng "Nghe lại" và "Ôn lại" trước.
```

Nếu còn thời gian:

```text
Phase 13.2 implement BookLearningRound.
```

Không làm giải pháp reset progress thô.

---

## 10. File Implement Dự Kiến

### 10.1 Constants

File:

```text
app/core/constant.py
```

Add nếu chọn Option A:

```python
class NotificationType(str, Enum):
    MISSED_PLAN_SESSION = "missed_plan_session"
```

Không cần thêm session status mới vì hiện đã có:

```text
scheduled
due
in_progress
completed
missed
skipped
cancelled
```

### 10.2 Models

File:

```text
app/models/db_models.py
```

Add:

```python
missed_notified_at: Optional[datetime] = Field(
    default=None,
    sa_column=Column(DateTime(timezone=True)),
)
```

Nếu implement learning round:

```text
BookLearningRound
round_id columns
new unique constraints
```

Nhưng learning round nên làm sau 13.1.

### 10.3 Schemas

File:

```text
app/schemas/plan.py
```

Add:

```python
class ReadingPlanSessionRangeResponse(ReadingPlanSessionListResponse):
    from_date: date
    to_date: date
    summary: dict[str, int] = Field(default_factory=dict)


class ReadingPlanSessionSkipRequest(BaseModel):
    reason: str | None = None


class ReadingPlanSessionRescheduleRequest(BaseModel):
    local_date: date
    reminder_time: str
    timezone: str | None = None


class ReadingPlanSessionActionResponse(BaseModel):
    message: str
    session: ReadingPlanSessionResponse
```

Validate `reminder_time` bằng helper chung, không lặp regex ở nhiều nơi.

### 10.4 Repository

File:

```text
app/repositories/reading_plan_session_repo.py
```

Add functions:

```python
def get_owned_session(session: Session, *, user_id: uuid.UUID, session_id: uuid.UUID) -> ReadingPlanSession | None:
    ...


def list_sessions_for_user_range(
    session: Session,
    *,
    user_id: uuid.UUID,
    from_local_date: str,
    to_local_date: str,
    book_id: uuid.UUID | None = None,
    mode: PlanMode | None = None,
    status: str | None = None,
) -> list[ReadingPlanSession]:
    ...


def find_session_schedule_conflict(
    session: Session,
    *,
    user_id: uuid.UUID,
    scheduled_at: datetime,
    exclude_session_id: uuid.UUID,
) -> ReadingPlanSession | None:
    ...
```

Repository chỉ query/mutate DB. Không convert timezone trong repo.

### 10.5 Service

File:

```text
app/services/reading_plan_session_service.py
```

Add functions:

```python
def list_reading_plan_sessions_range(...):
    ...


def skip_reading_plan_session(...):
    ...


def reschedule_reading_plan_session(...):
    ...


def mark_due_sessions_missed(...):
    # update để return list newly_missed_sessions thay vì chỉ count nếu cần notification
```

Service chịu trách nhiệm:

- Auth ownership đã có từ repo query user_id.
- Validate status transition.
- Convert local date/time sang UTC.
- Check conflict.
- Recalculate response.
- Commit transaction một lần.

### 10.6 Router

Recommendation: tạo router mới để không làm `audiobooks.py` quá lớn.

File mới:

```text
app/api/v1/routers/reading_plan_sessions.py
```

Routes:

```python
@router.get("/reading-plan/sessions", response_model=ReadingPlanSessionRangeResponse)
def get_reading_plan_sessions(...):
    ...


@router.post("/reading-plan/sessions/{session_id}/skip", response_model=ReadingPlanSessionActionResponse)
def skip_reading_plan_session_endpoint(...):
    ...


@router.put("/reading-plan/sessions/{session_id}/schedule", response_model=ReadingPlanSessionActionResponse)
def reschedule_reading_plan_session_endpoint(...):
    ...
```

Sau đó include router trong:

```text
app/main.py hoặc router aggregator hiện tại
```

Không xoá endpoints Phase 12 trong `audiobooks.py`.

### 10.7 Notification Services

Files:

```text
app/services/notification_event_service.py
app/tasks/notification_tasks.py
```

Add:

```python
def create_missed_plan_session_outbox_rows(session: Session, *, now: datetime) -> int:
    ...
```

Update scan task:

```python
missed_count = mark_due_sessions_missed(...)
created_count += create_missed_plan_session_outbox_rows(...)
```

Better implementation:

```text
mark_due_sessions_missed returns newly missed sessions.
create missed outbox only from newly missed sessions.
```

### 10.8 Notification Copy

Nếu có file copy riêng, add template:

```text
Title: Bạn đã lỡ một buổi học
Body: Sách "{book_title}" vẫn có thể học bù khi bạn rảnh.
```

Payload:

```json
{
  "action_type": "open_plan_session",
  "book_id": "...",
  "plan_id": "...",
  "session_id": "...",
  "mode": "pareto",
  "local_date": "2026-06-12"
}
```

---

## 11. Alembic Migration

Phase 13.1 migration:

```text
add missed_notified_at to reading_plan_sessions
optional add notification enum value MISSED_PLAN_SESSION
```

Postgres enum migration example:

```python
op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'MISSED_PLAN_SESSION'")
```

Lưu ý:

- Check tên enum thật trong DB trước khi viết migration.
- Nếu enum value đang lưu lowercase vì Python enum value, cần kiểm tra Alembic/autogen hiện tại.
- Không autogenerate mù với enum. Đọc migration trước khi chạy.

Phase 13.2 migration nếu làm learning round:

```text
create book_learning_rounds
add nullable round_id columns
backfill default round for existing progress
change unique constraints
```

Không nên làm 13.2 nếu chưa có thời gian test kỹ.

---

## 12. Testing Plan

### 12.1 Unit/Service Tests

File đề xuất:

```text
tests/test_phase13_calendar_session_actions.py
```

Cases:

1. Range endpoint returns only current user's sessions.
2. Range endpoint respects from_date/to_date.
3. Range endpoint filters by book_id/mode/status.
4. Skip scheduled session -> status skipped.
5. Skip completed session -> 409.
6. Skip session does not update learning progress.
7. Reschedule scheduled session -> updates scheduled_at/local_date/reminder_time.
8. Reschedule missed future -> clears missed_at and status becomes scheduled.
9. Reschedule conflict -> 409 with useful message.
10. Other user cannot skip/reschedule session -> 404.

### 12.2 Notification Tests

File đề xuất:

```text
tests/test_phase13_missed_session_notifications.py
```

Cases:

1. Overdue session becomes missed.
2. Newly missed session creates one outbox row.
3. Running scanner twice does not create duplicate outbox.
4. Completed session never gets missed notification.
5. Skipped session never gets missed notification.
6. Quiet hours/daily cap still apply.

### 12.3 Regression Tests

Run existing:

```powershell
uv run pytest tests/test_phase12_calendar_plan_sessions.py -q
uv run pytest tests/test_phase4_2_learning_loop.py -q
uv run pytest tests/test_notifications_api.py tests/test_notification_outbox_repo.py -q
```

Then:

```powershell
uv run ruff check app tests
uv run python -m py_compile app/core/constant.py app/models/db_models.py app/schemas/plan.py app/services/reading_plan_session_service.py
```

---

## 13. Manual Test Flow

### 13.1 Calendar Range

1. Upload book.
2. Generate plan with `activate=true`.
3. Call:

```http
GET /api/v1/reading-plan/sessions?from_date=2026-06-01&to_date=2026-06-30
```

Expected:

- Response contains sessions for this user only.
- `summary` count matches items.
- FE can render month calendar.

### 13.2 Skip

1. Pick a scheduled session.
2. Call:

```http
POST /api/v1/reading-plan/sessions/{session_id}/skip
```

Expected:

- Session status becomes `skipped`.
- Book progress does not change.
- Unit progress does not become completed.

### 13.3 Reschedule

1. Pick a scheduled/missed session.
2. Call:

```http
PUT /api/v1/reading-plan/sessions/{session_id}/schedule
```

Expected:

- Same session ID.
- Same units.
- New date/time.
- No full plan regeneration.

### 13.4 Missed Notification

1. Create session in the past.
2. Run notification scanner.
3. Check:

```text
reading_plan_sessions.status = missed
notification_outbox has one missed-session row
user_notifications receives one item after deliver
```

Run scanner again.

Expected:

```text
No duplicate notification.
```

---

## 14. FE Impact

Sau Phase 13.1, cần viết thêm FE contract:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_13_calendar_session_actions_contract.md
```

FE cần update:

- Calendar screen dùng `GET /reading-plan/sessions`.
- Session card có action:
  - Dời lịch.
  - Bỏ qua.
  - Học bù nếu missed.
- Notification click mở đúng session.
- Không dùng `POST /generate-plan` để dời một buổi học.
- Không tự complete session từ UI nếu backend chưa có explicit unit completion.

---

## 15. Trade-Offs

### 15.1 Lazy GET Có Ghi DB

Range endpoint nên chạy lazy missed evaluation.

Trade-off:

- GET không còn thuần read-only.

Lý do chấp nhận:

- FE luôn thấy trạng thái đúng.
- Hugging Face free có thể sleep, Celery Beat có thể delay.
- Write nhỏ, scoped theo user.

### 15.2 Skip Không Tự Rebalance Plan

Khi skip một session, các unit trong session không tự chuyển sang ngày khác.

Trade-off:

- User có thể bỏ qua một nội dung.

Lý do chấp nhận:

- Skip nghĩa là bỏ qua.
- Nếu user muốn học bù, dùng reschedule thay vì skip.

Phase sau có thể thêm:

```text
Skip and reassign units
```

nhưng không nên làm mặc định.

### 15.3 Reschedule Một Session Có Thể Lệch Weekly Rule

Ví dụ plan học Mon/Wed/Fri, user dời một session sang Tuesday.

Điều này chấp nhận được vì:

- Đây là override thủ công cho một buổi cụ thể.
- Weekly rule vẫn giữ cho các buổi tương lai khác.

FE nên hiển thị:

```text
Buổi này đã được dời lịch riêng.
```

Nếu muốn hiển thị chính xác hơn, phase sau có thể thêm field:

```text
is_manual_override
rescheduled_from
```

Không bắt buộc Phase 13.1.

### 15.4 Learn Again Là Scope Lớn

Learning round là hướng đúng nhưng ảnh hưởng nhiều bảng.

Recommendation:

```text
Không nhét learning round vào cùng PR với skip/reschedule.
```

---

## 16. Implementation Order

### Step 1 - Schema nhỏ cho Phase 13.1

- Add `missed_notified_at`.
- Add notification type nếu chọn Option A.
- Create Alembic migration.

### Step 2 - DTO

- Add range response.
- Add skip request.
- Add reschedule request.
- Add action response.

### Step 3 - Repository

- Add owned session query.
- Add range query.
- Add conflict query.

### Step 4 - Service

- Implement list range.
- Implement skip.
- Implement reschedule.
- Update missed marking to return newly missed sessions if needed.

### Step 5 - Router

- Add `reading_plan_sessions.py`.
- Include router.
- Keep old routes.

### Step 6 - Notification

- Add missed-session outbox creation.
- Update scanner.
- Add idempotency key.

### Step 7 - Tests

- Add Phase 13 tests.
- Run Phase 12 regression.
- Run notification regression.

### Step 8 - FE Contract

- Create Flutter Phase 13 contract.

---

## 17. Definition Of Done

Phase 13.1 complete khi:

- FE có API xem lịch theo khoảng ngày.
- User có thể dời một session mà không regenerate toàn plan.
- User có thể skip một session mà không làm sai progress.
- Missed sessions có thể tạo notification một lần.
- Scanner chạy idempotent.
- Auth isolation đúng.
- Existing Phase 11/12 APIs không breaking.
- Tests pass.

Phase 13.2 complete khi:

- Có `BookLearningRound`.
- User có thể học lại sách mà không mất lịch sử cũ.
- Progress, reading plan, sessions, reviews phân biệt được round.
- FE biết current active round.
- Existing books được backfill round mặc định an toàn.

---

## 18. Recommendation Cuối

Anh recommend implement theo thứ tự:

```text
Phase 13.1: Calendar range, skip, reschedule, missed notification.
Phase 13.2: Learning round cho học lại.
```

Không nên implement quick reset progress cho "học lại".

Đây là điểm khác nhau giữa app demo và app có logic học tập thật: hệ thống phải giữ lịch sử học cũ, lịch ôn tập cũ, và tạo vòng học mới có danh tính riêng nếu user muốn học lại từ đầu.
