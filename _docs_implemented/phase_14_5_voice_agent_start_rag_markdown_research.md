# Báo cáo Nghiên cứu: Phân tích Điểm Chính Xác Gây Startup RAG & Cấu hình Prompts Markdown (English Prompts)

Báo cáo này đã được cập nhật dựa trên nghiên cứu mã nguồn chi tiết để chỉ ra **chính xác các vị trí dòng code** gây ra hiện tượng Voice Agent tự động gọi RAG tìm kiếm sách khi kết nối, và đề xuất các chỉnh sửa prompt tiếng Anh (English prompts) cho phép hiển thị Markdown (cả đơn giản lẫn phức tạp) trên Frontend cho cả Text và Voice Agent.

---

## Vấn đề 1: Tự động chạy RAG khi kết nối (Startup RAG Trigger)

Hiện tượng RAG (truy vấn cơ sở dữ liệu sách/embeddings) tự động chạy ngay khi bắt đầu Voice Session mới tinh mà không qua câu chào xuất phát từ các điểm chính xác sau trong mã nguồn:

### 1. Điểm nạp lịch sử trò chuyện cũ vào Context của Session
*   **Vị trí**: [agent_voice_gpt_realtime.py:L1300-L1307](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L1300-L1307)
*   **Chi tiết dòng code**:
    ```python
    try:
        history_msgs = await transcript_store.load_recent_history(settings.VOICE_AGENT_HISTORY_LIMIT)
        # type: ignore[attr-defined]
        if hasattr(session, "history") and session.history is not None:
            for msg in history_msgs:
                # type: ignore[attr-defined]
                session.history.add_message(role="user" if msg.is_user else "assistant", content=msg.text)
            _truncate_session_history()
    except Exception as e:
        log.info(f"Lỗi khi load history: {e}")
    ```
*   **Giải thích cơ chế**: Khi Voice Session vừa bắt đầu (kết nối phòng LiveKit thành công), hệ thống lấy lịch sử tin nhắn gần nhất từ DB (dựa trên `thread_id` được truyền lên qua metadata). Các tin nhắn này được đẩy trực tiếp vào `session.history`. Nếu Frontend (FE) truyền lên một `thread_id` đã có sẵn (hoặc cache cũ), context hội thoại sẽ chứa các tin nhắn cũ từ trước.

### 2. Điểm kích hoạt phát sinh câu trả lời đầu tiên
*   **Vị trí**: [agent_voice_gpt_realtime.py:L1311-L1313](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L1311-L1313)
*   **Chi tiết dòng code**:
    ```python
    await session.generate_reply(
        instructions=GREETING_INSTRUCTIONS,
    )
    ```
*   **Giải thích cơ chế**: Sau khi nạp lịch sử, hệ thống gọi `session.generate_reply(...)` với chỉ dẫn chào hỏi. Tại thời điểm này, mô hình `gpt-4o-realtime` nhận được cả lịch sử trò chuyện vừa nạp lẫn chỉ dẫn `GREETING_INSTRUCTIONS`.
*   Nếu tin nhắn cuối cùng trong lịch sử là một câu hỏi của người dùng chưa được trả lời (hoặc mô hình tự đánh giá cần làm rõ tiếp bối cảnh sách), mô hình sẽ ưu tiên thực thi các công cụ (tool calls) theo luật chung thay vì chỉ phát âm câu chào tĩnh.

### 3. Vị trí Công cụ RAG được khai báo và kích hoạt
*   **Vị trí**: [agent_voice_gpt_realtime.py:L360-L375](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L360-L375)
*   **Chi tiết dòng code**:
    ```python
    @function_tool
    async def search_book_knowledge(
        self,
        query: Annotated[str, "Câu hỏi hoặc nội dung cần tìm trong sách"],
    ) -> str:
        self.tracer.record_tool(AgentInputMode.VOICE, "search_book_knowledge")
        return await self.resolve_book_query(query, AgentInputMode.VOICE)
    ```
