# Giai đoạn 14.12 - Spec Hợp đồng Context Agent (Agent Context Contract Spec)

Ngày: 2026-07-20

Phạm vi: Tài liệu hóa khoảng trống hợp đồng (contract gap) giữa Agent/Study Context đối với các context sách/tài liệu được tự động tạo (auto-generated). Spec này giả định không có bản vá backend nào được thực hiện trong nhiệm vụ frontend này; nó định nghĩa hợp đồng mà frontend sẵn sàng tiêu thụ (consume).

## Tóm tắt Vấn đề (Problem Summary)

Tri Am hiện có hai danh mục context:

- Manual study context (Context học tập thủ công): Không gian làm việc do người dùng tạo, có thể chứa nhiều tài liệu và nhiều luồng trò chuyện (chat thread).
- Auto-generated direct context (Context trực tiếp tự động tạo): Được tạo khi người dùng chọn một cuốn sách/tài liệu để trò chuyện với Agent.

Lỗi sản phẩm hiện tại không phải là một nhãn UI đơn lẻ. Đó là sự lệch pha về hợp đồng (contract mismatch) giữa "chọn một mục nội dung cho Agent" và "chọn một cặp context/thread cho Agent":

- Một context tự động tạo có thể tồn tại mà không có conversation/thread sử dụng được cho frontend, do đó việc chọn context đó khiến Agent không có `thread_id`.
- Các auto context mới mặc định tên là `New Book Chat`, khiến danh sách context không thể phân biệt được sách/tài liệu này với sách/tài liệu khác.
- Khi một cuốn sách được chọn cho LiveKit, UI có thể hiển thị tiêu đề context kỹ thuật thay vì hiển thị sách/tài liệu được chọn làm context đang hoạt động.
- Chưa có quy chuẩn đặt tên ngữ nghĩa (semantic naming contract) do backend sở hữu cho tiêu đề context/thread dựa trên nội dung được chọn hoặc lượt tương tác ý nghĩa đầu tiên của người dùng.
- Context thủ công và tự động hiển thị các khả năng quản lý (management affordances) khác nhau: context thủ công có thể thêm/xóa sách, đổi tên, xóa và quản lý luồng; context tự động ẩn nhiều chức năng đó mặc dù chúng đại diện cho cùng một đồ thị miền (domain graph).

## Trạng thái Frontend hiện tại (Current Frontend State)

Frontend đã có hầu hết hạ tầng cần thiết ngay khi backend công khai một hợp đồng ổn định:

| Khu vực FE | Khả năng hiện tại |
| --- | --- |
| Điểm vào sách Agent | `AgentNotifier.startBookSession()` giải quyết canonical book thread thông qua `AgentRepository.resolveBookThread()` trước LiveKit. |
| Đường dẫn token LiveKit | `AgentRepository.connectLiveKitThread*()` sử dụng `/api/v1/live-token/thread/{thread_id}`. |
| Repository knowledge context | `KnowledgeContextRepository` hỗ trợ danh sách/chi tiết context, xem trước tài liệu, thread, tin nhắn thread, tạo/cập nhật/xóa context, thêm/xóa tài liệu, tạo/cập nhật/xóa thread. |
| Cache local-first | `StudyContextLocalDataSource` lưu trữ context, xem trước tài liệu, thread, tin nhắn, các tác vụ xóa thread chờ xử lý và các hàng outbox cục bộ. |
| UI Context | `KnowledgeContextDetailSheet` hiển thị tài liệu và thread từ các provider và làm mới (invalidate) provider context/thread sau khi thay đổi dữ liệu. |
| UX Thread | Thao tác xóa thread đã có ngữ nghĩa stage/undo/commit thông qua `stageThreadDeletion`, `undoThreadDeletion` và `commitThreadDeletion`. |
| Chuyển tiếp lịch sử | `AgentLaunchRequest` có thể khởi chạy Agent từ một cặp `(contextId, threadId)` rõ ràng. |

