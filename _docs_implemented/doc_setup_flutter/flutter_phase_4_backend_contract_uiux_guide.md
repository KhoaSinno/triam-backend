# TRIAM Flutter Implementation Guide - Phase 4 Backend Contract And UI/UX

Ngày cập nhật: 2026-05-26  
Audience: Flutter team, backend maintainer, capstone reviewer  
Backend scope: Phase 1 -> Phase 4.2  
Mục tiêu: Một tài liệu FE contract mới, thay thế cách đọc rời rạc phase 1-3 và bổ sung learning loop/notification Phase 4.2.

Lưu ý cho Flutter team:

- FE đã có UI và cấu trúc project cơ bản, tài liệu này không yêu cầu đổi folder structure.
- Trọng tâm là map UI hiện tại vào đúng backend state, API, progress flow và business rule.
- Flutter không tự đoán trạng thái xử lý sách, tiến độ học, reminder hoặc review. Backend là source of truth.

## 0. Trạng Thái Backend Hiện Tại

Backend hiện đã có các nhóm chức năng:

- Upload PDF/EPUB/DOCX có cấu trúc.
- Generate reading plan.
- Celery/Redis background job.
- Polling progress bằng `processing_jobs`.
- Partial-ready unlock.
- Audiobook playback theo chapter/segment.
- Switch mode `full` / `pareto`.
- Study Context và thread chat.
- LiveKit realtime voice/text agent.
- In-app notification.
- Learning progress theo chapter/segment.
- Spaced review sau khi user hoàn thành chapter.
- Review complete/skip.

Phase 4.2 đã test bằng book thật:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

Kết quả backend real-book test:

```text
Book READY.
Job READY 100%.
3/3 chapters READY.
99 audio segments.
35 knowledge chunks.
first_playable notification sent.
book_ready notification sent.
spaced_review_due notification sent.
review complete API completed.
```

Log backend:

```text
logs/phase4_2_real_book_full_flow.json
logs/phase4_2_real_book_learning_flow.json
```

## 1. Auth Contract - Rất Quan Trọng

Product decision:

```text
Auth flow chính: Supabase email/password.
Auth flow phụ nếu FE làm kịp: Google OAuth qua Supabase.
Không dùng custom auth trong Phase 4.
```

Supabase hỗ trợ cả email/password và OAuth provider như Google. FE dùng Supabase SDK để login, lấy session/access token, rồi gửi token đó cho backend.

### 1.1 Trạng thái code hiện tại

Backend đã bật auth dependency cho các API user-owned:

```text
app/api/dependencies/auth.py
```

Hàm chính:

```python
get_current_user(...)
```

Hàm này:

- đọc `Authorization: Bearer <access_token>`;
- gọi Supabase Auth để verify token;
- trả về `UserTokenPayload`;
- `UserTokenPayload.sub` chính là `user_id`.

Backend cũng có alias ngắn:

```python
CurrentUser = Annotated[UserTokenPayload, Depends(get_current_user)]
```

Các router user-owned đã dùng `CurrentUser` thay cho `MOCK_USER_ID`.

### 1.2 BE Auth Pattern

Pattern backend hiện tại:

```python
from app.api.dependencies.auth import CurrentUser

@router.get("/books")
def read_all_books(
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
):
    return list_books(session, current_user.sub)
```

Nguyên tắc:

- Router lấy `current_user`.
- Router truyền `current_user.sub` xuống service.
- Service/repository query theo `user_id`.
- Service không tự lấy mock user.
- LiveKit token theo thread/book cũng kiểm tra ownership trước khi cấp token.

Deploy/migration note:

```text
Các sách/context/job/notification tạo trước auth refactor có thể đang thuộc mock user cũ.
Sau khi deploy auth thật, user thật sẽ không thấy dữ liệu mock đó.
```

Nếu cần giữ dữ liệu demo cũ, BE phải migrate `user_id` từ mock user sang Supabase user thật. Nếu không cần giữ, có thể reset data demo và test lại bằng account thật.

### 1.3 FE phải gửi auth thế nào?

Vì BE đã bật auth thật, mọi API user-data cần header:

```http
Authorization: Bearer <access_token>
```

Không gửi `user_id` trong body.

Access token là token login của Supabase/Auth provider.

Flutter nên có `AuthInterceptor`:

```dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = authStore.accessToken;
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
}
```

### 1.4 API nào không cần auth?

Có thể public:

```text
GET /
GET /api/v1/health
GET /api/v1/health/background
```

Còn lại nên cần auth:

```text
books
upload
generate-plan
jobs
learning-progress
notifications
reviews
study-contexts
threads
live-token/{book_id}
live-token/thread
```

`/live-token/{book_id}` vẫn là legacy/debug cho book-only session, nhưng cũng cần auth và kiểm tra book thuộc user hiện tại.

### 1.5 UI Auth Yêu Cầu

FE cần có tối thiểu:

- login bằng email/password;
- signup bằng email/password;
- logout;
- session restore khi mở app;
- expired session handling;
- Google OAuth nếu còn thời gian.

Sau login thành công:

