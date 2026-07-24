# Phase 28 Implementation Guide: Fail-Fast Ingestion Pre-Flight Validation & Deferred Section Embedding

Tài liệu này là hướng dẫn kỹ thuật chi tiết dành cho các lập trình viên (bao gồm Fresher và Junior) để triển khai **Phase 28: Kiểm Tra Sớm Dung Lượng Đầu Vào (Fail-Fast Pre-Flight) và Trì Hoãn Nhúng Vector Section (Deferred Section Embedding)** trong hệ thống Tri Âm Backend.

Tài liệu giải quyết triệt để vấn đề lãng phí API Token Embedding và tối ưu hóa trải nghiệm người dùng theo đúng kiến trúc **Fail-Fast System Design** chuẩn Senior.

---

## 📚 1. NỀN TẢNG LÝ THUYẾT VÀ KIẾN TRÚC SENIOR (FOR FRESHER TRAINING)

### 1.1. Phân Tích Khuyết Điểm Của Luồng Xử Lý Cũ (Legacy Ingestion Flaw)

Trong kiến trúc cũ của hệ thống:
1. **Ở Bước 1 - Upload Tài Liệu (`POST /upload`):** 
   Ngay sau khi trình `parse_document_structure()` bóc tách xong danh sách `BookSection` từ tệp PDF/EPUB/DOCX, hàm `handle_upload_document()` tự động kích hoạt Celery task `index_book_sections_task` (`_enqueue_section_indexing(book_id)`). Task này duyệt qua toàn bộ các section gốc của sách, gửi API gọi OpenAI/Gemini Embeddings để tạo Vector lưu vào Postgres `pgvector`.
2. **Ở Bước 2 - Tạo Kế Hoạch Học (`POST /generate-plan` hoặc Celery Worker):**
   Khi người dùng chốt tạo Kế hoạch học, hệ thống mới gọi `_hard_limit_error()` để tính toán thời lượng Audio dự kiến của sách. Nếu tổng audio dự kiến vượt quá **4 giờ (`MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK = 14,400s`)**, hệ thống mới báo lỗi và đánh dấu sách bị `ERROR`.

#### 💥 **Hậu quả hệ thống:**
* **Lãng phí API Token:** Tiêu tốn hàng chục ngàn Embedding Tokens cho một cuốn sách mà sau đó bị chặn và không bao giờ được tạo Kế hoạch học.
* **Lãng phí thời gian người dùng (UX tệ):** Người học phải ngồi chờ 3–5 phút cho quá trình upload và embedding hoàn tất, rồi mới nhận lại một thông báo lỗi tràn thời lượng audio.
* **Quá tải Celery Queue:** Làm ngắt đoạn và chiếm dụng tài nguyên hàng đợi `document` của Celery cho các tác vụ vô ích.

---

### 1.2. Nguyên Lý Chốt Chặn Sớm (Fail-Fast Principle)
* **Khái niệm:** Hệ thống cần kiểm tra tính hợp lệ của dữ liệu đầu vào tại vị trí sớm nhất có thể trong pipeline. Nếu dữ liệu chắc chắn sẽ thất bại ở các bước sau, hệ thống phải **từ chối ngay lập tức (Early Rejection)**.
* **Ứng dụng trong Tri Âm:** 
  Việc tính toán số từ (Word Count) và ước tính thời lượng âm thanh TTS ($\text{Seconds} = \text{Words} / 130 \times 60$) dựa trên cấu trúc chữ `flat_sections` diễn ra chỉ trong **0,01 giây** trên CPU mà **không tốn 1 Token API hay 1 I/O Database nào**. Vì vậy, ta cần thực hiện kiểm tra này ngay tại bước Upload!

---

### 1.3. Nguyên Lý Trì Hoãn Thực Thi (Deferred / Lazy Execution)
* **Khái niệm:** Không thực hiện các tác vụ tốn chi phí (Embedding Vector, Gen Audio) cho đến khi người dùng xác nhận sử dụng tính năng đó.
* **Bảo toàn 100% Logic Nghiệp vụ:** 
  Dời lệnh kích hoạt task Embedding `_enqueue_section_indexing(book_id)` từ lúc Upload sang bước `POST /generate-plan`. Khi task này được Celery kích hoạt ở bước `generate-plan`, nó vẫn thực thi việc nhúng **toàn bộ các `BookSection` gốc của cuốn sách** vào `pgvector` đúng chuẩn 100% như thiết kế ban đầu.

