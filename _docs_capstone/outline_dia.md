## I. Phân tích sự bất tương thích hiện tại

### 1. Phân tích hình vẽ bạn đính kèm trong chat

Hình vẽ bạn đính kèm là một sơ đồ kiến trúc thô ở mức hệ thống (System Architecture) rất cũ hoặc mang tính chung chung:

- **Điểm không khớp công nghệ:** Sơ đồ hiển thị các logo của **PHP**, **LangChain**, **Machine Learning Studio Workspaces**... Trong khi thực tế mã nguồn của hệ thống hiện tại sử dụng **FastAPI (Python)**, **Celery**, **LiveKit WebRTC**, **mutagen** và **Supabase**.
- **Điểm không khớp luồng nghiệp vụ:** Sơ đồ này vẽ vai trò của "Cán bộ", "Giảng viên", "Sinh viên" gửi PDF và hỏi đáp. Trong khi nội dung thực tế của Chương 5 đến Chương 8 mô tả **quy trình tiền xử lý âm thanh tự động, lập kế hoạch học tập cá nhân hóa, Spaced Repetition và Voice Agent thời gian thực**.

### 2. Phân tích tệp `.mmd` hiện tại của Chương 5 ([c5_intro_diagram_1.mmd](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/2022DoAnTN_KhoaDat/hinhve/c5_quy_trinh_chuyen_doi_tai_lieu/c5_intro_diagram_1.mmd))

Tệp Mermaid hiện tại thực chất đã mô tả đúng các bước nghiệp vụ trong code, nhưng nó đang ở dạng **luồng dữ liệu phẳng (Data Flow)**, chưa thể hiện rõ **sự tương tác của người học (User)** và **ranh giới xử lý (FastAPI Server vs Celery Worker)**.

---

## II. Giải pháp chuẩn hóa sơ đồ quy trình cho từng chương

Đối với luận văn tốt nghiệp ứng dụng kỹ thuật, cách vẽ sơ đồ chuẩn nhất cho các chương thiết kế/quy trình là **Sơ đồ quy trình tương tác phân làn (Swimlane Flowchart)** hoặc **Sơ đồ trình tự (Sequence Diagram)**. Sơ đồ này phải chỉ rõ:

1.  **Hành động của Người học (User / Flutter App)** kích hoạt quy trình.
2.  **Xử lý đồng bộ của API Server (FastAPI)** (Phản hồi nhanh).
3.  **Xử lý bất đồng bộ của Worker (Celery)** (Tiền xử lý âm thanh, AI).
4.  **Lưu trữ (Database / Supabase Storage)**.

Dưới đây là thiết kế chi tiết lại sơ đồ cho từng chương để khớp hoàn hảo 100% với nội dung text:

### 1. Thiết kế sơ đồ mới cho Chương 5 (Quy trình chuyển đổi và tiền xử lý âm thanh)

Sơ đồ này chia làn rõ ràng để người đọc nhìn hình là biết khối nào tương ứng với mục nào trong Chương 5 (Mục 5.1 đến 5.4):

