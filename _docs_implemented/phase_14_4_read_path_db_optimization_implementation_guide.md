# Phase 14.4 Implementation Guide - Read Path DB Optimization

## 1. Mục tiêu

Phase 14.4 tập trung tối ưu các API đọc dữ liệu thường xuyên được FE gọi, đặc biệt là Library, Book Detail, Reading Plan Calendar, Notification và Learning Progress.

Mục tiêu chính:

- Giảm số query DB trên các endpoint đọc.
- Loại bỏ N+1 query ở `GET /api/v1/books`.
- Tách read-only summary khỏi logic sync/write để API đọc không tự ghi DB ngoài ý muốn.
- Thêm composite/partial indexes bám đúng query pattern.
- Đo latency trước/sau bằng benchmark API thật.
- Không đổi response contract cho FE.
- Không đổi business logic học sách, tạo lịch, reminder, notification hoặc RAG.

## 2. Cơ sở nghiên cứu

Nguồn chính thống đã đối chiếu:

- Supabase Query Optimization: index phải bám common query patterns; index đúng có thể tăng tốc query lớn đáng kể.  
  https://supabase.com/docs/guides/database/query-optimization
- PostgreSQL Indexes: index giúp tìm và lấy row nhanh hơn, nhưng có overhead khi ghi nên cần dùng có chọn lọc.  
  https://www.postgresql.org/docs/current/indexes.html
- PostgreSQL Partial Indexes: partial index chỉ lưu subset row theo predicate, phù hợp query luôn lọc theo trạng thái cụ thể.  
  https://www.postgresql.org/docs/current/indexes-partial.html
- PostgreSQL EXPLAIN / EXPLAIN ANALYZE: dùng để xem planner chọn plan nào và đo runtime thật.  
  https://www.postgresql.org/docs/current/sql-explain.html
- SQLAlchemy relationship loading: `selectinload()` giải quyết dạng N+1 phổ biến bằng cách load collection liên quan bằng query riêng theo batch.  
  https://docs.sqlalchemy.org/en/latest/tutorial/orm_related_objects.html#selectin-load

Kết luận áp dụng cho TRIAM:

- Không thêm index tràn lan.
- Mỗi index phải tương ứng với một endpoint/query thật.
- Read endpoint không nên gọi service có side effect write nếu chỉ cần hiển thị UI.
- Tối ưu trước các endpoint FE gọi nhiều nhất.

## 3. Hiện trạng code quan trọng

## 3.1 `GET /api/v1/books` đang dễ bị N+1

File:

```text
app/services/audiobook_service.py
```

Hiện tại:

```python
def list_books(session: Session, user_id: uuid.UUID) -> list[dict]:
    return [_book_to_response_dict(session, book) for book in audiobook_repo.get_audiobooks_by_user(session, user_id)]
```

Trong mỗi `_book_to_response_dict()`:

- query plan hiện tại bằng `get_current_plan_for_owned_book()`;
- gọi `build_book_learning_summary()`;
- `build_book_learning_summary()` lại gọi `sync_book_learning_state()`;
- `sync_book_learning_state()` gọi:
  - `list_playable_unit_ids()`;
  - `list_book_progress()`;
  - `get_book_learning_state()`;
  - `get_latest_activity()`;
  - `upsert_book_learning_state()` và commit;
- sau đó count review due/upcoming.

Tác động:

```text
1 request /books
= 1 query list books
+ N * query plan
+ N * sync state queries
+ N * writes/commits tiềm ẩn
+ N * review count queries
```

Khi user có 20-50 sách, endpoint Library sẽ chậm và tốn connection hơn cần thiết.

## 3.2 `build_book_learning_summary()` đang vừa đọc vừa ghi

File:

```text
app/services/learning_progress_service.py
```

Hiện tại:

```python
def build_book_learning_summary(...):
    state = sync_book_learning_state(...)
    ...
```

Vấn đề:

- Tên hàm là `build`, nhưng thực tế có thể ghi DB.
- API đọc như `/books` có thể phát sinh commit.
- Dễ làm latency dao động mạnh.
- Dễ gây khó debug khi FE chỉ mở Library mà DB state lại thay đổi.

Rule Phase 14.4:

```text
Read path không sync/write.
Write path mới sync/write.
```

## 3.3 `count_review_items_for_user()` đang load list rồi đếm bằng Python

File:

```text
app/repositories/spaced_review_repo.py
```

Hiện tại:

```python
return len(
    list_review_items_for_user(... limit=1000)
)
```

Vấn đề:

- DB phải trả nhiều rows không cần thiết.
- Python phải allocate object để chỉ lấy count.
- Khi review nhiều, endpoint detail/progress chậm dần.

Rule Phase 14.4:

```text
Count thì dùng SELECT count(*), không load list.
```

## 3.4 Calendar/session read path đã batch tốt một phần

File:

```text
app/services/reading_plan_session_service.py
```

Điểm tốt:

- `sessions_to_response()` đã batch session units theo `session_ids`.
- `_learning_unit_title_map()` đã lấy title theo batch.

Điểm cần cải thiện:

- `build_plan_session_summary()` đang load toàn bộ sessions rồi đếm bằng Python.
- Các GET session vẫn gọi `mark_due_sessions_missed()` và commit. Đây là lazy evaluation đúng business, nhưng cần tối ưu bằng index và có thể chuyển thành bulk update trong phase này hoặc phase kế tiếp.

## 3.5 Notification read path tương đối ổn nhưng còn tối ưu được

Files:

```text
app/repositories/user_notification_repo.py
app/services/notification_service.py
```

Điểm tốt:

- `list_notifications()` fetch list có limit.
- `count_unread_notifications()` đã dùng SQL `count`.

Điểm cần cân nhắc:

- `mark_all_notifications_read()` đang load từng notification rồi loop set `read_at`.
- Đây là write path, không ưu tiên Phase 14.4 nếu chỉ tập trung read path.

## 4. Scope implement

## 4.1 Được làm

- Refactor repository/service cho `/books` để bulk load plan/state.
- Tạo read-only learning summary helper.
- Đổi review count sang SQL `count(*)`.
- Tối ưu `build_plan_session_summary()` để dùng aggregate/count query và next-session query.
- Thêm composite/partial indexes bằng Alembic migration.
- Thêm benchmark script hoặc test helper để đo endpoint read path.
- Thêm focused tests bảo vệ response contract và query behavior quan trọng.

## 4.2 Không làm trong Phase 14.4

- Không đổi schema response FE.
- Không đổi auth flow.
- Không đổi worker/Celery/TTS/RAG logic.
- Không xóa bảng cũ trong phase này.
- Không tối ưu query bằng cache Redis trước khi DB query sạch.
- Không chuyển toàn bộ app sang async DB.

## 5. Thiết kế giải pháp

## 5.1 Bulk load Library response

Tạo repository mới hoặc thêm vào `audiobook_repo.py`.

Recommendation:

```text
app/repositories/book_read_repo.py
```

Lý do:

- Tách read projection khỏi CRUD storage/delete side effects trong `audiobook_repo.py`.
- Dễ test query riêng.
- Không làm `audiobook_repo.py` phình thêm.

Pseudo code:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class BookListProjection:
    book: Book
    plan: ReadingPlan | None
    state: BookLearningState | None


