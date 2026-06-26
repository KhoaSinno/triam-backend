# Báo cáo Thiết kế & Hướng dẫn Triển khai: Tính năng Chọn Sách từ Thư viện Hệ thống (Shared Library)

Tài liệu này cung cấp bản thiết kế kỹ thuật hoàn chỉnh và hướng dẫn triển khai chi tiết cho tính năng: **Admin tải sách mẫu lên hệ thống -> User chọn sách từ thư viện này để học, đặt ReadingPlan và chạy RAG độc lập.**

---

## 1. Thay đổi Cấu trúc Database (Schema Migration)

Thêm hai trường mới vào class [Book](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/models/db_models.py#L54) trong file [db_models.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/models/db_models.py):

- **`is_shared` (bool)**: Đánh dấu sách thuộc thư viện dùng chung của hệ thống (do Admin upload). Default = `False`.
- **`parent_shared_id` (uuid.UUID, nullable)**: Trỏ tới `id` của cuốn sách hệ thống gốc nếu đây là bản sao (clone) của User. Default = `None`.

### Cập nhật Code Model:

```python
# Trong file app/models/db_models.py

class Book(SQLModel, table=True):
    __tablename__ = "books"

    # ... các trường cũ ...

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

_(Lưu ý: Chạy lệnh `uv run alembic revision --autogenerate -m "add shared book columns"` để tạo và chạy file migration đồng bộ database)._

---

## 2. Mã nguồn tầng Service: Logic Nhân bản (Cloning Service)

Khi User chọn một cuốn sách từ thư viện, Backend thực hiện nhân bản toàn bộ metadata sách đó sang cho User. Hàm này được thiết kế trong một Transaction an toàn và tối ưu hóa hiệu năng bằng **Bulk Insert** khi xử lý sách lớn:

```python
# Viết vào app/services/audiobook_service.py

import uuid
from sqlmodel import Session, select
from app.models.db_models import Book, BookSection, BookSectionKnowledge, LearningUnit, LearningUnitSegment, LearningUnitSource

def select_shared_book_to_user(session: Session, *, shared_book_id: uuid.UUID, user_id: uuid.UUID) -> Book:
    """
    Nhân bản toàn bộ metadata của một sách hệ thống (shared) cho một User cụ thể.
    Giữ nguyên các link audio/file vật lý trên Storage để tiết kiệm tài nguyên.
    """
    # 1. Kiểm tra sách gốc
    shared_book = session.get(Book, shared_book_id)
    if not shared_book or not shared_book.is_shared:
        raise ValueError("Sách hệ thống không tồn tại hoặc chưa được chia sẻ công khai.")

    # Kiểm tra xem user đã từng add cuốn này chưa
    existing = session.exec(
        select(Book).where(Book.parent_shared_id == shared_book_id, Book.user_id == user_id)
    ).first()
    if existing:
        return existing

    # 2. Tạo bản ghi Book mới cho User
    cloned_book = Book(
        user_id=user_id,
        title=shared_book.title,
        author=shared_book.author,
        file_url=shared_book.file_url,        # Trỏ chung đến file sách gốc
        document_type=shared_book.document_type,
        total_sections=shared_book.total_sections,
        total_units=shared_book.total_units,
        status="READY",                       # Sẵn sàng sử dụng ngay
        is_shared=False,
        parent_shared_id=shared_book.id
    )
    session.add(cloned_book)
    session.flush() # Lấy cloned_book.id

    # 3. Nhân bản BookSection (Cấu trúc cây mục lục)
    sections = session.exec(select(BookSection).where(BookSection.book_id == shared_book.id)).all()
    map_sections = {} # {old_section_id: new_section_id}

    for sec in sections:
        cloned_sec = BookSection(
            book_id=cloned_book.id,
            parent_id=None, # Sẽ map lại cấu trúc cây sau
            section_index=sec.section_index,
            title=sec.title,
            level=sec.level,
            path=sec.path,
            text_content=sec.text_content,
            text_char_count=sec.text_char_count,
            page_start=sec.page_start,
            page_end=sec.page_end,
            source_href=sec.source_href,
            source_anchor=sec.source_anchor
        )
        session.add(cloned_sec)
        session.flush()
        map_sections[sec.id] = cloned_sec.id

    # Map lại parent_id để khôi phục cấu trúc cây mục lục
    for sec in sections:
        if sec.parent_id and sec.parent_id in map_sections:
            new_sec = session.get(BookSection, map_sections[sec.id])
            new_sec.parent_id = map_sections[sec.parent_id]
            session.add(new_sec)

    # 4. Nhân bản BookSectionKnowledge (Vector Embeddings để RAG)
    knowledges = session.exec(select(BookSectionKnowledge).where(BookSectionKnowledge.book_id == shared_book.id)).all()

    # Tối ưu Bulk Insert nếu sách lớn (> 100 chunks) để tránh tràn RAM
    if len(knowledges) > 100:
        knowledge_mappings = [
            {
                "book_id": cloned_book.id,
                "section_id": map_sections[kn.section_id],
                "chunk_index": kn.chunk_index,
                "content": kn.content,
                "search_text": kn.search_text,
                "content_hash": kn.content_hash,
                "embedding_model": kn.embedding_model,
                "embedding_version": kn.embedding_version,
                "char_count": kn.char_count,
                "token_count": kn.token_count,
                "embedding": kn.embedding  # copy vector thô sang sách clone
            }
            for kn in knowledges
        ]
        session.bulk_insert_mappings(BookSectionKnowledge, knowledge_mappings)
    else:
        for kn in knowledges:
            cloned_kn = BookSectionKnowledge(
                book_id=cloned_book.id,
                section_id=map_sections[kn.section_id],
                chunk_index=kn.chunk_index,
                content=kn.content,
                search_text=kn.search_text,
                content_hash=kn.content_hash,
                embedding_model=kn.embedding_model,
                embedding_version=kn.embedding_version,
                char_count=kn.char_count,
                token_count=kn.token_count,
                embedding=kn.embedding
            )
            session.add(cloned_kn)

    # 5. Nhân bản LearningUnit (Các bài học mẫu)
    units = session.exec(select(LearningUnit).where(LearningUnit.book_id == shared_book.id)).all()
    map_units = {} # {old_unit_id: new_unit_id}

    for unit in units:
        cloned_unit = LearningUnit(
            user_id=user_id,
            book_id=cloned_book.id,
            mode=unit.mode,
            unit_index=unit.unit_index,
            title=unit.title,
            unit_type=unit.unit_type,
            status=unit.status,
            source_text_char_count=unit.source_text_char_count,
            estimated_tokens=unit.estimated_tokens,
            estimated_audio_seconds=unit.estimated_audio_seconds,
            main_segment_count=unit.main_segment_count,
            review_audio_url=unit.review_audio_url,
            review_text=unit.review_text,
            planner_reason=unit.planner_reason
        )
        session.add(cloned_unit)
        session.flush()
        map_units[unit.id] = cloned_unit.id

    # 6. Nhân bản LearningUnitSource (Liên kết mục lục & bài học)
    sources = session.exec(select(LearningUnitSource).where(LearningUnitSource.learning_unit_id.in_(list(map_units.keys())))).all()
    for src in sources:
        cloned_src = LearningUnitSource(
            learning_unit_id=map_units[src.learning_unit_id],
            section_id=map_sections[src.section_id],
            source_order=src.source_order
        )
        session.add(cloned_src)

    # 7. Nhân bản LearningUnitSegment (Phân đoạn và link file Audio)
    segments = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id.in_(list(map_units.keys())))).all()

    # Tối ưu Bulk Insert cho Segments lớn
    if len(segments) > 100:
        segment_mappings = [
            {
                "learning_unit_id": map_units[seg.learning_unit_id],
                "segment_index": seg.segment_index,
                "audio_url": seg.audio_url,
                "text_content": seg.text_content,
                "duration_ms": seg.duration_ms
            }
            for seg in segments
        ]
        session.bulk_insert_mappings(LearningUnitSegment, segment_mappings)
    else:
        for seg in segments:
            cloned_seg = LearningUnitSegment(
                learning_unit_id=map_units[seg.learning_unit_id],
                segment_index=seg.segment_index,
                audio_url=seg.audio_url,
                text_content=seg.text_content,
                duration_ms=seg.duration_ms
            )
            session.add(cloned_seg)

    session.commit()
    session.refresh(cloned_book)
    return cloned_book
