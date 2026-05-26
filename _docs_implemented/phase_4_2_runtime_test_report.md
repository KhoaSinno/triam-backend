# Phase 4.2 Runtime Test Report - Production Learning Loop Guardrails

Ngày test: 2026-05-25

## Mục tiêu test

Phase 4.2 cần chứng minh các business rule sau hoạt động đúng:

- FE cập nhật tiến độ nghe theo chapter/segment.
- Chapter chỉ tạo spaced review sau khi user học đủ ngưỡng hoàn thành.
- Ngưỡng hiện tại: `LEARNING_COMPLETION_THRESHOLD_PERCENT=80`.
- Review schedule neo theo `chapter_completed_at + interval_days`.
- User có thể resume đúng `segment_id`, `segment_index`, `position_ms`.
- Notification outbox tạo và deliver in-app được cho:
  - spaced review due
  - first playable
  - book ready
- Manual complete/skip review hoạt động qua API.
- Legacy `chapter.review_text` dạng plain text không làm API progress bị 500.

## Kết quả code-level

Đã implement các nhóm chính:

- `ChapterLearningProgress`: lưu tiến độ học theo `user_id + chapter_id + mode`.
- `ReadingPlanScheduleSlot`: giữ slot lịch học active, phục vụ conflict detection và giới hạn sách đang học.
- `SpacedReviewItem` production anchor:
  - `anchor_completed_at`
  - `source_progress_id`
  - `notified_at`
  - `last_reviewed_at`
- API mới:
  - `PUT /api/v1/books/{book_id}/chapters/{chapter_id}/progress`
  - `POST /api/v1/books/{book_id}/chapters/{chapter_id}/complete`
  - `GET /api/v1/books/{book_id}/learning-progress`
  - `POST /api/v1/reviews/{review_item_id}/complete`
  - `POST /api/v1/reviews/{review_item_id}/skip`
- Notification event production logic:
  - plan reminder chỉ nhắc khi còn playable chapter chưa completed
  - plan reminder không nhắc nếu user đã học sách đó trong ngày
  - spaced review chỉ gửi nếu chapter progress đã completed
  - content ready gom theo `first_playable` và `book_ready`

## Migration

Đã chạy:

```powershell
uv run alembic upgrade head
```

Kết quả:

```text
Running upgrade e4f7a9c2d1b0 -> f6a8c2d4e9b1, phase 4.2 learning progress
```

## Automated tests

### Phase 4.2 focused tests

```powershell
uv run pytest tests/test_phase4_2_learning_loop.py -q
```

Kết quả:

```text
5 passed in 36.11s
```

### Main non-live suite

```powershell
uv run pytest -q --ignore=tests/test_agent_chat_text_only.py --ignore=tests/test_threads_for_book.py
```

Kết quả:

```text
40 passed in 76.25s
```

### Live server integration: threads for book

Anh bật FastAPI tạm trên `127.0.0.1:8000`, chạy:

```powershell
uv run pytest tests/test_threads_for_book.py -q
```

Kết quả:

```text
6 passed in 24.15s
```

Log server:

```text
logs/phase4_2_uvicorn_threads.out.log
logs/phase4_2_uvicorn_threads.err.log
logs/phase4_2_threads_pytest.log
```

### Ruff

Chạy ruff trên toàn bộ file Phase 4.2 đã thêm/sửa:

```powershell
uv run ruff check <phase-4.2-touched-files>
```

Kết quả:

```text
All checks passed!
```

Ghi chú: `uv run ruff check app tests` toàn repo vẫn còn lint debt cũ ở migration/test realtime thủ công, không thuộc Phase 4.2.

## Runtime flow với dữ liệu thật

Runtime flow đã seed dữ liệu thật vào DB local bằng một runtime user riêng:

```json
{
  "runtime_user_id": "2cf03fcf-7fc0-4b38-9cb2-55fb618780d9",
  "book_id": "7caf6f2f-90b6-4c32-98a4-15cd99caaae1",
  "chapter_id": "83f2c497-fdb7-4f99-99b9-c5e32b1ea671",
  "segment_id": 1823
}
```

File log đầy đủ:

```text
logs/phase4_2_runtime_flow.json
```

Các bước đã đi qua:

1. Seed book/chapter/segment thật.
2. Gọi API progress 50%.
3. Verify chưa tạo review.
4. Gọi API progress 82%.
5. Verify chapter completed và tạo 5 review intervals.
6. Force review đầu tiên due.
7. Chạy `scan_due_notifications_task()`.
8. Chạy `deliver_due_notifications_task()`.
9. Gọi API notifications để verify in-app notification.
10. Gọi API complete review.
11. Tạo content-ready outbox `first_playable` và `book_ready`.
12. Deliver content-ready outbox.

Log worker/task quan trọng:

```text
Notification scan done | created=1 | recovered=0 | should_deliver=True
Notification delivery batch done | delivered_attempts=1
Notification delivery batch done | delivered_attempts=2
```

Kết quả chính:

```json
{
  "reviews_after_50": 0,
  "progress_82": {
    "progress_percent": 82,
    "max_progress_percent": 82,
    "status": "completed"
  },
  "book_progress": {
    "book_progress_percent": 82,
    "completed_chapters": 1,
    "playable_chapters": 1,
    "last_segment_id": 1823,
    "position_ms": 82000
  },
  "review_count_after_completion": 5,
  "review_intervals": [1, 3, 7, 14, 30],
  "spaced_review_outboxes_for_book": [
    {
      "type": "spaced_review_due",
      "status": "sent",
      "interval_days": 1
    }
  ],
  "content_ready_outboxes_for_book": [
    {
      "status": "sent",
      "subtype": "book_ready"
    },
    {
      "status": "sent",
      "subtype": "first_playable"
    }
  ],
  "final_review_status": "completed",
  "final_progress_status": "completed"
}
```

## Vấn đề phát hiện trong lúc test và đã fix

### Legacy review_text plain text

Trong runtime test, `chapter.review_text` dạng plain text làm completion API fail vì code cũ chỉ chấp nhận JSON theo mode.

Fix:

- Nếu `review_text` parse được JSON object, lấy theo `mode`.
- Nếu là plain text legacy, dùng trực tiếp text đó làm review snapshot.
- Không để user bị lỗi 500 khi họ vừa đạt mốc hoàn thành chapter.

Test bảo vệ:

```text
test_learning_progress_accepts_legacy_plain_review_text
```

### Notification settings legacy daily_cap

DB local có row cũ `daily_cap=50`, trong khi DTO response giới hạn `<=10`, làm API settings có thể fail response validation.

Fix:

- Repository tự normalize `daily_cap` về khoảng `0..10` khi đọc settings.
- Đây là dạng self-healing cho dữ liệu cũ, tránh 500 sau deploy.

### Test outbox phụ thuộc DB sạch

`test_claim_and_deliver_in_app_outbox_once` trước đó có thể claim thêm pending outbox rác trong DB thật.

Fix:

- Test claim `limit=1`.
- Outbox test dùng `due_at=2000-01-01` để deterministic trên DB không sạch.

## Ghi chú deploy

Phase 4.2 không yêu cầu thêm worker queue mới. Nó dùng lại:

- `maintenance`: scan due notifications
- `notification`: deliver due notifications

Các biến `.env.example` đã có default Phase 4.2:

```env
MAX_ACTIVE_LEARNING_BOOKS_PER_USER=3
LEARNING_COMPLETION_THRESHOLD_PERCENT=80
LEARNING_PROGRESS_STALE_SECONDS=30
PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS=24
```

Khi deploy thật, nhớ migrate DB trước khi test FE:

```powershell
uv run alembic upgrade head
```

## Kết luận

Phase 4.2 đã đạt điều kiện merge về mặt backend:

- Unit/API tests pass.
- Server integration threads pass khi bật FastAPI.
- Runtime learning loop pass với DB thật.
- Notification outbox deliver được đúng loại event.
- Progress/resume/review complete đúng logic production.

Các test realtime LiveKit agent vẫn là nhóm live/manual test riêng vì cần server + agent worker + LiveKit session thật, không nên coi là unit regression của Phase 4.2.

## Real Book Full Flow - Chương 4 PDF

Sau khi review lại, anh test thêm đúng file thật của dự án:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

Log đầy đủ:

```text
logs/phase4_2_real_book_full_flow.json
logs/phase4_2_real_book_learning_flow.json
```

### Preflight Parser

Parser đọc được hidden outline và text:

```text
chapters=3
chapter=1 title='Chương 4: Phương pháp luận nghiên cứu' chars=3552 estimated_tokens=1680
chapter=2 title='Chương 5: Kết quả phân tích và so sánh' chars=16337 estimated_tokens=7795
chapter=3 title='Chương 6: Bàn luận và Khuyến nghị' chars=14625 estimated_tokens=6978
```

