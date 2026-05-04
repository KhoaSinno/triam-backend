# Báo Cáo Nghiên Cứu & Hợp Đồng Kiến Trúc: Study Context (Mô hình 3 Lớp)

## 1. Vấn Đề Cốt Lõi (User Pains) & Tầm Nhìn Sản Phẩm

Hệ thống hiện tại có sự liên kết 1-1 giữa Sách (Book) -> Kế Hoạch Đọc (Plan) -> Nội Dung Audio (Chunks). Đây là **Core Engine** của việc sinh nội dung, tuyệt đối không được phá vỡ.
Tuy nhiên, nếu hội thoại AI cũng bị giới hạn trong 1 Sách, chúng ta sẽ gặp phải các "Nỗi Đau" (Pain Points):
- **Knowledge Silos (Cô lập tri thức):** User không thể hỏi AI đối chiếu kiến thức giữa Sách A và Slide B.
- **Context Switching:** Nếu muốn dùng chung 1 tập tài liệu cho nhiều mục đích thảo luận khác nhau (VD: Hôm nay luyện Speaking, ngày mai hỏi đáp ngữ pháp), user không có chỗ để lưu trữ các luồng hội thoại độc lập.
- **Thiếu tính định hướng trong ôn tập:** Quá trình Spaced Repetition bị rời rạc theo từng cuốn sách, thay vì ôn tập theo một "Chiến dịch" hay "Chủ đề".

**Giải pháp:** Nâng tầm `Study Context` thành một **"Chiến Dịch Học Tập" / "Không Gian Làm Việc"**. Nó đóng vai trò là một Lớp Tổng Hợp (Aggregator) và Lớp Hội Thoại (Chat Wrapper) bao bọc bên ngoài các tài liệu hiện có.

---

## 2. Kiến Trúc 3 Lớp (Industry Standard)

Để giải quyết triệt để vấn đề mà không làm hỏng Core Engine, hệ thống đã thống nhất sử dụng **Kiến trúc 3 Lớp Tách Biệt** (tương tự ChatGPT Projects / NotebookLM):

1. **Lớp Nguồn Dữ Liệu (The Data):** Các bảng `Book`, `Plan` giữ nguyên. Chịu trách nhiệm sinh Audio/Text.
2. **Lớp Không Gian Học Tập (Study Context):** Một "Thư mục" gom nhóm nhiều sách/tài liệu lại với nhau. Chỉ định nghĩa ranh giới tìm kiếm (RAG Scope). Không lưu trữ tin nhắn.
3. **Lớp Phiên Hội Thoại (Chat Thread):** Nơi lưu trữ thực tế của các luồng chat. Một `Study Context` có thể tạo ra vô hạn `Chat Thread`.

### Sự kết hợp mượt mà vào UI/UX:
- **Luồng Tự Động (Nghe sách đơn lẻ):** Khi user mở 1 Sách để nghe và bấm Chat, hệ thống ngầm định sinh ra 1 `Study Context` (chứa 1 sách đó) và 1 `Chat Thread` mặc định. Trải nghiệm mượt mà, user không cần setup.
- **Luồng Không Gian Học Tập (Góc ôn thi):** User chủ động tạo Context "Ôn thi IELTS", add 5 cuốn sách. Giao diện cung cấp cho user danh sách các `Chat Thread` để họ tùy ý tách luồng thảo luận (Ví dụ: Thread "Luyện Speaking", Thread "Hỏi đáp Reading").

---

## 3. Thiết Kế Database (SQLModel)

Cần tạo/cập nhật các bảng sau:

```python
# 1. Bảng Không Gian Học (StudyContext)
class StudyContext(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    title: str # VD: "Ôn thi IELTS" hoặc "Thảo luận Sách A"
    is_auto_generated: bool = Field(default=False) # True nếu do hệ thống tự tạo cho luồng sách đơn
    created_at: datetime
    updated_at: datetime

# 2. Bảng Quan Hệ (Context - Document)
class StudyContextDocumentLink(SQLModel, table=True):
    context_id: str = Field(foreign_key="studycontext.id", primary_key=True)
    book_id: str = Field(foreign_key="books.id", primary_key=True)

# 3. Bảng Phiên Hội Thoại (ChatThread)
class ChatThread(SQLModel, table=True):
    id: str = Field(primary_key=True)
    context_id: str = Field(foreign_key="studycontext.id", index=True)
    title: str # VD: "Luyện Speaking Thứ 2"
    created_at: datetime
    updated_at: datetime

# 4. Bảng Tin Nhắn (ChatMessage)
class ChatMessage(SQLModel, table=True):
    id: str = Field(primary_key=True)
    thread_id: str = Field(foreign_key="chatthread.id", index=True) # Gắn liền với Thread, không phải Context
    is_user: bool
    text: str
    source: str # "livekit" or "text"
    timestamp: datetime
```

---

## 4. Kế Hoạch Implement API & RAG Pipeline

### Bước 1: REST API (CRUD cho Context & Thread)

Tạo `app/api/v1/endpoints/study_context.py` implement các endpoints sau:

**Quản lý Context:**
- `GET /study-contexts` (Lấy danh sách Workspace)
- `POST /study-contexts` (Tạo Workspace mới)
- `GET /study-contexts/{id}` (Lấy chi tiết Workspace và các Book bên trong)
- `POST /study-contexts/{id}/documents` (Thêm/xóa sách khỏi Workspace)

**Quản lý Thread (Nằm trong Context):**
- `GET /study-contexts/{id}/threads` (Lấy danh sách các luồng chat của một Workspace)
- `POST /study-contexts/{id}/threads` (Tạo luồng chat mới)
- `GET /threads/{thread_id}/messages` (Lấy lịch sử tin nhắn của một luồng)

### Bước 2: Cập Nhật RAG Pipeline (Supabase)

Khi truy vấn RAG cho một Thread:
1. Lấy `context_id` từ `thread_id`.
2. Truy vấn Database lấy ra mảng `document_ids` (chứa các `book_id` thuộc Context đó).
3. Sử dụng mảng này làm filter cho Supabase Vector: `query(book_id IN [doc1, doc2, ...])`.

### Bước 3: Tích Hợp LiveKit Agent

- **Cấp Token API:** Frontend gọi endpoint `/live-token/thread/{thread_id}`.
- **Job Metadata:** Backend đóng gói `thread_id`, `context_id`, và mảng `document_ids` vào `Job Metadata` truyền cho LiveKit.
- **Khởi động Agent:** Agent đọc `thread_id` để tải đúng lịch sử hội thoại (nạp trí nhớ). Đọc `document_ids` để giới hạn phạm vi RAG.
- **Lưu Tin Nhắn:** Các sự kiện `user_speech_committed` và `agent_speech_committed` sẽ được ghi thẳng vào bảng `ChatMessage` với `thread_id` tương ứng.

---

## 5. Tổng Kết

Việc thống nhất Kiến trúc 3 Lớp này giải quyết hoàn hảo bài toán mở rộng trong tương lai. Nó không làm xáo trộn Core Engine sinh Audio hiện tại của ứng dụng, đồng thời mở khóa tính năng "Gia sư toàn năng" (Cross-document RAG) và "Quản lý chiến dịch học tập" - một "Killer Feature" thực sự cho sản phẩm.
