# Phase 10.7 Implementation Guide - Model Evaluation And Production Rollout

Date: 2026-06-06  
Status: Proposed implementation guide  
Depends on: Phase 10.0 -> 10.6  
Primary scope: model selection, chat/voice evaluation, canary rollout, rollback safety

---

## 1. Why Phase 10.7 Exists

Từ Phase 10.0 đến Phase 10.6, hệ thống đã xử lý các nguyên nhân lớn gây trả lời sai:

- có baseline trace để biết lỗi nằm ở đâu;
- metadata và câu hỏi theo chương/mục được route deterministic;
- RAG chuyển sang canonical `BookSection`;
- retrieval có hybrid/rerank/evidence validation;
- voice có guard chống STT/tool-call lệch;
- chat và voice dùng chung policy;
- transcript timeline có stable ID để FE không duplicate bubble.

Sau các phase này, nếu câu trả lời vẫn chưa đạt, lúc đó mới nên đánh giá model.

Nguyên tắc của Phase 10.7:

```text
Không nâng model bằng cảm giác.
Không dùng model mạnh hơn để che lỗi retrieval, STT hoặc routing.
Chỉ đổi model khi evaluation chứng minh tốt hơn theo metric đã chốt.
```

---

## 2. Goal

Xây một quy trình production-safe để chọn model cho Triam:

- typed chat generation;
- realtime voice model;
- voice transcription model;
- web permission classifier;
- optional: text answer synthesis model nếu sau này tách khỏi realtime model.

Kết quả mong muốn:

- biết model nào trả lời đúng hơn với sách thật;
- biết model nào ít hallucination hơn;
- biết model nào gọi tool đúng hơn;
- biết latency và cost tăng/giảm bao nhiêu;
- có rollout bằng env/config, không hard-code;
- có rollback nhanh nếu production xấu.

---

## 3. Non-Goals

Phase này không làm:

- không viết lại RAG pipeline;
- không đổi schema DB;
- không đổi `lk.chat`, `lk.transcript`, `lk.control`;
- không thêm provider mới nếu chưa có key và chưa có bài toán rõ;
- không đổi model mặc định trên production trước khi có report;
- không test thủ công một hai câu rồi kết luận.

---

## 4. Current Model Surfaces

Các vị trí model hiện tại trong code:

| Surface | Current config | File |
| --- | --- | --- |
| Voice realtime | `OPENAI_STREAM_MODEL_NAME` | `app/core/config.py`, `app/services/agent_voice_gpt_realtime.py` |
| Voice output voice | `OPENAI_REALTIME_VOICE` | `app/core/config.py`, `agent_voice_gpt_realtime.py` |
| Voice transcription | `OPENAI_REALTIME_TRANSCRIPTION_MODEL` | `app/core/config.py`, `agent_voice_gpt_realtime.py` |
| Voice transcription hint | `OPENAI_REALTIME_TRANSCRIPTION_PROMPT` | `app/core/config.py`, `agent_voice_gpt_realtime.py` |
| Typed chat LLM | `VOICE_AGENT_TEXT_LLM_MODEL` | `app/core/config.py`, `agent_voice_gpt_realtime.py` |
| Web permission classifier | `VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL` | `app/core/config.py`, `app/services/voice_agent/web_permission_intent_classifier.py` |
| TTS rewrite / normalize | `GEMINI_MODEL_LLM` | `app/core/config.py`, `app/services/llm_service.py` |
| Pareto planner | `PARETO_PLANNER_MODEL` | `app/core/config.py`, `app/services/pareto_planner_service.py` |

Phase 10.7 chỉ tập trung vào agent chat/voice surfaces. TTS/Pareto model tuning nên để phase riêng nếu cần.

---

## 5. Evaluation Philosophy

Model tốt cho Triam không chỉ là model trả lời nghe hay.

Model tốt phải:

- chọn đúng nguồn: metadata, section, RAG, web permission, clarification;
- không bịa khi sách không có dữ liệu;
- không tự search web nếu chưa được phép;
- giữ câu trả lời ngắn, rõ, đúng sách;
- không làm voice bị delay quá lâu;
- không làm cost vượt khả năng deploy/free tier;
- không làm tool calling bất ổn.

Vì vậy chấm model theo 5 nhóm:

```text
Accuracy
Groundedness
Tool behavior
Latency
Cost
```

---

## 6. Candidate Matrix

Không hard-code model trong code. Candidate được khai báo bằng file hoặc CLI argument cho runner.

Đề xuất tạo file:

```text
tests/fixtures/agent_eval/model_candidate_matrix.json
```

Example:

```json
[
  {
    "name": "baseline",
    "description": "Current production defaults",
    "env": {
      "VOICE_AGENT_TEXT_LLM_MODEL": "gpt-4o-mini",
      "OPENAI_STREAM_MODEL_NAME": "gpt-realtime",
      "OPENAI_REALTIME_TRANSCRIPTION_MODEL": "gpt-4o-transcribe",
      "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL": "gpt-4o-mini"
    }
  },
  {
    "name": "candidate_text_stronger",
    "description": "Stronger typed chat answer model only",
    "env": {
      "VOICE_AGENT_TEXT_LLM_MODEL": "<candidate-model>",
      "OPENAI_STREAM_MODEL_NAME": "gpt-realtime",
      "OPENAI_REALTIME_TRANSCRIPTION_MODEL": "gpt-4o-transcribe",
      "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL": "gpt-4o-mini"
    }
  },
  {
    "name": "candidate_voice_realtime",
    "description": "Realtime voice model candidate only",
    "env": {
      "VOICE_AGENT_TEXT_LLM_MODEL": "gpt-4o-mini",
      "OPENAI_STREAM_MODEL_NAME": "<candidate-realtime-model>",
      "OPENAI_REALTIME_TRANSCRIPTION_MODEL": "gpt-4o-transcribe",
      "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL": "gpt-4o-mini"
    }
  }
]
```

Rule:

- Mỗi candidate chỉ đổi một surface trước.
- Không đổi cùng lúc text model, realtime model, transcription model và classifier.
- Trước khi đưa model name vào matrix, phải verify model tồn tại bằng provider API/docs chính thức hoặc script list model local.
- Nếu provider/model không ổn định, ghi rõ trong report, không đưa thẳng lên production.

---

## 7. Evaluation Dataset

Dataset hiện có:

```text
tests/fixtures/agent_eval/book_grounding_cases.json
tests/fixtures/agent_eval/voice_manifest.json
tests/fixtures/*.wav
```

Phase 10.7 nên mở rộng dataset theo nhóm lỗi thật đã gặp:

### 7.1 Metadata cases

Ví dụ:

- tác giả của sách;
- tên sách;
- sách có bao nhiêu chương/mục lớn;
- câu hỏi metadata không được đi vector RAG.

Expected:

```json
{
  "expected_answer_source": "book_metadata",
  "must_include": ["John Steinbeck"],
  "must_not_include": ["internet", "không có sẵn"]
}
```

### 7.2 Explicit section cases

Ví dụ:

- đại ý chương 4;
- tóm tắt mục 1.2;
- hỏi một mục có title trùng nhau.

Expected:

```json
{
  "expected_intent": "section_lookup",
  "expected_answer_source": "book_section",
  "expected_section_ref": "4"
}
```

### 7.3 Semantic RAG cases

Ví dụ:

- hỏi một khái niệm có trong sách nhưng không nêu chương;
- hỏi bằng tiếng Việt về sách tiếng Anh;
- hỏi bằng diễn đạt khác với heading.

Expected:

```json
{
  "expected_answer_source": "book_rag",
  "must_include": ["required fact"],
  "must_not_include": ["forbidden hallucination"]
}
```

### 7.4 Web permission cases

Ví dụ:

- câu hỏi cần thông tin ngoài sách;
- sách không có dữ liệu;
- user từ chối search;
- user đồng ý search bằng voice: `Yup`, `Yub làm đi`, `Sure`.

Expected:

```json
{
  "expected_answer_source": "policy",
  "web_permission_required": true,
  "web_must_not_run_without_permission": true
}
```

### 7.5 Voice/STT cases

Mỗi voice case nên có:

- `wav_path`;
- expected transcript meaning;
- expected intent;
- expected source;
- required facts;
- forbidden facts.

Không cần exact transcript match 100%. Chỉ cần semantic intent preserved.

---

## 8. Metrics

### 8.1 Accuracy Metrics

Required:

```text
intent_accuracy
source_accuracy
section_accuracy
must_include_pass_rate
must_not_include_pass_rate
```

Pass/fail:

- `intent_accuracy >= baseline`
- `source_accuracy >= baseline`
- `must_not_include_pass_rate` không được giảm
- metadata cases phải đạt 100%
- web permission violations phải bằng 0

### 8.2 Groundedness Metrics

Required:

```text
hallucination_rate
unsupported_answer_rate
wrong_section_rate
web_fallback_rate
```

Rule:

- Nếu model mới trả lời hay hơn nhưng tăng hallucination, reject.
- Nếu model mới hay search web hơn vì retrieval yếu, reject hoặc tách lỗi sang retrieval phase.

### 8.3 Tool Behavior Metrics

Required:

```text
tool_selection_accuracy
wrong_tool_call_count
missing_tool_call_count
web_without_permission_count
clarification_when_needed_rate
```

Hard gate:

```text
web_without_permission_count == 0
```

### 8.4 Latency Metrics

Required:

```text
chat_first_response_p50_ms
chat_first_response_p95_ms
voice_user_transcript_p50_ms
voice_assistant_transcript_p50_ms
voice_answer_complete_p95_ms
```

Recommendation for capstone production:

- chat p95 should not regress more than 30%;
- voice answer p95 should not regress more than 25%;
- if accuracy improves a lot, allow a documented latency trade-off.

### 8.5 Cost Metrics

Required:

```text
estimated_input_tokens
estimated_output_tokens
audio_seconds
provider_cost_estimate
cost_per_successful_answer
```

Rule:

- A model that is 5% more accurate but 5x costlier is not automatically better.
- For Hugging Face free deployment and student capstone, stability/cost wins unless quality gap is obvious.

---

## 9. Implementation Plan

### Step 1 - Extend manual eval runner

File:

```text
scripts/manual_integration/phase10_agent_eval.py
```

Add:

- `--candidate-name`;
- `--candidate-matrix`;
- `--output-dir`;
- model/env snapshot in report;
- transcript payload ID validation after Phase 10.6;
- latency timestamps for:
  - request sent;
  - first `lk.chat`;
  - user `lk.transcript`;
  - assistant `lk.transcript`;
  - trace completed.

Expected output:

```text
_docs_implemented/eval_reports/phase10_7/<timestamp>_<candidate>.json
_docs_implemented/eval_reports/phase10_7/<timestamp>_<candidate>.md
```

JSON report should include:

```json
{
  "candidate": "baseline",
  "started_at": "...",
  "base_url": "...",
  "book_id": "...",
  "thread_id": "...",
  "model_config": {
    "VOICE_AGENT_TEXT_LLM_MODEL": "...",
    "OPENAI_STREAM_MODEL_NAME": "...",
    "OPENAI_REALTIME_TRANSCRIPTION_MODEL": "...",
    "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL": "..."
  },
  "summary": {
    "total_cases": 12,
    "passed_cases": 11,
    "failed_cases": 1,
    "source_accuracy": 0.92,
    "web_permission_violations": 0
  },
  "latency": {
    "chat_first_response_p50_ms": 1200,
    "chat_first_response_p95_ms": 2400
  },
  "cases": []
}
```

### Step 2 - Add offline report comparator

Create:

```text
scripts/manual_integration/compare_phase10_model_reports.py
```

