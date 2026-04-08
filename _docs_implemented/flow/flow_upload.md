# Flow Upload Document & Generate Reading Plan (PDF, Word, Ebook)

## 1. User Uploads Document (PDF, Word, Ebook)

- **Aim:** Denied trash from user, give user a good freedom experience. Trả về kết quả nhanh nhất có thể để UI không bị treo.
- **Logic flow:**
  - **Flutter:** Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook)
  - **Backend (API `/upload`):**
    - Validate type, size.
    - Store tmp local folder.
    - Rename fileName to be unique (UUID).
    - Extract NHANH outline (Table of Contents) bằng thư viện (VD: PyMuPDF). Chưa xử lý text vội.
    - Upload file PDF lên Supabase Storage (VD thư mục `raw_books`).
    - SaveDB (Draft): `books(id, user_id, title, file_url, total_chapters, status='DRAFT', created_at)`
    - Return `book_id` và `outline` về cho Flutter.
    - **[Dọn Rác]** Block `finally`: Phải xoá file tmp lưu ở máy chủ FastAPI để tránh đầy bộ nhớ Server.

## 2. Flutter appear outline & User configure Reading Plan

- **Aim:** Smooth exp, hide conflict process. Giúp người dùng nắm được tổng quan cuốn sách trước khi thiết lập lộ trình học tập dựa trên quỹ thời gian cá nhân.
- **Logic flow:**
  - **Flutter:** Show outline (nhận từ API `/upload`). Hiển thị cấu trúc các chương.
  - Hiển thị màn hình thiết lập Plan với các lựa chọn:
    - **Mode:** `FULL_MODE` (Đọc toàn văn) hoặc `PARETO_MODE` (AI tóm lọc 20% nội dung cốt lõi mang lại 80% giá trị).
    - **Pace:** Số lượng chương/ngày (VD: 2 chapter/day).
    - **Times:** Lịch học trong tuần (JSON config).
    - "Start plan" => Gửi request chứa cấu hình lên Backend.

## 3. Backend: Save Plan & Start Background Process

- **Aim:** Lưu trữ cấu hình học tập và chuyển các tác vụ nặng (AI, TTS, Embedding) xuống Background Task để giải phóng kết nối cho Client.
- **Logic flow:**
  - **Backend (API `/generate-plan`):**
    - Update `books` table: `status='PROCESSING'`.
    - Setup plan: SaveDB `reading_plans(book_id, mode, pace, schedule_config)`.
    - Kích hoạt Background Job chạy ngầm: `process_book_pipeline(book_id, mode)`.
    - Return status 200 OK immediately for Flutter.
  - **Flutter (Tracking Progress):**
    - Thay vì gọi API quét liên tục, App **subscribe vào kênh Supabase Realtime** lắng nghe sự thay đổi của bảng `chapters` hoặc `books` dựa trên `book_id`.
    - Navigate to "Book processing" screen (hiển thị thanh % Progress Bar mượt mà mỗi khi Backend xử lý xong 1 chapter và lưu DB, Supabase Realtime sẽ push event).

## 4. Background Process Logic (The Core AI Engine)

