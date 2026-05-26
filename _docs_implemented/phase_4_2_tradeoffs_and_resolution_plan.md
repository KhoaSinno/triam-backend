# Phase 4.2 - Tổng Hợp Implement, Test, Fix, Trade-off Và Hướng Giải Quyết

Ngày tổng hợp: 2026-05-25  
Trạng thái: Phase 4.2 backend đã implement và test pass với book thật  
File book thật đã test: `Chương 4_ Phương pháp luận nghiên cứu.pdf`

## 1. Kết Luận Ngắn Gọn

Phase 4.2 đã hoàn thành mục tiêu backend chính:

- User nghe sách có thể lưu tiến độ theo chapter/segment.
- FE có thể resume đúng segment và vị trí nghe.
- Spaced review chỉ được tạo sau khi user thật sự hoàn thành chapter.
- Plan reminder không còn nhắc bừa khi user đã học hôm đó hoặc không còn chapter playable chưa học.
- Notification in-app hoạt động qua outbox.
- Book thật đã upload, generate plan, xử lý audio/RAG, learning progress, spaced review, notification, review complete thành công.

Kết quả test quan trọng:

```text
PDF thật upload được.
Book READY.
Job READY 100%.
3/3 chapters READY.
99 audio segments được tạo.
35 knowledge chunks được tạo.
content_ready first_playable sent.
content_ready book_ready sent.
spaced_review_due sent.
review complete API completed.
```

## 2. Những Gì Đã Implement

### 2.1 Database

Đã thêm hoặc mở rộng các bảng phục vụ learning loop:

- `chapter_learning_progress`
- `reading_plan_schedule_slots`
- `spaced_review_items.anchor_completed_at`
- `spaced_review_items.source_progress_id`
- `spaced_review_items.notified_at`
- `spaced_review_items.last_reviewed_at`

Ý nghĩa:

- `chapter_learning_progress` là sự thật về việc user đã học tới đâu.
- `reading_plan_schedule_slots` là sự thật về lịch học active của user.
- `spaced_review_items` giờ được neo vào thời điểm user hoàn thành chapter, không còn neo vào lúc chapter vừa được generate xong.

Migration đã chạy:

```text
f6a8c2d4e9b1 (head)
```

### 2.2 API

Đã thêm các API:

```text
PUT  /api/v1/books/{book_id}/chapters/{chapter_id}/progress
POST /api/v1/books/{book_id}/chapters/{chapter_id}/complete
GET  /api/v1/books/{book_id}/learning-progress
POST /api/v1/reviews/{review_item_id}/complete
POST /api/v1/reviews/{review_item_id}/skip
```

FE dùng các API này để:

- cập nhật tiến độ nghe;
- lấy vị trí nghe gần nhất;
- biết tổng tiến độ của book;
- đánh dấu chapter hoàn thành thủ công;
- hoàn thành hoặc bỏ qua một review.

### 2.3 Worker Và Notification

Đã cập nhật worker pipeline:

- Khi chapter đầu tiên playable, tạo event `content_ready:first_playable`.
- Khi cả book ready, tạo event `content_ready:book_ready`.
- Không tạo spaced review trong `chapter_worker` nữa.
- Spaced review chỉ tạo trong learning progress service khi user đạt completion threshold.

Notification outbox hiện hỗ trợ:

- `content_ready` subtype `first_playable`;
- `content_ready` subtype `book_ready`;
- `spaced_review_due`;
- `plan_reminder`.

### 2.4 Guardrails

Đã thêm các guardrails:

- Không cho trùng active schedule slot.
- Có giới hạn số book đang học active.
- Plan reminder bỏ qua nếu user đã học book đó trong ngày.
- Plan reminder bỏ qua nếu không còn chapter playable chưa completed.
- Spaced review không gửi nếu chapter progress chưa completed.
- Legacy `review_text` dạng plain text không làm API progress bị 500.
- Legacy `notification_settings.daily_cap` vượt giới hạn được normalize về khoảng hợp lệ.

## 3. Những Gì Đã Test

### 3.1 Automated Tests

```powershell
uv run pytest tests/test_phase4_2_learning_loop.py -q
```

Kết quả:

```text
5 passed
```

Các case chính:

- 50% chưa tạo review.
- >=80% tạo 5 review intervals.
- Không tạo duplicate review khi progress update nhiều lần.
- Book progress trả về resume position.
- Schedule conflict và active book limit hoạt động.
- Plan reminder bỏ qua nếu user đã học hôm nay.
- Legacy plain `review_text` vẫn tạo review được.

