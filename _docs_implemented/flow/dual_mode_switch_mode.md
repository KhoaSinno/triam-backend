# 📚 Tài Liệu Kỹ Thuật: Hệ Thống Dual-Mode (Full & Pareto)

Tài liệu này được soạn thảo để giúp bạn hiểu rõ **toàn bộ kiến trúc, luồng xử lý, và tư duy code** đằng sau tính năng xử lý Sách nói Đa chế độ (Dual-Mode) bao gồm `full` (Đọc toàn bộ) và `pareto` (Tóm tắt ý chính), cũng như cơ chế chuyển đổi qua lại (`switch-mode`) mượt mà. 

Trong tài liệu này, chúng ta sẽ đi sâu vào từng dòng code quan trọng để bạn nắm bắt chính xác cách hoạt động của hệ thống.

---

## 1. Tổng quan về Bài toán & Tư duy thiết kế

### Vấn đề ban đầu
Hệ thống cần xử lý 1 file PDF nhưng cho phép sinh ra 2 loại nội dung âm thanh khác nhau:
1. **Full Mode**: Đọc chi tiết toàn bộ sách.
2. **Pareto Mode**: Chỉ đọc tóm tắt các ý chính (nguyên lý 80/20).

### Tư duy Thiết kế (Architecture Mindset)
* **Không làm mất dữ liệu cũ**: Nếu user đang ở `full`, chuyển sang `pareto` rồi lại chuyển về `full`, hệ thống **không được phép** chạy lại LLM/TTS cho `full` vì tốn kém chi phí AI và thời gian. Dữ liệu của từng mode phải được lưu trữ độc lập.
* **Tách biệt Database**: Thay vì tạo 2 bảng khác nhau cho 2 mode, chúng ta thêm trường `mode` vào bảng `chapter_segments`. Nghĩa là 1 chapter có thể có nhiều segment thuộc `full` và nhiều segment thuộc `pareto`.
* **Tách biệt Storage**: Tránh ghi đè file âm thanh trên Supabase. Path lưu trữ phải chứa tên `mode` để các file `.mp3` không bị trùng lặp.
* **Bất đồng bộ (Async)**: Quá trình gọi LLM (để tóm tắt) và TTS (để tạo giọng nói) rất chậm. Mọi API phải trả về ngay lập tức (200 OK) và để việc xử lý nặng cho `BackgroundTasks`.

---

## 2. Cấu trúc Database (Những thay đổi quan trọng)

Chúng ta sử dụng **SQLModel** (dựa trên SQLAlchemy) để thao tác với DB. Để phục vụ Dual-Mode, hệ thống có các thay đổi sau:

### Bảng `ReadingPlan` (Kế hoạch học tập)
```python
class ReadingPlan(SQLModel, table=True):
    __tablename__ = "reading_plans"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    mode: str  # Lưu mode hiện tại đang được active ("full" hoặc "pareto")
```
* **Mục đích**: Bảng này đại diện cho "trạng thái đang chọn" của user. App Frontend sẽ nhìn vào đây để biết hiển thị giao diện cho mode nào.

### Bảng `ChapterSegment` (Đoạn âm thanh)
```python
class ChapterSegment(SQLModel, table=True):
    __tablename__ = "chapter_segments"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chapter_id: uuid.UUID = Field(foreign_key="chapters.id")
    audio_url: str
    text_content: str
    mode: str = Field(default="full") # Đánh dấu đoạn audio này thuộc về mode nào
```
* **Mục đích**: Một Chapter (chương) có thể có 5 segment `full` và 2 segment `pareto`. Khi gọi API lấy chi tiết sách, backend sẽ filter danh sách trả về dựa theo `mode` đang lưu trong `ReadingPlan`.

---

## 3. Luồng 1: Upload và Generate Plan (Lần đầu)

### A. API `/upload`
1. Nhận file PDF.
2. Lưu file lên Supabase Storage (`/raw_books/{book_id}/original.pdf`).
3. Dùng thư viện `PyMuPDF` / Regex để bóc tách mục lục (Outline).
4. Lưu sách và các `Chapter` (trạng thái DRAFT) vào DB.

### B. API `/generate-plan`
1. User chọn mode (vd: `"full"`) và config lịch học.
2. API chuẩn hóa mode đầu vào (`FULL_MODE` -> `full`).
3. Lưu thông tin vào `ReadingPlan`.
4. Gọi `BackgroundTasks` chạy hàm `run_background_processing(book_id, mode)`.
5. Trả về `200 OK` ngay lập tức để UI không bị treo.

---

## 4. Luồng 2: Xử lý Background AI (Trái tim của hệ thống)

Hàm `run_background_processing` điều phối công việc nặng. Mỗi chương chạy 2 luồng đồng thời: `_thread_1_rag` và `_thread_2_tts`. 

