# Contract Backend Cho Study Context

## Mục đích

Frontend đang refactor `Study -> Ngữ cảnh` từ một danh sách mock thành một chức năng ngữ cảnh học tập thật.

Một ngữ cảnh học tập nên hoạt động giống một thread lịch sử chat:

- Một ngữ cảnh chứa một hoặc nhiều sách/tài liệu.
- Mỗi ngữ cảnh có metadata hội thoại: lần tương tác cuối, preview tin nhắn cuối, tổng số tin nhắn.
- Khi mở một ngữ cảnh, người dùng xem được lịch sử tương tác mà `AgentConversationView` đã ghi lại.
- Khi tiếp tục một ngữ cảnh, app khôi phục lịch sử hội thoại trước đó và tiếp tục dùng các tài liệu trong ngữ cảnh làm nguồn tham chiếu.

Tài liệu này mô tả model phía frontend và contract API backend cần có để nối chức năng này.

## Trạng thái frontend hiện tại

Đã làm ở frontend:

- Thêm model mới:
  - `StudyContext`
  - `StudyContextDocumentPreview`
- Thêm repository riêng:
  - `lib/features/study/data/study_context_repository.dart`
- Thêm card UI dùng chung:
  - `lib/features/study/presentation/widgets/study_context_list_item_card.dart`
- Cập nhật UI dùng `StudyContext`:
  - `Study -> Ngữ cảnh`
  - `Quản lý ngữ cảnh`

Chưa nối backend:

- Danh sách ngữ cảnh từ backend.
- Chi tiết ngữ cảnh từ backend.
- Lưu/đọc lịch sử hội thoại theo `context_id`.
- Tạo/sửa/xóa ngữ cảnh.
- Thêm/bớt tài liệu trong ngữ cảnh.

Hiện tại frontend vẫn dùng mock data từ `MockService.contexts`.

## Backend base URL hiện tại

Frontend đang đọc backend URL từ `.env`:

```env
BACKEND_URL=https://khoasinoo-tri-am-backend.hf.space
```

Code hiện tại đã dùng backend cho các nhóm API như books, upload, library, generate-plan và LiveKit.

Trước khi frontend nối thật, backend cần xác nhận đã có endpoint context/conversation nào chưa. Nếu chưa có, có thể dùng contract đề xuất bên dưới.

## Model dữ liệu frontend cần

### StudyContext

Ví dụ payload:

```json
{
  "id": "ctx-startup",
  "title": "Dự án Startup",
  "documents": [],
  "last_interaction_at": "2026-05-01T09:30:00Z",
  "last_message_preview": "Tóm tắt giúp tôi các giả định rủi ro trước khi pitching.",
  "message_count": 18,
  "created_at": "2026-04-13T08:00:00Z",
  "updated_at": "2026-05-01T09:30:00Z"
}
```

Field bắt buộc:

- `id`: id ổn định của ngữ cảnh.
- `title`: tên hiển thị.
- `documents`: danh sách preview tài liệu/sách gắn với ngữ cảnh.
- `created_at`: thời điểm tạo, dạng ISO datetime.
- `updated_at`: thời điểm cập nhật, dạng ISO datetime.

Field nên có:

- `last_interaction_at`: timestamp của tin nhắn user/agent gần nhất.
- `last_message_preview`: đoạn text ngắn hiển thị trên card ngữ cảnh.
- `message_count`: tổng số tin nhắn trong hội thoại của ngữ cảnh.

### StudyContextDocumentPreview

Ví dụ payload:

```json
{
  "id": "book-123",
  "title": "Clean Code",
  "cover_url": "https://example.com/cover.jpg",
  "format": "pdf"
}
```

Field bắt buộc:

- `id`: id sách/tài liệu.
- `title`: tên hiển thị.

Field tùy chọn:

- `cover_url`: URL ảnh bìa. Nếu rỗng, frontend sẽ tự render fallback cover dạng gradient.
- `format`: ví dụ `pdf`, `epub`, `web`, `audio`, hoặc string lowercase khác.