### 3.2 Non-live Regression Suite

```powershell
uv run pytest -q --ignore=tests/test_agent_chat_text_only.py --ignore=tests/test_threads_for_book.py
```

Kết quả:

```text
40 passed
```

### 3.3 Threads Integration

Bật FastAPI tạm ở `127.0.0.1:8000`, chạy:

```powershell
uv run pytest tests/test_threads_for_book.py -q
```

Kết quả:

```text
6 passed
```

### 3.4 Real Book Full Flow

Đã test với file thật:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

Kết quả:

```json
{
  "book_id": "4ff2cfd8-029d-46e0-baae-15ba634c9f21",
  "status": "ready",
  "total_chapters": 3,
  "total_segments": 99,
  "total_knowledge_chunks": 35,
  "job_status": "ready",
  "job_progress_percent": 100,
  "failed_units": 0
}
```

Learning progress với book thật:

```json
{
  "reviews_after_50": 0,
  "progress_after_80_percent": "completed",
  "review_intervals": [1, 3, 7, 14, 30],
  "final_review_status": "completed",
  "final_progress_status": "completed"
}
```

Log đầy đủ:

```text
logs/phase4_2_real_book_full_flow.json
logs/phase4_2_real_book_learning_flow.json
```

## 4. Những Bug Đã Phát Hiện Và Đã Fix

### Bug 1: `review_text` legacy làm API progress bị 500

Hiện tượng:

```text
Chapter review_text không phải JSON hợp lệ.
```

Nguyên nhân:

- Code cũ giả định `chapter.review_text` luôn là JSON dạng `{ "full": "...", "pareto": "..." }`.
- Nhưng dữ liệu cũ hoặc test seed có thể là plain text.

Fix:

- Nếu parse JSON được và là object thì lấy theo mode.
- Nếu không parse được thì xem như plain review text.

Lý do chọn cách này:

- Không làm user fail khi vừa hoàn thành chapter.
- Tương thích dữ liệu cũ.
- Không cần migration sửa toàn bộ dữ liệu text cũ ngay lập tức.

### Bug 2: `daily_cap=50` legacy làm API settings bị response validation error

Hiện tượng:

```text
Input should be less than or equal to 10
```

Nguyên nhân:

- DTO response giới hạn `daily_cap <= 10`.
- DB local có row cũ `daily_cap=50`.

Fix:

- Repository normalize `daily_cap` về khoảng `0..10` khi đọc settings.

Lý do chọn cách này:

- Self-healing dữ liệu cũ.
- Tránh 500 sau deploy khi gặp row cũ.

### Bug 3: Test outbox phụ thuộc DB sạch

Hiện tượng:

- Test claim outbox bị claim cả pending outbox rác trong DB thật.

Fix:

- Test claim `limit=1`.
- Outbox test có `due_at=2000-01-01` để deterministic hơn.

Lý do:

- Dự án đang test trên DB thật, không phải isolated test DB.
- Test phải chịu được DB có rác như em yêu cầu.

### Bug 4: Test sai mốc progress trên book thật

Hiện tượng:

- Gửi progress 82% nhưng chỉ ở segment đầu tiên, backend không completed.

Nguyên nhân:

- Backend không tin tuyệt đối `progress_percent` FE gửi nếu có đủ duration thật.
- Backend tính progress theo tổng duration của toàn chapter.

Kết luận:

- Đây không phải bug.
- Đây là logic đúng.

Hướng test đúng:

- Chọn segment/position tương ứng 82% của tổng duration chapter.
- Backend trả `81` do ép `int`, vẫn completed vì threshold là `80`.

## 5. Trade-off Còn Lại

Hiện còn **14 trade-off đáng theo dõi** trước khi gọi là production hoàn chỉnh. Không phải tất cả đều cần fix ngay, nhưng phải biết để bảo vệ đồ án và lên phase tiếp theo.

## 6. Danh Sách Trade-off Và Hướng Giải Quyết

### Trade-off 1: Vẫn dùng `MOCK_USER_ID`

Mức độ: Cao  
Ảnh hưởng: Tất cả user đang dùng chung logic giả lập nếu chưa thay auth thật.

Hiện trạng:

- Upload, progress, notification, review vẫn dùng mock user trong nhiều router/service.

Rủi ro:

- Khi nhiều user thật dùng app, dữ liệu sẽ bị lẫn nếu chưa thay bằng JWT user id.