def list_book_library_projection(session: Session, *, user_id: uuid.UUID) -> list[BookListProjection]:
    books = list(
        session.exec(
            select(Book)
            .where(Book.user_id == user_id)
            .order_by(Book.created_at.desc())
        ).all()
    )
    if not books:
        return []

    book_ids = [book.id for book in books]

    plans = list(
        session.exec(
            select(ReadingPlan)
            .where(
                ReadingPlan.book_id.in_(book_ids),
                ReadingPlan.status != PlanStatus.ERROR.value,
            )
            .order_by(ReadingPlan.book_id, ReadingPlan.updated_at.desc(), ReadingPlan.created_at.desc())
        ).all()
    )
    latest_plan_by_book: dict[uuid.UUID, ReadingPlan] = {}
    for plan in plans:
        latest_plan_by_book.setdefault(plan.book_id, plan)

    states = list(
        session.exec(
            select(BookLearningState).where(
                BookLearningState.user_id == user_id,
                BookLearningState.book_id.in_(book_ids),
            )
        ).all()
    )
    state_by_key = {(state.book_id, state.mode): state for state in states}

    return [
        BookListProjection(
            book=book,
            plan=latest_plan_by_book.get(book.id),
            state=state_by_key.get((book.id, latest_plan_by_book[book.id].mode)) if book.id in latest_plan_by_book else None,
        )
        for book in books
    ]
```

Sau đó sửa service:

```python
def _book_projection_to_response_dict(item: BookListProjection) -> dict:
    book_data = item.book.model_dump()
    state = item.state
    return {
        **book_data,
        "learning_status": state.status if state else None,
        "book_progress_percent": state.book_progress_percent if state else None,
        "completed_at": state.completed_at if state else None,
    }


def list_books(session: Session, user_id: uuid.UUID) -> list[dict]:
    return [_book_projection_to_response_dict(item) for item in list_book_library_projection(session, user_id=user_id)]
```

Trade-off:

- Library có thể hiển thị state cũ nếu legacy data chưa có `book_learning_states`.
- Chấp nhận được vì write path hiện đã sync state khi progress thay đổi.
- Nếu cần self-heal, chỉ chạy sync ở endpoint detail/progress hoặc background maintenance, không chạy trong list.

## 5.2 Tách read-only learning summary

Thêm helper:

```python
def read_book_learning_summary_from_state(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
    mode: PlanMode,
    include_review_counts: bool = True,
) -> BookLearningSummaryResponse:
    state = get_book_learning_state(session, user_id=user_id, book_id=book_id, mode=mode)
    if not state:
        return BookLearningSummaryResponse(
            book_id=book_id,
            mode=mode,
            learning_status=BookLearningStatus.NOT_STARTED,
            is_completed=False,
            can_resume=False,
            can_review=False,
            book_progress_percent=0,
            completed_units=0,
            playable_units=0,
            last_learning_unit_id=None,
            last_segment_id=None,
            last_segment_index=None,
            position_ms=None,
            started_at=None,
            last_activity_at=None,
            completed_at=None,
            due_reviews_count=0,
            upcoming_reviews_count=0,
        )
    ...
```

Sau đó:

- `GET /books` dùng projection/state trực tiếp, không count review.
- `GET /books/{book_id}/details` dùng read-only summary.
- `GET /books/{book_id}/learning-progress` có thể tiếp tục gọi sync nếu muốn self-heal vì endpoint này chuyên về progress.
- Write path `update_learning_unit_progress()` và `complete_learning_unit_manually()` vẫn gọi sync state sau khi lưu progress.

Không nên:

```python
build_book_learning_summary()
```

tiếp tục ghi DB trong mọi read path.

Tên hàm nên rõ:

```python
sync_book_learning_state(...)
read_book_learning_summary_from_state(...)
build_book_learning_summary_after_sync(...)
```

## 5.3 Đổi review count sang SQL aggregate

Sửa:

```text
app/repositories/spaced_review_repo.py
```

Pseudo code:

```python
def count_review_items_for_user(...):
    statement = select(func.count(SpacedReviewItem.id)).where(
        SpacedReviewItem.user_id == user_id,
        SpacedReviewItem.book_id == book_id,
        SpacedReviewItem.mode == mode,
    )
    if status_filter == "due":
        statement = statement.where(
            SpacedReviewItem.status.in_([ReviewItemStatus.DUE, ReviewItemStatus.PENDING]),
            SpacedReviewItem.due_at <= now,
        )
    elif status_filter == "upcoming":
        statement = statement.where(
            SpacedReviewItem.status == ReviewItemStatus.PENDING,
            SpacedReviewItem.due_at > now,
        )
    ...
    return int(session.exec(statement).one() or 0)
