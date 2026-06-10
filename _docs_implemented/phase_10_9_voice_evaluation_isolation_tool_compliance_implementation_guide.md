# Phase 10.9 Implementation Guide - Voice Evaluation Isolation And Tool Compliance

Date: 2026-06-06  
Status: Implemented and offline-tested  
Depends on: Phase 10.0 -> 10.8  
Primary scope: voice eval determinism, LiveKit room/thread isolation, voice tool compliance, audio fixture quality

---

## Implementation Status

Implemented files:

- `scripts/manual_integration/phase10_agent_eval.py`
  - added direct-script project-root bootstrap;
  - added `--isolate-voice-cases`;
  - added `--voice-isolation-strategy`;
  - added `--case-thread-map`;
  - added `--disconnect-grace-seconds`;
  - refactored LiveKit connection lifecycle into `EvalRoomSession`, `connect_eval_room`, and `disconnect_eval_room`;
  - supports room-only isolation and case-thread room isolation;
  - records `eval_thread_id`, `eval_room_name`, `isolation_strategy`, and `case_isolation_quality` per case;
  - calculates DB message delta across all eval threads used by the selected cases;
  - defaults new reports to `_docs_implemented/eval_reports/phase10_9`.
- `app/services/agent_observability/model_eval_report.py`
  - added `VOICE_TOOL_BYPASS` classification;
  - treats `VOICE_TOOL_BYPASS` as a primary failure code and suppresses generic routing/context-validation noise for that case;
  - added warning counts for non-fatal evaluator issues such as `INPUT_STT_MINOR`;
  - renders `## Voice Isolation` in markdown reports when metadata exists.
- `tests/fixtures/agent_eval/voice_case_threads.example.json`
  - committed example map for clean per-case voice thread evaluation.
- `.gitignore`
  - ignores `tests/fixtures/agent_eval/*.local.json`.
- `tests/services/agent_observability/test_model_eval_report.py`
  - covers `VOICE_TOOL_BYPASS`;
  - covers non-fatal warning counts;
  - covers markdown voice isolation rendering.
- `tests/services/agent_observability/test_phase10_eval_runner.py`
  - covers thread-map validation;
  - covers strategy validation;
  - covers eval thread id collection and isolation quality.
  - covers clarification intent aliasing;
  - covers minor STT warning behavior.
- `tests/services/agent_observability/test_eval_fixtures.py`
  - verifies example thread map matches all voice cases.

Verification completed:

```powershell
uv run ruff check app\services\agent_observability\model_eval_report.py scripts\manual_integration\phase10_agent_eval.py tests\services\agent_observability
uv run python -m py_compile app\services\agent_observability\model_eval_report.py scripts\manual_integration\phase10_agent_eval.py
uv run pytest tests\services\agent_observability -q
uv run pytest tests\services\voice_agent tests\services\agent_policy -q
uv run python scripts\manual_integration\phase10_agent_eval.py --help
uv run pytest tests -q --maxfail=1 --durations=20
```

Results:

```text
Ruff passed.
Py compile passed.
41 agent_observability tests passed.
53 voice_agent/agent_policy tests passed.
Manual runner --help passed.
250 full test-suite tests passed.
```

Not run automatically:

- real LiveKit/provider voice eval;
- production Hugging Face eval.

Reason:

```text
These require running FastAPI, realtime worker, LiveKit Cloud, provider calls, and a valid access token.
```

---

## Phase 10.9.1 Patch - Clarification Trace Normalization And Minor STT Warning

Date: 2026-06-06  
Status: Implemented and offline-tested  

### Why This Patch Exists

Real `case_thread_new_room` evaluation produced a useful result:

```text
3/5 passed, but the two failed cases were not true RAG/tool failures.
```

Observed issues:

1. `mice-author-vi-voice`
   - STT transcript became `Giả của quyển sách là ai?`.
   - Agent still understood the request and answered `John Steinbeck`.
   - Trace was correct: `detected_intent=book_metadata.author`, `answer_source=book_metadata`.
   - The evaluator was too strict because `voice_transcript_meaning=false` made the whole case fail.

2. `mice-ambiguous-chapter-vi-voice`
   - Agent response correctly asked which chapter the user wanted.
   - Trace had `answer_source=clarification`.
   - But `detected_intent=None`, while fixture expected `clarification_required`.
   - This is instrumentation/evaluator mismatch, not bad user-facing behavior.

