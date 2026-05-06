# TRIAM Study Context & LiveKit Agent - Frontend API Contract

Tài liệu này cung cấp đặc tả API chính xác để đội ngũ Frontend (Flutter) tích hợp tính năng **Study Context** (Ngữ cảnh học tập) và gọi **AI Voice Agent** đa tài liệu thông qua LiveKit.

---

## 1. Quy trình Tích hợp (Frontend Workflow)

Để bắt đầu một cuộc hội thoại với AI tích hợp RAG (đọc hiểu sách), Frontend cần làm theo các bước sau:

1. **Khởi tạo Context**: Mỗi môn học hoặc mục tiêu học tập (ví dụ: "Ôn thi Triết học") là một `StudyContext`. Gọi API tạo Context.
2. **Chọn Tài Liệu**: User chọn những cuốn sách muốn AI đọc. Frontend gọi API gắn sách (`book_id`) vào cái Context vừa tạo.
3. **Tạo Cuộc Trò Chuyện**: Gọi API tạo một `ChatThread` (Luồng chat) nằm trong Context đó.
4. **Kết nối LiveKit**: Gọi API lấy **Token LiveKit** truyền vào `thread_id`. Frontend dùng Token này để kết nối WebSocket.
5. **Hiển thị Lịch sử**: Khi người dùng vào lại Thread cũ, gọi API lấy danh sách Message để hiển thị lên màn hình.

> **💡 Lưu Ý Quan Trọng:** Frontend **KHÔNG CẦN** phải gọi API lưu tin nhắn (Save Message). Ngay khi kết nối vào LiveKit, mọi câu nói của User và AI sẽ được Backend tự động lắng nghe và ghi thẳng vào Database theo thời gian thực.

---

## 2. Đặc tả API (Endpoints)

Base URL: `https://khoasinoo-tri-am-backend.hf.space/api/v1`

### 2.1 Quản lý Study Context (Ngữ cảnh học tập)

#### 🔹 Lấy danh sách Context của User

- **GET** `/study-contexts`
- **Response** (200 OK):
  ```json
  [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Ôn thi Triết học",
      "is_auto_generated": false,
      "created_at": "2026-05-05T02:00:00Z"
    }
  ]
  ```

#### 🔹 Lấy chi tiết Context

- **GET** `/study-contexts/{context_id}`
- **Response** (200 OK): Trả về Object StudyContext.

#### 🔹 Tạo mới Context

- **POST** `/study-contexts`
- **Body**:
  ```json
  {
    "title": "Ôn thi Triết học"
  }
  ```
- **Response** (200 OK): Trả về Object StudyContext vừa tạo.

#### 🔹 Đổi tên Context

- **PATCH** `/study-contexts/{context_id}`
- **Body**:
  ```json
  {
    "title": "Ôn thi Triết học (Sửa)"
  }
  ```
- **Response** (200 OK): Trả về Object StudyContext đã cập nhật.

#### 🔹 Xóa Context

- **DELETE** `/study-contexts/{context_id}`
- **Response** (200 OK): `{"message": "Study context deleted successfully"}`

---

### 2.2 Quản lý Tài Liệu (Books) trong Context

#### 🔹 Gắn Sách vào Context

- **POST** `/study-contexts/{context_id}/documents`
- **Body**:
  ```json
  {
    "book_id": "uuid-của-cuốn-sách"
  }
  ```
- **Response** (200 OK): Trả về chi tiết Link.

#### 🔹 Gỡ Sách khỏi Context

- **DELETE** `/study-contexts/{context_id}/documents/{book_id}`
- **Response** (200 OK): `{"message": "Context document deleted successfully"}`

---

### 2.3 Quản lý Luồng Chat (Chat Thread) & Lịch Sử (History)

#### 🔹 Lấy danh sách luồng chat trong Context

- **GET** `/study-contexts/{context_id}/threads`
- **Response** (200 OK):
  ```json
  [
    {
      "id": "thread-uuid-1",
      "context_id": "context-uuid",
      "title": "Hỏi đáp chương 1",
      "created_at": "2026-05-05T02:10:00Z"
    }
  ]
  ```

#### 🔹 Tạo một luồng chat mới

- **POST** `/study-contexts/{context_id}/threads`
- **Body**:
  ```json
  {
    "title": "Hỏi đáp chương 1"
  }
  ```
- **Response** (200 OK): Trả về Object ChatThread vừa tạo.

#### 🔹 Lấy toàn bộ lịch sử tin nhắn của một luồng chat

Dùng API này để render UI khung chat mỗi khi User mở lại Thread.

- **GET** `/threads/{thread_id}/messages`
- **Response** (200 OK):
  ```json
  [
    {
      "id": "uuid",
      "thread_id": "thread-uuid",
      "is_user": true,
      "text": "Tóm tắt chương 1 giúp tôi",
      "source": "livekit",
      "timestamp": "2026-05-05T02:11:00Z"
    },
    {
      "id": "uuid",
      "thread_id": "thread-uuid",
      "is_user": false,
      "text": "Chương 1 nói về...",
      "source": "livekit",
      "timestamp": "2026-05-05T02:11:15Z"
    }
  ]
  ```
  _(Lưu ý: `is_user=true` là tin nhắn của người dùng (nằm bên phải), `is_user=false` là tin nhắn của AI (nằm bên trái)._

---

### 2.4 Kết nối LiveKit Voice Agent

#### 🔹 Lấy LiveKit Token cho một Thread

- **GET** `/live-token/thread/{thread_id}`
- **Response** (200 OK):
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "room_name": "triam_c36851c1_3f3d0c"
  }
  ```
- **Hướng dẫn dùng ở Flutter:**
  Dùng biến `token` nhận được để kết nối vào LiveKit. Khi kết nối thành công, Backend sẽ tự động giật dây kích hoạt Worker Agent. Agent sẽ **tự động** load lịch sử trò chuyện của `thread_id` đó (Nhờ vậy Agent có trí nhớ) và giới hạn RAG đúng vào các `book_id` nằm trong Context!
