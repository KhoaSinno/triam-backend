# Báo cáo Đặc tả Các Phương thức Chức năng CSDL (TRIAM Domain Class Methods Specification)

Tài liệu này đặc tả chi tiết và đầy đủ nhất các phương thức nghiệp vụ cốt lõi (Domain Methods) tương ứng với từng bảng/thực thể trong sơ đồ lớp của hệ thống **TRIAM Backend**. Các phương thức CRUD cơ bản (Create, Read, Update, Delete) được lược bỏ để tập trung vào các luồng xử lý logic phức tạp, giải thuật AI, lập lịch thông báo và xử lý đồng bộ tiến trình học tập.

---

## 1. Phân hệ Người dùng & Cấu hình (User, Security & Config)

### 1.1 Thực thể `User` (Người dùng)

* **`login()` / `logout()`**
  * **Mô tả**: Đồng bộ trạng thái phiên làm việc của người dùng từ hệ thống định danh của Supabase Auth.
* **`verify_auth_session()`**
  * **Mô tả**: Xác thực mã JWT token nhận từ Client gửi lên trong mỗi request API để trích xuất `user_id` và xác thực quyền truy cập.

### 1.2 Thực thể `AdminUser` (Admin)

* **`can_access_admin()`**
  * **Mô tả**: Kiểm tra xem tài khoản người dùng có quyền quản trị viên đang hoạt động (`role = 'admin'` và `is_active = True`).
* **`revoke_admin_access()`**
  * **Mô tả**: Thu hồi quyền truy cập admin của một người dùng, lưu vết thời điểm thu hồi và tài khoản thực hiện thu hồi.

### 1.3 Thực thể `NotificationSettings` (Cấu hình nhắc nhở)

* **`get_or_create_notification_settings()`**
  * **Mô tả**: Truy xuất cài đặt thông báo của người dùng. Nếu chưa tồn tại (ví dụ: người dùng mới đăng ký), hệ thống tự động sinh cấu hình mặc định (Múi giờ `"Asia/Ho_Chi_Minh"`, Giờ học `"20:00"`, daily cap = 3).
* **`validate_daily_cap()`**
  * **Mô tả**: Đảm bảo số lượng thông báo được thiết lập của người dùng nằm trong khoảng an toàn (ví dụ: tối thiểu là 0, tối đa là 10) trước khi cập nhật.

---

## 2. Phân hệ Tài liệu & RAG Engine (Documents & RAG)

### 2.1 Thực thể `Book` (Sách/Tài liệu)

* **`parse_and_extract_structure()`**
  * **Mô tả**: Trích xuất cấu trúc mục lục và nội dung văn bản thô từ tệp tin tải lên (PDF, EPUB, DOCX) thành các nút cây thư mục `BookSection`.
  * **Ví dụ thực tế**: Khi người dùng tải lên cuốn sách EPUB *Harry Potter*, phương thức này quét tệp tin mục lục điều hướng `toc.ncx`, tìm ra các chương, ánh xạ chúng thành danh sách `BookSection` có phân cấp (level) tương ứng.
* **`delete_book_and_assets()`**
  * **Mô tả**: Xóa sách khỏi hệ thống và thực hiện dọn dẹp an toàn các tệp tin âm thanh trên kho lưu trữ đám mây (Supabase Storage).
  * **Quy tắc nghiệp vụ**: Kiểm tra trường `parent_shared_id`. Nếu sách này được tạo bằng cách Clone (chia sẻ chung), hệ thống chỉ xóa các bản ghi liên kết CSDL cá nhân và **không xóa tệp tin vật lý** trên Storage vì chúng đang được dùng chung cho các người dùng khác.

### 2.2 Thực thể `BookSection` (Chương/Đề mục)

* **`generate_sections_outline()`**
  * **Mô tả**: Sắp xếp các chương phẳng từ DB thành một cây thư mục phân cấp (TOC Tree) dựa vào trường `path` và `level`.
  * **Ví dụ thực tế**: Chuyển đổi các hàng cơ sở dữ liệu phẳng có path: `1`, `1.1`, `1.2`, `1.2.1` thành một cấu trúc JSON dạng cây để Frontend hiển thị thanh Menu bên lề cho người dùng điều hướng.

### 2.3 Thực thể `BookSectionKnowledge` (Tri thức & Vector nhúng)

* **`index_book_sections()`**
  * **Mô tả**: Lấy văn bản thô của từng chương, chia thành các đoạn văn ngắn (chunks) bằng giải thuật LangChain với kích thước `3600` ký tự và độ đè lên nhau `500` ký tự. Sau đó gọi API của OpenAI để tạo mảng Vector `1536` chiều và lưu xuống DB.
