Để tự tin trả lời phỏng vấn từ mức **Middle đến Senior**, bạn không chỉ cần biết Celery là một "công cụ chạy ngầm", mà phải hiểu rõ **bản chất phân tán (Distributed System)**, **luồng dữ liệu (Data Flow)**, **cơ chế đảm bảo tin cậy (Reliability & Idempotency)** và **cách kiến trúc này được áp dụng thực tế trong `triam-backend`**.

Dưới đây là cẩm nang toàn diện được chia làm 4 phần:

1. **Bản chất cốt lõi của Celery (Under the Hood)**
2. **Kiến trúc & Luồng hoạt động thực tế trong Triam-Backend**
3. **Các cạm bẫy kỹ thuật & Cơ chế then chốt (Deep Dive)**
4. **Bộ câu hỏi & câu trả lời phỏng vấn "chuẩn điểm 10"**

---

### PHẦN 1: BẢN CHẤT CỐT LÕI CỦA CELERY LÀ GÌ?

Celery là một **Distributed Task Queue (Hàng đợi tác vụ phân tán)** hoạt động theo mô hình **Producer – Broker – Consumer**:

```
[Producer: FastAPI Web API]
        │
        │ 1. Đẩy message (Task ID, Args) vào queue
        ▼
[Broker: Redis]  <──────── Queue (FIFO / Priority)
        │
        │ 2. Lấy message về thực thi
        ▼
[Consumer: Celery Worker Process Pool]
        │
        │ 3. Ghi trạng thái / kết quả (Job status, Progress)
        ▼
[Database / Result Store: PostgreSQL / Supabase]
```

#### Bản chất kỹ thuật bên dưới:

1. **Message Passing (Không chia sẻ bộ nhớ)**: FastAPI và Celery Worker là **các tiến trình (OS processes) hoàn toàn độc lập**, thậm chí chạy trên các container hoặc máy chủ khác nhau. FastAPI không gọi hàm trực tiếp mà chỉ đóng gói tên hàm và tham số thành một chuỗi JSON (Serialization), rồi đẩy vào Redis.
2. **Broker (Redis)**: Đóng vai trò là "bưu điện". Redis lưu trữ hàng đợi bằng cấu trúc dữ liệu `LIST` (sử dụng các lệnh `LPUSH` để đẩy task vào và `BRPOP` để worker lấy task ra một cách non-blocking/blocking) hoặc `ZSET` cho các task có hẹn giờ (`ETA / countdown`).
3. **Worker Pool (Bộ máy thực thi)**: Celery Worker lắng nghe Redis. Khi có task, một tiến trình con (child process) trong worker pool sẽ nhận message, giải mã (Deserialize), thực thi logic hàm Python, và gửi tín hiệu xác nhận (**ACK - Acknowledgment**) về Broker khi hoàn tất.

---

### PHẦN 2: CELERY TRONG `triam-backend` HOẠT ĐỘNG NHƯ THẾ NÀO?

Trong dự án `triam-backend`, Celery chịu trách nhiệm xử lý các tác vụ **nặng, tốn thời gian (Long-running Tasks)** và **tác vụ định kỳ (Scheduled Tasks)**:

#### 1. Các tác vụ nghiệp vụ chính mà Celery đảm nhận:

- **`generate-plan` (Sinh kế hoạch học tập)**: Gọi AI/LLM để phân tích giáo trình, tạo lộ trình học tập cá nhân hóa (mất từ 10s – 45s).
- **`audio-generation` (Sinh giọng đọc TTS)**: Tạo file âm thanh bài học/từ vựng qua mô hình TTS, sau đó upload lên Supabase Storage (I/O bound + CPU bound).
- **`switch-mode` / `spaced-review`**: Tính toán lại lịch ôn tập ngắt quãng (Spaced Repetition Algorithm: SuperMemo SM-2 / FSRS) cho người học.
- **`reminders` & `notification-outbox`**: Tác vụ định kỳ quét cơ sở dữ liệu để gửi email/thông báo nhắc nhở học tập (chạy qua **Celery Beat**).
- **`orphan-cleanup`**: Quét và dọn dẹp các file audio/tài liệu mồ côi trên Supabase Storage khi user huỷ hoặc xóa sách.

