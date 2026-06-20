# Hướng dẫn Bắt đầu dành cho Nhà phát triển mới (TRIAM Codebase Onboarding & Architecture Guide)

Chào mừng bạn đến với dự án **TRIAM Backend**. Tài liệu này được thiết kế dành riêng cho các lập trình viên mới (onboarding developers) chưa biết gì về hệ thống, giúp bạn tiếp cận và hiểu toàn bộ mã nguồn một cách nhanh chóng, bài bản và thực chiến nhất.

---

## 1. Bức tranh Tổng thể (The Big Picture)

### TRIAM là gì?
TRIAM (Tri Âm) là ứng dụng hỗ trợ học tập thông minh. Khác với trình đọc sách thông thường, TRIAM chuyển đổi sách/tài liệu (PDF, EPUB, DOCX) thành **sách nói tương tác** có khả năng:
1.  **AI Audiobook**: AI tự động đọc và biên soạn tóm tắt kiến thức (TTS).
2.  **Lập lộ trình cá nhân hóa**: Học chi tiết (`DETAILED`) hoặc học tinh gọn theo nguyên lý 80/20 (`PARETO`).
3.  **Realtime Voice Agent**: Cho phép người dùng vừa nghe sách vừa nói chuyện trực tiếp với trợ lý AI giọng nói (độ trễ cực thấp qua LiveKit) để thảo luận về cuốn sách, giải bài tập, hoặc tìm kiếm ngữ cảnh.
4.  **Ôn tập ngắt quãng**: Tự động sinh thẻ ôn tập theo chu kỳ SuperMemo SM-2 và gửi thông báo đẩy (push notifications).

---

## 2. Kiến trúc Công nghệ & Mô hình Thiết kế (Tech Stack & Pattern)

### 2.1 Công nghệ cốt lõi
*   **Ngôn ngữ**: Python 3.11+.
*   **Web Framework**: FastAPI (hỗ trợ async/await, tự động sinh tài liệu OpenAPI `/docs`).
*   **ORM (Kết nối CSDL)**: SQLModel (sự kết hợp giữa Pydantic và SQLAlchemy).
*   **CSDL**: PostgreSQL + phần mở rộng `pgvector` (để lưu trữ vector 1536 chiều).
*   **Task Queue (Xử lý tác vụ nặng)**: Celery + Redis broker (xử lý parse tài liệu, sinh audio TTS ngầm).
*   **Realtime Streaming**: LiveKit Agents (kết nối luồng âm thanh hai chiều trực tiếp).
*   **AI Models**: OpenAI (GPT-4o-mini, text-embedding-3-small) và Gemini (gemini-2.5-flash).

### 2.2 Cấu trúc Thư mục và Luồng đi của dữ liệu
Hệ thống tuân thủ mô hình **Clean Architecture** được chia lớp rõ ràng từ ngoài vào trong:

```
[Client/Frontend]
       │
       ▼ (Request)
[Routers (app/api/)] ───> Kiểm tra Token, nhận Pydantic Schemas (app/schemas/)
       │
       ▼
[Services (app/services/)] ───> Thực hiện logic nghiệp vụ chính (Business Logic)
       │
       ▼
[Repositories (app/repositories/)] ───> Viết các câu lệnh truy vấn SQL (Data Access)
       │
       ▼
[Models (app/models/)] ───> Ánh xạ cấu trúc bảng CSDL (SQLModel)
       │
       ▼
[PostgreSQL Database]
```

---

## 3. Lộ trình Từng bước để Đọc và Hiểu Code (Step-by-Step Code Walkthrough)

Để không bị ngợp giữa hàng chục file code, bạn hãy đọc mã nguồn theo đúng thứ tự 6 bước sau đây:

### Bước 1: Đọc và hiểu Sơ đồ thực thể dữ liệu (The Schema Root)
*   **File cần đọc**: [db_models.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/models/db_models.py).
*   **Mục tiêu**: Đây là xương sống của toàn dự án. Bạn cần nắm rõ 8 phân hệ chính:
    *   *Người dùng*: `User`, `AdminUser`, `NotificationSettings`.
    *   *Sách & cấu trúc*: `Book`, `BookSection`, `BookSectionKnowledge`.
    *   *Kế hoạch & Lịch trình*: `ReadingPlan`, `ReadingPlanScheduleSlot`.
    *   *Phiên học thực tế*: `ReadingPlanSession`, `ReadingPlanSessionUnit`.
    *   *Bài học audio*: `LearningUnit`, `LearningUnitSegment`, `LearningUnitSource`.
    *   *Tiến độ*: `LearningUnitProgress`, `BookLearningState`.
    *   *Thảo luận chat*: `StudyContext`, `ChatThread`, `ChatMessage`, `DirectBookContext`.
    *   *Thông báo*: `NotificationOutbox`, `UserNotification`.

### Bước 2: Tìm hiểu Luồng tải lên và Xử lý tài liệu ngầm (Asynchronous Document Pipeline)
*   **File cần đọc**:
    1.  [app/api/v1/audiobook.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/audiobook.py): Xem API nhận file sách.
    2.  [app/services/upload_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/upload_service.py): Xem API lưu trữ file tạm.
    3.  [app/tasks/book_tasks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/tasks/book_tasks.py): Đây là Celery Task. Đọc hàm `process_book_upload_task()`.
*   **Giải thích luồng**:
    ```
    Upload File ──> Lưu Supabase Storage ──> Đẩy Task vào Celery ──> Parse mục lục (PDF/EPUB) 
    ──> Chia nhỏ văn bản (Chunking) ──> Gọi OpenAI tạo Embeddings ──> Lưu vào `book_section_knowledge`.
    ```

### Bước 3: Tìm hiểu Bộ hoạch định Lộ trình học (The Plan Generator)
*   **File cần đọc**:
    1.  [learning_unit_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/learning_unit_planner_service.py).
    2.  [pareto_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pareto_planner_service.py).
*   **Mục tiêu**:
    *   Xem cách hệ thống tính toán token bằng `estimate_text_budget`.
    *   Hiểu logic chia nhỏ/gộp chương sách (`split_large_chapters` / `merge_tiny_chapters`).
    *   Đọc prompt gửi cho Gemini (`PARETO_PLANNER_SYSTEM_PROMPT`) để hiểu cách AI chấm điểm chọn lọc 20% kiến thức cốt lõi.

### Bước 4: Xem luồng Ghi nhận tiến độ nghe và Lập lịch học hàng ngày (Scheduler & Progress)
*   **File cần đọc**:
    1.  [learning_progress_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/learning_progress_service.py): Hàm `update_learning_unit_progress()`.
    2.  [reading_plan_session_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/reading_plan_session_service.py): Hàm `ensure_future_sessions_for_plan()`.
*   **Mục tiêu**:
    *   Hiểu cách tính phần trăm nghe (`_compute_progress_percent`) dựa trên segment index.
    *   Hiểu cơ chế hoàn thành bài nghe (ngưỡng 80%) và tự động kích hoạt tạo lịch ôn tập ngắt quãng.
    *   Hiểu cách tính toán ngày học tiếp theo dựa trên múi giờ (timezone) của người dùng.

### Bước 5: Tìm hiểu Trợ lý giọng nói thời gian thực (Realtime Voice Agent - LiveKit)
*   **File cần đọc**:
    1.  [app/services/agent_voice_gpt_realtime.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py).
    2.  [app/services/rag_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/rag_service.py).
*   **Mục tiêu**:
    *   Hiểu cách thiết lập kênh truyền âm thanh WebRTC thông qua LiveKit.
    *   Hiểu cách Agent gọi công cụ RAG (`search_book_knowledge`).
    *   Xem luồng Tìm kiếm hỗn hợp Hybrid RAG (kết hợp vector tìm kiếm ngữ nghĩa pgvector + tìm kiếm từ khóa lexical matching).

