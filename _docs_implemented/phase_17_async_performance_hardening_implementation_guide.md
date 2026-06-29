# Phase 17: Async Event Loop Hardening & Performance Hardening

Tài liệu này hướng dẫn chi tiết cách cải thiện hiệu năng và bảo vệ Event Loop của ứng dụng `triam-backend` khỏi tình trạng bị chặn (blocking) bởi các tác vụ nặng về CPU (Document Parsing) hoặc các tác vụ I/O mạng đồng bộ (Supabase API, Database writes in loops) tương tự như giải pháp an toàn trong luồng Reranker.

---

## 📌 Các vấn đề chính được xử lý
1. **CPU-bound Event Loop Blocking:** Phân tách các tiến trình phân tích tài liệu nặng (`pdfplumber`, `ebooklib`, `python-docx`) ra khỏi luồng Event Loop chính của FastAPI bằng `asyncio.to_thread`.
2. **Sync Network I/O in Async Context:** Chuyển các tác vụ tải lên và xóa tệp tin đồng bộ của Supabase SDK sang chạy song song trong Thread Pool.
3. **Frequent Database Write blocking in Async Workers:** Giảm thiểu nghẽn luồng nền bằng cách đẩy các tác vụ ghi DB đồng bộ của background workers vào Thread Pool.
4. **LLM Client Timeouts:** Bổ sung timeout ở cấp độ Client cho các API LLM (Gemini/OpenAI) để phòng tránh treo worker vô hạn.

---

## 🛠️ Hướng dẫn cập nhật chi tiết từng File

### 1. Cấu hình Timeout cho LLM Client
Bổ sung `timeout` mặc định khi khởi tạo `AsyncOpenAI` client để bảo vệ ứng dụng khỏi nguy cơ Socket hang.

#### 1.1. MODIFY [llm_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/llm_service.py)
*   **Vị trí:** Dòng 17
*   **Mã nguồn thay đổi:**
```python
# Cũ:
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Mới (Clean & Robust):
client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0  # Cấu hình timeout mặc định 60 giây ở cấp độ client
)
```

#### 1.2. MODIFY [pareto_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pareto_planner_service.py)
*   **Vị trí:** Dòng 19
*   **Mã nguồn thay đổi:**
```python
# Cũ:
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Mới (Clean & Robust):
client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0  # Cấu hình timeout mặc định 60 giây ở cấp độ client
)
```

---

### 2. Tối ưu hóa Document Parser (Giải phóng CPU-bound)
Chuyển đổi các hàm phân tích cấu trúc tài liệu từ `async def` sang `def` đồng bộ, và sử dụng `asyncio.to_thread` trong bộ điều phối chung. Thao tác này cũng truyền dữ liệu dưới dạng `bytes` độc lập để đảm bảo an toàn đa luồng (thread-safety).

#### 2.1. MODIFY [pdf_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pdf_service.py)
*   **Vị trí:** Dòng 159
*   **Mã nguồn thay đổi:**
```python
# Cũ:
async def parse_pdf_structure(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    ...

# Mới: Chuyển thành hàm đồng bộ thuần túy nhận vào BytesIO
def parse_pdf_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    outline_tree = _read_pdf_outline_tree(file_obj)
    outline_items = flatten_sections(outline_tree)

    if not outline_items or len(outline_items) <= 1:
        raise DocumentOutlineRequiredError(
            "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
        )

    file_obj.seek(0)
    text_by_path: dict[str, tuple[str, int | None]] = {}

    try:
        with pdfplumber.open(file_obj) as pdf:
            ordered_items = sorted(
                enumerate(outline_items),
                key=_pdf_outline_sort_key,
            )

            for i, (_, current_section) in enumerate(ordered_items):
                next_section = ordered_items[i + 1][1] if i < len(ordered_items) - 1 else None
                chapter_text, section_page_end = _extract_section_text_from_pdf(pdf, current_section, next_section)
                text_by_path[current_section.path] = (chapter_text, section_page_end)

    except DocumentOutlineRequiredError:
        raise
    except Exception as exc:
        raise PdfExtractionError(f"Không thể đọc nội dung PDF: {exc}") from exc

    sections = [_replace_section_text(section, text_by_path) for section in outline_tree]
    if not has_extractable_text(sections):
        raise PdfExtractionError(
            "PDF có outline nhưng không trích xuất được text. File có thể là scan ảnh hoặc bị lỗi."
        )

    return ParsedDocument(document_type="pdf", sections=sections)
```

