## 1. Thiết kế Giao diện Web Admin (UI Config)

Khi Admin chọn file và chuẩn bị tải lên, giao diện Web Admin sẽ cung cấp các tùy chọn cấu hình sau (thường hiển thị dưới dạng Radio Buttons và Checkbox):

1. **Chọn File**: Kéo thả hoặc chọn tệp `.pdf`, `.epub`, hoặc `.docx`.
2. **Chế độ xử lý dữ liệu (Processing Mode - Radio Buttons)**:
   - `( ) Full Mode`: Chỉ sinh bài học & âm thanh cho toàn bộ sách.
   - `( ) Pareto Mode`: Chỉ sinh bài học & âm thanh cho chế độ trọng tâm (25%).
   - `(*) Cả hai chế độ (Recommended)`: Sinh song song dữ liệu cho cả 2 chế độ. Người dùng clone về có thể chọn bất kỳ chế độ nào học được ngay.
3. **Quy chế công khai (Publish Type - Checkbox/Toggle)**:
   - `[x] Tự động công khai (Auto-Publish)`: Sách tự động xuất hiện trong thư viện dùng chung ngay khi hệ thống hoàn tất xử lý.
   - `[ ] Duyệt thủ công (Manual)`: Sách sẽ ở trạng thái ẩn (Draft/Ready riêng tư). Admin kiểm tra lại rồi bấm nút "Share" sau.

---

## 2. Chi tiết Luồng API dưới Backend cho từng cấu hình

### Kịch bản 1: Chỉ xử lý 1 chế độ (Full hoặc Pareto) + Tự động công khai

1. **Bước 1 (FE Web Admin)**: Gọi `POST /api/v1/upload` gửi file tài liệu.
   - _Backend_: Tạo bản ghi Book mới với `status="draft"` và `is_shared=False`. Trả về `book_id` và outline.
2. **Bước 2 (FE Web Admin)**: Gọi API Admin để kích hoạt tiến trình sinh:
   `POST /api/v1/admin/books/{book_id}/process?mode=full` (hoặc `pareto`)
   _Nếu Admin tích chọn **Auto-Publish**, API này sẽ truyền thêm cờ hoặc tự động cập nhật trường `is_shared = True` cho sách ngay lập tức._
   - _Backend_:
     - Lưu `book.is_shared = True` và chuyển `book.status = "processing"`.
     - Sinh các bài học trống (`learning_units`) cho chế độ học được chọn.
     - Tạo `ProcessingJob` và đẩy task bất đồng bộ vào Celery.
3. **Bước 3 (Celery Worker nền)**: Chạy sinh văn bản nói, sinh audio MP3 và sinh vector RAG. Khi hoàn thành, worker cập nhật `book.status = "ready"`.
4. **Kết quả**: Do sách đã thỏa mãn đồng thời: `is_shared = True` và `status = "ready"`, sách tự động hiển thị trong thư viện của tất cả các User.

---

### Kịch bản 2: Xử lý cả hai chế độ (Both modes) — _Trải nghiệm người dùng tốt nhất_

Để người dùng học được ngay cả 2 chế độ khi chọn sách từ thư viện, Admin nên kích hoạt xử lý cả hai.

1. **Bước 1 (FE Web Admin)**: Gọi `POST /api/v1/upload` gửi file. Nhận về `book_id`.
2. **Bước 2 (FE Web Admin)**: Gửi 2 request gọi API xử lý liên tiếp (hoặc gửi 1 request với payload là danh sách các mode):
   - Request 1: `POST /api/v1/admin/books/{book_id}/process?mode=full`
   - Request 2: `POST /api/v1/admin/books/{book_id}/process?mode=pareto`
3. **Bước 3 (Backend & Celery)**:
   - Tạo 2 `ProcessingJob` tương ứng cho 2 chế độ.
   - 2 Celery task chạy song song độc lập để sinh Audio & Vector cho cả `full` và `pareto`.
   - Cập nhật `book.is_shared = True` ngay lúc này (nếu tích chọn Auto-Publish).
4. **Kết quả**: Cả 2 luồng hoàn thành, sách gốc lưu trữ sẵn cả 2 bộ bài học & âm thanh. Khi User clone sách về, tất cả dữ liệu của cả 2 chế độ đều được nhân bản tức thì, học viên đổi chế độ học (`switch-mode`) không cần chờ xử lý lại nữa.

---

### Kịch bản 3: Duyệt thủ công (Không tích chọn Auto-Publish)

1. Luồng xử lý âm thanh/vector (Bước 1 và Bước 2) diễn ra tương tự như trên, nhưng trường `is_shared` của sách được giữ nguyên là `False`.
2. Sách xử lý xong, Admin vào danh sách sách trên Web Portal, nghe thử audio, kiểm tra outline.
3. Nếu hài lòng, Admin bấm nút **"Publish" / "Chia sẻ"**. Giao diện FE gọi API:
   `PATCH /api/v1/admin/books/{book_id}/share`
4. Hệ thống cập nhật `is_shared = True`. Sách chính thức công khai ra thư viện.