### Bước 6: Xem Cơ chế ôn tập ngắt quãng và Gửi thông báo an toàn (Outbox Notification)
*   **File cần đọc**:
    1.  [spaced_review_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/spaced_review_service.py).
    2.  [notification_event_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/notification_event_service.py).
*   **Mục tiêu**:
    *   Hiểu giải thuật tạo 5 mốc thời gian ôn tập lùi dần `[1, 3, 7, 14, 30]` ngày.
    *   Hiểu cơ chế **Outbox Pattern**: thay vì gọi FCM trực tiếp làm nghẽn luồng API, hệ thống ghi bản ghi pending vào bảng `notification_outbox`, sau đó worker định kỳ sẽ quét và thực hiện gửi tin nhắn ngầm.

---

## 4. Các Kinh nghiệm Thực chiến để Đọc hiểu nhanh Codebase

### 1. Bắt đầu từ Unit Tests
*   Nếu bạn chưa biết cách sử dụng một hàm, hãy mở thư mục [tests/](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/) ra đọc.
*   Ví dụ: File `tests/services/test_book_section_chunker.py` sẽ chỉ ra chính xác các tham số truyền vào hàm chunking và cấu trúc kết quả đầu ra. Chạy thử test bằng lệnh:
    ```powershell
    uv run pytest tests/services/test_book_section_chunker.py
    ```

### 2. Sử dụng tài liệu OpenAPI tương tác
*   Khởi chạy server local:
    ```powershell
    uv run uvicorn app.main:app --reload
    ```
*   Truy cập đường dẫn: [http://localhost:8000/docs](http://localhost:8000/docs)
*   Tại đây, bạn có thể chạy thử trực tiếp (Try it out) các API của người dùng và quản trị viên, xem luồng đi thực tế của dữ liệu JSON đi vào và đi ra.

### 3. Đọc các tài liệu thiết kế hệ thống có sẵn
*   Dự án có lưu trữ các tài liệu kiến trúc chất lượng cao, hãy đọc chúng trước khi viết code:
    *   Báo cáo cấu trúc bảng chi tiết: [db_architecture_report.md](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/_docs_capstone/_doc_core_feat/db_architecture_report.md)
    *   Báo cáo giải đáp thắc mắc CSDL: [db_architecture_qna.md](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/_docs_capstone/_doc_core_feat/db_architecture_qna.md)
    *   Đặc tả các hàm nghiệp vụ chính: [class_methods_report.md](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/_docs_capstone/_doc_core_feat/class_methods_report.md)

---

## 5. Danh sách Thuật ngữ Chuyên ngành trong Dự án

| Thuật ngữ | Định nghĩa trong TRIAM |
| :--- | :--- |
| **RAG (Retrieval-Augmented Generation)** | Kỹ thuật tìm kiếm dữ liệu từ sách làm ngữ cảnh nền tảng đưa vào LLM để tạo câu trả lời chính xác, tránh ảo tưởng. |
| **pgvector** | Phần mở rộng của PostgreSQL giúp tìm kiếm vector tương đồng ngữ nghĩa. |
| **TTS (Text-to-Speech)** | Chuyển đổi kịch bản văn bản tóm tắt bài học thành file âm thanh nghe (sách nói). |
| **Hybrid Search** | Phép tìm kiếm kết hợp cả Vector Search (ngữ nghĩa) và Lexical Search (từ khóa/BM25) để tối đa độ chính xác. |
| **Outbox Pattern** | Mẫu thiết kế ghi thông tin cần gửi vào DB trước, sau đó worker quét gửi sau để đảm bảo không bị mất thông báo kể cả khi lỗi mạng. |
| **Spaced Repetition** | Phương pháp ôn tập lặp lại ngắt quãng để ghi nhớ kiến thức lâu hơn. |
