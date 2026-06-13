# Phase 12 Implementation Guide - Calendar Reading Plan Sessions

Date: 2026-06-11  
Status: **Implemented and locally tested**  
Depends on:

- `_docs_implemented/phase_7_2_deferred_reading_plan_activation_implementation_guide.md`
- `_docs_implemented/phase_11_learning_progress_completion_state_implementation_guide.md`
- `_docs_implemented/doc_setup_flutter/flutter_phase_11_learning_progress_completion_contract.md`

Audience: Backend developer, Flutter developer, capstone reviewer

---

## 1. Goal

Phase 12 sửa phần **Reading Plan** để đúng nghĩa kế hoạch học theo lịch thật:

```text
Không chỉ:
  Thứ hai, thứ tư, thứ sáu lúc 20:00

Mà phải có:
  Ngày 15/06/2026 lúc 20:00 học Unit 1, Unit 2
  Ngày 17/06/2026 lúc 20:00 học Unit 3, Unit 4
  Ngày 19/06/2026 lúc 20:00 học Unit 5
```

Vấn đề hiện tại:

- `ReadingPlan.schedule_config` chỉ lưu các ngày trong tuần.
- `ReadingPlanScheduleSlot` chỉ lưu slot lặp lại theo `weekday + reminder_time`.
- FE không biết chính xác ngày/tháng/năm nào học unit nào.
- Plan reminder chỉ biết hôm nay có lịch học hay không, chưa biết buổi học cụ thể.
- Khi user học xong sách, Phase 11 đã fix completion, nhưng planner vẫn chưa có calendar sessions.

Mục tiêu sau Phase 12:

- Backend sinh danh sách buổi học cụ thể theo ngày/tháng/năm.
- Mỗi buổi học biết học learning units nào.
- FE có endpoint để hiển thị lịch học hiện tại.
- Reminder dựa trên session cụ thể, không chỉ dựa trên weekday.
- Progress/completion Phase 11 cập nhật ngược lại vào session.
- Update plan có thể regenerate future sessions an toàn.

---

## 2. Relationship With Phase 11

Phase 11 trả lời:

```text
User đã học tới đâu?
User đã học xong sách chưa?
User có thể resume hoặc review không?
```

Phase 12 trả lời:

```text
Ngày giờ nào user nên học unit nào?
Buổi học hôm nay là buổi nào?
Buổi học này đã xong, trễ, bỏ qua hay chưa?
```

Không nên làm Phase 12 trước Phase 11 vì planner cần biết:

- Unit nào đã completed.
- Book có completed chưa.
- Progress hiện tại tới unit/segment nào.
- Plan đã `completed` hay còn active.

---

## 3. Current Architecture Problem

### 3.1 Current Tables

```text
reading_plans
  book_id
  mode
  pace
  schedule_config = ["Mon", "Wed"]
  reminder_time = "20:00"
  status = inactive | active | completed | error

reading_plan_schedule_slots
  user_id
  plan_id
  book_id
  weekday
  reminder_time
  timezone
  is_active
```

This is a recurrence definition, not a real calendar plan.

### 3.2 Why FE Cannot Implement Correct UI

FE cần hiển thị:

```text
Hôm nay học gì?
Tuần này học gì?
Ngày 17/06 học unit nào?
Sách này còn mấy buổi?
Buổi nào đã hoàn thành?
```

Nhưng backend hiện chỉ nói:

```text
Thứ hai lúc 20:00 có lịch học.
```

Không đủ dữ liệu để FE build calendar UX chính xác.

---

## 4. Core Decision

Phase 12 không xoá `reading_plan_schedule_slots` ngay.

Thay vào đó thêm calendar layer:

```text
ReadingPlan
-> recurring schedule slots
-> generated concrete sessions
-> session units
-> progress/completion sync
```

Reason:

- Giữ backward compatibility cho FE hiện tại.
- Không phá reminder conflict logic cũ.
- Có thể rollout từ từ.
- Planner mới có dữ liệu ngày/tháng/năm rõ ràng.

---

## 5. New Business Concepts

### 5.1 Schedule Slot

Slot là quy tắc lặp lại:

```text
Thứ hai lúc 20:00
Thứ tư lúc 20:00
```

Slot dùng để:

- Validate trùng lịch active.
- Biết user thích học vào thứ/giờ nào.
- Sinh concrete sessions.

### 5.2 Study Session

Session là một buổi học cụ thể:

```text
2026-06-15 20:00 Asia/Ho_Chi_Minh
```

Session dùng để:

- FE hiển thị calendar.
- Reminder nhắc đúng buổi.
- Track buổi nào completed/missed/skipped.

### 5.3 Session Unit

Một session có thể chứa nhiều learning units.

Ví dụ `pace=2`:

```text
Session ngày 15/06:
  - Unit 1
  - Unit 2
```

Vì vậy không nên gán trực tiếp `learning_unit_id` vào `reading_plan_sessions` nếu muốn support `pace > 1` đúng nghĩa.

---

## 6. Database Design

### 6.1 Constants

File:

```text
app/core/constant.py
```

Add:

```python
class ReadingPlanSessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    DUE = "due"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class ReadingPlanSessionUnitStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
```

Recommended DB column type:

```text
Text + Python enum validation
```

Lý do:

- Dự án từng gặp lỗi migration Postgres enum.
- Status session có thể còn thay đổi theo business.
- Text dễ migrate hơn trong capstone timeline.

### 6.2 Table: reading_plan_sessions

File:

```text
app/models/db_models.py
```

Add:

```python
class ReadingPlanSession(SQLModel, table=True):
    __tablename__ = "reading_plan_sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), index=True, nullable=False))

    session_index: int = Field(sa_column=Column(Integer, nullable=False))
    scheduled_at: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True, nullable=False))
    local_date: str = Field(sa_column=Column(Text, index=True, nullable=False))  # YYYY-MM-DD
    reminder_time: str = Field(sa_column=Column(Text, nullable=False))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False))

    status: str = Field(default="scheduled", sa_column=Column(Text, index=True, nullable=False))
    completed_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))
    total_units: int = Field(default=0, sa_column=Column(Integer, nullable=False, server_default="0"))

    started_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    completed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    skipped_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    missed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        Index("ix_reading_plan_sessions_plan_index", "plan_id", "session_index"),
        Index("ix_reading_plan_sessions_user_status", "user_id", "status"),
        Index("ix_reading_plan_sessions_book_mode", "book_id", "mode"),
        Index("ix_reading_plan_sessions_plan_status", "plan_id", "status"),
    )
```

### 6.3 Table: reading_plan_session_units

```python
class ReadingPlanSessionUnit(SQLModel, table=True):
    __tablename__ = "reading_plan_session_units"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plan_sessions.id", ondelete="CASCADE"), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    learning_unit_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("learning_units.id", ondelete="CASCADE"), index=True, nullable=False))

    unit_order: int = Field(sa_column=Column(Integer, nullable=False))
    status: str = Field(default="pending", sa_column=Column(Text, index=True, nullable=False))
    completed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        Index("ix_reading_plan_session_units_plan_unit", "plan_id", "learning_unit_id"),
        UniqueConstraint("session_id", "unit_order", name="uq_reading_plan_session_units_session_order"),
        Index("ix_reading_plan_session_units_session_status", "session_id", "status"),
        Index("ix_reading_plan_session_units_book_unit", "book_id", "learning_unit_id"),
    )
```

### 6.4 Why Separate Session And SessionUnit?

Because `pace` means:

```text
Số learning units mỗi buổi/ngày học
```

If `pace=3`, one session can contain 3 units.

If we put only one `learning_unit_id` in session:

- Either create 3 sessions at same timestamp.
- Or cannot support pace correctly.

