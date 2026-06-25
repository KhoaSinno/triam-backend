# Flutter Phase 15 Contract - Select Book from Shared Library & Direct Study Setup

Date: 2026-06-25  
Status: **Backend ready, Mobile FE integration contract (Suggestion Only)**  
Backend phase: `_docs_implemented/phase_15_select_book_from_library_implementation_guide.md`

> [!IMPORTANT]
> Tài liệu này đóng vai trò như một bản đặc tả giao tiếp API (API Contract) và các gợi ý thiết kế luồng UI/UX. Việc tổ chức mã nguồn, kiến trúc component, và quản lý trạng thái cụ thể trên ứng dụng Flutter sẽ do nhà phát triển Frontend tự quyết định và cài đặt sao cho phù hợp với dự án.

---

## 1. Mục Tiêu Của Phase 15 Cho Frontend (Flutter)

Trong phase này, hệ thống hỗ trợ tính năng **Thư viện sách hệ thống dùng chung (Shared Library)**. Thay vì mỗi người dùng đều phải tải lên file PDF/EPUB và đợi hệ thống chạy xử lý AI lâu (RAG vector, bóc tách mục lục, sinh giọng đọc), người dùng có thể:
1. Duyệt danh sách sách mẫu dùng chung được chia sẻ sẵn trên hệ thống.
2. Chọn một cuốn sách và cấu hình chế độ học (`FULL` hoặc `PARETO`) cùng với số lượng học phần/tuần (`pace`).
3. Nhấp chọn sách -> Hệ thống sẽ **nhân bản (clone) siêu tốc** cấu trúc sách, toàn bộ learning units và tệp âm thanh ở database của backend (trong khoảng ~100ms-200ms).
4. Tạo lịch trình học (`generate-plan`) và chuyển ngay tới màn hình học tập của sách đó để bắt đầu nghe/ôn tập tức thì, không cần qua bước hàng đợi `processing` của Celery.

---

## 2. Đặc Tả Giao Tiếp API (API Contract)

### 2.1 Lấy Danh Sách Sách Thư Viện Chung
*   **Endpoint**: `GET /api/v1/books/library`
*   **Headers**: `Authorization: Bearer <user_token>`
*   **Response**: `List[BookResponse]`
*   **Ví dụ Response**:
    ```json
    [
      {
        "id": "899367c3-8e3c-4971-8bc6-eb52c80aa123",
        "title": "C# programming example and solutions",
        "author": "Không rõ tác giả",
        "total_sections": 132,
        "total_units": 16,
        "status": "ready",
        "learning_status": null,
        "book_progress_percent": 0,
        "document_type": "pdf",
        "is_shared": true,
        "parent_shared_id": null,
        "has_full_mode": true,
        "has_pareto_mode": true,
        "created_at": "2026-06-25T16:39:00Z",
        "updated_at": "2026-06-25T16:39:00Z"
      }
    ]
    ```
*   **Lưu ý**: Chỉ những sách mẫu có `is_shared=true` và `status="ready"` mới được trả về trong danh sách này. Những sách mẫu chưa xử lý xong hoặc đang ở trạng thái xử lý lỗi (`processing`, `partial_ready`, `error`) sẽ **không hiển thị** cho người dùng thông thường.

### 2.2 Chọn Sách Từ Thư Viện (Clone Sách)
*   **Endpoint**: `POST /api/v1/books/{shared_book_id}/select`
*   **Headers**: `Authorization: Bearer <user_token>`
*   **Response**: `BookResponse` (Thông tin cuốn sách mới được tạo riêng cho người dùng hiện tại)
*   **Ví dụ Response**:
    ```json
    {
      "id": "e00a5a22-38d7-4638-aa21-bf9902621111",
      "title": "C# programming example and solutions",
      "author": "Không rõ tác giả",
      "total_sections": 132,
      "total_units": 16,
      "status": "ready",
      "learning_status": "not_started",
      "book_progress_percent": 0,
      "document_type": "pdf",
      "is_shared": false,
      "parent_shared_id": "899367c3-8e3c-4971-8bc6-eb52c80aa123",
      "has_full_mode": true,
      "has_pareto_mode": true,
      "created_at": "2026-06-25T23:15:00Z",
      "updated_at": "2026-06-25T23:15:00Z"
    }
    ```
