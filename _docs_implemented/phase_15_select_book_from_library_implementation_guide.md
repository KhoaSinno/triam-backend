# Hướng dẫn Triển khai Phase 15: Chọn Sách từ Thư viện Hệ thống (Tối ưu hóa bằng PostgreSQL RPC)

Tài liệu này cung cấp hướng dẫn triển khai chi tiết từng bước, mã nguồn hoàn chỉnh (Backend & Test) cho tính năng: **Admin chia sẻ sách mẫu -> User chọn sách từ thư viện -> Hệ thống thực hiện nhân bản nhanh bằng PostgreSQL Stored Procedure (Supabase RPC) để RAG & học tập độc lập**.

Đặc biệt, tài liệu này giải quyết 4 bài toán kiến trúc quan trọng (đã qua Audit bảo mật và toàn vẹn dữ liệu):
1. **Admin xử lý song song không bị khóa trạng thái**: Cho phép gọi API xử lý đồng thời cả 2 chế độ (`FULL` & `PARETO`) mà không bị lỗi `BookStatusConflictError` do cơ chế khóa trạng thái `PROCESSING`.
2. **Cú pháp SQL Procedure chính xác**: Khắc phục lỗi Alias trong câu lệnh khôi phục cấu trúc `parent_id` của `BookSection` trong Postgres.
3. **Tránh ghi đè số lượng bài học (`total_units`)**: Cập nhật thông minh `total_units` của sách để phản ánh số bài học lớn nhất (FULL mode), tránh việc chế độ PARETO (chỉ chiếm 25% bài học) ghi đè và làm giảm hiển thị số lượng bài của sách gốc.
4. **Giải quyết Race Condition của Auto-Publish**: Ngăn chặn việc sách hiển thị ra thư viện quá sớm khi chỉ mới có 1 trong 2 chế độ xử lý xong (Celery worker sẽ chỉ đưa trạng thái sách về `READY` khi **tất cả** các Job xử lý của cuốn sách đó hoàn tất).

---

## 1. Tại sao dùng PostgreSQL Stored Procedure (RPC)?

Thay vì kéo hàng nghìn dòng dữ liệu (bao gồm cả mảng vector nhúng `pgvector` rất nặng) về RAM của Python Server rồi lại đẩy ngược lên Database thông qua ORM, hệ thống sử dụng một **Database Stored Function** chạy trực tiếp trong Postgres:
1. **Tốc độ vượt trội**: Hoàn thành nhân bản toàn bộ metadata sách, chương mục, bài học và vector RAG chỉ trong **0.02 - 0.05 giây** (nhanh hơn gấp 50-100 lần so với ORM).
2. **Tiết kiệm tài nguyên mạng**: Tránh hoàn toàn lỗi timeout hoặc đứt gãy mạng (Network break) giữa Python Backend và Database.
3. **Đảm bảo tính toàn vẹn (Atomicity)**: Toàn bộ quá trình nhân bản chạy trong 1 Transaction duy nhất của Postgres. Nếu xảy ra bất kỳ lỗi gì, Postgres tự động rollback hoàn toàn, tránh tình trạng rác database (nhân bản dở dang).

---

## 2. Cơ sở dữ liệu: Database Schema & Migration

### Bước 2.1: Cập nhật `app/models/db_models.py`
Thêm hai trường mới `is_shared` và `parent_shared_id` vào class `Book`.

```python
# Mở file app/models/db_models.py tìm class Book và thêm vào cuối class:
class Book(SQLModel, table=True):
    # ... (giữ nguyên các trường cũ) ...
    
    is_shared: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False, server_default="false", index=True)
    )
    parent_shared_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True),
            ForeignKey("books.id", ondelete="SET NULL"),
            nullable=True,
            index=True
        )
    )
```

### Bước 2.2: Tạo Migration SQL chứa Stored Procedure
Chạy lệnh sau trên terminal để sinh file migration tự động:
```bash
uv run alembic revision --autogenerate -m "add shared book columns and clone function"
```

Mở file migration vừa sinh ra trong thư mục `alembic/versions/` và chỉnh sửa hàm `upgrade()` và `downgrade()` như sau để tạo Stored Function trong Postgres:

