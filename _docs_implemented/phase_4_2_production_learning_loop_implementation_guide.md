# Phase 4.2 Implementation Guide - Production Learning Loop Guardrails

Date: 2026-05-25  
Status: **Implementation plan only, not source code yet**  
Depends on: `_docs_implemented/phase_4_production_notification_business_logic.md`  
Audience: Backend developer, Flutter developer, capstone reviewer

---

## 1. Goal

Phase 4.1 đã có notification infrastructure:

- `notification_settings`
- `notification_outbox`
- `user_notifications`
- Celery Beat `scan_due`
- Celery worker `deliver_due`
- quiet hours, daily cap, idempotency, stale-lock recovery

Nhưng Phase 4.1 vẫn còn một lỗi business lớn:

```text
spaced_review_items đang được tạo khi chapter READY,
trong khi đúng ra phải tạo khi user đã học xong chapter.
```

Phase 4.2 sửa phần business logic để hệ thống nhắc học/ôn tập dùng được như sản phẩm thật:

```text
ReadingPlan schedule guardrails
-> chapter learning progress
-> segment resume
-> completion-based spaced review
-> production plan reminder filters
-> review complete/skip
-> content-ready aggregation
```

Điều quan trọng:

```text
Không triển khai Push Notification trước khi Phase 4.2 xong.
```

Lý do: nếu logic reminder/review còn sai, push thật sẽ gửi sai notification ra ngoài app và làm trải nghiệm tệ hơn.

---

## 2. Final Business Decisions

| Problem | Decision |
| --- | --- |
| User học nhiều sách | Cho phép nhiều sách active nhưng có giới hạn |
| Lịch học bị trùng | Không cho trùng active schedule slot |
| Active schedule slot | `user_id + weekday + reminder_time` |
| Max active books | Config theo hệ thống/tier, ví dụ 3 |
| Progress granularity | Lưu progress theo chapter, nhưng có segment resume |
| Resume listening | Dựa vào `current_segment_id/last_segment_index + position_ms` |
| Completion threshold | `max_progress_percent >= 80` hoặc manual complete |
| Spaced review anchor | `due_at = chapter_completed_at + interval_days` |
| Content-ready UX | Gửi `first_playable` và `book_ready`, không spam từng chapter |
| Plan reminder | Dựa trên ReadingPlan + learning progress |
| Review reminder | Chỉ gửi nếu chapter thật sự completed |

---

## 3. Scope

### 3.1 In Scope

Phase này implement:

1. Reading plan schedule conflict validation.
2. Max active learning books guardrail.
3. `chapter_learning_progress` table.
4. Segment-level resume fields.
5. Book-level progress summary endpoint.
6. Completion detection at 80 percent.
7. Manual complete chapter endpoint.
8. Move spaced review creation from chapter ready to chapter completed.
9. Add review complete/skip endpoints.
10. Improve plan reminder filters.
11. Aggregate content-ready notification into first-playable/book-ready.
12. Tests for no premature review and no duplicate reminders.

### 3.2 Out Of Scope

Do not implement yet:

- Auth user id replacement.
- Firebase Cloud Messaging.
- Device tokens.
- Payment/subscription.
- Advanced analytics/streak dashboard.
- ML-based adaptive spaced repetition.

Those features depend on this phase being correct.

---

## 4. Current Files To Touch

### Core

```text
app/core/constant.py
app/core/config.py
app/core/exceptions.py
```

### Models/Migration

```text
app/models/db_models.py
app/db/migrations/versions/<new_revision>_phase_4_2_learning_progress.py
```

### Repositories

```text
app/repositories/learning_progress_repo.py
app/repositories/reading_plan_schedule_repo.py
app/repositories/spaced_review_repo.py
app/repositories/notification_outbox_repo.py
```

### Services

```text
app/services/learning_progress_service.py
app/services/reading_plan_schedule_service.py
app/services/spaced_review_service.py
app/services/notification_event_service.py
app/services/notification_copy_service.py
app/services/upload_service.py
```

### Routers/Schemas

```text
app/api/v1/routers/learning_progress.py
app/api/v1/routers/reviews.py
app/schemas/learning_progress.py
app/schemas/review.py
```

