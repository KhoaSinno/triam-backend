# Phase 10.0 Implementation Guide - Agent Evaluation Baseline And Safe Trace

Date: 2026-06-04  
Status: Implemented and locally validated  
Depends on: Phase 5, Phase 7, Phase 7.1, Phase 10 roadmap  
Primary scope: grounded book chat, realtime voice, RAG trace, evaluation

---

## 1. Mục Tiêu

Phase 10.0 chưa sửa routing, RAG, prompt, STT hoặc model. Phase này xây nền tảng đo lường để những phase tiếp theo có thể trả lời chính xác:

```text
Agent trả lời sai vì:
- voice transcript sai;
- intent/router chọn sai nguồn;
- section resolver sai;
- RAG lấy sai hoặc thiếu dữ liệu;
- model tạo câu trả lời sai dù context đúng;
- web permission flow sai;
- FE hiển thị sai?
```

Kết quả cần có:

1. Một failure taxonomy dùng chung.
2. Một trace contract an toàn cho mỗi lượt chat/voice.
3. Một golden evaluation dataset có expected behavior.
4. Một runner chạy được text và voice manual integration.
5. Một baseline report trước khi Phase 10.1 thay đổi hành vi.

---

## 2. Vì Sao Phải Làm Phase Này Trước

Hiện tại một lỗi có thể bị kết luận sai:

```text
Voice trả lời sai
-> tưởng model yếu
-> nâng model
-> vẫn sai vì transcript hoặc RAG thiếu section
```

Hoặc:

```text
Agent yêu cầu tìm web
-> tưởng web permission lỗi
-> thực tế canonical section chưa được index
```

Nếu không có baseline và trace, mỗi lần sửa prompt/model có thể:

- chỉ khắc phục một câu hỏi test;
- làm chat tốt hơn nhưng voice tệ hơn;
- tăng latency hoặc chi phí mà không cải thiện accuracy;
- che lỗi retrieval bằng kiến thức có sẵn của model;
- tạo regression khó phát hiện.

OpenAI khuyến nghị bắt đầu model optimization bằng evals và baseline. LiveKit lưu ý realtime transcript có thể đến trễ, đôi khi sau câu trả lời, nên không thể dùng thời điểm transcript hiển thị để kết luận model chưa nghe user.

---

## 3. Những Việc Không Làm Trong Phase 10.0

- Không đổi `gpt-realtime` hoặc `gpt-4o-mini`.
- Không sửa threshold RAG.
- Không thêm hybrid search.
- Không thay đổi `BookKnowledge`.
- Không reindex sách.
- Không sửa prompt theo riêng `Of Mice and Men`.
- Không thay đổi web-search permission policy.
- Không thay đổi DataChannel contract của FE.
- Không thêm bảng database chỉ để lưu trace.

Mọi thay đổi hành vi thuộc Phase 10.1 trở đi.

---

## 4. Hiện Trạng Cần Đo

### 4.1 Luồng text

```text
lk.chat
-> handle_data_input
-> naive RAG hoặc agentic loop
-> search_voice_book_context
-> model trả lời
-> lk.chat + lk.transcript + DB
```

### 4.2 Luồng voice

```text
microphone audio
-> OpenAI Realtime model
-> tool call nếu model quyết định
-> assistant response
-> final transcript có thể đến trễ
-> conversation_item_added
-> lk.transcript + DB
```

### 4.3 Khoảng trống quan sát hiện tại

Log hiện tại biết:

- input/reply có bao nhiêu ký tự;
- RAG hoặc web search có lỗi hay không;
- permission được grant/deny;
- transcript final có đến hay không.

Log hiện tại chưa chứng minh được:

- intent được hiểu là gì;
- câu hỏi được route đến metadata, section, RAG hay web;
- RAG tìm các chunk nào và score bao nhiêu;
- context trả về có đúng section không;
- nguồn cuối cùng của câu trả lời;
- latency thuộc bước nào;
- câu trả lời sai từ STT, retrieval hay generation.

