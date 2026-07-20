# Phase 25: Database SSL Connection Resilience, Decoupled Async Delete Operations & Book Details Graceful Fallback Implementation Guide

Hướng dẫn này trình bày chi tiết kiến trúc và cách hiện thực chuẩn **Senior Software Engineering** nhằm giải quyết dứt điểm 3 vấn đề hệ thống quan trọng trong TRIAM Backend:
1. **Lỗi đứt kết nối Database Postgres SSL đột ngột** (`psycopg2.OperationalError: SSL connection has been closed unexpectedly`).
2. **Độ trễ và lỗi lặp request khi xóa tài nguyên Sách (`DELETE /books/{id}`)** thông qua mô hình **Xóa 2 Pha Bất Đồng Bộ (Two-Phase Decoupled Deletion Pattern)**.
3. **Lỗi 400/404 bất thường khi truy vấn chi tiết sách (`GET /books/{id}/details`)** khi sách chưa có kế hoạch đọc (`ReadingPlan`), bằng cơ chế **Dự phòng Mềm mại (Graceful Fallback)**.

---

## 1. Mục Tiêu Nghiệp Vụ & Kiến Trúc (Business & Architecture Goals)

### 1.1. Khắc phục lỗi đứt kết nối Postgres SSL (DB Connection Resilience)
* **Vấn đề thực tế:** Khi ứng dụng chạy trên Cloud (như Hugging Face Spaces kết nối tới Supabase Postgres), cổng kết nối Cloud NAT Gateway sẽ tự động ngắt kết nối TCP/SSL nhàn rỗi (idle) sau **350 giây (~5.8 phút)**. Cấu hình cũ cài đặt `DATABASE_POOL_RECYCLE=900` (15 phút) khiến SQLAlchemy giữ lại socket SSL đã bị ngắt ngầm, dẫn tới exception HTTP 500 khi client thực hiện request tiếp theo.
* **Giải pháp Senior:**
  * Giảm `DATABASE_POOL_RECYCLE` xuống **`280` giây** (dưới ngưỡng ngắt 350s của Cloud NAT Gateway).
  * Bổ sung các thông số **TCP Keepalive Probes** (`keepalives=1`, `keepalives_idle=30`, `keepalives_interval=10`, `keepalives_count=5`) vào driver `psycopg2` để chủ động gửi gói tin giữ kết nối SSL luôn sống.

### 1.2. Chuẩn hóa thao tác Xóa 2 Pha Bất Đồng Bộ (Two-Phase Decoupled Deletion)
* **Vấn đề thực tế:** Hàm xóa cũ thực hiện xóa file vật lý trên Supabase Storage đồng bộ (Synchronous) ngay trong lượt gọi HTTP Request `DELETE /books/{id}`. Thao tác I/O qua mạng này tốn **2 - 5+ giây**, khiến request bị chậm, dễ gây ra Timeout/Retry trùng lặp ở phía Client (Mobile App/Front-End). Ngoài ra, I/O Storage không nằm trong DB Transaction nên nếu xóa Storage thành công mà DB rollback, hệ thống sẽ bị mất file vĩnh viễn.
* **Giải pháp Senior (Two-Phase Decoupled Deletion):**
  * **Pha 1 (Xóa Database Đồng bộ - `< 50ms`):** Kiểm tra quyền sở hữu, dọn dẹp các bảng liên quan (`cleanup_book_side_effects`) và thực hiện `delete(book)` trong Postgres DB ngay lập tức. Phản hồi `HTTP 200 OK` (hoặc `204 No Content`) lập tức cho Client.
  * **Pha 2 (Xóa Storage Bất đồng bộ - Background Task):** Đẩy thông tin `book_id` vào Celery Worker (`purge_book_storage_assets_task`) để tiến hành quét RPC và xóa file vật lý trên Supabase Storage bên dưới nền.

### 1.3. Dự phòng mềm mại cho API Chi tiết Sách (`Graceful Fallback for /books/{id}/details`)
* **Vấn đề thực tế:** Hàm `get_book_details` cũ luôn gọi `_active_plan(session, book_id, user_id)`. Nếu sách vừa upload hoặc chưa được người dùng chọn mode / tạo kế hoạch đọc, hàm lập tức `raise NoReadingPlanError()` khiến API quăng lỗi HTTP `400/404`, làm vỡ giao diện trên Mobile App.
* **Giải pháp Senior:** Bổ sung cơ chế Fallback mềm mại: Nếu sách chưa có `ReadingPlan`, trả về dữ liệu chuẩn của Sách với `learning_summary: null` và `units: []` kèm status `HTTP 200 OK` thay vì ném ra Exception.

