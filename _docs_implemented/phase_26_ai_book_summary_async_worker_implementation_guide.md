# Phase 26: Asynchronous AI Book Summary Worker, Full-Context Gemini 2.5 Flash, Token Ceiling Safeguard (800k Tokens) & Retry Backoff Resiliency Implementation Guide

Hướng dẫn này trình bày chi tiết kiến trúc và cách hiện thực chuẩn **Senior Software Engineering** nhằm xây dựng tính năng **AI Tóm Tắt Sách Tổng Quan (Executive AI Book Summary)** cho nền tảng TRIAM Backend.

---

## 1. Mục Tiêu Nghiệp Vụ & Kiến Trúc (Business & Architecture Goals)

### 1.1. Giải quyết bài toán độ trễ (Latency Bottleneck) bằng Celery Worker
* **Vấn đề thực tế:** Khi nạp 100% nội dung một cuốn sách (70k - 200k tokens) vào Gemini 2.5 Flash để sinh bản tóm tắt chất lượng cao, thời gian xử lý thực tế qua mạng tốn **35 - 45 giây**. Nếu gọi đồng bộ qua HTTP Request, kết nối sẽ bị **HTTP Gateway Timeout 504** (Hugging Face / Cloudflare ngắt sau 30s) và làm đơ giao diện ứng dụng.
* **Giải pháp Senior:**
  * Kích hoạt **Celery Background Worker** (`generate_book_summary_task`) chạy ngầm ngay sau khi quá trình upload sách và trích xuất cấu trúc chương (`BookSection`) thành công.
  * Bản tóm tắt sau khi sinh ra được lưu vĩnh viễn vào trường `ai_summary` (JSON) trong Postgres DB.
  * API `GET /api/v1/books/{id}/summary` phía Client (FE) sẽ đọc trực tiếp từ DB cache với tốc độ siêu nhanh **< 20ms**.

### 1.2. Kiểm soát ngưỡng Token (Token Budget Safeguard - `TOTAL_TOKEN_LIMIT = 800_000`)
* **Vấn đề thực tế:** Giới hạn Context Window tối đa của Gemini 2.5 Flash là 1.000.000 tokens. Nếu một bộ sách hoặc giáo trình siêu dày vượt quá 1 triệu tokens, API Gemini sẽ ném ra lỗi `400 Bad Request: context_length_exceeded`.
* **Giải pháp Senior (Cơ chế Phòng thủ 2 Lớp):**
  * Đặt ngưỡng trần an toàn: **`TOTAL_TOKEN_LIMIT = 800_000` tokens** (~3.2 triệu ký tự).
  * **Luồng A (Single-Pass Full-Context):** Nếu `estimated_tokens <= 800_000` (chiếm 99.5% sách thông thường), nạp 100% nội dung sách từ tất cả các `BookSection` vào Gemini 2.5 Flash trong 1 Prompt duy nhất để cho ra chất lượng tóm tắt Overview sâu sắc nhất.
  * **Luồng B (Section Outline Compression Fallback):** Nếu `estimated_tokens > 800_000`, tự động nén dữ liệu bằng cách chỉ nạp Tiêu đề chương + 400 ký tự tóm tắt mở đầu của từng chương (~10k tokens) để đảm bảo **không bao giờ bị tràn Context**.

### 1.3. Cơ chế Retry tự động và Xử lý Lỗi Resilient (Automatic Retry & Backoff)
* **Quy định kích hoạt:** Task chỉ được kích hoạt **SAU KHI** upload sách thành công và cây danh mục chương (`BookSection`) đã được lưu thành công vào Database.
* **Chính sách Thử lại (Retry Policy):** Khi xảy ra sự cố mạng chập chờn hoặc API Gemini bận:
  * Celery Task tự động thử lại tối đa **2 lần** (`max_retries=2`), mỗi lần cách nhau **15 giây** (`default_retry_delay=15`).
  * Nếu cả 3 lần (1 lần chạy chính + 2 lần retry) đều thất bại, Worker sẽ chuyển trạng thái `ai_summary_status = "failed"` và ghi nhận lỗi vào `ai_summary_error` để FE hiển thị giao diện báo lỗi mượt mà kèm nút **"Thử lại"** (Regenerate).

