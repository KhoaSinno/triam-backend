study_context# Phase 11 Implementation Guide - Learning Progress Completion State And Review Access

Date: 2026-06-11  
Status: **Implementation plan only, not source code yet**  
Depends on:

- `_docs_implemented/phase_4_2_production_learning_loop_implementation_guide.md`
- `_docs_implemented/phase_7_2_deferred_reading_plan_activation_implementation_guide.md`
- `_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md`

Audience: Backend developer, Flutter developer, capstone reviewer

---

## 1. Goal

Phase 11 xử lý trước phần **progress/completion** để hệ thống biết rõ user đã học tới đâu và đã hoàn thành sách hay chưa.

Vấn đề hiện tại:

```text
Book.status = ready
ReadingPlan.status = inactive
FE hiểu nhầm đây là sách đã sẵn sàng nhưng chưa bắt đầu
=> UI hiện CTA "Bắt đầu học lại" hoặc reset như sách mới
```

Trong khi business thật là:

```text
Sách đã xử lý audio xong
User đã học hết các learning units
Plan không còn cần reminder học nữa
Nhưng sách phải được hiển thị là "Đã hoàn thành" và vẫn có thể ôn tập
```

Mục tiêu sau Phase 11:

- Tách rõ trạng thái xử lý sách, trạng thái kế hoạch học, và trạng thái học tập của user.
- Không dùng `inactive` để đại diện cho cả "chưa bắt đầu", "đã tạm dừng", và "đã hoàn thành".
- Khi user học xong sách, backend trả được `learning_status=completed`.
- FE có thể render đúng CTA: tiếp tục học, đã hoàn thành, ôn tập, nghe lại.
- Nút "Ôn" trong book detail có API để lấy review items, không phụ thuộc notification.
- Chuẩn bị nền cho Phase 12 planner theo ngày/tháng/năm.

---

## 2. Core Decision

Không nên tiếp tục suy ra trạng thái học tập từ `Book.status` hoặc `ReadingPlan.status`.

Phase 11 chốt 3 nhóm trạng thái riêng:

| Nhóm | Field | Ý nghĩa |
| --- | --- | --- |
| Xử lý sách/audio | `Book.status` | Backend đã parse/generate audio tới đâu |
| Lịch học | `ReadingPlan.status` | Plan đang active, inactive, completed, error |
| Tiến độ học của user | `BookLearningState.status` | User chưa học, đang học, đã học xong |

### 2.1 Book.status

Giữ nguyên ý nghĩa hiện tại:

```text
draft         Upload xong, chưa generate plan
processing    Đang xử lý nội dung/audio
partial_ready Có nội dung đầu tiên nghe được
ready         Xử lý xong toàn bộ nội dung/audio
error         Xử lý lỗi
```

Không dùng `Book.status=ready` để hiểu là user đã học xong.

### 2.2 ReadingPlan.status

Mở rộng:

```text
inactive   Đã cấu hình nhưng chưa active, hoặc user pause
active     Đang có lịch học/reminder
completed  Plan đã hoàn thành vì user học xong các unit thuộc plan
error      Plan lỗi
```

Quan trọng:

```text
completed != inactive
```

Nếu plan đã completed thì không nên hiện như plan chưa bắt đầu.

### 2.3 BookLearningState.status

Thêm trạng thái riêng cho user:

```text
not_started  User chưa học unit nào
in_progress  User đã học một phần
completed    User đã hoàn thành toàn bộ playable units
```

Đây là source of truth cho UI học tập.

---

## 3. Scope

### 3.1 In Scope

Implement:

1. Add `BookLearningState` model/table.
2. Add `PlanStatus.COMPLETED`.
3. Update progress service để sync book-level learning state.
4. Khi hoàn thành toàn bộ playable units:
   - set `BookLearningState.status=completed`;
   - set `BookLearningState.completed_at`;
   - set `ReadingPlan.status=completed`;
   - delete/deactivate active schedule slots để không nhắc học tiếp.
5. Extend `GET /api/v1/books/{book_id}/learning-progress`.
6. Extend `GET /api/v1/books/{book_id}/details`.
7. Optional but recommended: extend `GET /api/v1/books`.
8. Add review list endpoints để FE mở màn hình ôn tập từ book detail.
9. Add tests cho completion, CTA state, review access.
10. Update Flutter contract after implementation.

