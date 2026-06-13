# Phase 14.1 Implementation Guide - Clean ReadingPlan Weekly Fallback

## 1. Mục tiêu

Phase 14.1 dùng để dọn logic plan cũ sau khi Phase 11, Phase 12 và Phase 13 đã đưa hệ thống sang mô hình lịch học cụ thể theo từng buổi.

Mục tiêu chính:

- Xoá vai trò runtime của `ReadingPlan.schedule_config`.
- Xoá fallback nhắc học theo tuần trực tiếp từ `ReadingPlan.schedule_config`.
- Giữ `reading_plan_sessions` là nguồn dữ liệu chính thức cho lịch học ngày giờ cụ thể.
- Giữ `reading_plan_schedule_slots` làm cấu hình lặp lại để tạo hoặc tái tạo sessions.
- Giữ toàn bộ logic mới Phase 11-13:
  - `learning_unit_progress`
  - `book_learning_states`
  - `reading_plan_sessions`
  - `reading_plan_session_units`
  - session skip/reschedule
  - session missed notification
  - spaced review theo learning unit completion

Không làm trong phase này:

- Không thêm `user_id` vào `reading_plans`.
- Không làm sách hệ thống dùng chung nhiều user.
- Không làm learning round/học lại nhiều vòng.
- Không refactor lớn notification push.
- Không đổi business logic Pareto/RAG/TTS.

## 2. Kết luận kiến trúc

Trước Phase 12, `ReadingPlan.schedule_config` có vai trò lưu ngày học lặp lại:

```text
ReadingPlan.schedule_config = ["Mon", "Wed", "Fri"]
ReadingPlan.reminder_time = "20:00"
```

Sau Phase 12, lịch học thật đã nằm ở:

```text
reading_plan_sessions
- scheduled_at
- local_date
- reminder_time
- timezone
- status
- session units
```

Vì vậy `ReadingPlan.schedule_config` trở thành dữ liệu lặp và dễ gây lệch logic:

- Plan nói học thứ hai, tư, sáu.
- Nhưng sessions có thể đã được dời lịch thủ công.
- Notification fallback đọc `schedule_config` có thể nhắc sai so với session thật.
- FE có thể hiểu nhầm plan weekly rule là lịch học thật.

Quyết định Phase 14.1:

```text
reading_plan_sessions = source of truth cho lịch học cụ thể
reading_plan_schedule_slots = source of truth cho rule lặp lại
ReadingPlan.schedule_config = legacy, cần xoá khỏi runtime và DB
```

## 2.1 Audit Update - Vấn Đề Cần Sửa Trước Khi Drop Column

Sau khi rà lại code và report audit bổ sung, có một điểm bắt buộc phải sửa trước khi drop `ReadingPlan.schedule_config`:

```text
Không được xóa slot lịch khi pause/inactive nữa.
```

Lý do:

- `pause_reading_plan` hiện đang gọi `delete_slots_for_plan`.
- `generate-plan` với `activate=false` hiện không tạo slot.
- Trước đây `ReadingPlan.schedule_config` còn giữ được cấu hình ngày học.
- Nếu drop `schedule_config` mà không đổi logic slot, plan `inactive` hoặc plan đã pause sẽ mất cấu hình lịch, không resume đúng được.

Quyết định cập nhật:

```text
reading_plan_schedule_slots lưu cả cấu hình active và inactive.
is_active=true: slot đang chiếm lịch, dùng để validate conflict và tạo sessions.
is_active=false: slot cấu hình tạm dừng/chưa kích hoạt, không gây conflict.
```

Nói ngắn gọn:

```text
Slots không còn là "active slots only".
Slots là cấu hình lịch của plan.
is_active chỉ cho biết cấu hình đó có đang chiếm lịch hay không.
```

## 3. Data Ownership Mới

### 3.1 ReadingPlan

Sau cleanup, `ReadingPlan` chỉ còn mô tả plan cấp cao:

```text
reading_plans
- id
- book_id
- mode
- pace
- status
- reminder_time
- started_at
- paused_at
- completed_at
- created_at
- updated_at
```

`reminder_time` vẫn giữ tạm trong `ReadingPlan` vì hiện response và update flow đang dùng nó như default time của plan. Về lâu dài có thể chuyển hết sang slots, nhưng chưa nên làm trong Phase 14.1 để tránh đổi quá rộng.

### 3.2 ReadingPlanScheduleSlot

`reading_plan_schedule_slots` là nơi lưu rule lặp lại:

```text
reading_plan_schedule_slots
- user_id
- book_id
- plan_id
- weekday
- reminder_time
- timezone
- is_active
```

