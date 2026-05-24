# Fix Logging Secret Leak va Hoan Thien Upload EPUB/DOCX

Ngay 2026-05-18.

Tai lieu nay ghi lai nhan dinh va huong implement cho 2 van de con lai sau khi test upload:

1. Log server qua verbose, lam lo `apikey` / `Authorization Bearer ...` cua Supabase.
2. Backend dang claim support PDF/EPUB/DOCX, nhung thuc te moi PDF co parser that. EPUB/DOCX dang bi reject tai dispatcher.

Muc tieu: fix theo huong production-safe, deterministic, de debug, khong fallback doan chuong sai logic.

---

## 0. Sau Khi Implement: Senior Review Notes

Phan nay la ghi chu training sau khi da implement that trong source code. Muc tieu khong chi la "da sua cai gi", ma la giup ban hieu tai sao sua nhu vay, moi doan code giai quyet rui ro nao, va cac lua chon khac vi sao khong phu hop bang.

### Ket qua implement

Da implement cac file chinh:

- [app/core/config.py](../app/core/config.py): them `LOG_LEVEL`, `LOG_THIRD_PARTY_LEVEL`.
- [app/core/logger.py](../app/core/logger.py): ha log level, chan noisy third-party loggers, redact secret.
- [app/core/exceptions.py](../app/core/exceptions.py): them `DocumentExtractionError`, giu `PdfExtractionError` ke thua de khong break code cu.
- [app/services/document_parser_service.py](../app/services/document_parser_service.py): dispatcher chung cho PDF/EPUB/DOCX.
- [app/services/epub_service.py](../app/services/epub_service.py): parse EPUB theo TOC.
- [app/services/docx_service.py](../app/services/docx_service.py): parse DOCX theo Heading style.
- [app/services/upload_service.py](../app/services/upload_service.py): upload flow dung parser chung, response them `document_type`, `page_start` co the `null`.
- [app/services/workers/book_pipeline.py](../app/services/workers/book_pipeline.py): background worker khong con hard-code PDF; co the xu ly lai PDF/EPUB/DOCX tu Storage.
- [tests/test_document_parsers.py](../tests/test_document_parsers.py): test parser va logging redaction.

Da them dependencies:

```toml
"ebooklib>=0.20",
"beautifulsoup4>=4.14.3",
"python-docx>=1.2.0",
```

Da test:

- `uv run pytest tests\test_document_parsers.py -q` -> `7 passed`
- `uv run ruff check ...` -> pass
- Upload PDF khong outline -> `422`
- Upload PDF co outline -> `200`
- Upload DOCX co Heading -> `200`
- Upload DOCX khong Heading -> `422`
- Upload EPUB co TOC -> `200`
- Scan log secret -> khong thay raw `authorization`, `apikey`, `service_role`, `Bearer`, `eyJ`

### Bai hoc kien truc so 1: Fix logging truoc parser

Logging leak la security issue. Parser EPUB/DOCX la feature gap. Khi co 2 van de cung luc, minh uu tien security truoc vi:

- Security issue co the gay lo Supabase service role key.
- Fix logging doc lap, it anh huong business logic.
- Neu tiep tuc test parser trong luc log con leak, moi lan upload thanh cong co the lai ghi secret vao file log.

Day la mindset quan trong khi lam do an that: viec nao co blast radius cao va doc lap thi xu ly truoc.

### Bai hoc kien truc so 2: Khong chi sua upload endpoint

Luc dau nhin vao loi, ta co the nghi chi can sua [upload_service.py](../app/services/upload_service.py). Nhung khi doc tiep [book_pipeline.py](../app/services/workers/book_pipeline.py), minh thay background worker dang:

```python
storage_path = f"{book_id}/original.pdf"
chapters_data = await extract_pdf_chapters(pdf_file)
```

Neu chi sua upload, thi DOCX/EPUB upload `200` nhung den luc user bam generate plan, pipeline van download `original.pdf` va parse PDF. Nghia la feature nhin nhu xong nhung fail o buoc sau.

Vi vay minh tao [document_parser_service.py](../app/services/document_parser_service.py) lam dispatcher chung:

