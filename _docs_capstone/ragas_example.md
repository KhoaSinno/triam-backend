# MÔ PHỎNG LUỒNG DỮ LIỆU VÀ TÍNH TOÁN — `eval_llm_as_judge.py`

> Tài liệu này mô phỏng lại **từng bước xử lý** của script [`tests/eval_llm_as_judge.py`](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/eval_llm_as_judge.py) bằng **dữ liệu thực tế** trích từ tệp `production_flow_trace.json`, giúp minh bạch hóa toàn bộ quy trình tính toán 5 chỉ số RAGAS cho Hội đồng Bảo vệ.

---

## 1. ĐẦU VÀO: Một test case từ `production_flow_trace.json`

Mỗi dòng trong `production_flow_trace.json` là một **Test Case** gồm đúng 4 trường dữ liệu:

```json
{
  "query_id": "Q42",
  "user_input": "Tôi thắc mắc là trong sách có nói là ngôi nhà là tài sản lớn nhất và là khoản đầu tư tối ưu nhất. Vậy thì tại sao phải nói vậy?",
  "reference": "Cha Giàu Cha Nghèo phản bác quan điểm đó: ngôi nhà bạn ở KHÔNG phải tài sản vì nó không tạo ra dòng tiền — thay vào đó nó tiêu thụ tiền (thế chấp, bảo trì, thuế). Tài sản thực sự là thứ bỏ tiền vào túi bạn mỗi tháng.",
  "route": "book_rag",
  "response": "Trong sách Cha Giàu Cha Nghèo, tác giả Robert Kiyosaki phản bác quan điểm đó. Ông lập luận rằng ngôi nhà bạn đang ở KHÔNG phải là tài sản — nó là tiêu sản (liability), vì nó không mang lại thu nhập mà còn tốn chi phí hàng tháng như trả nợ thế chấp, bảo trì, và thuế bất động sản.",
  "contexts": [
    "[4.1] Section 4.1: The Rich Don't Work for Money — Assets vs Liabilities. Kiyosaki defines an asset as something that puts money in your pocket. A liability takes money out. Most people think their home is their biggest asset, but Kiyosaki argues it is a liability because you pay mortgage, maintenance, and taxes every month without income from it.",
    "[4.2] Section 4.2: The Cash Flow Pattern of the Poor. The poor work for money, spend it all, and own liabilities they think are assets. Their house, car, and credit card debts drain their cash flow.",
    "[4.3] Section 4.3: Building the Asset Column. Rich people focus on building their asset column — stocks, bonds, real estate that generates rent, royalties, and business that runs without them."
  ]
}
```

**Chú thích 4 trường dữ liệu đầu vào:**

| Trường | Nguồn gốc | Vai trò |
| :--- | :--- | :--- |
| `user_input` | Log thoại thực tế từ `log_live_context_3.md` | Câu hỏi của người học |
| `reference` | Biên soạn thủ công từ sách gốc | Đáp án chuẩn Ground Truth |
| `response` | Backend sinh ra qua `gemini-3.5-flash-lite` | Câu trả lời thực tế của AI |
| `contexts` | Query từ PostgreSQL DB (chunk_ids 8892, 8885, 8922) | Các đoạn văn bản RAG retrieve được |

---

## 2. LUỒNG XỬ LÝ BẤT ĐỒNG BỘ (`evaluate_item`)

Khi script gọi `asyncio.gather(...)`, 5 hàm tính chỉ số **chạy đồng thời** cho Test Case Q42:

```
asyncio.gather(
    evaluate_faithfulness(q, ctx, resp),       ─┐
    evaluate_answer_relevancy(q, resp),         │  Chạy song song
    evaluate_context_recall(q, ref, ctx),       │  (không đợi nhau)
    evaluate_answer_correctness(q, ref, resp),  │
    evaluate_context_precision(q, ctx),        ─┘
)
```

`asyncio.Semaphore(5)` đảm bảo tối đa **5 test case** được xử lý đồng thời, tránh nghẽn API Gemini.

---

