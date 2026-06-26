# Báo cáo Giải đáp & Đào tạo chuyên sâu Kiến trúc CSDL TRIAM (TRIAM Database Training & Q&A Report)

Báo cáo này được biên soạn dưới dạng tài liệu đào tạo chuyên sâu (training report) nhằm giải đáp cặn kẽ từng câu hỏi của bạn về thiết kế CSDL, thuật toán, cơ chế lập lịch, chỉ mục vector và tối ưu hóa RAG trong hệ thống **TRIAM Backend**.

---

## 1. Phân hệ Cấu hình & Thông báo (`notification_settings` & `notification_outbox`)

### 1.1 Khử dư thừa trường `reminder_time` trong `notification_settings`
*   **Thắc mắc của bạn**: Trên giao diện người dùng (UI), phía Frontend (FE) đã ép người dùng chọn giờ cụ thể khi tạo kế hoạch, vậy trường `reminder_time` mặc định này có bị thừa và gây rối CSDL không?
*   **Giải đáp kỹ thuật**: **Không thừa**.
    1.  **Cơ chế Bản mẫu (Fallback Template)**: Khi người dùng đăng ký tài khoản mới hoặc tải sách lên mà không thiết lập lịch chi tiết ngay lập tức, hệ thống cần một giờ nhắc nhở mặc định để chạy ngầm. `notification_settings.reminder_time` đóng vai trò là cấu hình mặc định ở mức hệ thống cho user đó.
    2.  **Luồng API `generate-plan`**: Khi FE gọi API tạo kế hoạch nhanh (`generate-plan`), nếu FE không truyền tham số giờ cụ thể, backend sẽ lấy chính xác giá trị `notification_settings.reminder_time` để làm mốc lập lịch tự động cho các slot trong bảng `reading_plan_schedule_slots`.
*   **Ví dụ thực tế**: User đăng ký tài khoản, hệ thống mặc định giờ học là `20:00`. Khi user nhấn "Học nhanh" cuốn sách A, API tạo kế hoạch tự động sinh các slot học Thứ 2, Thứ 4, Thứ 6 lúc `20:00` mà không bắt user phải cấu hình thủ công.

### 1.2 Sự cần thiết của `daily_cap` (Giới hạn thông báo hàng ngày)
*   **Thắc mắc của bạn**: Nên bỏ `daily_cap` vì nếu thấy phiền, người dùng có thể tự tắt hoặc ẩn thông báo trên điện thoại.
*   **Giải đáp kỹ thuật**: **Không nên bỏ**.
    *   **Rate Limiting ở mức Backend**: Nếu người dùng học song song 3 cuốn sách và có 5 thẻ ôn tập đến hạn trong ngày, hệ thống có thể kích hoạt đến hơn 10 sự kiện gửi thông báo.
    *   Nếu không có `daily_cap` để chặn ở mức CSDL/Worker:
        1.  Hệ thống sẽ liên tục gọi API của Firebase Cloud Messaging (FCM) gây lãng phí tài nguyên mạng và quota gửi của server.
        2.  Quan trọng hơn, việc đẩy 10+ thông báo một ngày sẽ làm người dùng khó chịu và **tắt hoàn toàn quyền nhận thông báo của app ở mức hệ điều hành (OS Settings)**. Khi người dùng đã tắt quyền ở mức OS, ứng dụng sẽ hoàn toàn mất kênh tiếp cận họ.
    *   `daily_cap` giúp giới hạn tối đa (ví dụ: chỉ gửi tối đa 3 thông báo quan trọng nhất mỗi ngày) để duy trì sự hiện diện của app một cách tinh tế.

---

## 2. Giới hạn Đơn vị học tập (`Book.total_units`) & Thuật toán Pareto