Both are weaker than a session-unit mapping.

---

## 7. Planner Algorithm

### 7.1 Inputs

```text
plan_id
book_id
mode
pace
schedule_config
reminder_time
timezone
start_date optional
```

Default `start_date`:

```text
today in user's timezone if book is already playable
otherwise first date after activation/resume
```

### 7.2 Unit Source

Use learning units:

```text
LearningUnit.book_id = book_id
LearningUnit.mode = plan.mode
LearningUnit.status in READY/PARTIAL_READY? 
```

Recommended:

- Include all learning units in correct `unit_index`.
- FE can show sessions even if audio generation is still running.
- If a unit is not playable yet, session still exists but FE should mark unit as not ready.

For first implementation, use units with at least one segment if product wants only playable schedule.

Recommendation:

```text
Generate sessions for all learning units.
Use unit.status/segment count to show whether unit is playable.
```

Reason:

- Calendar represents learning plan, not only audio readiness.
- User can see total plan upfront.

### 7.3 Date Generation

Pseudo:

```python
def generate_session_dates(schedule_config, reminder_time, timezone, start_date, required_sessions):
    weekdays = normalize weekdays
    cursor = start_date
    dates = []

    while len(dates) < required_sessions:
        if cursor.weekday() in weekdays:
            local_dt = combine(cursor, reminder_time, timezone)
            if local_dt >= now_local:
                dates.append(local_dt)
        cursor += 1 day

    return dates
```

### 7.3.1 Timezone And local_date Rule

This rule is mandatory.

`scheduled_at` must be stored as timezone-aware UTC in DB.

`local_date` must be derived from the user's configured timezone:

```text
user_settings.timezone
-> convert scheduled_at UTC to local datetime
-> local_date = YYYY-MM-DD in that timezone
```

Do not use:

```text
server timezone
UTC date
datetime.now() without timezone
```

Why:

- Home screen `GET /reading-plan/sessions/today` depends on local date.
- A UTC date can be different from the user's local date.
- If `local_date` is wrong, FE will show the wrong "today" plan.

Implementation helper should be explicit:

```python
def build_session_local_fields(scheduled_at_utc: datetime, timezone_name: str) -> tuple[str, str]:
    local_dt = to_local(scheduled_at_utc, timezone_name)
    return local_dt.date().isoformat(), local_dt.strftime("%H:%M")
```

`reminder_time` should remain the user's intended wall-clock time, while `scheduled_at` is the UTC instant.

### 7.4 Assign Units To Sessions

Pseudo:

```python
units = list units ordered by unit_index
chunks = chunk(units, size=pace)
dates = generate dates for len(chunks)

for index, chunk in enumerate(chunks):
    create ReadingPlanSession(session_index=index, scheduled_at=dates[index])
    for order, unit in enumerate(chunk):
        create ReadingPlanSessionUnit(unit_order=order, learning_unit_id=unit.id)
```

### 7.5 Skip Already Completed Units

When regenerating future sessions:

- Completed learning units should not be put into new future sessions.
- In-progress current unit should stay in current/next session.

Rules:

```text
Initial plan generation:
  include all units.

Update plan after user has progress:
  keep past/completed sessions as historical records.
  cancel future pending sessions.
  regenerate only for remaining uncompleted units.
```

---

## 8. API Contract

### 8.1 POST /api/v1/generate-plan

Keep current request:

```json
{
  "book_id": "uuid",
  "mode": "full",
  "pace": 2,
  "schedule_config": ["Mon", "Wed", "Fri"],
  "reminder_time": "20:00",
  "activate": false
}
```

Response should add optional session preview:

```json
{
  "plan_id": "uuid",
  "plan_status": "inactive",
  "planned_sessions": [
    {
      "session_index": 0,
      "scheduled_at": "2026-06-15T13:00:00Z",
      "local_date": "2026-06-15",
      "reminder_time": "20:00",
      "unit_count": 2
    }
  ]
}
```