## 3. TÍNH TOÁN CHI TIẾT TỪNG CHỈ SỐ

---

### 3.1. CONTEXT PRECISION — MAP@K (Mean Average Precision)

**Prompt gửi cho LLM Judge:**

```
Câu hỏi: Tôi thắc mắc là trong sách có nói là ngôi nhà là tài sản lớn nhất và là
khoản đầu tư tối ưu nhất. Vậy thì tại sao phải nói vậy?

Danh sách các đoạn ngữ cảnh trích xuất theo thứ tự xếp hạng (từ Top 1 đến Top K):
Chunk [1]: [4.1] Section 4.1: The Rich Don't Work for Money — Assets vs Liabilities...
Chunk [2]: [4.2] Section 4.2: The Cash Flow Pattern of the Poor...
Chunk [3]: [4.3] Section 4.3: Building the Asset Column...

Nhiệm vụ: Kiểm tra từng Chunk xem nó CÓ CHỨA thông tin hữu ích để trả lời câu hỏi không.
Trả về JSON: {"verdicts": [true/false cho Chunk 1, true/false cho Chunk 2, ...]}
```

**LLM Judge trả về:**

```json
{ "verdicts": [true, false, true] }
```

**Python tự tính MAP@K (không để LLM tự tính):**

```
verdicts = [True, False, True]
  Chunk 1 = True  → relevant_count = 1, Precision@1 = 1/1 = 1.000
  Chunk 2 = False → bỏ qua
  Chunk 3 = True  → relevant_count = 2, Precision@3 = 2/3 = 0.667

sum_precision  = 1.000 + 0.667 = 1.667
relevant_count = 2

MAP@K = sum_precision / relevant_count = 1.667 / 2 = 0.833
clamp(0.833) → context_precision = 0.83
```

**Công thức MAP@K:**

$$\text{Context Precision@K} = \dfrac{\sum_{k=1}^{K} \left( \text{Precision@k} \times v_k \right)}{\text{Tổng số chunk có liên quan}}$$

---

### 3.2. FAITHFULNESS — Tách mệnh đề, Python tự tính tỷ lệ

**Prompt gửi cho LLM Judge:**

```
Ngữ cảnh nguồn:
[4.1] Section 4.1: The Rich Don't Work for Money — Assets vs Liabilities...
---
[4.2] Section 4.2: The Cash Flow Pattern of the Poor...

Câu trả lời:
Trong sách Cha Giàu Cha Nghèo, tác giả Robert Kiyosaki phản bác quan điểm đó.
Ông lập luận rằng ngôi nhà bạn đang ở KHÔNG phải là tài sản — nó là tiêu sản (liability)...

Nhiệm vụ:
1. Phân rã câu trả lời thành các mệnh đề khẳng định nhỏ (atomic claims).
2. Kiểm tra từng mệnh đề có được suy ra trực tiếp từ ngữ cảnh nguồn không.
Trả về JSON: {"claims": [{"claim": "...", "is_supported": true/false}]}
```

**LLM Judge trả về:**

```json
{
  "claims": [
    {"claim": "Tác giả sách là Robert Kiyosaki",                 "is_supported": true},
    {"claim": "Ngôi nhà bạn ở không phải là tài sản",            "is_supported": true},
    {"claim": "Ngôi nhà là tiêu sản (liability)",                 "is_supported": true},
    {"claim": "Ngôi nhà không mang lại thu nhập hàng tháng",      "is_supported": true},
    {"claim": "Ngôi nhà tốn chi phí thế chấp, bảo trì, và thuế", "is_supported": true}
  ]
}
```

**Python tự tính tỷ lệ:**

```
claims = 5 mệnh đề
supported_count = 5  (tất cả is_supported = True)

Faithfulness = supported_count / len(claims) = 5 / 5 = 1.000
clamp(1.000) → faithfulness = 1.00
```

**Công thức:**

$$\text{Faithfulness} = \dfrac{|\text{Mệnh đề được ngữ cảnh chứng minh}|}{|\text{Tổng số mệnh đề}|}$$

---

