# Flow upload document (PDF, Word, Ebook)

---

## 1. User uploads a document (PDF, Word, Ebook) to the system

- **Aim:** Denied trash from user, give user a good freedom experience

- **Logic flow:**
  - Flutter: Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook)
  - Backend:
    - Validate type, size
    - Store tmp local/Supabase Storage
    - Rename fileName to be unique

## 2. Flutter appear outline

- **Aim:** Smooth exp, hide conflict process

- **Logic flow:**
  - Flutter: Show outline (await/fetch api)
  - Backend:
    - Extract outline + text from doc
    - SaveDB: `books(id, title, total_chapters, status, created_at)`
    - Return outline to Flutter

## 3. User configure Reading Plan

- **Aim:** User choose/setup plan: mode, times, (TODO: language)

- **Logic flow:**
  - Flutter: On the screen
    - Mode: `FULL_MODE` (Read all content), `PARETO_MODE` (Summarize 20% key content)
    - Times: Mon, Tue, Wed, Thu, Fri, Sat, Sun
    - Pace: 2 (chapter/day)
    <!-- - Speed: 0.5x, 1x, 1.5x, 2x (@TODO AFTER MVP)
    - Language: (@TODO AFTER MVP) -->
    - "Start plan" => Send req to BE

## 4. Backend: Save Plan & Start Background Process

- **Aim:** Save plan / Create to run backgroud jobs

- **Logic flow:**
  - **Backend (API `/generate-plan`):**
    - Update `books` table: `status='PROCESSING'`.
    - Setup plan: SaveDB `reading_plans(book_id, mode, pace, ...)`.
    - Run Background Process with plan config: `process_book_pipeline(book_id, mode)`.
    - Return status 200 OK immediately for Flutter.
  - **Flutter:** Navigate to "Book processing" screen (display progress bar or loading state).

## 5. Logic flow: Background process logic (The core AI Engine)

- **Aim:** ETL data, TTS, Embedding, SaveDB

- **Logic flow:** Each chapter in a book
  - Step 1: Extract text and rewrite it (base on plan mode)
    - User `outline framework` to get text in book base on outline
    - OPT 2 mode:
      - `PARETO_MODE`: "Hãy đóng vai trò biên tập viên, phân tích và trích xuất 20% nội dung cốt lõi nhất chứa đựng 80% giá trị của chương này. Sau đó chuẩn hóa từ ngữ để làm kịch bản sách nói.". AI will return a summary script (Chunks).
      - `FULL_MODE`:

```python
  SYSTEM_PROMPT_REWRITE (FULL_MODE template) = """
  Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
  Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

  QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
  1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
  2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
  3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
  4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
  5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

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
    - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
    - Ngắt đoạn đúng dấu chấm câu.

  2. "review_script" (Chuỗi):
    - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
    - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
    - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

  Input: Văn bản gốc.
  Output: Chỉ trả về JSON thuần.
  """
```

- **Step 2: Convert audio (TTS) & Storage**
  - TTS and storage to cloud base on plan (full/80_20): local generate => upload cloud => Delete local => Append to list
  - SaveDB base on list above: `chapter_segments('chapter_id', 'segment_index', 'audio_url', 'text_content')

- **Step 3: Embedding (content fullMode) because with fullMode seperated chunks meaningful and save it to DB**
  - Call OpenAI embedding API
  - Generate/Insert embedding vector base on text planed: `book_knowledge('book_id', 'chapter_index', 'chunk_index', 'content', 'embedding')`
  - _(Reason: When user listen Pareto Mode feels difficult, they stop and ask: "Assistant explain more about concept X?". If Vector DB only save 20% summary, RAG will not find detail concept X to answer)._

- **Bước 4.4: Hoàn thiện**
  - Update `chapters` status = `READY`.
  - Khi tất cả chapters xong: Update `books` status = `READY`.

<!-- ===== OLD LOGIC FLOW ===== -->
<!-- - Rewrite text/review_text to chunks. One chapter have many chunks, each chunk is a paragraph or 2-3 sentences meaningful
- TTS and storage to cloud base on plan (full/80_20): local generate => upload cloud => Delete local => Append to list
- SaveDB base on list above: `chapter_segments('chapter_id', 'segment_index', 'audio_url', 'text_content')`
- Generate/Insert embedding vector base on text planed: `book_knowledge('book_id', 'chapter_index', 'chunk_index', 'content', 'embedding')`
- Update chapter status to "ready"
- Update book status to "ready" when all chapters are ready -->