Hướng giải quyết:

1. Tạo dependency `get_current_user_id`.
2. Decode JWT Supabase/Auth provider.
3. Thay toàn bộ `MOCK_USER_ID`.
4. Thêm test user A không đọc được data user B.

Phase đề xuất: Phase 5 Auth Hardening.

### Trade-off 2: Notification hiện mới là in-app

Mức độ: Trung bình đến cao  
Ảnh hưởng: User không mở app thì không nhận nhắc học.

Hiện trạng:

- `notification_outbox` và `user_notifications` đã ổn.
- Chưa có FCM/device token/push thật.

Hướng giải quyết:

1. Thêm `user_devices`.
2. Thêm `NotificationChannel.PUSH`.
3. Thêm FCM adapter.
4. Outbox deliver theo channel.
5. FE gửi device token sau login.

Phase đề xuất: Phase 5 hoặc Phase 6 Push Notification.

### Trade-off 3: Celery Beat phải đảm bảo chỉ chạy một instance

Mức độ: Cao khi deploy nhiều runtime  
Ảnh hưởng: Nếu nhiều Beat cùng scan có thể tạo tải thừa hoặc tranh lock.

Hiện trạng:

- Outbox có idempotency nên giảm duplicate.
- Nhưng Beat multi-instance vẫn không nên.

Hướng giải quyết:

1. Chỉ bật `ENABLE_CELERY_BEAT=true` ở một runtime.
2. Khi scale nhiều server, tách Beat thành một deployment riêng.
3. Có thể thêm DB advisory lock cho scanner.

Phase đề xuất: Deploy hardening tiếp theo.

### Trade-off 4: Progress write chưa throttle

Mức độ: Trung bình  
Ảnh hưởng: FE gửi progress quá dày sẽ làm tăng DB writes.

Hiện trạng:

- Có config `LEARNING_PROGRESS_STALE_SECONDS`.
- Nhưng logic update hiện vẫn ghi mỗi request hợp lệ.

Hướng giải quyết:

1. Nếu progress mới không tăng đáng kể và chưa quá stale window thì bỏ qua write.
2. Chỉ ghi khi đổi segment, tăng >= 2%, hoặc qua `LEARNING_PROGRESS_STALE_SECONDS`.
3. FE cũng debounce, ví dụ 10 đến 30 giây/lần.

Phase đề xuất: Phase 4.3 hoặc FE integration hardening.

### Trade-off 5: Percent completion đang dùng integer floor

Mức độ: Thấp đến trung bình  
Ảnh hưởng: Test/FE có thể thấy request 82% nhưng BE trả 81%.

Hiện trạng:

- BE tính `int(current * 100 / total)`.
- Đây là floor.

Hướng giải quyết:

1. Giữ nguyên nếu chấp nhận đơn giản.
2. Hoặc lưu basis points `0..10000` để chính xác hơn.
3. Hoặc dùng `round`.

Khuyến nghị:

- Chưa cần sửa ngay.
- FE chỉ nên check `status`, không nên suy luận completion từ số lẻ.

### Trade-off 6: `listened_ms` chưa phải listening analytics thật

Mức độ: Trung bình  
Ảnh hưởng: Analytics/streak/số phút học có thể chưa chính xác nếu user seek.

Hiện trạng:

- BE lấy `max(progress.listened_ms, payload.listened_ms)`.
- Đây là đủ cho MVP progress, chưa đủ cho thống kê học nghiêm túc.

Hướng giải quyết:

1. Tạo bảng `learning_sessions`.
2. FE gửi session start/pause/heartbeat.
3. Tính listened duration từ session events thay vì chỉ position.

Phase đề xuất: Phase Analytics hoặc Study Streak.

### Trade-off 7: Reading plan schedule vẫn đơn giản

Mức độ: Trung bình  
Ảnh hưởng: User chưa có lịch học cực linh hoạt.

Hiện trạng:

- `schedule_config` là danh sách weekday.
- Reminder time lấy từ notification settings.
- Chưa có per-book custom reminder time.

Hướng giải quyết:

1. Mở rộng DTO generate plan.
2. Cho phép mỗi book có reminder time riêng.
3. UI nên hiển thị conflict trước khi submit.

Phase đề xuất: FE/BE Schedule UX Improvement.

### Trade-off 8: Active book limit còn theo config chung, chưa theo tier

Mức độ: Trung bình  
Ảnh hưởng: Sau này có free/pro thì cần limit khác nhau.

