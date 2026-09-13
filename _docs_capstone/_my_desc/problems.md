Để nâng trình độ từ **Junior lên Middle/Senior** và **tự tin "out trình" khi phỏng vấn Backend/AI Engineer**, bạn không nên học dàn trải. Bạn hãy học sâu vào **5 trụ cột kiến trúc cốt lõi ngay trong dự án `triam-backend` này**.

Dưới đây là lộ trình các chủ đề bạn **bắt buộc phải nắm tiếp theo**, kèm theo lý do tại sao nhà tuyển dụng cực kỳ thích hỏi những phần này.

---

### TRỤ CỘT 1: DATABASE & ORM DEEP-DIVE (POSTGRESQL + SQLMODEL)
> 💡 *60% thời lượng phỏng vấn Backend xoay quanh Database. Nếu bạn chỉ biết viết CRUD cơ bản thì chỉ ở mức Fresher/Junior.*

1. **Vấn đề N+1 Query trong SQLModel / SQLAlchemy**:
   * *Nghiệp vụ*: Khi lấy danh sách sách (Books) và các chương (Chapters) hoặc tác giả, code có bị bắn ra $1 + N$ câu truy vấn SQL làm chậm server không?
   * *Phỏng vấn hỏi*: Làm sao phát hiện và tối ưu N+1 query trong SQLAlchemy? (`joinedload` vs `selectinload` khác nhau thế nào?).
2. **Database Indexing & Query Optimization**:
   * Hiểu bản chất B-Tree Index (Composite index, Leftmost prefix rule).
   * Biết đọc lệnh `EXPLAIN ANALYZE` (Seq Scan vs Index Scan vs Index Only Scan).
3. **Transaction & Locking (Concurrency Control)**:
   * **Pessimistic Locking (`SELECT FOR UPDATE`)** vs **Optimistic Locking (dùng `version` column)**: Ví dụ khi 2 request cùng cố gắng cập nhật trạng thái học tập hoặc trừ slot tài khoản cùng 1 mili-giây, làm sao tránh **Race Condition**?
4. **Connection Pooling**:
   * Pool size, Max overflow, Timeout.
   * Tại sao trong container/serverless lại cần PgBouncer?

---

### TRỤ CỘT 2: FASTAPI INTERNALS & ASYNCIO (CÂU HỎI TỬ HUYỆT)
> 💡 *Đây là câu hỏi "bẫy" phổ biến nhất để phân loại ứng viên xem có thực sự hiểu async hay chỉ copy-paste cú pháp.*

1. **Sự khác biệt cốt lõi giữa `async def` và `def` trong FastAPI**:
   * *Bản chất*: Nếu một endpoint viết `async def` nhưng bên trong lại gọi một hàm đồng bộ chặn (blocking I/O như `requests.get` hoặc hàm tính toán nặng), điều gì sẽ xảy ra với Event Loop? (Hệ thống sẽ bị treo toàn bộ!).
   * *FastAPI xử lý thế nào*: Hàm `def` thường được FastAPI đẩy vào một threadpool riêng (`anyio/starlette worker threads`), còn `async def` chạy trực tiếp trên main Event Loop.
2. **Vòng đời của Database Session qua Dependency Injection (`Depends`)**:
   * Làm sao đảm bảo mỗi HTTP request có một DB Session riêng, commit khi thành công và tự động rollback/close khi có exception?

---

### TRỤ CỘT 3: REDIS & CÁC PATTERN HỆ THỐNG PHÂN TÁN (DISTRIBUTED PATTERNS)
> 💡 *Celery chỉ là một ứng dụng của Redis. Redis còn làm được rất nhiều thứ mà Senior Engineer phải biết.*

1. **Cache Strategies & Cạm bẫy kinh điển**:
   * **Cache-Aside Pattern**: Luồng đọc/ghi cache chuẩn.
   * **Cache Stampede (Dog-piling)**: Khi một key cache bị hết hạn (TTL expire) ngay lúc có 10.000 user cùng truy cập, làm sao không để Database bị sập?
   * **Cache Penetration** (truy vấn key không tồn tại) & **Cache Avalanche** (hàng loạt key cùng hết hạn một lúc).