```python
async def extract_chapters_by_document_type(file_obj, document_type: str) -> list[dict]:
    normalized_type = normalize_document_type(document_type)

    if normalized_type == "pdf":
        return await extract_pdf_chapters(file_obj)

    if normalized_type == "epub":
        return await extract_epub_chapters(file_obj)

    if normalized_type == "docx":
        return await extract_docx_chapters(file_obj)
```

Y nghia:

- Upload va background worker dung cung 1 contract.
- Sau nay them `txt`, `md`, `pptx` thi chi them parser + them branch o dispatcher.
- Khong lap logic `if pdf/epub/docx` o nhieu noi.

Alternative khong chon:

- **Chi implement trong `upload_service.py`**: nhanh nhung worker van fail khi generate plan.
- **Them ngay cot `document_type` vao DB**: sach hon ve data model, nhung can migration va co rui ro lon hon trong luc minh dang fix feature. Lan nay minh infer tu `file_url` vi storage path da co `original.pdf|epub|docx`. Sau nay neu product lon hon, nen them cot `document_type` bang Alembic.
- **Luu extracted text vao DB ngay khi upload**: giam viec re-extract o worker, nhung doi schema/storage va co the lam upload cham hon. Hien tai giu flow cu: upload nhanh tao DRAFT, generate plan moi xu ly nang.

### Bai hoc kien truc so 3: Parser phai deterministic

Rule san pham cua ban: khong co outline/TOC/Heading thi bao FE ngay, khong fallback. Minh giu rule nay vi ung dung hoc tap can chia chuong dung. Neu chia sai, RAG/TTS/reading plan se sai ca downstream.

Voi PDF:

- Dung hidden outline/bookmark.
- Khong co outline -> `DocumentOutlineRequiredError` -> HTTP `422`.

Voi EPUB:

- Dung EPUB TOC (`book.toc`) qua `ebooklib`.
- Map TOC href sang XHTML document.
- Convert HTML sang text bang BeautifulSoup.
- Khong scan regex trong body.

Voi DOCX:

- Dung style `Heading 1`, `Heading 2`, `Heading 3`.
- Co them support style custom co `outlineLvl` trong XML.
- Khong scan regex "Chuong 1", "Chapter 1".

Alternative khong chon:

- **Regex theo text nhu `^Chương \d+`**: co ve tien, nhung sai voi sach co muc "Chuong trinh", heading bi xuong dong, ngon ngu khac, hoac tai lieu co so thu tu trong body.
- **Chia theo so ky tu/token**: tot cho chunking RAG, khong tot cho chapter structure. FE dang can outline chuong, khong phai chunk noi bo.
- **OCR cho scanned PDF**: day la feature rieng, ton chi phi va latency. Neu upload scan thi nen bao user doi file text-based truoc.

### Giai thich logging code

Trong [logger.py](../app/core/logger.py), minh them:

```python
SENSITIVE_PATTERNS = (
    re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?Bearer\s+)[^'\",\s}]+"),
    re.compile(r"(?i)(apikey['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(service_role['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
)
```

Y nghia:

- Bat cac dang log pho bien: dict string, JSON-ish, key-value.
- Giu lai key de debug biet co header nao xuat hien.
- Thay value bang `[REDACTED]`.

Minh them:

```python
NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "hpack",
    "h11",
    "supabase",
    "postgrest",
    "storage3",
    "gotrue",
)
```

Y nghia:

- Cac logger nay hay log HTTP internals.
- App khong can xem frame/header o moi request.
- Day len `WARNING` de van thay loi that, nhung khong thay request debug.

Minh sua:

```python
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
```

Truoc do `level=0` nghia la bat tat ca, gom ca DEBUG cua thu vien ben ngoai. Dung `INFO` de root logger khong hut het debug noise.

Minh van giu `InterceptHandler` vi project dang dung Loguru, nhung nhieu thu vien Python dung standard `logging`. Intercept giup log di ve mot format chung.

Alternative khong chon:

- **Tat hoan toan third-party logger bang `disabled=True`**: co the mat log loi quan trong khi Supabase/httpx that bai.
- **Chi redact ma van de DEBUG**: van qua on, log nang, latency/log file phinh to, va regex redact khong bao gio nen la lop bao ve duy nhat.
- **Bo Loguru, chuyen het sang standard logging**: sach trong dai han neu lam lai logging, nhung thay doi lon, khong can cho bug hien tai.

### Giai thich EPUB parser

File [epub_service.py](../app/services/epub_service.py) co 3 y chinh.

1. `_flatten_epub_toc`

EPUB TOC co the la list long nhau. Ham nay bien TOC thanh list phang:

```python
[("Chương 1", "chap_01.xhtml"), ("Chương 2", "chap_02.xhtml")]
```

No cung bo fragment sau dau `#`, vi giai doan nay minh parse theo document-level:

```python
href.split("#", 1)[0]
```

2. `_html_to_text`

EPUB chapter thuc chat la XHTML/HTML. Minh dung BeautifulSoup de:

- Xoa `script`, `style`, `nav`.
- Lay text co newline.
- Strip dong rong.

3. `extract_epub_chapters`

Flow:

- `epub.read_epub(...)`
- Lay `book.toc`; khong co thi raise `DocumentOutlineRequiredError`.
- Tao map `href -> content`.
- Duyet TOC va lay text theo href.
- Khong co chapter text thi raise `DocumentExtractionError`.

Alternative khong chon:

- **Doc tat ca XHTML theo spine**: co the lay duoc noi dung nhung khong dam bao outline. User yeu cau khong fallback neu khong co TOC.
- **Dung nav.xhtml parse tay**: duoc, nhung `ebooklib` da expose `book.toc`, dung API thu vien se on dinh hon.
- **Parse anchor-level section ngay**: phuc tap hon, can crop HTML theo id anchor. Chua can cho MVP.

### Giai thich DOCX parser

File [docx_service.py](../app/services/docx_service.py) dung `python-docx`.

`_is_heading(paragraph)` check 2 truong hop:

- Style name la `Heading 1`, `Heading 2`, `Heading 3`.
- Style custom co `w:outlineLvl` trong XML.

Ly do them `outlineLvl`: nhieu file Word tieng Viet/custom template co style ten khac, nhung ve mat Word outline van la heading. Neu chi check style name, se reject nham mot so DOCX hop le.

`extract_docx_chapters` dung state machine don gian:

- Gap heading -> bat dau chapter moi.
- Paragraph sau heading -> gom vao chapter hien tai.
- Gap heading tiep theo -> dong chapter cu, mo chapter moi.
- Khong co chapter nao -> `DocumentOutlineRequiredError`.

Alternative khong chon:

- **Doc built-in Table of Contents trong DOCX**: TOC trong Word thuong la field/rendered text, khong dang tin bang Heading style.
- **Lay page number DOCX**: DOCX khong co page number on dinh neu khong render bang Word engine. Page phu thuoc font/margin/device. Vi vay `page_start = None`.
- **Chap nhan Title style la chapter**: minh khong chon trong code final vi `Title` thuong la ten sach, khong phai chapter. Neu can, co the mo rong sau.

### Giai thich response contract

Truoc day outline co:

```json
{"title": "...", "page_start": 1}
```

Voi EPUB/DOCX, page number khong co nghia on dinh. Vi vay response moi:

```json
{
  "book_id": "...",
  "total_chapters": 2,
  "document_type": "docx",
  "outline": [
    {"title": "Chương 1", "page_start": null}
  ]
}
```

Y nghia cho FE:

- Neu `page_start` la number -> hien "Trang X".
- Neu `page_start` la `null` -> chi hien title.
- FE co the dung `document_type` de hien icon/label file.

Alternative khong chon:

- **Gan page_start = 0 cho EPUB/DOCX**: gay hieu nham, FE co the hien "Trang 0".
- **Bo field page_start khoi EPUB/DOCX**: lam response shape khong dong nhat.
- **Tinh page DOCX bang library khac**: khong on dinh neu khong render document that su.

### Giai thich background worker fix

