# Tài liệu Kiến trúc: LiveKit Voice & Text Agent (Dual-Model)

Tệp: `app/services/agent_voice_gpt_realtime.py`

Tài liệu này giải thích chi tiết luồng hoạt động của Voice Assistant được xây dựng bằng LiveKit Python SDK phiên bản mới nhất (1.5.8). Hệ thống sử dụng kiến trúc **Dual-Model** độc đáo nhằm tối ưu chi phí token, đồng thời hỗ trợ tra cứu RAG (Retrieval-Augmented Generation) thông qua sách mà user cung cấp.

---

## 1. Tổng quan Kiến trúc (The "Why")

Hệ thống cung cấp hai phương thức giao tiếp cho người dùng (Voice và Text). Nếu sử dụng chung một mô hình Realtime duy nhất cho cả hai luồng, chi phí Token Audio sinh ra từ các câu trả lời Text là rất đắt đỏ.

**Giải pháp Dual-Model:**

- **Voice (Giọng nói):** Sử dụng mô hình `gpt-4o-realtime-preview-2024-10-01` (qua class `RealtimeModel`) để giao tiếp trực tiếp bằng giọng nói độ trễ thấp. Mô hình này có toàn quyền sử dụng **tất cả các Tools** (bao gồm `search_book_knowledge` và `search_web`).
- **Text (Văn bản):** Khi user chat text qua DataChannel (`lk.chat`), hệ thống sẽ chuyển câu hỏi cho mô hình `gpt-4o-mini` (rẻ và nhanh hơn nhiều) để sinh câu trả lời chữ, không tạo ra Audio.

> [!WARNING]
> **Hạn chế của mô hình Text hiện tại:** Theo kiến trúc hiện tại, để tối ưu tốc độ và tránh phải xử lý luồng (stream) Tool Calls vô cùng phức tạp, mô hình Text (`gpt-4o-mini`) được thiết lập chạy theo cơ chế **Naive RAG** (chủ động ép tìm kiếm trong sách). Do đó, LLM phụ này sẽ **KHÔNG** tự động dùng được tool `search_web` hay tự suy luận gọi tool như mô hình Voice. Nó chỉ thuần tuý lấy Text user -> Tìm RAG sách -> Trả lời.

---

## 2. Chi tiết các Hàm và Luồng xử lý trong `entrypoint`

`entrypoint` là trái tim của file này. Hàm này sẽ được LiveKit gọi tự động ngay khi một **Job mới** (tương ứng với một người dùng truy cập vào phòng) được tạo ra.

Khi Frontend kết nối vào phòng LiveKit, họ sẽ truyền kèm Metadata.

```python
job_meta = json.loads(ctx.job.metadata or "{}")
# Lấy ra book_id, thread_id (Định danh chuỗi chat) và document_ids (Các tài liệu cần tìm kiếm)
```

### Bước 1: `_save_message` và `_publish_transcript`

- `_save_message(text, is_user)`: Lưu tin nhắn vào DB Supabase. Hàm dùng `await asyncio.to_thread` để chặn (block) luồng hiện tại cho đến khi lưu xong, đảm bảo **thứ tự thời gian vật lý** (Insert Order) vào DB không bị lộn xộn.
- `_publish_transcript(role, text)`: Gói tin nhắn dạng JSON và gửi qua kênh `lk.transcript` để Frontend đồng bộ giao diện chat.

### Bước 2: Các hàm lắng nghe sự kiện Chat (`on_data_received` & `handle_text_input`)

Đây là 2 ngõ vào (entry) cho tin nhắn Text từ người dùng:

- `on_data_received`: Lắng nghe kênh Custom DataChannel có tên là `lk.chat`. Đây là kênh độc quyền do ta tự định nghĩa để Frontend truyền Text siêu tốc. Khi có gói tin, nó giải mã `utf-8` và đẩy dữ liệu vào `handle_data_input`.
- `handle_text_input`: Lắng nghe sự kiện `room_io.TextInputEvent` (kênh Text mặc định của LiveKit, phòng hờ Frontend gọi theo chuẩn mặc định). Hàm này cũng chỉ là một wrapper chuyển tiếp dữ liệu vào `handle_data_input`.

### Bước 3: Trái tim của Text Chat (`handle_data_input`) và khái niệm "Naive RAG"

Hàm này chứa toàn bộ logic Dual-Model cho Chat.

1. Dừng giọng nói hiện tại của Agent (`session.interrupt()`) nếu AI đang lỡ dở nói chuyện.
2. **Naive RAG (RAG ngây thơ/thủ công):** Khái niệm "Naive" ở đây có nghĩa là "Không qua suy luận LLM". Thay vì nạp bộ Tools cho `gpt-4o-mini` và đợi nó mổ xẻ câu hỏi xem có nên gọi Tool không (tốn thêm thời gian và rủi ro stream lỗi), ta **ép hệ thống TỰ ĐỘNG gọi hàm `agent_instance.search_book_knowledge(text)` ở mọi trường hợp**. Bất kể user hỏi gì, code đều tự cào Database sách trước.
3. Nếu cào được dữ liệu sách, code tự động nhồi kết quả vào một biến tạm `temp_ctx` (giả làm lời nhắc hệ thống System Prompt).
4. **Gọi LLM:** Đưa `temp_ctx` chứa sẵn kiến thức cho `gpt-4o-mini` đọc và nhả ra câu trả lời ngay lập tức. LLM không hề biết tới khái niệm Tool, nó chỉ biết đọc System Prompt và trả lời.
5. Gửi Text trả về lại Frontend qua `lk.chat` và cập nhật lịch sử.

### Bước 4: Khởi động AgentSession (Voice Pipeline)

Khởi tạo các Core Instances:

```python
agent_instance = TriamAssistant(document_ids) # Chứa Tools đầy đủ cho Voice
chat_llm = OpenAILLM(model="gpt-4o-mini")     # LLM nhạt nhẽo chỉ để đọc RAG cho Text
model = RealtimeModel(modalities=["audio", "text"], ...) # LLM xịn cho Voice
session = AgentSession(llm=model)             # Bao bọc mọi thứ
```

### Bước 5: Lắng nghe Sự kiện Giọng nói (`_attach_session_handlers`)

Hàm `_attach_session_handlers` gắn các "hook" (lắng nghe) vào `session` của Voice:

- `@sess.on("user_speech_committed")`: Kích hoạt khi user **nói xong** 1 câu vào Micro. Hàm lấy lời dịch transcript lưu vào DB và đẩy lên UI.
- `@sess.on("agent_speech_committed")`: Kích hoạt khi AI **đáp xong** 1 câu bằng giọng nói. Lưu DB và đẩy lên UI.
  Nhờ hàm này mà cả luồng Voice và luồng Text Chat đều được quy về một mối, hiển thị chung trên một màn hình chat của người dùng.

### Bước 6: Phục hồi trí nhớ (`_load_history`)

Sau khi mọi thứ sẵn sàng, code gọi DB lấy toàn bộ lịch sử (`_load_history`), đẩy vào `session.history` để Agent nhớ lại câu chuyện cũ, rồi gọi `session.generate_reply(...)` để phát âm thanh chào hỏi bắt đầu cuộc trò chuyện.