#### 2. Luồng thực thi chi tiết (End-to-End Flow):

```
Client (App/Web)          FastAPI (Producer)           Redis (Broker)         Celery Worker            PostgreSQL (Supabase)
      │                           │                           │                     │                        │
      │── 1. POST /generate-plan ─>│                           │                     │                        │
      │                           │── 2. Tạo Job (PENDING) ──────────────────────────────────────────────────>│
      │                           │── 3. task.delay(job_id) ─>│                     │                        │
      │<─ 4. Trả 202 Accepted ────│                           │                     │                        │
      │      {job_id: "xyz"}      │                           │                     │                        │
      │                                                       │── 5. Worker fetch ─>│                        │
      │                                                       │      message        │── 6. Update: RUNNING ──>│
      │                                                       │                     │      (progress=20%)    │
      │                                                       │                     │── 7. Gọi LLM/Service   │
      │── 8. GET /jobs/xyz (Poll) ──────────────────────────────────────────────────────────────────────────>│ (Trả PENDING/RUNNING)
      │                                                       │                     │── 9. Update: COMPLETED ─>│
      │                                                       │                     │      (lưu kết quả)      │
      │                                                       │<─ 10. Gửi ACK ──────│                        │
      │── 11. GET /jobs/xyz (Poll) ─────────────────────────────────────────────────────────────────────────>│ (Trả kết quả cuối)
```

#### 3. Điểm kiến trúc rất đáng giá trong dự án: **"DB Progress Polling" thay vì Celery Result Backend**

> **Phỏng vấn viên sẽ rất thích điểm này:**
>
> - Celery mặc định hỗ trợ cấu hình `result_backend = "redis://..."`. Nhưng `triam-backend` **chủ động dùng PostgreSQL để theo dõi trạng thái tác vụ**.
> - **Lý do**:
>   1. **Persistence & Relations**: Kết quả nghiệp vụ (kế hoạch học tập, link audio, trạng thái flashcard) cần lưu vĩnh viễn và gắn liền với `user_id`, `book_id` theo quan hệ cơ sở dữ liệu quan hệ, trong khi Redis Result Backend chỉ lưu tạm (TTL) và ở dạng key-value cô lập.
>   2. **Granular Progress**: Dễ dàng cập nhật tiến độ chi tiết (ví dụ: `progress: 10% -> 40% -> 80% -> 100%`) cùng message hiển thị cho người dùng qua cột `status` và `progress` trong bảng DB.
>   3. **Audit & Debug**: Dễ dàng truy vấn log lịch sử xem job nào thất bại, lỗi do đâu (lưu `traceback` vào DB).

---

### PHẦN 3: CÁC CƠ CHẾ KỸ THUẬT THEN CHỐT CỦA CELERY CẦN HIỂU SÂU

#### 1. Concurrency Models: Prefork vs Threads vs Gevent

- **Prefork (Mặc định)**: Celery dùng `multiprocessing` của Python. Mỗi worker process là một tiến trình OS riêng biệt, né được GIL (Global Interpreter Lock). Phù hợp với tác vụ **CPU-bound** (xử lý văn bản, nén file).
- **Gevent / Eventlet hoặc Threads**: Phù hợp với **I/O-bound** (gọi hàng loạt API ngoài, gọi TTS, upload file).
- **Lưu ý về DB Pool trong Prefork**: Không bao giờ được dùng chung Database connection pool giữa các process con sau khi `fork()`. Trong code Celery của dự án, mỗi task khi chạy phải tự mở và đóng DB Session riêng biệt (`with Session(engine) as session:`).

#### 2. Cơ chế đảm bảo tin cậy: `acks_late` & `visibility_timeout`

- Mặc định, Celery gửi `ACK` ngay khi worker **vừa nhận task** (trước khi chạy). Nếu worker đang chạy bị crash (ví dụ: hết RAM OOM), task đó sẽ **mất vĩnh viễn**.
- Để đảm bảo hệ số an toàn cao cho các tác vụ quan trọng, ta cấu hình `task_acks_late = True`: Worker chỉ gửi `ACK` **sau khi hàm đã thực thi xong**. Nếu worker bị crash giữa chừng, Redis broker sẽ tự động đưa task đó cho worker khác chạy lại khi hết thời gian `visibility_timeout`.

