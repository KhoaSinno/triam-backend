# FE Spec — Preview sách mẫu trước khi clone

## Mục tiêu

Trước khi thêm sách mẫu vào thư viện cá nhân, user có thể xem cấu trúc sách, lộ trình học của từng mode và nghe một audio mẫu. Preview là chỉ đọc; không được tạo tiến độ, ReadingPlan hay bản clone.

## Endpoint

```http
GET /api/v1/books/library/{shared_book_id}/preview?mode=full
Authorization: Bearer <access-token>
```

`mode` nhận `full` hoặc `pareto`; mặc định là `full`.

Endpoint chỉ trả sách có `is_shared=true` và `status=ready`. Nếu sách không còn public, chưa sẵn sàng hoặc không tồn tại, API trả `404`.

## Chọn mode trước khi gọi API

Danh sách thư viện (`GET /api/v1/books/library`) đã có hai cờ:

| `has_full_mode` | `has_pareto_mode` | Mode FE phải gọi | UI mode |
| --- | --- | --- | --- |
| true | true | `full` khi mở lần đầu | Hiển thị selector Full/Pareto. |
| true | false | `full` | Không hiển thị selector. |
| false | true | `pareto` | Không hiển thị selector. |
| false | false | Không gọi preview audio | Hiển thị sách chưa có lộ trình nghe. |

Khi user đổi selector, gọi lại endpoint với mode mới. Không gọi `POST /books/{id}/switch-mode`: đó là API cho sách đã clone.

## Response contract

```json
{
  "book": {
    "id": "uuid",
    "title": "Tên sách",
    "author": "Tác giả",
    "total_sections": 12,
    "total_units": 8,
    "status": "ready",
    "ai_summary": {},
    "document_type": "pdf",
    "file_url": "...",
    "is_shared": true,
    "has_full_mode": true,
    "has_pareto_mode": true,
    "created_at": "2026-08-06T00:00:00Z",
    "updated_at": "2026-08-06T00:00:00Z"
  },
  "mode": "full",
  "available_modes": ["full", "pareto"],
  "total_sections": 12,
  "outline_tree": [
    {
      "id": "uuid",
      "title": "Chương 1",
      "level": 1,
      "path": "1",
      "page_start": 1,
      "page_end": 10,
      "children": []
    }
  ],
  "total_units": 8,
  "learning_outline": [
    {
      "id": "uuid",
      "title": "Nền tảng chương 1",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "full_chapter",
      "estimated_audio_seconds": 240,
      "planner_reason": null,
      "has_audio_sample": true
    }
  ],
  "audio_sample": {
    "id": "uuid",
    "title": "Nền tảng chương 1",
    "status": "ready",
    "unit_index": 0,
    "unit_type": "full_chapter",
    "estimated_audio_seconds": 240,
    "review_text": "",
    "review_audio_url": "",
    "segments": [
      {
        "id": 123,
        "segment_index": 0,
        "audio_url": "https://...",
        "text_content": "Nội dung đoạn nghe thử.",
        "duration_ms": 12000
      }
    ]
  }
}
```

`outline_tree` là mục lục sách gốc, chỉ có metadata cấu trúc; không chứa text tài liệu. `learning_outline` là toàn bộ unit của mode đang xem, cũng chỉ có metadata. `audio_sample` chỉ là một unit có audio đầu tiên; các unit khác không được coi là có thể phát.

## Quy tắc UI và hành vi

1. Hiển thị `outline_tree` dưới tiêu đề “Mục lục sách” để user hình dung bố cục; hỗ trợ tree/expand-collapse, thụt lề theo `level`.
2. Hiển thị `learning_outline` dưới tiêu đề “Lộ trình nghe thử”. Với Pareto, hiển thị thêm `planner_reason` khi có.
3. Chỉ hiện nút “Nghe thử” ở item có `has_audio_sample=true`; phát các `audio_sample.segments` theo `segment_index`.
4. Nếu `audio_sample=null`, vẫn hiển thị mục lục và lộ trình, nhưng hiển thị “Mode này hiện chưa có audio nghe thử”.
5. Trong preview, ẩn/vô hiệu hoá các action học thật: lưu tiến độ, hoàn thành unit, ôn tập, tạo ReadingPlan, chat theo ngữ cảnh sách.
6. CTA chính là “Thêm vào Sách đã lưu”, gọi `POST /api/v1/books/{shared_book_id}/select`. Sau khi clone thành công, chuyển sang màn hình chi tiết của bản clone và dùng các API sách cá nhân hiện có.
7. Không cache payload preview như learning journey/progress cá nhân. Có thể cache in-memory ngắn hạn theo `{shared_book_id, mode}` để đổi tab mượt hơn.

## Trạng thái lỗi

- `404`: rời màn hình và báo “Sách mẫu này không còn khả dụng.”
- Network/5xx: giữ UI cũ nếu có, hiện nút thử lại gọi đúng mode hiện tại.
- `learning_outline=[]`: hiển thị “Mode này chưa có lộ trình học.”
- `audio_sample=null`: không fallback sang mode khác tự động; giữ mode user đã chọn. Chỉ tự chọn mode thay thế lúc mở màn hình theo bảng ở trên.
