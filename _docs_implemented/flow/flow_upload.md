# Flow Upload Document & Generate Reading Plan (PDF, Word, Ebook)

## 1. User Uploads Document (PDF, Word, Ebook)

- **Aim:** Denied trash from user, give user a good freedom experience. Trả về kết quả nhanh nhất có thể để UI không bị treo.
- **Logic flow:**
  - **Flutter:** Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook)
  - **Backend (API `POST /api/v1/upload`):**
    - Validate type (pdf, docx, epub), size (≤ 50MB).
    - Lưu file tạm vào thư mục `uploads/` với tên unique (UUID).
    - Gọi `extract_pdf_chapters()` để phân tích outline (danh sách tiêu đề chương).
    - SaveDB (DRAFT):
      - `books(id, user_id, title, total_chapters, status='DRAFT', file_url='pending', created_at)` — `user_id` lấy từ JWT Token (mock: `862d7c26-3160-4f76-9e77-07d91f7317cc`).
      - `chapters(book_id, chapter_index, title, status='DRAFT')` — Lưu ngay để Backend có thể fetch lại sau.
    - **[Dọn Rác]** Block `finally`: Xóa file tạm để tránh đầy bộ nhớ Server.
    - **Return:** `{ book_id, outline: [{title, page_start}, ...] }` → Flutter dùng để hiển thị danh sách chương.

## 2. Flutter Displays Outline & User Configures Reading Plan

- **Aim:** Smooth exp, hide conflict process. Giúp người dùng nắm được tổng quan cuốn sách trước khi thiết lập lộ trình học tập dựa trên quỹ thời gian cá nhân.
- **Logic flow:**
  - **Flutter:** Show outline (nhận từ API `/upload`). Hiển thị cấu trúc các chương.
  - Hiển thị màn hình thiết lập Plan với các lựa chọn:
    - **Mode:** `FULL_MODE` (Đọc toàn văn) hoặc `PARETO_MODE` (AI tóm lọc 20% nội dung cốt lõi mang lại 80% giá trị).
    - **Pace:** Số lượng chương/ngày (VD: 2 chapter/day).
    - **Times:** Lịch học trong tuần, lưu dạng JSON (VD: `["Mon", "Wed", "Fri"]`).
    - "Start plan" => Gửi request lên **API `/generate-plan`** riêng biệt với body: `{ book_id, mode, pace, schedule_config }`.

## 3. Backend: Save Plan & Start Background Process

- **Aim:** Lưu trữ cấu hình học tập và chuyển các tác vụ nặng (AI, TTS, Embedding) xuống Background Task để giải phóng kết nối cho Client.
- **Logic flow:**
  - **Backend (API `POST /api/v1/generate-plan`):**
    - Validate `book_id` tồn tại trong DB.
    - Update `books` table: `status='PROCESSING'`.
    - SaveDB: `reading_plans(book_id, mode, pace, schedule_config)`.
    - Kích hoạt Background Job chạy ngầm: `run_background_processing(book_id, mode)`.
    - **Return `200 OK` ngay lập tức** cho Flutter.
  - **Flutter (Tracking Progress):**
    - Subscribe vào kênh **Supabase Realtime** lắng nghe sự thay đổi `status` của bảng `chapters` theo `book_id`.
    - Navigate to "Book processing" screen (hiển thị thanh % Progress Bar — tăng mỗi khi 1 chapter được Backend update `status='READY'`).

## 4. Background Process Logic (The Core AI Engine)