* **`match_similar_chunks()`** *(Ánh xạ từ hàm match_book_section_knowledge trong CSDL)*
  * **Mô tả**: Thực hiện tìm kiếm láng giềng gần nhất (ANN) sử dụng khoảng cách Cosine kết hợp với bộ lọc ID sách và ID chương để trả về ngữ cảnh phù hợp nhất cho chatbot.
  * **Ví dụ thực tế**: Khi người dùng hỏi *"Ai là Brimmy?"*, vector câu hỏi được so khớp trực tiếp với các vector của sách thông qua pgvector để lấy ra đoạn trích *"Dimmy called Mrs. Brimming as Brimmy..."*.

### 2.4 Thực thể `ProcessingJob` (Tiến trình xử lý nền)

* **`track_progress()`**
  * **Mô tả**: Cập nhật tiến độ phần trăm (`progress_percent`) và mô tả bước hiện tại (`current_step`) của các tiến trình xử lý nền (Chaptering, AI rewriting, TTS audio).
* **`fail_processing_job()`**
  * **Mô tả**: Đánh dấu tiến trình bị lỗi, cập nhật trạng thái `status = 'failed'` và lưu lại thông điệp lỗi chi tiết (`error_message`) để quản trị viên đối chiếu.

---

## 3. Phân hệ Kế hoạch học tập & Phiên học (Study Planning)

### 3.1 Thực thể `ReadingPlan` (Kế hoạch đọc sách)

* **`switch_book_mode()`**
  * **Mô tả**: Chuyển đổi chế độ học tập giữa `DETAILED` (chi tiết) và `PARETO` (học tinh gọn 20%).
  * **Quy tắc nghiệp vụ**: Khi đổi mode, nếu hệ thống chưa có sẵn các Đơn vị học tập (`learning_units`) cho mode mới, nó sẽ gọi giải thuật AI Planner để tái cấu trúc lộ trình và khởi chạy Job Celery để sinh văn bản/âm thanh mới.
* **`pause_reading_plan()`**
  * **Mô tả**: Tạm dừng kế hoạch học. Trạng thái chuyển thành `inactive`, toàn bộ lịch học tuần (`schedule_slots`) bị tắt, và các phiên học tương lai (`ReadingPlanSession` có status `scheduled`) chưa diễn ra sẽ bị hủy bỏ.
* **`resume_reading_plan()`**
  * **Mô tả**: Kích hoạt lại kế hoạch học. Xác thực lại xem lịch học có bị trùng giờ với các cuốn sách đang học khác hay không, bật lại slots và tự động dựng lại các phiên học tiếp theo cho người dùng dựa trên tiến độ học cũ.

### 3.2 Thực thể `ReadingPlanScheduleSlot` (Lịch học tuần)

* **`validate_plan_schedule_slots()`**
  * **Mô tả**: Ngăn chặn sự chồng chéo lịch học của một người dùng trên các cuốn sách khác nhau.
  * **Ví dụ thực tế**: Nếu người dùng đã cài đặt học sách *Đắc Nhân Tâm* vào lúc 20:00 tối Thứ Hai, hệ thống sẽ chặn và báo lỗi nếu họ đăng ký học thêm sách *Nhà Giả Kim* cũng vào khung giờ 20:00 tối Thứ Hai.

### 3.3 Thực thể `ReadingPlanSession` (Phiên học hàng ngày)

* **`ensure_future_sessions_for_plan()`**
  * **Mô tả**: Tự động tính toán các ngày học tiếp theo trong tương lai dựa trên cấu hình slot và chia nhóm các bài học chưa hoàn thành theo tốc độ học (`pace`).
  * **Xử lý Timezone (DST)**: Hệ thống sử dụng giá trị `timezone` cục bộ (ví dụ: `Europe/Paris`) của slot học để tính toán giờ UTC chính xác cho trường `scheduled_at`, bảo đảm thông báo nhắc nhở luôn được đẩy đi đúng giờ địa phương bất kể múi giờ mùa hè/mùa đông dịch chuyển.
* **`sync_reading_plan_session_unit_completion()`**
  * **Mô tả**: Khi một Đơn vị học tập (`learning_unit`) được người dùng nghe xong, phương thức này cập nhật trạng thái liên kết trong `ReadingPlanSessionUnit`. Sau đó, nó tự động tính toán lại phiên học chứa bài nghe đó; nếu toàn bộ bài nghe trong phiên đạt trạng thái hoàn thành, trạng thái của `ReadingPlanSession` tự động chuyển sang `COMPLETED`.
* **`mark_due_sessions_missed()`**
  * **Mô tả**: Quét định kỳ qua worker để tìm các phiên học ở trạng thái `SCHEDULED` có ngày giờ dự kiến `scheduled_at` đã trôi qua so với hiện tại, tự động cập nhật trạng thái thành `MISSED` (lỡ học) và gửi cảnh báo nhắc nhở.