```

---

## 3. Mã nguồn tầng Router: Các API Endpoint mới

Bổ sung các routes API mới vào file [audiobooks.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/audiobooks.py) (hoặc một file router riêng tùy chọn):

```python
# Thêm vào app/api/v1/routers/audiobooks.py

from fastapi import HTTPException
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
    User chọn một cuốn sách từ thư viện.
    Backend thực hiện nhân bản nhanh toàn bộ cấu trúc bài học và embeddings để sẵn sàng học ngay.
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

---

## 4. Phân quyền Admin: Upload & Đánh dấu Sách Thư viện

Để biến một cuốn sách đã xử lý thành sách mẫu của hệ thống, thêm route quản trị vào file [admin.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/api/v1/routers/admin.py):

```python
# Thêm vào app/api/v1/routers/admin.py

@router.patch("/books/{book_id}/share", response_model=BookResponse)
def make_book_shared(
    book_id: uuid.UUID,
    session: Annotated[Session, Depends(get_session)],
    current_admin: CurrentAdmin # Middleware kiểm tra quyền Admin
):
    """
    Đánh dấu cuốn sách đã qua xử lý thành sách dùng chung trong thư viện hệ thống.
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách.")
    if book.status != "READY":
        raise HTTPException(status_code=400, detail="Chỉ có thể chia sẻ sách đã hoàn thành xử lý dữ liệu.")

    book.is_shared = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
```

