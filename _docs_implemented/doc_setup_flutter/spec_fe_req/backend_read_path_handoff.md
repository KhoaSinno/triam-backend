# Bàn giao Backend - Phase 9 Tối ưu luồng đọc Frontend

Cập nhật: 2026-06-04

## 1. Mục đích

Tài liệu này thông báo cho backend về kế hoạch tối ưu Phase 9 của frontend.
Frontend sẽ coi direct Supabase reads là luồng đọc chính thức, có kiểm soát
cho dữ liệu UI đọc nhiều, đồng thời vẫn giữ backend APIs cho orchestration,
mutations, secrets, background jobs, và realtime tokens.

Đây không phải yêu cầu rewrite backend. Đây là ghi chú phối hợp để backend
kiểm tra RLS, indexes, và optional read models trước khi frontend phụ thuộc
nhiều hơn vào Supabase direct reads.

## 2. Vì sao cần thay đổi

Backend hiện deploy trên Hugging Face Spaces và dùng Supabase
free/pay-as-you-go. Một protected backend request có nhiều hop:

```text
Flutter -> HF FastAPI -> Supabase Auth get_user -> Supabase Postgres -> Python serialize -> Flutter
```

Trong source backend, dependency auth verify mọi protected request qua:

```text
D:/triam-backend/app/api/dependencies/auth.py
supabase.auth.get_user(token)
```

Với read-heavy requests, cách này có thể chậm hơn direct Supabase reads:

```text
Flutter -> Supabase PostgREST/DB with JWT/RLS -> Flutter
```

Quan sát deploy ngày 2026-06-04:

```text
GET /api/v1/health              ~341 ms
GET /                           ~1457 ms
GET /api/v1/health/background   ~4174 ms
```

Đây không phải benchmark chính thức, nhưng đủ để tránh việc mọi UI render ban đầu
phụ thuộc vào HF backend như một generic read proxy.

## 3. Backend vẫn là ưu tiên cho các workflow này

Frontend sẽ tiếp tục dùng backend APIs cho:

```text
POST   /api/v1/upload
POST   /api/v1/generate-plan
GET    /api/v1/jobs/{job_id}
GET    /api/v1/books/{book_id}/processing-status
POST   /api/v1/books/{book_id}/switch-mode
POST   /api/v1/books/{book_id}/pause
POST   /api/v1/books/{book_id}/resume
PUT    /api/v1/books/{book_id}/reading-plan
DELETE /api/v1/books/{book_id}
GET    /api/v1/live-token/thread/{thread_id}
POST   /api/v1/agent/chat
```

Lý do:

- upload cần parse file, storage write, và DB write;
- generate/switch-mode cần LLM/TTS/job orchestration;
- pause/resume/update plan cần conflict validation và schedule slot mutation;
- delete cần dọn storage assets và DB;
- LiveKit/agent cần secrets và server-issued tokens;
- jobs/processing status thể hiện workflow state của backend.

## 4. Các backend APIs dự kiến dùng ít hơn

Nếu refactor Phase 9 thành công, các read-heavy APIs này sẽ được dùng ít hơn,
hoặc chỉ làm fallback khi direct Supabase read/cache chưa sẵn sàng:

```text
GET /api/v1/books
GET /api/v1/books/{book_id}
GET /api/v1/books/{book_id}/outline
GET /api/v1/books/{book_id}/details?mode=...
GET /api/v1/books/{book_id}/learning-units
GET /api/v1/books/{book_id}/learning-progress?mode=...
GET /api/v1/reading-plan-slots
GET /api/v1/books/{book_id}/reading-plan
GET /api/v1/study-contexts
GET /api/v1/study-contexts/{context_id}
GET /api/v1/study-contexts/{context_id}/threads
GET /api/v1/threads/{thread_id}/messages
GET /api/v1/notifications
GET /api/v1/notifications/settings
```

Thay thế dự kiến:

- `/books` và `/books/{book_id}`: đọc projected metadata từ `books` kèm local cache.
- `/outline`: đọc `book_sections` trực tiếp và cache với TTL dài.
- `/details`: đọc `learning_units` và `learning_unit_segments` trực tiếp, hoặc qua read model theo `{bookId, mode}`.
- `/learning-progress`: đọc snapshot từ `learning_unit_progress`; progress mutation có thể vẫn cần backend nếu cần side effects cho completion/review.
- `/reading-plan` và `/reading-plan-slots`: direct read cho prefill/warnings; update/pause/resume vẫn backend-first.
- đọc context/thread/message: direct read với pagination để tránh frontend N+1 hydration qua HF.
- notification list/settings: direct read chấp nhận được nếu RLS được xác nhận; read/read-all/update settings cần mutation review riêng.

Các APIs dưới đây cần giữ backend-first và không nên giảm dùng một cách tùy tiện:

```text
POST   /api/v1/upload
POST   /api/v1/generate-plan
GET    /api/v1/jobs/{job_id}
GET    /api/v1/books/{book_id}/processing-status
POST   /api/v1/books/{book_id}/switch-mode
POST   /api/v1/books/{book_id}/pause
POST   /api/v1/books/{book_id}/resume
PUT    /api/v1/books/{book_id}/reading-plan
DELETE /api/v1/books/{book_id}
GET    /api/v1/live-token/thread/{thread_id}
POST   /api/v1/agent/chat
```