### 3.2 Out Of Scope

Không implement trong phase này:

- Planner theo ngày/tháng/năm.
- Calendar sessions.
- Firebase push notification.
- Adaptive spaced review bằng ML.
- Restart/learn-again flow phức tạp.
- Multi-user shared system book refactor toàn bộ.

Những phần trên để Phase 12+.

---

## 4. Why This Phase Must Come Before Planner

Planner trả lời câu hỏi:

```text
User nên học vào ngày giờ nào?
```

Progress/completion trả lời câu hỏi:

```text
User đã học tới đâu?
User đã học xong chưa?
Còn unit nào cần học không?
Có item nào cần ôn không?
```

Nếu progress sai, planner dù đúng ngày giờ vẫn sẽ nhắc sai, mở sai CTA, hoặc reset sách đã hoàn thành thành sách mới.

Vì vậy thứ tự đúng:

```text
Phase 11: learning truth
Phase 12: calendar planner
Phase 13: notification/review polish
```

---

## 5. Database Design

### 5.1 New Table: book_learning_states

File:

```text
app/models/db_models.py
```

Add model:

```python
class BookLearningState(SQLModel, table=True):
    __tablename__ = "book_learning_states"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: uuid.UUID = Field(index=True)
    book_id: uuid.UUID = Field(foreign_key="books.id", index=True)
    mode: str = Field(default=Mode.full.value, index=True)

    status: str = Field(default="not_started", index=True)

    book_progress_percent: float = Field(default=0.0)
    completed_units: int = Field(default=0)
    playable_units: int = Field(default=0)

    last_learning_unit_id: uuid.UUID | None = Field(default=None, foreign_key="learning_units.id")
    last_segment_id: uuid.UUID | None = Field(default=None, foreign_key="learning_unit_segments.id")
    last_segment_index: int | None = None
    position_ms: int = Field(default=0)

    started_at: datetime | None = None
    last_activity_at: datetime | None = None
    completed_at: datetime | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", "mode", name="uq_book_learning_state_user_book_mode"),
        Index("ix_book_learning_states_user_status", "user_id", "status"),
        Index("ix_book_learning_states_book_mode", "book_id", "mode"),
    )
```

### 5.2 Why Use A Separate Table?

Không nên nhét thêm toàn bộ trạng thái vào `ReadingPlan` vì:

- Một plan là cấu hình lịch học.
- Progress là kết quả user học thật.
- Sau này có thể có nhiều plan, học lại, hoặc shared/system book.
- Review vẫn cần hoạt động sau khi plan học đã hoàn thành.

`BookLearningState` là bảng tổng hợp để FE đọc nhanh, còn `LearningUnitProgress` vẫn là dữ liệu chi tiết theo unit/segment.

### 5.3 Status Column Type

Recommended:

```python
status: str = Field(default="not_started", index=True)
```

Không dùng PostgreSQL enum ở phase này.

Lý do:

- Dự án từng gặp lỗi Alembic/Postgres enum duplicate.
- `ReadingPlan.status` hiện cũng đang là text-like field.
- Với trạng thái app-level nhỏ, validate bằng Python enum/service là đủ.

Trade-off:

- DB không tự enforce enum value.
- Cần service/test đảm bảo chỉ ghi giá trị hợp lệ.

Nếu sau này hệ thống ổn định, có thể migrate sang DB enum.

---

## 6. Constants

File:

```text
app/core/constant.py
```

Add:

```python
class BookLearningStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
```

Update:

```python
class PlanStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    ERROR = "error"
```

Rule:

- `PlanStatus.INACTIVE`: chưa active hoặc user pause.
- `PlanStatus.COMPLETED`: user đã học xong plan.
- Không dùng `inactive` cho completed nữa.

---

## 7. Migration Plan

Create migration:

```powershell
uv run alembic revision -m "phase 11 learning completion state"
```

Migration should:

1. Create `book_learning_states`.
2. Add nullable `completed_at` to `reading_plans`.
3. Optional: add nullable `started_at`, `paused_at` to `reading_plans`.
4. Backfill existing progress.