2. **Distributed Lock (Khóa phân tán với Redis)**:
   * Lệnh `SET key uuid NX EX 10` dùng để làm gì?
   * Tại sao cần khóa phân tán khi có nhiều Celery worker cùng tranh chấp xử lý tài nguyên của một người dùng?
3. **Rate Limiting (Giới hạn tốc độ gọi API)**:
   * Thuật toán Token Bucket hoặc Sliding Window dùng Redis để chặn spam API sinh kế hoạch / sinh audio.

---

### TRỤ CỘT 4: RAG & AI AGENT ARCHITECTURE (VŨ KHÍ ĐẶC BIỆT CỦA TRIAM)
> 💡 *Triam là một ứng dụng học tập thông minh có RAG, LLM và Realtime Voice. Đây là "điểm sáng ăn tiền" nhất trên CV của bạn so với các ứng viên backend truyền thống.*

1. **RAG Pipeline & Vector Search**:
   * Cơ chế Ingestion: Document chunking (Recursive Character Text Splitter), Overlap size tại sao quan trọng?
   * Vector Index trong Postgres (`pgvector`): Sự khác nhau giữa **IVFFlat** và **HNSW** (Hierarchical Navigable Small World).
   * **Hybrid Search**: Kết hợp Semantic Search (Vector) + Keyword Search (Full-text search BM25) để tránh hallucination khi tra cứu thuật ngữ chuyên ngành.
2. **Tối ưu độ trễ cho AI / Voice Agent (TTFT - Time To First Token)**:
   * Streaming response (Server-Sent Events - SSE) thay vì đợi LLM sinh hết toàn bộ câu trả lời.
   * Kiến trúc Realtime Voice (WebRTC / LiveKit) truyền nhận âm thanh full-duplex 2 chiều.
3. **Grounding & Guardrails (Chống ảo giác - Hallucination)**:
   * Làm sao ép model chỉ trả lời dựa trên sách giáo trình/tài liệu được cung cấp (system prompt, fallback logic, RAG evaluation metrics).

---

### TRỤ CỘT 5: OBSERVABILITY, TESTING & DOCKER PRODUCTION
> 💡 *Senior không chỉ viết code chạy được, mà còn phải đảm bảo hệ thống sống sót trên Production.*

1. **Graceful Shutdown**:
   * Khi server bị stop/restart để deploy code mới, làm sao để web server và Celery worker đợi xử lý xong các request/task đang dở trước khi tắt hẳn?
2. **TDD & Mocking trong Testing**:
   * Viết Unit test và Integration test với `pytest`, `pytest-asyncio`.
   * Cách mock các 3rd-party services (gọi OpenAI, gọi Supabase Storage) để test chạy độc lập không tốn tiền API.
3. **Docker Multi-stage Build & tối ưu Image size**:
   * Giảm dung lượng Docker image từ 2GB xuống 300MB với `uv` hoặc poetry.

---

### BÂY GIỜ CHÚNG TA NÊN BẮT ĐẦU TỪ ĐÂU?

Để học nhanh và chắc nhất, bạn hãy chọn **1 trong 3 hướng** sau đây để chúng ta mổ xẻ tiếp theo:

1. **Lựa chọn 1 (Ưu tiên số 1 cho Backend Core)**: Đi sâu vào **Database & Async FastAPI** (N+1 Query, Locking, Tránh lỗi treo Event Loop khi dùng `async def`).
2. **Lựa chọn 2 (Ưu tiên cho System Design)**: Đi sâu vào **Redis & Distributed Patterns** (Cache Stampede, Distributed Lock `Redlock`, Rate Limiter).
3. **Lựa chọn 3 (Ưu tiên nâng tầm AI Backend)**: Đi sâu vào **RAG & Vector Search trong PostgreSQL** (pgvector, HNSW index, Hybrid Search và kiểm soát Hallucination).
