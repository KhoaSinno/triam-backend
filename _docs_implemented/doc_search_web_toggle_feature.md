# Báo cáo Nghiên cứu (v2 - Phiên bản Đã Cải tiến)
# Tính năng: Smart Web Search Toggle

Tài liệu: `_docs_implemented/doc_search_web_toggle_feature.md`

---

## Lý do Thiết kế Lại

Phiên bản đầu tiên có hai vấn đề logic nghiêm trọng:
- **Feature 1:** `if rag_empty` là điều kiện mù. RAG luôn trả về *gì đó* nếu database có dữ liệu, nhưng dữ liệu đó có thể hoàn toàn không liên quan đến câu hỏi. Chỉ **LLM mới đủ thông minh** để phán xét mức độ liên quan.
- **Feature 2:** Hardcode keywords xác nhận là anti-pattern. "Ừ", "Ok ạ", "Thôi cũng được", "Sure bro"... có vô hạn cách đồng ý không thể liệt kê hết.

**Triết lý thiết kế mới:** Nhường quyền phán xét ngữ nghĩa cho LLM. Code chỉ làm nhiệm vụ routing và truyền dữ liệu.

---

## 1. Kết luận Nghiên cứu: Hoàn toàn Khả Thi ✅

Sau khi kiểm tra trực tiếp mã nguồn của `livekit-agents` v1.5.8:

| Cơ chế cần dùng | API thực tế | Mô tả |
|---|---|---|
| `LLMStream.collect()` | ✅ Đã verify | Thu gọn stream thành `CollectedResponse` gồm `.text` và `.tool_calls` |
| `llm.execute_function_call(tc, tool_ctx)` | ✅ Đã verify | Thực thi tool call từ LLM, trả về `FunctionCallResult` |
| `ctx.insert(result.fnc_call)` | ✅ Docs chính thức | Nạp kết quả tool vào ChatContext để LLM đọc |
| Tool thiết kế 2 pha cho Voice | ✅ Best practice | LLM tự phân tích câu trả lời của user qua natural conversation turn |

---

## 2. Tính năng 1: Toggle Search Web cho Text Chat

### Vấn đề Cốt lõi Cần Giải quyết
Không thể dùng code logic để biết RAG kết quả có đủ hay không. Giải pháp: **dùng chính `gpt-4o-mini` để phán xét và quyết định gọi tool**.

### Giải pháp: Agentic Loop với `collect()` API

Khi toggle BẬT, thay vì Naive RAG, ta chuyển `gpt-4o-mini` sang **chế độ Agentic** với đúng 2 tools: `search_book_knowledge` và `search_web`. Framework (`llm.execute_function_call`) sẽ tự xử lý tool call, không cần code tay.

**Luồng thực thi:**
```
User gõ → gpt-4o-mini phân tích → gọi search_book_knowledge
        → nếu RAG đủ: trả lời ngay
        → nếu RAG không đủ + toggle BẬT: tự gọi search_web → trả lời
        → nếu RAG không đủ + toggle TẮT: thông báo không có thêm thông tin
```

### Code Implement cho `handle_data_input`

```python
async def handle_data_input(text: str, participant_id: str | None) -> None:
    # ... (lưu DB, publish transcript, interrupt, add_message như cũ) ...

    try:
        # --- PHÂN NHÁNH dựa theo trạng thái toggle ---
        if web_search_enabled:
            full_reply = await _chat_with_agentic_loop(text)
        else:
            full_reply = await _chat_naive_rag(text)  # Luồng hiện tại, giữ nguyên

        # ... (lưu reply, publish lk.chat, lk.transcript như cũ) ...
```