- lưu session theo chuẩn Supabase SDK;
- attach `Authorization: Bearer <access_token>` vào mọi API user-owned;
- không gửi `user_id` trong body/query;
- nếu API trả `401`, thử refresh session hoặc đưa user về màn login.

## 2. Base URL

Production hiện tại:

```text
https://khoasinoo-tri-am-backend.hf.space/api/v1
```

Flutter nên cấu hình theo environment:

```dart
enum AppEnvironment { local, staging, production }

const localApiBaseUrl = 'http://127.0.0.1:8000/api/v1';
const productionApiBaseUrl = 'https://khoasinoo-tri-am-backend.hf.space/api/v1';
```

Không hard-code URL ở từng repository.

## 3. Global Error Contract

Domain error thường có dạng:

```json
{
  "detail": "Human-readable message"
}
```

FastAPI validation error có thể có dạng:

```json
{
  "detail": [
    {
      "loc": ["body", "mode"],
      "msg": "...",
      "type": "..."
    }
  ]
}
```

FE cần parser chung:

```dart
String parseApiError(Object error) {
  // 1. Nếu response.detail là String -> show.
  // 2. Nếu response.detail là List -> show msg đầu tiên.
  // 3. Nếu không parse được -> show fallback an toàn.
}
```

HTTP status cần xử lý:

| Code | Ý nghĩa | UI |
| --- | --- | --- |
| 400 | input sai, file quá lớn, loại file không hỗ trợ | hướng dẫn sửa |
| 401 | access token thiếu/hết hạn | logout hoặc refresh token |
| 403 | không có quyền | báo không có quyền |
| 404 | không tìm thấy resource | refresh state |
| 409 | state conflict, ví dụ book không còn draft | refresh book/job |
| 422 | tài liệu không hợp lệ về mặt cấu trúc | hướng dẫn file có outline/TOC/Heading |
| 500 | lỗi hệ thống | retry/support |
| 502 | lỗi external service | thử lại sau |

## 4. Canonical Enums

### 4.1 Book Status

Backend JSON:

```text
draft
processing
partial_ready
ready
error
```

Flutter enum:

```dart
enum BookStatus {
  draft,
  processing,
  partialReady,
  ready,
  error,
}
```

### 4.2 Processing Job Status

Backend JSON:

```text
queued
processing
partial_ready
ready
error
cancelled
```

Flutter enum:

```dart
enum ProcessingJobStatus {
  queued,
  processing,
  partialReady,
  ready,
  error,
  cancelled,
}
```

### 4.3 Plan Mode

Backend JSON:

```text
full
pareto
```

UX copy đề xuất:

| Mode | Label | Mô tả |
| --- | --- | --- |
| `full` | Đầy đủ | Nghe kỹ, giữ mạch nội dung chính |
| `pareto` | Tinh gọn | Nghe nhanh các ý cốt lõi, khái niệm, quy trình, kiến thức quan trọng |

### 4.4 Learning Progress Status

Backend JSON:

```text
not_started
in_progress
completed
```

### 4.5 Notification Type

Backend JSON:

```text
plan_reminder
content_ready
spaced_review_due
```

## 5. FE Mapping Principles

FE đã có cấu trúc sẵn, vì vậy không cần đổi folder. Chỉ cần đảm bảo các nguyên tắc sau trong code hiện tại:

- Không để widget gọi HTTP trực tiếp nếu project đã có repository/service layer.
- Có một nơi chung để attach `Authorization` header.
- Có một parser lỗi API chung để xử lý `detail` dạng string và list.
- UI render theo enum/status backend trả về, không hard-code suy đoán.
- Polling job/progress phải dừng khi gặp terminal status: `ready`, `error`, `cancelled`.
- Audio player không reset khi book details refresh.
- Notification/review/progress không tạo local fake state nếu backend chưa xác nhận.
- Những API ghi tiến độ audio phải debounce/throttle ở FE để tránh spam backend.

Tư duy chính:

```text
Backend state -> FE state model -> UI render.
Không để UI tự tạo business rule riêng.
```

## 6. Upload Document

### 6.1 API

```http
POST /api/v1/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file=<PDF|EPUB|DOCX>
```

Response:

```json
{
  "book_id": "uuid",
  "total_chapters": 3,
  "document_type": "pdf",
  "outline": [
    {
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "page_start": 1
    }
  ]
}
```

`page_start` có thể `null` với EPUB/DOCX.

### 6.2 Rule Tài Liệu

Backend chỉ support tài liệu có cấu trúc:

| Type | Cần có |
| --- | --- |
| PDF | hidden outline/bookmarks |
| EPUB | TOC/navigation |
| DOCX | Heading styles |

Không support:

- scanned PDF;
- OCR tự động;
- regex detect chapter;
- auto split chương bằng số trang/token.

UI copy đề xuất khi chọn file:

```text
TRIAM cần tài liệu có cấu trúc chương rõ ràng.
PDF cần bookmark/outline, EPUB cần mục lục, DOCX cần Heading.
```

### 6.3 Upload Screen UX

Flow:

```text
Pick file
-> validate extension/size local
-> upload
-> show extracted outline
-> user confirm
-> go to reading plan setup
```