Tóm tắt: backend API vẫn là lớp "do work"; direct Supabase read
kèm local cache là lớp "read fast". Backend không bị loại bỏ, nhưng
nó nên ngừng là proxy mặc định cho mọi UI render query.

## 5. Kế hoạch direct Supabase reads

Frontend dự kiến đọc trực tiếp các read-only data sources này khi RLS/indexes
được xác nhận:

```text
books
book_sections
learning_units
learning_unit_segments
learning_unit_progress
reading_plans
reading_plan_schedule_slots
study_contexts
study_context_document_links
chat_threads
chat_messages
user_notifications
notification_settings
processing_jobs read-only status may remain backend-first unless RLS/read model is confirmed
```

Frontend sẽ không dùng service role key. Chỉ dùng anon key cộng
JWT của user và RLS.

## 6. Cần backend/DB xác nhận

Backend cần xác nhận các tables/views ứng viên có user-owned read RLS đúng.

Yêu cầu về hiệu năng policy:

- các cột dùng trong policies phải có indexes;
- nếu policies dùng `auth.uid()`, cân nhắc `(select auth.uid())` khi phù hợp;
- frontend queries vẫn lặp filter như `.eq('user_id', uid)` để planner dùng indexes;
- tránh policy join phức tạp theo từng row nếu security definer function/view/RPC giúp read rẻ hơn.

Yêu cầu xác nhận indexes:

```text
books.user_id
book_sections.book_id
book_sections(book_id, section_index)
learning_units(book_id, mode, unit_index)
learning_unit_segments(learning_unit_id, segment_index)
learning_unit_progress(user_id, book_id, mode)
learning_unit_progress(user_id, learning_unit_id)
reading_plans.book_id
reading_plan_schedule_slots(user_id, is_active)
reading_plan_schedule_slots(plan_id)
study_contexts.user_id
study_context_document_links(context_id)
study_context_document_links(book_id)
chat_threads.context_id
chat_messages(thread_id, timestamp)
user_notifications(user_id, created_at)
user_notifications(user_id, read_at)
```

Phần lớn các mục này có vẻ đã được index trong models/migrations, nhưng Phase 9
cần xác minh schema Supabase đang deploy, không chỉ source code.

## 7. Read models tùy chọn từ backend/DB

Nếu direct table reads tạo quá nhiều request nhỏ hoặc expose quá nhiều
columns không cần thiết, backend/DB có thể hỗ trợ Supabase views/RPCs. Mục tiêu
là read-only, RLS-safe, truy cập nhẹ.

Các read models ứng viên:

```text
v_book_detail_summary
  book metadata + reading plan summary + active mode summary

v_learning_units_with_segment_counts
  units + segment_count + first/last segment state, without full segment payload

v_context_summary
  context metadata + document_count + thread_count + latest_interaction_at

v_notification_summary
  unread_count + latest notifications projection
```

Views/RPCs vẫn có thể được gọi trực tiếp qua Supabase. Backend API chỉ cần khi
read model đòi hỏi server-only logic hoặc secrets.

## 8. Các hotspot backend hiện tại cho frontend reads

Từ source backend:

```text
D:/triam-backend/app/services/audiobook_service.py
get_book_details:
  book lookup
  active reading plan lookup
  learning_units query
  learning_unit_segments query
  Python grouping + serialization

get_book_outline:
  book lookup
  book_sections projection query
  Python tree build

D:/triam-backend/app/services/study_context_service.py
get_threads_for_context / get_thread_messages:
  ownership validation
  thread/message queries
```

Các endpoint này hợp lệ, nhưng frontend Phase 9 sẽ tránh biến chúng thành yêu cầu
bắt buộc cho mọi initial render khi direct read/cache sẵn sàng.

## 9. Hành vi frontend dự kiến

Frontend sẽ:

- render local cache trước;
- refresh direct Supabase read ở background;
- fallback sang backend API nếu direct path bị tắt hoặc thất bại;
- giữ mutation/workflow calls ở backend API;
- invalidate local cache sau backend mutation;
- tránh full page loading khi có stale data;
- paginate messages/notifications và tránh context N+1 hydration.

## 10. Frontend sẽ không làm

Frontend sẽ không:

- expose service role key;
- bypass RLS;
- perform direct mutations cần business validation;
- rename backend endpoints/JSON keys trong Phase 9;
- yêu cầu backend hardware upgrade như điều kiện tiên quyết;
- giả định direct read an toàn trước khi RLS/index được xác nhận.

## 11. Checklist hành động cho backend

- [ ] Confirm RLS enabled and correct for candidate read tables.
- [ ] Confirm indexes exist on RLS/filter/order columns in deployed Supabase project.
- [ ] Review whether `auth.uid()` policies should use `(select auth.uid())`.
- [ ] Identify read queries that should become views/RPC instead of multi-table client fetches.
- [ ] Confirm whether frontend may read `processing_jobs` directly or should keep job status backend-first.
- [ ] Confirm if any tables contain columns that should never be exposed through direct select, even with RLS.
- [ ] Provide SQL/view names if backend chooses to expose read models.

## 12. Tham khảo

Frontend plan:

```text
docs/_phase9_0_fix_bug_optimize/phase9_fix_bug_optimize_plan.md
```

External docs:

```text
https://huggingface.co/docs/hub/spaces-overview
https://supabase.com/docs/guides/platform/compute-and-disk
https://supabase.com/docs/guides/database/postgres/row-level-security
https://supabase.com/docs/guides/database/debugging-performance
```