Responsibilities:

- load baseline report and candidate report;
- compare pass rate, source accuracy, hallucination signals, latency and cost;
- print go/no-go recommendation;
- fail with non-zero exit code if candidate violates hard gates.

Example command:

```powershell
uv run python scripts/manual_integration/compare_phase10_model_reports.py `
  --baseline _docs_implemented/eval_reports/phase10_7/20260606_baseline.json `
  --candidate _docs_implemented/eval_reports/phase10_7/20260606_candidate_text_stronger.json
```

### Step 3 - Add deterministic unit tests for metrics

File:

```text
tests/services/agent_observability/test_model_eval_report.py
```

Test:

- report summary calculates accuracy correctly;
- hard gate fails when web search runs without permission;
- comparator rejects candidate with worse metadata accuracy;
- comparator allows candidate with equal safety and better accuracy.

Keep this offline. Do not call provider APIs in pytest.

### Step 4 - Add rollout config contract

No DB migration.

Config already supports:

```text
VOICE_AGENT_TEXT_LLM_MODEL
OPENAI_STREAM_MODEL_NAME
OPENAI_REALTIME_TRANSCRIPTION_MODEL
VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL
```

Optional addition:

```python
AGENT_MODEL_PROFILE: str = "baseline"
```

Purpose:

- logs/reports know which profile is active;
- production canary can be identified from logs without exposing secrets.

Do not add dynamic per-request model switching yet unless product needs A/B per user.

### Step 5 - Add startup log snapshot

When voice agent starts, log safe model metadata:

```text
Agent model profile active | profile=baseline | text_model=... | realtime_model=... | transcription_model=... | classifier_model=...
```

Do not log API keys.

### Step 6 - Production smoke test script

Create or extend manual command docs:

```powershell
make gat
uv run python scripts/manual_integration/phase10_agent_eval.py `
  --base-url https://khoasinoo-tri-am-backend.hf.space/api/v1 `
  --livekit-url wss://tri-am-bmdl413w.livekit.cloud `
  --access-token "<token>" `
  --book-id "<book_id>" `
  --thread-id "<thread_id>" `
  --mode all `
  --candidate-name baseline `
  --output-dir _docs_implemented/eval_reports/phase10_7
```

Access token must never be written into reports.

---

## 10. Production Rollout Strategy

### 10.1 Local baseline

Run local server + worker:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uv run python -m app.services.agent_voice_gpt_realtime start
```

Then run eval:

```powershell
uv run python scripts/manual_integration/phase10_agent_eval.py `
  --base-url http://127.0.0.1:8000/api/v1 `
  --mode all `
  --candidate-name baseline
```

### 10.2 Local candidate

Change only one env variable.

Example:

```powershell
$env:VOICE_AGENT_TEXT_LLM_MODEL="<candidate-model>"
uv run python -m app.services.agent_voice_gpt_realtime start
```

Run eval again and compare.

### 10.3 Production canary

Because Hugging Face free Space usually has one runtime, true traffic split may be limited.

Recommended capstone-safe canary:

- deploy candidate to dev/staging Space first;
- run production-like eval against staging;
- only then update production env;
- keep previous env values documented for rollback.

If only one production Space exists:

- deploy during low-traffic window;
- run smoke test immediately;
- rollback env if hard gate fails.

### 10.4 Rollback

Rollback is env-only:

```text
VOICE_AGENT_TEXT_LLM_MODEL=<previous>
OPENAI_STREAM_MODEL_NAME=<previous>
OPENAI_REALTIME_TRANSCRIPTION_MODEL=<previous>
VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL=<previous>
AGENT_MODEL_PROFILE=baseline
```

Restart Space after env rollback.

---

## 11. Go/No-Go Rules

Candidate can go production only if:

- metadata cases pass 100%;
- web permission violation count is 0;
- source accuracy is equal or better than baseline;
- hallucination/forbidden fact failures are not worse than baseline;
- voice STT meaning pass rate is not worse than baseline;
- latency p95 regression is within accepted threshold or explicitly approved;
- cost increase is documented and acceptable;
- no new duplicated timeline messages after Phase 10.6 checks.