Important:

- If `activate=false`, backend may create configured plan but not active slots.
- For Phase 12, session generation can happen at activation/resume, not necessarily at upload/generate-plan.
- To avoid confusing FE, return `planned_sessions=[]` if sessions are not generated yet.

Recommendation:

```text
Generate concrete sessions when plan becomes active.
```

Reason:

- If book audio is still processing, activation may happen later.
- Start date should be based on real activation date.

### 8.2 POST /api/v1/books/{book_id}/resume

Current behavior:

```text
inactive plan -> active plan + create schedule slots
```

Phase 12 behavior:

```text
inactive plan -> active plan + create schedule slots + generate future sessions
```

Response add:

```json
{
  "plan_status": "active",
  "active_slots": [],
  "sessions_created": 8,
  "next_session": {
    "session_id": "uuid",
    "scheduled_at": "2026-06-15T13:00:00Z",
    "local_date": "2026-06-15",
    "units": []
  }
}
```

### 8.3 GET /api/v1/books/{book_id}/reading-plan

Add summary:

```json
{
  "plan_id": "uuid",
  "book_id": "uuid",
  "mode": "full",
  "pace": 2,
  "schedule_config": ["Mon", "Wed"],
  "reminder_time": "20:00",
  "plan_status": "active",
  "session_summary": {
    "total_sessions": 8,
    "completed_sessions": 2,
    "remaining_sessions": 6,
    "next_session_at": "2026-06-15T13:00:00Z"
  }
}
```

### 8.4 GET /api/v1/books/{book_id}/reading-plan/sessions

New endpoint.

Query:

```text
from=2026-06-01 optional local date
to=2026-06-30 optional local date
status=scheduled|due|in_progress|completed|missed|skipped|cancelled|all
mode=full|pareto optional
```

Response:

```json
{
  "items": [
    {
      "session_id": "uuid",
      "session_index": 0,
      "book_id": "uuid",
      "plan_id": "uuid",
      "mode": "full",
      "scheduled_at": "2026-06-15T13:00:00Z",
      "local_date": "2026-06-15",
      "reminder_time": "20:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "status": "scheduled",
      "completed_units": 0,
      "total_units": 2,
      "units": [
        {
          "learning_unit_id": "uuid",
          "title": "Unit 1",
          "unit_index": 0,
          "unit_order": 0,
          "status": "pending",
          "progress_status": "not_started",
          "is_playable": true
        }
      ]
    }
  ],
  "total": 1
}
```

### 8.5 GET /api/v1/reading-plan/sessions/today

New endpoint for home screen:

```text
GET /api/v1/reading-plan/sessions/today
```

Response:

```json
{
  "items": [
    {
      "session_id": "uuid",
      "book_id": "uuid",
      "book_title": "Tên sách",
      "scheduled_at": "2026-06-15T13:00:00Z",
      "status": "due",
      "units": []
    }
  ],
  "total": 1
}
```

### 8.6 POST /api/v1/reading-plan/sessions/{session_id}/skip

Optional in first implementation but recommended.

Rules:

- Marks session as `skipped`.
- Does not mark learning units completed.
- Future reschedule can include skipped units again.

### 8.7 POST /api/v1/reading-plan/sessions/{session_id}/complete

Optional.

Prefer not to implement as primary completion method.

Reason:

- Unit completion should still come from learning progress/manual unit complete.
- Session completion should be derived from its units.

Recommended:

```text
Do not add manual session complete in first pass.
Use unit progress completion to sync session status.
```

---

## 9. Service Design

### 9.1 New Service

Create:

```text
app/services/reading_plan_session_service.py
```

Responsibilities:

- Generate concrete sessions.
- Assign units to sessions.
- List sessions for FE.
- Sync session status from unit progress.
- Cancel future sessions when updating plan.
- Mark missed sessions.

