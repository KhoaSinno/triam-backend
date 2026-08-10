Để thuyết trình slide **"Tổng kết: Evaluation với RAGAS framework"** một cách ấn tượng, khoa học và thuyết phục trước Hội đồng Bảo vệ Luận văn/Đồ án, bạn nên chia bài nói thành **2 phần chính (Hiệu năng độ trễ $\rightarrow$ Chất lượng RAGAS & Ablation)** với thời lượng lý tưởng từ **60 đến 90 giây**.

Dưới đây là **kịch bản thuyết trình từng lời (Speech Script)** cùng **dự đoán các câu hỏi phản biện từ Hội đồng** để bạn tự tin làm chủ slide này:

---

### 🎙️ Kịch bản thuyết trình chi tiết (Thuyết minh 60-90s)

> **[Lời mở đầu slide]**
> *"Kính thưa Hội đồng, để chứng minh tính khả thi và hiệu quả của hệ thống, nhóm chúng em đã tiến hành đánh giá thực nghiệm toàn diện trên 60 ca đàm thoại giọng nói thực tế thuộc 3 miền tri thức (Văn học, CNTT và Tài chính) dựa trên hai trụ cột: **Hiệu năng độ trễ vận hành** và **Chất lượng truy xuất RAGAS**."*

> **[Nhóm 1: Thuyết minh Hàng trên - Hiệu năng độ trễ (P50 & TTFA)]**
> *"Về phía hiệu năng máy chủ (như thể hiện ở hàng trên):*
> 1. *Bộ phân loại ý định **Semantic Router** chạy cục bộ tại Agent cho độ trễ trung vị $P_{50}$ chỉ **$29\text{ ms}$**, giúp định tuyến tức thì câu hỏi của người học mà không tốn chi phí gọi LLM lớn.*
> 2. *Luồng truy xuất tri thức **Retrieval RAG** kết hợp Hybrid Search và mô hình Cohere Reranker đạt độ trễ $P_{50}$ là **$1493\text{ ms}$** ($\sim 1,5\text{ giây}$).*
> 3. *Nhờ đó, tổng độ trễ phát ra âm thanh phản hồi đầu tiên — **TTFA (Time To First Audio)** — trong môi trường đàm thoại WebRTC thực tế dao động mượt mà từ **$1,8$ đến $2,5\text{ giây}$**, đảm bảo trải nghiệm giao tiếp tự nhiên rảnh tay cho người học."*

> **[Nhóm 2: Thuyết minh Hàng dưới - Đánh giá RAGAS & Ablation Study]**
> *"Về phía chất lượng câu trả lời (như thể hiện ở hàng dưới):*
> 1. *Nhóm áp dụng khung **RAGAS** theo phương pháp **LLM-as-a-Judge** để đánh giá bám nguồn. Kết quả đạt các chỉ số tích cực: độ liên quan câu trả lời (**Answer Relevancy**) đạt **$0,81$**, độ chính xác (**Answer Correctness**) đạt **$0,77$** và độ trung thực bám sát ngữ cảnh (**Faithfulness**) đạt **$0,68$**.*
> 2. *Đặc biệt, qua **Ablation Study (Thử nghiệm triệt tiêu)** đối chiếu giữa BM25 từ khóa, Vector Search thuần túy và Hybrid RAG, kết quả chứng minh việc kết hợp cả hai phương pháp cùng mô hình Reranker giúp tăng vượt trội khả năng chọn lọc tri thức và loại bỏ triệt để hiện tượng ảo giác thông tin."*

> **[Lời chốt slide]**
> *"Những số liệu này khẳng định hệ thống vừa đạt độ trễ phản hồi giọng nói mượt mà, vừa đảm bảo tính chính xác và trung thực cao của tri thức trả về."*

---

### 💡 3 Câu hỏi Phản biện Hội đồng hay hỏi nhất (và cách trả lời)

#### ❓ Câu hỏi 1: *"TTFA (Time To First Audio) là gì và tại sao TTFA từ 1.8 - 2.5s lại được coi là ấn tượng đối với Voice Assistant?"*
* **Trả lời:** 
  > *"Dạ thưa Thầy/Cô, TTFA là khoảng thời gian tính từ lúc người dùng vừa dứt lời đến khi âm thanh giọng nói của trợ lý AI bắt đầu phát ra từ loa. Trong các hệ thống Voice AI truyền thống (STT $\rightarrow$ LLM $\rightarrow$ TTS), độ trễ thường từ $4 - 6\text{s}$. Hệ thống của nhóm sử dụng chuẩn kết nối thời gian thực WebRTC kết hợp OpenAI Realtime API streaming âm thanh dạng chunk, giúp giảm tổng thời gian chờ xuống còn $1.8 - 2.5\text{s}$, tạo cảm giác hội thoại nối tiếp tự nhiên như giao tiếp giữa người với người."*

#### ❓ Câu hỏi 2: *"Tại sao điểm Context Precision lại thấp hơn các chỉ số khác (đạt khoảng 0.36)?"*
* **Trả lời:**
  > *"Dạ thưa Thầy/Cô, đặc thù dữ liệu đầu vào của hệ thống là các cuốn sách chuyên ngành có độ dài lớn. Khi tạo vector embedding, nhóm chia chunk kích thước $3.600$ ký tự kèm $500$ ký tự chồng lấp để bảo toàn ngữ cảnh đoạn sách. Do kích thước chunk lớn nên thông tin trực tiếp phục vụ câu hỏi chỉ chiếm một phần trong chunk đó, dẫn đến điểm Context Precision bị giảm. Tuy nhiên, điểm Answer Relevancy ($0,81$) và Answer Correctness ($0,77$) vẫn rất cao, chứng tỏ mô hình LLM đã trích xuất đúng trọng tâm thông tin từ các chunk được cung cấp."*

#### ❓ Câu hỏi 3: *"Tại sao phải thực hiện Ablation Study (Thử nghiệm triệt tiêu) cho phần Retrieval?"*
* **Trả lời:**
  > *"Dạ thưa Thầy/Cô, Ablation Study giúp chứng minh vai trò không thể thay thế của từng thành phần: Nếu chỉ dùng BM25 từ khóa sẽ bị bỏ sót câu hỏi đồng nghĩa; nếu chỉ dùng Vector Search thuần túy sẽ dễ bắt sai thuật ngữ chuyên ngành; và việc kết hợp Hybrid Search (BM25 + pgvector + RRF) cùng Cohere Reranker mang lại điểm số bám nguồn cao nhất và ổn định nhất."*

---

### 🎨 Mẹo trình bày thêm trên Slide (nhỏ nhưng ghi điểm):
* Phần **TTFA ($1.8-2.5\text{ s}$)** và **RAGAS ($0.81$)** là hai "ngôi sao" của slide, khi nói bạn có thể dùng con trỏ laser hoặc khoanh vùng nhấn mạnh vào 2 ô này.
* Giữ phong thái tự tin, nói rõ ràng các thuật ngữ viết tắt ($P_{50}$, TTFA, Hybrid RAG, RAGAS, Ablation).