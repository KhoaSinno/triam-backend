# Tài liệu Phân tích Chi tiết Luồng Điều hướng trong Grounding Router

Tài liệu này phân tích chi tiết nguyên lý hoạt động, luồng xử lý dữ liệu và cấu trúc mã nguồn của 3 nhánh định tuyến chính (`BOOK_METADATA`, `BOOK_SECTION`, `BOOK_RAG`) trong bộ điều hướng `GroundingRouter`.

---

## 1. Luồng Metadata Sách (`BOOK_METADATA`)

Luồng này phục vụ cho việc trả lời các câu hỏi về thông tin cấu trúc, tác giả, tựa đề, số chương, định dạng file hoặc trạng thái của sách. Luồng này **không truy cập vào nội dung chữ** của sách nên có độ trễ cực thấp và không tốn bộ nhớ ngữ cảnh.

### 1.1 Sơ đồ lớp & Dữ liệu
*   **Thực thể đầu vào**: `NormalizedQuery` (chứa câu hỏi đã chuẩn hóa).
*   **Cấu trúc dữ liệu đại diện**: `GroundingBook` (Contract chứa: `id: UUID`, `title: str`, `author: str | None`, `document_type: str | None`, `total_sections: int | None`, `root_section_count: int`, `status: str | None`).

### 1.2 Chi tiết các bước xử lý trong mã nguồn