### 3.3. CONTEXT RECALL — % ý chính của Reference có trong Context

**Prompt gửi cho LLM Judge:**

```
Đáp án chuẩn (Reference):
Cha Giàu Cha Nghèo phản bác quan điểm đó: ngôi nhà bạn ở KHÔNG phải tài sản vì nó
không tạo ra dòng tiền — thay vào đó nó tiêu thụ tiền (thế chấp, bảo trì, thuế).
Tài sản thực sự là thứ bỏ tiền vào túi bạn mỗi tháng.

Các đoạn ngữ cảnh trích xuất (Retrieved Contexts):
[4.1] Section 4.1: The Rich Don't Work for Money — Assets vs Liabilities...
---
[4.3] Section 4.3: Building the Asset Column...

Đánh giá xem bao nhiêu % thông tin và ý chính trong Đáp án chuẩn có mặt trong ngữ cảnh.
Trả về JSON: {"recall_score": 0.0-1.0, "reason": "..."}
```

**LLM Judge trả về:**

```json
{
  "recall_score": 1.0,
  "reason": "Tất cả ý chính của Reference (nhà không phải tài sản, tạo liability,
             tốn tiền thay vì tạo ra tiền, định nghĩa tài sản thực sự) đều có mặt
             đầy đủ trong Chunk [4.1] và Chunk [4.3]."
}
```

```
clamp(1.0) → context_recall = 1.00
```

---

### 3.4. ANSWER RELEVANCY — Câu trả lời có bám sát câu hỏi không?

**Prompt gửi cho LLM Judge:**

```
Câu hỏi: Tôi thắc mắc là trong sách có nói là ngôi nhà là tài sản lớn nhất và là
khoản đầu tư tối ưu nhất. Vậy thì tại sao phải nói vậy?

Câu trả lời: Trong sách Cha Giàu Cha Nghèo, tác giả Robert Kiyosaki phản bác
quan điểm đó. Ông lập luận rằng ngôi nhà bạn đang ở KHÔNG phải là tài sản...

Đánh giá xem câu trả lời có trực tiếp giải quyết đúng và đầy đủ trọng tâm câu hỏi.
Không phạt nếu câu trả lời ngắn gọn.
Trả về JSON: {"relevancy_score": 0.0-1.0, "reason": "..."}
```

**LLM Judge trả về:**

```json
{
  "relevancy_score": 1.0,
  "reason": "Câu trả lời đi thẳng vào vấn đề: giải thích TẠI SAO ngôi nhà không
             phải tài sản theo lý luận của Kiyosaki, đúng với điểm mấu chốt mà
             người học thắc mắc."
}
```

```
clamp(1.0) → answer_relevancy = 1.00
```

---

### 3.5. ANSWER CORRECTNESS — Câu trả lời có chính xác so với Reference?

**Prompt gửi cho LLM Judge:**

```
Câu hỏi: Tôi thắc mắc là trong sách có nói là ngôi nhà là tài sản lớn nhất...

Đáp án chuẩn (Reference): Cha Giàu Cha Nghèo phản bác quan điểm đó: ngôi nhà bạn
ở KHÔNG phải tài sản vì nó không tạo ra dòng tiền...

Câu trả lời thực tế (Response): Trong sách Cha Giàu Cha Nghèo, tác giả Robert
Kiyosaki phản bác quan điểm đó. Ông lập luận rằng ngôi nhà bạn đang ở KHÔNG phải
là tài sản — nó là tiêu sản (liability)...

So sánh độ chính xác về mặt sự thật và thông tin giữa Response và Reference.
Trả về JSON: {"correctness_score": 0.0-1.0, "reason": "..."}
```

**LLM Judge trả về:**

```json
{
  "correctness_score": 1.0,
  "reason": "Response khớp hoàn toàn với Reference về luận điểm chính: nhà là
             tiêu sản, tốn chi phí định kỳ, không tạo dòng tiền vào. Không có
             thông tin sai lệch hay bịa đặt."
}
```

```
clamp(1.0) → answer_correctness = 1.00
```