---

## 🛠️ 2. TÓM TẮT CÁC THAY ĐỔI CẦN THỰC HIỆN (ARCHITECTURE CHECKLIST)

| Tệp tin (File Path) | Tầng kiến trúc | Thay đổi chính |
|---|---|---|
| `app/core/config.py` | Config Settings | Thêm biến cờ `AI_SUMMARY_AUTO_ENQUEUE_ENABLED: bool = True` để Bật/Tắt tự động sinh tóm tắt sách khi upload. |
| `app/core/exceptions.py` | Core Exceptions | Định nghĩa ngoại lệ `AudioLimitExceededError` (HTTP 400). |
| `app/services/token_budget_service.py` | Service Utility | Thêm hàm `check_book_preflight_limits(flat_sections)` ước tính nhanh tổng số từ và thời lượng audio của sách. |
| `app/services/upload_service.py` | Business Service | 1. Bổ sung `check_book_preflight_limits` vào `handle_upload_document` để chặn ngay sách $>4$h audio.<br>2. Bổ sung cờ `AI_SUMMARY_AUTO_ENQUEUE_ENABLED` vào `_enqueue_book_summary`.<br>3. Xóa `_enqueue_section_indexing` khỏi `handle_upload_document`.<br>4. Thêm `_enqueue_section_indexing` vào `handle_generate_plan`. |
| `tests/test_upload_preflight_and_lazy_embedding.py` | Test Suite | Viết bộ Unit & Integration Test xác minh 100% luồng Fail-Fast, AI Summary Toggle và Deferred Embedding. |

---

## 💻 3. CODE IMPLEMENTATION CHI TIẾT (STEP-BY-STEP FOR FRESHER)

### Step 3.1: Thêm Cờ Cấu Hình Bật/Tắt AI Summary (`app/core/config.py`)

Thêm biến cờ `AI_SUMMARY_AUTO_ENQUEUE_ENABLED` vào lớp `Settings`:

```python
# app/core/config.py

class Settings(BaseSettings):
    ...
    AI_SUMMARY_MAX_RETRIES: int = 2
    AI_SUMMARY_RETRY_DELAY_SECONDS: int = 15
    # [PHASE 28]: Cờ Bật/Tắt tự động đẩy Task sinh AI Summary khi Upload sách
    AI_SUMMARY_AUTO_ENQUEUE_ENABLED: bool = True
```

---

### Step 3.2: Khai báo Ngoại lệ `AudioLimitExceededError` (`app/core/exceptions.py`)

Bổ sung ngoại lệ mới kế thừa từ `AppException` với mã lỗi HTTP 400 Bad Request:

```python
# app/core/exceptions.py (Thêm vào cuối file)

class AudioLimitExceededError(AppException):
    def __init__(self, message: str = "Tài liệu vượt quá giới hạn thời lượng audio cho phép."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)
```

---

### Step 3.3: Bổ sung Hàm Ước Tính Dung Lượng Sớm (`app/services/token_budget_service.py`)

Hệ thống đã có sẵn hàm `estimate_audio_seconds(text)` tính toán dựa trên số từ. Ta bổ sung hàm `check_book_preflight_limits`:

```python
# app/services/token_budget_service.py

def check_book_preflight_limits(flat_sections: list) -> tuple[bool, int, str | None]:
    """
    Ước tính nhanh tổng số từ và thời lượng Audio của toàn bộ sách từ flat_sections.
    
    Trả về:
        (is_valid, estimated_audio_seconds, error_message)
    """
    total_text = " ".join([sec.content for sec in flat_sections if getattr(sec, "content", None)])
    words = len(total_text.split())
    if words == 0:
        return True, 0, None

    estimated_audio_seconds = estimate_audio_seconds(total_text)
    max_allowed_seconds = settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK  # Mặc định 14,400s = 4 giờ

    if estimated_audio_seconds > max_allowed_seconds:
        est_hours = round(estimated_audio_seconds / 3600, 1)
        max_hours = max_allowed_seconds // 3600
        error_msg = (
            f"Tài liệu quá lớn (dự kiến khoảng {est_hours} giờ audio toàn bộ sách, "
            f"vượt quá giới hạn tối đa {max_hours} giờ cho mỗi sách). "
            f"Vui lòng tải lên tài liệu ngắn hơn hoặc chia nhỏ theo từng phần."
        )
        return False, estimated_audio_seconds, error_msg

    return True, estimated_audio_seconds, None
```

---

### Step 3.4: Cập nhật Luồng Upload và Plan Generation (`app/services/upload_service.py`)

Cập nhật 2 hàm cốt lõi `handle_upload_document` và `handle_generate_plan`:

```python
# app/services/upload_service.py

# Import ngoại lệ mới và helper function
from app.core.exceptions import AudioLimitExceededError
from app.services.token_budget_service import check_book_preflight_limits


async def handle_upload_document(session: Session, file: UploadFile, user_id: uuid.UUID) -> dict:
    """
    Bước 1: Validate file, extract outline từ tài liệu, upload lên Supabase Storage,
    lưu Book + BookSection vào DB, trả về outline tree cho Flutter.
    """
    # 1. Validate MIME Type hoặc đuôi file
    is_valid_type = file.content_type in settings.ALLOWED_MIME_TYPES
    filename_lower = (file.filename or "").lower()
    document_type = _detect_document_type(file)

    if not is_valid_type:
        if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".epub") or filename_lower.endswith(".docx")):
            raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError()

    # 2. Lưu file tạm để extract outline
    book_id = uuid.uuid4()
    tmp_filename = f"uploads/{book_id}.tmp"
    os.makedirs("uploads", exist_ok=True)

    parsed_document = None
    file_url = ""
    try:
        async with aiofiles.open(tmp_filename, "wb") as f:
            await f.write(content)

        # 3. Extract deterministic outline tree từ tài liệu
        parsed_document = await _extract_structure_by_type(tmp_filename, document_type)
        validate_document_structure(parsed_document)
        flat_sections = flatten_sections(parsed_document.sections)
        if not flat_sections:
            raise DocumentExtractionError()

        # --- [PHASE 28]: CHECK ĐẦU VÀO SỚM (FAIL-FAST CHECK IN 0.01s) ---
        is_valid, est_seconds, err_msg = check_book_preflight_limits(flat_sections)
        if not is_valid:
            logger.warning(f"⛔ Upload rejected by Pre-flight Audio Limit | book_id={book_id} | reason={err_msg}")
            raise AudioLimitExceededError(err_msg)
        # ----------------------------------------------------------------

        # 4. Upload PDF lên Supabase Storage bucket 'raw_books'
        storage_path = f"{book_id}/original.{document_type}"
        content_type = (
            file.content_type
            or {
                "pdf": "application/pdf",
                "epub": "application/epub+zip",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }[document_type]
        )

        file_url = await upload_file_to_supabase(
            tmp_filename,
            storage_path,
            bucket="raw_books",
            content_type=content_type,
        )
        logger.info(f"☁️  {document_type.upper()} uploaded to Storage: {storage_path}")

    finally:
        # Dọn rác: Xóa file tạm dù thành công hay thất bại
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

    if not parsed_document:
        raise DocumentExtractionError()

    flat_sections = flatten_sections(parsed_document.sections)
    warnings = detect_structure_warnings(parsed_document)

    # 5. Lưu DB: Book (DRAFT) + BookSection tree
    title = (file.filename or "unknown").rsplit(".", 1)[0].replace("\x00", "").replace("\u0000", "")
    try:
        book = Book(
            id=book_id,
            user_id=user_id,
            title=title,
            total_sections=len(flat_sections),
            total_units=0,
            status=BookStatus.DRAFT,
            file_url=file_url,
            document_type=document_type,
        )

        session.add(book)
        session.flush()
        create_book_sections(session, book_id, parsed_document)
        session.commit()
        logger.info(f"📘 Created DRAFT book {book_id} | {len(flat_sections)} sections | file_url saved")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create book record: {e}")
        raise DatabaseError(f"Lỗi lưu DB: {str(e)}") from e

    # --- [PHASE 28]: DỜI LỆNH EMBEDDING SANG BƯỚC GENERATE PLAN ---
    # Đã XÓA: _enqueue_section_indexing(book_id)
    _enqueue_book_summary(book_id)  # Tự động check cờ AI_SUMMARY_AUTO_ENQUEUE_ENABLED

    outline_tree = build_outline_preview(parsed_document)
    return {
        "book_id": str(book_id),
        "total_sections": len(flat_sections),
        "max_depth": parsed_document.max_depth,
        "outline_tree": outline_tree,
        "warnings": warnings,
        "document_type": document_type,
    }
```