1.  **Phân giải sách (Book Resolution)**:
    Hàm `resolve_metadata_book(scope, query)` trong [section_resolver.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/section_resolver.py#L26) thực hiện phân giải xem câu hỏi đang nhắm tới cuốn sách nào:
    *   Gọi `_named_books(scope, query)` để lọc sách theo tên được nhắc đến trong câu hỏi.
    *   Nếu trong `scope` học tập hiện tại chỉ có **duy nhất 1 cuốn sách**, hàm trả về kết quả khớp duy nhất với chất lượng `ResolutionQuality.UNIQUE` và mã lý do `single_book_scope`.
    *   Nếu có nhiều sách mà người dùng không chỉ rõ, hàm trả về chất lượng `ResolutionQuality.AMBIGUOUS` và yêu cầu học viên làm rõ (`clarification`).
2.  **Kết xuất câu trả lời xác định (Deterministic Answer)**:
    Hàm `render_metadata_answer(book, intent)` trong [response_renderer.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/response_renderer.py#L14) nhận đối tượng sách đã phân giải thành công và thực hiện sinh chuỗi tiếng Việt tĩnh:
    *   *Ví dụ (Ý định hỏi tác giả)*: `intent = GroundingIntent.BOOK_METADATA_AUTHOR` $\rightarrow$ Trả về: `f'Tác giả của "{book.title}" là {book.author}.'`
    *   *Ví dụ (Ý định hỏi trạng thái nạp)*: Ánh xạ trạng thái qua từ điển dịch `STATUS_LABELS` (ví dụ: `ready` $\rightarrow$ `"đã xử lý xong"`) $\rightarrow$ Trả về: `f'"{book.title}" đã xử lý xong.'`
3.  **Đóng gói gửi LLM**:
    Hàm `format_grounding_tool_result` đóng gói kết quả dưới dạng chuỗi có cấu trúc để trả về cho tool call của LLM:
    ```text
    BOOK_METADATA_FOUND:
    Tác giả của "Of Mice and Men" là John Steinbeck.
    ```

---

## 2. Luồng Đề mục cụ thể (`BOOK_SECTION`)

Luồng này kích hoạt khi học viên yêu cầu tóm tắt hoặc đọc nội dung của một chương hoặc mục lục cụ thể (Ví dụ: *"Tóm tắt chương 4"*). Hệ thống sẽ truy vấn toàn bộ văn bản của chương đó từ cơ sở dữ liệu và nạp vào ngữ cảnh của LLM.

### 2.1 Sơ đồ lớp & Dữ liệu
*   **Thực thể phân tích đề mục**: `SectionReference` (Trích xuất từ câu hỏi nhờ regex và quy đổi số viết chữ sang số điện tử).
*   **Cấu trúc dữ liệu DB**: Bảng `book_sections` lưu phân cấp đề mục, bảng `book_section_knowledge` lưu các đoạn text tương ứng của mục đó.

### 2.2 Chi tiết các bước xử lý trong mã nguồn

1.  **Tìm kiếm đề mục khớp mục tiêu**:
    Hàm `resolve_section(scope, query, reference)` trong [section_resolver.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/section_resolver.py#L183) tìm đề mục đích:
    *   Nếu khớp số thứ tự chương (ví dụ: `"chương 4"` $\rightarrow$ `explicit_ordinal = 4`): Hàm `_ordinal_candidates` lọc ra các chương gốc (chương cấp 1, không có `parent_id`) và trả về chương tương ứng tại chỉ mục số 4.
    *   Nếu khớp trực tiếp đường dẫn (ví dụ: mục `"4.1"` $\rightarrow$ `explicit_path = "4.1"`): Tìm đề mục có `path == "4.1"`.
2.  **Truy vấn đệ quy lấy toàn bộ mục con (Descendant Section IDs)**:
    Do một chương lớn có thể chứa nhiều đề mục con nhỏ bên trong (Ví dụ: Chương 4 chứa mục 4.1, 4.2...), hàm `descendant_section_ids(scope, target_section_id)` sẽ quét đệ quy cấu trúc hình cây của sách để lấy ra **tất cả ID của mục gốc và mục con cháu** nằm dưới nó.
3.  **Nạp văn bản từ Database**:
    Gọi hàm nạp `section_text_loader(book_id, section_ids)` để thực hiện truy vấn SQL:
    ```sql
    SELECT id, section_id, path, title, text_content, section_index 
    FROM book_section_knowledge 
    WHERE book_id = :book_id AND section_id IN :section_ids
    ORDER BY section_index ASC
    ```
4.  **Nối và tối ưu hóa ngữ cảnh (Build Context)**:
    Hàm `build_section_context` trong [section_context_builder.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/section_context_builder.py#L46) thực hiện gộp văn bản:
    *   **Loại bỏ trùng lặp (Deduplication)**: Sử dụng hàm `_dedupe_rows` loại bỏ các đoạn text giống nhau.
    *   **Định dạng chuỗi (Formatting)**: Nối các đoạn văn bản kèm theo tiêu đề đường dẫn dạng Markdown:
        ```text
        [4 Chapter 4]
        Lennie sat in the barn...
        ```
    *   **Phân bổ hạn ngạch ký tự công bằng (Fair Share Allocation)**: Để ngăn chặn mục con đầu tiên quá dài chiếm hết giới hạn ký tự làm các mục con sau bị mất hoàn toàn, hàm chia đều dung lượng cho các mục: `fair_share = remaining // remaining_rows`.
    *   *Cơ chế kiểm soát độ dài*: Để tránh làm tràn bộ nhớ ngữ cảnh của LLM (Context Window Overflow), hàm sẽ giới hạn độ dài ký tự tối đa `max_chars = 16000` (được cấu hình qua biến `AGENT_SECTION_CONTEXT_MAX_CHARS` trong cấu hình hệ thống `Settings`). Nếu văn bản của toàn bộ chương và các mục con vượt quá 16,000 ký tự (khoảng 3,000 - 4,000 từ), hệ thống sẽ tự động cắt ngắn và chèn thêm nhãn `...[truncated]`.
*   **Bước 3: Định dạng gửi cho LLM**:
    ```text
    BOOK_SECTION_FOUND:
    BOOK_SECTION_CONTEXT
    Book: "Of Mice and Men"
    Target section: 4 - Chapter 4

    [4 Chapter 4]
    Lennie sat in the barn looking at a little dead puppy...
    ...
    Answer only from this section context. Do not use model memory or request web search.
    ```

---

## 3. Luồng RAG Ngữ nghĩa (`BOOK_RAG`)

Luồng này kích hoạt khi học viên hỏi các câu hỏi ngữ nghĩa tự do trên toàn cuốn sách (Ví dụ: *"George gặp Lennie trong hoàn cảnh nào?"*). Hệ thống thực hiện tìm kiếm lai (Hybrid Search) và xếp hạng lại (Reranking).

### 3.1 Sơ đồ lớp & Dữ liệu
*   **Thực thể xử lý**: `search_book_hybrid_knowledge` trong [rag_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/rag_service.py#L117).
*   **Công cụ bên ngoài**: Cohere Rerank API (v2).

### 3.2 Chi tiết các bước xử lý trong mã nguồn

1.  **Tìm kiếm lai song song (Parallel Hybrid Search)**:
    Hệ thống sử dụng `asyncio.gather` kích hoạt song song 2 tác vụ để tối ưu thời gian phản hồi:
    *   **Nhánh Vector (Dense Search)**: Gọi `search_book_section_knowledge` thực hiện truy vấn khoảng cách cosine của vector embedding câu hỏi (1536 chiều) trên cột `embedding` (đã đánh chỉ mục HNSW/IVFFlat pgvector) trong DB.
    *   **Nhánh Từ khóa (Lexical Search)**: Gọi `search_book_section_knowledge_lexical` truy vấn Full-Text Search của PostgreSQL dựa trên khớp từ vựng của câu hỏi.
2.  **Xếp hạng lai thô (Hybrid Fusion)**:
    Hàm `build_hybrid_retrieval_result` kết hợp kết quả từ hai nhánh truy vấn bằng thuật toán xếp hạng lai (Reciprocal Rank Fusion - RRF hoặc tương tự) để chọn ra 20 ứng cử viên tốt nhất.
3.  **Tái xếp hạng chính xác bằng Cohere (Reranking)**:
    Đưa 20 ứng cử viên qua hàm `rerank_candidates` sử dụng API Cohere Reranker:
    *   Cohere tính toán chính xác điểm tương hợp ngữ nghĩa giữa câu hỏi và các đoạn text.
    *   Hệ thống lọc lấy tối đa 12 đoạn tốt nhất đạt điểm số tối thiểu trên ngưỡng quy định.
4.  **Đóng gói gửi LLM**:
    Nối các đoạn đã được rerank lại thành một khối ngữ cảnh có cấu trúc kèm theo ID để OpenAI Realtime tự do đọc hiểu và đưa ra câu trả lời cuối cùng.