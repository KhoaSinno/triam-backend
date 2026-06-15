# Phase 14.2 Implementation Guide - Runtime Cleanup And Legacy Code Removal

## 1. Mục tiêu

Phase 14.2 tập trung dọn phần code runtime và script cũ sau khi hệ thống đã chuyển sang kiến trúc mới:

```text
BookSection -> LearningUnit -> LearningUnitSegment
ReadingPlan -> ReadingPlanScheduleSlot -> ReadingPlanSession -> ReadingPlanSessionUnit
BookSectionKnowledge -> hybrid/vector/lexical RAG
```

Mục tiêu chính:

- Xóa code sai hoặc không còn chạy đúng với kiến trúc hiện tại.
- Xóa script legacy còn trỏ về `book_knowledge`, `chapters`, `chapter_segments`.
- Sửa config/env gây hiểu nhầm hoặc không có tác dụng.
- Gỡ endpoint demo không nên xuất hiện ở production.
- Làm comment code ngắn hơn, giải thích business rule thay vì mô tả từng bước.
- Không phá API FE đang dùng.
- Không squash migration trong phase này.

## 1.1 Kết quả implement

Phase này đã được implement theo hướng xóa hẳn legacy path, không giữ flag rollback mơ hồ.

Đã làm:

- Xóa query overlap guard cũ trong voice agent.
- Xóa các env/config liên quan `VOICE_AGENT_QUERY_GUARD_*OVERLAP*`.
- Xóa endpoint demo `/test-voice-stream-edge`.
- Xóa helper PDF raw extraction/debug không còn dùng.
- Xóa alias compatibility cũ `ChapterTooLargeError` và `BookInput`.
- Xóa script/test manual legacy Phase 5/7/RAG/WebSocket/Supabase auth cũ.
- Xóa dependency dev `websockets` vì chỉ còn phục vụ script đã xóa.
- Clean script dev còn giữ: database reset, RLS setup, Firebase smoke test, DB connect, model listing.
- Refactor nhỏ `section_resolver.py` và `transcription_prompt.py` để ruff runtime sạch hơn mà không đổi contract.
- Dọn format migration lịch sử ở mức import/whitespace, không đổi SQL behavior.

Checks đã chạy:

```powershell
uv run ruff check app tests scripts
uv run pytest tests -q
uv run python -m py_compile app/main.py app/core/config.py app/core/exceptions.py app/schemas/audiobook.py app/services/agent_voice_gpt_realtime.py app/services/voice_agent/query_guard.py app/services/agent_grounding/section_resolver.py app/services/voice_agent/transcription_prompt.py app/services/pdf_service.py app/services/tts_service.py scripts/clean_database.py scripts/enable_rls.py scripts/list_models.py scripts/check_model_methods.py scripts/test_db_connect.py scripts/test_firebase_connection.py
git diff --check
```

Kết quả:

- `ruff`: pass.
- `pytest`: `296 passed`.
- `py_compile`: pass.
- `git diff --check`: pass.

## 2. Nguyên tắc cleanup

### 2.1 Xóa thẳng khi thỏa ít nhất một điều kiện

- File gọi bảng/RPC đã bị drop, ví dụ `book_knowledge`, `match_book_knowledge`.
- Script import hàm không còn tồn tại.
- Script là test tay cũ đã được thay bằng script/test mới rõ hơn.
- Alias compatibility không còn import ở đâu.
- Endpoint demo public không phục vụ sản phẩm.

### 2.2 Không xóa nếu đang là runtime contract

Không xóa các bảng/model sau:

- `book_sections`
- `learning_units`
- `learning_unit_sources`
- `learning_unit_segments`
- `learning_unit_progress`
- `book_learning_states`
- `reading_plan_schedule_slots`
- `reading_plan_sessions`
- `reading_plan_session_units`
- `book_section_knowledge`
- `notification_outbox`
- `user_notifications`
- `direct_book_context`

Lý do:

- Đây là phần kiến trúc mới đang phục vụ upload, generate plan, nghe audio, tracking progress, lịch học, nhắc học, chat theo sách và RAG.
- Một số bảng nhìn như cache/tổng hợp, ví dụ `book_learning_states`, nhưng cần cho resume nhanh và giảm query nặng cho FE.

### 2.3 Không xóa migration cũ trong phase này

Các migration cũ có nhắc `chapters`, `chapter_segments`, `book_knowledge` là lịch sử Alembic. Không được xóa file migration cũ nếu production/dev DB đang dùng Alembic history.

Nếu muốn repo sạch tuyệt đối cho bản luận văn cuối, tạo phase riêng:

```text
Phase 14.3 - Alembic Baseline Squash
```

Chỉ làm phase đó khi chấp nhận reset toàn bộ DB hoặc đã có quy trình migrate production rõ ràng.