```

Test bắt buộc:

- `due` count đúng.
- `upcoming` count đúng.
- `completed` count đúng nếu đang dùng.
- Không bị giới hạn 1000 items như logic cũ.

## 5.4 Tối ưu plan session summary

Hiện tại:

```python
sessions = list_sessions_for_plan(session, plan_id=plan_id)
```

rồi Python đếm total/completed/missed và lấy next session.

Đề xuất:

```python
def get_plan_session_summary_counts(session: Session, *, plan_id: uuid.UUID) -> PlanSessionSummaryCounts:
    rows = session.exec(
        select(ReadingPlanSession.status, func.count(ReadingPlanSession.id))
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status != ReadingPlanSessionStatus.CANCELLED.value,
        )
        .group_by(ReadingPlanSession.status)
    ).all()
    ...
```

Next session query:

```python
def get_next_session_for_plan(session: Session, *, plan_id: uuid.UUID) -> ReadingPlanSession | None:
    return session.exec(
        select(ReadingPlanSession)
        .where(
            ReadingPlanSession.plan_id == plan_id,
            ReadingPlanSession.status.notin_([
                "completed",
                "skipped",
                "cancelled",
            ]),
        )
        .order_by(ReadingPlanSession.scheduled_at, ReadingPlanSession.session_index)
        .limit(1)
    ).first()
```

Sau đó only call `sessions_to_response()` cho next session, không load toàn bộ sessions.

Trade-off:

- Code dài hơn một chút.
- Đổi lại endpoint `GET /books/{book_id}/reading-plan` không bị chậm khi plan có nhiều session lịch sử.

## 5.5 Giữ lazy missed evaluation nhưng làm rẻ hơn

Business hiện đã chốt:

```text
GET sessions sẽ lazy update session quá hạn thành missed trước khi trả về.
```

Không bỏ logic này trong Phase 14.4.

Nhưng cần tối ưu:

- Index đúng cho `mark_overdue_sessions_missed`.
- Có thể đổi từ load rows + loop sang SQL `update(...).returning(...)` trong phase này nếu test chắc.
- Nếu chưa muốn đổi behavior, ít nhất thêm composite/partial index trước.

Query hiện tại:

```python
ReadingPlanSession.scheduled_at < now
status in scheduled/due/in_progress
completed_units < total_units
optional user_id
```

Index đề xuất:

```sql
create index ix_rps_overdue_user_status_scheduled
on reading_plan_sessions (user_id, status, scheduled_at)
where status in ('scheduled', 'due', 'in_progress');
```

Nếu Celery scan toàn hệ thống không có `user_id`:

```sql
create index ix_rps_overdue_status_scheduled
on reading_plan_sessions (status, scheduled_at)
where status in ('scheduled', 'due', 'in_progress');
```

## 6. Index plan

Schema/index changes phải qua Alembic.

Tạo migration:

```powershell
uv run alembic revision -m "phase 14 4 read path indexes"
```

Không cần autogenerate nếu dùng partial indexes bằng raw SQL. Nếu dùng autogenerate, vẫn phải đọc lại migration.

## 6.1 Books

Query:

```python
select(Book).where(Book.user_id == user_id).order_by(Book.created_at.desc())
```

Index:

```sql
create index if not exists ix_books_user_created_at
on books (user_id, created_at desc);
```

Trade-off:

- Tăng nhẹ chi phí insert book.
- Đổi lại Library list ổn định hơn khi user có nhiều sách.

## 6.2 Reading plans

Query:

```python
where book_id in (...)
and status != 'error'
order by book_id, updated_at desc, created_at desc
```

Index:

```sql
create index if not exists ix_reading_plans_book_status_updated
on reading_plans (book_id, status, updated_at desc, created_at desc);
```

Optional partial index:

```sql
create index if not exists ix_reading_plans_book_active_updated
on reading_plans (book_id, updated_at desc, created_at desc)
where status <> 'error';
```

Recommendation:

- Dùng partial index nếu dữ liệu `error` ít nhưng query hầu như luôn exclude error.
- Nếu PostgreSQL planner không dùng partial do predicate mismatch, dùng composite thường.

## 6.3 Book learning states

Đã có:

```text
UniqueConstraint(user_id, book_id, mode)
Index(user_id, status)
Index(book_id, mode)
```

Phase 14.4 không cần thêm index mới nếu query chỉ dùng:

```python
where user_id = ...
and book_id in (...)
```

Cần verify bằng EXPLAIN. Nếu planner không dùng unique index tốt với `book_id in (...)`, cân nhắc:

```sql
create index if not exists ix_book_learning_states_user_book
on book_learning_states (user_id, book_id);
```

Không thêm ngay nếu chưa đo, vì unique `(user_id, book_id, mode)` có thể đã đủ.

## 6.4 Learning unit progress

Queries:

```python
list_book_progress:
where user_id = ...
and book_id = ...
and mode = ...
order by updated_at
```

```python
get_latest_activity:
where user_id = ...
and book_id = ...
and mode = ...
and last_activity_at is not null
order by last_activity_at desc
```

Indexes:

```sql
create index if not exists ix_lup_user_book_mode_updated
on learning_unit_progress (user_id, book_id, mode, updated_at);