---

## 5. Nguồn Tài Liệu Chính Thức

- OpenAI Agent evals: https://platform.openai.com/docs/guides/agent-evals
- OpenAI model optimization: https://platform.openai.com/docs/guides/model-optimization
- OpenAI trace grading: https://platform.openai.com/docs/guides/trace-grading
- LiveKit realtime limitations: https://docs.livekit.io/agents/models/realtime/
- LiveKit events and per-turn metrics: https://docs.livekit.io/reference/other/events/
- LiveKit observability: https://docs.livekit.io/agents/build/metrics/

Kết luận áp dụng:

- eval phải reproducible;
- trace phải thể hiện workflow, không chỉ output cuối;
- voice final transcript có thể đến sau agent response;
- `conversation_item_added` và per-turn metrics phù hợp để quan sát turn đã commit;
- không dùng raw transcript timing làm correlation ID.

---

## 6. Failure Taxonomy

Mọi case thất bại phải có một primary failure layer và có thể có secondary layers.

| Code | Layer | Mô tả |
| --- | --- | --- |
| `INPUT_STT` | Voice/STT | Transcript final sai hoặc mất thông tin quan trọng |
| `INPUT_AMBIGUOUS` | Input | Câu hỏi vốn không đủ thông tin để trả lời |
| `ROUTING_INTENT` | Router | Hiểu sai loại câu hỏi hoặc chọn sai nguồn |
| `ROUTING_SECTION` | Resolver | Không resolve hoặc resolve sai section/chapter |
| `RETRIEVAL_COVERAGE` | Index | Dữ liệu đúng không tồn tại trong index |
| `RETRIEVAL_RELEVANCE` | Retrieval | Index có dữ liệu nhưng top results không liên quan |
| `CONTEXT_VALIDATION` | Guardrail | Context yếu nhưng vẫn được xem là đủ |
| `GENERATION_GROUNDING` | Model | Context đúng nhưng câu trả lời sai/bịa |
| `WEB_PERMISSION` | Policy | Tìm web sai thời điểm hoặc hỏi permission sai |
| `PERSISTENCE_DUPLICATE` | Backend | DB lưu trùng message |
| `FE_RECONCILIATION` | Frontend | DB đúng nhưng UI hiển thị trùng/sai thứ tự |
| `INFRA_LATENCY` | Runtime | Timeout hoặc latency vượt budget |
| `UNKNOWN` | Chưa đủ bằng chứng | Phải ghi rõ dữ liệu còn thiếu |

Quy tắc:

- Không gắn `GENERATION_GROUNDING` nếu chưa xác minh context đưa vào model.
- Không gắn `INPUT_STT` chỉ vì UI transcript hiển thị trễ.
- Không gắn `INFRA_LATENCY` nếu lỗi thực tế là retrieval sai.
- Không kết luận model yếu từ output không có canonical context.

---

## 7. Trace Contract

### 7.1 Package mới

```text
app/services/agent_observability/
  __init__.py
  contracts.py
  turn_trace.py
```

Không đặt logic đánh giá vào `agent_voice_gpt_realtime.py`. File realtime chỉ phát signal vào tracer.

### 7.2 Contract đề xuất

```python
class AgentInputMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"


class AgentAnswerSource(str, Enum):
    UNKNOWN = "unknown"
    BOOK_METADATA = "book_metadata"
    BOOK_SECTION = "book_section"
    BOOK_RAG = "book_rag"
    WEB = "web"
    CLARIFICATION = "clarification"
    POLICY = "policy"
    ERROR = "error"
```

Safe turn trace:

```python
@dataclass
class AgentTurnTrace:
    trace_id: str
    thread_id: str | None
    room_name: str | None
    input_mode: AgentInputMode
    started_at: datetime

    transcript_final_seen: bool = False
    transcript_char_count: int = 0
    detected_language: str | None = None

    detected_intent: str | None = None
    resolved_book_ids: list[str] = field(default_factory=list)
    resolved_section_ids: list[str] = field(default_factory=list)

    retrieval_method: str | None = None
    retrieval_result_count: int = 0
    retrieval_chunk_ids: list[int] = field(default_factory=list)
    retrieval_section_ids: list[str] = field(default_factory=list)
    retrieval_scores: list[float] = field(default_factory=list)

    tool_names: list[str] = field(default_factory=list)
    answer_source: AgentAnswerSource = AgentAnswerSource.UNKNOWN
    assistant_char_count: int = 0
    stage_latency_ms: dict[str, int] = field(default_factory=dict)
    error_code: str | None = None
```

### 7.3 Safe logging

Không log:

- token, API key hoặc headers;
- raw audio;
- full transcript hoặc assistant response;
- full RAG chunk hoặc nội dung sách;
- embedding vector;
- full web result.

Có thể log:

- trace/stage IDs;
- IDs, counts và rounded scores;
- tool names;
- latency;
- answer source;
- error class/code.

Text preview chỉ được bật local bằng:

```env
AGENT_TRACE_LOG_TEXT_PREVIEW=false
```

và phải giới hạn ký tự.

---

## 8. Correlation Cho Voice Turn

### 8.1 Vấn đề

Realtime transcript có thể đến sau assistant response. Không được:

- tạo trace chỉ khi `user_input_transcribed` đến;
- dùng transcript text làm khóa;
- giả định transcript final đến trước tool call.

### 8.2 Quy tắc correlation

Mỗi session có một `AgentTurnTracer`.

Với text:

```text
handle_data_input -> begin trace
```

Với voice:

```text
speech/tool/conversation event đầu tiên của user turn
-> tạo active trace nếu chưa có
-> tool calls và assistant response ghi vào active trace
-> final transcript đến trễ thì bổ sung cùng trace
-> assistant conversation item committed thì complete trace
```

Nếu SDK cung cấp message/item ID ổn định thì lưu làm correlation metadata. Không phụ thuộc hoàn toàn vào timestamp.

### 8.3 Event nên dùng

- `user_input_transcribed`: final transcript và language.
- `conversation_item_added`: user/assistant item đã commit.
- `function_tools_executed`: tool flow nếu SDK hỗ trợ ổn định.
- `ChatMessage.metrics`: per-turn latency nếu có.
- `session_usage_updated`: usage tracking tổng hợp.

Không thiết kế mới dựa trên session-level `metrics_collected` đã deprecated.

---

## 9. Cấu Hình Đề Xuất

Thêm vào `Settings` và `.env.example` khi implement:

```env
AGENT_TRACE_ENABLED=true
AGENT_TRACE_SCORE_PRECISION=4
AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS=15
```

Nguyên tắc:

- safe metadata trace có thể bật production;
- text preview phải tắt production;
- mọi biến có default bảo thủ;
- server vẫn khởi động nếu chưa khai báo biến mới.

---

## 10. Golden Evaluation Dataset

### 10.1 Vị trí

```text
tests/fixtures/agent_eval/
  book_grounding_cases.json
  voice_manifest.json
```

Voice `.wav` tiếp tục nằm dưới `tests/fixtures/` và được `.gitignore` loại trừ. Manifest chỉ lưu đường dẫn tương đối và expected behavior.

### 10.2 Schema text case

```json
{
  "id": "mice-author-vi-text",
  "book_id": "book-id",
  "context_id": "context-id",
  "thread_id": "thread-id",
  "input_mode": "text",
  "question": "Tác giả của quyển sách là ai?",
  "expected_intent": "book_metadata.author",
  "expected_answer_source": "book_metadata",
  "expected_section_paths": [],
  "must_include": ["John Steinbeck"],
  "must_not_include": ["Curley"],
  "web_search_allowed": false
}
```

### 10.3 Schema voice case