Bảng này không phải fallback. Nó là cấu hình chuẩn để:

- validate trùng lịch giữa các sách đang học;
- tạo `reading_plan_sessions`;
- prefill UI chọn thứ và giờ học nếu FE cần.

Rule sau Phase 14.1:

- Plan active: slots có `is_active=true`.
- Plan inactive do chưa kích hoạt: slots vẫn tồn tại nhưng `is_active=false`.
- Plan inactive do pause: slots vẫn tồn tại nhưng `is_active=false`.
- Plan completed: slots nên chuyển `is_active=false` để giữ lịch sử cấu hình, không nên xóa cứng nếu không có lý do rõ ràng.
- Conflict validation chỉ xét slots `is_active=true`.

### 3.3 ReadingPlanSession

`reading_plan_sessions` là lịch học thực tế:

```text
reading_plan_sessions
- scheduled_at
- local_date
- reminder_time
- timezone
- status
- completed_units
- total_units
```

Notification và màn hình lịch học phải đọc từ bảng này.

## 4. Files Cần Chỉnh

### 4.1 Model

File:

```text
app/models/db_models.py
```

Chỉnh:

- Xoá field `ReadingPlan.schedule_config`.
- Giữ `ReadingPlan.reminder_time`.
- Không đụng các model Phase 11-13.

Trước:

```python
schedule_config: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
```

Sau:

```python
# Removed in Phase 14.1.
# Weekly recurrence is stored in reading_plan_schedule_slots.
```

### 4.2 Schema

File:

```text
app/schemas/plan.py
```

Hiện tại FE đang gửi `schedule_config` khi tạo hoặc update plan. Có hai hướng:

#### Recommended: compatibility bridge một phase

Giữ input field `schedule_config` trong request để không làm vỡ FE ngay:

```python
class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int
    schedule_config: list[str]
    reminder_time: str | None = None
    activate: bool = False
```

Nhưng không lưu vào `ReadingPlan.schedule_config` nữa. BE chỉ dùng `schedule_config` để tạo `reading_plan_schedule_slots`.

Response có thể giữ `schedule_config` tạm thời nhưng derive từ all slots of plan:

```text
schedule_config = all plan slots -> weekday labels
```

Sau khi FE chuyển qua dùng `active_slots`, có thể xoá `schedule_config` khỏi response ở phase sau.

#### Strict cleanup

Xoá `schedule_config` khỏi response và yêu cầu FE dùng `active_slots`.

Trade-off: sạch hơn nhưng breaking change cao hơn.

Recommendation Phase 14.1:

```text
Giữ request schedule_config để FE không vỡ.
Không lưu DB ReadingPlan.schedule_config.
Response schedule_config derive từ reading_plan_schedule_slots trong 1 phase chuyển tiếp.
```

Chi tiết response compatibility:

- `schedule_config`: derive từ tất cả slots của plan, bao gồm inactive slots.
- `active_slots`: chỉ trả slots `is_active=true`.
- Lý do: inactive/paused plan vẫn cần prefill UI bằng lịch đã chọn trước đó.

### 4.3 Repository Reading Plan

Tạo file mới:

```text
app/repositories/reading_plan_repo.py
```

Mục tiêu:

- Không còn query trực tiếp `select(ReadingPlan).where(ReadingPlan.book_id == book_id).first()` rải rác.
- Tập trung định nghĩa "current plan".

Đề xuất helper:

```python
def get_current_plan_for_owned_book(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
) -> ReadingPlan | None:
    ...
```

Rule Phase 14.1:

```text
Current plan = plan mới nhất của book không ở status error,
ưu tiên active, inactive, completed theo updated_at desc.
```

Nếu muốn chặt hơn:

```text
Current plan = plan duy nhất hiện có của book.
Nếu phát hiện nhiều plan không phải completed/error, raise conflict để tránh silent bug.
```

Recommendation:

```text
Không tạo nhiều ReadingPlan cho cùng một book trong phase hiện tại.
Nếu data dev có nhiều plan, chọn updated_at mới nhất nhưng log warning.
```

### 4.4 Audiobook Service

File:

```text
app/services/audiobook_service.py
```

Cần clean các chỗ:

```text
_book_to_response_dict
_active_plan
get_reading_plan
get_book_details
switch_book_mode
pause_reading_plan
resume_reading_plan
update_reading_plan
```

Thay mọi query:

```python
session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
```

bằng repository helper.

Không dùng `plan.schedule_config` nữa. Khi cần tạo slot:

```text
payload.schedule_config -> validate -> reading_plan_schedule_slots
```

Khi cần response:

```text
all slots -> schedule_config compatibility field
active slots -> active_slots field
```