Quy tắc frontend quan trọng từ Phase 10.7 vẫn áp dụng: frontend không được suy luận danh tính tài liệu từ tiêu đề như `New Book Chat`. Frontend chỉ được nạp dữ liệu (hydrate) bản xem trước tài liệu từ dữ liệu quan hệ rõ ràng: payload `documents` của context, `/study-contexts/{id}/documents`, `study_context_document_links` có thể đọc được, hoặc `direct_book_context` có thể đọc được.

## Hợp đồng Yêu cầu (Required Contract)

### 1. Context Sách Trực tiếp Phải Hoàn chỉnh Thread (Direct Book Context Must Be Thread-Complete)

Endpoint:

```text
GET /api/v1/threads/for-book/{book_id}
```

Bất biến bắt buộc (Required invariant):

- Nếu cuốn sách thuộc về người dùng đã xác thực và phản hồi là `200`, phản hồi phải luôn bao gồm cả `context_id` hợp lệ và `thread_id` hợp lệ.
- Nếu một direct context tồn tại nhưng thiếu thread chính, backend nên sửa chữa hoặc tạo lại thread chính trước khi trả về.
- Frontend không bao giờ được nhận phản hồi direct-book thành công mà lại phải tự đoán thread nào cần sử dụng.

Cấu trúc phản hồi tối thiểu (Minimum response shape):

```json
{
  "context_id": "uuid",
  "thread_id": "uuid",
  "is_auto_generated": true
}
```

Cấu trúc phản hồi ưu tiên (Preferred response shape):

```json
{
  "context_id": "uuid",
  "thread_id": "uuid",
  "is_auto_generated": true,
  "book_id": "uuid",
  "book_title": "Of Mice and Men",
  "context_title": "Of Mice and Men",
  "thread_title": "Of Mice and Men"
}
```

### 2. Danh sách/Chi tiết Context Phải Hiển thị Quan hệ Nội dung (Context List/Detail Must Expose Content Relation)

Endpoints:

```text
GET /api/v1/study-contexts
GET /api/v1/study-contexts/{context_id}
GET /api/v1/study-contexts/{context_id}/documents
```

Bất biến bắt buộc:

- Mỗi context cần hiển thị tài liệu phải công khai dữ liệu quan hệ tài liệu rõ ràng.
- Auto direct-book context phải hiển thị cuốn sách/tài liệu duy nhất được chọn thông qua một trong các cách:
  - `documents` trong payload danh sách/chi tiết context;
  - `document_count` cộng với endpoint `/documents` hoạt động;
  - `study_context_document_links` hoặc `direct_book_context` có thể đọc được thông qua truy cập dữ liệu trong phạm vi người dùng.

Mục xem trước tài liệu ưu tiên (Preferred document preview item):

```json
{
  "id": "book-id",
  "title": "Of Mice and Men",
  "cover_url": "https://...",
  "format": "pdf"
}
```

### 3. Việc Đặt tên Phải Mang Tính Ngữ nghĩa (Naming Must Be Semantic)

Giá trị mặc định do Backend sở hữu:

- Tiêu đề direct-book auto context nên mặc định lấy theo tiêu đề sách/tài liệu được chọn, không phải `New Book Chat`.
- Tiêu đề thread chính cũng nên mặc định lấy theo tiêu đề sách/tài liệu được chọn trừ khi một tiêu đề thread có tính ngữ nghĩa tốt hơn đã được tạo.
- `New Book Chat` nên được đối xử như một phương án dự phòng cũ/nội bộ (legacy/internal fallback), không phải là văn bản hiển thị sản phẩm (product copy).

Quy tắc đặt tên ngữ nghĩa trong tương lai:

- Sau khi có đủ tín hiệu hội thoại, backend có thể đổi tên thread từ tiêu đề nội dung sang một tóm tắt lượt hội thoại mang tính ngữ nghĩa.
- Tên được tạo phải ổn định và rõ ràng trong payload của thread; frontend chỉ nên hiển thị tiêu đề mà nó nhận được.
- Frontend không nên tự tổng hợp tên ngữ nghĩa từ nhật ký tin nhắn vì điều đó tạo ra sự bất nhất giữa các thiết bị.