---

## 2. Thiết Kế Cơ Sở Dữ Liệu & API Contract (Database & API Specs)

### 2.1. Cập nhật Model Database (`app/models/db_models.py`)

Thêm 3 trường mới vào bảng `Book`:

```python
ai_summary: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
ai_summary_status: str = Field(default="pending", sa_column=Column(String, nullable=False, server_default="pending"))
ai_summary_error: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
```

### 2.2. Schema Phản Hồi Chuẩn JSON (Response Schema)

```json
{
  "book_id": "1827c581-997e-413e-b8d3-4d1091cf898c",
  "status": "completed",
  "ai_summary": {
    "book_title": "The Mystery of Moon Castle",
    "author": "Enid Blyton",
    "summary": "Nội dung tóm tắt tổng quan toàn bộ cuốn sách...",
    "main_characters": [
      "Mike Arnold",
      "Jack",
      "Prince Paul"
    ],
    "setting": [
      "Lâu đài Moon Castle",
      "Mỏ thiếc cổ"
    ],
    "major_themes": [
      "Phiêu lưu và khám phá",
      "Tình bạn và lòng dũng cảm"
    ],
    "key_takeaways": [
      "Sự tò mò và lòng dũng cảm dẫn đến những khám phá vĩ đại.",
      "Tình bạn là chìa khóa vượt qua mọi thử thách."
    ]
  },
  "error_message": null
}
```

---

## 3. Hướng Dẫn Hiện Thực Mã Nguồn Chi Tiết (Code Implementation Steps)

### Bước 3.1: Bổ sung cấu hình và Enum hằng số

Trong `app/core/config.py`:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AI Summary Configs
    TOTAL_TOKEN_LIMIT: int = 800_000
    AI_SUMMARY_MAX_RETRIES: int = 2
    AI_SUMMARY_RETRY_DELAY_SECONDS: int = 15
```

Trong `app/core/constant.py`:
```python
from enum import Enum

class SummaryStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
```

---

### Bước 3.2: Ánh xạ Routing Celery Task trong [app/core/celery_app.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/celery_app.py)

Bổ sung task `triam.books.generate_summary` vào `task_routes`:

```python
    task_routes={
        "triam.books.process": {"queue": "document"},
        "triam.books.switch_mode": {"queue": "document"},
        "triam.books.index_sections": {"queue": "document"},
        "triam.books.purge_storage_assets": {"queue": "document"},
        "triam.books.generate_summary": {"queue": "document"},
        "triam.notifications.scan_due": {"queue": "maintenance"},
        "triam.notifications.deliver_due": {"queue": "notification"},
    },
```

---

### Bước 3.3: Tạo Service Tóm Tắt Sách [app/services/book_summary_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/book_summary_service.py)

*Lưu ý: Tất cả các câu lệnh `import` phải đặt ở đầu file theo chuẩn PEP 8. Không dùng hardcode string.*

```python
import json
import time
from typing import List, Optional
import uuid

from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from sqlmodel import Session, select, col

from app.core.config import settings
from app.core.constant import SummaryStatus
from app.core.logger import log
from app.models.db_models import Book, BookSection, BookSectionKnowledge

# Schema Structured Output cho Pydantic Parser (Khớp 1-1 với FE Flutter UI)
class BookSummarySchema(BaseModel):
    key_idea: str = Field(description="Ý tưởng chính tổng quan nhất của cuốn sách (Khớp FE 'Ý tưởng chính').")
    target_audience: str = Field(description="Đối tượng độc giả phù hợp nhất để đọc cuốn sách này (Khớp FE 'Đối tượng phù hợp').")
    estimated_read_minutes: int = Field(description="Thời gian đọc ước tính tính bằng phút (Khớp FE 'Thời gian đọc ước tính').")
    key_takeaways: List[str] = Field(description="Top 5-7 bài học / đánh giá cốt lõi đắt giá nhất (Khớp FE 'Đánh giá tổng quan').")
    summary: str = Field(description="Bản tóm tắt tổng quan toàn bộ cốt truyện và thông điệp của cuốn sách.")
    main_characters: List[str] = Field(description="Danh sách các nhân vật chính.")