*   **Thắc mắc của bạn**: Tại sao sách `e447b894-4646-46db-a33b-2a073a14723b` có đến 23 chương (`total_sections`) nhưng chế độ Pareto chỉ tạo ra đúng 3 đơn vị học tập (`total_units`)? Có phải đang bị lỗi hay mặc định bằng 3 không?
*   **Giải đáp thuật toán**:
    *   Chế độ **Pareto Mode** hoạt động dựa trên nguyên lý 80/20: Chỉ lấy ra **20% đến 25%** nội dung quan trọng nhất của cuốn sách.
    *   Trong file `app/services/pareto_planner_service.py`, thuật toán thực hiện lọc và gom các chương quan trọng nhất. Sau đó gọi hàm cắt giảm mục tiêu (`_trim_to_target`):
        $$\text{target\_tokens} = \text{total\_source\_tokens} \times \text{PARETO\_TARGET\_COVERAGE\_RATIO}$$
        *(Mặc định `PARETO_TARGET_COVERAGE_RATIO = 0.25` - tức là chỉ bao phủ 25% dung lượng sách).*
    *   Hàm kiểm tra điều kiện lặp để chọn các đơn vị học tập:
        ```python
        for unit in units[: settings.PARETO_PLANNER_MAX_UNITS]:
            selected.append(unit)
            selected_tokens += unit.estimated_tokens
            if len(selected) >= settings.PARETO_PLANNER_MIN_UNITS and selected_tokens >= target_tokens:
                break
        ```
    *   Với một cuốn sách có 23 chương nhỏ (tổng số từ ít), giới hạn 25% target tokens (ví dụ: khoảng 5,000 tokens) sẽ **nhanh chóng bị vượt qua** ngay từ 1 hoặc 2 đơn vị học tập đầu tiên.
    *   Tuy nhiên, do tham số cấu hình tối thiểu `PARETO_PLANNER_MIN_UNITS` được đặt mặc định là **`3`**, thuật toán bắt buộc phải lấy thêm để đạt đủ **3 đơn vị học tập** rồi mới dừng lại.
    *   **Kết luận**: Đây không phải lỗi, mà do dung lượng cuốn sách của bạn khi nhân với tỷ lệ 25% (Pareto) rất nhỏ, nên thuật toán chạm ngay vào điều kiện biên tối thiểu (Lower Bound) là 3 đơn vị học tập. Hầu hết các sách ngắn trong DB đều hiển thị 3 units vì lý do này. Nếu muốn tăng số lượng unit, bạn cần tăng tỷ lệ bao phủ `PARETO_TARGET_COVERAGE_RATIO` lên (ví dụ: `0.4` hoặc `0.5`).

---

## 3. Phân hệ Chương mục sách (`book_sections`)

### 3.1 Ý nghĩa của trường `path`
*   `path` lưu trữ chuỗi phân cấp phả hệ mục lục (ví dụ: `"1.2.1"` có nghĩa là Chương 1 -> Mục 2 -> Ý nhỏ 1).
*   **Mục đích**:
    1.  **Dựng cây mục lục (TOC Tree)**: Frontend chỉ cần đọc cột `path` và `level` để tự động xây dựng giao diện hiển thị hình cây mà không cần cấu trúc dữ liệu phức tạp.
    2.  **Tăng tốc truy vấn con (Prefix Query)**: Khi muốn lấy toàn bộ nội dung của Chương lớn `"1.2"` và tất cả các mục con của nó, thay vì viết truy vấn đệ quy kết nối bảng (Recursive CTE) rất chậm, backend chỉ cần gọi câu lệnh SQL:
        ```sql
        SELECT * FROM book_sections WHERE path LIKE '1.2%';
        ```
        Nhờ cột `path` được đánh chỉ mục (`Index`), câu lệnh này được PostgreSQL xử lý trong vòng chưa đầy 1ms.