### Upload + Generate Plan + Worker Pipeline

Flow đã chạy:

1. `POST /api/v1/upload` với PDF thật.
2. `POST /api/v1/generate-plan`.
3. Chạy cùng entrypoint worker `process_book_task(book_id, "full", job_id)`.
4. Worker download lại file từ Supabase Storage.
5. Worker chạy RAG embedding + LLM normalize + TTS + upload audio.
6. Worker tạo content-ready outbox.
7. Book/job/chapter chuyển `ready`.

Book thật đã xử lý:

```json
{
  "book_id": "4ff2cfd8-029d-46e0-baae-15ba634c9f21",
  "status": "ready",
  "document_type": "pdf",
  "total_chapters": 3
}
```

Job:

```json
{
  "status": "ready",
  "progress_percent": 100,
  "total_units": 3,
  "done_units": 3,
  "failed_units": 0,
  "estimated_input_tokens": 16453,
  "estimated_audio_seconds": 3382,
  "error_message": null
}
```

Generated content:

```json
{
  "total_segments": 99,
  "total_knowledge_chunks": 35,
  "chapters": [
    {
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "status": "ready",
      "segments": 11,
      "knowledge_chunks": 4,
      "review_text_present": true,
      "review_audio_present": true
    },
    {
      "title": "Chương 5: Kết quả phân tích và so sánh",
      "status": "ready",
      "segments": 38,
      "knowledge_chunks": 16,
      "review_text_present": true,
      "review_audio_present": true
    },
    {
      "title": "Chương 6: Bàn luận và Khuyến nghị",
      "status": "ready",
      "segments": 50,
      "knowledge_chunks": 15,
      "review_text_present": true,
      "review_audio_present": true
    }
  ]
}
```

Worker log quan trọng:

```text
PDF uploaded to Storage: 4ff2cfd8-029d-46e0-baae-15ba634c9f21/original.pdf
ReadingPlan created for book 4ff2cfd8-029d-46e0-baae-15ba634c9f21 | mode=full
Chapter 1 READY | mode=full | segments=11
Chapter 2 READY | mode=full | segments=38
Chapter 3 READY | mode=full | segments=50
Content-ready first-playable event | created=True
Content-ready book-ready event | created=True
Book 4ff2cfd8-029d-46e0-baae-15ba634c9f21 READY
```

### Learning Progress With Real Generated Segments

Sau khi book thật ready, anh test tiếp progress bằng chính segment duration thật.

Kết quả:

```json
{
  "reviews_after_50": 0,
  "progress_82_payload_result": {
    "progress_percent": 81,
    "max_progress_percent": 81,
    "status": "completed"
  },
  "review_intervals": [1, 3, 7, 14, 30],
  "final_review_status": "completed",
  "final_progress_status": "completed"
}
```

Ghi chú: request test nhắm mốc 82%, nhưng backend tính theo tổng duration thật của chapter rồi ép `int`, nên response là `81`. Vì ngưỡng hoàn thành là `80`, trạng thái `completed` là đúng.

Notification outbox/user notification:

```json
{
  "outboxes_for_book": [
    {
      "type": "content_ready",
      "status": "sent",
      "subtype": "first_playable"
    },
    {
      "type": "content_ready",
      "status": "sent",
      "subtype": "book_ready"
    },
    {
      "type": "spaced_review_due",
      "status": "sent",
      "interval_days": 1
    }
  ],
  "user_notifications_for_book": [
    {
      "type": "content_ready",
      "title": "Có thể bắt đầu nghe rồi"
    },
    {
      "type": "spaced_review_due",
      "title": "Đến lúc ôn lại rồi"
    },
    {
      "type": "content_ready",
      "title": "Sách đã sẵn sàng"
    }
  ]
}
```

### Real Book Conclusion

Real-book test đã hoàn thành đúng plan:

- PDF thật upload được.
- Parser outline đúng.
- Generate plan thành công.
- Worker xử lý đủ 3 chương.
- Audio segments/review audio được tạo.
- RAG knowledge chunks được tạo.
- Job/book/chapter status đúng.
- Content-ready notification đúng.
- Learning progress/resume đúng theo segment thật.
- Spaced review chỉ tạo sau khi chapter completed.
- Review complete API hoạt động.

Không phát hiện bug code mới trong Phase 4.2 sau real-book test.