## 3. Việc cần làm trong Phase 14.2

## 3.1 Sửa logger sai trong `app/main.py`

### Hiện trạng

`app/main.py` đang import logger từ Alembic:

```python
from alembic.autogenerate.api import log
```

Đây là sai về kiến trúc. FastAPI runtime không nên dùng logger nội bộ của Alembic.

### Cách sửa

Đổi sang logger chung của app:

```python
from app.core.logger import log
```

### Lý do

- Log runtime thống nhất với cấu hình redaction.
- Tránh phụ thuộc vô tình vào internal API của Alembic.
- Dễ kiểm soát log level khi deploy.

## 3.2 Xóa endpoint demo `/test-voice-stream-edge`

### Hiện trạng

`app/main.py` có endpoint:

```python
@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(...)
```

Endpoint này public và có thể bị gọi để tạo audio thử.

### Cách xử lý

Xóa:

- import `StreamingResponse`
- import `stream_text_to_speech_edge`
- route `/test-voice-stream-edge`

Nếu vẫn cần test TTS, dùng script local:

```text
scripts/test_google_tts.py
```

hoặc tạo script dev-only riêng, không expose qua FastAPI production.

### Lý do

- Tránh người ngoài gọi API để đốt tài nguyên TTS.
- Làm API surface gọn hơn.
- Backend production chỉ giữ endpoint phục vụ sản phẩm.

## 3.3 Sửa `.env.example` sai cú pháp

### Hiện trạng

`.env.example` đang có dòng dạng Python:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
```

Đây không phải cú pháp `.env` hợp lệ.

### Cách sửa

Đổi thành:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
```

### Lý do

- Tránh copy sai khi deploy.
- Giúp biến môi trường hoạt động đúng với Pydantic settings.

## 3.4 Xóa biến `VOICE_AGENT_QUERY_GUARD_ENFORCE_TRANSCRIPT_OVERLAP`

### Hiện trạng

Voice query guard từng có nhánh so khớp token giữa tool query và transcript:

```python
VOICE_AGENT_QUERY_GUARD_ENFORCE_TRANSCRIPT_OVERLAP: bool = False
```

Nhánh này không ổn định với tiếng Việt, câu ngắn, câu xác nhận, hoặc STT bị sửa lại giữa final transcript và committed text.

### Cách sửa đã chốt

Xóa hẳn:

- `VOICE_AGENT_QUERY_GUARD_ENFORCE_TRANSCRIPT_OVERLAP`
- `VOICE_AGENT_QUERY_GUARD_MIN_OVERLAP_RATIO`
- `VOICE_AGENT_QUERY_GUARD_MIN_IMPORTANT_OVERLAP_RATIO`
- field tương ứng trong `VoiceQueryGuardConfig`
- nhánh `tool_query_transcript_mismatch` / `tool_query_important_token_mismatch`

Voice guard chỉ còn chịu trách nhiệm chặn các lượt quá ngắn, câu trả lời permission, và clarification flow. Chất lượng STT/RAG được đo bằng trace/eval riêng thay vì chặn bằng overlap heuristic.

### Lý do

- Một flag có tác dụng mơ hồ làm dev sau debug sai hướng.
- Overlap heuristic dễ chặn nhầm câu hỏi hợp lệ.
- Khi STT sai, giải pháp đúng là đo trace, cải thiện transcription prompt, retrieval, và model policy.

## 3.5 Xóa script legacy RAG cũ

### Xóa các file sau

```text
scripts/recreate_rpcs.py
scripts/test_rag.py
scripts/test_rag_R.py
scripts/old_generate_rag_report.py
```

### Lý do

Các script này còn dùng:

```text
book_knowledge
match_book_knowledge
```

Trong khi kiến trúc mới đã dùng:

```text
book_section_knowledge
match_book_section_knowledge
match_book_section_knowledge_lexical
```

Giữ các script này sẽ làm người mới hiểu sai hệ thống RAG hiện tại.

### Script thay thế cần giữ

```text
scripts/backfill_book_section_knowledge.py
scripts/production_smoke_test.py
```

## 3.6 Xóa hoặc viết lại script PDF test cũ

### File cần xử lý

```text
scripts/test_pdf_extraction.py
```

### Lý do

Script này import:

```python
extract_pdf_chapters
```

Nhưng hàm này không còn tồn tại trong `app/services/pdf_service.py`.

### Cách xử lý khuyến nghị

Xóa file này.

Nếu sau này cần test parser PDF bằng tay, tạo script mới dùng API hiện tại:

```python
from app.services.pdf_service import parse_pdf_structure
```

Không dùng lại khái niệm `chapter extraction`.

## 3.7 Dọn manual integration tests bị đặt nhầm trong `tests/`

### File hiện tại