```json
{
  "id": "mice-chapter-four-vi-voice",
  "book_id": "book-id",
  "thread_id": "thread-id",
  "input_mode": "voice",
  "audio_fixture": "tests/fixtures/mice-chapter-four.wav",
  "expected_transcript_meaning": "Tóm tắt chương 4",
  "expected_intent": "book_section.summary",
  "expected_section_paths": ["4"],
  "expected_answer_source": "book_section",
  "web_search_allowed": false
}
```

### 10.4 Coverage tối thiểu

| Nhóm | Text | Voice |
| --- | ---: | ---: |
| Metadata | 5 | 2 |
| Section/chapter | 8 | 4 |
| Semantic toàn sách | 4 | 2 |
| Không có trong sách | 3 | 1 |
| Mơ hồ/cần hỏi lại | 4 | 3 |
| Web permission | 3 | 2 |
| Tổng | 27 | 14 |

Runner phải hỗ trợ trạng thái `not_recorded`, `not_run`, `passed`, `failed` để bổ sung audio dần mà không làm sai report.

### 10.5 Quy tắc chấm

- Đánh giá source, intent và section trước exact wording.
- Không yêu cầu model trả câu giống hệt reference.
- Dùng `must_include`, `must_not_include`, source và section để chấm deterministic.
- LLM-as-judge chỉ là lớp bổ sung, không thay deterministic checks.

---

## 11. Manual Evaluation Runner

### 11.1 Vị trí

```text
scripts/manual_integration/phase10_agent_eval.py
```

Không đặt test cần server/token/provider thật vào pytest mặc định.

### 11.2 Chế độ

```text
--mode text
--mode voice
--mode all
--base-url http://127.0.0.1:8000/api/v1
--case-id optional
--output logs/agent_eval/<timestamp>.json
```

Runner phải:

1. Đọc manifest.
2. Lấy LiveKit token qua API được auth.
3. Gửi typed input hoặc publish WAV như microphone.
4. Thu `lk.chat`, `lk.transcript` và DB message delta.
5. Thu trace metadata.
6. Chấm deterministic assertions.
7. Ghi JSON report và Markdown summary vào `logs/agent_eval/`.
8. Không in access token.

Book/thread IDs là runtime parameters hoặc environment variables:

```env
AGENT_EVAL_BOOK_ID=
AGENT_EVAL_CONTEXT_ID=
AGENT_EVAL_THREAD_ID=
TRIAM_ACCESS_TOKEN=
```

Credentials và token không được commit.

---

## 12. Metrics

### 12.1 Accuracy

```text
intent_accuracy
section_resolution_accuracy
retrieval_hit_at_k
wrong_section_rate
book_answerable_web_fallback_rate
grounded_answer_rate
```

### 12.2 Voice

```text
voice_meaning_preservation_rate
clarification_rate_for_ambiguous_voice
wrong_answer_rate_after_bad_transcript
```

Không dùng exact word error rate làm chỉ số duy nhất. Transcript có thể khác câu chữ nhưng vẫn giữ đúng intent.

### 12.3 Latency

```text
input_to_first_tool_ms
retrieval_ms
web_search_ms
llm_response_ms
input_to_first_assistant_output_ms
turn_total_ms
```

Báo cáo p50/p95 khi đủ mẫu. Không kết luận từ một cold-start request.

---

## 13. File Thay Đổi Khi Implement

### File mới

```text
app/services/agent_observability/__init__.py
app/services/agent_observability/contracts.py
app/services/agent_observability/turn_trace.py
tests/services/agent_observability/test_turn_trace.py
tests/fixtures/agent_eval/book_grounding_cases.json
tests/fixtures/agent_eval/voice_manifest.json
scripts/manual_integration/phase10_agent_eval.py
```

### File cập nhật

```text
app/core/config.py
.env.example
app/services/agent_voice_gpt_realtime.py
app/services/rag_service.py
app/services/voice_agent/rag_context.py
tests/services/voice_agent/test_rag_context.py
```

### Không cần thay đổi

```text
app/models/db_models.py
Alembic migrations
FE API/DataChannel contract
Full/Pareto pipeline
```