### Workers/Tasks

```text
app/services/workers/chapter_worker.py
app/services/workers/book_pipeline.py
app/tasks/notification_tasks.py
```

### Tests

```text
tests/test_learning_progress_service.py
tests/test_learning_progress_api.py
tests/test_reading_plan_schedule_guardrails.py
tests/test_completion_based_spaced_review.py
tests/test_notification_plan_reminder_filters.py
```

---

## 5. Config Changes

File: `app/core/config.py`

Add:

```python
    # Phase 4.2 production learning loop
    MAX_ACTIVE_LEARNING_BOOKS_PER_USER: int = 3
    LEARNING_COMPLETION_THRESHOLD_PERCENT: int = 80
    LEARNING_PROGRESS_STALE_SECONDS: int = 30
    PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS: int = 24
```

File: `.env.example`

Add:

```env
# Phase 4.2 production learning loop
MAX_ACTIVE_LEARNING_BOOKS_PER_USER=3
LEARNING_COMPLETION_THRESHOLD_PERCENT=80
LEARNING_PROGRESS_STALE_SECONDS=30
PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS=24
```

Why:

- `MAX_ACTIVE_LEARNING_BOOKS_PER_USER` controls focus and cost.
- `LEARNING_COMPLETION_THRESHOLD_PERCENT` keeps completion logic configurable.
- `LEARNING_PROGRESS_STALE_SECONDS` can later throttle duplicate progress writes.
- `PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS` documents the business window clearly, even if timezone-local day remains the main rule.

---

## 6. Constants

File: `app/core/constant.py`

Add:

```python
class LearningProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ReviewAction(str, Enum):
    COMPLETE = "complete"
    SKIP = "skip"
```

Do not add a separate `BOOK_COMPLETED` status yet unless product really needs it.

Reason:

```text
Book completion can be derived from chapter_learning_progress.
Adding a stored Book.completed state too early risks drift.
```

---

## 7. Database Design

### 7.1 `chapter_learning_progress`

Purpose:

```text
Track real user learning progress by chapter/mode,
and store segment resume position for "continue listening".
```

Model to add in `app/models/db_models.py`:

```python
class ChapterLearningProgress(SQLModel, table=True):
    __tablename__ = "chapter_learning_progress"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    chapter_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), index=True, nullable=False))
    mode: PlanMode = Field(sa_column=Column(SAEnum(PlanMode), nullable=False))

    current_segment_id: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    last_segment_index: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    position_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    listened_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    total_duration_ms: int = Field(default=0, sa_column=Column(Integer, nullable=False))

    progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    max_progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    status: LearningProgressStatus = Field(default=LearningProgressStatus.NOT_STARTED, sa_column=Column(SAEnum(LearningProgressStatus), index=True, nullable=False))

    started_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    last_activity_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    completed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))

    __table_args__ = (
        UniqueConstraint("user_id", "chapter_id", "mode", name="uq_learning_progress_user_chapter_mode"),
    )
```

Notes:

- `current_segment_id` is currently `int` because `ChapterSegment.id` is `int`.
- `last_segment_index` is kept because FE playlist ordering uses segment index naturally.
- `progress_percent` can go down if user seeks backward.
- `max_progress_percent` never goes down and should drive completion.

### 7.2 `reading_plan_schedule_slots`

Purpose:

```text
Prevent active reading plans from overlapping on the same local weekday/time.
```

Model:

```python
class ReadingPlanScheduleSlot(SQLModel, table=True):
    __tablename__ = "reading_plan_schedule_slots"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    plan_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("reading_plans.id", ondelete="CASCADE"), index=True, nullable=False))
    book_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True, nullable=False))
    weekday: int = Field(sa_column=Column(Integer, nullable=False))
    reminder_time: str = Field(sa_column=Column(Text, nullable=False))
    timezone: str = Field(default="Asia/Ho_Chi_Minh", sa_column=Column(Text, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, index=True, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
```

Manual migration should add a partial unique index:

```python
op.create_index(
    "uq_active_plan_slot_user_weekday_time",
    "reading_plan_schedule_slots",
    ["user_id", "weekday", "reminder_time"],
    unique=True,
    postgresql_where=sa.text("is_active = true"),
)
```

Why not only service validation:

- Service validation catches normal API calls.
- DB unique index protects against concurrent requests and worker retries.

### 7.3 Extend `spaced_review_items`

Current `completed_at` should mean:

```text
The review item itself was completed by user.
```

Add fields:

```python
anchor_completed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))
source_progress_id: uuid.UUID | None = Field(default=None, sa_column=Column(UUID(as_uuid=True), ForeignKey("chapter_learning_progress.id", ondelete="SET NULL"), index=True))
notified_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
last_reviewed_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
```

Why:

- `anchor_completed_at` records when the learning event happened.
- `due_at` can be shifted by quiet hours later.
- `completed_at` should remain available for review completion.
- `source_progress_id` makes debugging clear.

### 7.4 Migration Checklist

Create migration:

```powershell
uv run alembic revision -m "phase 4 2 learning progress"
```

Migration must:

1. Create enum for `LearningProgressStatus`.
2. Create `chapter_learning_progress`.
3. Create `reading_plan_schedule_slots`.
4. Add partial unique index on active schedule slots.
5. Add `anchor_completed_at`, `source_progress_id`, `notified_at`, `last_reviewed_at` to `spaced_review_items`.
6. Add useful indexes:

```text
chapter_learning_progress(user_id, book_id, mode)
chapter_learning_progress(user_id, book_id, last_activity_at)
chapter_learning_progress(user_id, book_id, status)
reading_plan_schedule_slots(user_id, is_active)
spaced_review_items(source_progress_id)
spaced_review_items(status, due_at)
```

Data migration:

- Existing `spaced_review_items` created from chapter ready are not reliable.
- If the project data can reset, delete existing review items.
- If production data must be preserved, mark old review items `cancelled` and regenerate only after real progress.

Recommended for current project:

```text
Reset or cancel old spaced_review_items, because they were generated from the wrong anchor.
```

---

## 8. DTOs

### 8.1 `app/schemas/learning_progress.py`

```python
class ChapterProgressUpdateRequest(BaseModel):
    mode: PlanMode
    segment_id: int | None = None
    segment_index: int = Field(ge=0)
    position_ms: int = Field(ge=0)
    listened_ms: int = Field(default=0, ge=0)
    total_duration_ms: int | None = Field(default=None, ge=0)
    progress_percent: int | None = Field(default=None, ge=0, le=100)


class ChapterProgressResponse(BaseModel):
    chapter_id: uuid.UUID
    mode: PlanMode
    segment_id: int | None
    segment_index: int
    position_ms: int
    progress_percent: int
    max_progress_percent: int
    status: LearningProgressStatus
    started_at: datetime | None
    last_activity_at: datetime | None
    completed_at: datetime | None


class BookLearningProgressResponse(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    book_progress_percent: int
    completed_chapters: int
    playable_chapters: int
    last_chapter_id: uuid.UUID | None
    last_segment_id: int | None
    last_segment_index: int | None
    position_ms: int | None
    chapters: list[ChapterProgressResponse]
```

Validation rule:

```text
FE may send progress_percent, but backend should compute progress from segment durations when possible.
```

### 8.2 `app/schemas/review.py`

```python
class ReviewActionResponse(BaseModel):
    review_item_id: uuid.UUID
    status: ReviewItemStatus
    completed_at: datetime | None = None
```

---

## 9. Repositories

### 9.1 `learning_progress_repo.py`

Required functions:

```python
def get_progress(session, *, user_id, chapter_id, mode) -> ChapterLearningProgress | None: ...

def upsert_progress(session, *, progress: ChapterLearningProgress) -> ChapterLearningProgress: ...

def list_book_progress(session, *, user_id, book_id, mode) -> list[ChapterLearningProgress]: ...

def has_studied_book_on_local_date(session, *, user_id, book_id, mode, start_utc, end_utc) -> bool: ...

def has_playable_uncompleted_chapter(session, *, user_id, book_id, mode) -> bool: ...

def get_latest_activity(session, *, user_id, book_id, mode) -> ChapterLearningProgress | None: ...
```