---

## 5. Điểm mấu chốt: "Cắt đuôi" luồng xóa sách (Chống xóa file gốc)

### ⚠️ Rủi ro đặc biệt nghiêm trọng:

Hiện tại, khi xóa sách, hàm [delete_book_storage](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py#L99) sẽ tự động gọi API Supabase Storage để xóa toàn bộ folder file vật lý dựa trên prefix là `book_id`.
Vì sách clone chia sẻ chung file sách gốc và các file âm thanh `.mp3` của sách hệ thống để tối ưu hóa tài nguyên:

- Nếu user xóa sách clone mà hệ thống **tiện tay xóa luôn file vật lý**, toàn bộ các User khác đang học cuốn sách đó sẽ lập tức bị lỗi _"Mất file âm thanh"_.
- **Giải pháp:** Chặn đứng (cắt đuôi) lệnh xóa Storage khi sách được xóa là sách clone (`parent_shared_id is not None`).

### 🛠️ Cập nhật hàm Xóa An toàn:

Thay thế code trong file [audiobook_repo.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/repositories/audiobook_repo.py#L99):

```python
# Trong file app/repositories/audiobook_repo.py

async def delete_book_storage(session: Session, book_id: uuid.UUID, user_id: uuid.UUID):
    """
    Xóa assets vật lý trên Storage (chỉ áp dụng cho sách tự upload gốc)
    và dọn dẹp sạch bản ghi metadata trong Database.
    """
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    str_book_id = str(book_id)

    # ĐIỂM MẤU CHỐT: Nếu là sách clone, CHỈ xóa DB, CẤM xóa file vật lý trên Storage
    if book.parent_shared_id is not None:
        log.info(f"Book {str_book_id} là sách clone. Bỏ qua bước xóa file vật lý trên Storage.")

        # Chỉ xóa DB records và các mối liên kết (notifications, plans, sessions)
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch sẽ database của sách clone: {str_book_id}")
        return

    # --- ĐỐI VỚI SÁCH TỰ UPLOAD GỐC (Chạy xóa file bình thường) ---
    target_buckets = ["audios", "raw_books"]
    try:
        # 1. Lấy danh sách file từ tất cả bucket liên quan qua RPC
        result = supabase.rpc("get_book_asset_paths", {"bucket_names": target_buckets, "book_id_prefix": str_book_id}).execute()

        # 2. Xóa file vật lý qua Storage API
        if result.data:
            data_list = result.data if isinstance(result.data, list) else []
            for bucket in target_buckets:
                paths = [str(item["name"]) for item in data_list if isinstance(item, dict) and item.get("bucket_id") == bucket]
                if paths:
                    supabase.storage.from_(bucket).remove(paths)
                    log.info(f"Đã xóa {len(paths)} files từ bucket: {bucket}")

        # 3. Xóa record trong DB + notification
        cleanup_book_side_effects(session, book_id=book_id, user_id=user_id)
        delete_book(session, book_id)
        log.info(f"Đã dọn dẹp sạch sẽ database cho book tự upload: {str_book_id}")

    except Exception as e:
        session.rollback()
        log.exception(f"Lỗi nghiêm trọng khi xóa book {str_book_id}: {e}")
        raise StorageOperationError("Không thể xóa tài nguyên sách trong Storage.") from e
```

---

## 6. Phân tích: Tại sao luồng Sinh Lịch học (Plan Job) chạy tức thì cho Sách Clone?

Khi User tạo Reading Plan cho sách clone, hệ thống sẽ tự động xếp lịch học qua Celery task `triam.books.process`.
Vì chúng ta đã copy toàn bộ `LearningUnit` và `LearningUnitSegment` ở trạng thái `"READY"` sang cho cuốn sách clone:

- Celery worker khi chạy hàm [process_learning_unit](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/learning_unit_worker.py#L40) sẽ kích hoạt dòng check sau:
  ```python
  if current_unit and current_unit.status == ProcessingJobStatus.READY and unit_segments_exist(session, unit.id):
      logger.info(f"Learning unit {unit.unit_index + 1} already READY, skip.")
      return LearningUnitProcessingResult(...)
  ```
- Do dữ liệu đã được nạp sẵn từ trước, worker sẽ **bỏ qua việc gọi LLM và bỏ qua việc sinh âm thanh (TTS)**. Tiến trình tạo plan sẽ hoàn tất **chỉ trong vòng dưới 1 giây**, chuyển trạng thái `ReadingPlan` sang `ACTIVE` ngay lập tức để user sẵn sàng học mà không phải chờ đợi xử lý file.