---

## 2. Thiết Kế Luồng Xử Lý (Dataflow & Sequence Diagrams)

### 2.1. Sequence Diagram: Luồng Xóa 2 Pha Bất Đồng Bộ (Two-Phase Deletion)

```text
Client (FE)             FastAPI Router           Postgres DB            Celery Worker         Supabase Storage
    │                         │                       │                       │                      │
    │── DELETE /books/{id} ──>│                       │                       │                      │
    │                         │── Check Ownership ───>│                       │                      │
    │                         │── Delete DB Record ──>│                       │                      │
    │                         │   (Commit Transaction)│                       │                      │
    │                         │                       │                       │                      │
    │                         │── Dispatch Purge Task ───────────────────────>│                      │
    │                         │   purge_book_storage_assets_task.delay(id)    │                      │
    │                         │                       │                       │                      │
    │<── HTTP 200 OK ─────────│                       │                       │                      │
    │   (Phản hồi < 50ms)     │                       │                       │                      │
    │                         │                       │                       │── Call RPC & Remove─>│
    │                         │                       │                       │   Storage Files      │
    │                         │                       │                       │<── Remove Done ──────│
```

### 2.2. Sequence Diagram: Cơ chế Giữ kết nối DB Resilient (TCP Keepalives & Pool Recycle)

```text
SQLAlchemy Pool           psycopg2 Driver          Cloud NAT Gateway          Supabase Postgres DB
       │                         │                         │                           │
       │── Acquire Connection ──>│                         │                           │
       │                         │── TCP Keepalive (30s) ─>│── TCP Keepalive Probe ───>│
       │                         │<── TCP Keepalive ACK ───│<── Keepalive ACK ─────────│
       │                         │  (Duy trì Socket SSL)   │                           │
       │                         │                         │                           │
       │── Pool Recycle Check ──>│                         │                           │
       │   (280s < 350s NAT Limit)│                        │                           │
       │   Auto-renew connection │                         │                           │
```

---

## 3. Mã Nguồn Chi Tiết Cần Hiện Thực (Code Specifications)

### Bước 3.1: Cấu hình tham số môi trường mới

#### 1. Cập nhật [app/core/config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py)
Cập nhật `DATABASE_POOL_RECYCLE` thành `280` giây và thêm cấu hình TCP Keepalives:

```python
    DATABASE_POOL_RECYCLE: int = 280  # Tự động recycle connection sau 280s để tránh bị Cloud NAT Gateway ngắt ngầm (350s)
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_TCP_KEEPALIVES: bool = True
    DATABASE_TCP_KEEPALIVES_IDLE: int = 30
    DATABASE_TCP_KEEPALIVES_INTERVAL: int = 10
    DATABASE_TCP_KEEPALIVES_COUNT: int = 5
```

#### 2. Cập nhật [.env.example](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env.example)
```env
DATABASE_POOL_RECYCLE=280
DATABASE_POOL_PRE_PING=True
```

---

### Bước 3.2: Cấu hình DB Engine tự khôi phục kết nối trong [app/db/database.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/db/database.py)

Nâng cấp hàm `_connect_args_for` để tự động tiêm các thông số TCP Keepalive cho driver `psycopg2`:

```python
def _connect_args_for(database_url: str) -> dict[str, Any]:
    url = make_url(database_url)
    args: dict[str, Any] = {}
    if url.get_backend_name().startswith("postgresql"):
        if settings.DATABASE_APPLICATION_NAME:
            args["application_name"] = settings.DATABASE_APPLICATION_NAME
        
        # Bổ sung TCP Keepalive Probes cho driver psycopg2 nhằm ngăn Cloud NAT Gateway ngắt socket SSL ngầm
        if getattr(settings, "DATABASE_TCP_KEEPALIVES", True):
            args.update({
                "keepalives": 1,
                "keepalives_idle": getattr(settings, "DATABASE_TCP_KEEPALIVES_IDLE", 30),
                "keepalives_interval": getattr(settings, "DATABASE_TCP_KEEPALIVES_INTERVAL", 10),
                "keepalives_count": getattr(settings, "DATABASE_TCP_KEEPALIVES_COUNT", 5),
            })
    return args
```