Best practice:

- Repositories do not calculate business completion.
- Repositories only read/write DB.
- Services own threshold and business decisions.

### 9.2 `reading_plan_schedule_repo.py`

Required functions:

```python
def count_active_learning_books(session, *, user_id) -> int: ...

def list_active_slots(session, *, user_id) -> list[ReadingPlanScheduleSlot]: ...

def create_slots_for_plan(session, *, user_id, book_id, plan_id, slots) -> list[ReadingPlanScheduleSlot]: ...

def deactivate_slots_for_plan(session, *, plan_id) -> int: ...

def find_conflicting_slot(session, *, user_id, weekday, reminder_time) -> ReadingPlanScheduleSlot | None: ...
```

Use DB unique constraint as the final protection. Catch `IntegrityError` and convert to a domain conflict.

---

## 10. Services

### 10.1 `reading_plan_schedule_service.py`

Responsibilities:

- Parse `ReadingPlan.schedule_config`.
- Expand selected weekdays into normalized slots.
- Validate active book limit.
- Validate schedule conflicts.
- Create slots after `ReadingPlan` is created.

Suggested functions:

```python
def normalize_schedule_config(schedule_config: Any, *, reminder_time: str, timezone: str) -> list[ScheduleSlotInput]:
    ...

def validate_active_learning_capacity(session: Session, *, user_id: uuid.UUID, exclude_book_id: uuid.UUID | None = None) -> None:
    ...

def validate_schedule_slots_available(session: Session, *, user_id: uuid.UUID, slots: list[ScheduleSlotInput]) -> None:
    ...

def create_schedule_slots_for_plan(session: Session, *, user_id: uuid.UUID, book_id: uuid.UUID, plan_id: uuid.UUID, schedule_config: Any) -> None:
    ...
```

Conflict behavior:

```text
Raise domain exception -> router returns 409.
```

Recommended exception:

```python
class ReadingPlanScheduleConflictError(AppException): ...
class ActiveLearningBookLimitExceededError(AppException): ...
```

### 10.2 `learning_progress_service.py`

Responsibilities:

1. Validate book/chapter ownership.
2. Validate segment belongs to chapter/mode.
3. Compute chapter progress.
4. Upsert progress.
5. Detect first completion.
6. Trigger spaced review creation exactly once.
7. Return progress response to FE.

Core rule:

```text
Completion is based on max_progress_percent, not current progress_percent.
```

Progress calculation:

```python
def compute_progress_percent(
    *,
    segment_index: int,
    position_ms: int,
    segment_durations: list[int | None],
    fallback_percent: int | None,
) -> tuple[int, int]:
    total = sum(duration or 0 for duration in segment_durations)
    if total > 0:
        before = sum((duration or 0) for duration in segment_durations[:segment_index])
        current = min(total, before + max(0, position_ms))
        return int(current * 100 / total), total
    return min(max(fallback_percent or 0, 0), 100), 0
```

Upsert rule:

```text
If existing status is completed:
  keep completed_at unchanged.
  keep status completed.
  still update resume position and last_activity_at.
```

Completion trigger:

```python
crossed_completion = (
    existing.completed_at is None
    and new_max_progress >= settings.LEARNING_COMPLETION_THRESHOLD_PERCENT
)
```

Manual complete:

```text
Manual complete should set progress_percent=max_progress_percent=100,
status=completed,
completed_at=now,
then create spaced_review_items once.
```

### 10.3 `spaced_review_service.py`

Current function:

```python
create_spaced_reviews_for_chapter(... base_time=now)
```

Replace or add:

```python
def create_spaced_reviews_after_completion(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    mode: PlanMode,
    review_text: str,
    completed_at: datetime,
    source_progress_id: uuid.UUID,
) -> list[SpacedReviewItem]:
    ...
```

Rules:

- `due_at = completed_at + interval_days`.
- `anchor_completed_at = completed_at`.
- `source_progress_id = progress.id`.
- Do not create another review chain if one active chain already exists for the same user/chapter unless product explicitly supports per-mode chains.

Capstone-compatible check:

```text
Before creating items, check existing non-cancelled items by user_id + chapter_id.
If found, return [].
```

Trade-off:

- Current DB unique is `(user_id, chapter_id, mode, interval_days)`.
- That still permits duplicate chains across modes.
- Service-level check prevents this now.
- A future migration can change uniqueness if product decides one chain per chapter permanently.

### 10.4 `notification_event_service.py`

Current issue:

```python
create_chapter_ready_learning_events()
```

currently creates both:

```text
spaced_review_items
content_ready outbox
```

Change to:

```text
chapter ready -> content_ready only
chapter completed -> spaced_review_items
```

Recommended rename:

```python
create_chapter_ready_content_events(...)
create_chapter_completed_learning_events(...)
```

Content-ready aggregation:

Add:

```python
def create_first_playable_ready_outbox_once(...): ...
def create_book_ready_outbox_once(...): ...
```

Use idempotency keys:

```text
content-ready:first-playable:<user_id>:<book_id>:<mode>
content-ready:book-ready:<user_id>:<book_id>:<mode>
```

Plan reminder filter changes:

In `_build_plan_reminder_outbox(...)`, add:

```text
1. has_playable_uncompleted_chapter(...)
2. has_studied_book_on_local_date(...)
3. idempotency includes plan_id
```

New idempotency:

```text
plan:<user_id>:<book_id>:<plan_id>:<local_date>
```

Review outbox safety:

In `_build_review_outbox(...)`, verify:

```text
source ChapterLearningProgress exists and status == completed.
```

This protects the system even if bad old review rows exist.

### 10.5 `notification_copy_service.py`

Update copy to support content-ready subtypes in payload:

```python
if notification_type == NotificationType.CONTENT_READY:
    subtype = payload.get("subtype")
    if subtype == "first_playable":
        return ("Có thể bắt đầu nghe rồi", f"{book_title} đã có chương đầu tiên sẵn sàng.")
    if subtype == "book_ready":
        return ("Sách đã sẵn sàng", f"{book_title} đã được xử lý xong.")
```

Do not add LLM-generated copy yet.

Reason:

- Notification copy must be cheap, deterministic, and debuggable.
- Push notification later should not depend on LLM latency.

---

## 11. API Contracts

### 11.1 Update Chapter Progress

```text
PUT /api/v1/books/{book_id}/chapters/{chapter_id}/progress
```

Request:

```json
{
  "mode": "full",
  "segment_id": 12,
  "segment_index": 3,
  "position_ms": 92000,
  "listened_ms": 410000,
  "total_duration_ms": 500000,
  "progress_percent": 82
}
```

Response:

```json
{
  "chapter_id": "...",
  "mode": "full",
  "segment_id": 12,
  "segment_index": 3,
  "position_ms": 92000,
  "progress_percent": 82,
  "max_progress_percent": 82,
  "status": "completed",
  "started_at": "...",
  "last_activity_at": "...",
  "completed_at": "..."
}
```

Status behavior:

| Situation | Result |
| --- | --- |
| First progress event | `in_progress`, set `started_at` |
| Progress below threshold | update resume fields only |
| Cross 80 percent first time | set `completed`, create review items |
| Already completed and user seeks back | keep `completed_at`, update resume |

### 11.2 Manual Complete Chapter

```text
POST /api/v1/books/{book_id}/chapters/{chapter_id}/complete
```

Request:

```json
{
  "mode": "full"
}
```

Behavior:

- Set progress to completed.
- Create spaced review items once.
- Return chapter progress response.

### 11.3 Book Learning Progress

```text
GET /api/v1/books/{book_id}/learning-progress?mode=full
```

Response:

```json
{
  "book_id": "...",
  "mode": "full",
  "book_progress_percent": 42,
  "completed_chapters": 1,
  "playable_chapters": 3,
  "last_chapter_id": "...",
  "last_segment_id": 12,
  "last_segment_index": 3,
  "position_ms": 92000,
  "chapters": []
}
```

FE uses this for:

- progress bar;
- continue listening;
- deciding whether to show "resume" button.

### 11.4 Review Complete/Skip

