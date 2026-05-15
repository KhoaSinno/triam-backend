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

---

## 3. 🆕 Book Detail Chat Flow (Simplified - recommended for MVP)

Khi user **mở Book Detail và bắt đầu chat trực tiếp** (không qua Study Context), hệ thống cần đảm bảo:

- Có **1 auto-generated StudyContext** tự động cho `(user_id, book_id)` pair
- Có **1 canonical ChatThread** duy nhất dưới context đó
- Lịch sử chat **luôn liên tục** và **không bị phân mảnh**

### 3.1 Luồng cho FE (BookDetail Screen)

```
[1] User mở Book Detail
    ↓
[2] FE gọi: GET /threads/for-book/{book_id}
    ↓
[3] BE trả về: { context_id, thread_id, is_auto_generated: true }
    ↓
[4] FE lấy Token: GET /live-token/thread/{thread_id}
    ↓
[5] FE connect LiveKit với Token
    ↓
[6] Chat/Voice như bình thường
```

### 3.2 Endpoint chính: Get-or-Create Thread cho Book

**Endpoint:**

- **GET** `/threads/for-book/{book_id}

- `user_id` (UUID): User ID không cần gửi Param (hiện BE dùng MOCK_USER_ID, sau này khi auth ready sẽ lấy từ JWT token header khi call api)

**Response** (200 OK):

```json
{
  "context_id": "uuid-của-auto-context",
  "thread_id": "uuid-của-canonical-thread",
  "is_auto_generated": true
}
```

**Behavior:**

- **Lần đầu gọi**: BE tạo `DirectBookContext` + auto `StudyContext` + 1 `ChatThread` → trả về `thread_id`
- **Lần tiếp theo**: Tìm `DirectBookContext` đã tồn tại → return `thread_id` cũ
- **Idempotent & Race-safe**: Cả 2 request cùng lúc → return cùng `thread_id`, không tạo duplicate

**Lưu ý trong code:**

```dart
// Flutter pseudocode
Future<void> openBookDetail(String bookId) async {
  // Bước 1: Get-or-create thread
  final resp = await http.get(
    Uri.parse('$baseUrl/threads/for-book/$bookId'),
  );

  final data = jsonDecode(resp.body);
  final threadId = data['thread_id'];
  final isAutoGenerated = data['is_auto_generated']; // true → don't show create context UI

  // Bước 2: Get LiveKit token
  final tokenResp = await http.get(
    Uri.parse('$baseUrl/live-token/thread/$threadId'),
  );
  final tokenData = jsonDecode(tokenResp.body);
  final token = tokenData['token'];

  // Bước 3: Connect to LiveKit & start chatting
  final room = Room();
  await room.connect(livekitUrl, token);

  // Load history nếu muốn
  final historyResp = await http.get(
    Uri.parse('$baseUrl/threads/$threadId/messages'),
  );
  // ... render chat history ...
}
```

### 3.3 DB Design (for reference)

Backend tạo 3 entities:

- **DirectBookContext** (user_id, book_id) → PRIMARY KEY
  - `context_id` (FK → StudyContext)
  - `primary_thread_id` (FK → ChatThread)
- **StudyContext** (auto-generated=true)
  - Link tới Book qua `StudyContextDocumentLink`
  - Có 1 ChatThread duy nhất
- **ChatThread** → ChatMessage list

### 3.4 Comparison: Old Flow vs New Flow for Book Detail

| Aspect                  | Old Flow (Manual Study Context)                        | New Flow (Book Detail Auto)                 |
| ----------------------- | ------------------------------------------------------ | ------------------------------------------- |
| **User Experience**     | User phải tạo Context, gắn sách, tạo thread            | User click Book → chat ngay                 |
| **API Calls**           | POST /study-contexts → POST /documents → POST /threads | GET /threads/for-book/{book_id}             |
| **Context ownership**   | Manual context (is_auto_generated=false)               | Auto context (is_auto_generated=true)       |
| **Thread guarantee**    | Có thể có nhiều threads dưới 1 context                 | Chỉ 1 canonical thread cho cặp (user, book) |
| **History persistence** | User chọn thread để xem history                        | Auto load history cho direct book context   |
| **Use case**            | Multi-book study sessions, organized learning          | Quick chat on book detail page              |

---

## 4. ⚠️ Important Notes for FE Implementation

### 4.1 User ID Handling

- Hiện endpoint `/threads/for-book/{book_id}` dùng `MOCK_USER_ID` trong backend.
- **Sau khi có auth**: backend sẽ lấy `user_id` từ JWT token, FE không cần gửi `user_id` param nữa.
- Tạm thời, nếu muốn test với real user_id, có thể thêm query param `?user_id=...`.

### 4.2 Thread Persistence

- `thread_id` là **canonical** cho luồng chat của cặp (user, book).
- Nếu user đóng app và mở lại → FE phải gọi lại `GET /threads/for-book/{book_id}` để lấy `thread_id` → sẽ nhận cùng thread (không duplicate).
- Toàn bộ lịch sử chat được lưu và load tự động khi connect LiveKit.

### 4.3 Auto-Generated Context

- `is_auto_generated=true` → FE không nên show "Create new context" UI cho book detail.
- User vẫn có thể tạo **explicit** Study Context khác (từ Study tab) và add cùng book vào, nhưng đó là context riêng biệt.

### 4.4 Error Handling

- **404 Book not found**: BE sẽ fail nếu `book_id` không tồn tại → FE show "Book not found".
- **Concurrent request race**: Very unlikely, nhưng nếu xảy ra → BE sẽ handle bằng DB transaction. FE chỉ cần retry 1 lần nếu gặp error.

---

## 5. Summary: When to Use Which Flow?

| Scenario                                                                 | Use API                                                      |
| ------------------------------------------------------------------------ | ------------------------------------------------------------ |
| User đang ở **Book Detail page** → muốn chat ngay                        | `GET /threads/for-book/{book_id}`                            |
| User muốn tạo **Study Context** dành cho nhiều sách (Organized Learning) | `POST /study-contexts` → `POST /documents` → `POST /threads` |
| User muốn xem **lịch sử chat** của 1 thread                              | `GET /threads/{thread_id}/messages`                          |
| User muốn **kết nối LiveKit**                                            | `GET /live-token/thread/{thread_id}`                         |