```mermaid
graph TD
    %% Định nghĩa các làn xử lý
    subgraph User [Người học / Mobile App]
        U1[1. Tải lên tài liệu PDF/EPUB/DOCX]
        U2[Xem Outline Preview & Thiết lập lịch học]
        U3[2. Xác nhận tạo kế hoạch học tập]
    end

    subgraph API [FastAPI Server - Đồng bộ]
        A1[Mục 5.1: Phân tích cấu trúc sách]
        A2{Cổng kiểm duyệt mục lục Validation Gate}
        A3[Lưu DRAFT Book & BookSection]
        A4[Kích hoạt Indexing Task]
        A5[Lưu ReadingPlan & Kích hoạt Processing Task]
    end

    subgraph IndexerWorker [Celery Indexer - Bất đồng bộ nền]
        W_Index[Mục 5.4: Trích xuất chunk & Xây dựng Vector Embedding]
    end

    subgraph TTSWorker [Celery TTS Worker - Bất đồng bộ nền]
        W_Norm[Mục 5.2: LLM chuẩn hóa văn bản nói]
        W_TTS[Mục 5.3: Tổng hợp giọng nói phân đoạn TTS]
    end

    subgraph DB [Database & Storage]
        D1[(PostgreSQL / Supabase)]
    end

    %% Luồng liên kết của Giai đoạn Upload (Step 1)
    U1 -->|HTTP POST /upload| A1
    A1 --> A2
    A2 -->|Thất bại: Thiếu outline| ERR[Trả về lỗi 422 cho User]
    A2 -->|Thành công| A3
    A3 -->|Lưu DRAFT Book & Section tree| D1
    A3 --> A4
    A4 -->|Gọi async Celery index_book_sections_task| W_Index
    A4 -->|Trả về outline tree preview| U2

    %% Luồng chạy ngầm của Indexer (Mục 5.4)
    W_Index -->|Gọi OpenAI Embedding API| D1

    %% Luồng liên kết của Giai đoạn Lập kế hoạch (Step 2)
    U2 --> U3
    U3 -->|HTTP POST /generate-plan| A5
    A5 -->|Lưu ReadingPlan & ProcessingJob| D1
    A5 -->|Gọi async Celery process_book_task| W_Norm
    
    %% Luồng chạy ngầm của TTS (Mục 5.2 & 5.3)
    W_Norm -->|Gọi API LLM chuẩn hóa phát âm| W_TTS
    W_TTS -->|Mutagen đo thời lượng & Gọi API TTS| D1
    W_TTS -->|Upload file MP3 lên Storage| D1
```

- **Cách map vào nội dung Chương 5:**
  - Khối **A1 & A2** ánh xạ trực tiếp vào **Mục 5.1 (Phân tích cấu trúc sách và Validation Gate)**.
  - Khối **W4** ánh xạ trực tiếp vào **Mục 5.4 (Xây dựng vector embedding)**.

---

### 2. Định hướng sơ đồ cho Chương 6 (Cơ chế lập kế hoạch và thiết lập chế độ học tập)

Sơ đồ của Chương 6 cần làm nổi bật sự khác biệt về thuật toán phân chia bài học giữa hai chế độ:

```mermaid
graph TD
    Start[Người dùng kích hoạt kế hoạch học tập] --> CheckMode{Chế độ học tập?}

    %% Nhánh FULL Mode (Mục 6.2)
    CheckMode -->|FULL Mode| F1[Quét toàn bộ cây thư mục gốc]
    F1 --> F2[Heuristic phân tách chương lớn > 12000 tokens]
    F2 --> F3[Heuristic gộp chương nhỏ < 300 tokens]
    F3 --> F4[Tạo danh sách bài học đầy đủ]

    %% Nhánh PARETO Mode (Mục 6.3)
    CheckMode -->|PARETO Mode| P1[Trích xuất thẻ thông tin đề mục SectionCard]
    P1 --> P2[Bộ lọc chấm điểm Heuristic Pareto & Multilingual Signal Optimizer]
    P2 --> P3{Gọi LLM Planner lập lịch học?}
    P3 -->|Thành công| P4[Nhận JSON kết quả gồm 3-8 bài học cốt lõi]
    P3 -->|Thất bại / Timeout 25s| P5[Kích hoạt cơ chế dự phòng Heuristic Pareto]
    P4 --> P6[Tạo danh sách bài học trọng tâm]
    P5 --> P6

    F4 --> End[(Lưu các thực thể LearningUnit vào Database)]
    P6 --> End
```

---

### 3. Định hướng sơ đồ cho Chương 7 (Hệ thống theo dõi tiến độ và ôn tập ngắt quãng)

Sơ đồ Chương 7 cần làm rõ vòng lặp học tập khép kín từ khi nghe nhạc, tính tiến độ chống tua, lập lịch nhắc nhở cho đến khi chạy Outbox gửi thông báo:

```mermaid
graph TD
    subgraph Client [Ứng dụng di động]
        C1[Người học nghe audio bài giảng] -->|Gửi tiến độ nghe| C2{Tiến độ đạt >= 80%?}
    end

    subgraph SyncDB [Máy chủ - Cập nhật tiến độ]
        C2 -->|Có| S1[Cập nhật Highest Progress & Đánh dấu Completed]
        S1 -->|Kích hoạt Spaced Repetition| S2[Sinh 5 mốc ôn tập trong tương lai]
    end

    subgraph OutboxPattern [Mục 7.4: Gửi thông báo nhắc nhở tự động]
        O1[Celery Beat quét DB mỗi 60 giây] -->|Lấy các phiên học/ôn tập đến hạn| O2[Tạo bản ghi pending trong Outbox với Idempotency Key]
        O2 --> O3{Kiểm tra Quiet Hours & Daily Cap?}
        O3 -->|Đang trong giờ yên tĩnh hoặc vượt Cap| O4[Trì hoãn thời gian gửi sang ngày hôm sau]
        O3 -->|Hợp lệ| O5[Thực hiện Row-Level Locking và gửi thông báo qua FCM]
    end

    S2 -->|Lưu mốc ôn tập chờ gửi| O1
    O5 -->|Hiển thị thông báo nhắc nhở| C1
```

---

### 4. Định hướng sơ đồ cho Chương 8 (Trợ lý giọng nói và RAG)

Sơ đồ Chương 8 mô tả luồng hội thoại giọng nói thời gian thực và cơ chế kiểm soát RAG/Internet Search:

```mermaid
graph TD
    U[Người học phát ngôn giọng nói] -->|Giao thức WebRTC| L[Phòng hội thoại LiveKit]
    L -->|Trực quan hóa text trên screen| D[Kênh dữ liệu Data Channel]
    L -->|Chuyển âm thanh thành text bằng STT| G[Mục 8.3: Grounding Router]

    G -->|Câu hỏi thông tin sách| G1[Truy vấn trực tiếp DB & Trả lời]
    G -->|Câu hỏi cụ thể đề mục| G2[Nạp trực tiếp nội dung chương & Trả lời]
    G -->|Câu hỏi tổng hợp kiến thức| G3[RAG Fallback: Hybrid Search]

    G3 -->|Tìm kiếm song song Vector + Lexical Trigram| R1[Gộp & Rerank cơ sở]
    R1 --> R2[Cổng xác thực ngữ cảnh Evidence Validation]
    
    R2 -->|Hợp lệ| R3{Kích hoạt Cohere Rerank?}
    R3 -->|Có| RC[API Cohere Rerank v2]
    R3 -->|Không hoặc Lỗi/Timeout| RF[Dùng điểm số Rerank cơ sở]
    
    RC --> ANS[AI tạo câu trả lời & Tổng hợp thành giọng nói qua TTS]
    RF --> ANS
    
    R2 -->|Thiếu thông tin hoặc nằm ngoài sách| S[Mục 8.6: Gọi công cụ xin quyền tìm kiếm Internet]

    S -->|Hỏi người học cấp quyền| U2{Người học phản hồi cấp quyền?}
    U2 -->|Đồng ý - grant| EXEC[Thực hiện tìm kiếm Web bằng Search Engine & Thu hồi quyền]
    U2 -->|Từ chối - deny| REJ[Thông báo không tìm kiếm ngoài sách]
```

---

## 📢 Báo cáo đề xuất hành động:

Tôi đề xuất chúng ta sẽ **cập nhật lại mã nguồn sơ đồ Mermaid** (các tệp `.mmd`) trong thư mục `hinhve` của bạn theo các sơ đồ quy trình tương tác phân làn ở trên. Việc này giúp:

1.  Người đọc luận văn có thể đối chiếu chính xác từng khối trong hình vẽ với các mục nhỏ trong văn bản.
2.  Làm nổi bật tính logic kỹ thuật của ứng dụng thay vì vẽ các hình vẽ hệ thống chung chung lỗi thời.

Bạn có muốn tôi tiến hành cập nhật tệp [c5_intro_diagram_1.mmd](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/2022DoAnTN_KhoaDat/hinhve/c5_quy_trinh_chuyen_doi_tai_lieu/c5_intro_diagram_1.mmd) thành sơ đồ quy trình phân làn mới này không?
