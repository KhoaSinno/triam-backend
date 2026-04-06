# Flow Upload Document & Generate Reading Plan (PDF, Word, Ebook)

## 1. User uploads a document (PDF, Word, Ebook) to the system

- **Aim:** Denied trash from user, give user a good freedom experience. Trả về kết quả nhanh nhất có thể để UI không bị treo.

- **Logic flow:**
  - **Flutter:** Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook)
  - **Backend (API `/upload`):**
    - Validate type, size.
    - Store tmp local/Supabase Storage.
    - Rename fileName to be unique.
    - Extract NHANH outline (Table of Contents) bằng thư viện (VD: PyMuPDF). Chưa xử lý text vội.
    - SaveDB (Draft): `books(id, title, total_chapters, status='DRAFT', created_at)`
    - Return `book_id` và `outline` về cho Flutter.

## 2. Flutter appear outline

- **Aim:** Smooth exp, hide conflict process. Giúp người dùng nắm được tổng quan cuốn sách trước khi lên lịch.

- **Logic flow:**
  - **Flutter:** Show outline (nhận từ API `/upload`). Hiển thị cấu trúc các chương.

## 3. User configure Reading Plan

- **Aim:** Trao quyền cho người dùng thiết lập lộ trình học tập dựa trên độ dài thực tế của cuốn sách và quỹ thời gian cá nhân.

- **Logic flow:**
  - **Flutter:** Hiển thị màn hình thiết lập Plan với các lựa chọn:
    - **Mode:** `FULL_MODE` (Đọc toàn văn) hoặc `PARETO_MODE` (AI tóm lọc 20% nội dung cốt lõi mang lại 80% giá trị).
    - **Times:** Lịch học trong tuần (Mon, Tue, Wed, Thu, Fri, Sat, Sun).
    - **Pace:** Số lượng chương/ngày (VD: 2 chapter/day).
    - "Start plan" => Gửi request chứa cấu hình lên Backend.

## 4. Backend: Save Plan & Start Background Process

- **Aim:** Lưu trữ cấu hình học tập và chuyển các tác vụ nặng (AI, TTS, Embedding) xuống Background Task để giải phóng kết nối cho Client.

- **Logic flow:**
  - **Backend (API `/generate-plan`):**
    - Update `books` table: `status='PROCESSING'`.
    - Setup plan: SaveDB Json data `reading_plans(book_id, mode, pace, times, ...)`.
    - Run Background Process with plan config: `process_book_pipeline(book_id, mode)`.
    - Return status 200 OK immediately for Flutter.
  - **Flutter:** Navigate to "Book processing" screen (display progress bar or loading state).

## 5. Logic flow: Background process logic (The core AI Engine)

- **Aim:** Phân tách xử lý ETL data, sinh TTS và Vector Embedding thành các luồng song song (Parallel) để tối ưu hiệu suất, tránh nghẽn cổ chai và giảm chi phí LLM.

- **Logic flow:** Lặp qua từng chương (Chapter) dựa trên outline. Trích xuất văn bản thô (Raw Text) của chương đó. Sau đó, chạy **2 tiến trình ngầm song song (`asyncio.gather`)**:

  ### 5.1. LUỒNG 1: Xây dựng dữ liệu RAG (Tốc độ cao - Phục vụ Voice-to-Voice)
  - **Aim:** Đảm bảo hệ thống Vector DB luôn có 100% kiến thức gốc để AI trả lời câu hỏi chi tiết, bất kể user đang học Mode nào.
  - **Logic flow:**
    - Không dùng LLM to split chunks. Sử dụng thuật toán chia văn bản (`RecursiveCharacterTextSplitter` của Langchain) trên Raw Text.
    - Cắt văn bản thành các `raw_chunks` ngắn (khoảng 1200, overlap 200), cấu hình ngắt đúng dấu chấm, `/n` để giữ nguyên văn phong.
    - Gọi OpenAI Embedding API (`text-embedding-3-small`) để vector hóa.
    - SaveDB: `book_knowledge('book_id', 'chapter_index', 'chunk_index', 'content', 'embedding')`.

  ### 5.2. LUỒNG 2: Xử lý kịch bản Audio & TTS (Passive listening)
  - **Aim:** Biên tập kịch bản mượt mà bằng LLM và chuyển đổi thành âm thanh theo đúng Mode người dùng đã chọn.
  - **Logic flow:**
    - **Step 1: LLM Rewrite (Tạo kịch bản JSON)**
      - Đưa Raw Text qua Gemini API. Phân nhánh prompt theo Plan:
        - `PARETO_MODE`: Dùng prompt yêu cầu AI trích xuất 20% nội dung cốt lõi chứa 80% giá trị. Trả về định dạng JSON (`main_scripts` array và `review_script` string). `NOTE:` Vẫn giống prompt "FULL_MODE" nhưng tóm tắt lại.
        - `FULL_MODE`: Dùng `SYSTEM_PROMPT_REWRITE` dưới đây:

```python
  SYSTEM_PROMPT_REWRITE (FULL_MODE template) = """
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
  - Lặp qua mảng `main_scripts` trong JSON.
  - Gọi engine TTS để sinh file audio cục bộ.
  - Upload file lên Cloud (Supabase Storage) -> Lấy `audio_url` -> Delete local file.
- **Step 3: Save Playlist to DB**
  - SaveDB: `chapter_segments('chapter_id', 'segment_index', 'audio_url', 'text_content')` (text_content ở đây là phần kịch bản đã qua LLM biên tập).
  - (Tuỳ chọn) Lưu `review_script` để phục vụ tính năng nhắc nhở ôn tập định kỳ.

## 6. Finalize

- **Aim:** Available for user.
- **Logic flow:**
  - Khi cả Luồng 1 và Luồng 2 của một chương hoàn tất: Update `chapters` status = `READY`.
  - Khi tất cả chapters hoàn tất: Update `books` status = `READY`.