---

## 14. Trình Tự Implement

1. Tạo contracts và tracer thuần, đảm bảo tracer không thể làm hỏng agent flow.
2. Instrument retrieval nhưng giữ nguyên threshold/kết quả.
3. Instrument text flow.
4. Instrument voice flow và delayed transcript.
5. Tạo golden dataset và runner.
6. Chạy local, production smoke và viết baseline report.

Không trộn behavior fix vào cùng diff Phase 10.0.

---

## 15. Test Plan

### Unit tests

```powershell
uv run pytest tests/services/agent_observability -q
uv run pytest tests/services/voice_agent -q
```

Test tối thiểu:

- trace lifecycle;
- delayed transcript bổ sung đúng active voice turn;
- safe payload không chứa text/secret;
- retrieval trace lưu IDs/scores nhưng không lưu content;
- tracer failure không làm hỏng Agent;
- answer source được ghi đúng;
- duplicate completion không tạo hai trace.

### Static checks

```powershell
uv run ruff check app/services/agent_observability app/services/voice_agent app/services/rag_service.py app/services/agent_voice_gpt_realtime.py tests/services/agent_observability tests/services/voice_agent
uv run python -m py_compile app/services/agent_voice_gpt_realtime.py app/services/rag_service.py
```

### Manual local integration

```powershell
make t1
make t5
make gat

uv run python scripts/manual_integration/phase10_agent_eval.py --mode text
uv run python scripts/manual_integration/phase10_agent_eval.py --mode voice
```

### Production smoke

Chỉ chạy bằng test account và case được đánh dấu cho phép ghi DB.

Không:

- chạy hàng loạt voice case không kiểm soát;
- xoá dữ liệu production;
- bật transcript preview;
- đưa token vào command history hoặc report.

---

## 16. Acceptance Criteria

Phase 10.0 hoàn thành khi:

- có failure taxonomy dùng trong report;
- mỗi text turn có safe trace;
- mỗi voice turn có trace dù final transcript đến trễ;
- retrieval trace có top IDs/scores nhưng không lộ chunk text;
- answer source được xác định hoặc ghi `unknown` có lý do;
- golden dataset đạt coverage tối thiểu hoặc case chưa có audio được đánh dấu rõ;
- runner text/voice tạo JSON và Markdown report;
- baseline report phân loại lỗi hiện tại;
- test/ruff pass;
- không thay đổi hành vi trả lời, API hoặc FE contract;
- không có migration;
- không lộ secret hoặc full document content trong log.

Phase 10.0 không yêu cầu accuracy cao. Nó yêu cầu accuracy hiện tại được đo đúng và reproducible.

Kết quả triển khai và baseline thực tế:

```text
_docs_implemented/phase_10_0_agent_evaluation_baseline_report.md
```

---

## 17. Trade-off

### Trace tăng log volume

Giảm bằng cách chỉ log stage quan trọng, dùng IDs/counts và không log mỗi audio frame/token.

### Realtime correlation không hoàn hảo

Dùng session-scoped active turn, ưu tiên SDK item ID và ghi `correlation_quality` khi phải fallback.

### Golden dataset có thể thiên lệch

Giữ case từ bug production thật, thêm nhiều sách/ngôn ngữ về sau và thêm regression case cho mỗi bug mới.

### Runner tạo chat data thật

Dùng test account/thread, report DB delta và không tự động xoá production.

---

## 18. Deliverable Cuối Phase

Sau khi implement và test, tạo:

```text
_docs_implemented/phase_10_0_agent_evaluation_baseline_report.md
```

Report phải có:

- environment và model versions;
- dataset coverage;
- metrics text/voice;
- latency p50/p95 nếu đủ mẫu;
- failure counts theo taxonomy;
- case sai quan trọng;
- bằng chứng ưu tiên Phase 10.1 và 10.2;
- trade-off chưa xử lý;
- quyết định go/no-go cho phase tiếp theo.