Không đi thẳng sang player sau upload. Upload chỉ tạo `Book DRAFT`.

### 6.4 Upload Timeout Rule

Backend phải đọc file và kiểm tra cấu trúc chương trước khi trả response upload. Vì vậy DOCX/PDF lớn có nhiều chương có thể mất vài chục giây.

FE không nên để timeout upload quá ngắn như 45 giây. Khuyến nghị:

```text
upload timeout: 120-180 giây
generate-plan/job polling: dùng polling endpoint, không giữ request dài
```

Nếu upload bị timeout ở FE nhưng user nghi ngờ backend đã nhận file, FE nên refresh Library trước khi yêu cầu upload lại. Lý do: request có thể đã hoàn thành ở backend nhưng response không về kịp app.

## 7. Generate Plan

### 7.1 API

```http
POST /api/v1/generate-plan
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "book_id": "uuid",
  "mode": "full",
  "pace": 1,
  "schedule_config": ["Mon", "Wed", "Fri"]
}
```

Response:

```json
{
  "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
  "book_id": "uuid",
  "job_id": "uuid",
  "mode": "full",
  "status": "queued",
  "progress_percent": 0
}
```

### 7.2 Schedule Guardrails

Backend Phase 4.2 có rule:

- không trùng active schedule slot;
- giới hạn số sách đang học active;
- slot dựa trên `weekday + reminder_time`.

FE cần xử lý `409`:

```text
Lịch học này bị trùng với một sách khác. Vui lòng chọn ngày hoặc giờ khác.
```

Hiện request chỉ gửi `schedule_config` là weekday list. Reminder time lấy từ notification settings.

### 7.3 Reading Plan Setup UX

UI nên có:

- mode segmented control: `Đầy đủ` / `Tinh gọn`;
- pace selector;
- weekday multi-select;
- reminder settings summary;
- link mở Notification Settings nếu user muốn đổi giờ nhắc chung;
- estimate bottom sheet trước khi submit;
- submit button.

Product decision:

```text
Reminder time dùng notification settings chung.
Phase 4 chưa cho chọn reminder time riêng theo từng book.
```

Estimate bottom sheet cần hiển thị:

- số chương lấy từ upload response;
- tổng số trang nếu backend có `page_start/page_end`;
- mode sẽ generate: `full` hoặc `pareto`;
- cảnh báo nếu sách lớn hoặc nhiều chương;
- message rõ ràng: "Sách này có thể mất vài phút để xử lý. Bạn có thể nghe khi nội dung đầu tiên sẵn sàng."

FE chưa cần hiển thị token/cost tiền thật nếu backend chưa trả estimate chính xác.

Sau submit:

```text
store job_id
go to Processing screen
start polling /jobs/{job_id}
```

## 8. Processing Job Polling

### 8.1 API

```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer <access_token>
```

Recovery after reload:

```http
GET /api/v1/books/{book_id}/processing-status
Authorization: Bearer <access_token>
```

Response:

```json
{
  "id": "uuid",
  "book_id": "uuid",
  "job_type": "generate_plan",
  "status": "processing",
  "mode": "full",
  "progress_percent": 33,
  "current_step": "Đã có nội dung đầu tiên có thể nghe. Phần còn lại đang được xử lý.",
  "total_units": 3,
  "done_units": 1,
  "failed_units": 0,
  "estimated_input_tokens": 16453,
  "estimated_audio_seconds": 3382,
  "error_message": null
}
```

### 8.2 Polling Rule

| Status | Interval |
| --- | --- |
| `queued` | 2s |
| `processing` | 2-3s |
| `partial_ready` | 5-10s |
| app background | pause hoặc 30-60s |
| `ready/error/cancelled` | stop |

### 8.3 Processing UI

Show:

- progress bar;
- `current_step`;
- `done_units / total_units`;
- estimated audio duration nếu có;
- CTA "Nghe chương đầu" khi `partial_ready`;
- error card nếu `error`.

Không show fake progress.

## 9. Partial Ready Unlock

`partial_ready` nghĩa là:

```text
Ít nhất có nội dung đầu tiên nghe được.
```

Không có nghĩa là đúng 50%.

FE khi thấy `partial_ready`:

1. Call `GET /books/{book_id}/details`.
2. Build playlist từ chapters đã có segments.
3. Unlock nghe.
4. Tiếp tục poll job cho đến `ready`.
5. Khi `done_units` tăng, refresh details.

UI:

```text
Chương 1: Có thể nghe
Chương 2: Đang xử lý
Chương 3: Đang xử lý
```

Không reorder chapter.

## 10. Book APIs

### 10.1 List Books

```http
GET /api/v1/books
Authorization: Bearer <access_token>
```

Response:

```json
[
  {
    "id": "uuid",
    "title": "Chương 4_ Phương pháp luận nghiên cứu",
    "author": null,
    "total_chapters": 3,
    "status": "ready",
    "document_type": "pdf",
    "file_url": "https://...",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

### 10.2 Get Book

```http
GET /api/v1/books/{book_id}
Authorization: Bearer <access_token>
```

### 10.3 Book Details

```http
GET /api/v1/books/{book_id}/details
Authorization: Bearer <access_token>
```

Response:

```json
{
  "book_status": "ready",
  "total_chapters": 3,
  "chapters": [
    {
      "id": "uuid",
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "status": "ready",
      "chapter_index": 0,
      "review_text": "...",
      "review_audio_url": "https://...",
      "chapter_segments": [
        {
          "id": 1830,
          "segment_index": 0,
          "audio_url": "https://...",
          "text_content": "...",
          "duration_ms": 18240,
          "mode": "full"
        }
      ]
    }
  ]
}
```

FE rules:

- sort chapters by `chapter_index`;
- sort segments by `segment_index`;
- `duration_ms` can be null;
- later chapters may have empty segments during `partial_ready`;
- keep player stable when refreshing details.

### 10.4 Update Book Metadata

```http
PUT /api/v1/books/{book_id}
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "title": "Tên mới",
  "author": "Tác giả"
}
```

### 10.5 Delete Book

```http
DELETE /api/v1/books/{book_id}
Authorization: Bearer <access_token>
```

Response:

```json
{
  "message": "Book deleted"
}
```

## 11. Switch Mode

### 11.1 API

```http
POST /api/v1/books/{book_id}/switch-mode
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "mode": "pareto"
}
```

Response nếu cần generate:

```json
{
  "message": "Đã chuyển sang mode pareto. Hệ thống đang sinh audio trong background.",
  "needs_generation": true,
  "job_id": "uuid",
  "status": "queued",
  "progress_percent": 0
}
```

Response nếu audio đã có:

```json
{
  "message": "Đã chuyển sang mode full. Audio đã có sẵn.",
  "needs_generation": false,
  "job_id": null,
  "status": null,
  "progress_percent": null
}
```

### 11.2 UI Rule

Nếu `needs_generation=false`:

```text
refresh details
switch playlist ngay
```

Nếu `needs_generation=true`:

```text
poll job_id
show generation progress for selected mode
unlock when partial_ready
refresh details on ready
```

Nếu job switch-mode trả `error`:

```text
giữ audio mode cũ nếu vẫn còn playable
show message lỗi ngắn
cho user retry switch mode sau
refresh book/details để lấy trạng thái thật từ backend
```

Product decision:

```text
Khi switch mode cần generate lại, FE giữ audio mode cũ đang phát cho tới khi mode mới partial_ready hoặc ready.
```

Ví dụ user đang nghe `full` và bấm switch sang `pareto`:

1. FE gọi `POST /books/{book_id}/switch-mode`.
2. Nếu response có `needs_generation=true`, FE giữ playlist/audio `full` hiện tại.
3. UI hiện badge: "Đang chuẩn bị bản Pareto".
4. FE poll `job_id`.
5. Khi mode mới đạt `partial_ready`, FE hiển thị CTA chuyển sang bản mới.
6. Khi mode mới `ready`, FE refresh details và cho phép dùng playlist mới hoàn chỉnh.

Không xoá hoặc hide audio mode cũ ngay khi user bấm switch. Switch mode là workflow background, không phải đổi tab tức thì.

## 12. Learning Progress And Resume

### 12.1 Get Book Learning Progress

```http
GET /api/v1/books/{book_id}/learning-progress?mode=full
Authorization: Bearer <access_token>
```

Response:

```json
{
  "book_id": "uuid",
  "mode": "full",
  "book_progress_percent": 27,
  "completed_chapters": 1,
  "playable_chapters": 3,
  "last_chapter_id": "uuid",
  "last_segment_id": 1839,
  "last_segment_index": 9,
  "position_ms": 3583,
  "chapters": [
    {
      "chapter_id": "uuid",
      "mode": "full",
      "segment_id": 1839,
      "segment_index": 9,
      "position_ms": 3583,
      "progress_percent": 81,
      "max_progress_percent": 81,
      "status": "completed",
      "started_at": "...",
      "last_activity_at": "...",
      "completed_at": "..."
    }
  ]
}
```

FE dùng để:

- hiện progress tổng của book;
- resume đúng chapter/segment/position;
- biết chapter nào completed;
- render button "Tiếp tục nghe".

### 12.2 Update Chapter Progress

```http
PUT /api/v1/books/{book_id}/chapters/{chapter_id}/progress
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "mode": "full",
  "segment_id": 1839,
  "segment_index": 9,
  "position_ms": 3583,
  "listened_ms": 3583,
  "total_duration_ms": null,
  "progress_percent": 82,
  "force_persist": false
}
```

Important:

```text
Nếu backend có segment duration thật, backend tự tính percent theo duration.
FE progress_percent chỉ là fallback.
```

Vì vậy FE không nên kỳ vọng response luôn bằng payload.

`force_persist=true` chỉ dùng cho các mốc quan trọng:

- pause;
- app background;
- user đóng player;
- user seek mạnh và muốn lưu resume ngay;
- trước khi chuyển sang màn khác.

### 12.3 Progress Sending Rule

FE không được spam mỗi giây.

Đề xuất:

```text
Gửi khi:
- bắt đầu nghe một chapter mới;
- đổi segment;
- pause;
- app background;
- user đóng player;
- mỗi 10-30 giây khi đang phát;
- khi progress tăng đáng kể, ví dụ >= 2%.
```

Sau khi BE implement throttle, FE vẫn nên debounce để tiết kiệm pin/network.

Backend hiện chỉ ghi DB khi:

- lần đầu tạo progress;
- đổi segment;
- progress tăng ít nhất `LEARNING_PROGRESS_MIN_DELTA_PERCENT`, mặc định 5%;
- progress đạt ngưỡng complete, mặc định 80%;
- record cũ hơn `LEARNING_PROGRESS_STALE_SECONDS`, mặc định 30 giây;
- request có `force_persist=true`.

Production verified ngày 2026-05-26:

```text
force_persist=true  -> backend lưu position_ms mới ngay.
progress nhỏ +1%    -> backend trả lại position_ms đã lưu trước đó, không ghi DB mới.
```

Vì vậy FE nên dùng response từ backend làm source of truth cho resume position, không tự tin rằng mọi payload progress đều được lưu.

### 12.4 Manual Complete

```http
POST /api/v1/books/{book_id}/chapters/{chapter_id}/complete
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "mode": "full"
}
```

UI:

```text
Button: "Đánh dấu đã học xong"
```

Chỉ show khi chapter có playable audio.

## 13. Spaced Review

Backend tạo spaced review khi:

```text
max_progress_percent >= 80
```

Hoặc user bấm manual complete.

Intervals:

```text
1, 3, 7, 14, 30 ngày
```

FE không tự tạo review.

FE nhận review thông qua notification:

```text
type = spaced_review_due
action_type = open_review
action_payload.review_item_id
```

### 13.1 Complete Review

```http
POST /api/v1/reviews/{review_item_id}/complete
Authorization: Bearer <access_token>
```

Response:

```json
{
  "review_item_id": "uuid",
  "status": "completed",
  "completed_at": "2026-05-25T10:21:57.833114Z"
}
```

### 13.2 Skip Review

```http
POST /api/v1/reviews/{review_item_id}/skip
Authorization: Bearer <access_token>
```

Response:

```json
{
  "review_item_id": "uuid",
  "status": "skipped",
  "completed_at": null
}
```

## 14. Notifications

### 14.1 List Notifications

```http
GET /api/v1/notifications?limit=30&unread_only=false
Authorization: Bearer <access_token>
```

Response:

```json
{
  "items": [
    {
      "id": "uuid",
      "type": "content_ready",
      "title": "Có thể bắt đầu nghe rồi",
      "body": "...",
      "action_type": "open_book",
      "action_payload": {
        "book_id": "uuid",
        "mode": "full"
      },
      "read_at": null,
      "created_at": "..."
    }
  ],
  "unread_count": 3
}
```

Production verified ngày 2026-05-26 với Celery Beat + notification worker bật:

```text
Sau generate-plan hoàn tất, backend tạo và deliver in-app content_ready notifications.
Trong test thật, notification xuất hiện sau khoảng 1 phút:
- "Có thể bắt đầu nghe rồi"
- "Sách đã sẵn sàng"
```

FE không nên kỳ vọng notification xuất hiện tức thì đúng thời điểm job chuyển `ready`. Notification đi qua outbox/Beat/worker nên có độ trễ ngắn. FE vẫn nên poll job để unlock playback; notification dùng cho badge/inbox/navigation.

### 14.2 Mark Read

```http
PATCH /api/v1/notifications/{notification_id}/read
Authorization: Bearer <access_token>
```

### 14.3 Mark All Read

```http
PATCH /api/v1/notifications/read-all
Authorization: Bearer <access_token>
```

### 14.4 Notification Settings

```http
GET /api/v1/notifications/settings
Authorization: Bearer <access_token>
```

```http
PUT /api/v1/notifications/settings
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:

```json
{
  "timezone": "Asia/Ho_Chi_Minh",
  "reminders_enabled": true,
  "spaced_review_enabled": true,
  "reminder_time": "20:00",
  "quiet_hours_start": "22:00",
  "quiet_hours_end": "07:00",
  "daily_cap": 3
}
```

Validation:

- time format: `HH:MM`;
- timezone: IANA timezone;
- daily_cap: `0..10`.

### 14.5 Notification Center UX

Screen:

- unread badge;
- list notifications newest first;
- filter unread;
- tap notification action;
- mark all read.

Action mapping:

| action_type | FE action |
| --- | --- |
| `open_book` | open book detail/listening |
| `open_review` | open review screen for review item |

## 15. Push Notification

Phase hiện tại:

```text
In-app notification only.
```

Product decision:

```text
Push notification không nằm trong Phase 4 hiện tại.
Push FCM làm ở phase sau khi Auth thật đã ổn định.
```

Vì sao cần Auth?

- FE cần gửi FCM device token gắn với user thật.
- BE cần biết token đó thuộc user nào.
- Logout cần unregister/deactivate token.

API dự kiến sau này:

```http
POST /api/v1/devices/register
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "device_token": "<fcm_device_token>",
  "platform": "android"
}
```

Nhớ phân biệt:

```text
access token = chứng minh user là ai
FCM token = gửi push tới thiết bị nào
```

## 16. Study Context

### 16.1 Manual Context APIs

Create:

```http
POST /api/v1/study-contexts
Authorization: Bearer <access_token>
```

```json
{
  "title": "Ôn thi phương pháp nghiên cứu"
}
```

List:

```http
GET /api/v1/study-contexts
Authorization: Bearer <access_token>
```

Get:

```http
GET /api/v1/study-contexts/{context_id}
Authorization: Bearer <access_token>
```

Update:

```http
PATCH /api/v1/study-contexts/{context_id}
Authorization: Bearer <access_token>
```

Delete:

```http
DELETE /api/v1/study-contexts/{context_id}
Authorization: Bearer <access_token>
```

Add document:

```http
POST /api/v1/study-contexts/{context_id}/documents
Authorization: Bearer <access_token>
```

```json
{
  "book_id": "uuid"
}
```

Create thread:

```http
POST /api/v1/study-contexts/{context_id}/threads
Authorization: Bearer <access_token>
```

```json
{
  "title": "Hỏi đáp chương 4"
}
```

### 16.2 Quick Book Chat

Cho Book Detail / Now Listening:

```http
GET /api/v1/threads/for-book/{book_id}
Authorization: Bearer <access_token>
```

Response:

```json
{
  "context_id": "uuid",
  "thread_id": "uuid",
  "is_auto_generated": true
}
```

Lấy history:

```http
GET /api/v1/threads/{thread_id}/messages
Authorization: Bearer <access_token>
```

Update thread:

```http
PUT /api/v1/threads/{thread_id}
Authorization: Bearer <access_token>
```

Delete thread:

```http
DELETE /api/v1/threads/{thread_id}
Authorization: Bearer <access_token>
```

## 17. LiveKit Voice/Text Agent

### 17.1 Token

Production path:

```http
GET /api/v1/live-token/thread/{thread_id}
Authorization: Bearer <access_token>
```

Response:

```json
{
  "token": "<livekit_jwt>",
  "room_name": "..."
}
```

Avoid:

```text
GET /api/v1/live-token/{book_id}
```

Vì endpoint này là legacy/debug và không gắn chặt thread persistence.

### 17.2 DataChannel Topics

`lk.chat`

```text
Client -> Server: text plain UTF-8
Server -> Client: fast assistant text/greeting
```

`lk.transcript`

```json
{
  "v": 1,
  "type": "transcript",
  "role": "assistant",
  "text": "...",
  "id": "uuid",
  "ts": "2026-05-26T10:00:00.000+00:00"
}
```

Rules:

- FE chỉ subscribe `lk.transcript`.
- FE không publish lên `lk.transcript`.
- Dedupe bằng `id`.
- Timeline chính nên dùng transcript/history.

`lk.control`

```json
{
  "type": "toggle_web_search",
  "enabled": true
}
```

Dùng cho web-search toggle nếu UI có.

## 18. Recommended Screens

### 18.1 Auth Screens

Required:

- login email/password;
- signup email/password;
- Google OAuth nếu FE làm kịp;
- logout;
- expired session handling.

After login:

- store access token securely;
- attach Authorization header;
- optionally fetch notification settings.

### 18.2 Library Screen

API:

```text
GET /books
```

UI:

- list books;
- status chip;
- continue listening card;
- upload CTA;
- notification badge.

Product decision:

```text
Library phải hiển thị cả draft, processing, partial_ready, ready và error.
```

Không chỉ hiển thị sách `ready`, vì user upload xong mà không thấy sách sẽ tưởng dữ liệu bị mất.

Status label:

| Backend | Label |
| --- | --- |
| `draft` | Chưa tạo kế hoạch |
| `processing` | Đang xử lý |
| `partial_ready` | Có thể nghe |
| `ready` | Sẵn sàng |
| `error` | Lỗi |

Recommended UI behavior:

| Status | Primary CTA | Secondary UI |
| --- | --- | --- |
| `draft` | Tạo kế hoạch | Xoá sách |
| `processing` | Xem tiến độ | Badge đang xử lý |
| `partial_ready` | Nghe ngay | Banner còn đang xử lý tiếp |
| `ready` | Tiếp tục nghe | Ôn tập / hỏi AI |
| `error` | Thử lại hoặc xoá | Hiển thị lỗi ngắn |

### 18.3 Upload Screen

UI:

- file picker;
- requirement hint;
- upload progress;
- outline preview;
- error guidance.

### 18.4 Reading Plan Setup Screen

UI:

- mode segmented control;
- pace selector;
- weekday picker;
- reminder settings summary;
- estimate bottom sheet before submit;
- submit button.

### 18.5 Processing Screen

UI:

- progress bar;
- current step;
- done/total;
- estimated audio time;
- listen CTA when partial;
- error action.

### 18.6 Book Detail Screen

UI:

- title;
- status;
- mode selector;
- chapter list;
- progress per chapter;
- resume CTA;
- ask AI CTA;
- review CTA.

### 18.7 Now Listening Screen

UI:

- audio player;
- current chapter/segment;
- playlist;
- progress sync;
- background processing banner if book still partial;
- quick chat entry.

### 18.8 Notification Center

UI:

- unread count;
- notification list;
- mark all read;
- action navigation.

### 18.9 Review Screen

UI:

- tab/section: "Ôn tập hôm nay";
- tab/section: "Sắp tới";
- tab/section: "Đã hoàn thành";
- tab/section: "Bỏ qua";
- book/chapter title;
- review text;
- review audio if available;
- complete button;
- skip button.

Product decision:

```text
Cần màn hình Review riêng.
Notification chỉ là entry point, không phải nơi duy nhất để mở review.
```

## 19. App Reload Recovery

When app starts:

1. Check auth session.
2. Call `GET /books`.
3. For processing/partial books, call `GET /books/{book_id}/processing-status`.
4. Resume polling non-terminal jobs.
5. For ready/partial books, call `GET /books/{book_id}/learning-progress?mode=...`.
6. Show resume card using `last_chapter_id`, `last_segment_id`, `position_ms`.

Do not require old `job_id` to exist in local storage forever.

## 20. FE Acceptance Checklist

Auth:

- [ ] Sends `Authorization: Bearer <access_token>` for user-owned APIs.
- [ ] Handles 401 by refresh/logout.
- [ ] Does not send `user_id` manually.
- [ ] Supports email/password login.
- [ ] Supports Google OAuth if included in scope.

Upload:

- [ ] Uploads file field name `file`.
- [ ] Validates PDF/EPUB/DOCX and max size locally.
- [ ] Shows outline preview.
- [ ] Handles 422 no outline/TOC/Heading.

Generate plan:

- [ ] Sends `book_id`, `mode`, `pace`, `schedule_config`.
- [ ] Handles 409 schedule conflict.
- [ ] Stores `job_id`.
- [ ] Shows simple estimate bottom sheet before generate.
- [ ] Shows reminder time from global notification settings.

Processing:

- [ ] Polls `/jobs/{job_id}`.
- [ ] Recovers with `/books/{book_id}/processing-status`.
- [ ] Unlocks listening on `partial_ready`.
- [ ] Stops on terminal status.

Playback:

- [ ] Sorts chapters and segments.
- [ ] Does not reset playback on details refresh.
- [ ] Handles partial playlist.
- [ ] Keeps old playable mode while new switch-mode job is generating.

Learning progress:

- [ ] Calls `GET /learning-progress` on book open.
- [ ] Sends progress every 10-30 seconds and on lifecycle events.
- [ ] Uses response `status`, not local guess, for completed state.
- [ ] Supports manual complete.

Review:

- [ ] Opens review from notification action.
- [ ] Has a dedicated Review screen/list.
- [ ] Calls complete/skip API.
- [ ] Does not create review locally.

Notification:

- [ ] Lists notifications.
- [ ] Shows unread count.
- [ ] Marks read/read-all.
- [ ] Navigates by `action_type`.

Voice/chat:

- [ ] Uses `/threads/for-book/{book_id}` for book quick chat.
- [ ] Uses `/live-token/thread/{thread_id}`.
- [ ] Publishes text to `lk.chat`.
- [ ] Subscribes to `lk.transcript`.
- [ ] Dedupe by transcript `id`.

## 21. BE Readiness Before FE Full Implementation

Trạng thái backend sau hardening ngày 2026-05-26:

```text
BE done all task 21.
Production smoke test passed after deploy for auth/upload/generate/progress/notification.
Switch-mode production passed after redeploy with loop-local async limiter.
```

### 21.1 Auth refactor

Status:

```text
Done in backend code.
```

Pattern:

```python
current_user: CurrentUser
user_id = current_user.sub
```

Đã cover bằng test tự động:

- user A không thấy books user B;
- user A không update/delete book user B;
- user A không đọc notification user B;
- user A không lấy LiveKit token thread user B.

Production verification sau deploy:

```text
GET /openapi.json cho thấy user-owned routes có security=true.
GET /api/v1/books không có token trả 401.
GET /api/v1/books có Supabase token hợp lệ trả dữ liệu của đúng user.
```

### 21.2 Production Redis/Celery smoke test

Status:

```text
Script smoke test đã hỗ trợ auth token.
Production smoke test đã pass ngày 2026-05-26.
```

Script:

```powershell
uv run python scripts/production_smoke_test.py `
  --base-url https://khoasinoo-tri-am-backend.hf.space `
  --access-token "<supabase_access_token>" `
  --pdf-path "Chương 4_ Phương pháp luận nghiên cứu.pdf" `
  --generate-plan `
  --poll `
  --require-background-ok `
  --timeout-seconds 1800
```

Flow script kiểm tra:

```text
POST /upload
POST /generate-plan
task đi qua Redis
Celery worker consume queue document
GET /jobs/{job_id} tới ready
```

Kết quả production test với file thật `Chương 4_ Phương pháp luận nghiên cứu.pdf`:

```text
health=ok
background health=ok
redis=ok
document_queue_length=0 trước khi test
upload: 3 chapters
job flow: queued -> processing -> partial_ready 33% -> partial_ready 66% -> ready 100%
done_units=3
failed_units=0
estimated_input_tokens=16453
estimated_audio_seconds=3382
```

Không chỉ gọi trực tiếp `process_book_task`; job đã đi qua API production, Redis broker và Celery document worker thật.

Production startup note:

```text
Khi bật document worker + notification worker + Celery Beat trên Redis Cloud free,
log startup có thể xuất hiện transient "max number of clients reached".
Trong test thật, worker tự reconnect và chuyển sang ready.
```

BE đã thêm config giảm Redis connection pressure:

```text
CELERY_BROKER_POOL_LIMIT=1
```

FE không cần xử lý riêng lỗi startup này. Nếu `/api/v1/health/background` trả `ok` và job polling chạy được, hệ thống background đang hoạt động.

### 21.3 Progress write throttle

Status:

```text
Done in backend code.
Production verified ngày 2026-05-26.
```

Backend giảm DB write spam:

```text
write khi:
- lần đầu tạo progress;
- đổi segment;
- progress tăng >= 5%;
- đạt ngưỡng complete;
- quá stale window;
- request force_persist=true.
```

FE vẫn phải debounce.

### 21.4 Production Phase 4 probe

Ngoài smoke upload/generate, production đã verify thêm:

```text
GET /books: account test thấy đúng book của user thật.
GET /books/{book_id}/details: book ready, 3 chapters, có audio segments.
PUT /progress force_persist=true: lưu resume position.
PUT /progress nhỏ ngay sau đó: bị throttle, trả lại position đã lưu.
GET /learning-progress: trả resume summary.
POST /chapters/{chapter_id}/complete: trả status=completed.
GET /threads/for-book/{book_id}: tạo/lấy direct book thread thành công.
GET /live-token/thread/{thread_id}: trả LiveKit token thành công.
GET /notifications: nhận 2 content_ready notifications sau khi Beat/worker chạy.
```

### 21.5 Switch-mode production verification

Production test đầu tiên ngày 2026-05-26 từng phát hiện switch-mode `full -> pareto` fail sau khi đạt `partial_ready`:

```text
job_type=switch_mode
status=error
progress_percent=33
error_message="<asyncio.locks.Semaphore ...> is bound to a different event loop"
```

Nguyên nhân là worker cũ dùng `asyncio.Semaphore` global trong process, trong khi Celery chạy nhiều job qua các event loop khác nhau. BE local đã fix bằng loop-local limiter:

```text
app/services/async_limiter.py
```

Sau khi deploy lại bản có fix, production retest đã pass:

```text
POST /books/{book_id}/switch-mode mode=pareto -> needs_generation=true
poll /jobs/{job_id}
actual: queued -> processing -> partial_ready 33% -> partial_ready 66% -> ready 100%
done_units=3
failed_units=0
details after switch: book_status=ready, 3 chapters, pareto segment_counts=[10, 14, 15]
```

FE contract giữ nguyên: khi `needs_generation=true`, giữ audio mode cũ, poll job, unlock mode mới khi `partial_ready`, refresh details khi `ready`.

## 22. Product Decisions Đã Chốt

Các quyết định dưới đây là contract để FE implement UI/UX Phase 4:

| Vấn đề | Quyết định |
| --- | --- |
| Auth flow | Supabase email/password là chính, Google OAuth nếu FE làm kịp |
| Custom auth | Không dùng |
| Library draft book | Có hiển thị `draft`, `processing`, `partial_ready`, `ready`, `error` |
| Reminder time | Dùng notification settings chung, chưa có per-book reminder override |
| Push notification | Để phase sau, Phase 4 chỉ in-app notification |
| Estimate trước generate | Có bottom sheet estimate đơn giản |
| Switch mode | Giữ audio mode cũ đang phát khi mode mới đang generate |
| Review UX | Có Review screen riêng, notification chỉ là entry point |

Những điểm còn có thể mở rộng sau Phase 4:

- per-book reminder override;
- push notification FCM/APNs;
- quota/cost estimate chính xác từ backend;
- retry UX chi tiết cho từng chapter lỗi;
- màn quản lý giới hạn số sách đang học song song.

## 23. Golden Path Cho FE Implement

Thứ tự đề xuất:

```text
1. Auth + ApiClient + AuthInterceptor
2. Book list/details
3. Upload + outline preview
4. Reading plan setup
5. Job polling + processing screen
6. Partial-ready playback unlock
7. Now listening + progress sync
8. Learning progress/resume
9. Notifications center
10. Review complete/skip
11. Study Context quick chat
12. LiveKit voice/text agent
13. Switch mode
14. QA diagnostics
```

Nếu làm theo thứ tự này, FE sẽ đi từ core flow tới advanced flow, ít bị vỡ kiến trúc.

## 24. Một Câu Định Hướng Cho FE

```text
Backend là source of truth cho trạng thái xử lý, tiến độ học, notification và review.
Flutter là UI state machine hiển thị đúng các trạng thái đó, không tự đoán business rule.
```

Đây là nguyên tắc quan trọng nhất khi implement TriAm Flutter Phase 4.