*   **Lý giải kỹ thuật**: Backend thực hiện stored procedure nhân bản tất cả `sections`, `knowledge RAG chunks`, `learning units`, `segments` và liên kết file âm thanh. Do đó sách mới sẽ có ngay trạng thái `status="ready"`.

### 2.3 Tạo Kế Hoạch Học Tập Cho Sách Đã Chọn
*   **Endpoint**: `POST /api/v1/generate-plan`
*   **Headers**: `Authorization: Bearer <user_token>`
*   **Body JSON**:
    ```json
    {
      "book_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", // UUID của sách clone nhận được từ API select
      "mode": "full", // "full" hoặc "pareto"
      "pace": 2, // Số lượng learning unit muốn học trong mỗi buổi học
      "schedule_config": ["Mon", "Wed", "Fri"], // Các ngày học trong tuần (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
      "reminder_time": "20:00", // Thời gian nhắc học hàng ngày định dạng "HH:MM"
      "activate": true // Kích hoạt ngay lịch trình học
    }
    ```
*   **Response**: `ReadingPlanResponse` (Chi tiết kế hoạch học tập được kích hoạt ngay lập tức)

---

## 3. Gợi Ý Luồng Nghiệp Vụ & Thiết Kế UI/UX (Suggestions)

*Dưới đây là một số gợi ý xây dựng màn hình nhằm đảm bảo trải nghiệm người dùng mượt mà nhất. FE có thể linh động điều chỉnh bố cục.*

### 3.1 Bổ sung tab/lối vào "Thư viện chung" tại trang Tủ Sách (Library Screen)
*   Tại màn hình danh sách Tủ sách của người dùng, nên bổ sung một nút bấm hoặc Tab Toggle:
    *   **Sách của tôi (My Books)**: Danh sách sách cá nhân do user upload.
    *   **Thư viện chung (Public Library)**: Nơi gọi `GET /books/library` để duyệt các sách hệ thống mẫu có sẵn.

### 3.2 Giao diện Hộp thoại / Bottom Sheet cấu hình khi chọn sách
Khi người dùng chạm vào một cuốn sách trong Thư viện chung:
1.  Hiển thị một **Bottom Sheet** chi tiết sách:
    *   Tiêu đề, Tác giả, số chương, số học phần.
    *   Mô tả ngắn gọn về sách.
2.  Giao diện lựa chọn cấu hình trước khi học (Form):
    *   **Chế độ học (Study Mode)**: Cho phép chọn **FULL Mode** (học toàn bộ 100% nội dung) hoặc **PARETO Mode** (rút gọn, tập trung 20% cốt lõi).
        > [!IMPORTANT]
        > **Hướng dẫn xử lý Logic hiển thị chế độ học cho FE:**
        >
        > **A. Định nghĩa Model dữ liệu:**
        > Khi parse `BookResponse` từ JSON sang model Dart, FE cần map thêm hai trường boolean mới:
        > ```dart
        > class BookModel {
        >   final String id;
        >   final String title;
        >   final bool hasFullMode;
        >   final bool hasParetoMode;
        >   // ... các trường hiện có
        > 
        >   factory BookModel.fromJson(Map<String, dynamic> json) {
        >     return BookModel(
        >       id: json['id'],
        >       title: json['title'],
        >       hasFullMode: json['has_full_mode'] ?? false,
        >       hasParetoMode: json['has_pareto_mode'] ?? false,
        >       // ...
        >     );
        >   }
        > }
        > ```
        >
        > **B. Gợi ý Logic khởi tạo UI State:**
        > Khi mở Bottom Sheet, FE cần tự động xác định và đặt trạng thái mặc định của chế độ được chọn (`selectedMode`) dựa trên các cờ có sẵn để tránh chọn nhầm chế độ chưa được biên dịch:
        > ```dart
        > String? selectedMode;
        > 
        > void initializeDefaultMode(BookModel book) {
        >   if (book.hasFullMode && book.hasParetoMode) {
        >     selectedMode = 'full'; // Mặc định chọn FULL nếu có cả hai
        >   } else if (book.hasFullMode) {
        >     selectedMode = 'full'; // Chỉ có FULL
        >   } else if (book.hasParetoMode) {
        >     selectedMode = 'pareto'; // Chỉ có PARETO
        >   } else {
        >     selectedMode = null; // Tránh lỗi dữ liệu trống
        >   }
        > }
        > ```
        >
        > **C. Điều khiển Widget Lựa Chọn (Ví dụ Radio / ChoiceChip / Switch):**
        > FE cấu hình thuộc tính active/enable của UI component dựa trên hai trường tương ứng:
        > - **FULL Mode Button**: Có thể click chỉ khi `book.hasFullMode == true`.
        > - **PARETO Mode Button**: Có thể click chỉ khi `book.hasParetoMode == true`.
        > - Nếu cờ tương ứng bằng `false`, hiển thị dạng disable (màu xám nhạt, giảm opacity) và không phản hồi sự kiện click của người dùng.
    *   **Tần suất học (Pace)**: Chọn số lượng bài học (Learning Units) muốn học mỗi buổi (ví dụ: 1, 2, 3 bài/buổi).
    *   **Lịch học trong tuần (Schedule Days)**: Cho phép chọn các ngày muốn học trong tuần (Ví dụ: Thứ 2, 4, 6 -> gửi lên `["Mon", "Wed", "Fri"]`).
    *   **Giờ nhắc nhở học (Reminder Time)**: Tích hợp Time Picker để cấu hình thời gian nhận thông báo đẩy nhắc nhở (Ví dụ: 20:30 -> gửi lên `"20:30"`).
