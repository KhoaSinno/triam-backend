# Phase 10.1 Test Report - Deterministic Metadata And Section Router

Date: 2026-06-04  
Environment: local FastAPI + local LiveKit worker + real LiveKit/OpenAI/Supabase providers  
Status: implemented and verified with known voice orchestration trade-offs

---

## 1. Kết Quả Triển Khai

Phase 10.1 đã bổ sung một lớp quyết định nguồn dữ liệu dùng chung:

```text
metadata question
-> Book metadata

explicit chapter/section question
-> canonical BookSection

ambiguous section question
-> clarification

semantic book question
-> existing RAG

external/current question
-> existing web permission policy
```

Các thay đổi chính:

- metadata không còn đi qua embedding/vector search;
- câu hỏi chỉ rõ chương hoặc đề mục được resolve bằng cây `BookSection`;
- section context chỉ đọc sau khi resolve và luôn bị giới hạn trong `document_ids`;
- text chat gọi router trực tiếp trước LLM/RAG;
- voice tool `search_book_knowledge` dùng cùng router;
- trace có thêm `grounding_route` và `grounding_reason_code`;
- không đổi API, DataChannel, schema database hoặc logic Full/Pareto.

Rollback:

```text
AGENT_GROUNDING_ROUTER_ENABLED=false
```

---

## 2. Kiểm Thử Tự Động

### Focused regression

```text
70 passed
```

Bao phủ:

- query normalization;
- bilingual metadata intent;
- section reference dạng số, chữ và Roman;
- scoped book/section resolution;
- section context và truncation;
- grounding route và safe trace;
- voice-agent regression cũ.

### Full regression

```text
175 passed in 156.91s
```

### Static checks

```text
focused ruff: passed
compileall: passed
git diff --check: passed
```

---

## 3. Real Typed-Chat Evaluation

Report:

```text
logs/agent_eval_phase10_1/phase10_agent_eval_20260604_194424.json
logs/agent_eval_phase10_1/phase10_agent_eval_20260604_194424.md
```

Kết quả:

| Metric | Result |
| --- | ---: |
| Strict cases | 8/10 |
| Content accuracy | 100% |
| Intent accuracy | 100% |
| Answer source accuracy | 100% |
| Section resolution accuracy | 60% |
| Web policy safety | 100% |
| Turn latency p50 | 2,296 ms |
| Turn latency p95 | 9,726 ms |
| DB message delta | 21 |

Hai strict case còn fail đều là câu hỏi semantic đi qua RAG cũ. Nội dung, intent và nguồn trả lời đúng, nhưng `BookKnowledge` hiện chưa lưu `section_id`, nên trace không thể chứng minh chunk thuộc chương nào.

Đây là scope của:

```text
Phase 10.2 - Canonical BookSection Knowledge Index
```

Không gán giả `section_id` để làm đẹp metric.

---

## 4. Supervised Realtime Voice Evaluation

Report:

```text
logs/agent_eval_phase10_1/phase10_agent_eval_20260604_200359.json
logs/agent_eval_phase10_1/phase10_agent_eval_20260604_200359.md
logs/phase10_1_voice_supervised.log
```

Kết quả:

| Metric | Result |
| --- | ---: |
| Strict cases | 1/5 |
| Content accuracy | 100% |
| Voice meaning preservation | 80% |
| Answer source accuracy | 80% |
| Section resolution accuracy for traced section cases | 100% |
| Turn latency p50 | 15,469 ms |
| Turn latency p95 | 25,603 ms |
| DB message delta | 11 |

Phân tích:

1. Metadata author đi đúng `book_metadata`, nhưng STT làm mất từ quan trọng trong transcript.
2. Câu tóm tắt chương 4 gọi shared router, resolve đúng section và pass.
3. Câu hỏi “ý chương 4” gọi đúng section, nhưng realtime model viết lại tool query thành dạng content nên trace intent là `book_section.content`.
4. Câu chương mơ hồ không gọi tool; realtime model tự trả lời nên không có grounding trace.
5. Câu Bitcoin gọi đúng web permission policy, nhưng bỏ qua grounding router nên trace không có detected intent.

Kết luận:

- shared router hoạt động đúng khi realtime model gọi `search_book_knowledge`;
- Phase 10.1 không thể đảm bảo mọi voice turn đi qua router khi OpenAI Realtime dùng turn detection nội bộ;
- không nên thêm heuristic theo từng câu audio để ép metric.

LiveKit ghi rõ: muốn dùng `on_user_turn_completed` để chặn và enrich mọi realtime turn, phải chuyển turn detection ra khỏi realtime model. Thay đổi này cần đánh giá latency, STT và tài nguyên riêng.

Nguồn:

- https://docs.livekit.io/agents/logic-structure/nodes/
- https://docs.livekit.io/agents/models/realtime/

---

## 5. Trade-off Còn Lại

### 5.1 Semantic RAG chưa có canonical section identity

Ảnh hưởng:

- semantic answer có thể đúng nhưng không chứng minh được đúng chương;
- trace `retrieval_section_ids` rỗng.

Xử lý:

- Phase 10.2 tạo canonical `BookSection` knowledge index;
- Phase 10.3 thêm hybrid retrieval và confidence guardrails.

### 5.2 Realtime model có thể bỏ qua tool

Ảnh hưởng:

- voice có thể trả đúng nội dung nhưng source/intent trace là `unknown`;
- hành vi voice và text chưa hoàn toàn đồng nhất.

Xử lý:

- Phase 10.4 đánh giá STT và clarification;
- Phase 10.5 quyết định shared orchestration hoặc agent-managed turn detection;
- không ép `tool_choice=required` ngay vì sẽ làm hỏng casual conversation và permission replies.

### 5.3 Voice section context tăng latency

Section context chính xác hơn vector RAG toàn sách, nhưng voice p95 hiện khoảng 25.6 giây do:

- provider round trip;
- context section dài;
- realtime model vừa sinh text vừa phát audio.

Xử lý:

- đo riêng input-to-first-audio thay vì chỉ turn completion;
- canonical index và bounded context ở Phase 10.2/10.3;
- không giảm context mù quáng trước khi đo groundedness.

---

## 6. Go/No-Go

### Go

- Merge Phase 10.1 cho typed chat và shared grounding tool.
- Deploy sau smoke test với `AGENT_GROUNDING_ROUTER_ENABLED=true`.
- Dùng feature flag để rollback nếu provider/runtime có regression.

### Không tuyên bố đã giải quyết

- semantic RAG đúng section;
- mọi realtime voice turn bắt buộc đi router;
- STT robust với audio bị mất từ quan trọng;
- voice/text orchestration hoàn toàn giống nhau.

Next phase:

```text
Phase 10.2 - Canonical BookSection Knowledge Index
```
