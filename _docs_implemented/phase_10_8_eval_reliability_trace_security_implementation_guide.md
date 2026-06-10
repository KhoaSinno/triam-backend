# Phase 10.8 Implementation Guide - Evaluation Reliability, Trace Coverage And Secure Test Hygiene

Date: 2026-06-06  
Status: Implemented and offline-tested  
Depends on: Phase 10.0 -> 10.7  
Primary scope: agent evaluation reliability, trace coverage, secure manual test workflow, voice/text failure classification

---

## 0. Implementation Status

Implemented files:

- `app/core/config.py`
  - enabled canonical section RAG by default;
  - enabled hybrid RAG by default.
- `.env.example`
  - documented Phase 10.8 canonical/hybrid RAG defaults.
- `.env` local
  - updated canonical/hybrid RAG flags to `true` for local eval. This file is ignored by git.
- `tests/fixtures/agent_eval/book_grounding_cases.json`
  - changed Chapter 5 fixture from a single Vietnamese wording requirement to fact-oriented terms.
- `app/services/agent_observability/model_eval_report.py`
  - added RAG runtime flags to safe report config;
  - added `TRACE_COVERAGE`, `NO_USER_TRANSCRIPT`, `INPUT_TIMEOUT`, `EVAL_FIXTURE_MISMATCH` classification support;
  - separated timeout/fixture/trace failures from product routing failures.
- `scripts/manual_integration/phase10_agent_eval.py`
  - warns when `--access-token` is passed directly;
  - prefers `TRIAM_ACCESS_TOKEN`;
  - validates WAV fixture metadata;
  - records safe audio metadata in voice case results;
  - filters trace by input mode, thread and room;
  - merges late transcript trace events;
  - writes reports to `_docs_implemented/eval_reports/phase10_8` by default.
- `tests/services/agent_observability/test_model_eval_report.py`
  - covers new failure-code behavior and RAG runtime config snapshot.
- `tests/services/agent_observability/test_phase10_eval_runner.py`
  - covers safe token CLI detection, trace selection, late transcript merge and WAV metadata validation.
- `tests/services/agent_observability/test_eval_fixtures.py`
  - verifies the Chapter 5 fixture now checks facts, not one translation.

Verification completed:

```powershell
uv run ruff check app\core\config.py app\services\agent_observability scripts\manual_integration tests\services\agent_observability tests\services\test_rag_service.py
uv run python -m py_compile app\core\config.py app\services\agent_observability\model_eval_report.py app\services\agent_observability\turn_trace.py scripts\manual_integration\phase10_agent_eval.py
uv run pytest tests\services\agent_observability -q
uv run pytest tests\services\test_rag_service.py tests\services\voice_agent\test_rag_context.py -q
uv run pytest tests\services\voice_agent tests\services\agent_policy tests\services\agent_observability -q
uv run pytest tests -q --maxfail=1 --durations=20
```

Results:

```text
Ruff passed.
Py compile passed.
28 agent_observability tests passed.
11 RAG/RAG-context tests passed.
81 voice_agent/agent_policy/agent_observability tests passed.
237 full test-suite tests passed.
```

Not run automatically:

- real LiveKit/provider eval;
- production Hugging Face eval.

Reason:

```text
These require running server, realtime worker, access token, LiveKit Cloud and paid/provider calls.
```

## 1. Why Phase 10.8 Exists

Phase 10.7 đã chạy được real evaluation cho agent chat và voice. Kết quả rất có giá trị, nhưng chưa nên dùng ngay để kết luận model nào tốt hay xấu.

Lý do:

- một số case fail vì trace thiếu dữ liệu, không chắc agent trả lời sai;
- voice test có case timeout không bắt được transcript user;
- RAG semantic trả lời đúng nội dung nhưng thiếu `section_id` trong trace;
- canonical/hybrid RAG hiện có thể đang bị tắt qua config/env, làm semantic RAG rơi về đường RPC cũ không đủ section metadata;
- report snapshot chưa ghi được `book_section_knowledge_count`;
- manual log có nguy cơ làm lộ access token nếu chạy command không đúng cách.