3.  **Nút CTA chính**: `Bắt đầu học ngay`
    *   Khi click, hiển thị Loading Indicator nhẹ nhàng.
    *   Thực hiện chuỗi API tuần tự (Sequence calls):
        ```dart
        // Bước 1: Clone sách mẫu về tài khoản user
        final clonedBook = await apiService.selectSharedBook(sharedBookId);
        
        // Bước 2: Tạo và kích hoạt ngay kế hoạch học tập cùng lịch/giờ nhắc nhở
        await apiService.generatePlan(
          bookId: clonedBook.id,
          mode: selectedMode, // full | pareto
          pace: selectedPace, // số unit/buổi
          scheduleConfig: selectedDays, // e.g. ["Mon", "Wed", "Fri"]
          reminderTime: selectedReminderTime, // e.g. "20:30"
          activate: true,
        );
        
        // Bước 3: Chuyển hướng về trang chi tiết học tập của clonedBook.id
        navigator.pushReplacementToBookDetail(clonedBook.id);
        ```

### 3.3 Tối ưu hóa Trạng thái Loading
Vì quá trình nhân bản dữ liệu được xử lý bằng stored function trong giao dịch SQL nguyên bản nên diễn ra cực kỳ nhanh (thường dưới 300ms). FE chỉ cần hiển thị một lớp phủ mờ loading (hoặc nút bấm chuyển sang trạng thái Disable + Spinner xoay) trong tích tắc để người dùng không bấm đúp, sau đó lập tức điều hướng chuyển trang.

---

## 4. Xử lý Lỗi & Tình Huống Đặc Biệt (Edge Cases)

1.  **Hủy/Xóa sách đã clone**:
    *   Khi người dùng xóa cuốn sách clone này ra khỏi tủ sách cá nhân, backend sẽ dọn dẹp các bản ghi DB tương ứng.
    *   Nhưng **Backend sẽ KHÔNG xóa các file âm thanh vật lý trên Cloud Storage** (vì nó thuộc về sách mẫu hệ thống gốc). FE không cần lo lắng về việc ảnh hưởng đến người dùng khác khi thực hiện xóa sách.
2.  **Sách mẫu chưa sẵn sàng**:
    *   Nếu một sách mẫu hệ thống chưa được xử lý xong hoặc gặp lỗi (trạng thái `processing`, `partial_ready`, hoặc `error`), backend sẽ tự động lọc và **không trả về** trong API `GET /api/v1/books/library`. Ứng dụng di động chỉ hiển thị các sách đã sẵn sàng học ở trạng thái `ready`.