### 7.1 ReadingPlan Columns

Recommended additions:

```text
reading_plans.started_at nullable timestamp
reading_plans.paused_at nullable timestamp
reading_plans.completed_at nullable timestamp
```

Why:

- FE can show "Hoàn thành lúc ...".
- Reminder scanner can skip completed plans cleanly.
- Later planner can know actual lifecycle timestamps.

### 7.2 Backfill Logic

Pseudo:

```text
for each user_id, book_id, mode found in learning_unit_progress:
  playable_units = count learning_units in book/mode that have at least one segment
  completed_units = count progress rows with status=completed
  latest_progress = latest progress row by last_activity_at/updated_at

  if playable_units == 0:
    status = not_started
  elif completed_units >= playable_units:
    status = completed
  elif any progress exists:
    status = in_progress
  else:
    status = not_started

  insert book_learning_states
```

Then:

```text
for each reading_plan:
  if matching book_learning_state.status == completed:
    reading_plan.status = completed
    reading_plan.completed_at = book_learning_state.completed_at
    delete active schedule slots
```

Important:

- Do not mark completed when `playable_units=0`.
- If old data is dirty, prefer `in_progress` over accidentally `completed`.

---

## 8. Repository Layer

Create:

```text
app/repositories/book_learning_state_repo.py
```

Functions:

```python
def get_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: str,
) -> BookLearningState | None:
    ...


def upsert_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: str,
    status: str,
    book_progress_percent: float,
    completed_units: int,
    playable_units: int,
    last_learning_unit_id: uuid.UUID | None,
    last_segment_id: uuid.UUID | None,
    last_segment_index: int | None,
    position_ms: int,
    started_at: datetime | None,
    last_activity_at: datetime | None,
    completed_at: datetime | None,
) -> BookLearningState:
    ...
```

Rules:

- Repository only reads/writes DB.
- No business decision inside repository.
- Service owns status calculation.
- Use unique `(user_id, book_id, mode)` for idempotency.

---

## 9. Service Layer

File:

```text
app/services/learning_progress_service.py
```

Add helper:

```python
def sync_book_learning_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: str,
) -> BookLearningState:
    ...
```

### 9.1 Sync Algorithm

Pseudo:

```python
def sync_book_learning_state(session, *, user_id, book_id, mode):
    playable_units = count_playable_units(session, book_id=book_id, mode=mode)
    unit_progress_rows = list_unit_progress(session, user_id=user_id, book_id=book_id, mode=mode)

    completed_units = count rows where status == completed
    latest = latest row by last_activity_at / updated_at

    if playable_units == 0:
        status = BookLearningStatus.NOT_STARTED
        progress_percent = 0
    else:
        progress_percent = min(100, completed_units / playable_units * 100)
        if completed_units >= playable_units:
            status = BookLearningStatus.COMPLETED
        elif unit_progress_rows:
            status = BookLearningStatus.IN_PROGRESS
        else:
            status = BookLearningStatus.NOT_STARTED

    completed_at = now if status just changed to completed else existing.completed_at

    state = upsert_book_learning_state(...)

    if status == BookLearningStatus.COMPLETED:
        complete_reading_plan_and_clear_slots(...)

    return state
```

### 9.2 Completion Rule

Unit completion remains:

```text
max_progress_percent >= LEARNING_COMPLETION_THRESHOLD_PERCENT
or manual complete button
```

Book completion:

```text
completed_units >= playable_units
and playable_units > 0
```

This means:

- User does not need to listen to exactly 100 percent of every unit.
- Threshold remains configurable.
- Manual complete still works.

### 9.3 Replace Current Auto-Deactivate Logic

Current behavior to replace:

```text
all units complete
-> reading_plan.status = inactive
-> delete slots
```

New behavior:

```text
all units complete
-> book_learning_state.status = completed
-> reading_plan.status = completed
-> reading_plan.completed_at = now
-> delete active slots
```

The schedule slots should still be removed because study reminders are no longer needed.

But the plan status must not become `inactive`.

### 9.4 Resume Behavior

For `POST /api/v1/books/{book_id}/resume`:

```text
if learning_status == completed:
  return 409 with message:
  "Sách đã hoàn thành. Hãy dùng chức năng ôn tập hoặc học lại nếu muốn bắt đầu vòng mới."
```

Do not silently reactivate a completed plan.

Later phase can add:

```text
POST /api/v1/books/{book_id}/restart-learning
```

But do not add it in Phase 11 unless FE explicitly needs it.

---

## 10. API Contract

### 10.1 GET /api/v1/books/{book_id}/learning-progress

Current response should be extended.

Add fields:

```json
{
  "book_id": "uuid",
  "mode": "full",
  "learning_status": "completed",
  "is_completed": true,
  "can_resume": false,
  "can_review": true,
  "book_progress_percent": 100,
  "completed_units": 12,
  "playable_units": 12,
  "started_at": "2026-06-11T09:00:00Z",
  "last_activity_at": "2026-06-11T10:20:00Z",
  "completed_at": "2026-06-11T10:20:00Z",
  "resume": null,
  "units": []
}
```

Rules:

- `learning_status` is required.
- `is_completed = learning_status == "completed"`.
- `can_resume = learning_status == "in_progress"`.
- `can_review = true` if due/upcoming/completed review items exist, or completed units have review content.
- Existing fields should remain backward compatible.

### 10.2 GET /api/v1/books/{book_id}/details

Add:

```json
{
  "learning_summary": {
    "learning_status": "in_progress",
    "book_progress_percent": 45,
    "completed_units": 5,
    "playable_units": 12,
    "is_completed": false,
    "can_resume": true,
    "can_review": true,
    "completed_at": null,
    "due_reviews_count": 2,
    "upcoming_reviews_count": 4
  }
}
```

Why:

- Book detail is the page where FE decides main CTA.
- Avoid making FE infer from `book_status` and `plan_status`.
- Avoid extra network call if FE already loads details.

### 10.3 GET /api/v1/books

Recommended add minimal fields per item:

```json
{
  "id": "uuid",
  "title": "Book title",
  "status": "ready",
  "learning_status": "completed",
  "book_progress_percent": 100,
  "completed_at": "2026-06-11T10:20:00Z"
}
```

This helps Library render:

```text
Đang xử lý
Sẵn sàng học
Đang học
Đã hoàn thành
Lỗi
```

without calling detail for every book.

### 10.4 GET /api/v1/books/{book_id}/reading-plan

Response should support:

```json
{
  "book_id": "uuid",
  "plan_id": "uuid",
  "plan_status": "completed",
  "status": "completed",
  "completed_at": "2026-06-11T10:20:00Z",
  "active_slots": []
}
```

Keep both `status` and `plan_status` if current FE already expects `status`.

---

## 11. Review Access API

Current issue:

```text
FE has a Review button in book detail,
but backend only supports complete/skip by review_item_id.
If user did not enter from notification, FE may not know review_item_id.
```

Phase 11 should add list/detail endpoints.

### 11.1 GET /api/v1/reviews

Query:

```text
status=due|upcoming|completed|skipped|all
book_id=optional uuid
mode=optional full|pareto
limit=optional
offset=optional
```

Response:

```json
{
  "items": [
    {
      "review_item_id": "uuid",
      "book_id": "uuid",
      "book_title": "Of Mice and Men",
      "learning_unit_id": "uuid",
      "learning_unit_title": "Chapter 4",
      "mode": "full",
      "status": "pending",
      "due_at": "2026-06-12T13:00:00Z",
      "interval_days": 1,
      "review_text": "Short review content...",
      "review_audio_url": "https://...",
      "completed_at": null,
      "skipped_at": null
    }
  ],
  "total": 1
}
```

### 11.2 GET /api/v1/books/{book_id}/reviews

Same response, book-scoped.

Recommended for FE book detail:

```text
Tap "Ôn tập"
-> GET /books/{book_id}/reviews?status=due
-> if empty, GET /books/{book_id}/reviews?status=upcoming
-> show review screen or upcoming schedule
```

### 11.3 GET /api/v1/reviews/{review_item_id}

Return one review item with full context.

### 11.4 Existing Endpoints Stay