### 9.2 New Repository

Create:

```text
app/repositories/reading_plan_session_repo.py
```

Functions:

```python
def list_sessions_for_plan(...)
def list_sessions_for_book(...)
def get_session_for_user(...)
def create_sessions_with_units(...)
def cancel_future_sessions(...)
def find_session_unit_by_learning_unit(...)
def update_session_status(...)
def list_today_sessions(...)
```

Repository must not contain business decisions.

### 9.3 Session Generation Trigger Points

Generate sessions when:

1. `POST /books/{book_id}/resume` activates a plan.
2. `PUT /books/{book_id}/reading-plan` updates an active plan.
3. `POST /generate-plan` only if `activate=true`.

Do not generate sessions for inactive plan by default.

Reason:

- Inactive plan is only configuration.
- Concrete dates should start from actual activation.

### 9.4 Updating Active Plan

When user updates schedule of an active plan:

```text
1. Validate new schedule conflict.
2. Keep historical sessions:
   - completed
   - skipped
   - missed
   - sessions scheduled_at < now
3. Cancel future scheduled/due sessions that are not started.
4. Generate new sessions for remaining uncompleted units.
5. Return new next_session.
```

This avoids losing history and avoids duplicate future sessions.

### 9.5 Lazy Missed Session Evaluation

Agree with Gemini's recommendation: lazy missed evaluation should be implemented.

Before returning session list APIs, the service should update overdue sessions for that user.

Run this inside:

```text
GET /api/v1/books/{book_id}/reading-plan/sessions
GET /api/v1/reading-plan/sessions/today
```

Pseudo:

```python
def mark_user_overdue_sessions_missed(session, *, user_id, now):
    rows = list scheduled/due/in_progress sessions where scheduled_at < now and not completed
    for row in rows:
        if row.total_units > 0 and row.completed_units >= row.total_units:
            row.status = completed
            row.completed_at = row.completed_at or now
        else:
            row.status = missed
            row.missed_at = row.missed_at or now
```

Why lazy evaluation is required:

- UI becomes correct immediately when user opens the app.
- It does not depend on Celery Beat being alive.
- It avoids stale `scheduled` sessions after server sleep/redeploy.

Rules:

- Only mark missed when `scheduled_at < now`.
- Do not mark cancelled/skipped/completed sessions missed.
- If the user already completed all units, mark completed, not missed.
- Commit before returning API response.

### 9.6 Periodic Missed Session Scanner

Also implement a Celery Beat task, but treat it as background maintenance, not the only source of truth.

Recommended schedule:

```text
Every 30-60 minutes
```

Task:

```text
triam.reading_plan_sessions.mark_missed
queue = maintenance
```

Responsibilities:

- Mark overdue sessions missed in bulk.
- Optionally create missed-session notification later.

Important caution:

```text
Do not send missed-session notifications in the first Phase 12 implementation
unless product copy, cooldown, and daily cap behavior are explicitly defined.
```

Reason:

- Late reminders can annoy users if they already ignored a study session.
- The current notification system already has daily cap and quiet hours, but missed-session copy/UX should be decided deliberately.
- For Phase 12, marking status correctly is more important than adding a new notification type.

---

## 10. Sync With Learning Progress

Phase 11 already updates `BookLearningState`.

Phase 12 should add:

```text
When a LearningUnitProgress becomes COMPLETED:
  find ReadingPlanSessionUnit by plan_id + learning_unit_id
  mark session unit completed
  recompute session.completed_units
  if all units in session completed:
    mark session completed
```

Where to call:

```text
app/services/learning_progress_service.py
```

After:

```text
sync_book_learning_state(...)
```

Call:

```python
sync_reading_plan_session_unit_completion(...)
```

Rules:

- Idempotent.
- If no session exists, do nothing.
- Do not create sessions from progress service.
- Do not mark plan completed here; Phase 11 already handles book/plan completion.