### What Changed

Files:

```text
scripts/manual_integration/phase10_agent_eval.py
app/services/agent_observability/model_eval_report.py
tests/services/agent_observability/test_phase10_eval_runner.py
tests/services/agent_observability/test_model_eval_report.py
```

Changes:

- Added `expected_intent_matches`.
  - If fixture expects `clarification_required` and trace says `answer_source=clarification`, intent check passes even when `detected_intent` is missing.
- Added `INPUT_STT_MINOR` warning.
  - If voice transcript keyword check fails but semantic behavior passes, the case can still pass.
  - The warning remains visible in JSON and Markdown report.
  - `voice_meaning_preservation_rate` still reports the STT/fixture quality honestly.
- Added `warning_counts` to metrics.
- Added `## Warnings` table to Markdown reports when warnings exist.

### Why This Is Better

This keeps two truths separate:

```text
Did the user-facing agent behave correctly?
Did STT preserve the exact expected wording?
```

For production quality, we still care about STT quality. But we should not fail a grounded-answer test if:

- the agent inferred intent correctly;
- selected the right source;
- returned the right content;
- did not violate web policy.

### Verification

```powershell
uv run ruff check app\services\agent_observability\model_eval_report.py scripts\manual_integration\phase10_agent_eval.py tests\services\agent_observability
uv run python -m py_compile app\services\agent_observability\model_eval_report.py scripts\manual_integration\phase10_agent_eval.py
uv run pytest tests\services\agent_observability -q
uv run pytest tests\services\voice_agent tests\services\agent_policy -q
```

Results:

```text
Ruff passed.
Py compile passed.
41 agent_observability tests passed.
53 voice_agent/agent_policy tests passed.
```

### Expected Real Eval Effect

After rerunning:

- `mice-author-vi-voice` should pass with warning `INPUT_STT_MINOR` if behavior remains semantically correct.
- `mice-ambiguous-chapter-vi-voice` should pass when `answer_source=clarification`.
- `warning_counts` should show STT weakness without marking grounded behavior as failed.

This patch does not change the realtime agent prompt, model, RAG, LiveKit contract, or FE contract.

---

## 0. Why Phase 10.9 Exists

Phase 10.8 đã làm sạch phần đo đạc tổng thể:

- text mode đạt kết quả ổn định hơn;
- canonical section RAG và hybrid RAG đã được bật;
- report không leak access token;
- trace đã ghi được nhiều metadata hơn;
- failure code đã phân biệt lỗi trace, timeout, STT và fixture.

Nhưng report voice-only mới nhất vẫn còn 3 case fail:

```text
_docs_implemented/eval_reports/phase10_8/phase10_8_eval_20260606_165324_baseline.md
```

Kết quả chính:

| Case | Nhận định |
| --- | --- |
| `mice-author-vi-voice` | Pass. Agent dùng metadata/tool đúng. |
| `mice-chapter-four-summary-vi-voice` | Pass. Agent resolve đúng chương 4. |
| `mice-chapter-four-idea-vi-voice` | Nội dung trả lời đúng, nhưng trace cho thấy `tool_names=[]`, `answer_source=unknown`. Đây là dấu hiệu voice bypass tool. |
| `mice-ambiguous-chapter-vi-voice` | Agent trả lời theo ngữ cảnh trước đó thay vì hỏi rõ. Có khả năng case bị ảnh hưởng bởi cùng room/thread đang giữ state trước. |
| `mice-current-bitcoin-vi-voice` | STT nhận thành “Hôm nay là bao nhiêu?”, mất từ “Bitcoin”. Đây là lỗi input/audio fixture, không nên chấm là lỗi web policy. |

Vì vậy Phase 10.9 không nên bắt đầu bằng sửa prompt/model. Phase này cần làm bộ voice evaluation đáng tin trước:

```text
Tách lỗi do input, lỗi do state cũ, và lỗi agent bỏ qua tool.
```

Nếu đo chưa đúng, mọi quyết định nâng model, sửa prompt hoặc chỉnh RAG đều có nguy cơ tối ưu sai tầng.

---

## 1. Review Đề Xuất Của Gemini

Gemini đề xuất 3 ý:

1. Thêm `--isolate-voice-cases`.
2. Thêm failure code `VOICE_TOOL_BYPASS`.
3. Làm sạch audio fixtures, đặc biệt case Bitcoin.

Anh đồng ý với hướng này, nhưng cần chỉnh một điểm rất quan trọng:

```text
Ngắt LiveKit room rồi lấy token mới chỉ làm sạch realtime room/session.
Nó chưa chắc làm sạch lịch sử hội thoại nếu vẫn dùng cùng thread_id.
```

Trong hệ thống hiện tại:

- LiveKit token được lấy từ `GET /api/v1/live-token/thread/{thread_id}`;
- mỗi lần gọi token tạo `room_name` mới;
- nhưng metadata vẫn chứa cùng `thread_id`;
- agent có thể load lịch sử chat từ DB theo `thread_id`;
- vì vậy nếu dùng lại cùng thread, case sau vẫn có thể bị ảnh hưởng bởi lịch sử case trước.

Kết luận:

```text
Đề xuất đúng hướng, nhưng Phase 10.9 phải tách rõ room isolation và thread isolation.
```

Nếu chỉ tạo room mới, report phải ghi rõ đó là `room_only`, không được gọi là “thread sạch”.

---

## 2. Goals

Phase 10.9 cần đạt các mục tiêu:

1. Voice eval có thể chạy từng case trong room mới.
2. Voice eval có chiến lược thread isolation rõ ràng:
   - dùng cùng thread nhưng room mới;
   - hoặc dùng thread riêng cho từng case.
3. Report ghi rõ isolation strategy để không hiểu nhầm kết quả.
4. Failure code phân biệt được `VOICE_TOOL_BYPASS`.
5. Audio fixture Bitcoin phải kiểm tra đúng ý định thật, không hạ tiêu chuẩn chỉ để pass.
6. Manual eval vẫn không leak token.
7. Không thay đổi API/contract của FE.
8. Không sửa prompt/model/RAG behavior trong cùng phase, trừ khi chỉ là instrumentation bắt buộc.

---

## 3. Non-Goals

Phase này không làm:

- không đổi default model;
- không đổi prompt chính của realtime agent;
- không đổi RAG ranking;
- không đổi web-search permission behavior;
- không thêm endpoint production mới chỉ để phục vụ test;
- không sửa câu trả lời riêng cho sách `Of Mice and Men`;
- không làm test real voice thành pytest mặc định.

Đây là phase evaluation hardening. Behavior tuning nên để phase sau, khi số liệu voice đã sạch.

---

## 4. Design Principle

### 4.1 Separate Three Layers

Mỗi voice case fail phải phân loại theo 3 tầng:

| Layer | Ví dụ | Cách xử lý |
| --- | --- | --- |
| Input/STT | Audio nói “Bitcoin” nhưng transcript mất “Bitcoin” | Sửa fixture hoặc metadata expected |
| Isolation/state | Case mơ hồ bị ảnh hưởng bởi câu hỏi trước | Tách room/thread |
| Tool compliance | Agent trả lời câu hỏi sách nhưng không gọi tool | Sửa prompt/tool policy sau khi đo được |

Không được gom cả 3 thành “model ngu” hoặc “RAG cùi”.

### 4.2 Room Isolation Is Not Thread Isolation

Room isolation:

```text
Mỗi case reconnect LiveKit room mới.
```

Ưu điểm:

- giảm ảnh hưởng audio/session buffer;
- giảm khả năng event từ case trước tràn sang case sau;
- phù hợp với LiveKit lifecycle.

Giới hạn:

- nếu cùng `thread_id`, DB history vẫn còn;
- agent có thể đọc lại lịch sử cũ;
- ambiguous follow-up có thể vẫn dùng ngữ cảnh trước.

Thread isolation:

```text
Mỗi case dùng thread riêng hoặc thread đã dọn sạch history.
```

Ưu điểm:

- deterministic hơn;
- case mơ hồ sẽ thật sự là mơ hồ;
- metric intent/tool/source đáng tin hơn.

Trade-off:

- tạo thêm dữ liệu test trong DB;
- setup test phức tạp hơn;
- nếu tạo/xóa thread tự động cần rất cẩn thận ownership và cleanup.

Recommendation cho dự án:

```text
Phase 10.9 implement room isolation trước, nhưng thiết kế sẵn thread isolation qua case-thread map.
```

