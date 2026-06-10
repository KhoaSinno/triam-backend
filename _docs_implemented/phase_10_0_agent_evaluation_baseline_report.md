# Phase 10.0 Agent Evaluation Baseline Report

Date: 2026-06-04  
Status: Implemented and locally validated  
Scope: book-grounded text chat, realtime voice, safe trace, deterministic evaluation

---

## 1. Kết Luận

Phase 10.0 đã hoàn thành mục tiêu đo lường mà không thay đổi hành vi trả lời hiện tại:

- mỗi lượt text và voice có safe trace;
- trace không chứa access token, raw audio, full transcript, full answer, nội dung chunk hoặc embedding;
- retrieval ghi lại IDs, số kết quả, score và latency;
- runner manual integration dùng API auth, LiveKit thật, voice fixture thật và dữ liệu sách thật;
- runner chấm riêng content, intent, answer source, section, web policy, voice meaning và latency;
- trace voice xử lý được final transcript đến trễ;
- pytest toàn dự án, focused ruff và compile đều pass.

Kết quả baseline chứng minh vấn đề chính hiện tại không đơn thuần là model yếu:

1. Text thường trả đúng fact nhưng chọn sai nguồn.
2. Hệ thống chưa có intent router và section resolver rõ ràng.
3. Voice có thêm lỗi STT và web permission flow.
4. Có trường hợp retrieval lấy được dữ liệu liên quan với score cao nhưng agent vẫn kết luận sách không có thông tin.

Phase 10.0 đủ điều kiện để chuyển sang Phase 10.1. Chưa nên tối ưu bằng cách chỉ đổi prompt hoặc nâng model trước khi sửa routing và section resolution.

---

## 2. Những Thành Phần Đã Implement

### Runtime safe trace

Package mới:

```text
app/services/agent_observability/
  contracts.py
  turn_trace.py
```

Trace theo dõi:

- input mode;
- final transcript có xuất hiện hay không;
- transcript/assistant character count;
- tool flow;
- retrieval IDs, score và latency;
- answer source;
- error code;
- total turn latency;
- mức độ tin cậy của correlation.

### Instrumentation

Đã instrument:

- text chat turn;
- realtime voice turn;
- vector retrieval;
- web search và permission tool;
- assistant committed response;
- delayed final transcript.

### Golden dataset và runner

Dataset hiện tại:

- 10 text cases;
- 5 voice cases dùng WAV thật;
- ground truth lấy qua authenticated API từ sách `Of Mice and Men`.

Runner:

```powershell
uv run python scripts/manual_integration/phase10_agent_eval.py --mode text
uv run python scripts/manual_integration/phase10_agent_eval.py --mode voice
```

Runner ghi JSON và Markdown report vào `logs/agent_eval/`, không in access token.

### Project skill

Đã thêm skill:

```text
.agents/skills/triam-grounded-agent-evaluation/
```

Skill yêu cầu agent phải đo, phân loại đúng tầng lỗi và thêm regression case trước khi sửa behavior.

---

## 3. Môi Trường Baseline

| Thành phần | Giá trị |
| --- | --- |
| API | Local FastAPI `http://127.0.0.1:8000/api/v1` |
| Ground truth | Authenticated API và dữ liệu thật |
| Realtime model | `gpt-realtime` |
| Realtime transcription | `gpt-4o-transcribe` |
| Text chat model | `gpt-4o-mini` |
| LiveKit Agents | `1.5.17` |
| LiveKit RTC | `1.1.8` |
| Voice fixtures | WAV mono 48 kHz, 16-bit PCM |

Final reports:

```text
logs/agent_eval/phase10_agent_eval_20260604_180921.json
logs/agent_eval/phase10_agent_eval_20260604_181111.json
```

---

## 4. Baseline Text

| Metric | Result |
| --- | ---: |
| Strict case pass | 0/10 |
| Content accuracy | 9/10, 90% |
| Intent accuracy | 0/10, 0% |
| Answer source accuracy | 3/10, 30% |
| Section resolution accuracy | 0/5, 0% |
| Web policy safety | 10/10, 100% |
| Turn latency p50 | 4,968 ms |
| Turn latency p95 | 11,739 ms |
| Retrieval latency p50 | 516 ms |
| Retrieval latency p95 | 1,445 ms |

`Strict case pass = 0%` vì case yêu cầu đúng cả content, intent, source và section. Nó không có nghĩa tất cả câu trả lời text đều sai nội dung.

### Nhận định chính

- Câu hỏi metadata như tác giả và tên sách có thể trả đúng, nhưng vẫn gọi vector RAG thay vì đọc metadata xác định từ database.
- Câu hỏi số phần chính không lấy được fact vì vector retrieval không phù hợp với metadata/count query.
- Câu hỏi chapter/section chưa resolve section ID; toàn bộ đi qua semantic RAG chung.
- Câu hỏi mơ hồ vẫn tự chọn một chương để trả lời thay vì yêu cầu user làm rõ.
- Web permission cho câu hỏi ngoài sách hoạt động đúng ở baseline text.

### Failure counts

Các code có thể cùng xuất hiện trong một case:

| Failure code | Count |
| --- | ---: |
| `ROUTING_INTENT` | 10 |
| `CONTEXT_VALIDATION` | 7 |
| `ROUTING_SECTION` | 5 |
| `RETRIEVAL_COVERAGE` | 1 |