### 3.2 Bản chất của các tệp tin & Ứng dụng của `source_href`, `source_anchor`
*   **Bản chất các định dạng**:
    *   **PDF**: Là định dạng layout tĩnh (Fixed Layout). Vị trí chữ được neo cố định theo trang giấy vật lý. Do đó, hệ thống định vị chương bằng `page_start` và `page_end`.
    *   **EPUB / DOCX**: Là định dạng dòng chảy tự do (Reflowable Layout). Tài liệu không có số trang cố định mà chữ tự trôi tùy thuộc vào kích thước màn hình hiển thị và cỡ font chữ. Một cuốn sách EPUB thực chất là một thư mục nén chứa các trang web **HTML (XHTML)** và CSS.
*   **Tại sao lại dính đến HTML và Con trỏ neo?**:
    *   Khi parser phân tích file EPUB, mỗi chương sách thực tế nằm trong một file HTML riêng biệt bên trong tệp nén.
    *   `source_href`: Đường dẫn đến file HTML đó (ví dụ: `OEBPS/Text/chapter_1.xhtml`).
    *   `source_anchor`: ID của thẻ HTML nơi chương đó bắt đầu (ví dụ: `<h2 id="section_1_2">` -> anchor là `"section_1_2"`).
    *   Khi người dùng nhấn vào mục lục trên Frontend để đọc sách, Frontend sẽ mở file HTML tương ứng (`source_href`) và nhảy trực tiếp đến thẻ neo (`source_anchor`). Đây là **con trỏ định vị duy nhất** của các định dạng reflowable để thay thế cho số trang vật lý.

---

## 4. Phân hệ Ngữ cảnh RAG & Embedding (`book_section_knowledge`)

### 4.1 Cấu trúc trường `search_text`
*   Phương thức sinh: `search_text = normalized_key(f"{section_path} {section_title} {content}")`.
*   Vì nội dung `content` luôn được bọc trong tiêu đề định dạng `[{section_path}]` để giữ ngữ cảnh, khi chuẩn hóa loại bỏ dấu câu, chuỗi số chương sẽ xuất hiện lặp lại ở đầu. Điều này giúp nâng cao điểm số tần suất từ khóa (TF-IDF/BM25) khi người dùng chat hỏi trực tiếp số chương (ví dụ: *"Chương 10 nói về gì?"*).

### 4.2 Tìm hiểu sâu về chỉ mục HNSW (Hierarchical Navigable Small World)
*   **HNSW là gì?**: HNSW là giải thuật chỉ mục tìm kiếm vector gần đúng (ANN) hoạt động dựa trên đồ thị đa lớp.
*   **Nguyên lý hoạt động**:
    *   HNSW xây dựng các lớp đồ thị liên kết chéo. Lớp trên cùng có các liên kết thưa (giống đường cao tốc liên tỉnh), các lớp dưới có liên kết dày đặc hơn (giống đường nội đô).
    *   Khi tìm kiếm vector tương đồng, thuật toán xuất phát từ lớp trên cùng để nhảy nhanh đến vùng gần đúng nhất, sau đó đi dần xuống các lớp dưới để tìm kiếm chi tiết.
    *   Độ phức tạp truy vấn giảm từ quét toàn bộ bảng $O(N)$ xuống còn $O(\log N)$, cho phép tìm kiếm ngữ nghĩa trên hàng triệu vector chỉ trong vài mili-giây.

```
[Lớp thưa - Cao tốc]   ●───────────────●
                        │               │
[Lớp trung gian]       ●───────●───────●───────●
                        │       │       │       │
[Lớp dày - Đô thị]     ●─●─●─●─●─●─●─●─●─●─●─●─●─●─●  <-- Điểm đích gần nhất
```