### 4. Khả năng của Context Thủ công và Tự động Phải Được Thiết kế Rõ ràng (Manual And Auto Context Capabilities Must Be Deliberate)

Context thủ công (Manual context):

- Có thể chứa nhiều tài liệu.
- Có thể chứa nhiều thread.
- Người dùng có thể thêm/xóa tài liệu, đổi tên/xóa context, đổi tên/xóa thread.

Context sách trực tiếp tự động (Auto direct-book context):

- Đại diện cho một tài liệu/sách chuẩn duy nhất được chọn.
- Phải có một thread chính.
- Có thể ẩn "thêm tài liệu phụ" và "tạo thread khác" nếu sản phẩm muốn chế độ direct-book giữ nguyên quan hệ 1-1.
- Vẫn nên hiển thị các hành động nhất quán khi hợp đồng cho phép: mở thread, đổi tên tiêu đề hiển thị nếu backend hỗ trợ, xóa direct context nếu backend hỗ trợ dọn dẹp `direct_book_context`, hàng context, liên kết tài liệu và thread chính.

Hiển thị hành động phía Frontend nên được điều khiển bởi metadata khả năng (capability metadata), không chỉ dựa vào `is_auto_generated`.

Payload capability ưu tiên:

```json
{
  "capabilities": {
    "can_add_documents": false,
    "can_remove_documents": false,
    "can_create_threads": false,
    "can_rename_context": true,
    "can_delete_context": true,
    "can_rename_threads": true,
    "can_delete_threads": true
  }
}
```

## Kế hoạch Kết nối Frontend (Frontend Connection Plan)

Không cần bản vá backend nào trong nhiệm vụ này. Khi backend cung cấp hợp đồng ưu tiên, các thay đổi FE sẽ nhỏ và mang tính cục bộ:

1. Mở rộng `AgentBookThread.fromMap()` để parse các trường tùy chọn `book_id`, `book_title`, `context_title` và `thread_title`.
2. Trong `AgentNotifier.startBookSession()`, tiếp tục sử dụng `threads/for-book/{book_id}`, nhưng hiển thị `book_title/context_title` thay vì quay về tiêu đề context kỹ thuật.
3. Trong quá trình nạp dữ liệu danh sách/chi tiết context, dựa vào `documents` hoặc `/documents` để hiển thị bìa/tiêu đề sách đã chọn cho các auto context.
4. Thay thế các kiểm tra UI ẩn hành động chỉ bằng `isAutoGenerated` bằng các cờ capability của backend khi các cờ này tồn tại.
5. Giữ nguyên luồng context thủ công: tạo context, thêm tài liệu, tạo thread, mở cặp `(contextId, threadId)` rõ ràng.

## Tiêu chí Nghiệm thu (Acceptance Criteria)

- Chọn bất kỳ sách/tài liệu nào cho Agent luôn trả về `selectedContextId` và `selectedThreadId` hợp lệ.
- Bắt đầu Live và trò chuyện văn bản chỉ sử dụng `/live-token/thread/{thread_id}` sau khi canonical thread đã được xác định.
- Nhãn context đang hoạt động hiển thị tiêu đề sách/tài liệu được chọn, không phải `New Book Chat`.
- Danh sách context có thể phân biệt các auto context theo tiêu đề/bìa tài liệu thực tế.
- Mở một auto context không bao giờ rơi vào trạng thái hiển thị "chọn một thread" trong khi FE không thể tạo được thread nào.
- Các hành động đối với context thủ công và tự động nhất quán với các capability rõ ràng từ backend.
- Xóa một context/thread/tài liệu tạo ra cùng một hành vi vô hiệu hóa (invalidation) local-first và xóa chờ xử lý (pending-delete) trên mọi giao diện.

## Nằm ngoài Phạm vi (Out Of Scope)

- Thực thi việc dọn dẹp/sửa chữa dữ liệu cũ (legacy rows) ở backend.
- Thêm dịch vụ đặt tên bằng LLM.
- Thay đổi vòng đời của phòng LiveKit.
- Suy luận quan hệ tài liệu từ tiêu đề context.
- Thay thế tầng repository Drift local-first hiện tại.


