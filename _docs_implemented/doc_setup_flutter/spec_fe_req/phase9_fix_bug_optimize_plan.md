# Phase 9.0 Plan - Fix Bug & Optimize Data Connectivity

Cap nhat: 2026-06-04

## 1. Muc Tieu

Phase 9 tap trung sua bug va toi uu toc do trai nghiem hoc/tai lieu trong dieu kien ha tang hien tai:

- backend FastAPI dang deploy tren Hugging Face Spaces;
- Supabase la database/auth/storage chinh, dang dung free/pay-as-you-go tier;
- server backend khong du manh de lam proxy cho moi truy van doc;
- mot so truy van co the tra ve ngay nhung van cham do hop backend, auth, DB, serialize, worker/agent cung chay;
- frontend can local caching nhu mot tang kien truc bat buoc, khong chi la toi uu phu.

Ket luan kien truc Phase 9: **direct Supabase read + local cache la read path chinh thuc co kiem soat**. Backend API tiep tuc giu cac workflow can secret, orchestration, mutation phuc tap, background job, LiveKit token, agent, TTS/LLM, upload/delete asset.

## 2. Tai Lieu Tham Khao Bat Buoc

Doc truoc khi sua code Phase 9:

```text
docs/data_connectivity_layer_spec.md
docs/_phase8_0_pareto_learning_experience/phase8_pareto_learning_experience_plan.md
docs/_phase8_0_pareto_learning_experience/IMPORTANT_technical_notes.md
docs/_phase7_1_naming_consolidation/phase7_1_document_workspace_plan.md
docs/_phase7_1_naming_consolidation/IMPORTANT_technical_notes.md
```

Backend source tham khao:

```text
D:/triam-backend/app/main.py
D:/triam-backend/app/api/dependencies/auth.py
D:/triam-backend/app/db/database.py
D:/triam-backend/app/api/v1/routers/audiobooks.py
D:/triam-backend/app/services/audiobook_service.py
D:/triam-backend/app/repositories/book_section_repo.py
D:/triam-backend/app/repositories/learning_unit_repo.py
D:/triam-backend/app/services/study_context_service.py
D:/triam-backend/app/models/db_models.py
D:/triam-backend/start.sh
D:/triam-backend/Dockerfile
```

External capacity references:

```text
https://huggingface.co/docs/hub/spaces-overview
https://supabase.com/docs/guides/platform/compute-and-disk
https://supabase.com/docs/guides/database/postgres/row-level-security
https://supabase.com/docs/guides/database/debugging-performance
```

## 3. Baseline Hien Tai

Frontend:

- `BackendApiService` la REST client static chinh, gan Supabase bearer token va retry 401 cho JSON request.
- `RemoteBookRepository` doc `/books`, `/details`, `/outline`, `/reading-plan`, `/learning-progress`, `/jobs`, `/upload`.
- `SharedPreferencesCache` da co user-scoped prefix va TTL nhung chua bao phu moi local state.
- Mot so local state dung `SharedPreferences` rieng: recent books, context access, recent arXiv, theme/navigation/TTS.
- `ChapterRepository` query Supabase table truc tiep, nhung con debug/default/hardcoded style va chua thanh read path co quy tac.

Backend:

- Protected API request verify token bang `supabase.auth.get_user(token)` moi request.
- DB engine dung QueuePool/NullPool tuy Supabase pooler; default pool nho `pool_size=3`, `max_overflow=2`.
- `start.sh` co the chay FastAPI chung voi voice agent, Celery worker, Celery beat tuy env.
- `/books/{book_id}/details` doc book, reading plan, learning units, segments roi serialize Python.
- `/books/{book_id}/outline` doc toan bo `book_sections` va build tree trong Python.
- `/study-contexts` va related threads/messages con co nguy co frontend hydrate N+1.

Observation ngay 2026-06-04 tren deploy:

```text
GET /api/v1/health              ~341 ms
GET /                           ~1457 ms
GET /api/v1/health/background   ~4174 ms
```

Day chi la smoke observation, khong phai benchmark ket luan. Tuy vay no du de Phase 9 khong dat UX phu thuoc vao backend warm/proxy cho moi read-heavy surface.

## 4. Contract/Data Stance

Khong doi wire contract backend trong Phase 9 neu khong bat buoc.

Backend API tiep tuc la source cho:

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

Direct Supabase read duoc phep cho:

```text
books list/detail metadata
book_sections outline rows
learning_units
learning_unit_segments
learning_unit_progress snapshot
reading_plans read-only prefill
reading_plan_schedule_slots read-only slots
study_contexts read-only list/detail
chat_threads read-only list
chat_messages read-only paged history
user_notifications read-only list
```

Dieu kien bat buoc cho direct read:

- table/view co RLS dung;
- query co filter ro: `user_id`, `book_id`, `context_id`, `thread_id`, `mode`;
- select field cu the, khong `select('*')` trong production path;
- co limit/range cho danh sach dai;
- co cache key/user namespace/schema version;
- co stale fallback hoac loading state khong trang rong;
- khong dung service role key trong Flutter.

## 5. Cac Epic Phase 9

### Epic A: Direct Supabase Read Path Co Kiem Soat

Frontend behavior:

- Tao facade/repository doc truc tiep Supabase cho read-heavy data.
- Giu API repository cu lam fallback/migration path.
- Khong goi Supabase table truc tiep tu UI widget/controller.
- Moi direct query duoc dat ten ro `ReadRepository` hoac `ReadDataSource`.

Candidate files:

```text
lib/core/services/supabase_read_client.dart
lib/shared/book/data/book_read_repository.dart
lib/shared/document/data/document_read_repository.dart
lib/features/knowledge/data/context_read_repository.dart
```

Acceptance:

- Read-heavy screens co the doc tu Supabase read path khi flag bat.
- Backend API van co the fallback khi direct path loi/chua co policy.
- Khong them query direct le te ngoai repository.

### Epic B: Cache-First UX Va Stale-While-Revalidate

Frontend behavior:

- Render cache truoc neu co.
- Refresh online o background.
- Neu online cham, UI hien data cu kem trang thai dang cap nhat, khong full blank.
- Neu online loi, stale cache van dung duoc neu con hop ly.

Cache categories:

```text
book_list:{userId}:{filterHash}:v1                 TTL 5-15 min
book_detail:{userId}:{bookId}:v1                   TTL 10-30 min
book_outline:{userId}:{bookId}:v1                  TTL 6-24 h
learning_units:{userId}:{bookId}:{mode}:v1         TTL 2-12 h
learning_segments:{userId}:{bookId}:{mode}:v1      TTL 2-12 h
reading_plan:{userId}:{bookId}:v1                  TTL 5-15 min
learning_progress:{userId}:{bookId}:{mode}:v1      TTL 30 s - 5 min
context_threads:{userId}:{contextId}:v1            TTL 5-15 min
thread_messages:{userId}:{threadId}:{page}:v1      TTL 1-15 min
notifications:{userId}:{filter}:v1                 TTL 1-7 days
```

Acceptance:

- Book Detail/Document Hub/Now Listening khong trang rong khi backend cham neu co cache.
- Cache invalidation ro sau upload, generate-plan, switch-mode, pause/resume, progress update, delete.
- Cache key co schema version.

### Epic C: Query Budget Va Pagination

Frontend behavior:

- Moi man hinh co query budget.
- Khong hydrate N+1 bang cach fetch detail tung context/thread neu co the hien aggregate cache.
- Messages, notifications, contexts co pagination/range.
- Outline/detail chi lay field can render.

Initial query budgets:

```text
Document Hub initial:
  1 query books metadata, limit 50
  optional 1 query active slots/progress summary if cached/stale

Book Detail initial:
  1 query book metadata
  1 query reading plan
  1 query learning units without huge source text
  1 query segments only for active mode, or lazy per unit if data large
  outline lazy/cached, not blocking hero

Context list initial:
  1 query contexts
  no per-context threads/messages hydrate in initial render

Thread detail:
  1 query thread
  1 paged query latest messages
```

Acceptance:

- `rg` khong thay pattern hydrate summary bang nested loops tren contexts -> threads -> messages trong initial list path.
- Moi query list co limit/range.
- Direct Supabase query duplicate RLS filter de planner dung index.

### Epic D: Backend API Load Reduction

Frontend behavior:

- Chuyen read-only endpoints nang sang direct read/cache theo flag.
- Giam polling tan suat khi job/progress khong can realtime lien tuc.
- Backoff polling job khi HF cham.

Backend-preserving behavior:

- Upload/generate/switch/job/token/agent van qua backend.
- Pause/resume/update plan van qua backend vi co validation conflict va mutation schedule slots.
- Delete book van qua backend vi can xoa storage assets + DB.

Acceptance:

- Trong golden path doc/learning, so request den HF giam ro: initial Document Hub/Book Detail khong bat buoc goi `/books`, `/details`, `/outline` neu direct read flag bat va cache hop le.
- User van co the dung app khi HF cold-start, mien Supabase read path va cache con hoat dong.

### Epic E: Bug Fix Sweep

Fix candidates tu audit:

- `BackendApiService.uploadMultipart` khong retry auth 401 nhu request JSON.
- `DocumentRepository.clearDocumentCaches(documentId)` bo qua `documentId` va chi clear list.
- `LiveKitAgentService._livekitUrl` hardcoded, chua dong bo voi env/config.
- `LiveKitAgentService._fetchToken(backendBaseUrl, tokenPath)` nhan `backendBaseUrl` nhung khong dung.
- `RecentArxivPapers` va `ContextAccessTracker` chua user-scoped ro.
- `ChapterRepository` con query debug all/default hardcoded book id; can chuyen thanh read repository nghiem tuc hoac xoa debug.
- `KnowledgeContextRepository._hydrateContextSummary` co nguy co N+1/N*M request.

Acceptance:

- Bug fix co test/smoke phu hop.
- Khong tron refactor lon voi bug fix nho trong cung commit neu co the tach.

### Epic F: File Cache Va Reader Optimization

Frontend behavior:

- File downloaded/cache co eviction/size limit.
- Cover/temp generated files co cleanup policy.
- Khong tai lai file lon neu cache hop le.
- Reader chi validate file khi can, tranh sync IO nang tren UI path.

Acceptance:

- Co file cache registry hoac metadata key de cleanup.
- Co cap dung luong/tong so file tam.
- PDF/EPUB/DOCX reader khong tao temp vo han.

### Epic G: Measurement & Verification Harness

Frontend/backend coordination:

- Them script/manual checklist do latency:
  - backend public health;
  - backend protected `/books`, `/details`, `/outline`;
  - direct Supabase equivalent query;
  - cached read;
  - cold-ish/warm-ish repeated samples.
- Khong log token, password, raw secret, full auth header.

Acceptance:

- Co so lieu truoc/sau cho it nhat 3 surface: Document Hub, Book Detail, Context/Thread.
- So lieu bao gom median tu 3-5 lan lap, khong chi mot lan.

## 6. Thu Tu Trien Khai De Xuat

1. Xac minh RLS/index hien co cho cac bang direct read candidate.
2. Them config flag cho direct Supabase read path, mac dinh co the off neu chua xong RLS.
3. Chuan hoa cache key/version va sua invalidation bug ro rang.
4. Sua bug nho co blast radius thap: upload retry, document cache clear, LiveKit config/token base URL.
5. Tao direct read repository cho `book_sections`, `learning_units`, `learning_unit_segments`.
6. Chuyen Book Detail/Document Detail sang cache-first + direct read flag.
7. Chuyen Document Hub list sang cache-first, pagination/filter ro.
8. Giam context hydrate N+1; them paged thread/messages read.
9. Them file cache eviction.
10. Chay measurement va cap nhat checklist/status.