**Hàm `_chat_with_agentic_loop` (dùng collect() API):**
```python
async def _chat_with_agentic_loop(user_text: str) -> str:
    """
    Chế độ Agentic: gpt-4o-mini tự quyết định cần dùng tool nào.
    Dùng LLMStream.collect() để handle tool calls đúng cách theo SDK.
    """
    # Tool context chứa ĐÚNG 2 tools
    tool_ctx = llm.ToolContext(tools=[
        agent_instance.search_book_knowledge,
        agent_instance.search_web,
    ])

    ctx = session.history.copy()
    MAX_STEPS = 3  # Giới hạn số vòng lặp tool call để tránh loop vô tận

    for _step in range(MAX_STEPS):
        # 1. Gọi LLM và collect toàn bộ response (cả text lẫn tool_calls)
        response = await chat_llm.chat(
            chat_ctx=ctx,
            tools=tool_ctx.function_tools,
        ).collect()

        # 2. Nếu không có tool call → LLM đã có câu trả lời cuối
        if not response.tool_calls:
            return response.text

        # 3. Thực thi từng tool call theo chuẩn SDK
        for tc in response.tool_calls:
            result = await llm.execute_function_call(tc, tool_ctx)
            ctx.insert(result.fnc_call)           # Ghi tool call vào context
            if result.fnc_call_out:
                ctx.insert(result.fnc_call_out)   # Ghi kết quả tool vào context

    # Nếu hết MAX_STEPS vẫn còn tool call → lấy text cuối cùng
    return response.text
```

**Hàm `_chat_naive_rag` (giữ nguyên luồng hiện tại):**
```python
async def _chat_naive_rag(user_text: str) -> str:
    """Chế độ RAG Naive: luôn search sách, không dùng tool web."""
    search_result = await agent_instance.search_book_knowledge(user_text)
    temp_ctx = session.history.copy()
    if search_result and "RAG don't have data" not in search_result:
        temp_ctx.add_message(
            role="system",
            content=f"Thông tin từ sách:\n{search_result}"
        )
    response = await chat_llm.chat(chat_ctx=temp_ctx).collect()
    return response.text
```

### Truyền Toggle từ Frontend

Frontend gửi JSON qua DataChannel kênh `lk.control` (kênh riêng để không lẫn với chat):
```javascript
// Flutter
room.localParticipant.publishData(
  utf8.encode(json.encode({"type": "toggle_web_search", "enabled": true})),
  reliable: true,
  topic: "lk.control",
);
```

Backend mở rộng `on_data_received` để lắng nghe thêm kênh `lk.control`:
```python
def on_data_received(packet: rtc.DataPacket) -> None:
    try:
        raw = packet.data.decode("utf-8")
        data = json.loads(raw)
    except Exception:
        return

    if packet.topic == "lk.control" and data.get("type") == "toggle_web_search":
        nonlocal web_search_enabled
        web_search_enabled = data.get("enabled", False)
        log.info(f"🌐 Web search toggle: {'BẬT' if web_search_enabled else 'TẮT'}")

    elif packet.topic == "lk.chat":
        asyncio.create_task(handle_data_input(raw, packet.participant.identity if packet.participant else None))
```

---

## 2. Tính năng 2: Voice Agent Hỏi Xác Nhận Trước Khi Search Web

### Vấn đề Cốt lõi Cần Giải quyết
Không thể hardcode keyword xác nhận. **Giải pháp: Để LLM phân tích câu trả lời của user**, vì LLM đã vốn giỏi hiểu ngữ nghĩa tự nhiên.

### Giải pháp: Thiết kế Tool 2 Pha (Two-Step Tool Pattern)

Thay vì code logic `asyncio.Event + keyword matching`, ta thiết kế 2 tools riêng biệt và để **System Prompt hướng dẫn RealtimeModel tự điều phối**:

- **Pha 1 - Tool `ask_web_search_permission(query)`:** AI gọi tool này khi sách không đủ. Tool trả về một chuỗi mẫu câu để AI **tự nói lên** câu hỏi xác nhận với user. Sau đó, AI kết thúc turn, chờ user trả lời.
- **Pha 2 - Tool `execute_web_search(query)`:** AI **chỉ gọi tool này** trong turn tiếp theo, **sau khi** user đã đồng ý. Đây là tool thực sự gọi `search_web`.

**Cơ chế hoạt động nhờ RealtimeModel:**
RealtimeModel (OpenAI) xử lý hội thoại theo từng turn. Khi Pha 1 kết thúc (AI đã hỏi), model sẽ tự động lắng nghe turn giọng nói tiếp theo của user. Vì System Prompt đã chỉ thị rõ logic, model sẽ tự phân tích ngữ nghĩa câu trả lời của user:
- Nếu user đồng ý (dù nói bất kỳ cách nào) → model tự quyết định gọi `execute_web_search`
- Nếu user từ chối → model tự quyết định không gọi tool và trả lời phù hợp