---

## 4. KẾT QUẢ SAU TÍNH TOÁN CHO Q42

Sau khi tất cả 5 hàm hoàn tất, `evaluate_item` trả về dict:

```python
{
    "query_id":           "Q42",
    "user_input":         "Tôi thắc mắc là trong sách có nói là ngôi nhà là tài sản...",
    "context_precision":  0.83,    # MAP@K Python tự tính
    "context_recall":     1.00,    # LLM Judge → clamp()
    "faithfulness":       1.00,    # Python tự tính (5/5 claims)
    "answer_relevancy":   1.00,    # LLM Judge → clamp()
    "answer_correctness": 1.00,    # LLM Judge → clamp()
}
```

---

## 5. VÍ DỤ THÊM: Câu xã giao (AGENT_CONTEXT bypass)

Test Case Q60 `"Bye bye, nghỉ rồi."` — câu tạm biệt, agent không gọi RAG:

```json
{
  "query_id": "Q60",
  "user_input": "Bye bye, nghỉ rồi.",
  "reference": "Câu tạm biệt xã giao, không cần kiến thức sách.",
  "response": "Hẹn gặp lại bạn! Chúc bạn học tốt và tiếp tục hành trình đọc sách nhé!",
  "contexts": ["AGENT_CONTEXT: small-talk, no retrieval"]
}
```

**Logic xử lý đặc biệt trong `evaluate_context_precision()` và `evaluate_context_recall()`:**

```python
if any("AGENT_CONTEXT" in str(ctx) for ctx in contexts):
    return 0.70  # Bypass LLM, trả về điểm trung bình định sẵn
```

```
context_precision = 0.70  (bypass LLM — không chấm retrieval vì không có)
context_recall    = 0.70  (bypass LLM — không có reference để so sánh)
faithfulness      = 1.00  (gọi LLM → 1 claim, is_supported: True → 1/1)
answer_relevancy  = 1.00  (gọi LLM → lời chào đúng trọng tâm)
answer_correctness= 0.80  (gọi LLM → đại ý đúng nhưng không có GT cụ thể)
```

---

## 6. TỔNG HỢP 60 TEST CASES → DataFrame → CSV

Sau khi `asyncio.gather(...)` hoàn tất 60 test cases:

```python
results = [
    {"query_id": "Q1",  "context_precision": 0.00, "context_recall": 0.00,
     "faithfulness": 0.00, "answer_relevancy": 1.00, "answer_correctness": 0.90},
    # ... 58 rows tiếp theo ...
    {"query_id": "Q42", "context_precision": 0.83, "context_recall": 1.00,
     "faithfulness": 1.00, "answer_relevancy": 1.00, "answer_correctness": 1.00},
    {"query_id": "Q60", "context_precision": 0.70, "context_recall": 0.70,
     "faithfulness": 1.00, "answer_relevancy": 1.00, "answer_correctness": 0.80},
]

df = pd.DataFrame(results)

summary = {
    "context_precision":  df["context_precision"].mean(),   # = 0.4067
    "context_recall":     df["context_recall"].mean(),      # = 0.4067
    "faithfulness":       df["faithfulness"].mean(),         # = 0.4602
    "answer_relevancy":   df["answer_relevancy"].mean(),    # = 0.8400
    "answer_correctness": df["answer_correctness"].mean(),  # = 0.7558
}
```

**Terminal output:**

```
=====================================================================
🏆 BẢNG TỔNG HỢP ĐIỂM SỐ TRUNG BÌNH RAGAS PRODUCTION FLOW:
=====================================================================
   • context_precision        : 0.4067 / 1.0000
   • context_recall           : 0.4067 / 1.0000
   • faithfulness             : 0.4602 / 1.0000
   • answer_relevancy         : 0.8400 / 1.0000
   • answer_correctness       : 0.7558 / 1.0000
=====================================================================
```

---

## 7. XUẤT FILE KẾT QUẢ VỚI TIMESTAMP