### 10.1 Catch-Up Study After Missed Session

Agree with Gemini's recommendation: a missed session must still be completable.

If a session is:

```text
missed
in_progress
due
scheduled
```

and user later completes all units assigned to that session, backend must update:

```text
session.status = completed
session.completed_at = now
session.completed_units = total_units
```

This is the "học bù" behavior.

Rules:

- `missed` is not terminal.
- `cancelled`, `skipped`, and `completed` are terminal unless product later adds undo/reschedule.
- A missed session can become completed through real unit progress.
- Completing a unit should update `ReadingPlanSessionUnit.status=completed` even if the parent session was missed.

Pseudo:

```python
def sync_reading_plan_session_unit_completion(...):
    session_unit.status = completed
    session_unit.completed_at = completed_at

    parent.completed_units = count_completed_units(parent.id)
    if parent.completed_units >= parent.total_units:
        parent.status = completed
        parent.completed_at = completed_at
    elif parent.status in (scheduled, due, missed):
        parent.status = in_progress
```

Question:

```text
If parent was missed but only one of several units is completed,
should it stay missed or move to in_progress?
```

Recommendation:

```text
Move to in_progress when user resumes catch-up work.
Move to completed only when all units are done.
```

Reason:

- UI can show "Đang học bù" instead of permanently missed.
- This feels more encouraging and accurate.

---

## 11. Reminder Logic Update

Current plan reminder:

```text
Scan active ReadingPlan
Check weekday/time
Check uncompleted playable unit
Create notification
```

Phase 12 reminder:

```text
Scan due ReadingPlanSession
Check notification settings / quiet hours / daily cap
Create notification for that session
Mark session DUE if needed
```

Missed session notification:

```text
Do not include in Phase 12 core unless explicitly approved.
```

If later added, use:

- quiet hours;
- daily cap;
- idempotency key per session;
- no duplicate missed reminder after session becomes completed.

Update file:

```text
app/services/notification_event_service.py
```

New rule:

```text
Plan reminder should prefer concrete sessions.
Fallback to old weekday logic only if no sessions exist for a legacy active plan.
```

This makes deployment safe:

- Existing active plans without sessions still get reminders.
- New plans use calendar sessions.

---

## 12. Conflict Logic

### 12.1 Keep Weekly Slot Conflict

Keep current conflict:

```text
user_id + weekday + reminder_time active unique
```

This prevents recurring schedule conflicts.

### 12.2 Add Concrete Session Conflict

Implemented conflict rule:

```text
user_id + scheduled_at where status != cancelled
```

This prevents two active sessions at the exact same datetime while still allowing cancelled historical sessions to remain.

Trade-off:

- User cannot study two books at the same exact time.
- This is correct for focus and reminder UX.
- Cancelled sessions are kept for audit/history, so `plan_id + session_index` and `plan_id + learning_unit_id` must be normal indexes, not unique constraints.
- This was confirmed during implementation: unique constraints on regenerated session history blocked active plan updates.

### 12.3 Future Improvement

If later app supports sessions with duration:

```text
scheduled_at + estimated_duration
```

Then conflict should be time range overlap, not exact timestamp.

Out of scope for Phase 12.

---

## 13. Backfill Strategy

Existing active plans may have no sessions.

Migration should create tables only.

Do not backfill sessions in migration.

Reason:

- Session generation needs timezone/settings/business logic.
- Migration should stay deterministic and fast.
- Backfill can run in service/admin script.

Add helper command/script later:

```text
scripts/backfill_reading_plan_sessions.py
```

For Phase 12 tests/manual use, sessions are generated when:

- `POST /generate-plan` is called with `activate=true`;
- inactive plan is resumed;
- active plan schedule/pace is updated.

---

## 14. FE UI/UX Contract

### 14.1 Book Detail

Add section:

```text
Lịch học sắp tới
```

Data:

```text
GET /api/v1/books/{book_id}/reading-plan/sessions?status=all
```

Show:

- Date.
- Time.
- Units in session.
- Status.
- Progress within session.

### 14.2 Home Screen

Use:

```text
GET /api/v1/reading-plan/sessions/today
```

Show:

```text
Hôm nay bạn có 2 buổi học
20:00 - Sách A - Unit 3, Unit 4
21:00 - Sách B - Unit 1
```

### 14.3 Update Plan Screen

When user updates schedule:

```text
PUT /api/v1/books/{book_id}/reading-plan
```

FE should show:

```text
Lịch học tương lai sẽ được cập nhật. Các buổi đã học vẫn được giữ.
```

### 14.4 Completed Book

If Phase 11 says:

```text
learning_status=completed
```

Then FE should not show future study sessions unless user chooses "Học lại".

Review schedule is separate:

```text
GET /api/v1/books/{book_id}/reviews
```

---

## 15. Tests Required

### 15.1 Unit Tests

Add:

```text
tests/test_phase12_calendar_plan_sessions.py
```

Cases:

1. Generate sessions from schedule weekdays and reminder time.
2. `pace=2` creates one session containing 2 units.
3. Generated sessions have concrete `scheduled_at` with timezone.
4. Completed units are skipped when regenerating future sessions.
5. Updating active plan cancels future sessions and keeps completed history.
6. Completing all units in a session marks session completed.
7. User A cannot see User B sessions.
8. Completed plan does not generate new sessions.
9. Overdue scheduled session becomes missed through lazy evaluation.
10. Missed session becomes in_progress/completed when user studies catch-up.
11. `local_date` is generated from user timezone, not UTC/server timezone.

### 15.2 API Tests

Cases:

1. Resume inactive plan creates sessions.
2. `GET /books/{book_id}/reading-plan/sessions` returns session units.
3. `GET /reading-plan/sessions/today` returns only current user sessions.
4. Update active plan regenerates future sessions.
5. Conflict at same date/time returns 409.
6. Listing sessions runs lazy missed evaluation before response.
7. Today's sessions use user's local date.

### 15.3 Notification Tests

Cases:

1. Due session creates plan reminder outbox.
2. Legacy active plan without sessions still uses old reminder path.
3. Completed session does not create reminder.
4. Completed book/plan does not create study reminder.
5. Missed-session maintenance task marks overdue sessions without creating duplicate notifications.

---

## 16. Manual Test Flow

Use one real uploaded book with multiple learning units.

```text
1. Upload book.
2. Generate plan with activate=false.
3. Wait until partial_ready/ready.
4. Resume plan.
5. Call GET /books/{book_id}/reading-plan/sessions.
6. Confirm sessions have concrete dates.
7. Complete first unit.
8. Confirm matching session unit completed.
9. Complete all units in first session.
10. Confirm session status completed.
11. Update reading plan schedule.
12. Confirm future sessions regenerated, completed sessions kept.
```

Expected:

```text
FE can show a calendar.
Plan no longer feels like vague week learning.
Reminder can point to a concrete session.
Progress and completion still work from Phase 11.
```

---

## 17. Implementation Order

### Step 1 - Constants And Models

Files:

```text
app/core/constant.py
app/models/db_models.py
app/db/migrations/versions/<revision>_phase_12_calendar_sessions.py
```

Add:

- `ReadingPlanSessionStatus`
- `ReadingPlanSessionUnitStatus`
- `ReadingPlanSession`
- `ReadingPlanSessionUnit`

### Step 2 - Repository

File:

```text
app/repositories/reading_plan_session_repo.py
```

Implement DB operations only.

### Step 3 - Service

File:

```text
app/services/reading_plan_session_service.py
```

Implement:

- Date generation.
- Unit assignment.
- Future session regeneration.
- Session status sync.
- Today session query.

### Step 4 - Integrate Existing Plan Flow

Files:

```text
app/services/audiobook_service.py
app/services/upload_service.py
```

Integrate:

- Resume creates sessions.
- Active plan update regenerates future sessions.
- Generate-plan with `activate=true` creates sessions.

Do not change inactive generate-plan behavior.

### Step 5 - Integrate Learning Progress

File:

```text
app/services/learning_progress_service.py
```

After unit progress completion:

```text
sync session unit completion
```

### Step 6 - API And Schemas

Files:

```text
app/schemas/plan.py
app/api/v1/routers/audiobooks.py
```

Add:

- Session response DTOs.
- Book sessions endpoint.
- Today sessions endpoint.

### Step 7 - Notification Scanner

File:

```text
app/services/notification_event_service.py
```

Prefer session-based reminder.

Keep legacy fallback.

### Step 8 - Tests

Run:

```powershell
uv run pytest tests/test_phase12_calendar_plan_sessions.py -q
uv run pytest tests/test_phase4_2_learning_loop.py tests/test_notification_outbox_repo.py -q
uv run ruff check app tests
```

Implemented local result:

```text
uv run pytest tests/test_phase12_calendar_plan_sessions.py -q
3 passed

uv run pytest tests/test_phase4_2_learning_loop.py -q
19 passed

uv run pytest tests/test_notification_outbox_repo.py tests/test_notifications_api.py -q
9 passed

uv run ruff check <changed Phase 12 files>
All checks passed

uv run python -m py_compile <changed runtime files>
passed
```

---

## 18. Trade-Offs

### 18.1 More Tables

Adding sessions and session_units increases schema complexity.

Worth it because:

- FE gets exact calendar data.
- Reminder becomes accurate.
- User can see plan progression clearly.

### 18.2 Regeneration Complexity

Updating plan now needs careful behavior:

- Keep history.
- Cancel only future pending sessions.
- Reassign remaining units.

This is more code, but prevents data loss and weird UI resets.

### 18.3 Not Backfilling In Migration

Old active plans may have no sessions until resume/update/backfill.

Mitigation:

- Reminder keeps legacy fallback.
- Add admin/dev backfill script later if needed.

### 18.4 Duration-Based Conflict Not Included

Phase 12 only prevents exact same scheduled time.

Future system can add estimated duration overlap.

### 18.5 Lazy Evaluation Writes During GET

Lazy missed evaluation means some GET requests can write to DB.

Trade-off:

- This is less "pure REST".
- But it ensures FE always sees correct schedule state even if Celery Beat is delayed or the server slept.

Mitigation:

- Keep the write small and scoped to current user/book.
- Only update rows whose state truly changed.
- Put the logic in service layer, not router.

### 18.6 Missed Notification Deferred

Marking sessions missed is in scope.

Sending missed-session notification is not core Phase 12 unless approved.

Reason:

- Notification copy and anti-spam rules need product decision.
- A bad missed notification can hurt UX more than no notification.

---

## 19. Definition Of Done

Phase 12 is complete when:

- Backend has concrete `reading_plan_sessions`.
- FE can fetch sessions for a book.
- FE can fetch today's sessions.
- Resume active plan creates future sessions.
- Update active plan regenerates future sessions without deleting history.
- Unit completion updates session/session-unit status.
- Missed sessions are updated by lazy evaluation and maintenance scanner.
- Catch-up learning can turn missed/in_progress sessions into completed.
- `local_date` is computed from user timezone.
- Plan reminder can use concrete session.
- Old plans without sessions still work through fallback.
- Tests pass for schedule generation, progress sync, and reminder behavior.

---

## 20. Recommended Next Phase

After Phase 12:

```text
Phase 13 - Learn Again Flow And Calendar Reschedule Polish
```

Phase 13 should handle:

- Học lại sách đã completed.
- Reset or create new learning round.
- Reschedule missed sessions.
- Better conflict response with book title/session detail.
- FE polish for calendar and overdue sessions.