Các thay đổi bắt buộc:

- `pause_reading_plan`: không gọi `delete_slots_for_plan`; chuyển slots của plan sang `is_active=false`.
- `resume_reading_plan`: đọc slots inactive/all của plan để lấy cấu hình cũ, validate conflict, rồi chuyển slots sang `is_active=true`.
- `update_reading_plan`: nếu request có `schedule_config`, replace slots theo request; nếu request không có `schedule_config`, dùng slots hiện có của plan.
- `_reading_plan_to_dict`: derive `schedule_config` từ slots thay vì đọc `plan.schedule_config`.

### 4.5 Upload Service

File:

```text
app/services/upload_service.py
```

Hiện tại tạo plan có:

```python
ReadingPlan(
    book_id=payload.book_id,
    mode=payload.mode,
    pace=payload.pace,
    schedule_config=payload.schedule_config,
    status=plan_status.value,
    reminder_time=resolved_reminder_time,
)
```

Sau cleanup:

```python
ReadingPlan(
    book_id=payload.book_id,
    mode=payload.mode,
    pace=payload.pace,
    status=plan_status.value,
    reminder_time=resolved_reminder_time,
)
```

`payload.schedule_config` chỉ dùng để validate và build slots.

Điểm cập nhật quan trọng:

```text
activate=false vẫn phải tạo reading_plan_schedule_slots với is_active=false.
```

Không tạo session khi `activate=false`, nhưng vẫn phải lưu cấu hình lịch để sau này resume/activate không mất data.

### 4.6 Reading Plan Session Service

File:

```text
app/services/reading_plan_session_service.py
```

`ensure_future_sessions_for_plan` hiện đang dùng:

```python
slots = list_slots_for_plan(session, plan_id=plan.id, active_only=True)
```

Đây là đúng. Giữ.

Cần clean thêm:

- Không để helper sync tự commit nếu đang nằm trong flow update progress.
- `sync_existing_session_units_from_progress` đang gọi helper có commit nhiều lần. Nên đổi sang batch mutate và để service caller commit một lần.

Phase 14.1 có thể làm phần này vì liên quan trực tiếp tới plan/session consistency.

Ngoài ra cần đảm bảo:

- `ensure_future_sessions_for_plan` chỉ dùng slots `is_active=true`.
- Khi plan inactive, không tạo sessions mới.
- Khi resume, chuyển slots sang active trước rồi mới gọi `ensure_future_sessions_for_plan`.

### 4.7 Notification Event Service

File:

```text
app/services/notification_event_service.py
```

Cần xoá fallback plan reminder theo weekly rule:

```text
_build_plan_reminder_outbox
create_due_plan_reminder_outbox_rows fallback branch reading_plans + schedule_config
```

Sau cleanup:

```text
Celery Beat
-> scan due reading_plan_sessions
-> create plan session reminder outbox
```

Không còn:

```text
ReadingPlan.schedule_config -> weekday_is_enabled -> reminder_time
```

Giữ:

```text
_build_plan_session_reminder_outbox
_create_due_plan_session_reminder_outbox_rows
_build_missed_plan_session_outbox
```

### 4.8 Reminder Schedule Service

File:

```text
app/services/reminder_schedule_service.py
```

Sau khi xoá fallback, kiểm tra `weekday_is_enabled` còn dùng ở đâu.

Nếu chỉ còn dùng cho fallback cũ thì xoá.

### 4.9 Tests

Cần update test cũ đang assert `schedule_config` được lưu trên `ReadingPlan`.

Files cần rà:

```text
tests/test_celery_enqueue.py
tests/test_phase4_2_learning_loop.py
tests/test_phase12_calendar_plan_sessions.py
tests/test_phase13_calendar_session_actions.py
tests/test_notification_outbox_repo.py
```

Rule mới cho tests:

- Request vẫn gửi `schedule_config`.
- DB `ReadingPlan` không còn field `schedule_config`.
- `reading_plan_schedule_slots` phải có đúng weekday/time/timezone cả khi plan inactive.
- `activate=false` phải tạo slots `is_active=false`.
- `pause` phải deactivate slots thay vì delete.
- `resume` phải reactivate slots và tạo sessions.
- `reading_plan_sessions` phải được tạo từ slots.
- Notification reminder phải dựa vào due sessions, không dựa vào weekly fallback.

## 5. Alembic Migration

Tạo migration:

```powershell
uv run alembic revision -m "phase 14 1 clean reading plan schedule config"
```

Không nên autogenerate mù. Migration nên viết tay để rõ ý đồ.

Upgrade phải backfill slots trước khi drop column. Không được drop thẳng nếu production/dev DB còn plan inactive/paused chỉ có `schedule_config`.