```text
POST /api/v1/reviews/{review_item_id}/complete
POST /api/v1/reviews/{review_item_id}/skip
```

Response:

```json
{
  "review_item_id": "...",
  "status": "completed",
  "completed_at": "..."
}
```

Rules:

- User can only update own review item.
- `completed_at` set once.
- `skip` sets `status=skipped`.
- Future review analytics can use this.

---

## 12. Router Wiring

Add:

```text
app/api/v1/routers/learning_progress.py
app/api/v1/routers/reviews.py
```

Register in `app/main.py`:

```python
api_router.include_router(learning_progress.router, prefix="/api/v1", tags=["learning-progress"])
api_router.include_router(reviews.router, prefix="/api/v1", tags=["reviews"])
```

Current project still uses mock user in several routers. Keep the same mock-user pattern for now, but isolate it:

```python
# TODO: Replace with JWT user later.
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")
```

When Auth is implemented, these services should already accept `user_id`, so replacing mock user is straightforward.

---

## 13. Worker Integration

### 13.1 `chapter_worker.py`

Current:

```text
after chapter ready -> create_chapter_ready_learning_events()
```

Required change:

```text
after chapter ready -> create content-ready event only
```

Do not create spaced review here.

### 13.2 `book_pipeline.py`

Create content-ready aggregation at the correct milestones:

```text
first useful playable chapter ready -> first_playable content_ready
all chapters ready -> book_ready content_ready
```

Where to hook:

- When job/book becomes `partial_ready`, call first-playable outbox helper.
- When job/book becomes `ready`, call book-ready outbox helper.

Important:

```text
Use idempotency keys so repeated worker retries do not duplicate notifications.
```

---

## 14. Celery Notification Changes

`app/tasks/notification_tasks.py` does not need a new queue for Phase 4.2.

Keep:

```text
scan_due -> maintenance
deliver_due -> notification
```

But scanner business logic changes:

```text
scan_due
-> recover stale outbox
-> create due review outbox only for completed chapters
-> create due plan reminder only if progress rules allow
-> enqueue delivery if due outbox exists
```

No Celery ETA/countdown.

Postgres remains source of truth.

---

## 15. Reading Plan Guardrails

### 15.1 Schedule Conflict

When creating a reading plan:

```text
1. Load user notification settings for timezone/reminder_time.
2. Expand `schedule_config` into weekdays.
3. Build slots: weekday + reminder_time.
4. Check active slots for same user.
5. If conflict exists, return 409.
6. Create ReadingPlan.
7. Create ReadingPlanScheduleSlot rows.
```

Example conflict response:

```json
{
  "detail": "Lịch học bị trùng với một sách khác.",
  "code": "reading_plan_schedule_conflict",
  "conflict": {
    "book_id": "...",
    "plan_id": "...",
    "weekday": 1,
    "reminder_time": "20:00"
  }
}
```

### 15.2 Max Active Learning Books

Rule:

```text
Count distinct books that have active reading plans and are not fully completed.
If count >= MAX_ACTIVE_LEARNING_BOOKS_PER_USER, reject new active plan.
```

Important:

```text
Do not count archived/inactive/completed books.
```

Since book completion is derived from progress, service can initially use:

```text
active ReadingPlan count by distinct book_id
```

Then improve after book completion summary exists.

---

## 16. Plan Reminder Production Filter

Current query:

```text
active plans + book partial_ready/ready
```

New required filters:

```text
active plan
book partial_ready/ready
weekday/reminder time due
user reminders_enabled
not quiet hours
daily cap available
has playable uncompleted chapter
user has not studied this book today
idempotency key not existing
```

Implementation helpers:

```python
def has_playable_uncompleted_chapter(session, *, user_id, book_id, mode) -> bool:
    ...

def has_studied_book_on_local_date(session, *, user_id, book_id, mode, local_date, timezone_name) -> bool:
    ...
```

Definition of studied today:

```text
Any chapter_learning_progress.last_activity_at within user's local day.
```

Definition of playable chapter:

```text
Chapter has at least one ChapterSegment for the plan mode.
```

Definition of uncompleted:

```text
No progress row exists
OR progress.status != completed.
```