#### 2.2. MODIFY [epub_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/epub_service.py)
*   **Vị trí:** Dòng 83
*   **Mã nguồn thay đổi:**
```python
# Cũ:
async def parse_epub_structure(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    ...

# Mới: Chuyển thành hàm đồng bộ thuần túy
def parse_epub_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)

    try:
        book = epub.read_epub(BytesIO(file_obj.read()))
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc EPUB: {exc}") from exc

    documents_by_href = {item.get_name(): item.get_content() for item in book.get_items_of_type(ITEM_DOCUMENT)}
    sections = _epub_toc_tree(book.toc, documents_by_href)
    if not sections:
        raise DocumentOutlineRequiredError("EPUB không có mục lục điều hướng hợp lệ. Vui lòng upload EPUB có TOC chuẩn.")

    if not has_extractable_text(sections):
        raise DocumentExtractionError("EPUB có mục lục nhưng không trích xuất được text. File có thể bị lỗi hoặc không phải text-based EPUB.")

    return ParsedDocument(document_type="epub", sections=sections)
```

#### 2.3. MODIFY [docx_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/docx_service.py)
*   **Vị trí:** Dòng 92
*   **Mã nguồn thay đổi:**
```python
# Cũ:
async def parse_docx_structure(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    ...

# Mới: Chuyển thành hàm đồng bộ thuần túy
def parse_docx_structure_sync(file_obj) -> ParsedDocument:
    file_obj.seek(0)

    try:
        document = Document(file_obj)
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc DOCX: {exc}") from exc

    roots: list[_SectionBuilder] = []
    stack: list[_SectionBuilder] = []
    sibling_counts: dict[str, int] = {"": 0}

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        if _is_heading(paragraph):
            level = _heading_level(paragraph) or 1
            while stack and stack[-1].level >= level:
                stack.pop()

            parent = stack[-1] if stack else None
            parent_path = parent.path if parent else ""
            sibling_counts[parent_path] = sibling_counts.get(parent_path, 0) + 1
            order_index = sibling_counts[parent_path] - 1
            path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
            builder = _SectionBuilder(title=text, level=level, order_index=order_index, path=path)

            if parent:
                parent.children.append(builder)
            else:
                roots.append(builder)

            stack.append(builder)
            continue

        if stack:
            stack[-1].parts.append(text)

    if not roots:
        raise DocumentOutlineRequiredError("DOCX không có Heading/mục lục hợp lệ. Vui lòng dùng Heading 1/Heading 2 cho tên chương.")

    return ParsedDocument(document_type="docx", sections=[root.to_parsed() for root in roots])
```

#### 2.4. MODIFY [document_parser_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/document_parser_service.py)
*   **Vị trí:** Dòng 7
*   **Mã nguồn thay đổi:**
```python
# Cũ:
from app.services.docx_service import parse_docx_structure
from app.services.epub_service import parse_epub_structure
from app.services.pdf_service import parse_pdf_structure
...
async def parse_document_structure(file_obj, document_type: str) -> ParsedDocument:
    normalized_type = normalize_document_type(document_type)

    if normalized_type == "pdf":
        return await parse_pdf_structure(file_obj)
    if normalized_type == "epub":
        return await parse_epub_structure(file_obj)
    if normalized_type == "docx":
        return await parse_docx_structure(file_obj)
    raise UnsupportedFileTypeError()

# Mới: Sử dụng Thread Pool và nạp dữ liệu độc lập vào BytesIO
import asyncio
from io import BytesIO
from app.services.docx_service import parse_docx_structure_sync
from app.services.epub_service import parse_epub_structure_sync
from app.services.pdf_service import parse_pdf_structure_sync
...
async def parse_document_structure(file_obj, document_type: str) -> ParsedDocument:
    normalized_type = normalize_document_type(document_type)
    
    # Đọc bytes đồng bộ ngay tại luồng chính để truyền an toàn xuyên tiểu luồng
    file_bytes = file_obj.read()

    def _execute_parser_sync() -> ParsedDocument:
        bio = BytesIO(file_bytes)
        if normalized_type == "pdf":
            return parse_pdf_structure_sync(bio)
        if normalized_type == "epub":
            return parse_epub_structure_sync(bio)
        if normalized_type == "docx":
            return parse_docx_structure_sync(bio)
        raise UnsupportedFileTypeError()

    # Offload việc CPU-bound parse vào asyncio Thread Pool
    return await asyncio.to_thread(_execute_parser_sync)
```

---

### 3. Tối ưu hóa Supabase Storage / RPC calls (Giải phóng Network I/O)
Bảo đảm các API mạng đồng bộ của Supabase SDK được chạy trong Thread Pool thay vì dừng cả tiến trình để đợi.

#### 3.1. MODIFY [storage_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/storage_service.py)
*   **Vị trí:** Dòng 44
*   **Mã nguồn thay đổi:**
```python
# Cũ:
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
            )

# Mới:
            await asyncio.to_thread(
                supabase.storage.from_(bucket).upload,
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
            )
```