Trong [book_pipeline.py](../app/services/workers/book_pipeline.py), minh them `_storage_path_for_book`.

Ly do: upload da luu file theo:

```python
storage_path = f"{book_id}/original.{document_type}"
```

Nhung worker cu hard-code:

```python
storage_path = f"{book_id}/original.pdf"
```

Neu file la DOCX/EPUB thi worker fail. Ham moi:

- Infer document type tu `file_url`.
- Neu public URL co path sau `/raw_books/`, lay dung storage path.
- Fallback ve `{book_id}/original.{document_type}`.

Day la fix it rui ro vi khong them DB migration. Sau nay ban nen can nhac them cot `document_type` vao bang `books`, vi infer tu URL la chap nhan duoc cho MVP nhung khong phai domain model dep nhat.

### Giai thich tests

[tests/test_document_parsers.py](../tests/test_document_parsers.py) co 7 test:

- PDF sample co outline parse duoc.
- DOCX co Heading parse duoc.
- DOCX khong Heading fail 422 domain.
- EPUB co TOC parse duoc.
- EPUB khong TOC fail 422 domain.
- Redaction an secret.
- Noisy HTTP loggers o `WARNING` tro len.

Tai sao test parser truoc integration?

- Parser la core business rule cua upload.
- Test nhanh, khong can Supabase, khong tao DB/storage that.
- Integration upload van can test manual voi server, nhung khong nen de moi bug parser phai can server that moi phat hien.

Alternative khong chon:

- **Chi manual test curl**: nhanh luc dau, nhung regressions sau nay de quay lai.
- **Mock toan bo upload service**: co the qua xa voi bug that; bug o day nam trong parser va logging.
- **Test Supabase storage trong unit test**: cham, phu thuoc network/key, khong phu hop unit.

### Dieu can canh giac tiep theo

1. Upload success hien tai tao DRAFT book va upload file that. Khi test local, can co cleanup script rieng cho test data.
2. Nen them cot `document_type` vao `books` bang Alembic trong mot task rieng.
3. Nen can nhac luu chapter text sau upload neu muon giam viec re-extract o background worker.
4. AppException handler hien log 422 bang `error`. Voi validation/domain error, co the giam thanh `warning` de log sach hon.
5. Neu sau nay support OCR, tach thanh flow rieng: user explicit chon OCR, bao chi phi/latency, khong ngam fallback.

---

## 1. Logging Leak Supabase Secret

### Nhan dinh

Van de khong nam o endpoint upload. Upload thanh cong, nhung khi server chay local, log stdout co log DEBUG tu cac thu vien HTTP nhu:

- `httpcore`
- `httpx`
- `hpack`
- co the them `supabase`, `postgrest`, `storage3`, `gotrue`

Nguyen nhan chinh nam o [app/core/logger.py](../app/core/logger.py):

```python
logger.add(sys.stdout, level="DEBUG", ...)
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
```

`level=0` bat tat ca standard logging, sau do redirect vao Loguru. Khi cac thu vien HTTP log request header o DEBUG, header nhay vao file/console log. Neu co `apikey` hoac `Authorization`, secret bi lo.

### Rule bat buoc cho du an

- Khong bao gio log request/response header day du cua SDK ben thu ba.
- Default console log khong duoc la `DEBUG` neu dang dung real service key.
- Neu can debug HTTP, bat rieng trong local bang env flag ngan han, va phai redact secret.
- File log share cho FE/teammate phai khong co `Authorization`, `apikey`, `service_role`, JWT.
- Error handler chi log domain error ngan gon; unhandled exception duoc log stacktrace nhung khong log input file bytes/header.

### Huong fix de xuat

Them setting log level:

File: [app/core/config.py](../app/core/config.py)

```python
class Settings(BaseSettings):
    ...
    LOG_LEVEL: str = "INFO"
    LOG_THIRD_PARTY_LEVEL: str = "WARNING"
```

Sua logger de:

- Console dung `settings.LOG_LEVEL`, default `INFO`.
- Standard logging root khong de `level=0`, dung `INFO` hoac `WARNING`.
- Ep level cua cac logger HTTP nhay cam ve `WARNING`.
- Them filter redact phong thu neu message van lot qua.