---

### Bước 3.3: Định nghĩa Celery Task dọn dẹp Storage trong [app/tasks/book_tasks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/tasks/book_tasks.py)

Bổ sung import `from app.core.supabase import supabase` lên đầu file [app/tasks/book_tasks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/tasks/book_tasks.py) và khai báo task `purge_book_storage_assets_task` ở cuối file:

```python
from app.core.supabase import supabase  # Module-level import theo chuẩn PEP 8

@celery_app.task(name="triam.books.purge_storage_assets")
def purge_book_storage_assets_task(book_id: str) -> None:
    """
    Celery Background Worker: Dọn dẹp tất cả các file vật lý trên Supabase Storage
    sau khi bản ghi sách đã được xóa sạch trong Database.
    """
    log.info(f"Celery purge_book_storage_assets_task started | book_id={book_id}")
    target_buckets = ["audios", "raw_books"]
    try:
        # Gọi RPC lấy danh sách đường dẫn file liên quan
        result = supabase.rpc(
            "get_book_asset_paths",
            {"bucket_names": target_buckets, "book_id_prefix": book_id}
        ).execute()

        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    supabase.storage.from_(bucket).remove(paths)
                    log.info(f"Celery purge_storage_assets | Deleted {len(paths)} files from bucket '{bucket}' for book {book_id}")
        
        log.info(f"Celery purge_book_storage_assets_task completed | book_id={book_id}")
    except Exception as exc:
        log.exception(f"Celery purge_book_storage_assets_task failed | book_id={book_id} | error={exc}")
```

---

### Bước 3.4: Tối ưu hóa hàm Xóa Sách trong [app/repositories/audiobook_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py)

Tách biệt hoàn toàn việc xóa DB và việc dọn dẹp Storage:

```python
async def delete_book_storage(session: Session, book_id: uuid.UUID, user_id: uuid.UUID):
    """
    Xóa bản ghi trong Database ngay lập tức (Synchronous) và đẩy nhiệm vụ xóa file
    trên Supabase Storage sang Celery Worker chạy ngầm (Asynchronous).
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)
    is_clone = book.parent_shared_id is not None

    # 1. Dọn dẹp các bảng phụ thuộc & Xóa bản ghi trong Postgres DB
    cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
    delete_book(session, book_id)
    log.info(f"Fast DB delete complete for book: {str_book_id}")

    # 2. Đẩy nhiệm vụ xóa file vật lý trên Storage cho Celery Worker (chỉ với sách tự upload)
    if not is_clone:
        try:
            from app.tasks.book_tasks import purge_book_storage_assets_task
            purge_book_storage_assets_task.delay(str_book_id)
            log.info(f"Dispatched background storage purge task for book: {str_book_id}")
        except Exception as exc:
            log.warning(f"Failed to dispatch purge task (will rely on periodic cleanup): {exc}")
```

---

### Bước 3.5: Xử lý Fallback Mềm mại trong [app/services/audiobook_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/audiobook_service.py)

Cập nhật hàm `get_book_details` để sử dụng Enum `PlanMode.PARETO.value` thay vì hardcode chuỗi chữ:

```python
def get_book_details(session: Session, book_id: uuid.UUID, user_id: uuid.UUID, *, mode: str | None = None) -> dict:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    # Kiểm tra Kế hoạch học tập hiện tại
    plan = get_current_plan_for_owned_book(session, user_id=user_id, book_id=book_id)
    
    # Graceful Fallback: Nếu sách chưa có ReadingPlan, trả về dữ liệu chuẩn bằng Enum PlanMode.PARETO.value
    if not plan:
        requested_mode = mode if mode else PlanMode.PARETO.value
        return {
            "book_id": book.id,
            "book_status": book.status,
            "mode": requested_mode,
            "total_sections": book.total_sections,
            "total_units": 0,
            "learning_summary": None,
            "units": [],
        }

    active_mode = PlanMode(mode) if mode else PlanMode(plan.mode)
    learning_summary = build_book_learning_summary_from_state(session, user_id=user_id, book_id=book_id, mode=active_mode)
    units = list_learning_units(session, book_id, active_mode)
    segments_map = _segments_by_unit(list_unit_segments(session, [unit.id for unit in units]))

    return {
        "book_id": book.id,
        "book_status": book.status,
        "mode": active_mode.value,
        "total_sections": book.total_sections,
        "total_units": len(units),
        "learning_summary": learning_summary,
        "units": [_unit_to_dict(unit, segments_map.get(unit.id, [])) for unit in units],
    }
```