#### 3. Idempotency (Tính khả quy) – Nguyên tắc sống còn

- Vì có cơ chế retry và `acks_late`, một task có thể bị thực thi **hơn một lần** (At-least-once delivery).
- **Cách xử lý trong dự án**:
  - Trước khi sinh audio hay sinh plan, task kiểm tra trạng thái trong DB: nếu đã có bản ghi hoặc đã hoàn thành, bỏ qua không tạo lại.
  - Sử dụng database transactions hoặc status checks (`WHERE status = 'PENDING'`) để tránh việc 2 worker cùng chạy đè dữ liệu của nhau.

#### 4. Chống Memory Leak: `--max-tasks-per-child`

- Trong Python, các thư viện xử lý dữ liệu nặng hoặc AI/NLP thường không giải phóng 100% bộ nhớ về OS sau mỗi tác vụ.
- Worker chạy lâu ngày sẽ bị phình RAM (Memory Leak).
- **Giải pháp**: Cấu hình `--max-tasks-per-child=50` (hoặc 100). Sau khi một worker process xử lý xong 50 task, Celery sẽ tự động tắt process đó và khởi động một process mới toanh thay thế.

---

### PHẦN 4: BỘ CÂU HỎI & CÂU TRẢ LỜI PHỎNG VẤN THỰC CHIẾN

Dưới đây là các câu hỏi phỏng vấn thực tế bạn có thể gặp và cách trả lời gãy gọn, chuyên nghiệp:

#### ❓ Câu 1: "Tại sao dự án dùng Celery mà không dùng `BackgroundTasks` có sẵn của FastAPI?"

- **Trả lời**:
  > "`FastAPI.BackgroundTasks` chạy ngay trong cùng tiến trình (in-process) của web server (sử dụng threadpool hoặc event loop). Điều này chỉ phù hợp với các tác vụ siêu nhẹ như bắn email xác thực đơn giản.
  > Đối với `triam-backend`, các tác vụ như gọi LLM sinh kế hoạch (mất 20-30s) hay sinh giọng đọc TTS là các tác vụ nặng:
  >
  > 1. Nếu dùng `BackgroundTasks`, khi traffic tăng cao, web server sẽ bị cạn kiệt CPU/Thread, dẫn đến nghẽn (starvation) các request HTTP thông thường.
  > 2. Nếu container API bị restart hoặc deploy phiên bản mới, toàn bộ task đang chạy ngầm trong in-memory queue của FastAPI sẽ bị mất sạch.
  > 3. Celery tách biệt hoàn toàn tiến trình Web và Worker, có Message Broker (Redis) bảo vệ task trên disk/RAM, cho phép scale độc lập worker và API."

#### ❓ Câu 2: "Broker và Result Backend trong Celery khác nhau như thế nào? Trong dự án bạn cấu hình ra sao?"

- **Trả lời**:
  > "\* **Broker** là hàng đợi trung gian nhận message từ Producer và điều phối cho Worker (ở đây dùng Redis).
  >
  > - **Result Backend** là nơi Celery lưu trữ kết quả trả về của hàm sau khi worker chạy xong (ví dụ: `AsyncResult.get()`).
  >   Trong dự án `triam-backend`, em dùng **Redis làm Broker**, nhưng **không phụ thuộc vào Celery Result Backend** để lưu kết quả nghiệp vụ. Thay vào đó, em thiết kế Worker ghi trực tiếp trạng thái và kết quả vào PostgreSQL (Supabase). Lý do là kết quả cần liên kết quan hệ với các bảng khác (User, Book, Plan), cần lưu vĩnh viễn và cho phép client thực hiện polling tiến độ chi tiết (10%, 50%, 100%)."

#### ❓ Câu 3: "Nếu Celery Worker bị chết đột ngột (OOM, đứt nguồn, kill container) khi đang thực hiện dở một task, hệ thống xử lý thế nào?"