Phase 10.8 sinh ra để làm một việc nền tảng:

```text
Đo cho đúng trước khi tối ưu model, prompt, RAG hoặc latency.
```

Nếu không làm phase này, các phase sau có thể tối ưu sai chỗ.

---

## 2. Evidence From Phase 10.7

Report đọc từ:

```text
_docs_implemented/eval_reports/phase10_7/phase10_7_eval_20260606_151058_baseline.md
_docs_implemented/eval_reports/phase10_7/phase10_7_eval_20260606_151058_baseline.json
```

Kết quả baseline:

| Metric | Value |
| --- | ---: |
| Total cases | 15 |
| Passed | 8 |
| Failed | 7 |
| Content accuracy | 85.7% |
| Intent accuracy | 78.6% |
| Answer source accuracy | 85.7% |
| Section resolution accuracy | 57.1% |
| Web policy safety rate | 100.0% |
| Voice meaning preservation rate | 75.0% |

Nhận định quan trọng:

- web-search guardrail đang tốt, không được phá;
- transcript payload contract sau Phase 10.6 đang ổn;
- section routing metric đang thấp, nhưng có case thấp do thiếu trace metadata;
- voice eval chưa ổn định đủ để dùng làm model benchmark cuối cùng;
- latency cao, nhưng chưa nên tối ưu latency trước khi trace và failure code đáng tin.

---

## 3. Goals

Phase này cần đạt được:

1. Manual eval không làm lộ access token trong command/log.
2. Failure code phân biệt được:
   - lỗi agent thật;
   - lỗi trace thiếu dữ liệu;
   - lỗi evaluator timeout;
   - lỗi STT/input;
   - lỗi RAG không có coverage;
   - lỗi expected fixture chưa đúng.
3. Trace phải ghi đủ dữ liệu cho các route chính:
   - metadata;
   - explicit section;
   - semantic RAG;
   - web permission;
   - clarification;
   - voice late transcript.
4. RAG trace phải có `retrieval_section_ids` khi dữ liệu có section.
5. Report snapshot phải có đủ thông tin về canonical index.
6. Official eval phải chạy với canonical section RAG và hybrid RAG đã bật, nếu index readiness đạt.
7. Rerun baseline sau khi sửa để có số liệu sạch hơn.

---

## 4. Non-Goals

Phase này không làm:

- không đổi model mặc định;
- không đổi prompt chính;
- không đổi API contract cho FE;
- không đổi `lk.chat`, `lk.transcript`, `lk.control`;
- không rewrite RAG ranking;
- không tối ưu latency sâu;
- không thêm provider mới;
- không sửa câu trả lời cho riêng sách `Of Mice and Men`.

Đây chủ yếu là phase instrumentation và evaluation hardening. Ngoại lệ được phép là bật đường canonical/hybrid RAG cho official eval nếu dữ liệu index đã sẵn sàng, vì đây là điều kiện để Phase 10.2/10.3 thật sự được đo đúng.

---

## 5. Current Problems To Fix

### 5.1 Access Token Leakage In Manual Logs

Vấn đề:

Manual test có thể bị chạy theo dạng:

```powershell
uv run python scripts/manual_integration/phase10_agent_eval.py --access-token "<token>"
```

Nếu terminal output được lưu vào file, token có thể bị lưu trong docs/log.

Rule mới:

```text
Không truyền access token trực tiếp qua command có thể được lưu log.
Không commit log chứa token.
Runner/document phải hướng dẫn dùng env var hoặc file local ignored.
```

Recommended local flow:

```powershell
$env:TRIAM_ACCESS_TOKEN = (uv run python scripts/get_supabase_access_token.py)
uv run python scripts/manual_integration/phase10_agent_eval.py --mode all --candidate baseline
Remove-Item Env:\TRIAM_ACCESS_TOKEN
```

Nếu script lấy token đang in thêm text ngoài token, cần dùng option output raw token hoặc copy token vào env thủ công, nhưng không ghi token vào report.

### 5.2 Section Metric False Negatives

Một số semantic RAG case có:

```text
content = pass
answer_source = pass
intent = pass
expected_section = fail
retrieval_section_ids = []
```