* **`skip_reading_plan_session()`**
  * **Mô tả**: Cho phép người dùng chủ động bỏ qua phiên học của ngày hôm đó. Toàn bộ trạng thái các bài nghe liên kết với phiên này sẽ được gán nhãn `SKIPPED`.
* **`reschedule_reading_plan_session()`**
  * **Mô tả**: Cho phép dời lịch phiên học sang một ngày/giờ khác tùy chọn, kiểm tra trùng lặp lịch biểu mới trước khi cập nhật.

### 3.4 Thực thể `ReadingPlanSessionUnit` (Đơn vị học trong phiên)

* **`sync_session_unit_status()`**
  * **Mô tả**: Đồng bộ trạng thái hoàn thành (`completed`) hoặc đang học (`in_progress`) của đơn vị học trực tiếp vào phiên học tương ứng.

---

## 4. Phân hệ Đơn vị học tập & Tiến độ (Learning Units & Progress)

### 4.1 Thực thể `LearningUnit` (Bài học)

* **`plan_pareto_learning_units()`**
  * **Mô tả**: Giải thuật AI lọc ra các chương cốt lõi nhất. Chấm điểm tần suất xuất hiện định nghĩa, nguyên lý, công thức để giữ lại tối thiểu 3 bài học đắt giá nhất.
* **`split_large_chapters()`**
  * **Mô tả**: Nếu một chương có dung lượng chữ quá lớn (vượt ngưỡng 12,000 tokens), phương thức này tự động chia chương đó thành các phần bài nghe nhỏ hơn (ví dụ: *Chương 1 - Phần 1/2* và *Chương 1 - Phần 2/2*) để bảo đảm thời lượng nghe mỗi bài không quá dài và không làm quá tải bộ nhớ xử lý âm thanh.
* **`merge_tiny_chapters()`**
  * **Mô tả**: Gom các chương ngắn liền kề (dưới 300 tokens) thành một bài học chung duy nhất để tránh việc người học phải liên tục chuyển tiếp các file âm thanh quá ngắn.

### 4.2 Thực thể `LearningUnitSource` (Nguồn gốc đơn vị học)

* **`list_unit_sources()`**
  * **Mô tả**: Truy vấn toàn bộ danh sách `BookSection` gốc tạo nên đơn vị học tập này.
  * **Ví dụ thực tế**: Lấy ra danh sách các đề mục 3.1, 3.2 để phục vụ tính năng hiển thị nguồn gốc tham chiếu cho người nghe.

### 4.3 Thực thể `LearningUnitProgress` (Tiến độ bài học)

* **`update_learning_unit_progress()`**
  * **Mô tả**: Cập nhật vị trí phát âm thanh (`position_ms`), mã định danh phân đoạn đang nghe (`current_segment_id`). Tự động tính toán tỷ lệ phần trăm đã nghe dựa trên tổng thời lượng của các segment cấu thành.
  * **Quy tắc hoàn thành**: Nếu tỷ lệ nghe đạt hoặc vượt ngưỡng cấu hình `LEARNING_COMPLETION_THRESHOLD_PERCENT` (mặc định là **80%**), trạng thái tiến độ tự động chuyển sang `COMPLETED`, đồng thời kích hoạt chuỗi tạo thẻ ôn tập ngắt quãng `create_spaced_reviews_after_unit_completion`.
  * **Ví dụ thực tế (Nhảy cóc/Tua đoạn)**: Người dùng bắt đầu nghe bài học dài 10 phút, họ nghe được 1 phút rồi nhấn tua nhanh tới phút thứ 9 (segment cuối cùng). Hệ thống sẽ tính lũy kế thời lượng phát đến phút thứ 9 (chiếm 90% tổng bài), so khớp thấy lớn hơn 80% nên lập tức đánh dấu bài học này là đã hoàn thành (`COMPLETED`).

### 4.4 Thực thể `BookLearningState` (Trạng thái học tổng thể sách)

* **`sync_book_learning_state()`**
  * **Mô tả**: Quét tất cả các bản ghi tiến độ của các bài học thuộc cuốn sách đó, tính trung bình cộng tỷ lệ phần trăm hoàn thành, cập nhật số lượng bài đã học trên tổng số bài sẵn có, và lưu vết ID bài nghe/phân đoạn âm thanh gần nhất để hỗ trợ tính năng "Nghe tiếp" (Resume).

---

## 5. Phân hệ Không gian thảo luận (AI Dialogue & Context)

### 5.1 Thực thể `StudyContext` (Workspace học tập)