*   Khi mô hình quyết định cần thông tin sách, nó thực hiện gọi công cụ `search_book_knowledge`.

### 4. Điểm thực thi truy vấn cơ sở dữ liệu sách (RAG Database Query)
*   **Vị trí**: [agent_voice_gpt_realtime.py:L529-L547](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L529-L547)
*   **Chi tiết dòng code**:
    ```python
    async def _resolve_rag_context(self, query: str, input_mode: AgentInputMode) -> str:
        try:
            result = await search_voice_book_context(
                query,
                self.document_ids,
                tracer=self.tracer,
                input_mode=input_mode,
            )
            ...
    ```
*   Hàm `search_voice_book_context` thực hiện vector search và nạp các đoạn văn bản (RAG) từ Postgres/Supabase lên, gây ra hiện tượng tự động chạy RAG khi kết nối.

### 5. Nhiễu Mic kích hoạt VAD/STT lúc khởi tạo
*   **Vị trí**: [agent_voice_gpt_realtime.py:L1182-L1185](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L1182-L1185)
*   **Chi tiết dòng code**:
    ```python
    @sess.on("user_input_transcribed")  # type: ignore[arg-type]
    def on_user_input_transcribed(ev):
        watchdog.record_user_transcribed()
        _handle_user_input_transcribed(ev)
    ```
*   **Giải thích cơ chế**: Khi mic mở, tiếng ồn click chuột hoặc nhiễu mic được Whisper STT dịch nhầm thành các từ khóa tiếng Việt. Vừa kết nối xong, mô hình nhận được text này dưới dạng tin nhắn của User, buộc nó phải phản hồi và kích hoạt tool RAG ngay lập tức.

### Giải pháp Khắc phục Đề xuất cho Vấn đề Startup RAG

Để chặn triệt để việc mô hình tự động gọi công cụ RAG ở lượt đầu tiên (lượt chào hỏi), ta cấu hình `GREETING_INSTRUCTIONS` thành một prompt tiếng Anh chỉ định hành vi nghiêm ngặt:

```python
GREETING_INSTRUCTIONS = (
    "Speak exactly the following greeting in Vietnamese: "
    "\"Chào ông, tôi là TRIAM đây. Bạn muốn thảo luận về chương sách nào hôm nay?\" "
    "Under no circumstances should you call any tools (including search_book_knowledge) "
    "or attempt to answer any historical queries from previous turns. Just output the "
    "greeting text and finish this turn immediately."
)
```

---

## Vấn đề 2: Cho phép hiển thị Markdown (Tiêu chuẩn Prompts tiếng Anh)

Để Frontend hiển thị định dạng văn bản trực quan và đẹp mắt (headings, lists, bold text, tables), các chỉ dẫn prompts tiếng Anh được thay đổi để cho phép trả về đầy đủ định dạng Markdown cho cả Chat thường (Text) và Voice Chat (Voice).

### 1. Chỉ dẫn cho Trợ lý Voice Chat (Voice Mode)
Mặc dù Voice Chat liên quan đến việc tổng hợp giọng nói (TTS), việc chấp nhận định dạng Markdown (kể cả phức tạp) sẽ giúp văn bản hiển thị trên app/web sinh động hơn. Chúng ta cập nhật prompt bằng tiếng Anh cho phép trả về Markdown đầy đủ, nhưng yêu cầu giọng điệu đọc tự nhiên.

*   **Vị trí cần sửa**: `VOICE_AGENT_INSTRUCTIONS` tại [agent_voice_gpt_realtime.py:L68-L96](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L68-L96).
*   **Prompt tiếng Anh đề xuất**:
    ```text
    - Answer in Vietnamese only.
    - Keep replies conversational, concise, and focused (typically 2-4 sentences).
    - Feel free to use rich Markdown formatting (including bold **, bullet lists -, numbered lists, headings #/##, and tables) in your response so that the transcript text is clearly structured and visually appealing on the user's screen.
    ```

