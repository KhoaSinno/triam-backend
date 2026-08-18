#### 1. Về Kiến trúc & Hiệu năng thời gian thực (Architecture & Realtime):
> *"Tại sao nhóm lại tách biệt luồng nghiệp vụ REST API (FastAPI) và luồng đàm thoại giọng nói (LiveKit WebRTC + OpenAI Realtime)? Tại sao không dùng WebSocket truyền thống kết nối trực tiếp từ Mobile tới Server FastAPI?"*

Khi dùng WebSocket truyền thống thì nhóm sẽ tự cấu hình khá là nhiều và nhiều vấn đề sẽ xảy ra về việc tương thích với các api từ bên thứ 3 cung cấp, nhóm quyết định chọn LiveKit bởi vì đó là một framework mã nguồn mở và hỗ trợ khá về về việc xử lý âm thanh ở phần hạ tầng. Giúp nhóm tiết kiệm thời gian trong quá trình nghiên cứu và chạy thử pipeline. WebSocket hoạt động trên nền giao thức TCP, WebRTC chạy trên nền UDP.

#### 2. Về Giải thuật Tìm kiếm lai (Hybrid RAG & Ranking):
> *"Tại sao nhóm phải kết hợp Dense Vector (pgvector) với Lexical Search (BM25)? Giải thích công thức Reciprocal Rank Fusion (RRF) và vai trò của Cohere Reranker trong quy trình này?"*

Trong học thuật thì sẽ có những thuật ngữ, việc map keyword sẽ không thể chính xác cao đối với semantic search, nên nhóm dùng lexical search BM25 để bố sung các chunk có giá trị về mặc thuật ngữ keyword thay vì gôm ứng cử viên gần đúng trong phạm vi.

RRF là cách để merge nhiều ứng cử viên từ nhiều giải pháp mà ko quan tâm đến việc giá trị xếp hạng của nó là bao nhiêu. RRF sẽ tính dựa vào công thức 1/ 60 + vị trí index của phần từ đó trong mỗi cách tính. Với index được bắt đầu từ 1, nếu phần tử đó không có trong tập thì sẽ có giá trị vô cực.

Vai trò của corehere là để rerank lại sau bước sử dụng RRF để merge, RRF chỉ merge và không đảm bảo được giá trị sẽ được trắc lọc tốt nhất, nếu không rerank sẽ tồn tại nhiều giá trị nhiễu chưa đc sắp xếp và lọc bỏ. Cohere Reranker đóng vai trò là một Cross-Encoder nhận đồng thời cả cặp (Câu hỏi, Đoạn trích).

#### 3. Về Cơ chế Chống ảo giác & Định tuyến (Grounding & Guardrails):
> *"Khi người dùng hỏi một câu không có trong sách hoặc hỏi thông tin thời sự bên ngoài, hệ thống xử lý như thế nào để vừa chống ảo giác (hallucination) vừa hỗ trợ người dùng linh hoạt?"*

Nếu câu hỏi không có trong sách thì câu hỏi đó được đánh nhãn là external thì agent yêu cầu quyền từ user để search Internet. 

#### 4. Về Tính nhất quán dữ liệu & Lập lịch thông báo (Distributed Systems & Outbox):
> *"Tại sao nhóm áp dụng Transactional Outbox Pattern kết hợp Celery Beat và cơ chế `FOR UPDATE SKIP LOCKED` cho chức năng nhắc nhở học tập và ôn tập SM-2? Nếu không dùng pattern này thì hệ thống sẽ gặp rủi ro gì?"*

Nếu không dùng pattern này thì sẽ xảy ra nhiều worker có thể cùng ghi vào 1 bảng làm sai lệch data. Tránh việc tranh chấp và gây nghẽn. 


#### 5. Về Đánh giá thực nghiệm & Số liệu (RAGAS Metrics):
> *"Trong Bảng đánh giá RAGAS của nhóm, tại sao chỉ số Faithfulness đạt $0.6818$ và Context Precision là $0.3586$, trong khi Answer Relevancy lại đạt tới $0.8133$? Nhóm giải thích như thế nào về sự chênh lệch này trước hội đồng?"*
 
> 1. **Answer Relevancy ($0.8133$) và Answer Correctness ($0.7695$):** Đạt điểm cao vì câu trả lời của trợ lý đi thẳng vào trọng tâm câu hỏi của người học và có ngữ nghĩa chính xác so với đáp án tham chiếu.
> 2. **Chỉ số Faithfulness ($0.6818$):** Cho thấy phần lớn câu trả lời bám sát ngữ cảnh tài liệu, tuy nhiên đôi khi LLM vẫn bổ sung một số từ nối tự nhiên hoặc tri thức nền để câu nói mạch lạc hơn khi phát âm qua giọng đọc thoại.
> 3. **Giải thích về Context Precision ($0.3586$):** Để phục vụ việc sinh âm thanh TTS mượt mà và giữ trọn vẹn lập luận của bài giảng, hệ thống chia chunk tài liệu với kích thước mục tiêu là **3.600 ký tự (overlap 500 ký tự)**. Kích thước chunk lớn này giúp bài học hoàn chỉnh ngữ cảnh, nhưng khi đưa vào RAGAS, một chunk dài sẽ chứa nhiều thông tin bối cảnh xung quanh (*surrounding context*) bên cạnh câu trả lời trực tiếp, khiến chỉ số Context Precision bị giảm xuống.
> 4. **Hướng phát triển:** Nhóm giữ sự trung thực khoa học trong báo cáo và đề xuất giải pháp cải tiến trong tương lai là áp dụng kỹ thuật **Parent Document Retriever (Small-to-Big Retrieval)**: Dùng chunk nhỏ 300-500 ký tự để tìm kiếm đạt Precision tối đa, sau đó mới nạp Parent Chunk lớn vào context để trả lời."


---

👉 **Bạn muốn tự trả lời trước câu nào (ví dụ Câu 1), hay muốn tôi phân tích chi tiết lần lượt từng câu?** Hãy cho tôi biết nhé!