Không nên tự động tạo/xóa thread trong runner nếu chưa có endpoint test-safe rõ ràng. Cách sạch hơn cho capstone:

- chuẩn bị trước một danh sách thread eval;
- truyền vào runner bằng file map;
- mỗi case dùng một thread riêng;
- không xóa dữ liệu sau test để có thể audit DB.

---

## 5. Implementation Plan

### Step 1 - Add Voice Isolation CLI Options

File:

```text
scripts/manual_integration/phase10_agent_eval.py
```

Thêm arguments:

```python
parser.add_argument(
    "--isolate-voice-cases",
    action="store_true",
    help="Reconnect a fresh LiveKit room for each voice case.",
)
parser.add_argument(
    "--voice-isolation-strategy",
    choices=("shared_thread_new_room", "case_thread_new_room"),
    default="shared_thread_new_room",
)
parser.add_argument(
    "--case-thread-map",
    help="Optional JSON file mapping case id to thread_id for clean voice eval.",
)
```

Ý nghĩa:

| Option | Ý nghĩa |
| --- | --- |
| `--isolate-voice-cases` | Mỗi voice case reconnect room mới. |
| `shared_thread_new_room` | Cùng thread, room mới. Không sạch DB history. |
| `case_thread_new_room` | Mỗi case dùng thread riêng từ map. Sạch hơn cho eval. |
| `--case-thread-map` | File JSON chứa mapping `case_id -> thread_id`. |

Ví dụ file map:

```json
{
  "mice-author-vi-voice": "11111111-1111-1111-1111-111111111111",
  "mice-chapter-four-summary-vi-voice": "22222222-2222-2222-2222-222222222222",
  "mice-chapter-four-idea-vi-voice": "33333333-3333-3333-3333-333333333333",
  "mice-ambiguous-chapter-vi-voice": "44444444-4444-4444-4444-444444444444",
  "mice-current-bitcoin-vi-voice": "55555555-5555-5555-5555-555555555555"
}
```

Template nên được commit vào git:

```text
tests/fixtures/agent_eval/voice_case_threads.example.json
```

Nội dung template dùng UUID giả hoặc placeholder để FE/BE/dev biết format, không chứa thread thật của môi trường dev/prod.

File thật dùng khi chạy local nên là:

```text
tests/fixtures/agent_eval/voice_case_threads.local.json
```

Rule:

```text
Commit file .example.json.
Không commit file .local.json.
Thêm tests/fixtures/agent_eval/*.local.json vào .gitignore khi implement.
```

Rule:

```text
Nếu strategy là case_thread_new_room mà thiếu case-thread-map thì fail sớm.
Không silently fallback sang shared thread.
```

### Step 2 - Refactor Runner Connection Lifecycle

Hiện tại runner connect room một lần rồi chạy toàn bộ cases.

Refactor thành helper:

```python
async def connect_eval_room(
    http: aiohttp.ClientSession,
    *,
    base_url: str,
    livekit_url: str,
    thread_id: str,
    timeout: float,
) -> EvalRoomSession:
    ...
```

`EvalRoomSession` nên chứa:

```python
@dataclass
class EvalRoomSession:
    room: rtc.Room
    room_name: str
    thread_id: str
    chat_queue: asyncio.Queue[str]
    transcript_queue: asyncio.Queue[dict[str, Any]]
```

Flow mới:

```text
For each case:
  resolve effective_thread_id
  if first case or isolation required:
      disconnect old room if exists
      wait short disconnect grace period
      get new LiveKit token
      connect new room
      wait greeting
      drain queues
  run case
  read trace filtered by thread_id + room_name
```

Quan trọng:

- luôn `await room.disconnect()` trong `finally`;
- khi disconnect room cũ trong vòng lặp, nên chờ một khoảng nhỏ, ví dụ `await asyncio.sleep(0.5)`, để LiveKit socket/resource đóng hẳn trước khi tạo room mới;
- sau reconnect phải drain queue;
- trace offset phải lấy ngay trước từng case;
- trace filter dùng đúng `effective_thread_id` và `room_name`;
- report lưu `effective_thread_id`, `room_name`, `isolation_strategy`.

Nên tạo helper riêng:

```python
async def disconnect_eval_room(session: EvalRoomSession | None, *, grace_seconds: float = 0.5) -> None:
    if session is None:
        return
    await session.room.disconnect()
    await asyncio.sleep(grace_seconds)
```