---

## 4. Hướng Dẫn Từng Bước Cho Fresher (Step-by-Step Training Guide)

Chào bạn Fresher, đây là bài học quan trọng về **Thiết kế Hệ thống Sản xuất (Production Engineering)**. Hãy làm theo các bước dưới đây và đọc kỹ phần giải thích tư duy lập trình:

### Bài Học 1: Tại sao không gọi I/O mạng trong HTTP Request?
* **Khái niệm:** HTTP Request có thời gian sống rất ngắn. Mọi thao tác kết nối mạng bên ngoài (như Supabase Storage, S3, Sending Email) đều có nguy cơ bị chậm hoặc ngắt kết nối.
* **Tư duy Senior:** Xóa DB trước $\rightarrow$ Trả kết quả cho User ngay $\rightarrow$ Đẩy việc nặng cho Celery Worker làm ở dưới nền.

### Bước 1: Cấu hình DB Keepalive & Pool Recycle
1. Mở [app/core/config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py).
2. Tìm đến biến `DATABASE_POOL_RECYCLE` và sửa thành `280`. Thêm các biến `DATABASE_TCP_KEEPALIVES`.
3. Mở [app/db/database.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/db/database.py) và cập nhật hàm `_connect_args_for` theo mẫu ở **Bước 3.2**.

### Bước 2: Tạo Celery Task Dọn dẹp File Bất đồng bộ
1. Mở [app/tasks/book_tasks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/tasks/book_tasks.py).
2. Dán đoạn mã hàm `purge_book_storage_assets_task` ở **Bước 3.3** vào cuối file.

### Bước 3: Cập nhật Hàm Xóa Sách & Chi Tiết Sách
1. Mở [app/repositories/audiobook_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py), cập nhật `delete_book_storage` theo mẫu **Bước 3.4**.
2. Mở [app/services/audiobook_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/audiobook_service.py), cập nhật `get_book_details` theo mẫu **Bước 3.5**.

---

## 5. Kịch Bản Kiểm Thử & Xác Minh (Verification & Testing Spec)

### 5.1. Viết Automated Unit Test
Tạo file kiểm thử mới `tests/services/test_phase25_resilience_and_async_delete.py`:

```python
import uuid
import pytest
from sqlmodel import Session
from app.models.db_models import Book
from app.services.audiobook_service import get_book_details, delete_book_and_assets
from app.core.exceptions import BookNotFoundError

@pytest.mark.asyncio
async def test_get_book_details_graceful_fallback(db_session: Session, sample_user_id: uuid.UUID):
    # Tạo 1 sách chưa có ReadingPlan
    book = Book(user_id=sample_user_id, title="Sách Test Fallback", total_sections=5)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    # Gọi get_book_details phải trả về 200 OK với units rỗng thay vì ném ra Exception 400/404
    res = get_book_details(db_session, book.id, sample_user_id, mode="pareto")
    assert res["book_id"] == book.id
    assert res["learning_summary"] is None
    assert res["total_units"] == 0
    assert res["units"] == []

@pytest.mark.asyncio
async def test_fast_delete_book(db_session: Session, sample_user_id: uuid.UUID):
    # Tạo 1 sách test để xóa
    book = Book(user_id=sample_user_id, title="Sách Test Xóa Nhanh")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    # Thực hiện xóa
    await delete_book_and_assets(db_session, book_id, sample_user_id)

    # Bản ghi trong DB phải mất ngay lập tức
    deleted_book = db_session.get(Book, book_id)
    assert deleted_book is None
```

### 5.2. Chạy Lệnh Kiểm Thử
Chạy lệnh kiểm thử tự động trong Terminal:
```bash
uv run pytest tests/services/test_phase25_resilience_and_async_delete.py -v
```
Nếu tất cả kiểm thử báo màu xanh `PASSED`, toàn bộ hệ thống đã đạt chuẩn vận hành sản xuất ổn định và mượt mà!
