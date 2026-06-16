# Phase 14 - Legacy DB, Logic, And Architecture Cleanup Plan

Date: 2026-06-13  
Status: **Runtime cleanup implemented; destructive DB migration file created, not auto-applied**

## 1. Mục tiêu

Phase này dùng để dọn các phần kiến trúc cũ sau khi hệ thống đã chuyển sang:

- `book_sections` làm cấu trúc mục lục/tài liệu chuẩn.
- `learning_units` làm đơn vị học chính cho full/pareto.
- `book_section_knowledge` làm nguồn RAG chính cho chat/voice.
- `reading_plan_sessions` làm lịch học theo ngày giờ cụ thể.
- `learning_unit_progress` và `book_learning_states` làm tracking tiến độ học.

Mục tiêu không phải là xoá nhanh các bảng nhìn có vẻ cũ. Mục tiêu là xoá đúng thứ tự để không làm vỡ:

- upload/generate-plan/switch-mode;
- audio generation;
- RAG của chat/voice;
- lịch học;
- tracking tiến độ;
- notification/review.

## 1.1. Implementation status - 2026-06-13

Đã implement:

- Cắt legacy fallback trong `app/services/rag_service.py`.
- `search_book_knowledge()` chỉ còn:
  - hybrid section RAG; hoặc
  - section vector RAG.
- Xoá runtime path:
  - `search_learning_unit_knowledge()`;
  - `match_book_knowledge`;
  - `book_knowledge`.
- Xoá legacy per-learning-unit embedding pipeline:
  - `app/services/embed_service.py`;
  - `app/repositories/book_knowledge_repo.py`;
  - `_run_rag_pipeline`;
  - `include_rag`;
  - `LEARNING_UNIT_LEGACY_RAG_INDEX_ENABLED`.
- Xoá `BookKnowledge` model khỏi `app/models/db_models.py`.
- Cập nhật tests để không còn expect fallback legacy.
- Tạo migration:

```text
app/db/migrations/versions/b14c2d3e4f50_phase_14_drop_legacy_book_knowledge.py
```

Chưa tự động chạy migration destructive vào DB thật trong quá trình implement. Lý do: cần xác nhận chắc chắn environment đang trỏ DB dev hoặc đã backup production.

## 2. Kết luận sau khi rà source

### 2.1. `book_knowledge` là legacy và phải được xoá

`book_knowledge` hiện là legacy thật. Nó không còn là nguồn tri thức đúng cho hệ thống mới vì RAG hiện nên bám theo `book_sections`, không bám theo `learning_units`.

Tuy nhiên chưa được drop DB ngay trong bước đầu vì vẫn còn runtime references:

- Model: `app/models/db_models.py`
- Repository: `app/repositories/book_knowledge_repo.py`
- Legacy embedding service: `app/services/embed_service.py`
- Learning unit worker cleanup: `app/services/workers/learning_unit_worker.py`
- RAG fallback: `app/services/rag_service.py`
- RPC: `match_book_knowledge`
- Tests: `tests/services/test_rag_service.py`

Ngoài ra, trong worker vẫn có cờ:

```python
settings.LEARNING_UNIT_LEGACY_RAG_INDEX_ENABLED
```

Cờ này đang default `False`, nhưng code path vẫn tồn tại. Nếu bật lên, hệ thống lại sinh vector vào `book_knowledge`.

Vì vậy thứ tự đúng là:

1. Chốt `book_section_knowledge` là RAG canonical duy nhất.
2. Xoá hoàn toàn fallback runtime vào `book_knowledge`.
3. Xoá service/repository/model cũ.
4. Chạy regression test RAG/chat/voice.
5. Sau cùng mới migration drop table/RPC.

### 2.2. `book_section_knowledge` là bảng cần giữ

`book_section_knowledge` là hướng mới đúng hơn vì nó bám theo outline thật của tài liệu:

- Có `section_id`.
- Có `section_path`.
- Có `search_text`.
- Có `content_hash`.
- Có `embedding_version`.
- Hỗ trợ vector search và lexical search.

Quan trọng:

```text
book_section_knowledge KHÔNG dùng RPC match_book_knowledge.
```

Các RPC đúng của `book_section_knowledge` là:

```text
match_book_section_knowledge
match_book_section_knowledge_lexical
```

RPC `match_book_knowledge` thuộc legacy table `book_knowledge` và phải bị xoá trong cleanup.

Đây là nguồn tốt hơn cho các câu hỏi kiểu:

- tác giả;
- chương/mục;
- nội dung chương;
- câu hỏi theo đề mục;
- voice query bị STT lệch nhẹ.

### 2.3. Chapter-era schema đã được cleanup một phần ở Phase 6

Migration Phase 6 đã có logic:

- drop `chapters`;
- drop `chapter_segments`;
- drop `chapter_processing_states`;
- drop `chapter_learning_progress`;
- drop các cột `chapter_id` cũ khỏi một số bảng.

Tuy nhiên migration cũ vẫn có dấu vết trong lịch sử Alembic. Điều này bình thường. Không cần sửa migration cũ đã chạy, trừ khi migration đang lỗi trên DB mới.

Điểm cần làm ở Phase 14 là kiểm tra DB hiện tại còn bảng/cột legacy thật hay không, sau đó tạo migration cleanup mới nếu còn.

### 2.4. `DirectBookContext` chưa nên xoá

`direct_book_context` nhìn giống bảng phụ, nhưng hiện vẫn dùng trong:

```text
app/repositories/study_context_thread_repo.py
```

Nó phục vụ flow mở nhanh chat/thread từ một quyển sách. Nếu xoá ngay sẽ làm vỡ direct book detail discussion.

Khuyến nghị:

- Giữ `direct_book_context` ở Phase 14.
- Chỉ dọn sau khi đã thống nhất toàn bộ chat/thread đều đi qua `study_contexts + study_context_document_links + chat_threads`.

### 2.5. Plan/progress mới là đúng hướng, nhưng còn query ambiguity

Kiến trúc mới hiện đúng về mặt hướng:

```text
ReadingPlan
  -> cấu hình kế hoạch học của sách/mode

ReadingPlanScheduleSlot
  -> slot lịch lặp weekly để chống trùng lịch giữa các sách

ReadingPlanSession
  -> buổi học cụ thể theo ngày giờ

ReadingPlanSessionUnit
  -> các learning unit nằm trong một buổi học

LearningUnitProgress
  -> tiến độ nghe theo unit/segment

BookLearningState
  -> summary denormalized cho FE đọc nhanh
```

Nhưng còn vài query đang lấy plan theo `book_id` rồi `.first()`:

```python
select(ReadingPlan).where(ReadingPlan.book_id == book_id).first()
```

Vấn đề:

- Nếu một sách có nhiều plan theo mode hoặc sau này có learning round, `.first()` có thể trả nhầm.
- Hiện tại phần lớn vẫn ổn vì business đang có một active plan chính cho sách, nhưng code chưa diễn đạt rõ điều đó.

Phase 14 nên chuẩn hoá helper lấy plan:

```text
get_current_reading_plan_for_book(user_id, book_id)
get_reading_plan_for_book_mode(user_id, book_id, mode)
get_active_reading_plan_for_book(user_id, book_id)
```

Không nên để mỗi service tự query `.first()` nữa.

## 3. Inventory cần audit trước khi xoá DB

Chạy các SQL này trên DB dev trước. Production chỉ chạy sau khi backup.

```sql
select to_regclass('public.book_knowledge') as book_knowledge_table;
select to_regclass('public.book_section_knowledge') as book_section_knowledge_table;
select to_regclass('public.chapters') as chapters_table;
select to_regclass('public.chapter_segments') as chapter_segments_table;
select to_regclass('public.chapter_processing_states') as chapter_processing_states_table;
select to_regclass('public.chapter_learning_progress') as chapter_learning_progress_table;

select count(*) as book_knowledge_rows from book_knowledge;
select count(*) as book_section_knowledge_rows from book_section_knowledge;

select proname
from pg_proc
where proname in (
  'match_book_knowledge',
  'match_book_section_knowledge',
  'match_book_section_knowledge_lexical'
)
order by proname;
```

Nếu `book_knowledge_rows > 0`, không cần migrate data sang `book_section_knowledge` nếu mọi sách hiện tại đã được index bằng section indexer. Nhưng phải kiểm chứng:

```sql
select b.id, b.title, count(bsk.id) as section_chunks
from books b
left join book_section_knowledge bsk on bsk.book_id = b.id
where b.status in ('partial_ready', 'ready')
group by b.id, b.title
order by section_chunks asc;
```

Sách `ready` mà `section_chunks = 0` cần re-index trước khi drop legacy RAG.

## 4. Phase 14.0 - Audit only

### Việc cần làm