Reject candidate if:

- it answers from memory when book context is required;
- it searches web before permission;
- it fails author/chapter metadata that baseline passes;
- it causes repeated answer loops;
- it breaks LiveKit tool calling;
- it requires changing FE contract.

---

## 12. Test Plan

### 12.1 Unit tests

```powershell
uv run pytest tests/services/agent_observability -q
uv run pytest tests/services/agent_policy tests/services/voice_agent -q
uv run ruff check scripts/manual_integration tests/services/agent_observability app/services/agent_observability
```

### 12.2 Manual local evaluation

```powershell
make gat
uv run python scripts/manual_integration/phase10_agent_eval.py `
  --base-url http://127.0.0.1:8000/api/v1 `
  --mode all `
  --candidate-name baseline
```

### 12.3 Manual production evaluation

```powershell
make gat
uv run python scripts/manual_integration/phase10_agent_eval.py `
  --base-url https://khoasinoo-tri-am-backend.hf.space/api/v1 `
  --mode all `
  --candidate-name production_current
```

### 12.4 Compare reports

```powershell
uv run python scripts/manual_integration/compare_phase10_model_reports.py `
  --baseline "<baseline_report.json>" `
  --candidate "<candidate_report.json>"
```

---

## 13. Documentation Updates

After implementation, update:

```text
_docs_implemented/phase_10_7_model_evaluation_production_rollout_test_report.md
_docs_implemented/phase_10_grounded_book_agent_voice_accuracy_roadmap.md
.env.example
README.md if deployment env guidance changes
```

Do not put access tokens or provider secrets in reports.

---

## 14. Trade-offs

### Trade-off 1: Evaluation takes time

Full voice eval with real LiveKit/provider calls is slower than unit tests.

Decision:

```text
Keep it manual integration, not default pytest.
```

### Trade-off 2: Metrics are not perfect

Some answer quality checks still use `must_include`/`must_not_include`.

Decision:

```text
Use deterministic checks first.
Only add LLM-as-judge later as secondary signal.
```

### Trade-off 3: Candidate model may improve quality but increase cost

Decision:

```text
Report cost explicitly.
For capstone/free deployment, prefer stable and affordable unless quality gap is large.
```

### Trade-off 4: Production canary is limited on one Hugging Face Space

Decision:

```text
Use staging/dev Space when possible.
If not possible, deploy during low traffic and keep env rollback ready.
```

---

## 15. Acceptance Criteria

Phase 10.7 is complete when:

1. Candidate matrix exists and is documented.
2. Eval runner records active model config safely.
3. Eval runner outputs JSON and Markdown reports.
4. Comparator can compare baseline vs candidate and produce go/no-go.
5. Unit tests cover metric/comparator logic offline.
6. Local baseline report exists.
7. At least one candidate report exists or the doc states why no candidate was approved.
8. Production smoke test report exists for current model config.
9. Rollback env values are documented.
10. No FE contract changes are required.

---

## 16. Senior Note Cho Em

Đến Phase 10.7, tư duy quan trọng nhất là:

```text
Model selection là một quyết định vận hành, không phải một cảm giác.
```

Nếu em đi bảo vệ đồ án và nói:

> Em đổi model này vì nó mới hơn.

thì chưa thuyết phục.

Nhưng nếu em nói:

> Em có bộ test gồm metadata, hỏi chương, RAG ngữ nghĩa, voice STT và quyền tìm web. Model mới chỉ được đưa vào production nếu không làm giảm groundedness, không vi phạm quyền tìm web, latency/cost chấp nhận được, và có rollback bằng biến môi trường.

thì đó là tư duy của một hệ thống thật.

Phase này giúp em chứng minh Triam không chỉ “gọi AI API”, mà có quy trình kiểm soát chất lượng AI trước khi triển khai.