## API đề xuất

### Lấy danh sách ngữ cảnh

```http
GET /api/v1/study-contexts?user_id={userId}&limit=20&offset=0
```

Backend có thể trả raw array:

```json
[
  {
    "id": "ctx-startup",
    "title": "Dự án Startup",
    "documents": [
      {
        "id": "book-123",
        "title": "Clean Code",
        "cover_url": "",
        "format": "pdf"
      }
    ],
    "last_interaction_at": "2026-05-01T09:30:00Z",
    "last_message_preview": "Tóm tắt giúp tôi các giả định rủi ro trước khi pitching.",
    "message_count": 18,
    "created_at": "2026-04-13T08:00:00Z",
    "updated_at": "2026-05-01T09:30:00Z"
  }
]
```

Hoặc wrapped object:

```json
{
  "contexts": [],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

Frontend có thể hỗ trợ cả hai dạng. Tuy nhiên raw array đang đơn giản hơn và gần với behavior hiện tại của `/api/v1/books`.

### Lấy chi tiết một ngữ cảnh

```http
GET /api/v1/study-contexts/{contextId}?user_id={userId}
```

Response:

```json
{
  "id": "ctx-startup",
  "title": "Dự án Startup",
  "documents": [],
  "last_interaction_at": "2026-05-01T09:30:00Z",
  "last_message_preview": "Tóm tắt giúp tôi các giả định rủi ro trước khi pitching.",
  "message_count": 18,
  "created_at": "2026-04-13T08:00:00Z",
  "updated_at": "2026-05-01T09:30:00Z"
}
```

### Tạo ngữ cảnh

```http
POST /api/v1/study-contexts?user_id={userId}
Content-Type: application/json
```

Request:

```json
{
  "title": "Kiến trúc IoT",
  "document_ids": ["book-1", "book-2"]
}
```

Response: trả về `StudyContext` vừa tạo.

### Cập nhật metadata ngữ cảnh

```http
PATCH /api/v1/study-contexts/{contextId}?user_id={userId}
Content-Type: application/json
```

Request:

```json
{
  "title": "Kiến trúc IoT nâng cao"
}
```

Response: trả về `StudyContext` sau khi cập nhật.

### Xóa ngữ cảnh

```http
DELETE /api/v1/study-contexts/{contextId}?user_id={userId}
```

Response:

```json
{}
```

### Thêm tài liệu vào ngữ cảnh

```http
POST /api/v1/study-contexts/{contextId}/documents?user_id={userId}
Content-Type: application/json
```

Request:

```json
{
  "document_ids": ["book-1", "book-2"]
}
```

Response: trả về `StudyContext` sau khi cập nhật.

### Gỡ tài liệu khỏi ngữ cảnh

```http
DELETE /api/v1/study-contexts/{contextId}/documents/{documentId}?user_id={userId}
```

Response: trả về `StudyContext` sau khi cập nhật.

## API hội thoại

Frontend hiện đã có sẵn model `Conversation` và `ChatMessage`:

- `Conversation.contextId`
- `Conversation.messages`
- `Conversation.createdAt`
- `Conversation.updatedAt`
- `ChatMessage.timestamp`
- `ChatMessage.isUser`
- `ChatMessage.metadata`

Endpoint đề xuất để lấy lịch sử hội thoại:

```http
GET /api/v1/study-contexts/{contextId}/conversation?user_id={userId}
```

Response:

```json
{
  "id": "conv-ctx-startup",
  "context_id": "ctx-startup",
  "messages": [
    {
      "id": "msg-1",
      "text": "Tóm tắt tài liệu này giúp tôi.",
      "is_user": true,
      "timestamp": "2026-05-01T09:00:00Z",
      "metadata": {
        "source": "text"
      }
    },
    {
      "id": "msg-2",
      "text": "Đây là phần tóm tắt...",
      "is_user": false,
      "timestamp": "2026-05-01T09:00:08Z",
      "metadata": {
        "source": "livekit"
      }
    }
  ],
  "created_at": "2026-05-01T09:00:00Z",
  "updated_at": "2026-05-01T09:00:08Z"
}
```

Endpoint đề xuất để append message:

```http
POST /api/v1/study-contexts/{contextId}/conversation/messages?user_id={userId}
Content-Type: application/json
```

Request:

```json
{
  "text": "Tóm tắt tài liệu này giúp tôi.",
  "is_user": true,
  "timestamp": "2026-05-01T09:00:00Z",
  "metadata": {
    "source": "text"
  }
}
```

Response:

```json
{
  "id": "msg-1",
  "text": "Tóm tắt tài liệu này giúp tôi.",
  "is_user": true,
  "timestamp": "2026-05-01T09:00:00Z",
  "metadata": {
    "source": "text"
  }
}
```

Sau mỗi lần append message, backend nên cập nhật context cha:

- `last_interaction_at`
- `last_message_preview`
- `message_count`
- `updated_at`

## Tích hợp Agent và LiveKit

Luồng agent hiện tại đang dùng book id như ngữ cảnh LiveKit:

```http
/api/v1/live-token/{bookId}
```

Với ngữ cảnh nhiều tài liệu, backend nên chọn một trong các hướng sau:

1. Thêm route LiveKit riêng cho context:

```http
/api/v1/live-token/context/{contextId}
```

2. Giữ route hiện tại nhưng cho phép `bookId` nhận cả context id.

3. Thêm query parameter:

```http
/api/v1/live-token/{primaryBookId}?context_id={contextId}
```

Khuyến nghị: dùng phương án 1. Route riêng sẽ rõ ràng hơn, tránh trộn id sách đơn lẻ với id ngữ cảnh.

## Kỳ vọng RAG

Với một ngữ cảnh có nhiều tài liệu:

- Backend lấy toàn bộ document ids đang gắn với context.
- RAG search trên toàn bộ tài liệu trong context.
- Câu trả lời của agent nên bám theo các tài liệu đã chọn trong context.
- Nếu context không có tài liệu, backend có thể trả lỗi rõ ràng hoặc cho phép general chat tùy quyết định sản phẩm.

Ví dụ lỗi đề xuất khi context chưa có tài liệu:

```json
{
  "error": "context_has_no_documents",
  "message": "Ngữ cảnh này chưa có tài liệu nào."
}
```

## Quy ước đặt tên field

Frontend dùng camelCase trong Dart, nhưng JSON nên ưu tiên snake_case để nhất quán với backend hiện tại.

Backend nên dùng:

- `context_id`
- `created_at`
- `updated_at`
- `last_interaction_at`
- `last_message_preview`
- `message_count`
- `cover_url`
- `document_ids`
- `is_user`

## Những điểm backend cần xác nhận trước khi frontend nối thật

Backend vui lòng xác nhận:

- Hiện đã có endpoint context hoặc conversation chưa.
- Có OpenAPI docs ở `/docs`, `/openapi.json`, hoặc route khác không.
- Lịch sử hội thoại LiveKit/backend hiện có được persist chưa.
- Message chat có thể gắn `context_id` không.
- Uploaded books/documents hiện đã đủ field cho `StudyContextDocumentPreview` chưa.

Nếu chưa có endpoint, backend có thể implement theo API đề xuất trong tài liệu này và báo lại frontend route cuối cùng + response shape thực tế.

## Ghi chú triển khai frontend tiếp theo

Khi backend sẵn sàng, frontend sẽ cập nhật:

- `StudyContextRepository.getContexts()`
- provider chi tiết context
- provider conversation
- hook lưu message từ agent
- action tạo/sửa/xóa context
- action thêm/bớt tài liệu trong context

Nếu backend trả đúng shape ở trên, frontend không cần viết lại card UI mới.