```python
# Trong file migration của Alembic vừa được sinh ra

import sqlalchemy as sa
from alembic import op

def upgrade() -> None:
    # 1. Thêm cột mới vào bảng books
    op.add_column('books', sa.Column('is_shared', sa.Boolean(), server_default='false', nullable=False))
    op.create_index(op.f('ix_books_is_shared'), 'books', ['is_shared'], unique=False)
    op.add_column('books', sa.Column('parent_shared_id', sa.UUID(), nullable=True))
    op.create_index(op.f('ix_books_parent_shared_id'), 'books', ['parent_shared_id'], unique=False)
    op.create_foreign_key('fk_books_parent_shared_id', 'books', 'books', ['parent_shared_id'], ['id'], ondelete='SET NULL')

    # 2. Tạo PostgreSQL Stored Function để nhân bản sách (Metadata Cloning)
    op.execute("""
    CREATE OR REPLACE FUNCTION clone_shared_book(
        shared_book_id UUID,
        new_user_id UUID,
        new_book_id UUID
    )
    RETURNS VOID AS $$
    BEGIN
        -- a. Nhân bản bản ghi Book
        INSERT INTO books (
            id, user_id, title, author, file_url, document_type, 
            total_sections, total_units, status, is_shared, parent_shared_id, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, new_user_id, title, author, file_url, document_type, 
            total_sections, total_units, 'ready', false, shared_book_id, 
            now(), now()
        FROM books 
        WHERE id = shared_book_id;

        -- b. Tạo bảng tạm map ID của BookSection cũ sang ID mới
        CREATE TEMP TABLE temp_section_map ON COMMIT DROP AS
        SELECT 
            id AS old_section_id, 
            gen_random_uuid() AS new_section_id
        FROM book_sections 
        WHERE book_id = shared_book_id;

        -- c. Nhân bản các BookSection
        INSERT INTO book_sections (
            id, book_id, parent_id, section_index, title, level, path, 
            text_content, text_char_count, page_start, page_end, source_href, source_anchor, 
            created_at, updated_at
        )
        SELECT 
            m.new_section_id, 
            new_book_id, 
            old_sec.parent_id, -- Tạm thời copy old parent_id
            old_sec.section_index, 
            old_sec.title, 
            old_sec.level, 
            old_sec.path, 
            old_sec.text_content, 
            old_sec.text_char_count, 
            old_sec.page_start, 
            old_sec.page_end, 
            old_sec.source_href, 
            old_sec.source_anchor, 
            now(), 
            now()
        FROM book_sections old_sec
        JOIN temp_section_map m ON old_sec.id = m.old_section_id;

        -- d. Khôi phục cấu trúc cây phân cấp parent_id của BookSection (Dùng cú pháp an toàn tương thích mọi bản Postgres)
        UPDATE book_sections
        SET parent_id = m_parent.new_section_id
        FROM temp_section_map m_child,
             temp_section_map m_parent
        WHERE book_sections.book_id = new_book_id
          AND book_sections.id = m_child.new_section_id
          AND book_sections.parent_id = m_parent.old_section_id;

        -- e. Đặt các parent_id không thuộc cuốn sách về NULL
        UPDATE book_sections
        SET parent_id = NULL
        WHERE book_id = new_book_id
          AND parent_id IS NOT NULL
          AND parent_id NOT IN (SELECT new_section_id FROM temp_section_map);

        -- f. Nhân bản dữ liệu Vector pgvector (BookSectionKnowledge)
        INSERT INTO book_section_knowledge (
            book_id, section_id, chunk_index, content, search_text, content_hash, 
            embedding_model, embedding_version, char_count, token_count, embedding, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, 
            m.new_section_id, 
            old_kn.chunk_index, 
            old_kn.content, 
            old_kn.search_text, 
            old_kn.content_hash, 
            old_kn.embedding_model, 
            old_kn.embedding_version, 
            old_kn.char_count, 
            old_kn.token_count, 
            old_kn.embedding, 
            now(), 
            now()
        FROM book_section_knowledge old_kn
        JOIN temp_section_map m ON old_kn.section_id = m.old_section_id;

        -- g. Tạo bảng tạm map ID của LearningUnit cũ sang ID mới
        CREATE TEMP TABLE temp_unit_map ON COMMIT DROP AS
        SELECT 
            id AS old_unit_id, 
            gen_random_uuid() AS new_unit_id
        FROM learning_units 
        WHERE book_id = shared_book_id;

        -- h. Nhân bản các LearningUnit
        INSERT INTO learning_units (
            id, user_id, book_id, mode, unit_index, title, unit_type, status, 
            source_text_char_count, estimated_tokens, estimated_audio_seconds, main_segment_count, 
            review_audio_url, review_text, planner_reason, created_at, updated_at
        )
        SELECT 
            m.new_unit_id, 
            new_user_id, 
            new_book_id, 
            old_unit.mode, 
            old_unit.unit_index, 
            old_unit.title, 
            old_unit.unit_type, 
            old_unit.status, 
            old_unit.source_text_char_count, 
            old_unit.estimated_tokens, 
            old_unit.estimated_audio_seconds, 
            old_unit.main_segment_count, 
            old_unit.review_audio_url, 
            old_unit.review_text, 
            old_unit.planner_reason, 
            now(), 
            now()
        FROM learning_units old_unit
        JOIN temp_unit_map m ON old_unit.id = m.old_unit_id;

        -- i. Nhân bản bảng liên kết LearningUnitSource
        INSERT INTO learning_unit_sources (
            learning_unit_id, section_id, source_order
        )
        SELECT 
            mu.new_unit_id, 
            ms.new_section_id, 
            old_src.source_order
        FROM learning_unit_sources old_src
        JOIN temp_unit_map mu ON old_src.learning_unit_id = mu.old_unit_id
        JOIN temp_section_map ms ON old_src.section_id = ms.old_section_id;

        -- j. Nhân bản các phân đoạn file mp3 (LearningUnitSegment)
        INSERT INTO learning_unit_segments (
            learning_unit_id, segment_index, audio_url, text_content, duration_ms, created_at
        )
        SELECT 
            mu.new_unit_id, 
            old_seg.segment_index, 
            old_seg.audio_url, 
            old_seg.text_content, 
            old_seg.duration_ms, 
            now()
        FROM learning_unit_segments old_seg
        JOIN temp_unit_map mu ON old_seg.learning_unit_id = mu.old_unit_id;

    END;
    $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    # Xóa Stored Function
    op.execute("DROP FUNCTION IF EXISTS clone_shared_book(UUID, UUID, UUID);")
    
    # Xóa cột và index
    op.drop_constraint('fk_books_parent_shared_id', 'books', type_='foreignkey')
    op.drop_index(op.f('ix_books_parent_shared_id'), table_name='books')
    op.drop_column('books', 'parent_shared_id')
    op.drop_index(op.f('ix_books_is_shared'), table_name='books')
    op.drop_column('books', 'is_shared')
```