Điều này có thể là:

- RAG result không trả `section_id`;
- trace không đọc được `section_id`;
- evaluator đang lấy nhầm trace event;
- canonical index chưa được backfill đủ;
- case expectation quá chặt.

Không nên đánh tất cả thành `ROUTING_SECTION`.

Phase 10.8 cần thêm failure code:

```text
TRACE_COVERAGE
```

Ví dụ:

```text
Nếu content/source/intent đều pass nhưng section fail vì trace không có section id,
thì classify là TRACE_COVERAGE, không phải ROUTING_SECTION.
```

### 5.3 Missing Voice Trace Correlation

Một số voice case có answer đúng nhưng trace thiếu:

- `detected_intent`;
- `answer_source`;
- `resolved_section_ids`;
- `tool_names`.

Nếu evaluator chỉ đọc `turn_completed` cuối cùng theo `input_mode`, có thể bị lệch turn khi LiveKit emit transcript/assistant event không đồng bộ.

Phase này cần cải thiện:

- runner chọn trace bằng `trace_id`, timestamp window, thread/room và input mode;
- voice timeout phải có error code rõ;
- late transcript phải được merge vào đúng completed trace.

### 5.4 Unknown Timeout Failure

Hiện có case:

```text
Timeout waiting for transcript role=user
```

Nhưng failure code là `UNKNOWN`.

Điều này không tốt cho report. Cần đổi thành:

```text
INPUT_TIMEOUT
```

hoặc:

```text
NO_USER_TRANSCRIPT
```

Rule:

```text
Không để timeout voice rơi vào UNKNOWN.
```

### 5.5 Incomplete Snapshot

Report hiện có:

```text
book_section_knowledge_count = None
```

Điều này làm mình không biết:

- canonical section index đã build đủ chưa;
- RAG semantic có đang chạy trên bảng mới không;
- baseline và candidate có cùng index snapshot không.

Phase này cần:

- cho runner lấy `book_section_knowledge_count` tự động nếu có DB URL local/dev;
- hoặc thêm optional safe API/internal helper;
- hoặc bắt buộc truyền `--book-section-knowledge-count` khi chạy report.

Recommended trước mắt:

```text
Runner giữ optional argument, nhưng docs/test command phải yêu cầu truyền count khi benchmark chính thức.
```

### 5.6 Canonical And Hybrid RAG May Be Disabled

Current risk:

```text
AGENT_CANONICAL_SECTION_RAG_ENABLED=false
AGENT_HYBRID_RAG_ENABLED=false
```

Nếu hai flag này vẫn `false`, semantic RAG có thể tiếp tục chạy qua đường legacy RPC. Khi đó:

- answer có thể vẫn đúng;
- `retrieval_result_count` có thể có dữ liệu;
- nhưng `retrieval_section_ids` có thể rỗng;
- evaluator sẽ không xác minh được câu trả lời đến từ đúng section.

Required Phase 10.8 decision:

```text
Official Phase 10.8 baseline must run with canonical section RAG enabled.
Hybrid RAG should also be enabled when canonical index coverage is ready.
```

Implementation target after readiness check:

```python
AGENT_CANONICAL_SECTION_RAG_ENABLED: bool = True
AGENT_HYBRID_RAG_ENABLED: bool = True
```

Files to update or verify:

```text
app/core/config.py
.env.example
.env local
Hugging Face Space env vars
```

Important:

```text
.env overrides config.py defaults.
Changing config.py alone is not enough if local/deploy env still sets false.
```

Readiness gate before enabling in production:

- `book_section_knowledge_count` is non-null and greater than zero for the evaluated book;
- canonical RAG unit tests pass;
- fallback behavior remains safe when a book has no canonical section index;
- official eval report records both flag values in the model/config snapshot.

Do not claim this guarantees 100% pass rate. It only ensures the evaluator is measuring the intended canonical RAG path.

### 5.7 Fixture Strictness Can Create False Failures

The Phase 10.7 text case `mice-chapter-five-summary-vi-text` failed while routing/source/section were correct:

```text
expected_intent = pass
expected_answer_source = pass
expected_section = pass
must_include = fail
```

