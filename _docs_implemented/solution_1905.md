Anh đã đọc lại flow code hiện tại và research thêm official docs. Anh chưa sửa code.

**Nhận Định Chính**
Vấn đề lớn nhất của dự án không nằm ở PDF parser nữa, mà nằm ở **pipeline xử lý sách đang là fire-and-forget**, chưa có job/progress model rõ ràng, và `normalize_text_for_speech()` đang xử lý **nguyên chapter bằng 1 LLM call**. Với sách/chapter lớn, hệ thống sẽ dễ gặp: vượt context, rate limit TPM/RPM, latency dài, lỗi khó retry, FE không biết tiến độ, và user phải đợi quá lâu trước khi nghe được.

FastAPI docs cũng nói rõ `BackgroundTasks` hợp với việc nhỏ trong cùng process; nếu task nặng, đa bước, cần retry/progress/durable thì nên dùng queue như Celery hoặc công cụ tương đương. Celery/RQ có model job state/progress/retry tốt hơn cho production.

**Về Upload Và Limit Theo User**
Hiện tại hệ thống mới có `MAX_FILE_SIZE_BYTES` theo file, chưa có quota theo tài khoản. Dự án thực tế nên có ít nhất:

- `max_books_per_user`
- `max_storage_bytes_per_user`
- `max_pages_or_chapters_per_book`
- `max_tokens_per_chapter`
- `max_active_processing_jobs`
- `monthly_llm_tokens` hoặc `monthly_audio_minutes`

Nên validate theo 2 tầng:

1. Trước upload: file type, file size, số job đang chạy của user.
2. Sau parse outline/text: số chapter, token estimate từng chapter, tổng token sách.

Nếu chapter vượt hard limit của model normalize thì có thể trả `422` rõ ràng: “Chương X quá dài, vui lòng tách tài liệu”. Nhưng anh không khuyên reject mọi chapter hơi lớn. Nên có ngưỡng mềm để chunk, và ngưỡng cứng mới reject.

**Full Và Pareto**
`full` không nên hiểu là “giữ nguyên từng chữ”. Với TTS, nó nên là: giữ đủ ý, đủ trình tự, đủ luận điểm, nhưng rewrite sang văn nói.

`pareto` là mode học nhanh theo 80/20: chọn phần kiến thức có tác động học tập cao nhất, ví dụ định nghĩa, công thức, luận điểm chính, keyword, kết luận, mối quan hệ nhân quả. Vấn đề là hiện tại dự án chỉ đổi system prompt, nên chất lượng Pareto chưa đảm bảo. Prompt-only là chưa đủ cho sản phẩm thật.

Giải pháp tốt hơn:

- Bước 1: extract “knowledge atoms” từ chapter: ý chính, định nghĩa, ví dụ, công thức, keyword.
- Bước 2: chấm điểm importance theo rubric.
- Bước 3: Pareto chỉ compose từ các atom điểm cao.
- Bước 4: lưu metadata để debug: vì sao ý này được chọn, source chapter/section nào.

Như vậy Pareto có thể kiểm soát được, không phải “LLM tự cảm thấy cái gì quan trọng”.

**Vấn Đề Normalize Chapter Quá Lớn**
Code hiện tại trong [app/services/llm_service.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/llm_service.py) gọi LLM một lần với toàn bộ `raw_text`. Đây là rủi ro cao.

Nên chuyển sang pipeline phân cấp:

1. Token estimate trước khi gọi LLM.
2. Nếu dưới limit: xử lý bình thường.
3. Nếu trên limit mềm: chia theo section/paragraph, không chia “bằng cơm” theo ký tự.
4. Tạo chapter brief trước: mục tiêu chương, thuật ngữ chính, outline.
5. Rewrite từng chunk với `chapter_brief + previous_tail`.
6. Stitch/QA lại để đảm bảo liền mạch.
7. Nếu vượt limit cứng: reject ngay.

Nguồn official Gemini nói nên dùng `count_tokens` trước request để kiểm tra kích thước input, và rate limit bị tính theo RPM/TPM/RPD. Đây đúng là thứ mình cần đưa vào pipeline.

**Progress Cho FE**
Anh đề xuất 2 giải pháp phù hợp nhất.

Giải pháp 1, đơn giản và chắc: **DB progress + polling endpoint**.

Thêm bảng kiểu `processing_jobs` hoặc mở rộng model hiện tại:

- `job_id`
- `user_id`
- `book_id`
- `job_type`: upload/generate_plan/switch_mode
- `mode`
- `status`: queued/processing/partial_ready/ready/error
- `total_units`
- `done_units`
- `failed_units`
- `progress_percent`
- `current_step`
- `error_message`

FE gọi:

```text
GET /api/v1/books/{book_id}/processing-status
```

Polling mỗi 2-5 giây. Cách này dễ debug, reload app không mất trạng thái, phù hợp capstone nhất.

Giải pháp 2, UX tốt hơn: **Supabase Realtime hoặc Broadcast + polling fallback**.

BE update `books`, `chapters`, `processing_jobs`, FE subscribe realtime. Supabase docs support listen Postgres changes, nhưng realtime không nên là nguồn dữ liệu duy nhất vì có thể miss event khi client disconnect. Vì vậy vẫn cần endpoint polling/status làm source of truth.

LiveKit DataChannel không nên dùng cho progress upload/gen audio dài hạn. LiveKit packet reliable vẫn là best-effort, có size limit khoảng 15KiB, hợp chat/realtime room hơn là trạng thái background job.

**Gen 50% Audio Trước**
Anh sẽ đổi tư duy từ “gen đúng 50% rồi unlock” thành **first playable content**.

Flow tốt hơn:

1. Sau `/generate-plan`, tạo job.
2. Worker xử lý chapter theo thứ tự, ưu tiên chapter đầu.
3. Khi chapter/segment đầu tiên ready, FE đã có thể unlock nghe.
4. Khi đạt 50% số chapter hoặc 50% estimated duration thì mark `PARTIAL_READY`.
5. Worker tiếp tục gen phần còn lại, FE không cần chờ.
6. FE gọi playlist endpoint chỉ lấy segment đã `ready`.

Nên có status mới:

```text
book.status = draft | processing | partial_ready | ready | error
chapter.status = draft | normalizing | tts_processing | ready | error
segment.status = pending | ready | error
```

Hiện tại `ChapterSegment` chưa có `status`, nên khó biết audio nào đã nghe được an toàn.

**Vấn Đề Liên Quan Cần Fix**

- `BackgroundTasks` hiện chưa durable. Server restart là mất job.
- `asyncio.gather()` xử lý nhiều chapter cùng lúc nhưng không ưu tiên “chapter đầu nghe trước”.
- Semaphore hiện chung cho cả RAG/TTS/LLM. Nên tách limiter riêng: `llm`, `tts`, `embedding`, `storage`.
- `tts_worker.py` đang warning nếu segment TTS lỗi rồi vẫn có thể lưu các segment còn lại. Với audiobook, thiếu segment là lỗi nghiêm trọng, nên chapter phải `ERROR` hoặc retry.
- `switch-mode` cần job/progress riêng, không chỉ bắn background task.
- Cần idempotency: chạy lại job không tạo duplicate segment/audio.
- Cần lưu token/audio usage để tính chi phí.
- Cần auth thật thay `MOCK_USER_ID` trước khi quota có ý nghĩa.
- Nên lưu `document_stats`: file_size, document_type, total_chapters, estimated_tokens, estimated_audio_minutes.

**Recommendation Của Anh**
Cho đồ án hiện tại, anh khuyên làm theo thứ tự:

1. Thêm `processing_jobs` + endpoint progress polling.
2. Thêm `PARTIAL_READY` và segment/chapter progress.
3. Thêm token validation trước normalize.
4. Refactor normalize sang hierarchical chunking.
5. Ưu tiên gen first playable content theo thứ tự chapter.
6. Sau đó mới cân nhắc Celery/RQ nếu muốn production hơn.

Nếu cần production thật, anh chọn **RQ hoặc Celery + Redis + DB progress table**. Nếu muốn ít hạ tầng hơn cho capstone, cứ dùng DB progress + FastAPI background trước, nhưng phải chấp nhận chưa durable khi server restart.

**Nguồn Tham Khảo**

- [FastAPI BackgroundTasks caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Celery task states/retry/progress](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [RQ job status/meta](https://python-rq.org/docs/jobs/)
- [Gemini token counting](https://ai.google.dev/gemini-api/docs/tokens)
- [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Supabase Realtime Postgres Changes](https://supabase.com/docs/guides/realtime/postgres-changes)
- [LiveKit data packet limits](https://docs.livekit.io/transport/data/packets/)