Keep:

```text
POST /api/v1/reviews/{review_item_id}/complete
POST /api/v1/reviews/{review_item_id}/skip
```

They should update review item status and can optionally refresh `BookLearningState.can_review` summary later.

---

## 12. Notification And Reminder Rules

Phase 11 should update reminder filters:

```text
Plan reminder should skip ReadingPlan.status=completed.
```

Current `has_playable_uncompleted_unit` is still useful, but `completed` status makes the logic explicit.

Rules:

- Completed learning plan should not receive "tiếp tục học" reminders.
- Spaced review reminders still work after completion.
- Book completed notification can be generated once if product wants it, but avoid adding push behavior in this phase.

---

## 13. FE UI Rules After Phase 11

FE should no longer decide learning CTA from only:

```text
book.status
reading_plan.status
```

Use:

```text
book.status           processing/audio readiness
learning_status       user's real learning state
plan_status           schedule state
```

### 13.1 Library Card

Recommended display:

| Backend state | FE label | Main CTA |
| --- | --- | --- |
| `book.status=draft` | Chưa tạo kế hoạch | Tạo kế hoạch |
| `book.status=processing` | Đang xử lý | Xem tiến độ |
| `book.status=partial_ready`, `learning_status=not_started` | Có thể bắt đầu | Bắt đầu học |
| `book.status=ready`, `learning_status=not_started` | Sẵn sàng học | Bắt đầu học |
| `learning_status=in_progress` | Đang học | Tiếp tục |
| `learning_status=completed` | Đã hoàn thành | Ôn tập |
| `book.status=error` | Lỗi xử lý | Thử lại/Xóa |

### 13.2 Book Detail CTA

```text
if learning_status == completed:
  primary CTA = Ôn tập
  secondary CTA = Nghe lại
elif learning_status == in_progress:
  primary CTA = Tiếp tục học
elif book is playable:
  primary CTA = Bắt đầu học
else:
  primary CTA = Xem tiến độ xử lý
```

### 13.3 Review Screen

FE should support:

```text
Ôn tập hôm nay
Sắp tới
Đã hoàn thành
Bỏ qua
```

This can use `GET /api/v1/reviews`.

---

## 14. Tests Required

### 14.1 Unit/Service Tests

Add/update:

```text
tests/test_learning_progress_service.py
tests/test_phase11_learning_completion_state.py
```

Cases:

1. First progress update creates `BookLearningState(status=in_progress)`.
2. Completing one unit updates completed count.
3. Completing final playable unit sets:
   - `BookLearningState.status=completed`;
   - `BookLearningState.completed_at`;
   - `ReadingPlan.status=completed`;
   - no active schedule slots.
4. `playable_units=0` never becomes completed.
5. Manual complete follows the same sync path as playback progress.
6. Repeating complete is idempotent.
7. Completed plan does not receive plan reminder.

### 14.2 API Tests

Add/update:

```text
tests/test_learning_progress_api.py
tests/test_reviews_api.py
tests/test_book_details_learning_summary.py
```

Cases:

1. `GET /books/{book_id}/learning-progress` returns `learning_status`.
2. Completed book returns `is_completed=true`, `can_resume=false`, `can_review=true`.
3. `GET /books/{book_id}/details` includes `learning_summary`.
4. `GET /books/{book_id}/reviews?status=due` returns review items for that user/book only.
5. User A cannot see user B review items.
6. Completed book resume returns 409 or a documented non-reactivation response.

### 14.3 Regression Test For Current Bug

Create direct regression:

```text
Given:
  book.status = ready
  all playable units completed
When:
  FE calls book detail/progress
Then:
  response.learning_status = completed
  response.plan_status = completed
  response.can_resume = false
  response.can_review = true
```

This prevents the old UI bug from coming back.

---

## 15. Manual Test Flow

Use a real uploaded book.

```text
1. Upload document.
2. Generate plan.
3. Wait until partial_ready/ready.
4. Start/resume plan.
5. Update progress for each learning unit to >= 80 percent.
6. Call GET /books/{book_id}/learning-progress.
7. Call GET /books/{book_id}/details.
8. Call GET /books/{book_id}/reading-plan.
9. Call GET /books/{book_id}/reviews?status=due.
```