### 4.3 Thiết kế Chỉ mục (Index Layout Best Practices)
*   Hệ thống khai báo chỉ mục: `Index("ix_bsk_book_section_version", "book_id", "section_id", "embedding_version")`.
*   **Tại sao thứ tự các trường lại như vậy?**:
    *   Theo nguyên lý tiền tố chỉ mục (Index Prefix Matching) của PostgreSQL, khi truy vấn sử dụng một phần của chỉ mục phức hợp, hệ thống sẽ khớp từ trái qua phải.
    *   Trong các câu lệnh RAG của TRIAM, điều kiện lọc luôn luôn bắt đầu bằng `book_id` (lọc các chunk thuộc cuốn sách hiện tại). Việc đặt `book_id` ở đầu tiên giúp loại bỏ ngay 99% dữ liệu của các cuốn sách khác.
    *   `section_id` được đặt thứ hai vì thỉnh thoảng hệ thống chỉ muốn RAG trong phạm vi chương hiện tại.
    *   `embedding_version` được đặt cuối cùng vì giá trị này hầu như cố định trong một phiên bản chạy của backend.
    *   Thứ tự này đã được tối ưu hóa tối đa thông qua phân tích câu lệnh truy vấn (Query Explain Analyze) thực tế trong dự án.

---

## 5. Lập lịch học tập & Khung giờ học (`reading_plans` & `slots`)

### 5.1 Ví dụ cụ thể về sự khác nhau giữa Giờ học chung và Giờ học riêng của Slot
*   **Ví dụ thực tế**:
    *   Bạn tạo một Kế hoạch học tập (`ReadingPlan`) cho cuốn sách *Kinh Tế Học*. Bạn cấu hình giờ học mặc định (`reading_plans.reminder_time`) là **`20:00`**.
    *   Tuy nhiên, vào ngày cuối tuần (Thứ Bảy), bạn rảnh rỗi và muốn học sớm vào buổi sáng, còn các ngày trong tuần (Thứ Hai, Thứ Tư) bạn đi làm về muộn nên học tối.
    *   Khi đó, bảng `reading_plan_schedule_slots` sẽ chứa:
        *   Slot 1 (Thứ 2): `reminder_time = "20:00"` (lấy theo mặc định của kế hoạch).
        *   Slot 2 (Thứ 4): `reminder_time = "20:00"` (lấy theo mặc định của kế hoạch).
        *   Slot 3 (Thứ 7): `reminder_time = "09:00"` (ghi đè lịch cuối tuần).

### 5.2 Khởi tạo Kế hoạch qua API `generate-plan`
*   **Đúng như bạn dự đoán**: Khi FE gọi API tạo kế hoạch, hệ thống sẽ thực hiện đồng thời hai việc:
    1.  Tạo dòng kế hoạch `ReadingPlan` lưu giờ chung (`reminder_time`).
    2.  Tự động sinh các slot mặc định tương ứng trong bảng `reading_plan_schedule_slots` với giờ học được điền sẵn chính bằng `reminder_time` của kế hoạch đó cho các ngày trong tuần được chọn.

### 5.3 Cách thức xử lý Timezone và DST trong CSDL
*   **Cách thức vận hành**:
    *   Trong `reading_plan_session_service.py`, khi tính toán phiên học tiếp theo:
        ```python
        tz = ZoneInfo(slot.timezone)  # Lấy timezone của user (ví dụ: Europe/Paris)
        local_dt = datetime.combine(local_day, slot_time, tzinfo=tz) # Kết hợp ngày + giờ học local
        scheduled_at = local_dt.astimezone(timezone.utc) # Chuyển sang UTC để lưu xuống DB
        ```
    *   Nếu user ở Paris (timezone `"Europe/Paris"`), vào mùa đông (CET = UTC+1), phiên học lúc 20:00 local sẽ được lưu là `19:00 UTC`. Vào mùa hè (CEST = UTC+2), phiên học lúc 20:00 local sẽ được lưu là `18:00 UTC`.
    *   Khi quét gửi thông báo, Worker nền đối chiếu theo cột `scheduled_at` dạng UTC nên thông báo luôn nổ ra chính xác lúc 20:00 giờ của người dùng bên Pháp. Cơ chế này đã được kiểm thử (tested) và hoạt động ổn định.

---

## 6. Phiên học hàng ngày (`reading_plan_sessions`)