#### 3.2. MODIFY [audiobook_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py)
*   **Vị trí:** Dòng 122
*   **Mã nguồn thay đổi:**
```python
# Cũ:
        # Lấy danh sách file từ tất cả bucket liên quan qua RPC
        result = supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute()

        # Xóa file vật lý qua Storage API
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    supabase.storage.from_(bucket).remove(paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

# Mới: Sử dụng asyncio.to_thread để tránh block luồng chính
        # 1. Gọi RPC không đồng bộ qua Thread Pool
        result = await asyncio.to_thread(
            supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute
        )

        # 2. Xóa các tệp vật lý không đồng bộ qua Thread Pool
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    await asyncio.to_thread(supabase.storage.from_(bucket).remove, paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")
```

---

### 4. Tối ưu hóa database writes của Background Workers
Các worker thường cập nhật trạng thái Job/Book rất nhiều lần trong các vòng lặp xử lý song song. Hãy đẩy các giao dịch mở `Session` đồng bộ này vào Thread Pool.

#### 4.1. MODIFY [book_pipeline.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/book_pipeline.py)
*   **Vị trí:** Các hàm cập nhật đồng bộ (`_update_job`, `_set_book_status`, `_fail_job`, `_job_is_ready`, `_load_book_processing_input`, v.v.)
*   **Mã nguồn thay đổi:**
```python
# Chuyển đổi các lời gọi đồng bộ trong luồng chạy async chính:
# Ví dụ thay đổi trong _run_unit_pipeline và _track_progress:

# Thay đổi 1: Tại _track_progress:
# Cũ:
            if is_partial:
                _set_book_status(book_id, BookStatus.PARTIAL_READY)
            _update_job(...)

# Mới:
            if is_partial:
                await asyncio.to_thread(_set_book_status, book_id, BookStatus.PARTIAL_READY)
            await asyncio.to_thread(_update_job, job_id, status=job_status, ...)

# Thay đổi 2: Tại _run_unit_pipeline:
# Cũ:
    processing_input = _load_book_processing_input(book_id, mode_value, job_id)
# Mới:
    processing_input = await asyncio.to_thread(_load_book_processing_input, book_id, mode_value, job_id)
```

#### 4.2. MODIFY [learning_unit_worker.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/learning_unit_worker.py)
*   **Vị trí:** Hàm `process_learning_unit`
*   **Mã nguồn thay đổi:**
```python
# Cũ:
        with Session(engine) as session:
            current_unit = session.get(LearningUnit, unit.id)
            if current_unit and current_unit.status == ProcessingJobStatus.READY and unit_segments_exist(session, unit.id):
                ...
            if current_unit:
                update_learning_unit_processing(...)

# Mới: Chuyển đóng gói logic kiểm tra và cập nhật DB vào helper đồng bộ
def _pre_check_and_update_unit_db(unit_id: uuid.UUID, raw_text_char_count: int, estimated_tokens: int, estimated_audio_seconds: int) -> tuple[bool, int]:
    with Session(engine) as session:
        current_unit = session.get(LearningUnit, unit_id)
        if current_unit and current_unit.status == ProcessingJobStatus.READY and unit_segments_exist(session, unit_id):
            return True, current_unit.main_segment_count
        if current_unit:
            update_learning_unit_processing(
                session,
                current_unit,
                status=ProcessingJobStatus.PROCESSING,
                raw_text_char_count=raw_text_char_count,
                estimated_tokens=estimated_tokens,
                estimated_audio_seconds=estimated_audio_seconds,
            )
        return False, 0

# Và gọi từ process_learning_unit qua Thread Pool:
        is_ready, segment_count = await asyncio.to_thread(
            _pre_check_and_update_unit_db,
            unit.id,
            raw_text_char_count,
            estimated_tokens,
            estimated_audio_seconds
        )
        if is_ready:
            return LearningUnitProcessingResult(unit.id, segment_count, skipped=True)
```

---

## 🧪 Kế hoạch Kiểm thử & Xác minh (Verification Plan)

### 1. Kiểm thử tự động (Unit Tests)
Đảm bảo tất cả các test suite của parsers, storage và pipeline vẫn hoạt động chính xác sau khi chuyển đổi mô hình đa luồng:
```powershell
# Chạy bộ test cho các dịch vụ upload và parser
uv run pytest tests/test_upload_service_batch_commit.py -q
uv run pytest tests/services/test_live_service.py -q
```

### 2. Kiểm thử thủ công (Console/Staging Verification)
*   **Tải lên sách mới (Upload Book):** Đăng nhập vào giao diện hoặc gọi API tải lên một tài liệu PDF lớn (>10MB). Kiểm tra xem log của FastAPI có bị treo giữa chừng hay không, đồng thời gửi song song các request nhẹ (như `GET /health`) để chứng minh hệ thống không bị block.
*   **Chạy Pipeline sinh âm thanh (TTS pipeline):** Theo dõi logs của worker và đảm bảo việc sinh audio (`edge`/`google`) diễn ra ổn định, tệp tin MP3 tải lên Supabase Storage thành công mà không có ngoại lệ đa luồng nào xảy ra.