Current fixture expects:

```json
"must_include": ["Lennie", "vợ"]
```

For an English book, a correct answer may use `"Curley's wife"` or `"wife"` instead of the Vietnamese word `"vợ"`.

Required update:

```json
"must_include": ["Lennie", "Curley"]
```

Alternative acceptable update:

```json
"must_include": ["Lennie", "wife"]
```

Recommended:

```text
Use ["Lennie", "Curley"] because it validates the involved character relationship without forcing Vietnamese wording.
```

Rule:

```text
Fixture updates are allowed only when the expected answer wording is stricter than the business fact being tested.
Do not loosen fixtures just to improve pass rate.
```

---

## 6. Proposed Implementation

### Step 1 - Secure Manual Test Workflow

Files:

```text
scripts/manual_integration/phase10_agent_eval.py
_docs_implemented/phase_10_7_model_evaluation_production_rollout_implementation_guide.md
```

Implementation:

- keep `--access-token` for backward compatibility;
- prefer `TRIAM_ACCESS_TOKEN`;
- add startup warning if `--access-token` is used;
- never print token;
- add `.gitignore` patterns for local eval raw logs if missing.

Suggested warning:

```python
if args.access_token and "--access-token" in sys.argv:
    print("WARNING: --access-token can leak into shell history/logs. Prefer TRIAM_ACCESS_TOKEN.")
```

Do not print the token value.

### Step 2 - Add Evaluation Failure Codes

Files:

```text
app/services/agent_observability/model_eval_report.py
tests/services/agent_observability/test_eval_metrics.py
tests/services/agent_observability/test_model_eval_report.py
```

Add codes:

```text
TRACE_COVERAGE
INPUT_TIMEOUT
NO_USER_TRANSCRIPT
EVAL_FIXTURE_MISMATCH
```

Classification rules:

| Situation | Failure code |
| --- | --- |
| voice user transcript timeout | `NO_USER_TRANSCRIPT` |
| trace missing but transcript/answer exists | `TRACE_COVERAGE` |
| content/source/intent pass but expected section fails due empty trace section ids | `TRACE_COVERAGE` |
| expected facts fail while trace route/source/section are correct | `EVAL_FIXTURE_MISMATCH` or `CONTENT_ACCURACY` depending evidence |
| source becomes web/policy for book question | `CONTEXT_VALIDATION` |
| unauthorized web search | `WEB_PERMISSION` |

Important:

```text
Không được làm metric đẹp giả.
Chỉ chuyển sang TRACE_COVERAGE khi answer behavior thực sự pass các check chính.
```

Unit tests required:

- `TRACE_COVERAGE` when content/source/intent pass but section IDs are missing from trace;
- `NO_USER_TRANSCRIPT` when voice runner times out waiting for user transcript;
- `INPUT_TIMEOUT` when a case-level timeout occurs before answer evaluation;
- `EVAL_FIXTURE_MISMATCH` or equivalent content-fixture classification when route/source/section are correct but required wording is too strict;
- `WEB_PERMISSION` still has zero tolerance.

### Step 3 - Improve Trace Selection In Runner

Files:

```text
scripts/manual_integration/phase10_agent_eval.py
tests/services/agent_observability/test_phase10_eval_runner.py
```

Current pattern:

```text
read trace events from log offset
select last turn_completed for input_mode
merge late_transcript if trace_id matches
```

Problems:

- last event may not be the case's event;
- voice can emit late transcript after assistant;
- multiple cases close together can pollute selection.

Recommended improvement:

1. Capture `case_started_at`.
2. Read events after log offset.
3. Filter by:
   - `input_mode`;
   - `thread_id` when available;
   - `room_name` when available;
   - event timestamp after case start if available.
4. Prefer completed trace where:
   - assistant char count > 0;
   - tool/source matches transcript behavior;
   - latest event before next case.
5. If no strong match, return trace with:
   - `trace_selection_quality = weak`;
   - add `TRACE_COVERAGE`.

This keeps evaluation honest.

### Step 4 - Enable Canonical And Hybrid RAG For Official Eval