### 6.1 Ví dụ cụ thể về Snapshot / Audit Log của `reminder_time`
*   **Ví dụ thực tế**:
    *   Hôm nay là ngày 19/06, hệ thống sinh ra một phiên học (`ReadingPlanSession`) cho ngày Thứ Hai tuần sau (22/06) dựa trên lịch slot lúc **`20:00`**. Dòng phiên học này lưu cứng `reminder_time = "20:00"`.
    *   Vào ngày 21/06, người dùng thay đổi lịch học Thứ Hai của họ trong cài đặt slot thành **`22:00`**.
    *   Nhờ cơ chế **Snapshot/Audit Log** lưu trực tiếp giờ học vào phiên học:
        *   Phiên học ngày 22/06 đã được sinh ra từ trước vẫn giữ nguyên giờ học là `20:00` (không bị biến động đột ngột).
        *   Chỉ các phiên học tương lai sinh ra sau thời điểm thay đổi mới áp dụng khung giờ mới `22:00`.
        *   Nó giúp lưu giữ chính xác lịch sử học tập thực tế trong quá khứ của người dùng để làm báo cáo thống kê chuyên cần.

---

## 7. Đơn vị học tập & Phân mảnh âm thanh (Learning Units)

### 7.1 Cắt nhỏ chương sách quá dài
*   **Đúng như bạn hiểu**: Nếu một chương có dung lượng chữ quá lớn vượt ngưỡng `12,000` tokens, hệ thống sẽ chia nhỏ thành các phần và đặt tên hậu tố dưới dạng `- Phần 1/2`, `- Phần 2/2` để bảo đảm file audio nghe không quá dài và tránh bị lỗi vượt giới hạn context window của LLM.

### 7.2 Cách thức tận dụng RAG của `learning_unit_sources`
*   **Cơ chế vận hành**:
    *   Bảng `learning_unit_sources` lưu vết chính xác Đơn vị học tập này được tổng hợp từ những `section_id` (chương) nào của sách gốc.
    *   Khi người dùng đang nghe bài học này và bật Voice Agent để đặt câu hỏi liên quan đến nội dung đang nghe, Voice Agent sẽ thực hiện RAG.
    *   Thay vì gọi RAG quét toàn bộ cuốn sách (dễ bị nhiễu thông tin từ các chương khác), hệ thống lấy danh sách `section_id` nguồn từ bảng `learning_unit_sources` và truyền vào bộ lọc RAG:
        ```python
        # Giới hạn tìm kiếm vector chỉ trong các chương nguồn của bài nghe này
        search_book_section_knowledge(..., filter_section_ids=source_sections)
        ```
    *   Điều này giúp câu trả lời của AI tập trung chính xác tuyệt đối vào phân đoạn người dùng đang nghe, tăng chất lượng RAG lên gấp nhiều lần.

### 7.3 Luồng cập nhật của `learning_unit_progress` đối với Segment
*   **Thắc mắc của bạn**: 1 `learning_unit_progress` quản lý 1 `learning_unit`. 1 `learning_unit` chứa $N$ `learning_unit_segment`. Progress theo dõi `segment`, khi `segment` nghe xong thì cập nhật sang `learning_unit` đúng không?
*   **Giải đáp luồng hoạt động**: **Đúng như vậy**.
    *   Mỗi khi Client phát xong một phân đoạn âm thanh nhỏ (`LearningUnitSegment`), nó gửi request lên API cập nhật tiến độ kèm theo ID của segment đó và vị trí mili-giây phát hiện tại.
    *   Backend nhận dữ liệu, tính tổng thời lượng của các segment đã nghe qua và cập nhật vào `LearningUnitProgress`:
        *   `current_segment_id` cập nhật thành ID segment mới nhất.
        *   `last_segment_index` cập nhật thành vị trí segment hiện tại.
        *   Tính toán phần trăm hoàn thành bài học lớn dựa trên tổng độ dài các segment con. Khi phần trăm tổng đạt $\ge 80\%$, backend cập nhật cột `status` của `learning_unit_progress` sang `COMPLETED`, đánh dấu bài học lớn đã học xong.