- Chạy SQL inventory trên DB dev.
- Ghi lại số row của các bảng legacy.
- Kiểm tra sách `ready` có `book_section_knowledge` đầy đủ chưa.
- Chạy các test RAG/chat/voice hiện tại để có baseline.

### Không làm ở phase này

- Không drop table.
- Không drop RPC.
- Không xoá model.
- Không sửa response contract FE.

### Output mong muốn

- Một file log audit hoặc note trong PR:

```text
book_knowledge rows: ...
book_section_knowledge rows: ...
chapters exists: yes/no
chapter_segments exists: yes/no
ready books missing section index: ...
```

## 5. Phase 14.1 - Cut legacy RAG runtime path

Status: **Implemented**

### Mục tiêu

Sau phase này, runtime không còn bất kỳ đường nào dùng `book_knowledge` hoặc `match_book_knowledge`.

Decision đã chốt:

```text
Không giữ fallback legacy RAG.
Không search qua book_knowledge khi section RAG không có kết quả.
Nếu section/hybrid RAG không tìm thấy, trả BOOK_CONTEXT_NOT_FOUND_MESSAGE để agent hỏi web-permission hoặc trả lời không có dữ liệu.
```

### Code cần sửa

#### `app/services/rag_service.py`

Xoá hoặc deprecate:

```python
LEGACY_BOOK_KNOWLEDGE_EMBEDDING_MODEL
search_learning_unit_knowledge()
AGENT_CANONICAL_SECTION_RAG_ENABLED branch
AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY branch
```

Logic target:

```text
if hybrid enabled:
    use section hybrid RAG
else:
    use section vector RAG
```

Không fallback về `book_knowledge`.

Target runtime flow:

```text
search_book_knowledge()
  -> if AGENT_HYBRID_RAG_ENABLED:
       search_book_hybrid_knowledge()
       -> match_book_section_knowledge
       -> match_book_section_knowledge_lexical
     else:
       search_book_section_knowledge()
       -> match_book_section_knowledge
```

Forbidden runtime flow:

```text
search_book_knowledge()
  -> search_learning_unit_knowledge()
  -> match_book_knowledge
  -> book_knowledge
```

#### `app/core/config.py`

Xoá hoặc ngừng dùng:

```python
AGENT_CANONICAL_SECTION_RAG_ENABLED
AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY
LEARNING_UNIT_LEGACY_RAG_INDEX_ENABLED
```

Khuyến nghị giữ ngắn hạn trong `.env.example` dưới nhóm deprecated nếu sợ deploy env cũ còn set, nhưng code runtime không đọc nữa.

#### `.env.example`

Đồng bộ default:

```env
AGENT_HYBRID_RAG_ENABLED=true
```

Không nên để:

```env
AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY=true
```

Vì config hiện tại default `False`, còn `.env.example` lại gợi ý `true`, dễ gây deploy lệch.

Sau cleanup, nên xoá hẳn dòng fallback này khỏi `.env.example` thay vì chỉ đổi thành `false`, vì nó không còn là một tùy chọn được support.

#### Tests

Sửa `tests/services/test_rag_service.py`:

- Xoá test legacy fallback.
- Thêm test đảm bảo `search_book_knowledge()` chỉ gọi hybrid hoặc section RAG.
- Thêm test khi section RAG không có kết quả thì trả `BOOK_CONTEXT_NOT_FOUND_MESSAGE`, không gọi legacy.
- Thêm test đảm bảo không còn reference `search_learning_unit_knowledge` trong public path.

## 6. Phase 14.2 - Remove legacy embedding pipeline

Status: **Implemented**

### Code cần xoá

- `app/services/embed_service.py`
- `app/repositories/book_knowledge_repo.py`
- Import và call `delete_knowledge_by_learning_unit` trong `app/services/workers/learning_unit_worker.py`
- `_run_rag_pipeline()` và `include_rag` trong `learning_unit_worker.py`
- `include_rag` parameter trong `book_pipeline.py`
- `LEARNING_UNIT_LEGACY_RAG_INDEX_ENABLED`

### Code cần giữ

- `app/services/book_section_knowledge_indexer.py`
- `app/repositories/book_section_knowledge_repo.py`
- `index_book_sections_task`
- `_enqueue_section_indexing(book_id)` trong upload flow

### Lưu ý kiến trúc

Section index nên chạy sau upload, không chạy theo từng learning unit. Vì section index là tri thức của tài liệu gốc, không phụ thuộc full/pareto audio generation.

## 7. Phase 14.3 - DB migration drop legacy RAG

Status: **Migration file created; execution requires DB target confirmation**