- **Trả lời**:
  > "Mặc định Celery dùng cơ chế _Acknowledge Early_ (gửi ACK ngay khi nhận task), nếu worker chết thì task sẽ bị mất. Để phòng chống việc này:
  >
  > 1. Cấu hình `task_acks_late = True` và `task_reject_on_worker_lost = True`. Worker chỉ gửi ACK sau khi hoàn thành task. Nếu worker bị kill, broker sẽ phát hiện timeout (`visibility_timeout`) và đẩy lại task đó cho worker còn sống khác xử lý.
  > 2. Đi kèm với việc này, task bắt buộc phải thiết kế có tính **Idempotent** (khả quy), để khi chạy lại không tạo ra dữ liệu trùng lặp.
  > 3. Trong DB, ta có thể có một cron job kiểm tra các job có trạng thái `PROCESSING` quá lâu (ví dụ > 10 phút) để đánh dấu `FAILED` hoặc tự động requeue."

#### ❓ Câu 4: "Bạn xử lý lỗi và Retry trong Celery như thế nào?"

- **Trả lời**:
  > "Em sử dụng decorator `@celery_app.task(bind=True, max_retries=3)` kết hợp với `autoretry_for` hoặc gọi `self.retry()`.
  > Để tránh việc worker gọi dồn dập vào API của bên thứ 3 (như OpenAI hay Supabase) khi họ đang bị quá tải, em áp dụng **Exponential Backoff** kèm Jitter:
  > `countdown = 2 ** self.request.retries` (ví dụ: thử lại sau 2s, 4s, 8s...).
  > Nếu đã vượt quá `max_retries`, bắt exception cuối cùng và cập nhật `status = 'FAILED'` cùng nội dung lỗi vào PostgreSQL để báo cho frontend biết."

#### ❓ Câu 5: "Làm sao để chạy các tác vụ định kỳ (Cron job) trong Celery?"

- **Trả lời**:
  > "Dùng **Celery Beat**. Celery Beat là một bộ scheduler riêng biệt. Cứ đến đúng chu kỳ (hoặc theo cú pháp crontab), Beat sẽ gửi một message vào Redis Broker giống hệt như một request bình thường từ FastAPI. Các worker đang rảnh sẽ bốc task đó ra chạy. Trong dự án, Celery Beat được dùng cho: gửi thông báo nhắc học bài hàng ngày, dọn dẹp file rác trên storage và tính toán lại danh sách flashcard cần ôn tập."

#### ❓ Câu 6: "Làm thế nào để scale Celery khi hệ thống có hàng triệu người dùng?"

- **Trả lời**:
  > "Có 3 cấp độ scale:
  >
  > 1. **Horizontal Scaling**: Tăng số lượng Celery Worker container (chỉ cần chỉ trỏ về cùng một Redis Broker).
  > 2. **Task Routing & Multiple Queues**: Chia hàng đợi chuyên biệt thay vì dùng 1 queue `default`. Ví dụ:
  >    - Queue `high_priority`: Dành cho các task phản hồi nhanh cho user (ví dụ: tạo record tức thì).
  >    - Queue `llm_heavy`: Dành cho sinh kế hoạch học tập.
  >    - Queue `tts_audio`: Dành cho render âm thanh.
  >      Worker nào mạnh về CPU sẽ gắn cờ nghe queue `tts_audio`, worker bình thường nghe `high_priority`. Tránh trường hợp task nặng làm nghẽn task nhẹ.
  > 3. **Concurrency tuning**: Tùy chỉnh số lượng worker process (`--concurrency`) dựa trên số lõi CPU của server."

---

### TÓM TẮT KEYWORD ĐỂ HỌC THUỘC TRƯỚC KHI PHỎNG VẤN:

- **Mô hình**: Producer (FastAPI) -> Broker (Redis) -> Consumer (Celery Worker).
- **Pattern**: DB Status Polling (lưu tiến độ vào Postgres thay vì dùng Celery Result Backend).
- **Độ tin cậy**: `acks_late=True`, `visibility_timeout`, `Idempotency`, `Exponential Backoff Retry`.
- **Quản lý tài nguyên**: `--max-tasks-per-child` (tránh rò rỉ RAM), DB Session scope an toàn cho từng task.