Recommended upgrade outline:

```python
def upgrade() -> None:
    # 1. Backfill reading_plan_schedule_slots from reading_plans.schedule_config
    #    for plans that do not already have slots.
    # 2. Use notification_settings.timezone when available,
    #    fallback to Asia/Ho_Chi_Minh.
    # 3. Set is_active based on reading_plans.status == 'active'.
    # 4. Drop reading_plans.schedule_config.
```

Minimal final step:

```python
op.drop_column("reading_plans", "schedule_config")
```

Backfill rule:

```text
ReadingPlan.status == active -> backfilled slots is_active=true
ReadingPlan.status != active -> backfilled slots is_active=false
```

If a plan already has slots, do not duplicate them.

Downgrade:

```python
def downgrade() -> None:
    op.add_column(
        "reading_plans",
        sa.Column("schedule_config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
```

Trước khi drop column, cần đảm bảo toàn bộ active/inactive plan đã có slots.

Nếu muốn an toàn hơn cho production:

```sql
select rp.id, rp.book_id
from reading_plans rp
left join reading_plan_schedule_slots slots
  on slots.plan_id = rp.id
where rp.status in ('active', 'inactive')
group by rp.id, rp.book_id
having count(slots.id) = 0;
```

Nếu query trả rows, migration backfill phải xử lý trước khi drop column. Khi deploy production, vẫn nên chạy audit query trước để biết dữ liệu có lệch không.

Recommendation sau audit:

```text
Luôn viết migration có backfill.
Không drop thẳng, kể cả dev, vì migration backfill giúp tránh bug lặp lại khi deploy production.
```

## 6. Business Rules Sau Cleanup

### 6.1 Tạo plan

```text
POST /api/v1/generate-plan
payload.schedule_config
-> validate weekdays
-> create ReadingPlan
-> create reading_plan_schedule_slots
   - activate=true: is_active=true
   - activate=false: is_active=false
-> if activate=true, create reading_plan_sessions from active slots
-> enqueue document worker
```

### 6.2 Update plan

```text
PUT /api/v1/books/{book_id}/reading-plan
payload.schedule_config
-> validate conflict
-> replace slots
   - active plan: new slots is_active=true
   - inactive plan: new slots is_active=false
-> cancel unfinished sessions
-> create new future sessions from slots
-> sync existing progress into new session units
```

Nếu `payload.schedule_config` không được gửi:

```text
-> reuse existing slots of plan
-> only update pace/reminder_time fields requested
```

### 6.3 Resume plan

```text
POST /api/v1/books/{book_id}/resume
-> read existing inactive slots of plan
-> validate those slots against active slots of other plans
-> set slots is_active=true
-> create future sessions from active slots
```

Nếu plan không có slots:

```text
-> raise clear 409/422 asking FE/user to update reading plan schedule first
```

### 6.4 Notification

```text
Celery Beat
-> due reading_plan_sessions
-> outbox PLAN_REMINDER
-> user_notifications / FCM
```

Không còn:

```text
ReadingPlan.schedule_config weekly fallback
```

## 7. Expected API Contract

### 7.1 Request

Tạm giữ `schedule_config` trong request:

```json
{
  "book_id": "uuid",
  "mode": "pareto",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "activate": true
}
```

### 7.2 Response

Recommended transition response:

```json
{
  "plan_id": "uuid",
  "book_id": "uuid",
  "mode": "pareto",
  "pace": 2,
  "reminder_time": "20:00",
  "plan_status": "active",
  "active_slots": [
    {
      "weekday": 0,
      "weekday_label": "monday",
      "reminder_time": "20:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "is_active": true
    }
  ],
  "session_summary": {
    "total_sessions": 3,
    "completed_sessions": 0,
    "missed_sessions": 0,
    "next_session": {}
  }
}
```

`schedule_config` trong response nên được xem là deprecated. Nếu còn giữ, phải derive từ all slots of plan, không đọc DB `ReadingPlan.schedule_config`.

## 8. Test Plan

### 8.1 Unit/API tests

Chạy:

```powershell
uv run pytest tests/test_phase12_calendar_plan_sessions.py tests/test_phase13_calendar_session_actions.py -q
uv run pytest tests/test_phase4_2_learning_loop.py -q
uv run pytest tests/test_notification_outbox_repo.py -q
```

### 8.2 Focus cases

Case 1: Create inactive plan

Expected:

- `reading_plans` created.
- `reading_plan_schedule_slots` created with `is_active=false`.
- No sessions.
- No `ReadingPlan.schedule_config`.

Case 2: Create active plan

