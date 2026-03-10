Tuyệt vời! Quyết định dùng **`uv`** (của Astral) cho thấy bạn rất cập nhật công nghệ. Đây là trình quản lý package nhanh nhất hiện nay (viết bằng Rust), thay thế hoàn hảo cho pip/poetry.

Với vai trò Tech Lead, tôi sẽ hướng dẫn bạn dựng khung dự án (Skeleton) chuẩn **Clean Architecture** để đảm bảo mở rộng sau này, tối ưu cho **Async/Streaming**.

---

### Bước 1: Khởi tạo dự án với `uv`

Mở terminal và chạy các lệnh sau để tạo môi trường sạch sẽ, tốc độ cao:

```bash
# 1. Cài đặt uv (nếu chưa có)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Khởi tạo project mới
uv init triam-backend
cd triam-backend

# 3. Tạo môi trường ảo (Virtual Environment)
uv venv
source .venv/bin/activate  # Trên Mac/Linux
# .venv\Scripts\activate   # Trên Windows

```

---

### Bước 2: Cài đặt các thư viện "Core" (Tối ưu Async)

Chúng ta sẽ cài các thư viện cần thiết nhất. Tôi chọn **FastAPI** (Web), **Uvicorn** (Server), **OpenAI** (AI), và **Python-Multipart** (Upload file).

Chạy lệnh sau:

```bash
uv add fastapi uvicorn python-dotenv openai python-multipart pinecone-client pypdf tiktoken

```

* `fastapi`, `uvicorn`: Combo backend chuẩn.
* `openai`: SDK chính chủ, hỗ trợ async.
* `python-multipart`: Bắt buộc để nhận file PDF upload.
* `pinecone-client`: Để giao tiếp Vector DB.
* `pypdf`: Nhẹ, nhanh để extract text cơ bản (sau này có thể đổi sang LlamaParse nếu cần xịn hơn).
* `tiktoken`: Để đếm token, tránh vượt quá giới hạn Context Window.

---

### Bước 3: Cấu trúc thư mục (Clean Architecture)

Đừng viết tất cả vào 1 file `main.py`. Hãy chia module ngay từ đầu để dễ quản lý logic "Voice", "PDF", "Chat".

Bạn hãy tạo cấu trúc thư mục như sau:

```text
triam-backend/
├── .env                  # Lưu API Keys (Rất quan trọng)
├── .gitignore            # Ignore .env, .venv, __pycache__
├── pyproject.toml        # File quản lý dependency của uv
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── core/             # Cấu hình hệ thống
│   │   └── config.py
│   ├── api/              # Chứa các Router (Endpoint)
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── upload.py  # Xử lý PDF
│   │       │   └── chat.py    # Xử lý hỏi đáp
│   ├── services/         # Logic nghiệp vụ (Brain)
│   │   ├── llm_service.py     # Xử lý OpenAI (Normalization, Chat)
│   │   ├── tts_service.py     # Xử lý Text-to-Speech Streaming
│   │   └── pdf_service.py     # Xử lý File
│   └── schemas/          # Pydantic Models (Validation)

```

---

### Bước 4: Thiết lập API Key (.env)

Tạo file `.env` ở thư mục gốc và điền key của bạn vào.
*Lưu ý: Tôi thêm các key khác bạn nên đăng ký Free tier ngay để test.*

```env
# OPENAI (Đã có)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx

# PINECONE (Vector DB - Free Tier)
PINECONE_API_KEY=xxxx-xxxx-xxxx
PINECONE_ENV=us-east-1

# TAVILY (Search Web - Free Tier)
TAVILY_API_KEY=tvly-xxxx

```

---

### Bước 5: Viết Code Core - "Streaming Pipeline" (Quan trọng nhất)

Đây là phần "ăn tiền" để chứng minh độ mượt. Tôi sẽ viết mẫu file `app/services/tts_service.py` sử dụng cơ chế **Async Generator** để stream audio.

**File: `app/core/config.py**`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Các config khác...

settings = Settings()

```

**File: `app/services/tts_service.py**`
*(Logic: Text vào -> OpenAI TTS stream -> Trả về từng chunk bytes)*

```python
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def stream_text_to_speech(text: str, voice: str = "alloy"):
    """
    Hàm này nhận text, gọi OpenAI TTS và trả về stream audio ngay lập tức.
    """
    try:
        # Gọi API OpenAI với chế độ stream (Dù TTS API trả về binary, ta sẽ chunk nó)
        response = await client.audio.speech.create(
            model="tts-1", # Model nhanh nhất, độ trễ thấp
            voice=voice,
            input=text
        )

        # Streaming response (Chunking 4096 bytes để gửi dần xuống client)
        async for chunk in response.iter_bytes(chunk_size=4096):
            if chunk:
                yield chunk

    except Exception as e:
        print(f"Error in TTS Stream: {e}")
        # Trong thực tế nên log vào file hoặc Sentry

```

**File: `app/main.py**`
*(Tạo endpoint test stream)*

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.services.tts_service import stream_text_to_speech

app = FastAPI(title="TRIAM Assistant API")

@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}

@app.get("/test-voice-stream")
async def test_voice_stream(text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM."):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(
        stream_text_to_speech(text),
        media_type="audio/mpeg"
    )

if __name__ == "__main__":
    import uvicorn
    # Reload=True để code tới đâu server cập nhật tới đó
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

---

### Bước 6: Chạy thử (Run & Test)

1. Tại terminal thư mục gốc `triam-backend`:
```bash
uv run app/main.py

```


2. Mở trình duyệt hoặc Postman truy cập:
`http://localhost:8000/docs` (Swagger UI tự động của FastAPI).
3. Vào endpoint `/test-voice-stream`, nhập text: *"Công nghệ thông tin là nền tảng của chuyển đổi số."* và bấm **Execute**.

**Kết quả mong đợi:**
Bạn sẽ thấy trình duyệt (hoặc Postman) bắt đầu phát file âm thanh **gần như ngay lập tức** (chỉ trễ khoảng 1-1.5s), thay vì phải đợi tải xong.

---

### Nhiệm vụ tiếp theo cho bạn:

Hệ thống đã chạy "Hello World" với Async Streaming. Bước tiếp theo, bạn cần xử lý phần **Normalization (Chuẩn hóa)** để AI đọc "CNTT" thành "Công nghệ thông tin" trước khi đưa vào hàm `stream_text_to_speech`.

Bạn có muốn tôi viết tiếp module `llm_service.py` để xử lý logic **"Biên tập viên AI"** (Text Normalization) này không?