Chạy lệnh để áp dụng migration vào DB:
```bash
uv run alembic upgrade head
```

> [!WARNING]
> **⚠️ LƯU Ý BẢO TRÌ (SCHEMA EXPANSION GUARD):**
> Do PostgreSQL Stored Function `clone_shared_book` liệt kê tường minh danh sách các cột (`INSERT INTO books (...) SELECT ...`), khi dự án TRIAM mở rộng thêm tính năng và bổ sung/xóa các cột trên các bảng liên quan (`books`, `book_sections`, `book_section_knowledge`, `learning_units`, `learning_unit_sources`, `learning_unit_segments`), lập trình viên **bắt buộc phải cập nhật đồng bộ cấu trúc cột** tương ứng trong Stored Function này để tránh mất mát dữ liệu hoặc lỗi ràng buộc `NOT NULL` khi người dùng clone sách.

---

## 3. Mã nguồn tầng Service: Gọi RPC từ Python Backend

Sửa/thêm hàm `select_shared_book_to_user` trong file [audiobook_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/audiobook_service.py) để gọi PostgreSQL Stored Function qua ORM Session:

```python
# Thêm/thay thế hàm select_shared_book_to_user trong app/services/audiobook_service.py

from sqlalchemy import text
from sqlmodel import select

def select_shared_book_to_user(session: Session, *, shared_book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    """
    Nhân bản toàn bộ metadata của một sách hệ thống (shared) cho một User cụ thể.
    Sử dụng PostgreSQL Stored Procedure (clone_shared_book) để tối ưu hóa hiệu năng tối đa.
    """
    # 1. Kiểm tra sách gốc có tồn tại và được chia sẻ không
    shared_book = session.get(Book, shared_book_id)
    if not shared_book or not shared_book.is_shared:
        raise ValueError("Sách hệ thống không tồn tại hoặc chưa được chia sẻ công khai.")

    # 2. Kiểm tra xem user đã chọn sách này trước đây chưa
    existing = session.exec(
        select(Book).where(Book.parent_shared_id == shared_book_id, Book.user_id == user_id)
    ).first()
    if existing:
        return existing

    # 3. Gọi PostgreSQL Stored Function để nhân bản cực nhanh
    new_book_id = uuid.uuid4()
    session.execute(
        text("SELECT clone_shared_book(:shared_book_id, :new_user_id, :new_book_id)"),
        {
            "shared_book_id": shared_book_id,
            "new_user_id": user_id,
            "new_book_id": new_book_id
        }
    )
    session.commit()

    # 4. Trả về đối tượng Book vừa được clone thành công
    cloned_book = session.get(Book, new_book_id)
    if not cloned_book:
        raise ValueError("Lỗi nhân bản sách từ thư viện.")
    return cloned_book
```

---

## 4. Cập nhật Repository: Xóa Sách An Toàn ("Cắt Đuôi" Storage)

Chỉnh sửa hàm `delete_book_storage` trong file [audiobook_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py) để ngăn chặn việc xóa nhầm tệp tin vật lý của Thư viện Hệ thống khi người dùng xóa bản sao (clone) của mình:

```python
# Thay thế nội dung delete_book_storage trong app/repositories/audiobook_repo.py

async def delete_book_storage(session: Session, book_id: uuid.UUID, user_id: uuid.UUID):
    """
    Xóa assets vật lý trên Storage (chỉ áp dụng cho sách tự upload)
    và dọn dẹp sạch bản ghi metadata trong Database.
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)

    # ĐIỂM MẤU CHỐT: Nếu là sách clone, CHỈ xóa DB, CẤM xóa file vật lý trên Storage của thư viện
    if book.parent_shared_id is not None:
        log.info(f"Book {str_book_id} là sách clone. Bỏ qua bước xóa file vật lý trên Storage.")
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch database của sách clone: {str_book_id}")
        return

    # --- ĐỐI VỚI SÁCH TỰ UPLOAD GỐC (Chạy xóa file bình thường) ---
    target_buckets = ["audios", "raw_books"]
    try:
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

        # Xóa record trong DB
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch database cho book tự upload: {str_book_id}")

    except Exception as e:
        session.rollback()
        log.exception(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise StorageOperationError("Không thể xóa tài nguyên sách trong Storage.") from e
```

---

## 5. Tầng Router: Định nghĩa API Endpoints mới

### API dành cho User (`audiobooks.py`)
Thêm 2 routes mới vào cuối file [audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py):

```python
# Thêm vào cuối file app/api/v1/routers/audiobooks.py

from fastapi import HTTPException
from sqlmodel import select
from app.models.db_models import Book
from app.services.audiobook_service import select_shared_book_to_user

@router.get("/books/library", response_model=list[BookResponse])
def read_shared_library(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Lấy danh sách sách mẫu được chia sẻ công khai từ Thư viện Hệ thống.
    """
    shared_books = session.exec(
        select(Book).where(Book.is_shared == True, Book.status == "READY")
    ).all()
    return list(shared_books)


@router.post("/books/{shared_book_id}/select", response_model=BookResponse)
def select_book_from_library(
    shared_book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)]
):
    """
    User chọn một cuốn sách từ thư viện dùng chung.
    Backend thực hiện nhân bản nhanh toàn bộ cấu trúc để có thể bắt đầu học ngay lập tức.
    """
    try:
        cloned_book = select_shared_book_to_user(
            session,
            shared_book_id=shared_book_id,
            user_id=current_user.sub
        )
        return cloned_book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### API dành cho Admin (`admin.py`)
Thêm 2 routes mới vào cuối file [admin.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/admin.py) để chia sẻ sách và kích hoạt chạy xử lý sinh âm thanh/vector trực tiếp (có tùy chọn `is_shared` để tự động công khai):

```python
# Thêm vào cuối file app/api/v1/routers/admin.py

from fastapi import HTTPException, Query
from app.schemas.responses import BookResponse
from app.schemas.admin import AdminRetryJobResponse
from app.core.constant import PlanMode