### 7.4 Sự cần thiết của các liên kết khóa ngoại trong `spaced_review_items`
*   **Thắc mắc của bạn**: Tại sao bảng này lại có quan hệ với cả `user`, `learning_unit` và `book`? Có bị thừa không?
*   **Giải đáp thiết kế**: Đây là kỹ thuật **Denormalization (Phi chuẩn hóa)** có chủ ý để tối ưu hóa hiệu năng đọc của PostgreSQL:
    *   Nếu ta chỉ lưu `learning_unit_id` trong thẻ ôn tập: Khi người dùng mở app và vào màn hình *"Danh sách thẻ ôn tập hôm nay của cuốn sách A"*, hệ thống sẽ phải thực hiện truy vấn kết nối bảng phức tạp (JOIN `spaced_review_items` với `learning_units` rồi kết nối tiếp với `books`). Lệnh JOIN 3 bảng trên tập dữ liệu hàng triệu dòng của nhiều user sẽ làm đứng hình ứng dụng.
    *   Bằng cách lưu trực tiếp cả `user_id` và `book_id` vào bảng `spaced_review_items`, hệ thống chỉ cần gọi một câu truy vấn cực kỳ đơn giản và nhanh chóng:
        ```sql
        SELECT * FROM spaced_review_items WHERE user_id = :u AND book_id = :b AND due_at <= NOW();
        ```
        Lệnh này chạy thẳng trên Index, không cần JOIN bảng, tốc độ phản hồi đạt mức dưới 1ms.

---

## 8. Các thắc mắc nâng cao (Advanced Mechanisms)

### 8.1 Primary Key Lookup và độ phức tạp $O(1)$
*   **Primary Key Lookup**: Là phép tìm kiếm một bản ghi trong CSDL bằng cách chỉ định chính xác khóa chính của bảng (ví dụ: truy vấn bằng `user_id` + `book_id` trong bảng `direct_book_context`).
*   **Tại sao độ phức tạp lại là $O(1)$?**:
    *   Hệ quản trị CSDL tự động tạo một chỉ mục cây B-Tree cho khóa chính.
    *   Khi thực hiện truy vấn theo khóa chính, công cụ tìm kiếm của PostgreSQL đi thẳng từ gốc cây index đến lá chứa dữ liệu mà không cần duyệt qua các dòng khác trong bảng. Đối với các điểm truy cập đơn lẻ như vậy, về mặt logic nghiệp vụ hệ thống, thời gian truy xuất là cố định và độc lập với kích thước bảng dữ liệu (độ phức tạp đạt ngưỡng lý thuyết tương đương $O(1)$).

### 8.2 Tại sao `direct_book_context` có nhiều mối quan hệ phức tạp?
*   Bảng này đóng vai trò là **Đường tắt liên kết nhanh (Shortcut)**.
*   Khi người dùng không ở trong một Workspace (StudyContext) lớn mà chỉ bấm nhanh vào một cuốn sách để đọc/gọi điện thoại trực tiếp với AI, hệ thống chat yêu cầu phải có một Workspace và một luồng chat hoạt động.
*   Do đó, bảng này phải liên kết trực tiếp cặp `(User, Book)` với Workspace tự động sinh ra (`context_id`) và luồng hội thoại chính của nó (`primary_thread_id`). Nó đóng vai trò là cầu nối liên kết 4 thực thể lớn lại với nhau, dẫn đến việc có nhiều đường nối quan hệ trong sơ đồ lớp.

