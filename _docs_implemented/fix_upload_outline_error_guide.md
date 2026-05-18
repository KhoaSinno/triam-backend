# Fix Guide: Upload Document Outline Validation

## 1. Bối Cảnh

FE báo lỗi khi upload tài liệu:

```json
{ "detail": "Lỗi hệ thống nội bộ." }
```

Log server cho thấy lỗi thật nằm ở backend:

```text
POST /api/v1/upload
handle_upload_document()
extract_pdf_chapters()
ValueError: Tài liệu PDF không có Mục lục (Outline) ẩn.
```

Điều này nghĩa là file upload không sai về network/form-data. Backend đang ném `ValueError` từ parser, sau đó global exception handler chuyển thành HTTP 500 chung chung.

## 2. Product Rule

TRIAM hiện support upload các định dạng:

- PDF
- EPUB
- DOCX

Nhưng mỗi tài liệu phải có cấu trúc chương có thể trích xuất đáng tin cậy.

Rule bắt buộc:

- Nếu PDF không có hidden outline/bookmark: trả lỗi rõ cho FE, không xử lý tiếp.
- Nếu EPUB/DOCX không đọc được heading/table-of-contents/chapter structure: trả lỗi rõ cho FE.
- Không fallback auto-split theo số trang.
- Không fallback OCR/scanned document.
- Không tạo `Book`, không upload Storage, không tạo `Chapter` nếu chưa extract được outline hợp lệ.

Lý do: auto-split hoặc OCR có thể làm sai ranh giới chương, sai logic đọc/nghe/học theo chương.

## 3. Nhận Định Kỹ Thuật

### Lỗi chính

`app/services/pdf_service.py` đang ném `ValueError` khi PDF không có outline:

```python
if not outlines or len(outlines) <= 1:
    raise ValueError(
        "Tài liệu PDF không có Mục lục (Outline) ẩn. Hệ thống hiện chỉ hỗ trợ PDF có Mục lục chuẩn."
    )
```

`ValueError` không phải `AppException`, nên FastAPI rơi vào global handler:

```python
return JSONResponse(status_code=500, content={"detail": "Lỗi hệ thống nội bộ."})
```

### Lỗi phụ nhưng quan trọng

`pypdf.get_destination_page_number(item)` trả page index 0-based, nhưng code hiện tại lại trừ thêm 1:

```python
page_number = reader.get_destination_page_number(item)
outline_data.append({"title": item.title, "page_start": page_number})

start_p = current_chap["page_start"] - 1
```

Nếu outline trỏ tới trang đầu tiên, `start_p` có thể thành `-1`, dẫn đến đọc sai trang.

### Mismatch product support

`upload_service.py` cho phép `.pdf`, `.epub`, `.docx`, nhưng hiện đang luôn gọi:

```python
chapters_data = await extract_pdf_chapters(f)
```

Trong code hiện tại, `extract_pdf_chapters()` là parser PDF. Vì vậy backend đang tuyên bố support EPUB/DOCX nhưng chưa route parser theo định dạng.

## 4. Hướng Fix Đề Xuất

### Mục tiêu

1. Không còn HTTP 500 cho tài liệu thiếu outline.
2. FE nhận lỗi domain rõ ràng, ví dụ HTTP 422.
3. Parser thống nhất page index.
4. Upload service route parser theo file type.
5. Không tạo dữ liệu rác nếu parser fail.

## 5. Code Fix Đề Xuất

### 5.1. Thêm domain exception rõ nghĩa

File: `app/core/exceptions.py`

Thêm exception mới ở nhóm 422:

```python
class DocumentOutlineRequiredError(AppException):
    status_code = 422
    detail = (
        "Tài liệu không có cấu trúc chương hợp lệ. "
        "Vui lòng upload PDF có bookmark/outline, EPUB có mục lục, hoặc DOCX có heading."
    )
```

Có thể giữ `PdfExtractionError` cho lỗi file hỏng/không extract được text. `DocumentOutlineRequiredError` dùng riêng cho case file hợp lệ nhưng thiếu outline.

### 5.2. Chuẩn hóa parser result

Nên thống nhất internal page index là 0-based, còn response về FE là 1-based.

File: `app/services/pdf_service.py`

Sửa `get_pdf_outline_structure()`:

```python
def get_pdf_outline_structure(file_obj) -> list[dict]:
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    _parse_outline(item)
                    continue

                try:
                    page_index = reader.get_destination_page_number(item)
                    title = str(getattr(item, "title", "") or "").strip()
                    if title:
                        outline_data.append(
                            {
                                "title": title,
                                "page_index": page_index,
                            }
                        )
                except Exception as exc:
                    log.warning(f"Bỏ qua outline item lỗi: {exc}")

        _parse_outline(reader.outline)
        outline_data.sort(key=lambda x: x["page_index"])
        return outline_data
    except Exception as exc:
        log.warning(f"Lỗi đọc PDF outline: {exc}")
        return []
```

Sửa `extract_pdf_chapters()` thành PDF-specific rõ nghĩa:

```python
from app.core.exceptions import DocumentOutlineRequiredError, PdfExtractionError


async def extract_pdf_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)

    if not outlines or len(outlines) <= 1:
        raise DocumentOutlineRequiredError(
            "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
        )

    file_obj.seek(0)
    chapters = []

    try:
        with pdfplumber.open(file_obj) as pdf:
            total_pages = len(pdf.pages)

            for i, current_chap in enumerate(outlines):
                start_idx = max(0, int(current_chap["page_index"]))
                if i < len(outlines) - 1:
                    end_idx = int(outlines[i + 1]["page_index"])
                else:
                    end_idx = total_pages

                end_idx = min(max(end_idx, start_idx + 1), total_pages)

                chapter_text_parts = []
                for page_idx in range(start_idx, end_idx):
                    text = pdf.pages[page_idx].extract_text() or ""
                    if text.strip():
                        chapter_text_parts.append(text)

                chapter_text = "\n".join(chapter_text_parts).strip()
                if chapter_text:
                    chapters.append(
                        {
                            "title": current_chap["title"],
                            "text": chapter_text,
                            "page_start": start_idx + 1,
                            "page_end": end_idx,
                        }
                    )

    except DocumentOutlineRequiredError:
        raise
    except Exception as exc:
        raise PdfExtractionError(f"Không thể đọc nội dung PDF: {exc}") from exc

    if not chapters:
        raise PdfExtractionError(
            "PDF có outline nhưng không trích xuất được text. File có thể là scan ảnh hoặc bị lỗi."
        )

    return chapters
```

Giữ alias tạm nếu nhiều nơi còn gọi tên cũ:

```python
extract_pdf_chapters = extract_pdf_chapters
```

Nhưng nên migrate dần sang tên rõ hơn.

### 5.3. Route parser theo định dạng

File: `app/services/upload_service.py`

Thêm helper phân loại:

```python
def _detect_document_type(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if filename.endswith(".pdf") or content_type == "application/pdf":
        return "pdf"
    if filename.endswith(".epub") or content_type == "application/epub+zip":
        return "epub"
    if (
        filename.endswith(".docx")
        or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return "docx"

    raise UnsupportedFileTypeError(
        f"Loại file không hỗ trợ ({file.content_type}). Chỉ chấp nhận PDF, EPUB, DOCX."
    )
```

Thêm dispatcher:

```python
async def _extract_chapters_by_type(tmp_filename: str, document_type: str) -> list[dict]:
    with open(tmp_filename, "rb") as f:
        if document_type == "pdf":
            return await extract_pdf_chapters(f)

        if document_type == "epub":
            # TODO: implement extract_epub_chapters(f)
            raise DocumentOutlineRequiredError(
                "EPUB parser chưa được bật hoặc EPUB không có mục lục hợp lệ."
            )

        if document_type == "docx":
            # TODO: implement extract_docx_chapters(f)
            raise DocumentOutlineRequiredError(
                "DOCX parser chưa được bật hoặc DOCX không có heading/mục lục hợp lệ."
            )

    raise UnsupportedFileTypeError()
```

Sau đó trong `handle_upload_document()`:

```python
document_type = _detect_document_type(file)
```

và thay:

```python
with open(tmp_filename, "rb") as f:
    chapters_data = await extract_pdf_chapters(f)
```

bằng:

```python
chapters_data = await _extract_chapters_by_type(tmp_filename, document_type)
```

Storage path/content-type nên theo định dạng:

```python
storage_path = f"{book_id}/original.{document_type}"
content_type = file.content_type or {
    "pdf": "application/pdf",
    "epub": "application/epub+zip",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}[document_type]
```

### 5.4. Không wrap domain exception thành DatabaseError

Hiện đoạn DB create đang đúng phạm vi DB. Parser exceptions xảy ra trước đó nên sẽ không bị wrap nếu làm như trên.

Nếu sau này thêm try/catch rộng hơn, nhớ rule:

```python
except AppException:
    raise
except Exception as exc:
    raise DatabaseError(...) from exc
```

## 6. EPUB/DOCX Parser Rule

### EPUB

Chỉ accept EPUB nếu đọc được TOC/nav.

Parser nên trả:

```python
[
    {
        "title": "Chương 1",
        "text": "...",
        "page_start": 1,
        "page_end": 1,
    }
]
```

Với EPUB không có page thật, `page_start/page_end` có thể là thứ tự section/chapter, nhưng phải document rõ cho FE.

Nếu EPUB không có TOC:

```python
raise DocumentOutlineRequiredError(
    "EPUB không có mục lục hợp lệ. Vui lòng upload EPUB có TOC."
)
```

### DOCX

Chỉ accept DOCX nếu có heading style như `Heading 1`, `Heading 2` hoặc cấu trúc tương đương.

Nếu DOCX chỉ là text phẳng:

```python
raise DocumentOutlineRequiredError(
    "DOCX không có heading chương hợp lệ. Vui lòng dùng Heading 1/Heading 2."
)
```

### Scanned/OCR

Không tự OCR trong upload flow hiện tại.

Nếu PDF có outline nhưng page text rỗng:

```python
raise PdfExtractionError(
    "PDF có thể là scan ảnh hoặc không trích xuất được text. Vui lòng upload file có text selectable."
)
```

## 7. FE Contract Sau Fix

Case thiếu outline trả HTTP 422:

```json
{
  "detail": "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
}
```

FE nên hiển thị trực tiếp `detail`.

Không nên retry tự động với cùng file, vì đây là lỗi nội dung file, không phải lỗi network.

## 8. Test Checklist

### Unit / Service Tests

- PDF có outline: trả danh sách chapter.
- PDF không outline: raise `DocumentOutlineRequiredError`.
- PDF scan/text rỗng: raise `PdfExtractionError`.
- PDF outline trang đầu: không đọc page `-1`.
- Upload unsupported file: HTTP 400.
- Upload PDF không outline: HTTP 422, không tạo Book, không upload Storage.
- Upload PDF valid: tạo Book DRAFT + Chapter DRAFT.

### Manual Curl

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@no-outline.pdf"
```

Expected:

```json
{
  "detail": "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
}
```

Status: `422`.

## 9. Project Rules Cần Nhớ

- Router chỉ nhận request, inject session, gọi service.
- Service layer raise `AppException`, không raise `HTTPException`.
- Repository chỉ thao tác DB, không chứa HTTP logic.
- Parser không tự fallback nếu fallback làm sai cấu trúc chương.
- Không tạo record DB trước khi validate/extract outline thành công.
- Không biến domain error thành 500.
- Log server phải có lỗi kỹ thuật; response FE phải có lỗi dễ hiểu.
- Với EPUB/DOCX/PDF, parser nào chưa hoàn chỉnh phải fail rõ bằng 422, không giả vờ support.

## 10. Skills Nên Dùng Khi Thực Hiện

Khi bắt tay sửa code thật, dùng các skill/rule sau:

- `fastapi-sqlmodel-clean-architecture`: để giữ đúng layering Router → Service → Repository.
- `supabase-postgres-best-practices`: nếu thay đổi transaction, query hoặc storage/DB consistency.
- `spreadsheets/documents/presentations`: không cần dùng cho fix này.
- Không cần OpenAI docs cho task này vì lỗi nằm ở upload/parser, không liên quan OpenAI API.

## 11. Thứ Tự Thực Hiện Khi Được Approve

1. Thêm `DocumentOutlineRequiredError` trong `app/core/exceptions.py`.
2. Sửa `app/services/pdf_service.py` để:
   - không ném `ValueError`;
   - chuẩn hóa page index;
   - phân biệt thiếu outline và PDF không extract được text.
3. Sửa `app/services/upload_service.py` để:
   - detect document type;
   - route parser theo PDF/EPUB/DOCX;
   - trả 422 cho parser chưa hỗ trợ/thiếu structure;
   - lưu đúng extension/content-type lên Storage.
4. Thêm test service/API.
5. Chạy:

```bash
uv run ruff check app tests
uv run pytest
```

Nếu test toàn bộ quá nặng, chạy tối thiểu:

```bash
uv run ruff check app/services/pdf_service.py app/services/upload_service.py app/core/exceptions.py
uv run python -m py_compile app/services/pdf_service.py app/services/upload_service.py app/core/exceptions.py
```