```text
tests/test_phase7_realtime_voice_chat.py
tests/test_phase7_1_voice_web_permission.py
```

Hai file này tự ghi rõ là manual integration test, cần server thật, LiveKit thật, token thật.

### Cách xử lý

Di chuyển sang:

```text
scripts/manual_integration/phase7_realtime_voice_chat.py
scripts/manual_integration/phase7_1_voice_web_permission.py
```

Sau khi move, kiểm tra lại import/path fixture audio:

```text
tests/fixtures/Có-những-phương-pháp.wav
tests/fixtures/yub-làm-đi.wav
```

### Lý do

- `pytest` mặc định chỉ nên chạy unit/API tests có thể tự động hóa.
- Manual tests cần lệnh riêng, không nằm trong test suite mặc định.
- Tránh CI/local test bị treo vì đòi LiveKit thật.

## 3.8 Xóa script test tay cũ nếu đã có script thay thế

### Có thể xóa

```text
scripts/phase5_real_flow_test.py
scripts/test_live_client.py
scripts/test_websocket.py
scripts/upload_llm_rewrite_flow/test_llm_bug.py
scripts/auth_script_test_supabase/test_login.py
scripts/auth_script_test_supabase/test_supabase_sdk.py
```

### Điều kiện xóa

Chỉ xóa nếu các flow này đã được thay thế bởi:

```text
scripts/get_supabase_access_token.py
scripts/production_smoke_test.py
scripts/manual_integration/phase10_agent_eval.py
tests/services/**
```

### Khuyến nghị

Trong Phase 14.2, xóa các script chắc chắn lỗi hoặc trỏ DB cũ trước. Với các script test provider còn hữu ích, giữ lại.

Giữ:

```text
scripts/get_supabase_access_token.py
scripts/production_smoke_test.py
scripts/backfill_book_section_knowledge.py
scripts/test_google_tts.py
scripts/test_firebase_connection.py
scripts/test_db_connect.py
scripts/clean_database.py
scripts/enable_rls.py
```

## 3.9 Xóa alias compatibility cũ

### File 1

`app/core/exceptions.py`

Hiện có:

```python
ChapterTooLargeError = LearningUnitTooLargeError
```

Nếu không còn import ở đâu, xóa alias này.

### File 2

`app/schemas/audiobook.py`

Hiện có:

```python
BookInput = BookUpdateRequest
```

Nếu không còn import ở đâu, xóa alias này.

### Lý do

- Các alias này giữ lại từ giai đoạn đổi chapter -> learning unit.
- Nếu không còn ai import, giữ lại chỉ làm người đọc tưởng vẫn có logic cũ.

## 3.10 Dọn helper PDF legacy

### File

`app/services/pdf_service.py`

Các hàm có thể xóa nếu không còn script nào cần:

```python
extract_text_from_pdf
extract_text_by_page_range
extract_clean_text
```

### Không xóa

Giữ:

```python
parse_pdf_structure
get_pdf_outline_structure
```

`parse_pdf_structure` là parser runtime chính.

`get_pdf_outline_structure` cũng xóa nếu không còn import runtime/test nào dùng.

## 3.11 Dọn comment kiểu tutorial

### Nơi nên sửa

```text
app/main.py
app/api/v1/routers/upload.py
app/services/upload_service.py
app/repositories/audiobook_repo.py
app/services/pdf_service.py
```

### Nguyên tắc comment mới

Nên comment business invariant:

```python
# Upload succeeds before DB commit so a book never points to a missing raw file.
```

Không nên comment từng bước hiển nhiên:

```python
# 1. Validate MIME Type hoặc đuôi file
# 2. Lưu file tạm để extract outline
# 3. Extract deterministic outline tree từ tài liệu
```

### Lý do

Code production nên đọc như hệ thống thật, không giống bài tutorial.

## 3.12 Dọn `__pycache__`

### Lệnh local

PowerShell:

```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```

### Lưu ý

Chỉ xóa local cache, không cần migration/test logic.

Nếu `__pycache__` bị track trong git thì phải xóa khỏi git và kiểm tra `.gitignore`.

## 4. Không làm trong Phase 14.2

Không làm các việc sau trong phase này:

- Không squash Alembic migrations.
- Không đổi response contract `schedule_config` ngay.
- Không drop bảng runtime mới.
- Không refactor lớn `audiobook_service.py` thành nhiều service nếu chưa có test contract đầy đủ.
- Không đổi logic voice agent ngoài việc xóa query overlap guard legacy.
- Không đổi RAG ranking/hybrid score.
- Không đổi business rule lịch học.

## 5. Những phần nên để Phase sau

### Phase 14.3 - Alembic Baseline Squash

Chỉ làm nếu:

- DB dev/prod có thể reset hoặc có migration strategy rõ.
- Muốn repo sạch cho giai đoạn cuối luận văn.