create index if not exists ix_lup_user_book_mode_last_activity
on learning_unit_progress (user_id, book_id, mode, last_activity_at desc)
where last_activity_at is not null;
```

## 6.5 Spaced review items

Queries:

```python
user_id, book_id, mode, status, due_at
```

Index:

```sql
create index if not exists ix_sri_user_book_mode_status_due
on spaced_review_items (user_id, book_id, mode, status, due_at);
```

For due queue worker:

```sql
create index if not exists ix_sri_due_queue
on spaced_review_items (status, due_at)
where status in ('pending', 'due');
```

## 6.6 Reading plan sessions

Queries:

```python
list_sessions_for_user_local_date:
user_id, local_date, status != cancelled
order by scheduled_at, session_index
```

```python
list_sessions_for_user_range:
user_id, local_date between from/to, optional book_id/mode/status
order by scheduled_at, session_index
```

```python
list_sessions_for_book:
user_id, book_id, optional mode, status != cancelled
order by scheduled_at, session_index
```

Indexes:

```sql
create index if not exists ix_rps_user_local_date_scheduled
on reading_plan_sessions (user_id, local_date, scheduled_at, session_index)
where status <> 'cancelled';

create index if not exists ix_rps_user_book_mode_scheduled
on reading_plan_sessions (user_id, book_id, mode, scheduled_at, session_index)
where status <> 'cancelled';
```

For overdue lazy update:

```sql
create index if not exists ix_rps_overdue_user_status_scheduled
on reading_plan_sessions (user_id, status, scheduled_at)
where status in ('scheduled', 'due', 'in_progress');

create index if not exists ix_rps_overdue_status_scheduled
on reading_plan_sessions (status, scheduled_at)
where status in ('scheduled', 'due', 'in_progress');
```

## 6.7 User notifications

Existing migrations already appear to have:

```text
ix_user_notifications_user_created_at
ix_user_notifications_user_read_at
```

Before adding more, verify indexes in DB:

```sql
select indexname, indexdef
from pg_indexes
where tablename = 'user_notifications';
```

If missing, add:

```sql
create index if not exists ix_user_notifications_user_created_at
on user_notifications (user_id, created_at desc);