### 2. Chỉ dẫn cho Trợ lý Text Chat (Text Mode)
Đối với giao diện Text Chat không sử dụng âm thanh nói, Markdown đầy đủ được khuyến khích để tạo cấu trúc thông tin rõ ràng.

*   **Vị trí cần sửa**: `TEXT_AGENTIC_SYSTEM_INSTRUCTIONS` tại [agent_voice_gpt_realtime.py:L99-L118](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L99-L118).
*   **Prompt tiếng Anh đề xuất**:
    ```text
    - Answer in Vietnamese only, keeping the response structured and focused.
    - You are encouraged to use rich Markdown formatting (such as headings #/##, bold text **, lists, and tables) to present your answers in a professional, readable, and visually beautiful format on the UI.
    ```

### 3. Chỉ dẫn khi nhận kết quả Tìm kiếm Web (Web Search Results)
Khi người dùng cho phép tìm kiếm web, prompt định hình câu trả lời cũng được mở khóa định dạng Markdown.

*   **Vị trí cần sửa**: `WEB_GRANTED_REPLY_INSTRUCTIONS` tại [agent_voice_gpt_realtime.py:L134-L144](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py#L134-L144).
*   **Prompt tiếng Anh đề xuất**:
    ```text
    - Answer in Vietnamese only, briefly.
    - You are encouraged to use Markdown formatting (such as bold text, headings, and bullet/numbered lists) to structure your explanation clearly based on the web results.
    - If the web result is weak or incomplete, say so.
    ```

### 4. Phát hiện quan trọng: Hàm chuẩn hóa văn bản làm phẳng Markdown (Flatten Newlines)
*   **Vấn đề**: Trong quá trình dò quét mã nguồn, chúng tôi phát hiện ra hàm [normalize_transcript_text](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/transcript_store.py#L18-L23) trong [transcript_store.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/transcript_store.py):
    ```python
    def normalize_transcript_text(text: str) -> str:
        return " ".join((text or "").split())
    ```
    Hàm này được gọi tự động mỗi khi lưu và gửi tin nhắn của cả User lẫn Assistant qua LiveKit hoặc DB (`save_and_publish_assistant`, `save_and_publish_user`).
    Cơ chế `.split()` không tham số của Python sẽ gộp toàn bộ khoảng trắng bao gồm ký tự xuống dòng (`\n`), và `" ".join()` sẽ biến văn bản nhiều dòng thành một dòng duy nhất được ngăn cách bởi dấu cách.
    Điều này làm biến mất toàn bộ các ngắt dòng của Markdown (chẳng hạn các thẻ list `-`, tiêu đề `#`, hoặc cấu trúc bảng), khiến Frontend nhận về một chuỗi văn bản phẳng dẹt và làm hỏng hiển thị Markdown.
*   **Giải pháp đã triển khai**:
    Thay đổi logic hàm `normalize_transcript_text` để chuẩn hóa khoảng trắng trên từng dòng một cách độc lập và ghép lại bằng ký tự ngắt dòng (`\n`), từ đó bảo toàn nguyên vẹn cấu trúc Markdown gốc:
    ```python
    def normalize_transcript_text(text: str) -> str:
        if not text:
            return ""
        lines = text.splitlines()
        normalized_lines = [" ".join(line.split()) for line in lines]
        return "\n".join(normalized_lines)
    ```

---

## Kế hoạch triển khai

1.  **Cập nhật các hằng số prompt**:
    *   `GREETING_INSTRUCTIONS`
    *   `VOICE_AGENT_INSTRUCTIONS`
    *   `TEXT_AGENTIC_SYSTEM_INSTRUCTIONS`
    *   `WEB_GRANTED_REPLY_INSTRUCTIONS`
2.  **Kiểm tra hoạt động**:
    *   Chạy test suite để đảm bảo không bị lỗi cú pháp hay hỏng cấu trúc logic.
    *   Thực hiện kết nối thử nghiệm phiên Voice để xác thực tác vụ chào hỏi đầu tiên không kích hoạt RAG.