### Phase 14.4 - Service Boundary Refactor

Tách:

```text
app/services/audiobook_service.py
```

thành:

```text
book_service.py
book_detail_service.py
reading_plan_service.py
switch_mode_service.py
```

Chỉ nên làm sau khi Phase 14.2 xanh test.

### Phase 14.5 - Voice Agent Architecture Slimdown

Tách tiếp `agent_voice_gpt_realtime.py` theo nhóm:

```text
voice_session_factory.py
voice_text_chat_handler.py
voice_realtime_handler.py
voice_tool_registry.py
voice_prompt_builder.py
```

Không làm chung với Phase 14.2 vì rủi ro realtime cao.

## 6. Checklist implementation

### Step 1 - Cleanup config/runtime nhỏ

- [ ] Sửa logger import trong `app/main.py`.
- [ ] Xóa `/test-voice-stream-edge`.
- [ ] Xóa import không còn dùng trong `app/main.py`.
- [ ] Sửa `.env.example`.
- [ ] Xóa query guard overlap env/config/logic cũ.

### Step 2 - Xóa script sai/legacy

- [ ] Xóa script `book_knowledge` legacy.
- [ ] Xóa script PDF test cũ bị hỏng.
- [ ] Move manual LiveKit tests ra khỏi `tests/`.
- [ ] Xóa script one-off không còn giá trị.

### Step 3 - Dọn alias/helper cũ

- [ ] Xóa `ChapterTooLargeError` alias nếu không import.
- [ ] Xóa `BookInput` alias nếu không import.
- [ ] Xóa helper PDF không dùng.

### Step 4 - Comment cleanup

- [ ] Rút gọn comment tutorial.
- [ ] Giữ comment giải thích business rule và side effect.

### Step 5 - Cache cleanup

- [ ] Xóa `__pycache__`.
- [ ] Kiểm tra git không track `.pyc`.

## 7. Test bắt buộc sau cleanup

### Static checks

```powershell
uv run ruff check app tests scripts
uv run python -m py_compile app/main.py app/services/agent_voice_gpt_realtime.py app/services/pdf_service.py
```

### Focused tests

```powershell
uv run pytest tests/test_document_parsers.py -q
uv run pytest tests/services/test_rag_service.py -q
uv run pytest tests/services/voice_agent/test_query_guard.py -q
uv run pytest tests/services/voice_agent/test_agent_voice_query_guard.py -q
uv run pytest tests/test_auth_user_isolation.py -q
uv run pytest tests/test_phase12_calendar_plan_sessions.py tests/test_phase13_calendar_session_actions.py -q
```

### Smoke local API

Chạy server:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Call:

```text
GET /api/v1/health
GET /api/v1/books
GET /api/v1/books/{book_id}/reading-plan
GET /api/v1/reading-plan/sessions
GET /api/v1/notifications
```

### Manual checks

- Upload PDF/DOCX/EPUB vẫn nhận outline đúng.
- Generate plan vẫn tạo job.
- Job vẫn qua Celery document worker.
- Book detail vẫn trả `units`.
- Reading progress vẫn update.
- Voice agent vẫn start được.

## 8. Rủi ro và rollback

### Rủi ro 1 - FE hoặc script ngoài repo còn dùng endpoint demo

Khả năng thấp. Nếu FE đang gọi `/test-voice-stream-edge`, đó là sai scope production. FE phải dùng audio đã generate hoặc flow voice LiveKit.

Rollback:

- Khôi phục endpoint tạm thời trong branch hotfix.
- Sau đó thay FE.

### Rủi ro 2 - Manual test bị mất do xóa script

Giải pháp:

- Chỉ giữ manual test có hướng dẫn chạy rõ trong `scripts/manual_integration`.
- Script cũ gọi DB/table đã drop thì không nên giữ.

### Rủi ro 3 - Xóa overlap guard làm giảm khả năng chặn STT lệch

Đây là đánh đổi có chủ ý. Overlap guard từng chặn nhầm nhiều hơn là giúp ổn định hội thoại.

Giải pháp thay thế:

- Dùng agent trace Phase 10 để đo transcript/query/source.
- Giữ clarification state cho các lượt xác nhận thật sự.
- Tối ưu STT prompt và grounding router bằng test production có ground truth.

## 9. Definition of Done

Phase 14.2 hoàn tất khi:

- Không còn script runtime/manual hiện tại gọi `book_knowledge` hoặc `match_book_knowledge`.
- Không còn endpoint demo public TTS trong FastAPI.
- `.env.example` không còn dòng sai cú pháp.
- Không còn query guard overlap env/config/logic cũ.
- `pytest` focused pass.
- `ruff check` pass cho file đã đổi.
- Không thay đổi DB schema runtime.
- Không breaking FE contract.