- **Aim:** Phân tách xử lý ETL data, sinh TTS và Vector Embedding thành các luồng song song (Parallel) để tối ưu hiệu suất, tránh nghẽn cổ chai và giảm chi phí LLM.
- **Logic flow:**
  - Fetch danh sách `chapters` từ DB (đã lưu `status='DRAFT'` ở bước 1).
  - Dùng `asyncio.Semaphore(3)` để giới hạn tối đa 3 chương xử lý đồng thời.
  - Với mỗi chương, trích xuất Raw Text rồi chạy **2 tiến trình ngầm song song (`asyncio.gather`)**:

  ### 4.1. LUỒNG 1: Xây dựng dữ liệu RAG (Phục vụ Voice-to-Voice)
  - **Aim:** Đảm bảo hệ thống Vector DB luôn có 100% kiến thức gốc để AI trả lời câu hỏi chi tiết, bất kể user đang học Mode nào.
  - **Logic flow:**
    - Không dùng LLM để split chunks. Dùng `RecursiveCharacterTextSplitter` (Langchain) trên Raw Text.
    - Cắt văn bản: chunk size ~1200 ký tự, overlap 200, ngắt đúng dấu chấm.
    - Gọi OpenAI Embedding API batch (`text-embedding-3-small`) để vector hóa.
    - SaveDB: `book_knowledge(book_id, chapter_id, chunk_index, content, embedding)`.

  ### 4.2. LUỒNG 2: Xử lý kịch bản Audio & TTS (Khả năng nghe thụ động)
  - **Aim:** Biên tập kịch bản mượt mà bằng LLM và chuyển đổi thành âm thanh theo đúng Mode người dùng đã chọn.
  - **Logic flow:**
    - **Step 1: LLM Rewrite (Tạo kịch bản JSON)**
      - Đưa Raw Text qua Gemini 2.5 Flash API.
      - Phân nhánh prompt theo `mode`:
        - `PARETO_MODE`: Prompt yêu cầu AI đóng vai biên tập viên, trích xuất 20% lượng kiến thức cốt lõi.
        - `FULL_MODE`: Dùng `SYSTEM_PROMPT_REWRITE` (đã có trong `app/services/llm_service.py`).
      - Output bắt buộc là JSON: `{ "main_scripts": [...], "review_script": "..." }`.

    ```python
    SYSTEM_PROMPT_REWRITE (FULL_MODE) = """
    Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
    Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

    QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
    1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
    2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi".
    3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến.
    4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
    5. Văn phong: Giữ nguyên ý nghĩa gốc, KHÔNG bịa thêm nội dung sai lệch.

    YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
    {
      "main_scripts": [
        "Đoạn văn bản 1 đã biên tập...",
        "Đoạn văn bản 2 đã biên tập..."
      ],
      "review_script": "Nội dung tóm tắt để ôn tập..."
    }

    HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
    1. "main_scripts" (Mảng các chuỗi):
      - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
      - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
      - QUAN TRỌNG: Đảm bảo tính liền mạch. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu. Ngắt đoạn đúng dấu chấm câu.
    2. "review_script" (Chuỗi):
      - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất (100-150 từ) dạng văn nói gợi nhớ.
    """
    ```

    - **Step 2: Convert Audio (TTS) & Storage**
      - Lặp qua mảng `main_scripts`.
      - Gọi `generate_audio_and_get_duration(text, filename)`:
        - **Dùng EdgeTTS** (giai đoạn DEV) hoặc **OpenAI TTS** (PROD) để sinh file `.mp3` local.
        - Dùng `mutagen` để đo `duration_ms` ngay sau khi sinh file.
      - Upload file audio lên Supabase Storage bucket `audios` → lấy `audio_url`.
      - **[Dọn Rác]**: Xóa file `.mp3` local ngay sau khi upload xong.
    - **Step 3: Save Playlist to DB**
      - SaveDB: `chapter_segments(chapter_id, segment_index, audio_url, duration_ms, text_content)`.
      - SaveDB: `chapters(review_text=review_script)` (và optionally sinh audio ôn tập cho `review_audio_url`).

## 5. Progress Synchronization & Error Handling

- **Hoàn thành Chapter:** Khi cả Luồng 1 và Luồng 2 của một chương hoàn tất:
  - Update `chapters.status = 'READY'`.
  - _(Supabase Realtime tự động push event này về Flutter → Flutter tăng Progress Bar)_.
- **Hoàn thiện Book:** Khi tất cả chapters hoàn thành: Update `books.status = 'READY'`.
- **[CRITICAL] Bắt lỗi (Exception Handling):**
  - Toàn bộ tiến trình chạy ngầm KHÔNG ĐƯỢC chết mà không để lại dấu vết. Cần bọc trong khối `try...except`.
  - Nếu có lỗi (LLM từ chối trả lời, file bị hỏng, lỗi TTS Rate Limit...):
    - Bắt Exception, lấy nguyên nhân lỗi.
    - Update `books.status = 'ERROR'`, `books.error_message = <Chi tiết nguyên nhân>`.
    - Supabase Realtime push status ERROR về Flutter → Flutter hiển thị popup lỗi.

## 6. Mock User (Dev Phase — Trước khi có Auth tích hợp)

- Trong giai đoạn phát triển, `user_id` được hard-code là UUID của tài khoản test:
  ```python
  MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")
  ```
- Khi tích hợp Auth (Supabase JWT), chỉ cần thay dòng này bằng việc decode JWT Token từ Header.