File: [app/core/logger.py](../app/core/logger.py)

```python
import logging
import re
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(authorization['\"]?\s*[:=]\s*['\"]?Bearer\s+)[^'\",\s}]+"),
    re.compile(r"(?i)(apikey['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
    re.compile(r"(?i)(service_role['\"]?\s*[:=]\s*['\"]?)[^'\",\s}]+"),
]

NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "hpack",
    "h11",
    "supabase",
    "postgrest",
    "storage3",
    "gotrue",
)


def _redact_message(message: str) -> str:
    redacted = message
    for pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub(r"\1[REDACTED]", redacted)
    return redacted


def setup_logger():
    logger.remove()

    app_log_level = settings.LOG_LEVEL.upper()
    third_party_level = settings.LOG_THIRD_PARTY_LEVEL.upper()

    def redact_filter(record):
        record["message"] = _redact_message(record["message"])
        return True

    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level=app_log_level,
        colorize=True,
        filter=redact_filter,
    )

    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        rotation="10 MB",
        retention="7 days",
        level=app_log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8",
        filter=redact_filter,
    )

    logger.add(
        LOG_DIR / "app_json_{time:YYYY-MM-DD}.log",
        rotation="50 MB",
        retention="14 days",
        level=app_log_level,
        serialize=True,
        encoding="utf-8",
        filter=redact_filter,
    )

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            message = _redact_message(record.getMessage())
            logger.opt(depth=depth, exception=record.exc_info).log(level, message)

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.setLevel(app_log_level)
        logging_logger.propagate = False

    for logger_name in NOISY_LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.setLevel(third_party_level)
        logging_logger.propagate = False

    return logger
```

Ghi chu senior:

- `redact_filter` la lop phong thu thu hai, khong thay the viec ha log level.
- Khong nen set root logging `DEBUG` trong app co Supabase service key.
- Neu can debug request HTTP, tao script local rieng va dung anon key/test project, khong debug tren app server that.

### Test logging sau khi fix

Chay:

```powershell
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Upload lai file thanh cong:

```powershell
$file = Get-ChildItem -File | Where-Object { $_.Name -like 'Chương 4_*' } | Select-Object -First 1
curl.exe -s -S -w "`nHTTP_STATUS:%{http_code}`n" -X POST "http://127.0.0.1:8000/api/v1/upload" -F "file=@$($file.FullName);type=application/pdf"
```

Kiem tra log:

```powershell
Select-String -Path server_upload_test.out.log,logs\*.log -Pattern "authorization|apikey|service_role|Bearer" -CaseSensitive:$false
```

Ket qua mong doi:

- Khong co secret raw.
- Neu co line match thi gia tri phai la `[REDACTED]`.
- Log upload chi nen co thong tin nghiep vu: document type, storage path, book id, so chuong.

---

## 2. Hoan Thien Parser EPUB/DOCX

### Nhan dinh

File [app/services/upload_service.py](../app/services/upload_service.py) dang cho phep detect:

- PDF
- EPUB
- DOCX

Nhung dispatcher hien tai:

```python
if document_type == "epub":
    raise DocumentOutlineRequiredError("EPUB parser chưa được bật ...")

if document_type == "docx":
    raise DocumentOutlineRequiredError("DOCX parser chưa được bật ...")
```

Nghia la product noi support EPUB/DOCX, nhung backend chua support that.

### Rule nghiep vu can giu

- PDF: bat buoc co hidden outline/bookmark. Khong co thi 422.
- EPUB: bat buoc co navigation TOC (`nav.xhtml`/NCX) doc duoc. Khong co thi 422.
- DOCX: bat buoc co Heading style chuan (`Heading 1`, `Heading 2`, hoac style outline level). Khong co thi 422.
- Khong fallback sang "chia theo do dai text", "doan nao in dam thi la chuong", "regex Chuong 1". Nhung cach nay de sai logic.
- File scan/OCR khong nam trong upload parser hien tai. Neu khong trich text duoc thi 422 va bao FE doi file text-based.
- Service layer raise `DocumentOutlineRequiredError` hoac `PdfExtractionError`/`DocumentExtractionError`; router khong tu xu ly logic parser.

### Nen doi ten exception

Hien co `PdfExtractionError`, nhung khi support EPUB/DOCX thi ten nay khong con dung tong quat.

Option an toan:

File: [app/core/exceptions.py](../app/core/exceptions.py)

```python
class DocumentExtractionError(AppException):
    status_code = 422
    detail = "Không thể trích xuất nội dung từ file. File có thể bị lỗi, là scan ảnh, hoặc không có text."