create index if not exists ix_user_notifications_user_unread_created_at
on user_notifications (user_id, created_at desc)
where read_at is null;
```

## 6.8 Notification outbox

Worker queries:

```python
status = pending
due_at <= now
next_retry_at is null or next_retry_at <= now
order by due_at
```

Existing indexes:

```text
status_due_at
status_next_retry_at
```

Optional partial index:

```sql
create index if not exists ix_notification_outbox_pending_due_retry
on notification_outbox (due_at, next_retry_at)
where status = 'PENDING';
```

Do this only if EXPLAIN shows due outbox scan still expensive.

## 7. API benchmark plan

## 7.1 Benchmark endpoints

Test with real deployed/local API and dev access token:

```text
GET /api/v1/books
GET /api/v1/books/{book_id}
GET /api/v1/books/{book_id}/details?mode=full
GET /api/v1/books/{book_id}/learning-progress?mode=full
GET /api/v1/books/{book_id}/reading-plan
GET /api/v1/reading-plan/sessions/today
GET /api/v1/reading-plan/sessions?from_date=...&to_date=...
GET /api/v1/notifications?limit=30
```

Metrics:

```text
p50 latency
p95 latency
max latency
response size
status code
error body if any
```

## 7.2 Benchmark script

Tạo:

```text
scripts/benchmark_read_paths.py
```

Pseudo:

```python
import statistics
import time
import httpx

ENDPOINTS = [...]

def measure(client, endpoint, runs=10):
    latencies = []
    for _ in range(runs):
        start = time.perf_counter()
        response = client.get(endpoint)
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
        assert response.status_code < 500
    return {
        "p50_ms": statistics.median(latencies),
        "p95_ms": sorted(latencies)[int(len(latencies) * 0.95) - 1],
        "max_ms": max(latencies),
    }
