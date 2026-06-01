# Phase 7.2 Implementation Guide - Deferred Reading Plan Activation

## 1. Mục Tiêu

Phase này sửa lại business flow upload/generate-plan để đúng trải nghiệm sản phẩm thật:

```text
Upload tài liệu
-> cấu hình kế hoạch học
-> backend generate nội dung/audio trong background
-> tài liệu sẵn sàng
-> user bấm "Bắt đầu học"
-> lúc này mới activate lịch học và kiểm tra trùng lịch
```

Vấn đề hiện tại:

- `POST /api/v1/generate-plan` đang tạo `ReadingPlan` ở trạng thái `active`.
- Backend đang validate trùng lịch ngay trong bước generate-plan.
- User mới chỉ upload và cấu hình ban đầu nhưng đã có thể bị chặn bởi `409 schedule_conflict`.
- Điều này làm FE cảm giác "upload fail", dù lỗi thật ra nằm ở lịch học.

Mục tiêu sau phase này:

- Upload/configure không fail vì trùng lịch.
- Inactive reading plan không chiếm lịch.
- Conflict chỉ xảy ra khi user thật sự start/resume plan.
- FE có thể show CTA "Tài liệu đã sẵn sàng - Bắt đầu học ngay".

## 2. Phạm Vi Chốt

Implement theo core recommendation, không bê toàn bộ FE spec vào một lần.

### Implement ngay

- Thêm `activate` vào `PlanInput`.
- `activate=false` tạo plan `inactive`, không tạo active schedule slots.
- `activate=false` không validate conflict và không validate active learning capacity.
- `activate=true` giữ flow active hiện tại.
- `POST /books/{book_id}/resume` là điểm activate/start chính thức.
- `resume` validate conflict trước khi active plan.
- `resume` idempotent nếu plan đã active.
- `PUT /books/{book_id}/reading-plan`:
  - plan inactive: update config, chỉ validate shape.
  - plan active: validate conflict, delete slots cũ, tạo slots mới.
- Response thêm `plan_status` ở các action reading plan.
- Update Flutter contract doc.
- Thêm regression tests.

### Chưa implement trong phase này

- Không thêm `PlanStatus.COMPLETED`.
- Không thêm `PlanStatus.PAUSED`.
- Không đổi global error response sang `{error, message, conflicts}`.
- Không trả conflict list có `book_title`.
- Không thêm migration DB.

Lý do:

- Các phần trên tốt cho phase sau, nhưng không cần để sửa lỗi upload/configure flow.
- Đổi error contract toàn app có thể làm FE vỡ.
- Hiện `inactive` đủ đại diện cho cả "chưa bắt đầu" và "đã pause".

## 3. Business Logic Chuẩn Sau Phase Này

### 3.1 Book status

```text
draft         Upload xong, chưa generate plan
processing    Đang generate audio/content
partial_ready Có nội dung đầu tiên, user có thể bắt đầu học
ready         Xử lý xong toàn bộ
error         Xử lý lỗi
```

### 3.2 ReadingPlan status

```text
inactive  Đã cấu hình nhưng chưa active, hoặc user đã pause
active    Đang tham gia lịch học/reminder
error     Plan lỗi
```

### 3.3 Active schedule slots

`reading_plan_schedule_slots` chỉ đại diện cho lịch đang active.

```text
plan inactive -> không có active slot
plan active   -> có active slots theo schedule_config + reminder_time
```

Nhiều inactive plans được phép trùng ngày/giờ.

## 4. API Contract

### 4.1 POST /api/v1/generate-plan

Request mới:

```json
{
  "book_id": "uuid",
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "activate": false
}
```

Rules:

- `activate` optional.
- Recommended default backend: `false`.
- `reminder_time` vẫn optional để không breaking change.
- Nếu `reminder_time` thiếu, backend fallback từ notification settings.

Behavior `activate=false`:

```text
validate book exists and status=draft
validate schedule shape only
create ReadingPlan(status=inactive)
do not validate schedule conflict
do not validate active learning capacity
do not create ReadingPlanScheduleSlot rows
create ProcessingJob(status=queued)
set Book.status=processing
enqueue Celery document job
return active_slots=[]
```

Response:

```json
{
  "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
  "book_id": "uuid",
  "plan_id": "uuid",
  "job_id": "uuid",
  "mode": "pareto",
  "status": "queued",
  "plan_status": "inactive",
  "progress_percent": 0,
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": [],
  "planned_units": []
}
```

Behavior `activate=true`:

```text
validate schedule shape
validate active learning capacity
validate conflict against active slots
create ReadingPlan(status=active)
create active slots
enqueue job
```

This mode preserves the old behavior for clients that explicitly want immediate activation.

### 4.2 GET /api/v1/reading-plan-slots

Existing endpoint remains.

Rule:

- Return only slots from active plans.
- Inactive configured plans must not appear.

### 4.3 GET /api/v1/books/{book_id}/reading-plan

Existing endpoint remains.

Recommended response should include both `status` and `plan_status`:

```json
{
  "book_id": "uuid",
  "plan_id": "uuid",
  "status": "inactive",
  "plan_status": "inactive",
  "mode": "full",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "active_slots": []
}
```

Reason:

- `status` is existing field in current response.
- `plan_status` makes FE code clearer and matches generate-plan response.

### 4.4 PUT /api/v1/books/{book_id}/reading-plan

Request remains backward compatible:

```json
{
  "pace": 3,
  "schedule_config": ["Tue", "Thu"],
  "reminder_time": "21:00"
}
```

All fields stay optional.

Behavior:

```text
if current plan inactive:
  keep omitted fields from current plan
  validate shape only
  update plan config
  active_slots remains []

if current plan active:
  keep omitted fields from current plan
  validate shape
  validate conflict excluding current plan
  delete current slots
  create new active slots
  update plan config
```

### 4.5 POST /api/v1/books/{book_id}/resume

This becomes the official start/activate action.

Behavior:

```text
load owned book
load reading plan

if plan active:
  return success with current reading plan

if book status not in partial_ready/ready:
  return 409 document not ready

validate schedule shape
validate active learning capacity
validate conflict against active slots
set plan.status=active
create active slots
commit
return full reading plan response
```

Document not ready guard:

- This is recommended even if FE hides CTA during `processing`.
- Backend should still protect business state.

Suggested user-facing message:

```text
Tài liệu chưa sẵn sàng để bắt đầu học. Vui lòng chờ hệ thống xử lý thêm.
```

### 4.6 POST /api/v1/books/{book_id}/pause

Behavior:

```text
if plan active:
  delete active slots
  set status=inactive

if already inactive:
  idempotent success

return full reading plan response with active_slots=[]
```

## 5. Implementation Patch Points

### 5.1 app/schemas/plan.py

Add:

```python
class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int
    schedule_config: list[str]
    reminder_time: str | None = None
    activate: bool = False
```

Keep:

```python
class PlanUpdateRequest(BaseModel):
    pace: int | None = None
    schedule_config: list[str] | None = None
    reminder_time: str | None = None
```

Add `plan_status` to response DTOs if possible:

```python
class ReadingPlanResponse(BaseModel):
    status: str
    plan_status: str
```

Implementation detail:

- `plan_status` can mirror `status`.
- This is non-breaking because existing `status` remains.

### 5.2 app/services/reading_plan_schedule_service.py

Current function mixes shape validation + activation validation.

Add config-only helper:

```python
def validate_plan_schedule_shape(
    session: Session,
    *,
    user_id: uuid.UUID,
    schedule_config: object,
    reminder_time: str | None = None,
) -> list[ScheduleSlotInput]:
    user_settings = get_or_create_notification_settings(session, user_id)
    resolved_reminder_time = reminder_time or user_settings.reminder_time
    return normalize_schedule_config(
        schedule_config,
        reminder_time=resolved_reminder_time,
        timezone_name=user_settings.timezone,
    )
```

Keep activation helper:

```python
def validate_plan_schedule_for_activation(...):
    slots = validate_plan_schedule_shape(...)
    if exclude_plan_id is None:
        validate_active_learning_capacity(...)
    validate_schedule_slots_available(...)
    return slots
```

Backward compatibility:

- Existing `validate_plan_schedule_for_create` can remain as alias/wrapper to reduce code churn.

Recommended naming:

```python
validate_plan_schedule_shape
validate_plan_schedule_for_activation
```

### 5.3 app/services/upload_service.py

Refactor `_create_plan_and_job`:

```python
def _create_plan_and_job(..., plan_status: PlanStatus, slots: list[ScheduleSlotInput]):
    plan = ReadingPlan(
        status=plan_status.value,
        ...
    )

    if plan_status == PlanStatus.ACTIVE:
        for slot in build_slots_for_plan(...):
            session.add(slot)
```

In `handle_generate_plan`:

```python
if payload.activate:
    slots = validate_plan_schedule_for_activation(...)
    plan_status = PlanStatus.ACTIVE
else:
    slots = validate_plan_schedule_shape(...)
    plan_status = PlanStatus.INACTIVE
    active_slots_to_create = []
```

Response:

```python
"plan_status": plan.status,
"active_slots": [] if plan.status == PlanStatus.INACTIVE.value else ...
```

Important:

- `resolved_reminder_time = slots[0].reminder_time`
- Do not use raw `payload.reminder_time` because it may be `None`.

### 5.4 app/services/audiobook_service.py

#### `_reading_plan_to_dict`

Return:

```python
{
    "status": plan.status,
    "plan_status": plan.status,
}
```

#### `pause_reading_plan`

Make idempotent and return full response:

```python
if plan.status == PlanStatus.ACTIVE.value:
    delete_slots_for_plan(session, plan_id=plan.id)
    plan.status = PlanStatus.INACTIVE.value
    session.commit()

return {"message": "Đã tạm dừng kế hoạch học tập.", **_reading_plan_to_dict(session, plan)}
```

#### `resume_reading_plan`

Make idempotent:

```python
if plan.status == PlanStatus.ACTIVE.value:
    return {"message": "Kế hoạch học tập đang hoạt động.", **_reading_plan_to_dict(session, plan)}
```

Add document readiness guard:

```python
if book.status not in (BookStatus.PARTIAL_READY.value, BookStatus.READY.value):
    raise BookStatusConflictError("Tài liệu chưa sẵn sàng để bắt đầu học. Vui lòng chờ hệ thống xử lý thêm.")
```

Then validate activation:

```python
slots = validate_plan_schedule_for_activation(...)
plan.status = PlanStatus.ACTIVE.value
delete_slots_for_plan(session, plan_id=plan.id)
add build_slots_for_plan(...)
commit
```

#### `update_reading_plan`

Branch by current plan status:

```python
if plan.status == PlanStatus.ACTIVE.value:
    slots = validate_plan_schedule_for_activation(..., exclude_plan_id=plan.id)
    delete old slots
    create new slots
else:
    validate_plan_schedule_shape(...)
```

### 5.5 app/repositories/reading_plan_schedule_repo.py

Keep hard delete.

Important:

- Repository must not commit for multi-step service flow.
- Current recommended function:

```python
def delete_slots_for_plan(session: Session, *, plan_id: uuid.UUID) -> int:
    result = session.exec(
        delete(ReadingPlanScheduleSlot).where(
            ReadingPlanScheduleSlot.plan_id == plan_id
        )
    )
    return int(result.rowcount or 0)
```

## 6. Test Plan

### 6.1 Generate plan inactive does not conflict

Setup:

- User has active book A with slot Mon 20:00.
- Upload/create draft book B.

Action:

```http
POST /generate-plan
{
  "book_id": "book-b",
  "mode": "full",
  "pace": 1,
  "schedule_config": ["Mon"],
  "reminder_time": "20:00",
  "activate": false
}
```

Expected:

```text
200
plan_status=inactive
active_slots=[]
book B status=processing
```

### 6.2 Multiple inactive plans may share same slot

Create book B and book C with same schedule and `activate=false`.

Expected:

```text
both succeed
GET /reading-plan-slots returns only active book A
```

### 6.3 Resume inactive plan detects conflict

Setup:

- book A active Mon 20:00.
- book B inactive Mon 20:00.
- book B status partial_ready or ready.

Action:

```http
POST /books/{book_b}/resume
```

Expected:

```text
409 schedule conflict
book B remains inactive
no active slot for book B
```

### 6.4 Resume inactive plan success

Setup:

- book B inactive Tue 21:00.
- book B status partial_ready.

Expected:

```text
200
plan_status=active
active_slots contains Tue 21:00
```

### 6.5 Resume active plan idempotent

Action:

```http
POST /books/{active_book}/resume
```

Expected:

```text
200
does not duplicate slots
```

### 6.6 Resume processing book rejected

Setup:

- book status processing.
- plan inactive.

Expected:

```text
409
message: tài liệu chưa sẵn sàng
plan remains inactive
```

### 6.7 Update inactive plan does not conflict

Setup:

- book A active Mon 20:00.
- book B inactive Tue 21:00.

Action:

```http
PUT /books/{book_b}/reading-plan
{
  "schedule_config": ["Mon"],
  "reminder_time": "20:00"
}
```

Expected:

```text
200
book B remains inactive
active_slots=[]
no conflict
```

### 6.8 Update active plan still conflicts

Setup:

- book A active Mon 20:00.
- book B active Tue 21:00.

Action:

```http
PUT /books/{book_b}/reading-plan
{
  "schedule_config": ["Mon"],
  "reminder_time": "20:00"
}
```

Expected:

```text
409
book B old slot remains valid or transaction rolls back
```

## 7. Flutter Contract Update

Update:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md
```

Add:

- `activate` in `POST /generate-plan`.
- FE upload wizard should send `activate=false`.
- Generate-plan schedule conflict should no longer happen when `activate=false`.
- Ready CTA visible when:

```text
book.status in ["partial_ready", "ready"]
AND reading_plan.plan_status == "inactive"
```

- CTA action:

```http
POST /api/v1/books/{book_id}/resume
```

- If resume returns conflict, open edit schedule sheet.

## 8. Rollout Recommendation

Recommended backend default:

```python
activate: bool = False
```

Reason:

- This matches new product logic.
- FE explicitly asked for deferred upload flow.
- Existing clients that do not send `activate` will receive new behavior. This is a semantic change, but it fixes the current broken UX.

Alternative safer rollout:

```python
activate: bool | None = None
```

Then resolve with config flag:

```text
READING_PLAN_ACTIVATE_ON_GENERATE_DEFAULT=false
```

This is more flexible but adds config complexity. For current capstone scope, default `false` is acceptable once FE is aligned.

## 9. Trade-Offs

### Pros

- Upload/configure flow becomes clean.
- User can prepare many books without schedule conflict.
- Conflict appears at the correct moment: when user starts learning.
- `reading_plan_schedule_slots` stays a clean active-schedule projection.
- No DB migration required.

### Cons

- Existing clients may expect `generate-plan` to immediately activate plan.
- `inactive` now has two meanings: not started and paused.
- Notifications/reminders only work after resume/start.

Why acceptable:

- FE already wants this new flow.
- Product UX is better.
- `inactive` dual meaning is acceptable until a later phase adds `paused`.

## 10. Completion Checklist

- [x] `PlanInput.activate` added.
- [x] `generate-plan activate=false` creates inactive plan.
- [x] `generate-plan activate=false` does not create active slots.
- [x] `generate-plan activate=false` does not validate conflict/capacity.
- [x] `generate-plan activate=true` still validates conflict/capacity.
- [x] `resume` checks document readiness.
- [x] `resume` is idempotent for active plan.
- [x] `resume` activates inactive plan with slots.
- [x] `pause` is idempotent and returns full plan response.
- [x] `update inactive` validates shape only.
- [x] `update active` validates conflict and updates slots atomically.
- [x] FE contract doc updated.
- [x] Focused tests pass.
- [x] Ruff and py_compile pass.

## 11. Implementation Verification

Implemented in this phase:

- `app/schemas/plan.py`
- `app/services/reading_plan_schedule_service.py`
- `app/services/upload_service.py`
- `app/services/audiobook_service.py`
- `tests/test_celery_enqueue.py`
- `tests/test_phase4_2_learning_loop.py`
- `_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md`

Verification commands:

```powershell
uv run ruff check app\schemas\plan.py app\services\reading_plan_schedule_service.py app\services\upload_service.py app\services\audiobook_service.py tests\test_celery_enqueue.py tests\test_phase4_2_learning_loop.py
uv run pytest tests\test_celery_enqueue.py tests\test_phase4_2_learning_loop.py -q
uv run python -m py_compile app\schemas\plan.py app\services\reading_plan_schedule_service.py app\services\upload_service.py app\services\audiobook_service.py
```

Latest local result:

```text
ruff: All checks passed
pytest: 25 passed
py_compile: passed
```