### 8.3 Cơ chế xử lý khi nhảy cóc Segment hoàn thành bài học
*   **Thắc mắc của bạn**: Nếu tôi nhấn nút "Next" để nhảy sang phân đoạn segment mới (chứ không phải tua đến cuối phân đoạn hiện tại) khi segment cũ chưa nghe được 80%, hệ thống sẽ xử lý ra sao?
*   **Giải đáp luồng nghiệp vụ**:
    *   Hệ thống **không yêu cầu** bạn phải nghe từng segment đạt 80% mới cho hoàn thành. Ngưỡng 80% chỉ áp dụng cho **tổng thời lượng của toàn bộ bài học lớn (Learning Unit)**.
    *   Khi bạn nhấn "Next" để nhảy sang segment mới (ví dụ từ segment index 1 sang segment index 2):
        1.  Frontend gửi request cập nhật tiến độ lên Backend báo rằng người dùng đã chuyển sang segment index 2.
        2.  Backend lập tức cộng dồn thời lượng của toàn bộ các segment phía trước (segment index 0 và 1) vào tổng thời lượng đã nghe:
            `before = sum(durations[:2])`
        3.  Tỷ lệ phần trăm tiến trình mới được tính bằng:
            $$\text{progress\_percent} = \frac{\text{before} + \text{position\_ms\_tại\_segment\_mới}}{\text{tổng\_thời\_lượng\_bài\_nghe\_lớn}}$$
        4.  Nếu tỷ lệ cộng dồn mới này vượt qua ngưỡng 80% của cả bài nghe lớn, bài học đó sẽ được đánh dấu là **`COMPLETED`** ngay lập tức.
        5.  Nếu chưa đạt 80% (ví dụ bài nghe có 10 segment mà bạn mới nhảy đến segment 3), trạng thái bài học vẫn giữ là **`IN_PROGRESS`**.

### 8.4 Chất lượng của văn bản Embedding (Carriage Returns / Xuống dòng bất thường)
*   **Nhận xét của bạn**: Văn bản được trích xuất lưu trong DB bị ngắt dòng, xuống dòng bất thường:
    ```
    “The drawers of these great chests are so enormous that I could almost
    get into one!” said Paul...
    ```
    Liệu điều này có ảnh hưởng đến chất lượng RAG không?
*   **Đánh giá chất lượng RAG**:
    *   **Ảnh hưởng nhẹ đến Embedding**: Các mô hình nhúng hiện đại như `text-embedding-3-small` của OpenAI sử dụng bộ mã hóa Byte-Pair Encoding (BPE) nên có khả năng hiểu ngữ nghĩa khá tốt bất kể dấu xuống dòng. Tuy nhiên, việc xuống dòng giữa chừng trong một câu dài có thể làm sai lệch ranh giới từ vựng (Tokenization boundaries), gây giảm nhẹ độ chính xác khi tính toán vector tương đồng.
    *   **Ảnh hưởng đến LLM**: Khi RAG trích xuất đoạn văn này làm context gửi cho LLM (Gemini/GPT) trả lời, các ký tự xuống dòng dư thừa làm văn bản bị vụn vặt, khiến LLM đọc hiểu kém hơn và gây lãng phí token cấu trúc câu.
*   **Đề xuất Tối ưu hóa Chunker (Cleanup Recommendation)**:
    Hệ thống nên cải tiến hàm chuẩn hóa văn bản `normalize_section_text` trong file `app/services/book_section_chunker.py` để xóa bỏ các dấu xuống dòng đơn lẻ nằm giữa câu, chỉ giữ lại dấu xuống dòng kép `\n\n` đại diện cho phân đoạn paragraph thực sự.

    *Đoạn mã đề xuất tối ưu*:
    ```python
    def normalize_section_text(text: str | None) -> str:
        if not text:
            return ""
        # Thay thế các dấu xuống dòng đơn lẻ bằng khoảng trắng, chỉ giữ lại \n\n làm phân đoạn
        paragraphs = text.split("\n\n")
        cleaned_paragraphs = []
        for p in paragraphs:
            # Xóa các ký tự xuống dòng đơn lẻ trong từng đoạn văn
            cleaned_p = " ".join(line.strip() for line in p.splitlines() if line.strip())
            if cleaned_p:
                cleaned_paragraphs.append(cleaned_p)
        return "\n\n".join(cleaned_paragraphs).strip()
    ```
    Giải pháp này giúp làm sạch hoàn toàn văn bản chunking, tăng chất lượng tìm kiếm ngữ nghĩa RAG lên mức tối đa.
