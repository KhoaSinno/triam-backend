Chào bạn. Đánh giá lược đồ cơ sở dữ liệu hiện tại và các luồng logic bạn vừa cấu trúc lại, tôi thấy bạn đã có một nền tảng tư duy rất tốt. Tuy nhiên, để đồ án hệ thống thông tin này đạt chuẩn Production, đáp ứng được luồng chạy ngầm phức tạp và khả năng scale (mở rộng), chúng ta cần chuẩn hóa (Normalize) lại một số điểm cốt lõi.

Điểm yếu lớn nhất ở schema cũ là **thiếu tính cá nhân hóa** (chưa có định danh người dùng) và **chưa lưu trữ cấu hình kế hoạch học tập** (Reading Plan) như đã thống nhất trong luồng xử lý.

Dưới đây là bản thiết kế Database chuẩn hóa trên PostgreSQL (Supabase), tối ưu hóa tốc độ truy vấn cho kiến trúc Decoupling mà chúng ta vừa vạch ra.

### 1. Nhóm Dữ liệu Cốt lõi & Cá nhân hóa

Hệ thống trợ lý ảo phục vụ khai thác tri thức cá nhân bắt buộc phải có sự phân quyền dữ liệu.

- **Bảng `books` (Quản lý file gốc)**
  - `id` (uuid, Primary Key)
  - `user_id` (uuid, Foreign Key trỏ về bảng `auth.users` của Supabase) - _Bắt buộc để bảo mật._
  - `title` (text)
  - `author` (text, nullable)
  - `source_file_url` (text) - Đường dẫn file PDF trên Supabase Storage.
  - `total_chapters` (int4)
  - `status` (varchar) - Chỉ nhận các giá trị: `DRAFT`, `PROCESSING`, `READY`, `ERROR`.
  - `created_at` (timestamptz)

- **Bảng `reading_plans` (Quản lý lộ trình học)**
  - `id` (uuid, Primary Key)
  - `book_id` (uuid, Foreign Key -> `books.id`)
  - `mode` (varchar) - `FULL_MODE` hoặc `PARETO_MODE`.
  - `pace` (int4) - Số chương một ngày.
  - `schedule_config` (JSONB) - Lưu lịch học dạng mảng, ví dụ `["Mon", "Wed", "Fri"]`. Việc dùng `JSONB` ở đây giúp dễ dàng thêm các option như language hay tốc độ đọc sau này mà không cần gỡ tung DB ra sửa đổi.
  - `status` (varchar) - `ACTIVE`, `PAUSED`, `COMPLETED`.
  - `created_at` (timestamptz)

### 2. Nhóm Dữ liệu Tiêu thụ (Audio / Playlist)

Đảm bảo trải nghiệm nghe mượt mà giống Youtube, load từng phần nhỏ.

- **Bảng `chapters` (Cấu trúc mục lục)**
  - `id` (uuid, Primary Key)
  - `book_id` (uuid, Foreign Key -> `books.id`)
  - `chapter_index` (int4) - Dùng để sắp xếp thứ tự phát.
  - `title` (text)
  - `review_text` (text) - Nội dung tóm tắt để ôn tập.
  - `review_audio_url` (text)
  - `status` (varchar)

- **Bảng `chapter_segments` (Các đoạn audio nhỏ)**
  - `id` (bigserial, Primary Key)
  - `chapter_id` (uuid, Foreign Key -> `chapters.id`) - _Liên kết trực tiếp với UUID của chapter thay vì index._
  - `segment_index` (int4)
  - `text_content` (text)
  - `audio_url` (text)
  - **`duration_ms` (int4)** - _[Senior Tip]_ Bạn PHẢI thêm trường này. Khi Flutter load danh sách phát, nếu có sẵn `duration` từ DB, app có thể hiển thị độ dài audio (ví dụ 03:15) ngay lập tức mà không cần tải file `.mp3` về để đo lường. Điều này tối ưu UI/UX cực kỳ lớn.

### 3. Nhóm Dữ liệu Khai thác (Vector RAG)

Bảng này sẽ bị query với cường độ rất cao khi user kích hoạt Live Assistant.

- **Bảng `book_knowledge` (Kho tri thức Vector)**
  - `id` (bigserial, Primary Key)
  - `book_id` (uuid, Foreign Key -> `books.id`)
  - `chapter_id` (uuid, Foreign Key -> `chapters.id`) - _Sửa đổi so với thiết kế cũ để đảm bảo tính toàn vẹn dữ liệu (Referential Integrity)._
  - `chunk_index` (int4)
  - `content` (text)
  - `embedding` (vector(1536)) - Assuming bạn dùng `text-embedding-3-small`.

---

### Bí quyết tối ưu Hiệu suất (Performance Tuning) cho Supabase

1.  **Index HNSW cho Vector (Sống còn):** Bảng `book_knowledge` sẽ lưu hàng ngàn vector. Hàm RPC tìm kiếm sẽ rất chậm nếu chạy quét toàn bảng (Full Table Scan). Bạn phải chạy lệnh SQL này trong Supabase SQL Editor để tạo index:
    ```sql
    CREATE INDEX ON book_knowledge USING hnsw (embedding vector_cosine_ops);
    ```
2.  **Bật Row Level Security (RLS):** Dữ liệu tri thức số cá nhân rất nhạy cảm. Bạn cần cấu hình RLS trên bảng `books` và `reading_plans` để đảm bảo `user_id_A` không bao giờ gọi API đọc trộm được tài liệu hay script của `user_id_B`.
3.  **Tạo Composite Index:** Khi RAG hoạt động, nó thường tìm kiếm kết hợp giữa `book_id` và vector similarity. Hãy tạo một index phụ (B-Tree) cho cột `book_id` trên bảng `book_knowledge` để Postgres thu hẹp phạm vi cuốn sách trong tích tắc trước khi tính toán độ tương đồng.

Bản thiết kế này đã khóa chặt các rủi ro về mặt kiến trúc. Tiếp theo, bạn muốn chúng ta viết trực tiếp hàm RPC PostgreSQL (`match_book_knowledge`) để tối ưu tìm kiếm RAG, hay bạn muốn đi vào việc cấu hình Background Tasks của FastAPI để handle việc ghi dữ liệu vào các bảng mới này?