* **`create_context()`**
  * **Mô tả**: Khởi tạo một không gian học tập mới (Workspace). Có thể liên kết nhiều cuốn sách với nhau.
* **`add_document_to_context()`**
  * **Mô tả**: Liên kết sách vào Workspace bằng cách tạo bản ghi trong bảng phụ `StudyContextDocumentLink`.
* **`delete_document_from_context()`**
  * **Mô tả**: Gỡ bỏ sách ra khỏi Workspace, dọn dẹp các liên kết tài liệu.

### 5.2 Thực thể `ChatThread` (Luồng hội thoại)

* **`get_or_create_thread_for_book()`**
  * **Mô tả**: Tìm hoặc tự động khởi tạo luồng hội thoại chat nhanh mặc định cho một cuốn sách (Direct Book Context).
* **`get_thread_messages()`**
  * **Mô tả**: Tải lịch sử tin nhắn của luồng hội thoại theo thứ tự thời gian.

### 5.3 Thực thể `ChatMessage` (Tin nhắn)

* **`search_book_hybrid_knowledge()`**
  * **Mô tả**: Thực hiện tìm kiếm hỗn hợp RAG (kết hợp vector ngữ nghĩa + lexical từ khóa) trên toàn bộ sách liên kết trong thread để trích xuất thông tin grounding cho chatbot.
* **`get_voice_agent_history()`**
  * **Mô tả**: Trong cuộc gọi thoại realtime của Voice Agent, phương thức này được gọi để tải nhanh $N$ tin nhắn hội thoại gần nhất nhằm thiết lập ngữ cảnh cho mô hình OpenAI Realtime.

### 5.4 Thực thể `DirectBookContext` (Đường tắt ngữ cảnh)

* **`resolve_primary_thread()`**
  * **Mô tả**: Truy xuất nhanh luồng chat chính (`primary_thread_id`) được liên kết trực tiếp giữa Người dùng và Sách mà không cần JOIN qua các bảng Workspace trung gian.
  * **Ví dụ thực tế**: Khi người dùng nhấn nút gọi điện cho AI Assistant từ màn hình đọc sách đơn lẻ, Voice Agent gọi trực tiếp phương thức này với độ phức tạp $O(1)$ để lấy ngay lịch sử trò chuyện cũ dưới 10ms, giúp cuộc hội thoại diễn ra tức thì không bị giật lag ban đầu.

---

## 6. Phân hệ Ôn tập & Thông báo nhắc nhở (Review & Push Notification)

### 6.1 Thực thể `SpacedReviewItem` (Thẻ ôn tập ngắt quãng)

* **`create_spaced_reviews_after_unit_completion()`**
  * **Mô tả**: Khi người học hoàn thành bài học, phương thức này tự động hủy các thẻ cũ chưa hoàn thiện và sinh ra 5 thẻ ôn tập mới với lịch hẹn lùi dần theo các mốc thời gian: `[1, 3, 7, 14, 30]` ngày.
* **`complete_review_item()`**
  * **Mô tả**: Đánh dấu thẻ ôn tập đã được thực hiện, ghi nhận thời điểm hoàn thành để phục vụ thống kê tiến độ.
* **`skip_review_item()`**
  * **Mô tả**: Người dùng có thể chọn bỏ qua thẻ ôn tập hôm nay nếu không muốn học lại.

### 6.2 Thực thể `NotificationOutbox` (Hộp thư đi thông báo đẩy)

* **`enqueue_notification()`**
  * **Mô tả**: Ghi nhận một sự kiện thông báo cần gửi vào hàng đợi lưu trữ kèm theo một khóa `idempotency_key` duy nhất để ngăn ngừa việc hệ thống phân tán gửi trùng lặp một thông báo nhiều lần.
* **`process_outbox_delivery()`**
  * **Mô tả**: Worker quét các bản ghi ở trạng thái `PENDING` có hạn định gửi `due_at <= NOW()`, thực hiện cơ chế khóa dòng (`locked_at`, `locked_by`) để tránh các worker khác giành giật, tiến hành gửi thông báo đẩy qua Firebase Cloud Messaging (FCM). Nếu gửi thất bại, tự động tăng bộ đếm số lần thử (`attempts`) và lập lịch thử lại (`next_retry_at`) với giải thuật giãn cách số mũ (Exponential Backoff).

### 6.3 Thực thể `UserNotification` (Thông báo hiển thị trên giao diện)

* **`mark_as_read()`**
  * **Mô tả**: Cập nhật thời điểm đọc `read_at` khi người dùng nhấn xem thông báo trên điện thoại.
* **`mark_all_as_read()`**
  * **Mô tả**: Đánh dấu đã đọc hàng loạt cho tất cả thông báo của một người dùng.