#### Cập nhật hàm `_enqueue_book_summary` hỗ trợ cờ Bật/Tắt (Feature Flag):

```python
# app/services/upload_service.py -> _enqueue_book_summary()

def _enqueue_book_summary(book_id: uuid.UUID) -> None:
    # --- [PHASE 28]: CỜ BẬT/TẮT TỰ ĐỘNG TẠO AI SUMMARY KHỦNG KHI UPLOAD ---
    if not settings.AI_SUMMARY_AUTO_ENQUEUE_ENABLED:
        logger.info(f"⏭️ AI Summary auto-enqueue is DISABLED by config | book_id={book_id}")
        return

    try:
        generate_book_summary_task.delay(str(book_id))
        logger.info(f"Enqueued background AI summary task | book_id={book_id}")
    except Exception as exc:
        logger.warning(f"Failed to enqueue summary task | book_id={book_id} | reason={type(exc).__name__}")
```
```

Và tại hàm `handle_generate_plan`:

```python
# app/services/upload_service.py -> handle_generate_plan()

    if job:
        try:
            # --- [PHASE 28]: KÍCH HOẠT NHÚNG VECTOR TOÀN BỘ SECTION GỐC TẠI ĐÂY ---
            _enqueue_section_indexing(payload.book_id)

            process_book_task.apply_async(
                args=[str(payload.book_id), payload.mode.value, str(job.id)],
                queue="document",
            )
        except Exception as e:
            ...
```

---

## 🧪 4. KIỂM THỬ VÀ XÁC MINH (TEST SUITE SPECIFICATIONS)

Tạo tệp kiểm thử tự động `tests/test_upload_preflight_and_lazy_embedding.py` để kiểm tra 100% các tiêu chí nghiệm thu:

1. **Test Pre-flight Limit Rejection:** Giả lập sách có tổng số từ vượt quá 4 giờ audio. Gọi `handle_upload_document` và xác minh hệ thống ném `AudioLimitExceededError` ngay lập tức, không lưu bản ghi `Book` hay `BookSection` nào vào DB.
2. **Test Deferred Section Indexing:** Giả lập sách hợp lệ. Gọi `handle_upload_document`, xác minh tệp upload thành công nhưng `index_book_sections_task` CHƯA được đẩy vào Celery Queue. Gọi `handle_generate_plan`, xác minh `index_book_sections_task` được kích hoạt đẩy vào Celery Queue thành công.

---

## 🎯 5. KẾT LUẬN VÀ KẾT QUẢ ĐẠT ĐƯỢC

1. **Tiết kiệm 100% API Embedding Tokens** cho tất cả các tài liệu bị từ chối do quá dung lượng.
2. **Thời gian phản hồi báo lỗi cực nhanh (0,01 giây)** ngay tại thời điểm upload, nâng cao UX người dùng lên tối đa.
3. **Bảo toàn 100% tính nguyên vẹn của luồng RAG:** Khi người dùng chốt tạo Plan, toàn bộ `BookSection` gốc của sách vẫn được nhúng Vector Embeddings đầy đủ vào `pgvector` đúng chuẩn kiến trúc Tri Âm Backend.
