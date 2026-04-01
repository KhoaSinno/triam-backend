# Flow Upload & Generate Reading Plan (Full / Pareto Mode)

---

## 1. User uploads a document (PDF, Word, Ebook) to the system

- **Aim:** Denied trash from user, give user a good freedom experience. Trả về kết quả nhanh nhất có thể để UI không bị treo.
- **Logic flow:**
  - **Flutter:** Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook).
  - **Backend (API `/upload`):**
    - Validate type, size.
    - Store tmp local/Supabase Storage.
    - Rename fileName to be unique.
    - **[NEW]** Extract NHANH outline (Table of Contents) bằng thư viện (ví dụ PyMuPDF). Chưa xử lý text vội.
    - SaveDB (Draft): `books(id, title, total_chapters, status='DRAFT', created_at)`
    - Return `book_id` và `outline` về cho Flutter.

## 2. Flutter appear outline & User configure Reading Plan

- **Aim:** Trao quyền cho người dùng thiết lập lộ trình học tập dựa trên độ dài thực tế của cuốn sách (ví dụ: chia số chương cần đọc mỗi ngày).
- **Logic flow:**
  - **Flutter:** Hiển thị danh sách chương. Cung cấp UI cho phép user chọn:
    - **Mode:** `FULL_MODE` (Đọc toàn văn) hoặc `PARETO_MODE` (Tóm lọc 20% cốt lõi).
    - **Pace (Tiến độ):** Ví dụ 2 chương/ngày.
    - Bấm nút "Bắt đầu tạo kế hoạch" -> Gửi request chứa cấu hình lên Backend.

## 3. Backend: Save Plan & Start Background Process

- **Aim:** Lưu trữ cấu hình học tập và chuyển các tác vụ nặng (LLM, TTS, Embedding) xuống Background Task để giải phóng kết nối cho Client.
- **Logic flow:**
  - **Backend (API `/generate-plan`):**
    - Update `books` table: `status='PROCESSING'`.
    - Lên lịch học: SaveDB `reading_plans(book_id, mode, pace, ...)`.
    - Kích hoạt Background Process `process_book_pipeline(book_id, mode)`.
    - Trả về status 200 OK ngay lập tức cho Flutter.
  - **Flutter:** Chuyển sang màn hình "Sách đang xử lý" (hiển thị progress bar giả lập hoặc trạng thái loading).

## 4. Background Process Logic (The Core AI Engine)

- **Aim:** Xử lý văn bản, sinh âm thanh và tạo Vector Database. Xử lý triệt để bài toán RAG phải có full 100% text dù ở Mode nào.
- **Logic flow:** Quét qua từng chapter trong sách:
  - **Bước 4.1: Rút trích Text & Phân nhánh Rewrite (LLM)**
    - Lấy toàn bộ Text thô của Chapter.
    - Lọc bỏ rác (header, footer, watermark).
    - Phân nhánh dựa trên `Mode`:
      - **IF FULL_MODE:** Gemini xử lý chuẩn hóa từ viết tắt (Ví dụ: "CNTT" -> "Công nghệ thông tin"). Chia văn bản thành các chunks để đọc.
      - **IF PARETO_MODE:** Gửi toàn bộ text thô của Chapter cho Gemini với System Prompt đặc biệt: _"Hãy đóng vai trò biên tập viên, phân tích và trích xuất 20% nội dung cốt lõi nhất chứa đựng 80% giá trị của chương này. Sau đó chuẩn hóa từ ngữ để làm kịch bản sách nói."_. AI sẽ trả về bản script tóm tắt (Chunks).
  - **Bước 4.2: Chuyển đổi âm thanh (TTS) & Lưu trữ**
    - Đưa các script chunks (Full hoặc Pareto) qua Edge TTS / OpenAI TTS.
    - Upload file audio lên Supabase Storage. Xóa file local.
    - SaveDB: `chapter_segments(chapter_id, segment_index, audio_url, text_content, duration)`
  - **Bước 4.3: Nhúng Vector (Embedding for RAG) - RẤT QUAN TRỌNG**
    - Bất kể user chọn Full hay Pareto, Backend **BẮT BUỘC** phải chia nhỏ toàn bộ 100% Text thô của sách (đã qua bước lọc rác) để nhúng Vector.
    - Gọi OpenAI Embeddings (`text-embedding-3-small`).
    - SaveDB: `book_knowledge(book_id, chapter_id, chunk_index, content, embedding)`.
    - _(Lý do: Khi user nghe Pareto Mode thấy khó hiểu, họ dừng lại hỏi: "Trợ lý giải thích rõ hơn khái niệm X được không?". Nếu Vector DB chỉ lưu 20% tóm tắt, RAG sẽ không tìm được chi tiết khái niệm X để trả lời)._

  - **Bước 4.4: Hoàn thiện**
    - Update `chapters` status = `READY`.
    - Khi tất cả chapters xong: Update `books` status = `READY`.