Expected:

- slots created.
- sessions created from slots.
- response `active_slots` correct.
- response `session_summary.next_session` correct.

Case 3: Update active plan

Expected:

- old active slots replaced.
- unfinished sessions cancelled.
- new sessions created.
- completed/started progress sync into matching session units.

Case 3b: Pause and resume plan

Expected:

- pause changes plan to inactive.
- pause sets plan slots `is_active=false`, does not delete them.
- resume validates existing slots.
- resume sets plan slots `is_active=true`.
- resume creates future sessions.

Case 4: Notification reminder

Expected:

- due session creates outbox.
- plan without sessions does not create weekly fallback reminder.

Case 5: Completed book

Expected:

- reading plan completed.
- slots deactivated with `is_active=false`.
- unfinished sessions cancelled.
- review flow still works.

## 9. Trade-offs

### Lợi ích

- Một nguồn sự thật rõ ràng cho lịch học: `reading_plan_sessions`.
- Không còn nhắc học sai khi user đã dời một buổi học.
- Ít query mơ hồ hơn.
- Dễ giải thích với FE và báo cáo capstone hơn.
- Dọn được legacy fallback sau Phase 12/13.

### Đánh đổi

- Cần migration drop column.
- Cần migration backfill slots từ `ReadingPlan.schedule_config`.
- Cần update tests cũ.
- Có thể breaking nhẹ nếu FE đang đọc `schedule_config` từ response.
- Active plan cũ không có sessions sẽ không còn được nhắc bằng fallback.

Mitigation:

- Giữ request field `schedule_config` trong API.
- Response có thể derive `schedule_config` từ all slots of plan trong một phase chuyển tiếp.
- Trước deploy production, audit active plans không có sessions.

## 10. Câu hỏi cần chốt trước khi implement

### 10.1 Có giữ `schedule_config` trong response tạm thời không?

Recommendation:

```text
Có, nhưng derive từ all slots of plan và đánh dấu deprecated trong FE contract.
```

Lý do: tránh vỡ FE nếu màn setup plan đang prefill bằng `schedule_config`.

### 10.2 Inactive plan có lưu slots không?

Hiện tại nếu `activate=false`, BE validate shape nhưng không tạo active slots. Cách này chỉ an toàn khi còn `ReadingPlan.schedule_config`. Sau Phase 14.1 thì không còn an toàn.

Recommendation:

```text
Đổi logic: inactive plan vẫn lưu slots, nhưng is_active=false.
```

Lý do:

- Không mất cấu hình lịch đã chọn.
- Không gây conflict với sách khác vì conflict chỉ check `is_active=true`.
- Resume có thể kích hoạt lại lịch mà không cần FE gửi lại toàn bộ `schedule_config`.

### 10.3 Có xoá luôn fallback notification theo plan không?

Recommendation:

```text
Có. Đây là mục tiêu chính của Phase 14.1.
```

Điều kiện: active plan phải có sessions. Nếu plan không có sessions, đó là data inconsistency cần fix bằng resume/update plan, không nên fallback tiếp.

## 11. Implementation Order

1. Add `reading_plan_repo.py`.
2. Replace direct `ReadingPlan` queries in `audiobook_service.py`.
3. Remove `ReadingPlan.schedule_config` usage from `upload_service.py`.
4. Ensure generate-plan with `activate=false` creates slots `is_active=false`.
5. Replace pause/delete slot behavior with deactivate slot behavior.
6. Make resume reactivate existing slots.
7. Derive response `schedule_config` from all slots only if compatibility is needed.
8. Remove weekly fallback reminder from `notification_event_service.py`.
9. Remove unused `weekday_is_enabled` if no longer referenced.
10. Remove hidden commits in session/progress sync where practical.
11. Add Alembic migration to backfill slots and drop `reading_plans.schedule_config`.
12. Update tests.
13. Run focused test suite and py_compile.

## 12. Acceptance Criteria

Phase 14.1 hoàn tất khi:

- Source không còn đọc `ReadingPlan.schedule_config`.
- DB model không còn field `ReadingPlan.schedule_config`.
- Migration backfill slots và drop column tồn tại.
- Inactive/deferred plans preserve schedule through inactive slots.
- Pause deactivates slots instead of deleting schedule config.
- Resume reactivates slots and creates sessions.
- Plan reminders chỉ dựa trên `reading_plan_sessions`.
- Generate/update/resume plan vẫn tạo sessions đúng.
- Learning progress completion vẫn sync session units đúng.
- FE vẫn có thể tạo/update plan bằng `schedule_config` request field.
- Không ảnh hưởng RAG, TTS, upload parser, book_section_knowledge.