```

Chạy:

```powershell
$env:TRIAM_API_BASE_URL="http://127.0.0.1:8000/api/v1"
$env:TRIAM_ACCESS_TOKEN="$(uv run python scripts/get_supabase_access_token.py)"
uv run python scripts/benchmark_read_paths.py
```

Không commit token hoặc raw response có dữ liệu người dùng.

## 7.3 DB query plan verification

Chạy EXPLAIN trên Supabase SQL editor hoặc psql dev DB:

```sql
explain (analyze, buffers)
select *
from books
where user_id = '<user-id>'
order by created_at desc;
```

Với write query, không dùng `EXPLAIN ANALYZE` trực tiếp nếu query có side effect, vì PostgreSQL sẽ thực thi câu lệnh khi dùng `ANALYZE`.

## 8. Implementation order đề xuất

## Step 1 - Baseline benchmark

- Chạy benchmark read paths hiện tại.
- Lưu kết quả vào:

```text
_docs_implemented/phase_14_4_read_path_benchmark_report.md
```

Format:

```markdown
| Endpoint | p50 before | p95 before | Notes |
```

## Step 2 - Refactor `/books` bulk read

- Tạo `book_read_repo.py`.
- Update `list_books()`.
- Update `get_book()` nếu cần dùng read-only helper.
- Không đổi schema response.

Expected impact:

```text
/books query count từ O(N) về O(1) theo số sách.
```

## Step 3 - Read-only learning summary

- Thêm `read_book_learning_summary_from_state()`.
- Dùng trong book details/list nếu không cần self-heal.
- Giữ `sync_book_learning_state()` cho write path.

Expected impact:

```text
GET endpoints không commit DB.
```

## Step 4 - SQL count for review

- Sửa `count_review_items_for_user()`.
- Thêm unit tests.

Expected impact:

```text
Không load 1000 review rows để đếm.
```

## Step 5 - Plan session summary aggregate

- Thêm repository aggregate count.
- Thêm next session query.
- Update `build_plan_session_summary()`.

Expected impact:

```text
GET reading-plan không load toàn bộ session history.
```

## Step 6 - Alembic indexes

- Add migration indexes theo mục 6.
- Ưu tiên:

```text
ix_books_user_created_at
ix_lup_user_book_mode_updated
ix_lup_user_book_mode_last_activity
ix_sri_user_book_mode_status_due
ix_rps_user_local_date_scheduled
ix_rps_user_book_mode_scheduled
ix_rps_overdue_user_status_scheduled
```

Không add tất cả optional index nếu benchmark chưa chứng minh cần.

## Step 7 - Post-benchmark

- Chạy lại benchmark.
- So sánh p50/p95.
- Kiểm tra không đổi response shape.

## 9. Test plan

## 9.1 Unit tests

Thêm/sửa:

```text
tests/test_audiobook_read_path.py
tests/test_spaced_review_repo.py
tests/test_reading_plan_session_summary.py
```

Cases:

- `/books` response giữ đủ fields cũ.
- Book without plan trả `learning_status=None`, `book_progress_percent=None`, `completed_at=None`.
- Book with state trả đúng learning status/progress.
- `count_review_items_for_user()` count đúng >1000 rows.
- `build_plan_session_summary()` không cần load all sessions nhưng trả đúng total/completed/missed/next_session.

## 9.2 API tests

Chạy:

```powershell
uv run pytest tests/test_auth_user_isolation.py tests/test_phase12_calendar_plan_sessions.py tests/test_phase13_calendar_session_actions.py tests/test_notifications_api.py -q
```

Nếu có test audiobook hiện tại:

```powershell
uv run pytest tests -q -k "book or audiobook or reading_plan"
```

## 9.3 Static checks

```powershell
uv run ruff check app/repositories app/services app/api tests
uv run python -m py_compile app/repositories/book_read_repo.py app/services/audiobook_service.py app/services/learning_progress_service.py
```

## 9.4 Migration checks

```powershell
uv run alembic upgrade head
uv run alembic current
```

Nếu DB dev reset được:

```powershell
uv run alembic downgrade -1
uv run alembic upgrade head
```

Không chạy downgrade trên production.

## 10. Trade-off

## 10.1 Read-only state có thể stale

Vấn đề:

- Nếu legacy row chưa sync, Library có thể hiển thị `not_started` hoặc `None`.

Giải pháp:

- Sync state ở write path.
- Có thể tạo maintenance script backfill `book_learning_states`.
- Không để `/books` tự sync từng book.

## 10.2 Thêm index làm write chậm hơn một chút

Vấn đề:

- Insert/update vào indexed table phải cập nhật thêm index.

Giải pháp:

- Chỉ add index cho query pattern thật.
- Benchmark trước/sau.
- Tránh index trùng với unique/composite đã có.

## 10.3 Lazy missed evaluation vẫn là write trong GET

Vấn đề:

- `GET /reading-plan/sessions` vẫn có thể update `missed`.

Lý do giữ:

- Business yêu cầu UI luôn đúng khi user mở app.

Giải pháp:

- Tối ưu bằng composite/partial index.
- Sau Phase 14.4 có thể tách thêm Phase 14.5 để chuyển missed marking sang bulk update + Celery beat hardening nếu cần.

## 10.4 Aggregate summary code phức tạp hơn

Vấn đề:

- Code count bằng SQL dài hơn Python count.

Lý do chọn:

- Query nhanh hơn khi plan/session/review nhiều.
- Ít memory allocation.
- Dễ đo bằng EXPLAIN.

## 11. Definition of Done

Phase 14.4 hoàn thành khi:

- `GET /api/v1/books` không còn gọi `build_book_learning_summary()` theo từng book.
- Read path Library không commit DB.
- `count_review_items_for_user()` dùng SQL `count(*)`.
- `build_plan_session_summary()` không load toàn bộ session history chỉ để count.
- Alembic migration thêm các indexes ưu tiên.
- Benchmark before/after có trong markdown report.
- Focused tests pass.
- API response FE không đổi.
- Không leak token/user document content trong benchmark logs.

## 12. Sau Phase 14.4

Nếu benchmark vẫn chậm, phase kế tiếp nên là:

```text
Phase 14.5 - Query Plan Driven API Optimization
```

Mục tiêu:

- Dùng `pg_stat_statements` hoặc Supabase Query Performance report để lấy top slow queries.
- Dùng EXPLAIN ANALYZE cho từng slow query.
- Tối ưu theo plan thật, không đoán.
- Cân nhắc cache ở app/Redis chỉ sau khi query DB đã sạch.
