Tuyệt vời! Bạn đang đi rất đúng lộ trình và tốc độ. Việc stream được audio là một cột mốc kỹ thuật lớn.

Giờ chúng ta sẽ xử lý "Phần hồn" của dự án: **Biến bộ đọc vô tri thành một Assistant có hiểu biết (Text Normalization)** và xử lý đầu vào **PDF**.

Chúng ta sẽ thực hiện 3 module tiếp theo:

1. **`llm_service.py`**: "Biên tập viên" xử lý văn bản (CNTT -> Công nghệ thông tin).
2. **`pdf_service.py`**: Trích xuất nội dung từ file user upload.
3. **`upload.py`**: API endpoint để ghép nối tất cả lại.

---

### Bước 1: Tạo "Biên tập viên AI" (`llm_service.py`)

Đây là nơi chứa logic thông minh mà bạn yêu cầu: xử lý từ viết tắt, tiếng Anh và giọng điệu.

Tạo file `app/services/llm_service.py`:

```python
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Prompt "thần thánh" để định hình phong cách đọc
SYSTEM_PROMPT = """
Bạn là một biên tập viên phát thanh chuyên nghiệp (Script Editor).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (Spoken Script) để người đọc tin (AI TTS) đọc tự nhiên nhất.

QUY TẮC BẮT BUỘC:
1. Mở rộng từ viết tắt: Dựa vào ngữ cảnh, hãy viết đầy đủ các từ viết tắt.
   - Ví dụ: "CNTT" -> "Công nghệ thông tin", "DN" -> "Doanh nghiệp", "NS" -> "Nhân sự".
2. Xử lý Tiếng Anh/Thuật ngữ:
   - Các từ tiếng Anh phổ biến (AI, CEO, Marketing) -> Giữ nguyên (nếu bộ đọc tốt) hoặc chú thích phiên âm nếu cần.
   - Ví dụ đặc biệt: "AI" -> "Ây Ai", "Agile" -> "A-chao".
3. Số liệu & Ký hiệu:
   - "5%" -> "Năm phần trăm".
   - "Tp.HCM" -> "Thành phố Hồ Chí Minh".
4. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

Input: Văn bản gốc từ sách.
Output: Chỉ trả về văn bản đã biên tập, không thêm lời chào hay giải thích gì khác.
"""

async def normalize_text_for_speech(raw_text: str) -> str:
    """
    Gửi text thô cho GPT-4o-mini biên tập lại trước khi đọc.
    Dùng model 'gpt-4o-mini' cho rẻ và nhanh (Latency thấp).
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3, # Giữ cho AI tập trung, ít sáng tạo lung tung
            max_tokens=2000  # Giới hạn output
        )
        normalized_text = response.choices[0].message.content
        return normalized_text
    except Exception as e:
        print(f"Lỗi Normalization: {e}")
        return raw_text # Fallback: Nếu lỗi thì trả về text gốc đọc tạm

```

---

### Bước 2: Tạo Module xử lý PDF (`pdf_service.py`)

Chúng ta dùng `pypdf` (đã cài ở bước trước) để lấy text nhanh.
_Lưu ý: Sau này nếu cần xử lý PDF 2 cột hoặc có bảng biểu phức tạp, ta sẽ nâng cấp lên `LlamaParse` sau. Giờ cứ dùng `pypdf` cho MVP chạy được đã._

Tạo file `app/services/pdf_service.py`:

```python
import pypdf
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile, max_pages: int = 5) -> str:
    """
    Trích xuất text từ file PDF upload.
    max_pages: Giới hạn số trang xử lý thử nghiệm để tránh đợi lâu.
    """
    try:
        # Đọc file từ memory (stream)
        pdf_reader = pypdf.PdfReader(file.file)

        text_content = []

        # Chỉ lấy text của max_pages trang đầu tiên (Ví dụ: Intro + Chương 1)
        num_pages = min(len(pdf_reader.pages), max_pages)

        for i in range(num_pages):
            page = pdf_reader.pages[i]
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)

        return "\n".join(text_content)
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
        return ""

```

---

### Bước 3: Tạo Endpoint Upload & Nghe thử (`upload.py`)

Giờ ta sẽ tạo API endpoint: **Upload PDF -> Extract Text -> Normalize -> Stream Voice**.

Tạo file `app/api/v1/endpoints/upload.py`:

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_service import normalize_text_for_speech
from app.services.tts_service import stream_text_to_speech

router = APIRouter()

@router.post("/process-book-intro")
async def process_book_intro(file: UploadFile = File(...)):
    """
    Flow Demo:
    1. User upload PDF.
    2. Server đọc 1-2 trang đầu.
    3. LLM sửa lỗi chính tả/viết tắt (CNTT -> Công nghệ thông tin).
    4. TTS đọc stream về ngay lập tức.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    # 1. Extract Text (Lấy 2 trang đầu làm Intro)
    raw_text = await extract_text_from_pdf(file, max_pages=2)

    if not raw_text:
        raise HTTPException(status_code=400, detail="Không đọc được nội dung PDF")

    # 2. Normalize (Biên tập lại - Bước quan trọng nhất!)
    # Cắt ngắn bớt nếu quá dài để demo cho nhanh (lấy 1000 ký tự đầu)
    short_preview = raw_text[:1000]
    script_ready = await normalize_text_for_speech(short_preview)

    print(f"Original: {short_preview[:100]}...")
    print(f"Normalized: {script_ready[:100]}...")

    # 3. Stream Audio về App
    return StreamingResponse(
        stream_text_to_speech(script_ready),
        media_type="audio/mpeg"
    )

```

---

### Bước 4: Đăng ký Router vào `main.py`

Quay lại file `app/main.py` và sửa lại để nhận diện router mới:

```python
from fastapi import FastAPI
from app.api.v1.endpoints import upload # Import router upload

app = FastAPI(title="TRIAM Assistant API")

# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])

@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

---

### Bước 5: Chạy thử nghiệm (Moment of Truth)

Đây là lúc kiểm tra xem logic "CNTT -> Công nghệ thông tin" có hoạt động không.

1. **Chuẩn bị:** Tạo một file PDF giả lập `test.pdf` có nội dung khó:

   > _"Chào mừng các bạn sinh viên ngành CNTT. Hôm nay chúng ta sẽ tìm hiểu về AI và cách các CEO ứng dụng nó."_

2. **Chạy server:** `uv run app/main.py`
3. **Test:**

- Mở trình duyệt: `http://localhost:8000/docs`
- Tìm endpoint **POST** `/api/v1/process-book-intro`.
- Upload file `test.pdf`.
- Bấm **Execute**.

**Kết quả mong đợi:**
Bạn sẽ nghe thấy giọng đọc vang lên:

> _"Chào mừng các bạn sinh viên ngành **Công nghệ thông tin**. Hôm nay chúng ta sẽ tìm hiểu về **Ây Ai** và cách các **Giám đốc điều hành** ứng dụng nó."_

---

### Checkpoint

Đến bước này, bạn đã hoàn thành **Core Loop** (Vòng lặp cốt lõi):

- Input (PDF) Process (Extraction + Normalization) Output (Voice Stream).

**Câu hỏi tiếp theo của bạn:**
Bạn muốn làm tiếp phần **Tạo lộ trình học (Lưu vào Database)** hay phần **Chat/Hỏi đáp với sách (RAG Logic)**? Tôi khuyên nên làm phần **Tạo lộ trình** để hoàn thiện luồng User Flow (Upload xong -> Thấy mục lục -> Chọn nghe).   