Chỉ làm sau khi Phase 14.1 và 14.2 pass test.

### Migration target

Tạo Alembic migration mới:

```powershell
uv run alembic revision -m "phase 14 drop legacy book knowledge"
```

Implementation đã tạo sẵn migration:

```text
app/db/migrations/versions/b14c2d3e4f50_phase_14_drop_legacy_book_knowledge.py
```

Upgrade:

```python
def upgrade() -> None:
    op.execute("drop function if exists match_book_knowledge(vector, double precision, integer, uuid[])")
    op.execute("drop table if exists book_knowledge cascade")
```

Không drop các RPC section:

```text
match_book_section_knowledge
match_book_section_knowledge_lexical
```

Hai RPC này là runtime path đúng của `book_section_knowledge`.

Downgrade:

```python
def downgrade() -> None:
    # Prefer no full restore here. Document that restoring this table requires DB backup.
    pass
```

### Vì sao downgrade có thể không restore full?

`book_knowledge` chứa embeddings cũ. Nếu drop table, downgrade không thể tự khôi phục vector data. Với destructive cleanup, rollback thực tế phải là DB backup/restore, không phải Alembic downgrade.

Production rule:

- Backup trước migration.
- Chạy audit row count.
- Chạy migration trên dev trước.
- Chỉ deploy production sau khi chat/voice RAG smoke test pass.

## 8. Phase 14.4 - Plan/progress query cleanup

Status: **Pending**

### Mục tiêu

Không còn query plan mơ hồ kiểu:

```python
select(ReadingPlan).where(ReadingPlan.book_id == book_id).first()
```

### Repository/helper đề xuất

Tạo hoặc bổ sung `app/repositories/reading_plan_repo.py`:

```python
def get_reading_plan_by_id_for_user(session, *, user_id, plan_id): ...
def get_current_plan_for_book(session, *, user_id, book_id): ...
def get_plan_for_book_mode(session, *, user_id, book_id, mode): ...
def list_plans_for_book(session, *, user_id, book_id): ...
```

Rule:

- Router/service không tự query `ReadingPlan` rải rác.
- Mọi query plan phải đi qua repository/helper có tên rõ ràng.
- Nếu business vẫn chỉ cho một plan chính trên một book, cần constraint hoặc code rule rõ ràng.

### Files cần refactor

- `app/services/audiobook_service.py`
- `app/services/learning_progress_service.py`
- `app/services/reading_plan_session_service.py`
- Tests ở `tests/test_phase4_2_learning_loop.py`, `tests/test_phase12_calendar_plan_sessions.py`, `tests/test_phase13_calendar_session_actions.py`

### Các case cần giữ

- `GET /api/v1/books/{book_id}/reading-plan` vẫn trả plan hiện tại cho FE.
- `PUT /api/v1/books/{book_id}/reading-plan` update plan hiện tại.
- Session regeneration vẫn preserve progress đã học.
- Book completed vẫn complete plan và cancel future sessions.

## 9. Phase 14.5 - Optional direct book context consolidation

Chưa khuyến nghị làm ngay.

Hiện tại `direct_book_context` đang có giá trị:

- map nhanh user + book -> context/thread;
- tránh tạo nhiều auto context cho cùng một sách;
- hỗ trợ direct discussion từ book detail.

Chỉ xoá nếu chốt business mới:

```text
Tất cả chat phải đi qua StudyContext.
Không còn direct book thread shortcut.
```

Nếu muốn xoá sau này, phải migrate:

```text
direct_book_context
-> study_contexts
-> study_context_document_links
-> chat_threads
```

Và update FE/API contract trước.

## 10. Phase 14.6 - Legacy naming cleanup

Không bắt buộc, nhưng nên làm để code dễ bảo trì:

- Đổi user-facing/internal wording từ `chapter` sang `section` hoặc `learning unit` ở nơi phù hợp.
- Không đổi các prompt cần hiểu user nói “chương”, vì người dùng vẫn sẽ hỏi theo “chương”.
- Không xoá test fixture tiếng Anh có `Chapter 1`, vì đó là nội dung tài liệu test.

Phân biệt:

```text
section/chapter trong câu hỏi user: giữ
chapter-era DB/service cũ: xoá
learning unit trong audio/progress: giữ
```

## 11. Test bắt buộc trước khi merge

### Static

```powershell
uv run ruff check app tests
uv run python -m py_compile app/services/rag_service.py app/services/workers/learning_unit_worker.py app/tasks/book_tasks.py
```