Expected:

```text
Book.status remains ready.
ReadingPlan.status becomes completed.
BookLearningState.status becomes completed.
No active schedule slot remains.
Review items exist based on completed units.
FE can show "Đã hoàn thành" and "Ôn tập".
```

---

## 16. Implementation Order

### Step 1 - Schema

Files:

```text
app/models/db_models.py
app/core/constant.py
app/db/migrations/versions/<revision>_phase_11_learning_completion_state.py
```

Implement:

- `BookLearningState`
- `BookLearningStatus`
- `PlanStatus.COMPLETED`
- `reading_plans.completed_at`
- migration + backfill

### Step 2 - Repository

Files:

```text
app/repositories/book_learning_state_repo.py
app/repositories/learning_progress_repo.py
app/repositories/review_repo.py
```

Implement:

- fetch/upsert state
- count playable units
- count completed units
- list review items by user/book/status

### Step 3 - Service

Files:

```text
app/services/learning_progress_service.py
app/services/review_service.py
app/services/reading_plan_schedule_service.py
```

Implement:

- `sync_book_learning_state`
- replace auto-inactive completion behavior
- skip completed plans in reminder filters
- review list service

### Step 4 - API DTO

Files:

```text
app/schemas/learning_progress.py
app/schemas/review.py
app/schemas/audiobook.py
```

Implement:

- `BookLearningSummary`
- extended progress response
- review list response

### Step 5 - Routers

Files:

```text
app/api/v1/routers/learning_progress.py
app/api/v1/routers/reviews.py
app/api/v1/routers/audiobooks.py
```

Implement:

- extended progress/detail/list responses
- review list/detail endpoints

### Step 6 - Tests

Run:

```powershell
uv run pytest tests/test_learning_progress_service.py tests/test_learning_progress_api.py tests/test_reviews_api.py -q
uv run ruff check app tests
```

If tests are too broad, run focused tests first, then full suite before deploy.

### Step 7 - FE Contract Update

After code passes tests, update:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md
```

or create:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_11_learning_progress_completion_contract.md
```

Recommended: create a Phase 11 FE contract so FE can migrate CTA logic deliberately.

---

## 17. Trade-Offs

### 17.1 More Table, More Clarity

Adding `book_learning_states` increases DB schema size, but makes UI and business state much clearer.

This is worth it because:

- FE no longer infers completion from unrelated fields.
- Review/reminder logic becomes easier.
- Future planner can query one summary row instead of recalculating all progress every time.

### 17.2 Backfill Complexity

Backfill requires careful handling of old rows.

Mitigation:

- Keep nullable timestamps.
- Do not mark completed when `playable_units=0`.
- Prefer conservative `in_progress` if uncertain.

### 17.3 PlanStatus New Value

Adding `completed` may require FE to handle one more plan status.

Mitigation:

- Keep old response fields.
- Add explicit `learning_status` so FE can migrate safely.
- Document UI state mapping.

### 17.4 Restart Learning Not Implemented Yet

After completion, user may want to study again.

Phase 11 should not overload resume.

Future endpoint:

```text
POST /api/v1/books/{book_id}/restart-learning
```

This can create a new learning round or reset progress depending on product decision.

---

## 18. Definition Of Done

Phase 11 is complete when:

- All completion state tests pass.
- A completed book never appears as "new ready book".
- `GET /books/{id}/learning-progress` exposes `learning_status`.
- `GET /books/{id}/details` exposes `learning_summary`.
- Completed plans are marked `completed`, not `inactive`.
- Plan reminders skip completed plans.
- FE can list review items without relying on notification payload.
- Manual test with a real book confirms:
  - continue CTA works before completion;
  - completed CTA works after completion;
  - review CTA has data.

---

## 19. Recommended Next Phase

After Phase 11:

```text
Phase 12 - Calendar-based Reading Plan Sessions
```

Phase 12 should handle:

- Plan theo ngày/tháng/năm.
- Generated study sessions.
- Calendar conflict by actual datetime.
- Reschedule logic.
- Missed session handling.

Do not start Phase 12 until Phase 11 completion state is stable.