---

## 17. Spaced Review Production Filter

Do not assume existing review items are clean.

Before creating a review notification:

```text
1. Load review item.
2. Load linked chapter progress by source_progress_id or user/chapter/mode.
3. If no completed progress exists, skip or cancel old review item.
4. Apply user spaced_review_enabled.
5. Apply quiet hours and daily cap.
6. Create outbox idempotently.
7. Mark review item due and set notified_at.
```

Recommended handling for old invalid rows:

```text
If review item has no completed progress, mark it cancelled.
```

This prevents old Phase 4.1 rows from leaking into production behavior.

---

## 18. Content Ready Aggregation

Current behavior may create per-chapter content-ready rows.

Replace with:

```text
first_playable_ready
book_ready
```

Payload example:

```json
{
  "subtype": "first_playable",
  "book_id": "...",
  "book_title": "Chương 4 - Phương pháp luận nghiên cứu",
  "mode": "full",
  "first_chapter_id": "...",
  "action_type": "open_book",
  "action_payload": {
    "book_id": "...",
    "mode": "full"
  }
}
```

Idempotency:

```text
content-ready:first-playable:<user_id>:<book_id>:<mode>
content-ready:book-ready:<user_id>:<book_id>:<mode>
```

Why:

- User only needs to know when they can start.
- User may also appreciate knowing the full book is ready.
- Sending one notification per chapter is noisy.

---

## 19. Tests

### 19.1 Schedule Guardrails

File:

```text
tests/test_reading_plan_schedule_guardrails.py
```

Cases:

- Create first active plan succeeds.
- Create second active plan with same weekday/time returns conflict.
- Create second active plan with different weekday succeeds.
- Create second active plan with same weekday but different time succeeds.
- Max active learning books reached returns conflict.
- Inactive plan slots do not block new plan.

### 19.2 Learning Progress

File:

```text
tests/test_learning_progress_service.py
```

Cases:

- New progress row starts as `in_progress`.
- Segment index and position are persisted.
- Progress below 80 does not create review items.
- Progress 82 creates review items.
- Repeating 82 does not duplicate review items.
- Seeking backward after completion does not unset completion.
- Manual complete creates review items once.
- Book progress derives from chapter progress.

### 19.3 API

File:

```text
tests/test_learning_progress_api.py
```

Cases:

- `PUT /books/{book_id}/chapters/{chapter_id}/progress`.
- Invalid chapter/book relation returns 404 or 422.
- Invalid segment/mode relation returns 422.
- `GET /books/{book_id}/learning-progress`.
- Manual complete endpoint.

### 19.4 Notification Filters

File:

```text
tests/test_notification_plan_reminder_filters.py
```

Cases:

- Plan reminder skipped if no playable uncompleted chapter.
- Plan reminder skipped if user already studied today.
- Plan reminder created if due and user has not studied.
- Review outbox not created for uncompleted chapter.
- Review outbox created for completed chapter.
- Old invalid review item is cancelled or ignored.

### 19.5 Regression

Run existing Phase 4 tests:

```powershell
uv run pytest tests/test_notification_services.py tests/test_notification_outbox_repo.py tests/test_notifications_api.py -q
```

---

## 20. Manual Test Flow

Use a real generated book with playable segments.

### Step 1 - Generate Book

```text
POST /upload
POST /generate-plan
wait until partial_ready or ready
```

Expected:

```text
content_ready:first_playable outbox created once.
No spaced_review_items yet.
```

### Step 2 - Report 50 Percent Progress

```text
PUT /books/{book_id}/chapters/{chapter_id}/progress
progress_percent=50
```

Expected:

```text
chapter_learning_progress.status = in_progress
spaced_review_items count = 0
```

### Step 3 - Report 82 Percent Progress

```text
PUT /books/{book_id}/chapters/{chapter_id}/progress
progress_percent=82
```

Expected:

```text
chapter_learning_progress.status = completed
completed_at is set
spaced_review_items created for 1,3,7,14,30 days
```

### Step 4 - Repeat 82 Percent

Expected:

```text
No duplicate spaced_review_items.
```

### Step 5 - Force Review Due