Dưới đây là hàm `_thread_2_tts` đảm nhận việc gọi LLM và TTS:

```python
async def _thread_2_tts(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str, # Tham số mode (full/pareto) được truyền vào đây
) -> None:
    # Bước 1: LLM Rewrite (Phụ thuộc vào mode)
    # LLM sẽ trả về main_scripts (cho nội dung) và review_script (cho tổng kết)
    obj_chapter = await normalize_text_for_speech(raw_text, mode)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # ... Lưu review text vào db ...

    # Bước 2: TTS + Upload từng segment
    segments: list[ChapterSegment] = []
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            # 2a. Gọi API Text-to-Speech
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            
            # 2b. Định nghĩa Storage Path TRÁNH XUNG ĐỘT (Có kẹp {mode})
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/part_{i + 1}.mp3"
            
            # 2c. Upload file lên Supabase
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            
            # 2d. Khởi tạo Object Segment với mode tương ứng để lưu vào DB
            segments.append(
                ChapterSegment(
                    chapter_id=chapter_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                    mode=mode, # QUAN TRỌNG: Gắn cờ mode
                )
            )
        except Exception as seg_err:
            logger.warning(f"Lỗi TTS: {seg_err}")
        finally:
            if os.path.exists(local_file): os.remove(local_file)

    # Bước 3: Bulk save segments vào Database
    if segments:
        with Session(engine) as session:
            bulk_create_segments(session, segments)
```

**Phân tích Code:**
* `normalize_text_for_speech(..., mode)`: Prompt của Gemini phụ thuộc vào cờ mode. Nếu `pareto`, Prompt yêu cầu tóm tắt siêu ngắn. Nếu `full`, giữ nguyên ý nhưng đổi sang văn phong kể chuyện.
* Việc kẹp `{mode}` vào biến `storage_path` đảm bảo file MP3 của 2 mode nằm ở 2 thư mục hoàn toàn khác nhau. Đây là điểm then chốt tránh bug ghi đè (duplicate) trên Supabase.

---

## 5. Luồng 3: Switch Mode (Chuyển đổi chế độ)

Đây là chức năng quan trọng để giúp tiết kiệm chi phí. Khi User bấm nút chuyển mode (vd từ `full` sang `pareto`), Backend sẽ tiếp nhận ở API `/switch-mode`.

### A. Code API Endpoint (`/switch-mode`)

```python
@router.post("/books/{book_id}/switch-mode")
def switch_book_mode(book_id: uuid.UUID, payload: SwitchModeRequest, background_tasks: BackgroundTasks, session: Session):
    # Lấy plan hiện tại
    plan = session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()
    
    # TRƯỜNG HỢP 1: User bấm switch sang đúng mode đang dùng -> Bỏ qua
    if plan.mode == payload.mode:
        total = count_segments_by_book_and_mode(session, book_id, payload.mode)
        if total > 0:
            return {"message": "Đã ở mode này và audio đã sẵn sàng.", "needs_generation": False}
        else:
            # Ngoại lệ: Mode này đã được chọn trước đó nhưng lần đó bị lỗi (chưa sinh ra segment nào)
            background_tasks.add_task(run_switch_mode_processing, book_id, payload.mode)
            return {"message": "Đang gen lại...", "needs_generation": True}

    # TRƯỜNG HỢP 2: Switch sang một mode hoàn toàn mới
    # Đổi mode vào DB
    plan.mode = payload.mode
    session.add(plan)
    session.commit()

    # CHECK THÔNG MINH: Đếm tổng segment của mode mới này trên TOÀN BỘ sách
    total = count_segments_by_book_and_mode(session, book_id, payload.mode)
    needs_generation = (total == 0)

    if needs_generation:
        # Nếu chưa từng gen mode này -> Gọi background task xử lý
        background_tasks.add_task(run_switch_mode_processing, book_id, payload.mode)
        return {"message": "Đang sinh audio...", "needs_generation": True}
    
    # Nếu đã từng gen mode này trong quá khứ -> Trả về luôn
    return {"message": "Audio đã có sẵn.", "needs_generation": False}
```

**Phân tích Code:**
* API phản hồi cực nhanh vì nó không trực tiếp làm việc nặng. 
* Biến `needs_generation` là tín hiệu quan trọng cho Frontend biết có nên hiển thị màn hình Loading hay không.

### B. Code Background (`run_switch_mode_processing`)

Hàm này nhẹ hơn hàm gen gốc vì nó **bỏ qua RAG**. Text PDF là bất biến nên vector database cho phần Hỏi - Đáp đã có sẵn từ lần tạo `full` mode rồi, ta không làm lại.