class PdfExtractionError(DocumentExtractionError):
    detail = "Không thể trích xuất nội dung từ PDF. File có thể bị lỗi hoặc là scan ảnh."
```

Sau do EPUB/DOCX parser raise `DocumentExtractionError`.

### Dependency can them

File: [pyproject.toml](../pyproject.toml)

```toml
dependencies = [
    ...
    "ebooklib>=0.19",
    "beautifulsoup4>=4.12.0",
    "python-docx>=1.1.0",
]
```

Sau do chay:

```powershell
uv sync
```

---

## 3. Thiet Ke Parser Layer

Nen tach moi format thanh 1 service file:

```text
app/services/pdf_service.py
app/services/epub_service.py
app/services/docx_service.py
app/services/upload_service.py
```

Contract chung cho tat ca parser:

```python
[
    {
        "title": "Chương 1 ...",
        "text": "...",
        "page_start": 1,   # PDF co page; EPUB/DOCX co the de None
        "page_end": 5,     # PDF co page; EPUB/DOCX co the de None
    }
]
```

Voi EPUB/DOCX, neu khong co page concept thi nen tra:

```python
"page_start": None,
"page_end": None,
```

Va response outline nen khong hard-code `page_start` = 0. FE co the hien thi title, con page chi hien neu co.

Sua response outline trong [app/services/upload_service.py](../app/services/upload_service.py):

```python
outline = [
    {
        "title": c.get("title", f"Chương {i + 1}"),
        "page_start": c.get("page_start"),
    }
    for i, c in enumerate(chapters_data)
]
```

---

## 4. EPUB Parser De Xuat

File moi: `app/services/epub_service.py`

Code mau:

```python
from __future__ import annotations

from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError


def _html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup(["script", "style", "nav"]):
        tag.decompose()

    text = soup.get_text("\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def _flatten_epub_toc(toc_items) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []

    for item in toc_items:
        if isinstance(item, tuple):
            parent, children = item
            href = getattr(parent, "href", None)
            title = str(getattr(parent, "title", "") or "").strip()
            if title and href:
                result.append((title, href.split("#", 1)[0]))
            result.extend(_flatten_epub_toc(children))
            continue

        href = getattr(item, "href", None)
        title = str(getattr(item, "title", "") or "").strip()
        if title and href:
            result.append((title, href.split("#", 1)[0]))

    return result


async def extract_epub_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)
    raw = file_obj.read()

    try:
        book = epub.read_epub(BytesIO(raw))
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc EPUB: {exc}") from exc

    toc = _flatten_epub_toc(book.toc)
    if len(toc) <= 1:
        raise DocumentOutlineRequiredError(
            "EPUB không có mục lục điều hướng hợp lệ. Vui lòng upload EPUB có TOC chuẩn."
        )

    documents_by_href: dict[str, bytes] = {}
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        href = item.get_name()
        documents_by_href[href] = item.get_content()

    chapters: list[dict] = []
    seen_hrefs: set[str] = set()

    for title, href in toc:
        if href in seen_hrefs:
            continue
        seen_hrefs.add(href)

        content = documents_by_href.get(href)
        if not content:
            continue

        text = _html_to_text(content)
        if text:
            chapters.append(
                {
                    "title": title,
                    "text": text,
                    "page_start": None,
                    "page_end": None,
                }
            )

    if not chapters:
        raise DocumentExtractionError(
            "EPUB có mục lục nhưng không trích xuất được text. File có thể bị lỗi hoặc không phải text-based EPUB."
        )

    return chapters