## 7. Backend Coordination Requests

Frontend Phase 9 can backend ho tro/confirm:

- RLS policies cho read candidate tables/views.
- Index tren cot dung trong RLS va filter:
  - `books.user_id`
  - `book_sections.book_id`, `book_sections(book_id, section_index)`
  - `learning_units(book_id, mode, unit_index)`
  - `learning_unit_segments(learning_unit_id, segment_index)`
  - `learning_unit_progress(user_id, book_id, mode)`, `learning_unit_progress(user_id, learning_unit_id)`
  - `reading_plans.book_id`
  - `reading_plan_schedule_slots(user_id, is_active)`
  - `study_contexts.user_id`
  - `chat_threads.context_id`
  - `chat_messages(thread_id, timestamp)`
  - `user_notifications(user_id, created_at)`, `user_notifications(user_id, read_at)`
- Neu RLS policy dung `auth.uid()`, can can nhac pattern `(select auth.uid())`.
- Neu direct table shape qua thua field/nang, backend/DB nen tao view/RPC read model, vi van nhanh hon proxy qua HF cho read-only.

## 8. Manual QA

Golden path:

1. Dang nhap.
2. Mo Document Hub khi HF warm: list hien nhanh, cache duoc ghi.
3. Mo lai app khi tat mang/hoac backend cham: Document Hub render cache.
4. Mo Book Detail: hero/detail render truoc, outline/learning units load lazy/cache.
5. Chuyen Full/Pareto: mutation qua backend, cache mode bi invalidate dung muc.
6. Nghe mot segment: progress local update ngay, backend persist theo throttle hien co.
7. Mo context list: khong bi cham do hydrate moi thread/message.
8. Mo thread: message list load paged.
9. Upload tai lieu: van qua backend, sau upload invalidate list/detail.
10. Delete tai lieu: van qua backend, sau delete xoa local cache va file cache.

## 9. Ngoai Pham Vi Phase 9

- Khong rewrite backend.
- Khong doi backend endpoint naming `/books`, `book_id`, `ReadingPlan`.
- Khong dua service role key vao Flutter.
- Khong bien direct read thanh direct mutation voi business logic phuc tap.
- Khong them analyzer lam gate mac dinh.
- Khong yeu cau Supabase paid upgrade nhu dieu kien bat buoc; chi ghi nhan neu metric cho thay can.

## 10. Gate Rules

Docs-only:

```bat
git status --short
```

Frontend UI/cache/read path:

```bat
flutter test test\_compile_smoke_test.dart
```

Model/repository/contract parser:

```bat
flutter test test\_contract_models_test.dart
```

Backend smoke neu can:

```bat
python scripts\ping_backend_auth.py
```

CodeGraph/reference checks:

```bat
codegraph sync .
rg -n "BackendApiService|getBookLearningJourney|getBookOutline|KnowledgeContextRepository|ChapterRepository|SharedPreferencesCache|LiveKitAgentService" lib -g "*.dart"
```

Tranh:

```bat
flutter analyze
```

Lenh nay da co tien su treo trong moi truong local nay.

## 11. Definition Of Done

- Read-heavy screens co cache-first behavior va khong full blank khi backend cham.
- Direct Supabase read path duoc dat trong repository/facade ro rang, khong leak vao UI.
- Backend API traffic giam o cac surface doc nhieu.
- RLS/index/query-budget duoc xac nhan cho bang/view direct read.
- Cac bug Phase 9 high-priority duoc sua hoac ghi explicit carryover.
- Co measurement truoc/sau cho Document Hub, Book Detail, Context/Thread.
- Smoke/contract tests pass tren cac be mat da sua.