Set one review due in DB:

```sql
update spaced_review_items
set due_at = now() - interval '1 minute'
where chapter_id = '<chapter_id>'
limit 1;
```

Run Beat/worker or call scanner task.

Expected:

```text
spaced_review_due outbox created.
delivery creates user_notifications.
```

### Step 6 - Plan Reminder Studied Today

If `last_activity_at` is today:

```text
scan_due should not create plan_reminder.
```

If `last_activity_at` is old and schedule is due:

```text
scan_due may create plan_reminder.
```

---

## 21. Backward Compatibility

### FE Compatibility

Existing notification endpoints remain unchanged:

```text
GET /notifications
PATCH /notifications/{id}/read
PATCH /notifications/read-all
GET /notifications/settings
PUT /notifications/settings
```

New FE requirements:

```text
FE must report playback progress.
FE should call learning-progress endpoint for continue listening.
FE should handle schedule conflict 409.
FE should call review complete/skip when user finishes a review.
```

### DB Compatibility

If test data can reset:

```text
Delete old spaced_review_items generated from chapter ready.
```

If not:

```text
Mark old rows cancelled unless a completed progress row exists.
```

### Worker Compatibility

Document worker still creates audio/RAG.

But:

```text
Document worker no longer creates spaced review schedules.
```

---

## 22. Implementation Order

Do this in small commits:

1. Add constants/config/exceptions.
2. Add DB models and migration.
3. Add schedule slot repo/service and tests.
4. Integrate schedule guardrails into generate-plan.
5. Add learning progress schemas/repo/service.
6. Add learning progress router and tests.
7. Move spaced review creation to completion event.
8. Remove spaced review creation from chapter-ready worker path.
9. Add review complete/skip API.
10. Improve plan reminder filters.
11. Implement first-playable/book-ready content-ready aggregation.
12. Run focused tests.
13. Run one manual end-to-end flow.

Avoid doing Auth/Push in the same branch.

Reason:

```text
Auth and Push introduce new failure surfaces.
Phase 4.2 should first make the learning logic correct.
```

---

## 23. Best Practice Rules

- Routers stay thin.
- Services own business logic.
- Repositories own DB access.
- Workers call service functions with IDs and primitive values.
- Do not trust FE ownership claims; validate user/book/chapter/segment.
- Do not trust FE `progress_percent` if backend can compute from durations.
- Use `max_progress_percent` for completion.
- Do not create spaced review from chapter ready.
- Do not send review notification for uncompleted chapters.
- Do not send plan reminder if user studied the book today.
- Use DB unique constraints for idempotency.
- Keep Redis as broker only.
- Keep Postgres as source of truth.
- Do not log raw study content or private notification payloads.

---

## 24. Definition Of Done

Phase 4.2 is complete when:

```text
1. User cannot create overlapping active study slots.
2. User cannot exceed active learning book limit.
3. FE can save and resume segment-level playback position.
4. Backend derives chapter and book progress.
5. Chapter completion is detected at 80 percent or manual complete.
6. Spaced review items are created only after chapter completion.
7. Old invalid review rows cannot produce notifications.
8. Content-ready is aggregated into first-playable/book-ready.
9. Plan reminder skips users who already studied today.
10. Review complete/skip endpoints work.
11. Existing in-app notification API still works.
12. Focused tests pass.
13. Manual runtime flow proves scanner and delivery still work.
```

Recommended command set:

```powershell
uv run alembic upgrade head
uv run pytest tests/test_reading_plan_schedule_guardrails.py tests/test_learning_progress_service.py tests/test_learning_progress_api.py tests/test_completion_based_spaced_review.py tests/test_notification_plan_reminder_filters.py -q
uv run pytest tests/test_notification_services.py tests/test_notification_outbox_repo.py tests/test_notifications_api.py -q
```

---

## 25. Senior Notes

This phase is the bridge between "notification exists" and "notification is pedagogically correct".

The most important invariant:

```text
Review follows learning.
Learning is proven by progress/completion.
Generation is not learning.
```

If this invariant holds, Auth and Push can be added safely later.

If this invariant does not hold, Push will only deliver wrong reminders faster.