Files:

```text
app/core/config.py
.env.example
.env local
Hugging Face Space env vars
tests/services/test_rag_service.py
```

Implementation:

- update code defaults only if fallback tests prove old books without section index remain safe;
- update `.env.example` to document the intended Phase 10.8 defaults;
- update local `.env` manually before official eval, because it overrides `config.py`;
- ensure deploy env values are explicitly set before production benchmark.

Recommended target:

```python
AGENT_CANONICAL_SECTION_RAG_ENABLED: bool = True
AGENT_HYBRID_RAG_ENABLED: bool = True
```

Official eval requirement:

```text
The Phase 10.8 baseline report must include the actual runtime values of both flags.
If either flag is false, the report is a legacy-RAG baseline, not the canonical Phase 10.8 baseline.
```

Rollback:

```text
Set AGENT_CANONICAL_SECTION_RAG_ENABLED=false and AGENT_HYBRID_RAG_ENABLED=false in env if canonical index causes production regression.
```

### Step 5 - Record Section IDs For Semantic RAG

Files to inspect and update:

```text
app/services/rag_service.py
app/services/voice_agent/rag_context.py
app/services/agent_observability/turn_trace.py
tests/services/voice_agent/test_rag_context.py
tests/services/test_rag_service.py
```

Required behavior:

```text
Every canonical RAG result should expose section_id when source data has it.
AgentTurnTracer.record_retrieval() must capture those section IDs.
Report should show retrieval_section_ids.
```

Expected trace shape:

```json
{
  "retrieval_method": "hybrid",
  "retrieval_result_count": 10,
  "retrieval_section_ids": ["..."],
  "retrieval_scores": [0.82, 0.79],
  "answer_source": "book_rag"
}
```

Do not log raw chunk content.

### Step 6 - Improve Snapshot Metadata

Files:

```text
app/services/agent_observability/model_eval_report.py
scripts/manual_integration/phase10_agent_eval.py
```

Preferred implementation:

- keep `build_snapshot_metadata()` pure;
- runner collects counts;
- report writes counts.

Options:

1. Pass manually:

```powershell
--book-section-knowledge-count 123
```

2. Add a local-only DB helper in runner:

```text
If DATABASE_URL exists and --allow-db-snapshot-query is set, query count from DB.
```

Recommended for this project:

```text
Use explicit CLI flag first.
Avoid auto-querying DB in manual runner unless explicitly enabled.
```

Reason:

- safer for production;
- avoids accidental DB load;
- keeps report reproducible.

### Step 7 - Fix Over-Strict Text Fixture

Files:

```text
tests/fixtures/agent_eval/book_grounding_cases.json
tests/services/agent_observability/test_eval_fixtures.py
```

Implementation:

- update `mice-chapter-five-summary-vi-text`;
- replace the language-specific required term `"vợ"` with a fact-oriented term;
- recommended `must_include`: `["Lennie", "Curley"]`;
- keep the case strict enough to verify the answer is about Chapter 5.

Why:

```text
The book is English. A correct answer may say "Curley's wife" instead of "vợ".
The fixture should validate the fact, not force one Vietnamese wording.
```

Guardrail:

```text
Do not loosen fixtures unless the previous expected phrase is narrower than the actual business fact.
```

### Step 8 - Add Audio Fixture Validation

Files:

```text
scripts/manual_integration/phase10_agent_eval.py
tests/fixtures/agent_eval/voice_manifest.json
```

Before publishing WAV:

- validate file exists;
- validate 16-bit PCM;
- validate duration;
- validate sample rate;
- optionally warn if duration is too short or too long.

Suggested metadata in report per voice case:

```json
{
  "audio": {
    "path": "tests/fixtures/...",
    "duration_ms": 2300,
    "sample_rate": 16000,
    "channels": 1
  }
}
```

Do not store raw audio bytes.

### Step 9 - Rerun Baseline And Write Phase 10.8 Report

Output folder:

```text
_docs_implemented/eval_reports/phase10_8
```

Expected report names:

```text
phase10_8_eval_<timestamp>_baseline.json
phase10_8_eval_<timestamp>_baseline.md
phase10_8_eval_notes.md
```