Hiện trạng:

- `MAX_ACTIVE_LEARNING_BOOKS_PER_USER=3`.

Hướng giải quyết:

1. Thêm user subscription/tier.
2. Rule service lấy limit theo tier.
3. Free 3 books, premium nhiều hơn.

Phase đề xuất: Payment/Tier later.

### Trade-off 9: Switch mode và review chain cần quyết định sâu hơn

Mức độ: Trung bình  
Ảnh hưởng: User học full rồi đổi pareto thì review nên dùng review nào?

Hiện trạng:

- Progress có `mode`.
- Active review unique theo `user_id + chapter_id + interval_days`, không tạo nhiều chain trùng cho cùng chapter.

Lý do hiện tại:

- Tránh spam user vì cùng một chapter bị review nhiều lần do đổi mode.

Câu hỏi business:

- Review nên theo chapter knowledge, hay theo mode user học?

Hướng giải quyết:

1. Nếu review theo knowledge: giữ như hiện tại.
2. Nếu review theo mode: unique index cần thêm `mode`.
3. FE cần giải thích rõ review đang dựa trên mode nào.

Khuyến nghị hiện tại:

- Giữ review theo chapter để tránh spam.
- Chỉ revisited khi product yêu cầu review riêng cho pareto/full.

### Trade-off 10: Real-book test gọi trực tiếp task entrypoint, chưa qua Redis worker process

Mức độ: Trung bình  
Ảnh hưởng: Chưa chứng minh Redis worker end-to-end trong đúng test này.

Hiện trạng:

- Test book thật gọi `process_book_task(...)` trực tiếp.
- Pipeline worker thật vẫn chạy đầy đủ.
- Lý do: tránh task lẫn queue Redis cũ và kiểm soát report.

Hướng giải quyết:

1. Bật FastAPI + Celery worker local.
2. Không monkeypatch `apply_async`.
3. Gọi API thật.
4. Poll `GET /jobs/{job_id}` tới READY.
5. Lưu log worker riêng.

Phase đề xuất:

- Trước deploy main hoặc production smoke test.

### Trade-off 11: Worker xử lý book thật còn tốn thời gian và chi phí

Mức độ: Cao với production thật  
Ảnh hưởng: File dài có thể tốn token, TTS cost, thời gian worker.

Kết quả thực tế:

- PDF nhỏ 3 chương tạo 99 segments.
- Worker chạy nhiều phút.

Hướng giải quyết:

1. Hard limit theo file/audio/token đã có, tiếp tục tinh chỉnh.
2. Thêm quota theo user/ngày.
3. Cho user xác nhận cost/time trước khi generate.
4. Ưu tiên generate first playable trước, phần sau chạy nền.
5. Tách worker document ra runtime riêng khi có tải thật.

Phase đề xuất:

- Cost control và quota phase.

### Trade-off 12: RAG và TTS cùng chapter đang coupling khá chặt

Mức độ: Trung bình  
Ảnh hưởng: Nếu TTS fail sau khi RAG đã xong, rollback sẽ xóa knowledge, có thể phải tốn embedding lại.

Hiện trạng:

- Đổi lại là consistency tốt: chapter fail thì không còn dữ liệu nửa vời.

Hướng giải quyết:

1. Tách `rag_state` và `tts_state`.
2. Cho phép retry riêng TTS mà không chạy lại embedding.
3. Cần idempotency kỹ hơn cho từng stage.

Khuyến nghị:

- Chưa cần sửa ngay nếu ưu tiên đơn giản và chắc.
- Khi cost embedding/TTS thành vấn đề thì tách stage.

### Trade-off 13: Plan reminder chưa có adaptive learning

Mức độ: Thấp đến trung bình  
Ảnh hưởng: Nhắc học vẫn dựa trên plan tĩnh, chưa cá nhân hóa.

Hiện trạng:

- Nếu user đã học hôm nay thì skip.
- Nếu còn playable uncompleted chapter thì có thể nhắc.

Hướng giải quyết:

1. Dựa vào streak.
2. Dựa vào thói quen giờ học.
3. Dựa vào chương đang học dở.
4. Dựa vào deadline hoặc mục tiêu của user.

Phase đề xuất:

- Phase Personalization.

### Trade-off 14: Test DB thật còn nhiều rác

Mức độ: Trung bình  
Ảnh hưởng: Test có thể bị ảnh hưởng bởi outbox/job/settings cũ.

Hiện trạng:

- Em cho phép rác DB.
- Anh đã làm test chịu được DB bẩn ở nhiều chỗ.

Hướng giải quyết:

1. Tạo test database riêng.
2. Dùng transaction rollback per test.
3. Hoặc dùng runtime user riêng cho integration test.
4. Có script cleanup dữ liệu test theo prefix.

Khuyến nghị:

- Khi gần bảo vệ, nên có script cleanup để demo sạch hơn.

## 7. Ưu Tiên Fix Tiếp Theo

Nếu đi theo thứ tự thực tế cho capstone, anh đề xuất:

### Ưu tiên 1: Auth thật

Lý do:

- Không thể production nếu vẫn dùng mock user.
- Tất cả API book/progress/notification đều cần user isolation.

### Ưu tiên 2: Production Redis/Celery smoke test

Lý do:

- Phase 4.2 đã test pipeline trực tiếp.
- Cần thêm một test qua Redis worker process trước deploy chính thức.

### Ưu tiên 3: Progress write throttle

Lý do:

- FE audio player có thể spam update.
- Cần bảo vệ DB.

### Ưu tiên 4: Push notification

Lý do:

- In-app chỉ hiệu quả khi user mở app.
- Reminder thật cần push.

### Ưu tiên 5: Quota/cost control

Lý do:

- Book thật generate nhiều segment.
- Cần tránh user upload quá nhiều làm cháy token/TTS.

## 8. Checklist Trước Khi Merge/Main Deploy

Trước khi merge lên main hoặc deploy bản có Phase 4.2:

- Chạy migration trên DB target:

```powershell
uv run alembic upgrade head
```

- Kiểm tra env:

```env
MAX_ACTIVE_LEARNING_BOOKS_PER_USER=3
LEARNING_COMPLETION_THRESHOLD_PERCENT=80
LEARNING_PROGRESS_STALE_SECONDS=30
PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS=24
```

- Đảm bảo worker đang chạy:

```powershell
uv run celery -A app.core.celery_app.celery_app worker -Q document,notification,maintenance -l info
```

- Nếu bật Beat:

```text
Chỉ một runtime được ENABLE_CELERY_BEAT=true.
```

- Chạy smoke test:

```text
upload PDF thật
generate plan
poll job tới READY
GET learning-progress
PUT progress tới 50%
PUT progress tới >=80%
scan/deliver notification
complete review
```

## 9. Câu Trả Lời Khi Bảo Vệ

Nếu giảng viên hỏi: "Tại sao không tạo lịch ôn tập ngay khi generate sách xong?"

Trả lời:

> Vì generate xong chỉ nghĩa là hệ thống đã có audio, không có nghĩa là user đã học. Nếu tạo spaced review ngay lúc chapter ready thì user có thể bị nhắc ôn một chương họ chưa từng nghe. Vì vậy em neo spaced review vào `chapter_completed_at`, được tạo khi user nghe đủ threshold hoặc bấm hoàn thành thủ công.

Nếu hỏi: "Tại sao phải có outbox?"

Trả lời:

> Outbox giúp tách việc quyết định notification khỏi việc deliver notification. Nếu deliver lỗi, hệ thống vẫn còn record trong DB để retry, debug và đảm bảo idempotency. Đây là pattern production cho workflow bất đồng bộ.

Nếu hỏi: "Redis có giữ dữ liệu business không?"

Trả lời:

> Không. Redis chỉ là broker cho Celery. Dữ liệu business như job status, progress, review schedule, notification đều nằm trong Postgres. Nếu Redis mất queue, FE vẫn đọc được trạng thái từ DB.

Nếu hỏi: "Tại sao tracking theo segment mà completion theo chapter?"

Trả lời:

> Segment giúp resume audio chính xác, còn chapter là đơn vị học và ôn tập hợp lý hơn. User nghe tới segment nào thì FE resume theo segment, nhưng khi đánh giá đã học xong chưa thì backend tính phần trăm của cả chapter.

## 10. Kết Luận

Phase 4.2 đã đạt chất lượng backend tốt cho capstone:

- Đúng business hơn Phase 4.1.
- Có DB schema rõ ràng.
- Có API cho FE.
- Có notification flow.
- Có real-book test.
- Có bug fix dựa trên lỗi thật.

Phần còn lại không phải lỗi của Phase 4.2, mà là các bước production hóa tiếp theo:

```text
Auth thật
Redis/Celery smoke test qua process thật
Progress throttle
Push notification
Quota/cost control
```