```

Ghi chu:

- EPUB khong co page number on dinh nhu PDF, dung `None`.
- Dung TOC cua EPUB, khong scan regex theo noi dung.
- Neu TOC co fragment `chapter.xhtml#section1`, ban dau lay file-level `chapter.xhtml`. Neu sau nay can section-level, moi xu ly anchor chi tiet.

---

## 5. DOCX Parser De Xuat

File moi: `app/services/docx_service.py`

Code mau:

```python
from __future__ import annotations

from docx import Document

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError


HEADING_STYLE_NAMES = {
    "heading 1",
    "heading 2",
    "title",
}


def _is_heading(paragraph) -> bool:
    style_name = (paragraph.style.name or "").strip().lower() if paragraph.style else ""
    if style_name in HEADING_STYLE_NAMES:
        return True

    # python-docx khong expose outline level truc tiep qua public API.
    # Neu style custom co outlineLvl, doc tu XML de chap nhan template custom.
    p_style = paragraph.style
    if p_style is not None and p_style.element is not None:
        outline_level = p_style.element.xpath("./w:pPr/w:outlineLvl")
        if outline_level:
            return True

    return False


async def extract_docx_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)

    try:
        document = Document(file_obj)
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc DOCX: {exc}") from exc

    chapters: list[dict] = []
    current_title: str | None = None
    current_parts: list[str] = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        if _is_heading(paragraph):
            if current_title and current_parts:
                chapters.append(
                    {
                        "title": current_title,
                        "text": "\n".join(current_parts).strip(),
                        "page_start": None,
                        "page_end": None,
                    }
                )

            current_title = text
            current_parts = []
            continue

        if current_title:
            current_parts.append(text)

    if current_title and current_parts:
        chapters.append(
            {
                "title": current_title,
                "text": "\n".join(current_parts).strip(),
                "page_start": None,
                "page_end": None,
            }
        )

    if not chapters:
        raise DocumentOutlineRequiredError(
            "DOCX không có Heading/mục lục hợp lệ. Vui lòng dùng Heading 1/Heading 2 cho tên chương."
        )

    return chapters
```

Ghi chu:

- DOCX khong co page number on dinh vi page phu thuoc renderer, font, margin.
- Chi parse theo heading style, khong regex "Chuong".
- Neu tai lieu co heading nhung khong co text trong chapter, chapter rong bi bo qua. Neu tat ca rong thi 422.

---

## 6. Noi Dispatcher Vao Upload Service

File: [app/services/upload_service.py](../app/services/upload_service.py)

```python
from app.services.docx_service import extract_docx_chapters
from app.services.epub_service import extract_epub_chapters
from app.services.pdf_service import extract_pdf_chapters
```

Sua dispatcher:

```python
async def _extract_chapters_by_type(tmp_filename: str, document_type: str) -> list[dict]:
    with open(tmp_filename, "rb") as f:
        if document_type == "pdf":
            return await extract_pdf_chapters(f)

        if document_type == "epub":
            return await extract_epub_chapters(f)

        if document_type == "docx":
            return await extract_docx_chapters(f)

    raise UnsupportedFileTypeError()
```

Nen sua comment cu:

```python
"""
Bước 1: Validate file, extract document outline, upload lên Supabase Storage,
lưu Book + Chapter (DRAFT) vào DB, trả về outline cho Flutter.
"""
```

---

## 7. API Response Va FE Contract

Hien response:

```json
{
  "book_id": "...",
  "total_chapters": 3,
  "outline": [
    {"title": "...", "page_start": 1}
  ]
}
```

De support EPUB/DOCX sach hon:

```json
{
  "book_id": "...",
  "total_chapters": 3,
  "document_type": "epub",
  "outline": [
    {"title": "Chapter 1", "page_start": null}
  ]
}
```

Sua return trong `handle_upload_document`:

```python
return {
    "book_id": str(book_id),
    "total_chapters": len(chapters_data),
    "document_type": document_type,
    "outline": outline,
}
```

FE rule:

- Neu `page_start` la `null`, chi hien title.
- Neu upload fail 422, hien message trong `detail` cho user.
- Khong retry cung file neu loi la missing outline/heading/TOC.

---

## 8. Test Plan

### Unit tests nen them

File moi: `tests/test_document_extractors.py`

Case can co:

- PDF co outline: pass, tra list chapter.
- PDF khong outline: raise `DocumentOutlineRequiredError`.
- PDF scan/khong extract text: raise `DocumentExtractionError` hoac `PdfExtractionError`.
- DOCX co Heading 1 + text: pass.
- DOCX plain paragraphs khong heading: raise `DocumentOutlineRequiredError`.
- EPUB co TOC + XHTML text: pass.
- EPUB khong TOC: raise `DocumentOutlineRequiredError`.

### Manual upload tests

PDF fail:

```powershell
curl.exe -s -S -w "`nHTTP_STATUS:%{http_code}`n" -X POST "http://127.0.0.1:8000/api/v1/upload" -F "file=@MGHP HK1(2025-2026).pdf;type=application/pdf"
```

Expected:

```text
HTTP_STATUS:422
```

PDF success:

```powershell
$file = Get-ChildItem -File | Where-Object { $_.Name -like 'Chương 4_*' } | Select-Object -First 1
curl.exe -s -S -w "`nHTTP_STATUS:%{http_code}`n" -X POST "http://127.0.0.1:8000/api/v1/upload" -F "file=@$($file.FullName);type=application/pdf"
```

Expected:

```text
HTTP_STATUS:200
```

EPUB/DOCX:

- Can tao sample file co TOC/Heading chuan.
- Can tao sample file khong TOC/Heading de dam bao 422.

### Secret scan sau test

```powershell
Select-String -Path logs\*.log,server_upload_test*.log -Pattern "authorization|apikey|service_role|Bearer|eyJ" -CaseSensitive:$false
```

Expected:

- Khong co raw secret.
- JWT pattern `eyJ...` khong xuat hien trong log app.

---

## 9. Thu Tu Implement De It Rui Ro

1. Fix logger truoc.
   - Day la security issue, doc lap voi parser.
   - Test bang upload PDF thanh cong va scan log.

2. Them dependency EPUB/DOCX.
   - `uv add ebooklib beautifulsoup4 python-docx`
   - Commit lock file neu co.

3. Them `DocumentExtractionError`.
   - Giu `PdfExtractionError` ke thua de khong break code cu.

4. Tao `epub_service.py` va `docx_service.py`.
   - Parser deterministic.
   - Khong fallback heuristic.

5. Noi dispatcher trong `upload_service.py`.
   - Tra `document_type` trong response.
   - `page_start` cho EPUB/DOCX de `None`.

6. Them tests.
   - Uu tien unit test parser truoc integration upload.

7. Manual test voi 3 loai file.
   - Pass/fail deu phai dung status code va message.

---

## 10. Checklist Review Truoc Khi Merge

- [ ] Upload PDF co outline tra 200.
- [ ] Upload PDF khong outline tra 422, khong tao Book/Chapter/Storage.
- [ ] Upload PDF scan tra 422, khong tao Book/Chapter/Storage.
- [ ] Upload EPUB co TOC tra 200.
- [ ] Upload EPUB khong TOC tra 422.
- [ ] Upload DOCX co Heading tra 200.
- [ ] Upload DOCX khong Heading tra 422.
- [ ] Log khong con `apikey`, `Authorization`, `Bearer`, JWT raw.
- [ ] FE hien duoc `detail` khi 422.
- [ ] `uv run ruff check ...` pass hoac chi con format loi da biet.
- [ ] `uv run pytest tests/test_document_extractors.py` pass.

---

## Ket Luan

Fix logging la viec can lam ngay truoc khi share log/deploy vi co rui ro lo service role key. Con EPUB/DOCX la feature gap: backend dang cho phep MIME/extension nhung chua co parser that. Huong fix tot nhat la them parser deterministic theo TOC/Heading, fail fast bang 422 neu tai lieu khong co cau truc chuan, dung dung rule san pham da thong nhat.