The notes file should answer:

- which previous failures were real;
- which previous failures were trace/evaluator gaps;
- which cases still need product fixes;
- whether model evaluation is now safe to run.

---

## 7. Test Plan

### Offline Tests

Run:

```powershell
uv run pytest tests/services/agent_observability -q
uv run pytest tests/services/voice_agent tests/services/agent_policy tests/services/agent_observability -q
uv run pytest tests/services/test_rag_service.py tests/services/agent_observability/test_eval_fixtures.py -q
uv run ruff check app/core/config.py app/services/agent_observability app/services/voice_agent app/services/rag_service.py scripts/manual_integration tests/services/agent_observability tests/services/voice_agent tests/services/agent_policy tests/services/test_rag_service.py
uv run python -m py_compile app/core/config.py app/services/agent_observability/model_eval_report.py app/services/agent_observability/turn_trace.py scripts/manual_integration/phase10_agent_eval.py
```

### Manual Local Eval

Required local processes:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uv run python -m app.services.agent_voice_gpt_realtime start
```

If Celery is not needed for agent eval, do not start it.

Safe token flow:

```powershell
$env:TRIAM_ACCESS_TOKEN = "<token-from-local-login-script>"
uv run python scripts/manual_integration/phase10_agent_eval.py `
  --mode all `
  --candidate baseline `
  --base-url http://127.0.0.1:8000/api/v1 `
  --trace-log logs/app_YYYY-MM-DD.log `
  --book-section-knowledge-count <count>
Remove-Item Env:\TRIAM_ACCESS_TOKEN
```

Do not paste token into a markdown/log file.

### Acceptance Criteria

Phase 10.8 passes when:

- no eval log contains access token;
- canonical and hybrid RAG runtime flags are recorded in report;
- official canonical baseline has both RAG flags enabled or explicitly explains why not;
- over-strict Chapter 5 fixture is updated to validate facts, not one Vietnamese wording;
- new failure codes are covered by unit tests;
- `UNKNOWN` failure count is zero or explained;
- voice transcript timeout is classified clearly;
- semantic RAG trace includes section IDs when canonical data has them;
- report snapshot has non-null `book_section_knowledge_count` for official benchmark;
- failed cases separate product failures from trace/evaluator failures;
- baseline can be rerun with comparable results.

---

## 8. Expected Outcome

After Phase 10.8, we should know:

- which failures are real agent failures;
- which failures are caused by STT/audio;
- which failures are caused by missing RAG section trace;
- which failures are evaluator fixture issues;
- whether Phase 10.9 model A/B testing is valid.

This phase may not increase accuracy immediately. Its value is making the measurement trustworthy.

---

## 9. Trade-Offs

| Choice | Benefit | Trade-off |
| --- | --- | --- |
| Add `TRACE_COVERAGE` | Avoid blaming agent for missing trace | Metrics become less simple |
| Keep real eval manual | Avoid token/cost surprises in pytest | Requires disciplined runbook |
| Require snapshot count | Better A/B validity | One more command/parameter |
| Improve trace selection | More reliable voice eval | More runner complexity |
| Do not change model yet | Avoid false optimization | User-visible accuracy may not improve this phase |

---

## 10. Phase 10.9 Gate

Only start Phase 10.9 model comparison when Phase 10.8 report shows:

```text
web_permission_violations = 0
UNKNOWN failures are explained or removed
TRACE_COVERAGE is below an acceptable threshold
voice timeout behavior is stable
snapshot metadata is complete
```

If these gates fail, fix evaluator/trace first.

---

## 11. Senior Notes For Implementation

- Do not make the evaluator forgiving just to improve pass rate.
- Do not hide real product failures under `TRACE_COVERAGE`.
- Do not add book-specific logic for `Of Mice and Men`.
- Do not log raw transcript, full answer, token, headers, embeddings or raw chunks.
- Keep behavior changes out of this phase unless required to emit safe trace metadata.
- Every new failure code needs a unit test.
- Every trace field used by evaluation needs at least one unit test.
- The report must help us decide the next engineering action, not merely show a score.