---

## 5. Baseline Voice

| Metric | Result |
| --- | ---: |
| Strict case pass | 0/5 |
| Content accuracy | 2/5, 40% |
| Voice meaning preservation | 4/5, 80% |
| Intent accuracy | 0/5, 0% |
| Answer source accuracy | 1/5, 20% |
| Section resolution accuracy | 0/2, 0% |
| Web policy safety | 5/5, 100% |
| Final transcript correlated | 5/5, 100% |
| Turn latency p50 | 12,233 ms |
| Turn latency p95 | 12,271 ms |
| Retrieval latency p50 | 662 ms |
| Retrieval latency p95 | 796 ms |

### Nhận định chính

- STT làm mất hoặc đổi một số từ quan trọng. Một case metadata mất từ khóa chỉ intent, làm câu hỏi khó route chính xác.
- Hai case chương 4 vẫn chuyển sang hỏi permission web dù retrieval đã trả 10 kết quả với top scores khoảng `0.65-0.68`.
- Câu hỏi mơ hồ có thể bị hiểu thành phản hồi cho pending web permission của lượt trước.
- Voice chậm hơn text đáng kể; retrieval không phải phần chiếm phần lớn latency.
- Sau khi harden correlation, toàn bộ voice cases đều ghi nhận đúng final transcript, kể cả transcript đến trễ.

### Failure counts

| Failure code | Count |
| --- | ---: |
| `ROUTING_INTENT` | 5 |
| `CONTEXT_VALIDATION` | 2 |
| `ROUTING_SECTION` | 2 |
| `WEB_PERMISSION` | 2 |
| `RETRIEVAL_RELEVANCE` | 2 |
| `INPUT_STT` | 1 |
| `RETRIEVAL_COVERAGE` | 1 |

---

## 6. Persistence Check

| Run | Cases | DB message delta | Expected |
| --- | ---: | ---: | ---: |
| Text | 10 | 21 | 20 user/assistant messages + 1 greeting |
| Voice | 5 | 11 | 10 user/assistant messages + 1 greeting |

Hai baseline runs không cho thấy duplicate persistence rõ ràng.

---

## 7. Trace Bugs Đã Phát Hiện Và Fix Trong Phase 10.0

### Final transcript của lượt mới bị gắn vào lượt trước

Nguyên nhân:

- final transcript của lượt mới đến trong cửa sổ late transcript;
- tracer trước đây luôn ưu tiên update last completed turn.

Fix:

- chỉ bổ sung late transcript vào completed turn nếu completed turn đó chưa từng có final transcript.

### Delayed tool event tạo orphan turn

Nguyên nhân:

- `function_tools_executed` có thể đến sau assistant response;
- handler dùng sự kiện trễ để tự tạo một turn mới rỗng.

Fix:

- delayed tool event chỉ bổ sung vào active voice turn;
- chính tool function vẫn chịu trách nhiệm ghi tool/source/retrieval.

Regression tests đã được thêm cho correlation behavior.

---

## 8. Trade-off Còn Lại

### Dataset chưa đạt coverage mục tiêu dài hạn

Hiện tại mới có 10 text và 5 voice cases trên một sách. Mục tiêu dài hạn là nhiều sách, nhiều ngôn ngữ và nhiều loại cấu trúc tài liệu.

### Shared test thread có thể gây ảnh hưởng giữa các case

Runner hiện dùng một test thread thật. Conversation history và pending web permission có thể ảnh hưởng case tiếp theo. Điều này hữu ích để phát hiện lỗi multi-turn, nhưng chưa phải isolated evaluation hoàn toàn.

Hướng xử lý:

- thêm isolated eval thread cho single-turn benchmark;
- giữ riêng một suite multi-turn để kiểm tra permission và conversation state.

### Voice turn correlation vẫn là best effort

LiveKit event ordering không cung cấp stable turn ID xuyên suốt mọi event trong flow hiện tại. Trace đã xử lý các ordering thực tế quan sát được, nhưng vẫn cần theo dõi khi SDK thay đổi.

### Trace làm tăng log volume

Safe trace không lộ nội dung nhưng làm tăng log. Production cần retention/rotation và sampling nếu traffic tăng.

### Intent và resolved section đang để trống có chủ đích

Đây là baseline đúng của kiến trúc hiện tại, không phải lỗi instrumentation. Phase 10.1 phải tạo router/resolver rồi ghi hai field này.

---

## 9. Quyết Định Cho Phase Tiếp Theo

### Go

- triển khai Phase 10.1: deterministic metadata router và section resolver;
- dùng các case hiện tại làm regression suite;
- giữ model hiện tại để đo cải thiện do routing trước;
- thêm isolated single-turn evaluation.

### No-go

- không chỉ sửa prompt cho riêng `Of Mice and Men`;
- không nâng model để che lỗi metadata/section routing;
- không tự tìm web khi retrieval/context yếu;
- không kết luận STT là nguyên nhân duy nhất của lỗi voice.

---

## 10. Verification

Đã chạy:

```text
37 focused tests passed
142 full project tests passed
focused ruff passed
py_compile passed
git diff --check passed
10 real text cases completed
5 real voice cases completed
```

Full-project ruff còn 12 lỗi format/import cũ trong Alembic migration legacy. Phase 10.0 không tự sửa migration lịch sử vì việc đó nằm ngoài scope và không liên quan agent behavior.
