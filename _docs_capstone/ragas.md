Dưới đây là lời giải thích chi tiết, minh bạch và chuẩn học thuật về cơ chế chấm điểm của bộ công cụ RAGAS trong tệp [`tests/eval_llm_as_judge.py`](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/eval_llm_as_judge.py):

---

### 1. BẢN CHẤT CỦA TRƯỜNG `contexts` TRONG DỮ LIỆU
* **Thực tế trong kiến trúc RAG của TRIAM:** `contexts` là một mảng (array) chứa **toàn bộ văn bản thô của các chunks** (mỗi chunk chứa khoảng 300–500 từ thuộc các `BookSection`) được Hybrid Search (Vector + Full-text) và Cohere Reranker v2 trích xuất và xếp hạng Top-K (thường K=3).
* **Trong tệp [`production_flow_trace.json`](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/logs/ragas_eval/production_flow_trace.json) hiện tại:** Trường `contexts` đang lưu đoạn ngữ cảnh chuẩn (Ground truth context) để đại diện cho tri thức của câu hỏi đó. 
* **Đưa cho LLM toàn bộ ngữ cảnh hay không?** $\rightarrow$ **CÓ!** Khi đánh giá, toàn bộ danh sách các chuỗi văn bản chunks trong `contexts` được nối lại (`"\n---\n".join(contexts)`) và gửi nguyên vẹn vào prompt cho LLM Judge để đối soát.

---

### 2. CƠ CHẾ CHẤM ĐIỂM: CÔNG THỨC HAY ĐỦ CHO LLM TỰ CHẤM?

Bộ chỉ số RAGAS sử dụng phương pháp **LLM-as-a-Judge** (dùng mô hình LLM độc lập như Gemini 3.5 Flash / GPT-4o để chấm điểm), kết hợp giữa **Phân rã Logic (Decomposition)** và **Công thức Toán học (MAP / Recall Ratio)**.

Chi tiết cơ chế chấm điểm từng chỉ số trong [`tests/eval_llm_as_judge.py`](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/eval_llm_as_judge.py):

#### 🔹 **1. Faithfulness (Độ trung thực - Chống ảo giác)**
* **Phương pháp:** LLM tự phân rã và chấm theo công thức.
* **Cách thực hiện:** 
  1. LLM Judge nhận `contexts` (văn bản nguồn) và `response` (câu trả lời của AI).
  2. LLM bóc tách `response` thành các khẳng định nhỏ độc lập (**atomic claims**).
  3. LLM đối soát từng khẳng định xem có căn cứ trực tiếp trong `contexts` hay không ($v_i = 1$ nếu có, $v_i = 0$ nếu ảo giác).
  4. Điểm số tính theo công thức:
     $$\text{Faithfulness} = \frac{\text{Số mệnh đề được hỗ trợ bởi Contexts}}{\text{Tổng số mệnh đề bóc tách trong Response}}$$

---

#### 🔹 **2. Answer Relevancy (Độ liên quan trọng tâm)**
* **Phương pháp:** LLM chấm mức độ phù hợp.
* **Cách thực hiện:** 
  1. LLM Judge nhận `user_input` (câu hỏi) và `response` (câu trả lời).
  2. LLM đánh giá xem câu trả lời có đi thẳng vào trọng tâm câu hỏi hay không, có bị lan man, lạc đề hoặc trả lời dông dài hay không.
  3. LLM xuất ra tỷ lệ chấm điểm từ `0.0` đến `1.0`.

---

#### 🔹 **3. Context Recall (Độ bao phủ tri thức)**
* **Phương pháp:** LLM phân tích ý chính và tính tỷ lệ bao phủ.
* **Cách thực hiện:** 
  1. LLM Judge nhận `reference` (đáp án chuẩn) và `contexts` (ngữ cảnh RAG trích xuất).
  2. LLM phân rã `reference` thành các ý chính (key facts).
  3. LLM kiểm tra xem bao nhiêu % ý chính đó xuất hiện trong `contexts`.
  4. Điểm số tính theo công thức:
     $$\text{Context Recall} = \frac{\text{Số ý chính trong Đáp án chuẩn có mặt trong Contexts}}{\text{Tổng số ý chính của Đáp án chuẩn}}$$

---

#### 🔹 **4. Context Precision (Độ chính xác Cohere Reranker)**
* **Phương pháp:** LLM gắn nhãn mức độ liên quan của từng Chunk + Công thức xếp hạng MAP@K (Mean Average Precision).
* **Cách thực hiện:** 
  1. Với danh sách $K$ chunks do Cohere Reranker trả về theo thứ tự từ $1$ đến $K$.
  2. LLM Judge duyệt qua từng chunk $k$ và xác định nhãn $v_k \in \{0, 1\}$ ($1$ nếu chunk chứa thông tin trả lời, $0$ nếu rác/không liên quan).
  3. Điểm số tính theo công thức MAP@K:
     $$\text{Context Precision@K} = \frac{\sum_{k=1}^{K} \left( \text{Precision@k} \times v_k \right)}{\text{Tổng số chunks có liên quan trong Top K}}$$
     *Trong đó:* $\text{Precision@k} = \frac{\text{Số chunks liên quan trong Top } k}{k}$.
     *(Công thức này thưởng điểm rất cao nếu Cohere Reranker đẩy chunk đúng lên vị trí Top 1).*

---

#### 🔹 **5. Answer Correctness (Độ chính xác nội dung thực tế)**
* **Phương pháp:** LLM so sánh ngữ nghĩa thực tế.
* **Cách thực hiện:** 
  1. LLM Judge nhận `user_input`, `reference` (đáp án chuẩn) và `response` (câu trả lời thực tế).
  2. LLM so sánh độ khớp dữ kiện lịch sử/khoa học/khái niệm giữa câu trả lời thực tế và đáp án chuẩn để đưa ra điểm số từ `0.0` đến `1.0`.

---

### 💡 **TÓM LẠI CHO BÁO CÁO LUẬN VĂN:**
- **Không phải LLM "chấm cảm tính":** LLM đóng vai trò là bộ trích xuất mệnh đề/ý chính (Extractor & Classifier), sau đó kết quả được tổng hợp theo **công thức toán học định lượng RAGAS**.
- **Toàn bộ ngữ cảnh thô** (Full RAG Chunks) được truyền thẳng vào prompt cho LLM Judge để kiểm tra sự thật (Grounding verification).