### Migration

```powershell
uv run alembic upgrade head
uv run alembic current
```

### RAG/chat/voice

```powershell
uv run pytest tests/services/test_rag_service.py -q
uv run pytest tests/services/agent_grounding -q
uv run pytest tests/services/agent_policy -q
```

Nếu có eval fixture Phase 10:

```powershell
uv run pytest tests/services/agent_observability -q
```

### Learning workflow

```powershell
uv run pytest tests/test_phase4_2_learning_loop.py -q
uv run pytest tests/test_phase11_learning_completion.py -q
uv run pytest tests/test_phase12_calendar_plan_sessions.py -q
uv run pytest tests/test_phase13_calendar_session_actions.py -q
```

### Manual smoke test

1. Upload PDF/DOCX thật.
2. Generate plan full.
3. Poll job tới `ready`.
4. Call book details.
5. Hỏi chat text câu nằm trong sách.
6. Hỏi voice câu nằm trong sách.
7. Update progress một unit.
8. Kiểm tra sessions update từ `scheduled/in_progress` sang `completed`.
9. Kiểm tra notification/review không lỗi.

## 12. Acceptance criteria

Phase này chỉ được xem là xong khi:

- Không còn import `BookKnowledge` trong runtime source.
- Không còn `book_knowledge_repo.py`.
- Không còn `embed_service.py` legacy learning-unit vector service.
- Không còn `match_book_knowledge` trong `rag_service.py`.
- Không còn `search_learning_unit_knowledge()` trong runtime source.
- Không còn flag `AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY`.
- Không còn flag `LEARNING_UNIT_LEGACY_RAG_INDEX_ENABLED`.
- `book_knowledge` table đã drop khỏi DB dev bằng migration mới.
- Chat/voice vẫn dùng được RAG qua `book_section_knowledge`.
- `match_book_section_knowledge` và `match_book_section_knowledge_lexical` vẫn tồn tại và pass tests.
- Plan/progress không còn query `.first()` mơ hồ theo `book_id` ở service chính.
- FE contract không bị breaking change.
- Các test learning workflow Phase 11/12/13 pass.

## 13. Thứ tự implement khuyến nghị

Làm theo 4 PR nhỏ hoặc 4 commit rõ ràng:

1. **PR 1 - RAG runtime cutover**
   - Remove legacy RAG fallback.
   - Update tests.

2. **PR 2 - Worker embedding cleanup**
   - Remove legacy per-learning-unit embedding path.
   - Keep section indexer.

3. **PR 3 - DB destructive cleanup**
   - Drop `book_knowledge` and `match_book_knowledge`.
   - Only after backup and audit.

4. **PR 4 - Plan/progress repository cleanup**
   - Centralize plan queries.
   - Remove ambiguous `.first()` patterns.

Không gộp destructive DB migration với refactor lớn. Nếu lỗi xảy ra, khó xác định là do migration hay do logic.

## 14. Vấn đề chưa chốt

### 14.1. Có giữ nhiều plan lịch sử cho cùng một book/mode không?

Hiện system có thể regenerate sessions và giữ history cancelled, nhưng chưa có learning round chính thức.

Recommendation hiện tại:

- Giữ một current plan chính cho mỗi book.
- Chưa thêm learning round cho tới khi cần chức năng “học lại sách từ đầu”.

### 14.2. Có xoá `direct_book_context` không?

Recommendation hiện tại:

- Chưa xoá.
- Đây không phải legacy chết, mà là shortcut phục vụ direct book discussion.

### 14.3. Có cần migrate data từ `book_knowledge` sang `book_section_knowledge` không?

Recommendation hiện tại:

- Không migrate vector cũ.
- Re-index từ `book_sections` bằng `index_book_sections_task`.
- Vector cũ theo learning unit không đủ tốt cho section-grounded RAG.

## 15. Kết luận kỹ thuật

Phần cần clean thật sự nhất là legacy RAG:

```text
book_knowledge
match_book_knowledge
embed_service.py
book_knowledge_repo.py
legacy fallback in rag_service.py
legacy include_rag path in learning_unit_worker.py
```

Phần plan/progress không nên xoá, vì đây là kiến trúc mới đúng. Việc cần làm là chuẩn hoá query và repository để tránh logic cũ kiểu “lấy plan đầu tiên” gây lỗi khi hệ thống lớn hơn.

Phase 14 nên ưu tiên an toàn dữ liệu: cắt code path trước, test RAG/learning workflow, rồi mới drop DB.
