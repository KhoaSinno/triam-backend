# RAG Advance - Đề xuất tối ưu RAG (GỢI ý từ agent)

### Giai đoạn 1 [DONE]: Làm giàu dữ liệu (Data Enrichment & Smart Chunking)

Đừng chỉ coi mỗi chunk là một đoạn văn bản thô. Hãy biến nó thành một "đơn vị tri thức" có đầy đủ bối cảnh.

1.  **Metadata Injection:** Khi lưu vào Supabase, mỗi chunk ngoài `content` và `embedding` cần có thêm:
    - `chapter_title`: Tên chương (giúp AI biết đoạn này thuộc chủ đề lớn nào).
    - `summary_context`: Một câu tóm tắt cực ngắn của chương đó.
2.  **Overlapping & Header:** Khi cắt chunk (ví dụ 1000 ký tự), hãy để overlap khoảng 200 ký tự. Đặc biệt, hãy luôn đính kèm tiêu đề chương vào đầu mỗi chunk trước khi tạo Embedding.
    - _Ví dụ:_ Thay vì "Bạn ấy nói...", hãy lưu là "[Chương 1: Sự tự lừa dối] Bạn ấy nói...". Điều này giúp Vector "ám thị" được ngữ cảnh của chương đó.

### Giai đoạn 2: Công nghệ tìm kiếm lai (Hybrid Search)

Như đã phân tích, Vector Search rất kém trong việc tìm từ khóa chính xác (như tên riêng "Eran Katz"). Em cần kết hợp sức mạnh của PostgreSQL.

1.  **Full-text Search (FTS):** Tận dụng tính năng `tsvector` của Postgres.
2.  **Kết hợp trong RPC:** Sửa lại hàm RPC để tìm kiếm bằng cả Vector lẫn Từ khóa.
3.  **RRF (Reciprocal Rank Fusion):** Đây là thuật toán để gộp kết quả từ 2 nguồn này lại. Những đoạn văn nào xuất hiện trong cả top Vector và top Keyword sẽ được đẩy lên đầu.

### Giai đoạn 3: Tinh chỉnh câu hỏi (Query Expansion & Rewriting)

Đây là phần em đang quan tâm. Để giải quyết vấn đề latency và token, hãy dùng kiến trúc **Small-to-Big**.

1.  **Context-Aware Rewrite:** Sử dụng một model cực rẻ (Gemini 2.5 Flash) để viết lại câu hỏi dựa trên tiêu đề sách.
2.  **HyDE (Hypothetical Document Embeddings):** Thay vì tìm kiếm bằng câu hỏi của user, hãy bảo AI: _"Hãy viết một đoạn trả lời giả định cho câu hỏi này"_. Sau đó dùng chính đoạn trả lời giả định đó để đi search Vector. Kết quả sẽ khớp hơn rất nhiều so với dùng câu hỏi gốc.

### Giai đoạn 4: Đánh giá và Tái xếp hạng (Reranking)

Sau khi lấy ra được top 10-15 đoạn văn từ Database, đừng đưa hết vào cho Gemini trả lời ngay.

1.  **Cross-Encoder Reranker:** Sử dụng một model rerank nhỏ (như của Cohere hoặc tự dựng một script Python nhẹ) để tính điểm lại độ liên quan giữa câu hỏi và 15 đoạn văn đó.
2.  **Top-K Selection:** Chỉ lấy ra 3-5 đoạn có điểm cao nhất sau khi rerank để đưa vào Prompt cuối cùng. Điều này giúp giảm nhiễu và tiết kiệm token cho model chính.