Lý do:

```text
Không để logic disconnect rải rác trong loop.
Tránh reconnect quá nhanh làm LiveKit client còn pending socket/task cũ.
Giữ cleanup an toàn kể cả khi case trước throw exception.
```

### Step 3 - Support Case Thread Map

Thêm helper:

```python
def load_case_thread_map(path: str | None) -> dict[str, str]:
    ...
```

Validate:

- file phải là JSON object;
- key là case id;
- value parse được UUID;
- mọi voice case trong mode `case_thread_new_room` phải có thread id;
- không cần map cho text case.

Khi chạy mixed mode `all`:

- text case có thể tiếp tục dùng `--thread-id`;
- voice case dùng case map nếu strategy yêu cầu.

### Step 4 - Report Isolation Metadata

Mỗi result nên có:

```json
{
  "eval_thread_id": "...",
  "eval_room_name": "...",
  "isolation_strategy": "case_thread_new_room",
  "case_isolation_quality": "thread_and_room"
}
```

Markdown report cũng phải hiển thị block này ở phần đầu, không chỉ lưu trong JSON:

```markdown
## Voice Isolation

- Enabled: `True`
- Strategy: `case_thread_new_room`
- Isolation Quality: `thread_and_room`
```

File cần update khi implement:

```text
app/services/agent_observability/model_eval_report.py
```

Trong `write_eval_reports`, nếu report có key `voice_isolation`, insert section `## Voice Isolation` ngay sau phần summary đầu báo cáo và trước `## Model Config`.

Nếu không có `voice_isolation`, không render section này để giữ backward compatibility với report cũ.

Mapping:

| Strategy | `case_isolation_quality` |
| --- | --- |
| shared thread, same room | `none` |
| shared thread, new room | `room_only` |
| case thread, new room | `thread_and_room` |

Snapshot/report top-level nên có:

```json
{
  "voice_isolation": {
    "enabled": true,
    "strategy": "case_thread_new_room",
    "quality": "thread_and_room"
  }
}
```

Nếu dùng `room_only`, report phải nói rõ:

```text
Voice cases are isolated by LiveKit room only. DB thread history may still affect ambiguous follow-up behavior.
```

### Step 5 - Add Failure Code `VOICE_TOOL_BYPASS`

File:

```text
app/services/agent_observability/model_eval_report.py
```

Định nghĩa:

```text
VOICE_TOOL_BYPASS = voice case hỏi kiến thức sách, agent trả lời nội dung nhưng trace không ghi tool call/source hợp lệ.
```

Điều kiện đề xuất:

```python
is_voice = case.get("input_mode") == "voice"
expected_source = case.get("expected_answer_source")
tool_names = trace.get("tool_names") or []
actual_source = trace.get("answer_source")
has_content_response = checks.get("must_include") is not False

if (
    is_voice
    and expected_source in BOOK_SOURCES
    and trace is not None
    and has_content_response
    and not tool_names
    and actual_source in (None, "unknown")
):
    failures.append("VOICE_TOOL_BYPASS")
```

Không classify bypass khi:

- case là casual chat;
- case expected source là `policy`;
- case expected source là `web`;
- trace missing hoàn toàn, vì đó là `TRACE_COVERAGE`;
- user transcript sai ý nghĩa, vì đó là `INPUT_STT`.

Lý do:

```text
Nếu agent trả lời đúng bằng may mắn/model memory nhưng không gọi tool, production vẫn rủi ro.
```

Với sách học tập, câu hỏi sách phải grounded bằng metadata/section/RAG, không dựa vào trí nhớ model.

### Step 6 - Add Optional Failure Code `VOICE_STATEFUL_AMBIGUITY`

Case:

```text
User voice: “Tóm tắt chương.”
```

Nếu chạy cùng thread/room sau case chương 4, agent có thể hiểu là follow-up chương 4. Trong real conversation, điều này không sai hoàn toàn.

Nhưng trong isolated eval, case này dùng để kiểm tra ambiguity handling. Vì vậy report nên phân biệt:

```text
Same-thread fail: possibly stateful ambiguity.
Thread-isolated fail: real clarification failure.
```

Đề xuất:

- chưa cần hard-fail mới nếu muốn giữ scope nhỏ;
- nhưng nên thêm warning metadata:

```json
{
  "ambiguity_state_note": "shared_thread_may_make_ambiguous_case_stateful"
}
```

Nếu muốn thêm failure code:

```text
VOICE_STATEFUL_AMBIGUITY
```

Chỉ dùng khi:

- input mode voice;
- case có `expected_intent=clarification`;
- isolation quality không phải `thread_and_room`;
- agent dùng source/section từ turn trước.

### Step 7 - Fix Bitcoin Audio Fixture Properly

Không nên sửa expected transcript thành:

```json
["hôm nay"]
```

Vì như vậy case không còn test web/current-info behavior nữa.

Đúng hơn:

1. Nghe lại fixture.
2. Nếu audio không rõ chữ “Bitcoin”, re-record fixture.
3. Giữ expected transcript theo ý định:

```json
"transcript_must_include_any": ["bitcoin", "bít coin", "bit coin"]
```

4. Nếu STT vẫn nhận sai, report phải classify `INPUT_STT`, không được chấm agent sai.

Fixture metadata nên có:

```json
{
  "id": "mice-current-bitcoin-vi-voice",
  "audio_fixture": "tests/fixtures/...",
  "transcript_must_include_any": ["bitcoin", "bít coin", "bit coin"],
  "expected_answer_source": "policy",
  "web_search_allowed": false
}
```

Rule:

```text
Không làm yếu fixture để pass. Chỉ sửa fixture khi input thật sự không thể hiện rõ intent.
```

### Step 8 - Add Unit Tests

Files:

```text
tests/services/agent_observability/test_model_eval_report.py
tests/services/agent_observability/test_phase10_eval_runner.py
```

Test cần thêm:

1. `VOICE_TOOL_BYPASS` được classify khi:
   - voice case;
   - expected source là book;
   - response content pass;
   - trace có `tool_names=[]`;
   - `answer_source=unknown`.

2. Không classify `VOICE_TOOL_BYPASS` khi:
   - text case;
   - web/policy case;
   - trace missing;
   - voice transcript meaning fail.

3. `load_case_thread_map` validate UUID.

4. `case_thread_new_room` thiếu map thì fail sớm.

5. Result metadata có:
   - `eval_thread_id`;
   - `eval_room_name`;
   - `isolation_strategy`;
   - `case_isolation_quality`.

6. Markdown report render `## Voice Isolation` khi report có voice isolation metadata.

7. `.local.json` case-thread map không bị commit nhầm.

---

## 6. Manual Test Commands

### 6.1 Shared Thread, New Room Per Voice Case

Đây là bước đầu dễ chạy nhất:

```powershell
$env:TRIAM_ACCESS_TOKEN = (uv run python scripts/get_supabase_access_token.py)

uv run python scripts/manual_integration/phase10_agent_eval.py `
  --mode voice `
  --candidate-name baseline `
  --base-url "http://127.0.0.1:8000/api/v1" `
  --book-id "<book_id>" `
  --thread-id "<thread_id>" `
  --database-label dev `
  --book-section-knowledge-count 53 `
  --isolate-voice-cases `
  --voice-isolation-strategy shared_thread_new_room `
  --include-text-preview `
  --output-dir "_docs_implemented/eval_reports/phase10_9"

Remove-Item Env:\TRIAM_ACCESS_TOKEN
```

Expected:

- mỗi case có `eval_room_name` khác nhau;
- `case_isolation_quality=room_only`;
- ambiguous case vẫn có thể bị state ảnh hưởng nếu cùng thread.

### 6.2 Case Thread, New Room Per Voice Case

Chuẩn hơn cho benchmark:

```powershell
$env:TRIAM_ACCESS_TOKEN = (uv run python scripts/get_supabase_access_token.py)

uv run python scripts/manual_integration/phase10_agent_eval.py `
  --mode voice `
  --candidate-name baseline `
  --base-url "http://127.0.0.1:8000/api/v1" `
  --book-id "<book_id>" `
  --thread-id "<fallback_thread_id>" `
  --database-label dev `
  --book-section-knowledge-count 53 `
  --isolate-voice-cases `
  --voice-isolation-strategy case_thread_new_room `
  --case-thread-map "tests/fixtures/agent_eval/voice_case_threads.local.json" `
  --include-text-preview `
  --output-dir "_docs_implemented/eval_reports/phase10_9"