- **Aim:** Phân tách xử lý ETL data, sinh TTS và Vector Embedding thành các luồng song song (Parallel) để tối ưu hiệu suất, tránh nghẽn cổ chai và giảm chi phí LLM.
- **Logic flow:** Tại Background, lặp qua từng chương (Chapter) dựa trên outline. Trích xuất văn bản thô (Raw Text) của chương đó. Cắt bỏ rác (watermark, footer). Sau đó chạy **2 tiến trình ngầm song song (`asyncio.gather`)**:

  ### 4.1. LUỒNG 1: Xây dựng dữ liệu RAG (Phục vụ Voice-to-Voice)
  - **Aim:** Đảm bảo hệ thống Vector DB luôn có 100% kiến thức gốc để AI trả lời câu hỏi chi tiết, bất kể user đang học Mode nào.
  - **Logic flow:**
    - Không dùng LLM to split chunks. Sử dụng thuật toán chia văn bản (`RecursiveCharacterTextSplitter` của Langchain) trên Raw Text.
    - Cắt văn bản thành các `raw_chunks` ngắn (khoảng 1200 kí tự, overlap 200), cấu hình ngắt đúng dấu chấm, `\n` để giữ nguyên văn phong.
    - Gọi OpenAI Embedding API (`text-embedding-3-small`) để vector hóa.
    - SaveDB: `book_knowledge(book_id, chapter_id, chunk_index, content, embedding)`.

  ### 4.2. LUỒNG 2: Xử lý kịch bản Audio & TTS (Khả năng nghe thụ động)
  - **Aim:** Biên tập kịch bản mượt mà bằng LLM và chuyển đổi thành âm thanh theo đúng Mode người dùng đã chọn.
  - **Logic flow:**
    - **Step 1: LLM Rewrite (Tạo kịch bản JSON)**
      - Đưa Raw Text qua Gemini 2.5 API. Phân nhánh prompt theo Plan:
        - `PARETO_MODE`: Prompt yêu cầu AI đóng vai biên tập viên, trích xuất 20% lượng kiến thức cốt lõi (mang lại 80% giá trị).
        - `FULL_MODE`: Prompt yêu cầu AI chuẩn hóa từ viết tắt (CNTT -> Công nghệ thông tin), số liệu, tự nhiên hóa câu văn để dùng cho TTS đọc tự nhiên.
        - Output phải lấy ra định dạng JSON (`main_scripts` array và `review_script` chuỗi tóm tắt).

  ```python
    TEMPLATE_SYSTEM_PROMPT_REWRITE (FULL_MODE template) = """
    Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
    Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

    QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
    1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
    2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi".
    3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến.
    4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
    5. Văn phong: Giữ nguyên ý nghĩa gốc, KHÔNG bịa thêm nội dung sai lệch.

    YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
    Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
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

  - **Step 2: Convert audio (TTS) & Storage**
    - Lặp qua mảng `main_scripts`.
    - **Dùng công nghệ EdgeTTS** (Trong giai đoạn DEV thử nghiệm) hoặc **OpenAI TTS** (Khi lên môi trường PROD) để sinh file audio (`.mp3`) cục bộ.
    - Lấy thời lượng âm thanh (`duration_ms`).
    - Upload file audio lên Supabase Storage -> Lấy `audio_url`.
    - **[Dọn Rác]**: Delete local file.
  - **Step 3: Save Playlist to DB**
    - SaveDB: `chapter_segments(chapter_id, segment_index, audio_url, duration_ms, text_content)`.
    - Save mảng ôn tập `review_script` vào bảng `chapters(review_text)` và/hoặc gọi sinh audio cho đoạn review gắn vào `review_audio_url`.

## 5. Progress Synchronization & Error Handling

- **Hoàn thành Chapter:** Khi Luồng 1 và Luồng 2 của một chương hoàn tất: Update `chapters.status = 'READY'`. (Tín hiệu này kích hoạt Supabase Realtime đẩy về Flutter tăng thanh Progress).
- **Hoàn thiện Book:** Khi tất cả chapters hoàn thành quá trình xử lý: Update `books.status = 'READY'`.
- **[CRITICAL] Bắt lỗi (Exception Handling):**
  - Toàn bộ tiến trình chạy ngầm KHÔNG ĐƯỢC chết mà không để lại vết sẹo. Cần bọc trong khối `try...catch`. Nếu có lỗi (LLM từ chối trả lời, file bị hỏng, lỗi quá hạn mức TTS Rate Limit...):
  - Bắt Exception và lấy nguyên nhân lỗi.
  - Update `books.status = 'ERROR'`.
  - Update `books.error_message = <Chi tiết nguyên nhân>`.
  - Lập tức Supabase Realtime gửi status ERROR => Flutter bắt tự động popup màn hình xin lỗi (Ví dụ: "Xử lý sách thất bại, do file bị hỏng hoặc lỗi hệ thống").