```python
async def _process_switch_mode_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
) -> None:
    """Chỉ chạy luồng 2 (TTS), bỏ qua luồng 1 (RAG)"""
    async with sem: # Semaphore giới hạn chạy 5 chương cùng lúc
        try:
            # 1. Xoá rác DB cũ (nếu mode này trước đó gen bị lỗi giữa chừng)
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, new_mode)
                
            # 2. Sinh Audio TTS mới (Gọi lại hàm _thread_2_tts như ở mục 4)
            await _thread_2_tts(book_id, chapter_id, chapter_index, raw_text, new_mode)
            
        except Exception as e:
            logger.error(f"Lỗi: {e}")
            raise
```

---

## 6. Phân tích 3 Bug Chí Mạng đã được khắc phục

Trong quá trình dev, khi chạy test switch mode, hệ thống chỉ gen được 1 chương và lỗi hàng loạt. Tư duy debug và giải quyết như sau:

### ❌ Bug 1: Xung đột Storage Path (Lỗi 409 Duplicate)
* **Triệu chứng**: Khi chạy Pareto, chỉ 1-2 đoạn đầu tiên được tạo, sau đó báo lỗi Supabase 409 Duplicate.
* **Nguyên nhân**: Code cũ lưu file vào `/{book_id}/chap_1/part_1.mp3`. Khi chạy full nó đã tạo file này. Khi chạy pareto nó lại cố lưu vào **cùng tên file** đó. Supabase từ chối ghi đè.
* **Giải pháp**: Đổi path thành `/{book_id}/chap_1/full/part_1.mp3` và `/{book_id}/chap_1/pareto/part_1.mp3`. Tách biệt hoàn toàn thư mục. (Xem mục 4, đoạn gán `storage_path`).

### ❌ Bug 2: Supabase không cho ghi đè ngầm định
* **Triệu chứng**: Khi gen lỗi giữa chừng, xoá DB gen lại vẫn bị 409.
* **Nguyên nhân**: Hàm `delete_segments_by_chapter_and_mode` chỉ xoá DB, nhưng quên xoá file cứng trên Supabase Storage. Khi gen lại, nó vẫn chọc vào file cứng đó.
* **Giải pháp**: Thêm cờ `upsert: true` vào hàm `upload_file_to_supabase` để ép Supabase ghi đè.
```python
# Code đã sửa trong app/helper/upload2supabase.py
supabase.storage.from_(bucket).upload(
    path=storage_path,
    file=file_bytes,
    file_options={
        "content-type": content_type,
        "upsert": "true", # ← Thêm cờ này là fix dứt điểm Bug 2
    },
)
```

### ❌ Bug 3: Nhận diện sai trạng thái "Đã có sẵn"
* **Triệu chứng**: App thỉnh thoảng báo audio đã sẵn sàng nhưng thực chất mới gen được 1 chương.
* **Nguyên nhân**: Code cũ (`check_segments_exist_by_mode`) chỉ lấy **chương 1** ra hỏi "Mày có segment chưa?". Ví dụ chương 1 tình cờ thành công nhưng chương 2,3 chết sập nguồn, code vẫn kết luận luôn CẢ SÁCH đã có.
* **Giải pháp**: Viết lại hàm `count_segments_by_book_and_mode` để đếm tổng số segment của mode đó trên **toàn bộ các chương**. Nếu tổng số > 0 mới xác nhận là đã gen.
```python
# Code đã sửa trong app/crud/chapter_segment.py
def count_segments_by_book_and_mode(session: Session, book_id: uuid.UUID, mode: str) -> int:
    result = session.exec(
        select(func.count(ChapterSegment.id))
        .join(Chapter, ChapterSegment.chapter_id == Chapter.id)
        .where(Chapter.book_id == book_id)
        .where(ChapterSegment.mode == mode) # Bắt buộc phải join để đếm tổng các chương
    ).one()
    return result or 0
```

---

## 7. Tổng kết (Dành cho Frontend / App Flutter)

Là dev Front-End gọi các API này, bạn chỉ cần nhớ:

1. Khi gọi `/switch-mode` truyền json `{"mode": "pareto"}`.
2. Chú ý trường `needs_generation` trong JSON trả về.
   - Nếu `False`: Reload lại màn hình nghe sách ngay lập tức, file đã có sẵn ở DB rồi.
   - Nếu `True`: Đẩy user vào màn hình Loading, rồi dùng timer (3-5s/lần) gọi API `GET /books/{id}/details` để chờ trường `book_status` bằng `READY`.
3. Mọi dữ liệu trả về từ `/details` (như danh sách chapter, đoạn audio) sẽ **tự động filter** theo đúng cái `mode` mà user vừa switch. Bạn không cần tự filter bằng code Frontend.

Chúc bạn hiểu rõ hệ thống và tích hợp thành công! 🚀