### Thay đổi System Prompt trong `TriamAssistant`

```python
instructions=(
    "Bạn là trợ lý AI sách nói TRIAM.\n"
    "\n"
    "## QUY TẮC TOOL (BẮT BUỘC TUÂN THỦ):\n"
    "- LUÔN gọi 'search_book_knowledge' TRƯỚC TIÊN cho mọi câu hỏi về kiến thức.\n"
    "- Nếu 'search_book_knowledge' không trả về thông tin đủ và liên quan:\n"
    "  → PHẢI gọi 'ask_web_search_permission' để xin phép user.\n"
    "  → TUYỆT ĐỐI KHÔNG gọi 'execute_web_search' trực tiếp mà không có bước xin phép trước.\n"
    "- Chỉ gọi 'execute_web_search' khi user đã xác nhận đồng ý ở turn hội thoại trước.\n"
    "\n"
    "## PHONG CÁCH: Ngắn gọn, không Markdown, không Emoji.\n"
)
```

### Thay đổi Tools trong `TriamAssistant`

```python
# Xóa tool search_web cũ, thay bằng 2 tools mới:

@function_tool
async def ask_web_search_permission(
    self,
    query: Annotated[str, "Nội dung dự kiến sẽ tìm trên web nếu user đồng ý"],
) -> str:
    """
    Gọi tool này khi search_book_knowledge không có đủ thông tin liên quan.
    Tool này KHÔNG tìm web ngay. Nó chỉ trả về mẫu câu hỏi xác nhận.
    AI sẽ đọc câu hỏi này cho user nghe, rồi đợi user trả lời ở turn tiếp theo.
    """
    # Trả về mẫu câu → AI sẽ tự đọc lên bằng giọng nói
    return (
        f"Thông tin về '{query}' không có trong sách. "
        f"Bạn có muốn tôi tìm kiếm thêm trên internet không?"
    )

@function_tool
async def execute_web_search(
    self,
    query: Annotated[str, "Nội dung cần tìm kiếm trên internet"],
) -> str:
    """
    Chỉ gọi tool này SAU KHI user đã xác nhận đồng ý ở turn hội thoại trước đó.
    Thực hiện tìm kiếm thực sự trên internet và trả về kết quả.
    """
    log.info(f"🌐 Thực hiện web search: {query}")
    return await web_search(query)
```

### Tại sao cách này hoàn hảo hơn `asyncio.Event + keyword matching`?

| Tiêu chí | asyncio.Event + hardcode keywords | Two-Step Tool Pattern |
|---|---|---|
| Nhận diện "đồng ý" | Chỉ các từ được liệt kê sẵn | **LLM phân tích toàn bộ ngữ nghĩa** |
| Xử lý tiếng địa phương/tiếng lóng | ❌ Không | ✅ Tự nhiên |
| Xử lý câu phức tạp ("Thôi oke bạn tìm đi nhé") | ❌ Không | ✅ LLM hiểu ngay |
| Code phức tạp | Cao (Event, timeout, cleanup) | **Thấp (chỉ thêm 2 tool functions)** |
| Sử dụng sức mạnh framework | Không | ✅ Hoàn toàn |

---

## 3. Tóm Tắt Thay Đổi Cần Làm

| File | Thay đổi |
|---|---|
| `agent_voice_gpt_realtime.py` | Thêm import `from livekit.agents import llm`; thêm biến `web_search_enabled`; tách hàm `_chat_with_agentic_loop` và `_chat_naive_rag`; mở rộng `on_data_received`; sửa `TriamAssistant.instructions`; thay 2 tools mới |
| Frontend | Gửi JSON `{"type": "toggle_web_search", "enabled": true/false}` qua DataChannel topic `lk.control` |

> [!IMPORTANT]
> Implement và test Feature 1 (Toggle Text) trước. Feature 2 (Voice) chỉ cần sửa tool và prompt, không cần logic code phức tạp. Toàn bộ điều phối được giao cho RealtimeModel xử lý.