async def generate_ai_book_summary(session: Session, book_id: uuid.UUID) -> dict:
    """Hàm xử lý nghiệp vụ chính: Kiểm tra token budget, gọi Gemini 2.5 Flash và lưu DB."""
    book = session.get(Book, book_id)
    if not book:
        raise ValueError(f"Book not found | book_id={book_id}")

    # Lấy toàn bộ các đoạn kiến thức / chương của sách theo đúng thứ tự
    statement = (
        select(BookSectionKnowledge)
        .join(BookSection, BookSectionKnowledge.section_id == BookSection.id)
        .where(BookSectionKnowledge.book_id == book_id)
        .order_by(col(BookSection.section_index).asc(), col(BookSectionKnowledge.chunk_index).asc())
    )
    chunks = session.exec(statement).all()

    if not chunks:
        # Nếu chưa có chunk kiến thức, lấy trực tiếp từ bảng book_sections
        sections = session.exec(
            select(BookSection).where(BookSection.book_id == book_id).order_by(col(BookSection.section_index).asc())
        ).all()
        full_text = "\n\n".join([f"[{s.title}]\n{s.text_content or ''}" for s in sections if s.text_content])
    else:
        full_text = "\n\n".join([c.content for c in chunks if c.content])

    word_count = len(full_text.split())
    estimated_tokens = int(word_count * 1.3)
    log.info(f"Book summary generation started | book_id={book_id} | estimated_tokens={estimated_tokens:,}")

    # Kiểm tra Token Ceiling Safeguard (800,000 Tokens)
    if estimated_tokens > settings.TOTAL_TOKEN_LIMIT:
        log.warning(f"Tokens exceed ceiling ({estimated_tokens:,} > {settings.TOTAL_TOKEN_LIMIT:,}). Fallback to Section Outlines.")
        sections = session.exec(
            select(BookSection).where(BookSection.book_id == book_id).order_by(col(BookSection.section_index).asc())
        ).all()
        full_text = "\n\n".join([f"[{s.title}]\n{(s.text_content or '')[:400]}" for s in sections])

    client = AsyncOpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=settings.GEMINI_BASE_URL,
        timeout=120.0,
    )

    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert literary analyst and executive book summarizer.\n"
                "Your task is to read the provided text of the book and extract a structured executive summary in raw JSON format.\n\n"
                "CRITICAL GROUNDING CONSTRAINTS:\n"
                "1. Base your summary STRICTLY AND EXCLUSIVELY on the provided book text.\n"
                "2. DO NOT hallucinate, infer, or fabricate any details, facts, plot points, or character traits not explicitly mentioned in the text.\n"
                "3. If any field cannot be explicitly determined from the text, set its string value to 'Chưa có thông tin' (or an empty array [] for list fields).\n"
                "4. Write the summary values in fluent, natural Vietnamese for direct display on the mobile app UI.\n"
                "5. Output ONLY valid raw JSON matching the required schema without Markdown code blocks."
            ),
        },
        {"role": "user", "content": f"Here is the complete content of the book:\n\n{full_text}\n\nProvide the executive summary in valid JSON format."},
    ]

    start_time = time.perf_counter()
    completion = await client.chat.completions.create(
        model=settings.GEMINI_MODEL_LLM,
        messages=prompt_messages,
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    elapsed_seconds = time.perf_counter() - start_time
    log.info(f"Gemini 2.5 Flash summary complete | book_id={book_id} | elapsed={elapsed_seconds:.2f}s")

    raw_output = completion.choices[0].message.content.strip()

    # Stripping markdown JSON wrappers if present
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`").strip()
        if raw_output.lower().startswith("json"):
            raw_output = raw_output[4:].strip()

    # Parse JSON
    try:
        raw_dict = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        log.error(f"Failed to parse LLM response JSON | book_id={book_id} | raw={raw_output[:200]}")
        raise LLMResponseFormatError("Kết quả trả về từ Gemini không phải là chuỗi JSON hợp lệ.") from exc

    # Validate cấu trúc dữ liệu theo Pydantic Schema
    try:
        validated_summary = BookSummarySchema.model_validate(raw_dict)
        result_dict = validated_summary.model_dump()
    except ValidationError as val_err:
        log.error(f"LLM JSON schema validation failed | book_id={book_id} | error={val_err}")
        # Nếu thiếu các trường bắt buộc, raise LLMResponseFormatError để Celery tự động Retry
        raise LLMResponseFormatError("Dữ liệu tóm tắt AI từ Gemini thiếu các trường bắt buộc.") from val_err

    # Cập nhật DB khi dữ liệu đã qua kiểm duyệt chuẩn 100%
    book.ai_summary = result_dict
    book.ai_summary_status = SummaryStatus.COMPLETED.value
    book.ai_summary_error = None
    session.add(book)
    session.commit()
    session.refresh(book)

    return result_dict
```

---

### Bước 3.4: Định nghĩa Celery Task với Retry Policy [app/tasks/book_tasks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/tasks/book_tasks.py)

Bổ sung task `generate_book_summary_task` với decorator retry tự động 2 lần:

```python
import asyncio
import uuid
from sqlmodel import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.constant import SummaryStatus
from app.core.logger import log
from app.db.database import engine
from app.models.db_models import Book
from app.services.book_summary_service import generate_ai_book_summary


@celery_app.task(
    name="triam.books.generate_summary",
    bind=True,
    max_retries=settings.AI_SUMMARY_MAX_RETRIES,
    default_retry_delay=settings.AI_SUMMARY_RETRY_DELAY_SECONDS,
)
def generate_book_summary_task(self, book_id: str) -> None:
    """Celery Background Worker: Sinh bản tóm tắt AI cho sách.
    Tự động retry tối đa 2 lần (mỗi lần cách 15s) nếu gặp sự cố.
    """
    log.info(f"Celery generate_book_summary_task started | book_id={book_id} | attempt={self.request.retries + 1}")
    parsed_book_id = uuid.UUID(book_id)

    with Session(engine) as session:
        book = session.get(Book, parsed_book_id)
        if not book:
            log.error(f"Generate summary task skipped: Book not found | book_id={book_id}")
            return

        # Đánh dấu trạng thái đang xử lý
        book.ai_summary_status = SummaryStatus.PROCESSING.value
        session.add(book)
        session.commit()

        try:
            asyncio.run(generate_ai_book_summary(session, parsed_book_id))
            log.info(f"Celery generate_book_summary_task completed successfully | book_id={book_id}")
        except Exception as exc:
            log.warning(f"Celery generate_book_summary_task failed (attempt {self.request.retries + 1}) | error={exc}")
            if self.request.retries < self.max_retries:
                raise self.retry(exc=exc)
            else:
                # Đã hết 2 lần retry, cập nhật trạng thái FAILED để FE hiển thị giao diện báo lỗi
                log.error(f"Celery generate_book_summary_task permanently failed after max retries | book_id={book_id}")
                book.ai_summary_status = SummaryStatus.FAILED.value
                book.ai_summary_error = f"Không thể tạo tóm tắt AI sau {self.max_retries + 1} lần thử: {str(exc)}"
                session.add(book)
                session.commit()
```

---

### Bước 3.5: Kích hoạt Task trong Luồng Upload Sách [app/services/upload_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/upload_service.py)

1. **Thêm import ở đầu tệp `app/services/upload_service.py`:**
```python
from app.tasks.book_tasks import generate_book_summary_task
```

2. **Kích hoạt Celery Task trong hàm `handle_upload_document` ngay sau khi các `BookSection` đã được trích xuất và lưu DB thành công:**

```python
    # Sau khi lưu Book (READY) và BookSection thành công vào DB:
    try:
        generate_book_summary_task.delay(str(book.id))
        logger.info(f"Enqueued background AI summary task | book_id={book.id}")
    except Exception as exc:
        logger.warning(f"Failed to enqueue summary task (will allow manual regenerate): {exc}")
```

---

### Bước 3.6: Khai báo API Endpoints Trong [app/api/v1/routers/audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py)

```python
@router.get("/books/{book_id}/summary")
def get_book_ai_summary(
    book_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """API lấy bản tóm tắt AI của sách (Cache-first từ DB < 20ms)."""
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, current_user.id)
    if not book:
        raise BookNotFoundError()

    return {
        "book_id": book.id,
        "status": book.ai_summary_status,
        "ai_summary": book.ai_summary,
        "error_message": book.ai_summary_error,
    }


@router.post("/books/{book_id}/summary/regenerate")
def regenerate_book_ai_summary(
    book_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """API yêu cầu tạo lại bản tóm tắt AI dưới nền."""
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, current_user.id)
    if not book:
        raise BookNotFoundError()

    book.ai_summary_status = SummaryStatus.PENDING.value
    book.ai_summary_error = None
    session.add(book)
    session.commit()

    generate_book_summary_task.delay(str(book.id))
    return {"message": "Đã gửi yêu cầu tạo lại tóm tắt AI dưới nền.", "status": "pending"}
```

---

## 4. Hướng Dẫn Từng Bước Cho Fresher (Step-by-Step Training Guide)

### 4.1. Tại sao phải để `import` ở đầu file?
* Sau chuẩn **PEP 8**, việc đặt câu lệnh `import` ở đầu file giúp các công cụ kiểm tra tĩnh (Linter, MyPy) phát hiện sớm các phụ thuộc bị thiếu, tránh lỗi đệ quy vòng (circular import) và giúp code sáng rõ.

### 4.2. Tại sao không được Hardcode String?
* Nếu bạn viết chữ `"pending"`, `"failed"` rải rác khắp code, khi cần đổi chữ `"failed"` thành `"error"`, bạn sẽ gõ thiếu hoặc gõ sai chính tả ở một nơi nào đó dẫn tới bug ngầm. Sử dụng Enum `SummaryStatus.FAILED.value` hoặc `settings.TOTAL_TOKEN_LIMIT` giúp quản lý hằng số tập trung tại một nơi duy nhất.

### 4.3. Cách hoạt động của `self.retry(exc=exc)` trong Celery Worker
* Khi gặp ngoại lệ mạng (như đứt kết nối Gemini), Celery bắt lấy `exc` và hoãn task lại `15 giây` (`default_retry_delay`). Khi hết 15s, Celery Worker sẽ tự động thực thi lại task. Nếu quá 2 lần thử lại (`max_retries=2`), Celery dừng retry và nhảy vào khối `else:` để ghi nhận trạng thái lỗi `FAILED` vào Database cho FE hiển thị.

---

## 5. Kế Hoạch Kiểm Thử Tự Động (Verification & Test Plan)

Tạo file test mới `tests/services/test_phase26_ai_book_summary.py`:

1. `test_book_summary_token_budget_ceiling`: Kiểm tra hàm tự động kích hoạt chế độ nén khi token vượt quá 800.000.
2. `test_celery_task_retry_and_failure_state`: Kiểm tra Celery Worker cập nhật đúng trạng thái `FAILED` và `ai_summary_error` khi thử lại 2 lần thất bại.
3. `test_get_summary_cache_first_response`: Kiểm tra API `/books/{id}/summary` trả về dữ liệu nhanh trong < 20ms từ DB Cache.