```python
now_str     = datetime.now().strftime("%Y%m%d_%H%M%S")  # "20260728_135042"
history_csv = "logs/ragas_eval/production_flow_ragas_report_20260728_135042.csv"
latest_csv  = "logs/ragas_eval/production_flow_ragas_report.csv"

df.to_csv(history_csv, index=False, encoding="utf-8-sig")  # Lưu lịch sử
df.to_csv(latest_csv,  index=False, encoding="utf-8-sig")  # Cập nhật file latest
```

**Cấu trúc file CSV xuất ra:**

```
query_id,user_input,context_precision,context_recall,faithfulness,answer_relevancy,answer_correctness
Q1,"Nhân vật chính trong câu chuyện là ai?",0.0,0.0,0.0,1.0,0.9
Q42,"Tôi thắc mắc là trong sách có nói là ngôi nhà...",0.83,1.0,1.0,1.0,1.0
Q60,"Bye bye, nghỉ rồi.",0.7,0.7,1.0,1.0,0.8
```

---

## 8. SƠ ĐỒ LUỒNG DỮ LIỆU TỔNG QUAN

```
production_flow_trace.json (60 test cases)
            |
            v
    run_evaluation()
    |-- asyncio.Semaphore(5)       <- Giới hạn 5 luồng song song
    +-- asyncio.gather(60 x evaluate_item())
                |
                v [Mỗi item]
        evaluate_item(item, sem)
        |-- evaluate_context_precision(q, ctx)
        |       |-- Phát hiện AGENT_CONTEXT? --> return 0.70
        |       |-- Gọi LLM Judge --> {"verdicts": [true, false, true, ...]}
        |       +-- Python tính MAP@K --> context_precision
        |
        |-- evaluate_faithfulness(q, ctx, resp)
        |       |-- Gọi LLM Judge --> {"claims": [{claim, is_supported}, ...]}
        |       +-- Python dem: supported/total --> faithfulness
        |
        |-- evaluate_context_recall(q, ref, ctx)
        |       |-- Phát hiện AGENT_CONTEXT? --> return 0.70
        |       |-- Gọi LLM Judge --> {"recall_score": 0.0-1.0}
        |       +-- clamp() --> context_recall
        |
        |-- evaluate_answer_relevancy(q, resp)
        |       |-- Gọi LLM Judge --> {"relevancy_score": 0.0-1.0}
        |       +-- clamp() --> answer_relevancy
        |
        +-- evaluate_answer_correctness(q, ref, resp)
                |-- Gọi LLM Judge --> {"correctness_score": 0.0-1.0}
                +-- clamp() --> answer_correctness
            |
            v
    pd.DataFrame(results) --> df.mean() --> Summary
            |
            v
    |-- production_flow_ragas_report_YYYYMMDD_HHMMSS.csv  (lich su)
    +-- production_flow_ragas_report.csv                  (latest)
```

---

## 9. TẠI SAO PYTHON TỰ TÍNH THAY VÌ ĐỂ LLM TÍNH?

| Chi so | Ai tinh? | Ly do |
| :--- | :---: | :--- |
| `context_precision` | **Python** (MAP@K) | LLM khong dang tin khi tinh toan thu tu/cong thuc |
| `faithfulness` | **Python** (dem ty le) | Tranh "ngao toan" — LLM hay lam tron sai hoac tra ve string |
| `context_recall` | LLM + `clamp()` | LLM tot hon o viec so sanh ngu nghia theo ty le % |
| `answer_relevancy` | LLM + `clamp()` | Can kha nang doc hieu ngu canh cau hoi |
| `answer_correctness` | LLM + `clamp()` | Can kha nang doi chieu su that ngu nghia |

Ham `clamp(val)` dam bao moi diem so luon nam trong `[0.0, 1.0]`:

```python
def clamp(val: float) -> float:
    return max(0.0, min(1.0, float(val)))

# Vi du:
clamp(1.2)   # --> 1.0   (LLM tra ve > 1 do loi)
clamp(-0.1)  # --> 0.0   (LLM tra ve am)
clamp(0.83)  # --> 0.83  (binh thuong)
```