Remove-Item Env:\TRIAM_ACCESS_TOKEN
```

Expected:

- mỗi case có `eval_room_name` khác nhau;
- mỗi voice case có `eval_thread_id` riêng;
- `case_isolation_quality=thread_and_room`;
- ambiguous case phải hỏi rõ nếu không có đủ thông tin.

File `voice_case_threads.local.json` nên ignored hoặc không commit nếu chứa dữ liệu môi trường riêng.

---

## 7. Acceptance Criteria

Phase 10.9 được xem là đạt khi:

1. Offline tests pass:

```powershell
uv run ruff check scripts\manual_integration app\services\agent_observability tests\services\agent_observability
uv run python -m py_compile scripts\manual_integration\phase10_agent_eval.py app\services\agent_observability\model_eval_report.py
uv run pytest tests\services\agent_observability -q
```

2. Manual voice eval report có isolation metadata.

3. Với `--isolate-voice-cases`, mỗi voice case dùng room mới.

4. Với `case_thread_new_room`, mỗi voice case dùng thread riêng từ map.

5. Failure code mới xuất hiện đúng lúc:

```text
VOICE_TOOL_BYPASS
```

6. Không có token/access key trong report/log committed.

7. Bitcoin voice case không bị làm yếu expected intent. Nếu STT vẫn sai, report classify là `INPUT_STT`.

8. Report cho biết rõ chất lượng isolation:

```text
room_only
thread_and_room
```

9. Không có thay đổi FE contract.

---

## 8. Trade-offs

| Decision | Benefit | Trade-off |
| --- | --- | --- |
| New room per voice case | Giảm event bleed, dễ debug | Chạy chậm hơn, tốn LiveKit session hơn |
| Case thread map | Deterministic hơn | Cần chuẩn bị dữ liệu test |
| Không tự động xóa thread test | Dễ audit DB sau test | DB có rác test |
| Không sửa prompt ngay | Tránh tối ưu sai tầng | Chưa cải thiện trải nghiệm user ngay |
| Giữ Bitcoin expected intent | Đo đúng web/current-info behavior | Có thể cần re-record audio |

---

## 9. Recommended Implementation Order

1. Thêm failure code `VOICE_TOOL_BYPASS` và unit test trước.
2. Refactor runner connection lifecycle thành helper nhỏ.
3. Thêm `--isolate-voice-cases`.
4. Thêm report metadata cho room/thread/isolation quality.
5. Thêm `--case-thread-map` và `case_thread_new_room`.
6. Rà lại voice manifest, đặc biệt Bitcoin fixture.
7. Thêm template `voice_case_threads.example.json` và gitignore cho `*.local.json`.
8. Update Markdown report để hiện `## Voice Isolation`.
9. Chạy offline tests.
10. Chạy real voice eval shared-thread room isolation.
11. Chuẩn bị case-thread map và chạy real voice eval thread-and-room isolation.
12. Sau khi report sạch, mới quyết định phase tiếp theo có cần sửa prompt/tool policy hay model không.

---

## 10. What To Do After Phase 10.9

Nếu Phase 10.9 xác nhận có `VOICE_TOOL_BYPASS`, phase tiếp theo nên là:

```text
Phase 10.10 - Realtime Voice Tool-First Grounding Policy
```

Mục tiêu:

- ép voice agent dùng tool cho câu hỏi sách;
- giảm trả lời bằng model memory;
- giữ natural conversation cho casual chat;
- không phá text chat path.

Nếu Phase 10.9 cho thấy fail chủ yếu do STT/audio:

```text
Phase 10.10 - Voice Input Quality And STT Robustness
```

Mục tiêu:

- chuẩn hóa audio fixtures;
- cải thiện phrase hints/prompt STT nếu SDK hỗ trợ;
- đánh giá headset/laptop mic/noise;
- thêm transcript repair hoặc clarification khi STT mất entity quan trọng.

Nếu Phase 10.9 cho thấy fail chủ yếu do shared thread state:

```text
Phase 10.10 - Conversation State Policy For Voice Follow-up
```

Mục tiêu:

- định nghĩa khi nào ambiguous follow-up được dùng context cũ;
- khi nào phải hỏi rõ;
- tránh user hỏi “chương nào?” mà agent đoán sai.
