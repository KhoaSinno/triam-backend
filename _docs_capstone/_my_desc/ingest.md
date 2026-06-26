# PHẦN 1: BẢN MÔ TẢ HOÀN CHỈNH

### 1. Nguyên tắc hoạt động chung (Planning Phase)

Cả hai chế độ **Full Mode** và **Pareto Mode** đều hoạt động dựa trên cấu trúc chương mục (`BookSection`) và đều xuất ra một cấu trúc dữ liệu tương tự nhau (lưu vào bảng `learning_units` và bảng liên kết `learning_unit_sources`).

- **Full Mode (Chế độ đầy đủ)**: Nhận toàn bộ các chương mục lớn của sách và tiến hành phân bổ đồng đều theo ngưỡng giới hạn cấu hình:
  - **Ngưỡng tối đa (Max limit)**: Nếu một chương lớn (kèm toàn bộ các phần con của nó) có dung lượng vượt quá `12.000 tokens` (`FULL_UNIT_MAX_TOKENS`), thuật toán sẽ tự động chia nhỏ chương này thành nhiều Unit bài học khác nhau (được đặt tên theo hậu tố `- Phần 1/2`, `- Phần 2/2`,...).
  - **Ngưỡng tối thiểu (Min limit)**: Nếu một chương quá ngắn (dưới `300 tokens` - `MIN_UNIT_TOKENS`), thuật toán sẽ tự động gộp chương đó với các chương liền kề tiếp theo để tạo thành một Unit bài học hoàn chỉnh, tránh việc file âm thanh bị chia quá vụn vặt.
  - **Trường hợp lý tưởng**: Nếu một chương có dung lượng nằm trong khoảng từ `300` đến `12.000` tokens, chương đó sẽ tương ứng chính xác với **1 Unit bài học**.
- **Pareto Mode (Chế độ rút gọn)**: Hoạt động với thuật toán gom nhặt tương tự, nhưng sử dụng Prompt riêng và giới hạn kích thước khác biệt (`PARETO_UNIT_MAX_TOKENS = 8.000` tokens). Thay vì lấy toàn bộ chương, nó chỉ chọn ra **20% nội dung cốt lõi** có điểm chất lượng cao nhất (dựa trên thuật toán chấm điểm tín hiệu Pareto) để phân bổ vào tối đa **8 Unit bài học**.

---

### 2. Luồng xử lý kỹ thuật sau khi chia Unit bài học

Sau khi Kế hoạch học tập được lưu vào database, hệ thống sẽ thực hiện 2 luồng xử lý độc lập nhưng bổ trợ cho nhau:

#### Luồng A: Trích xuất RAG & Tạo Vector Embedding (Chạy ngay khi Upload sách)

Luồng này diễn ra độc lập và chạy trước luồng sinh bài học, ngay khi sách được tải lên qua API `/upload`:

- Hệ thống đọc dữ liệu thô của tất cả các `BookSection`.
- Chia nhỏ văn bản của mỗi section thành các chunk có kích thước tĩnh: **3.600 ký tự (chars)**, độ gối đầu (overlap) là **500 ký tự** (tổng cộng khoảng 4.100 ký tự mỗi chunk).
- Gọi model Embedding của OpenAI để chuyển đổi các chunk này thành vector và lưu cứng vào bảng `book_section_knowledge`.

#### Luồng B: Biên tập kịch bản nói & Sinh âm thanh (Chạy bởi Worker tạo bài học)

Khi người dùng bấm học hoặc hệ thống chạy ngầm chuẩn bị bài học cho các Unit đã phân bổ:

1.  **Biên tập kịch bản nói (LLM Normalize)**: Hệ thống lấy văn bản thô của Unit gửi cho Gemini để rewrite thành ngôn ngữ nói tự nhiên, lược bỏ ký tự Markdown và bảng biểu. Cả hai chế độ **Full Mode** và **Pareto Mode** đều sử dụng chung thuật toán này, chỉ khác nhau về System Prompt gửi đi.
    - _Chiến lược chính - Gửi toàn bộ (Single Call)_: Vì Planner đã giới hạn kích thước mỗi Unit tối đa là `12.000 tokens` (Full Mode) hoặc `8.000 tokens` (Pareto Mode), nên trong hầu hết các trường hợp thông thường, dung lượng của Unit sẽ nhỏ hơn hoặc bằng giới hạn mềm `LLM_INPUT_SOFT_TOKEN_LIMIT` (mặc định là `12.000 tokens`). Do đó, hệ thống sẽ **gửi toàn bộ văn bản của Unit trong 1 lần duy nhất** cho Gemini.
    - _Chiến lược phòng vệ - Chia mảnh (Chunking)_: Chỉ khi một chương/section thô của sách quá lớn và không thể chia nhỏ thêm ở cấp độ mục lục (khiến dung lượng Unit vượt quá giới hạn mềm `12.000 tokens`), hệ thống mới kích hoạt chia mảnh. Khi đó, nó dùng LangChain chia văn bản thành các chunk nhỏ (target `5.000 tokens` - `LLM_CHUNK_TARGET_TOKENS`, overlap `300 tokens` - `LLM_CHUNK_OVERLAP_TOKENS`) và gọi Gemini cuốn chiếu từng chunk, gửi kèm đoạn văn đuôi **600 ký tự** của chunk trước để AI nối mạch văn. Kết quả trả về của từng chunk sẽ được Backend **tự động gộp** lại thành một JSON tổng.
2.  **Sinh âm thanh (TTS)**:
    - Hệ thống đọc mảng `main_scripts` đã gộp (AI được cấu trúc sẵn để mỗi phần tử trong mảng là một đoạn văn ngắn khoảng 3-5 câu).
    - Chạy vòng lặp song song gửi từng đoạn văn ngắn này cho công cụ TTS (Edge TTS hoặc Google TTS) để tạo thành các file audio tương ứng (`part_1.mp3`, `part_2.mp3`,...).
    - **Lưu ý**: Nếu một đoạn văn do LLM sinh ra quá dài (vượt giới hạn 5.000 bytes của Google TTS), hệ thống sẽ báo lỗi chứ không tự động dùng LangChain để chia nhỏ lại (nhằm giữ nguyên vẹn cấu trúc câu mà AI đã biên tập).

---

### 3. Sự phối hợp giữa hai bộ cắt của hệ thống (Planner Split vs. LLM Chunking)

Hệ thống thiết kế hai bộ cắt độc lập bổ trợ cho nhau nhằm giải quyết triệt để vấn đề giới hạn xử lý token:

*   **Bộ cắt thô của Planner (Cấp độ mục lục - Outline Level)**: 
    *   *Cơ chế*: Chia nhỏ bài học dựa trên ranh giới các chương con (`BookSection`) trong mục lục của sách.
    *   *Giới hạn*: Chỉ hoạt động ở mức độ cấu trúc cơ sở dữ liệu. Nó **không thể** tự ý cắt đôi nội dung văn bản của một dòng `BookSection` đơn lẻ.
    *   *Trường hợp Edge Case*: Nếu sách gốc viết một chương rất dài (ví dụ 20.000 tokens) nhưng không chia mục con (không có section con 1.1, 1.2), database sẽ chỉ lưu trữ 1 dòng `BookSection` 20.000 tokens. Lúc này, Planner bắt buộc phải tạo 1 Learning Unit duy nhất chứa trọn vẹn 20.000 tokens này (vượt Max 12k).
*   **Bộ cắt tinh của LLM Normalize (Cấp độ văn bản - Text Level via LangChain)**:
    *   *Cơ chế*: Sử dụng `RecursiveCharacterTextSplitter` của LangChain để chia nhỏ văn bản thô theo dấu câu và dấu xuống dòng (target 5.000 tokens).
    *   *Vai trò*: Đóng vai trò là chốt chặn cuối cùng. Khi bài học thô rơi vào trường hợp Edge Case ở trên (Unit > 12.000 tokens), bộ cắt này sẽ tự động kích hoạt để chia nhỏ văn bản và gọi AI cuốn chiếu, đảm bảo Gemini luôn nhận được các phần văn bản vừa vặn sức xử lý.