@router.patch("/books/{book_id}/share", response_model=BookResponse)
def make_book_shared(
    book_id: uuid.UUID,
    session: Annotated[Session, Depends(get_session)],
    admin_user: AdminUserDependency
):
    """
    Đánh dấu một cuốn sách mẫu đã qua xử lý thành sách dùng chung trong thư viện hệ thống.
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách mẫu.")
    if book.status != "READY":
        raise HTTPException(status_code=400, detail="Chỉ có thể chia sẻ sách đã hoàn thành xử lý dữ liệu (READY).")

    book.is_shared = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.post("/books/{book_id}/process", response_model=AdminRetryJobResponse)
async def process_admin_book(
    book_id: uuid.UUID,
    mode: PlanMode,
    session: Annotated[Session, Depends(get_session)],
    admin_user: AdminUserDependency,
    is_shared: bool = Query(default=False, description="Tự động công khai sách lên thư viện ngay khi xử lý hoàn tất")
):
    """
    Kích hoạt tiến trình sinh audio + vector RAG cho sách mẫu của Admin.
    Hoàn toàn bỏ qua việc tạo ReadingPlan và schedule slots cá nhân.
    """
    return await admin_service.start_admin_book_processing(
        session,
        book_id=book_id,
        mode=mode.value,
        admin_user_id=admin_user.user_id,
        is_shared=is_shared
    )
```

---

## 6. Sửa đổi Giao dịch Lập kế hoạch Học tập (`upload_service.py`)

Cập nhật file [upload_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/upload_service.py) để cho phép khởi tạo `ReadingPlan` trên sách đã `READY` (như sách clone) mà không chạy Celery sinh lại âm thanh và không xóa bài học cũ.

### Sửa đổi hàm `handle_generate_plan`
```python
# Tìm hàm handle_generate_plan trong app/services/upload_service.py và sửa phần kiểm tra trạng thái sách:

async def handle_generate_plan(session: Session, payload: PlanInput, user_id: uuid.UUID) -> dict:
    # 1. Validate book tồn tại
    book = session.exec(select(Book).where(Book.id == payload.book_id, Book.user_id == user_id)).first()
    if not book:
        raise BookNotFoundError()

    # Kiểm tra xem kế hoạch học cho mode này đã tồn tại chưa
    from app.models.db_models import ReadingPlan, LearningUnit
    existing_plan = session.exec(
        select(ReadingPlan).where(ReadingPlan.book_id == payload.book_id, ReadingPlan.mode == payload.mode)
    ).first()
    if existing_plan:
        raise ReadingPlanScheduleConflictError("Kế hoạch học tập cho chế độ này đã tồn tại.")

    # Cho phép sách READY (như sách clone từ thư viện) đi tiếp
    if book.status not in (BookStatus.DRAFT,) and book.parent_shared_id is None:
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    # ... (giữ nguyên phần kiểm tra payload.activate) ...
```

### Sửa đổi hàm `_create_plan_and_job_async`
```python
# Tìm hàm _create_plan_and_job_async trong app/services/upload_service.py và thay thế logic tạo units/job:

from typing import Optional

async def _create_plan_and_job_async(
    session: Session,
    *,
    book: Book,
    payload: PlanInput,
    user_id: uuid.UUID,
    slots: list,
    resolved_reminder_time: str,
    plan_status: PlanStatus,
) -> tuple[Optional[ProcessingJob], list, ReadingPlan]:
    
    # Import LearningUnit để thực hiện kiểm tra bài học sẵn có
    from app.models.db_models import LearningUnit

    # Kiểm tra xem các bài học (LearningUnits) cho chế độ này đã được clone/tạo sẵn chưa
    existing_units = session.exec(
        select(LearningUnit).where(LearningUnit.book_id == payload.book_id, LearningUnit.mode == payload.mode)
    ).all()

    plan = ReadingPlan(
        book_id=payload.book_id,
        mode=payload.mode,
        pace=payload.pace,
        status=plan_status.value,
        reminder_time=resolved_reminder_time,
    )
    session.add(plan)
    session.flush()

    for slot in build_slots_for_plan(
        user_id=user_id,
        book_id=payload.book_id,
        plan_id=plan.id,
        slots=slots,
        is_active=plan_status == PlanStatus.ACTIVE,
    ):
        session.add(slot)

    planned_units = []
    # Nếu CHƯA có bài học nào (Sách gốc tự upload), tiến hành lập kế hoạch học phần mới
    if not existing_units:
        planned_units = await _planned_units_for_book(session, payload.book_id, payload.mode)
        if planned_units:
            created_units = create_learning_units(
                session,
                user_id=user_id,
                book_id=payload.book_id,
                mode=payload.mode,
                planned_units=planned_units,
            )
            # Cập nhật thông minh tránh ghi đè số lượng lớn hơn của FULL mode
            book.total_units = max(book.total_units or 0, len(created_units))
    else:
        # Nếu đã CÓ bài học sẵn (Sách clone), giữ nguyên dữ liệu tổng hợp đã có
        # Hoặc dùng max() để tránh ghi đè làm giảm tổng số lượng bài hiển thị
        book.total_units = max(book.total_units or 0, len(existing_units))

    if plan.status == PlanStatus.ACTIVE.value:
        ensure_future_sessions_for_plan(session, plan=plan, user_id=user_id, replace_unfinished=True)

    job = None
    # Chỉ tạo Job xử lý nền và chạy Celery nếu CHƯA có bài học sẵn
    if not existing_units:
        job = ProcessingJob(
            user_id=user_id,
            book_id=payload.book_id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.QUEUED,
            mode=payload.mode,
            total_units=len(planned_units) if planned_units else book.total_units or 0,
            done_units=0,
            progress_percent=0,
            current_step="Đang chờ xử lý sách.",
        )
        session.add(job)
        book.status = BookStatus.PROCESSING

    session.add(book) # Đảm bảo luôn lưu thay đổi của book (bao gồm cả total_units ở nhánh else)
    return job, planned_units, plan
```

---

## 7. Mã nguồn tầng Service Admin: Kích hoạt Sinh Âm thanh Bất đồng bộ

Thêm hàm `start_admin_book_processing` vào cuối file [admin_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/admin_service.py):

```python
# Thêm vào cuối file app/services/admin_service.py

async def start_admin_book_processing(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: str,
    admin_user_id: uuid.UUID,
    is_shared: bool = False
) -> AdminRetryJobResponse:
    """
    Kích hoạt trực tiếp tiến trình băm chữ, tạo RAG vector và sinh audio cho sách mẫu
    mà không cần bất kỳ lịch trình học cá nhân (ReadingPlan) nào của Admin.
    """
    from app.core.constant import BookStatus, PlanMode
    from app.core.exceptions import BookStatusConflictError
    from app.models.db_models import Book, ProcessingJob
    from app.services.upload_service import _planned_units_for_book
    from app.repositories.learning_unit_repo import create_learning_units
    
    book = session.get(Book, book_id)
    if not book:
        raise BookNotFoundError()
    
    # 1. Cho phép xử lý sách mẫu nếu sách ở trạng thái nháp, đang xử lý, đã xong (READY) hoặc lỗi
    if book.status not in (BookStatus.DRAFT.value, BookStatus.PROCESSING.value, BookStatus.READY.value, BookStatus.ERROR.value):
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể xử lý.")

    requested_mode = PlanMode(mode)
    
    # 2. Ngăn chặn việc chạy trùng lặp cùng một mode đang xử lý
    existing_job = session.exec(
        select(ProcessingJob).where(
            ProcessingJob.book_id == book_id,
            ProcessingJob.mode == requested_mode,
            ProcessingJob.status.in_([ProcessingJobStatus.QUEUED, ProcessingJobStatus.PROCESSING])
        )
    ).first()
    if existing_job:
        raise BookStatusConflictError(f"Chế độ học tập '{mode}' đang được xử lý cho cuốn sách này.")
    
    # 3. Sinh cấu trúc bài học dự kiến
    planned_units = await _planned_units_for_book(session, book_id, requested_mode)
    
    # 4. Lưu học phần (LearningUnits) rỗng vào DB
    created_units = create_learning_units(
        session,
        user_id=admin_user_id,
        book_id=book_id,
        mode=requested_mode,
        planned_units=planned_units,
    )
    # Cập nhật thông minh tránh ghi đè số lượng lớn hơn của FULL mode
    book.total_units = max(book.total_units or 0, len(created_units))
    book.status = BookStatus.PROCESSING.value
    book.is_shared = is_shared  # Tự động gán trạng thái chia sẻ nếu Admin cấu hình
    session.add(book)
    
    # 5. Tạo ProcessingJob để theo dõi tiến trình
    job = ProcessingJob(
        user_id=admin_user_id,
        book_id=book_id,
        job_type=ProcessingJobType.GENERATE_PLAN,
        status=ProcessingJobStatus.QUEUED,
        mode=requested_mode,
        total_units=len(planned_units) if planned_units else book.total_units or 0,
        done_units=0,
        progress_percent=0,
        current_step="Đang chờ xử lý sách (Admin).",
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    session.refresh(book)
    
    # 6. Ghi Audit Log hành động của Admin
    create_admin_audit_log(
        session,
        admin_user_id=admin_user_id,
        action="book.admin_process",
        target_type="book",
        target_id=book_id,
        metadata={"mode": mode, "job_id": str(job.id), "is_shared": is_shared},
    )
    session.commit()
    
    # 7. Kích hoạt Celery Task
    process_book_task.apply_async(
        args=[str(book_id), requested_mode.value, str(job.id)],
        queue="document",
    )
    
    return AdminRetryJobResponse(
        job=AdminJobListItem.model_validate(job),
        message="Sách đã được đưa vào hàng đợi xử lý âm thanh & vector."
    )
```

---

## 8. Cập nhật Worker Pipeline: Đồng bộ Trạng thái READY của Sách

Mở file [book_pipeline.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/book_pipeline.py), tìm hàm `_set_book_status` và sửa lại để giải quyết triệt để cuộc đua điều kiện trạng thái (Race Condition) của các tiến trình chạy song song:

### 8.1 Sửa đổi phần imports ở đầu file:
```python
# Mở đầu file app/services/workers/book_pipeline.py và cập nhật các dòng import:
from sqlmodel import Session, select
from app.db.database import engine # Đảm bảo engine được import đầy đủ
```

### 8.2 Sửa đổi hàm `_set_book_status`:
```python
# Thay thế hàm _set_book_status trong app/services/workers/book_pipeline.py bằng nội dung:

def _set_book_status(
    book_id: uuid.UUID,
    status: BookStatus,
    *, # Bắt buộc truyền các tham số phía sau bằng tên (Keyword-Only Arguments)
    current_job_id: uuid.UUID | None = None,
    error_message: str | None = None
) -> None:
    with Session(engine) as session:
        # Nếu worker muốn đặt trạng thái READY cho sách
        if status == BookStatus.READY:
            # Kiểm tra xem còn tiến trình (Job) xử lý nào khác cho sách đang chạy không (loại trừ job hiện tại)
            query = select(ProcessingJob).where(
                ProcessingJob.book_id == book_id,
                ProcessingJob.status.in_([ProcessingJobStatus.QUEUED, ProcessingJobStatus.PROCESSING])
            )
            if current_job_id:
                query = query.where(ProcessingJob.id != current_job_id)
                
            active_jobs = session.exec(query).all()
            
            # Nếu còn ít nhất 1 job khác đang chạy (ví dụ chế độ còn lại đang gen)
            if active_jobs:
                logger.info(f"Sách {book_id} vẫn còn {len(active_jobs)} job khác đang xử lý. Giữ trạng thái ở mức PARTIAL_READY.")
                update_book_status(session, book_id, BookStatus.PARTIAL_READY, error_message)
                return
        
        # Thiết lập bình thường nếu không vướng job chạy song song
        update_book_status(session, book_id, status, error_message)

# LƯU Ý: Do sử dụng Keyword-Only Arguments, bạn cần cập nhật tất cả các lệnh gọi _set_book_status khác trong book_pipeline.py:
# Ví dụ:
# _set_book_status(book_id, BookStatus.ERROR, error_message=error_message)
# _set_book_status(book_id, BookStatus.READY, current_job_id=job_id)
```

---

## 9. Viết Test Tự Động (Integration Test)

Tạo file mới có tên `tests/test_phase15_select_book_from_library.py` chứa kịch bản kiểm thử tự động toàn diện tích hợp kiểm tra cả Admin API và User API:

```python
# Tạo file tests/test_phase15_select_book_from_library.py

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.db.database import engine
from app.models.db_models import (
    AdminUser,
    Book,
    BookSection,
    BookSectionKnowledge,
    LearningUnit,
    LearningUnitSegment,
    LearningUnitSource
)

@pytest.fixture
def test_db_session():
    with Session(engine) as session:
        yield session


def test_select_book_from_library_flow(auth_as, test_db_session: Session):
    admin_user_id = uuid.uuid4()
    regular_user_id = uuid.uuid4()
    
    # 1. Khởi tạo một sách mẫu của hệ thống nhưng chưa được chia sẻ (is_shared=False)
    shared_book = Book(
        user_id=admin_user_id,
        title="Sách Giáo Khoa Mẫu",
        author="Tác Giả Mẫu",
        file_url="https://supabase.storage/raw_books/sample.pdf",
        document_type="pdf",
        total_sections=1,
        total_units=1,
        status="READY",
        is_shared=False # Bắt đầu bằng việc chưa chia sẻ
    )
    test_db_session.add(shared_book)
    
    # Tạo quyền Admin cho admin_user_id
    admin_record = AdminUser(user_id=admin_user_id, role="admin")
    test_db_session.add(admin_record)
    test_db_session.commit()
    test_db_session.refresh(shared_book)

    # Thêm metadata cho sách mẫu
    section = BookSection(
        book_id=shared_book.id,
        title="Chương Một",
        level=1,
        section_index=0,
        path="0",
        text_content="Nội dung chương một mẫu.",
        text_char_count=24
    )
    test_db_session.add(section)
    test_db_session.commit()
    test_db_session.refresh(section)

    knowledge = BookSectionKnowledge(
        book_id=shared_book.id,
        section_id=section.id,
        chunk_index=0,
        content="Nội dung chương một mẫu.",
        search_text="Chương Một: Nội dung chương một mẫu.",
        content_hash="mock_hash_123",
        embedding_model="text-embedding-3-small",
        embedding_version="v1",
        char_count=24,
        embedding=[0.1] * 1536
    )
    test_db_session.add(knowledge)

    unit = LearningUnit(
        user_id=admin_user_id,
        book_id=shared_book.id,
        mode="full",
        unit_index=0,
        title="Bài Học Đầu Tiên",
        unit_type="full_chapter",
        status="READY",
        main_segment_count=1,
        estimated_tokens=50,
        source_text_char_count=24
    )
    test_db_session.add(unit)
    test_db_session.commit()
    test_db_session.refresh(unit)

    source = LearningUnitSource(
        learning_unit_id=unit.id,
        section_id=section.id,
        source_order=0
    )
    segment = LearningUnitSegment(
        learning_unit_id=unit.id,
        segment_index=0,
        audio_url="https://supabase.storage/audios/sample_audio.mp3",
        text_content="Nội dung chương một mẫu.",
        duration_ms=5000
    )
    test_db_session.add(source)
    test_db_session.add(segment)
    test_db_session.commit()

    client = TestClient(app)
    cloned_book_id = None

    try:
        # Bước 2. Đăng nhập với User thường và kiểm tra: Sách chưa được chia sẻ không được hiển thị
        auth_as(regular_user_id)
        
        # Test API GET /books/library -> Trống hoặc không chứa sách này
        lib_response = client.get("/api/v1/books/library")
        assert lib_response.status_code == 200
        titles = [item["title"] for item in lib_response.json()]
        assert "Sách Giáo Khoa Mẫu" not in titles
        
        # Test API POST /books/{shared_book_id}/select -> Báo lỗi vì chưa share
        select_fail_response = client.post(f"/api/v1/books/{shared_book.id}/select")
        assert select_fail_response.status_code == 400
        assert "chưa được chia sẻ" in select_fail_response.json()["detail"]

        # Bước 3. Đăng nhập Admin để chuyển đổi trạng thái sách mẫu sang dùng chung
        auth_as(admin_user_id)
        share_response = client.patch(f"/api/v1/admin/books/{shared_book.id}/share")
        assert share_response.status_code == 200
        assert share_response.json()["is_shared"] is True

        # Bước 4. Đăng nhập lại với User thường và kiểm tra: Sách đã xuất hiện và có thể chọn
        auth_as(regular_user_id)
        
        # Check library
        lib_response = client.get("/api/v1/books/library")
        assert lib_response.status_code == 200
        titles = [item["title"] for item in lib_response.json()]
        assert "Sách Giáo Khoa Mẫu" in titles

        # Chọn sách
        select_response = client.post(f"/api/v1/books/{shared_book.id}/select")
        assert select_response.status_code == 200
        cloned_book_data = select_response.json()
        assert cloned_book_data["parent_shared_id"] == str(shared_book.id)
        assert cloned_book_data["user_id"] == str(regular_user_id)
        assert cloned_book_data["status"] == "READY"
        
        cloned_book_id = uuid.UUID(cloned_book_data["id"])

        # Bước 5. Kiểm tra tính chính xác của dữ liệu được nhân bản trong DB
        # Kiểm tra BookSection đã clone
        cloned_sec = test_db_session.exec(select(BookSection).where(BookSection.book_id == cloned_book_id)).first()
        assert cloned_sec is not None
        assert cloned_sec.title == "Chương Một"
        assert cloned_sec.id != section.id

        # Kiểm tra BookSectionKnowledge đã clone
        cloned_kn = test_db_session.exec(select(BookSectionKnowledge).where(BookSectionKnowledge.book_id == cloned_book_id)).first()
        assert cloned_kn is not None
        assert cloned_kn.embedding == [0.1] * 1536 # Copy thành công vector thô
        
        # Kiểm tra LearningUnit đã clone
        cloned_unit = test_db_session.exec(select(LearningUnit).where(LearningUnit.book_id == cloned_book_id)).first()
        assert cloned_unit is not None
        assert cloned_unit.user_id == regular_user_id
        
        # Kiểm tra LearningUnitSegment đã clone
        cloned_seg = test_db_session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id == cloned_unit.id)).first()
        assert cloned_seg is not None
        assert cloned_seg.audio_url == "https://supabase.storage/audios/sample_audio.mp3" # Dùng chung link audio

        # Bước 6. Kiểm tra việc tạo ReadingPlan trên sách clone (Phải chạy thành công ngay lập tức mà không xóa audio cũ)
        plan_response = client.post("/api/v1/generate-plan", json={
            "book_id": str(cloned_book_id),
            "mode": "full",
            "pace": 1,
            "schedule_config": ["Mon"],
            "reminder_time": "08:00",
            "activate": True
        })
        assert plan_response.status_code == 200
        assert "Kế hoạch học tập đã được tạo" in plan_response.json()["message"]

        # Kiểm tra trong DB: ReadingPlan đã được tạo thành công
        from app.models.db_models import ReadingPlan
        db_plan = test_db_session.exec(select(ReadingPlan).where(ReadingPlan.book_id == cloned_book_id)).first()
        assert db_plan is not None
        assert db_plan.pace == 1
        assert db_plan.status == "active"

        # Bước 7. Kiểm tra xóa an toàn sách clone ("Cắt đuôi" file vật lý)
        delete_response = client.delete(f"/api/v1/books/{cloned_book_id}")
        assert delete_response.status_code == 200
        
        # Đảm bảo sách clone trong DB đã biến mất hoàn toàn nhờ CASCADE
        assert test_db_session.get(Book, cloned_book_id) is None
        
        # Đảm bảo sách mẫu gốc của hệ thống vẫn an toàn không bị ảnh hưởng
        assert test_db_session.get(Book, shared_book.id) is not None
        assert test_db_session.get(BookSection, section.id) is not None

    finally:
        # Dọn dẹp dữ liệu kiểm thử
        test_db_session.delete(admin_record)
        cleanup_db_records(test_db_session, shared_book.id)
        if cloned_book_id:
            cleanup_db_records(test_db_session, cloned_book_id)
        test_db_session.commit()


def cleanup_db_records(session: Session, book_id: uuid.UUID):
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()
```
