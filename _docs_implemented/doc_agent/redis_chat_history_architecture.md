# Báo Cáo Chi Tiết: Triển Khai Redis Cho Lịch Sử Hội Thoại (ChatContext)

Tài liệu này quy chuẩn hóa **Business Logic** và **Luồng hoạt động (Flows)** khi tích hợp Redis để xử lý bài toán "Ghi nhớ ngữ cảnh hội thoại cho LiveKit Agent trong cửa sổ Reconnect (Warm Room 35s)".

Đây là Use Case hoàn hảo: Sử dụng Redis làm Trạng thái Phiên (Session State) để biến các Python Worker xử lý AI thành dạng **Stateless (Không lưu trạng thái nội tại)**.

---

## 1. Cốt Lõi Kiến Trúc (Core Concept)

- **Thay đổi tư duy:** Không giữ Agent sống dặt dẹo khi user rớt mạng (`close_on_disconnect=True`). Agent sẽ "chết" ngay lập tức để giải phóng tài nguyên (tránh STT/VAD bị treo).
- **Vai trò của Redis:** Đóng vai trò là "Bộ Não Mở Rộng". Khi Agent A chết, nó đã kịp ghi nhớ toàn bộ cuộc hội thoại vào Redis. Khi user reconnect trong vòng 35s, Agent B (mới tinh) được sinh ra, ngay lập tức đọc não từ Redis và tiếp tục câu chuyện mượt mà.

---

## 2. Cấu Trúc Dữ Liệu Trên Redis

Dữ liệu hội thoại (`ChatContext`) của LLM là chuỗi các tin nhắn dạng text. Redis lưu trữ tốt nhất dưới dạng **JSON String**.

- **Key:** `agent_context:{book_id}_{user_id}` (hoặc `room_id`). VD: `agent_context:book123_user456`
- **Value:** Mảng JSON các tin nhắn.
  ```json
  [
    { "role": "system", "text": "Bạn là trợ lý TRIAM..." },
    { "role": "user", "text": "Tóm tắt chương 1 cho tôi" },
    { "role": "assistant", "text": "Chương 1 nói về..." }
  ]
  ```
- **TTL (Time-To-Live):** `40 giây` (Dư dả hơn 35s của frontend một chút để đảm bảo an toàn mốc thời gian reconnect).

---

## 3. Business Logic & Luồng Xử Lý (Flows)

### Luồng 1: Khởi tạo/Phục hồi phiên (Khi User Join hoặc Reconnect)

_Xảy ra tại hàm `entrypoint`, trước khi gọi `session.start()`._

1. **Truy xuất Redis:** Agent lấy cấu trúc JSON từ key `agent_context:{room_id}`.
2. **Kiểm tra:**
   - **Nếu KHÔNG có (Hoặc TTL đã hết hạn):** Đây là phiên mới hoàn toàn (hoặc user đã bỏ đi quá lâu). Agent khởi tạo `initial_ctx = llm.ChatContext()` trống rỗng, chỉ add System Prompt.
   - **Nếu CÓ dữ liệu:** Đây là pha Reconnect! Agent parse JSON, nạp toàn bộ các object `{role, text}` vào `initial_ctx`.
3. **Thực thi:** Gọi `session.start(initial_ctx=initial_ctx)`. Lúc này Agent B có trí nhớ y hệt Agent A.

### Luồng 2: Cập nhật thời gian thực (Lưu trữ vào Redis)

_Xảy ra liên tục trong suốt quá trình user đang nói chuyện._

1. **Lắng nghe Event:** Lợi dụng event của LiveKit Agent: `@session.on("user_speech_committed")` và `@session.on("agent_speech_committed")`. Đồng thời áp dụng cho cả Data Channel (Text Chat).
2. **Logic Cập nhật (Save):**
   - Mỗi khi User vừa nói xong 1 câu, hoặc Agent vừa trả lời xong 1 câu -> Trigger hàm lưu.
   - Lấy toàn bộ mảng `session.chat_ctx.messages` hiện tại, convert sang JSON.
   - Ghi đè (SET) vào key Redis `agent_context:{room_id}`.
3. **Gia hạn TTL (Reset Timer):** Cứ mỗi lần lưu, bắt buộc set lại TTL của Key này về `40 giây`.
   _(Nghĩa là: Nếu họ cứ nói chuyện liên tục, Key này không bao giờ bị xóa. Chỉ khi phòng im lặng hoàn toàn vô tác động, hoặc user rớt mạng, đồng hồ 40s đếm ngược mới thực sự trôi về 0)._

### Luồng 3: User Đứt Kết Nối (Disconnect)

1. User rớt mạng (Mạng chập chờn, tắt app đột ngột).
2. LiveKit Server nhận diện disconnected -> Phát tín hiệu đóng Room.
3. Python Worker nhận tín hiệu -> **Tự sát (Kill Job/Worker)**. Giải phóng RAM, ngắt sạch WebSocket của STT Deepgram, giải phóng bộ đệm VAD Silero.
4. **Redis:** Bắt đầu lùi bộ đếm TTL từ 40s lùi dần về 0.
5. Nếu user quay lại ở giây thứ 30 -> Kích hoạt lại **Luồng 1**.

---

## 4. Mô phỏng Code Tích Hợp (Pseudocode)

Dưới đây là hình dung cách các mảnh ghép ráp vào file `agent_voice.py`:

```python
import json
import redis.asyncio as redis
from livekit.agents import llm

# Khởi tạo Redis Client
redis_client = redis.Redis.from_url("redis://localhost:6379", decode_responses=True)
TTL_SECONDS = 40

async def entrypoint(ctx: JobContext):
    room_id = ctx.room.name
    redis_key = f"agent_context:{room_id}"

    # --- LUỒNG 1: LOAD CONTEXT TỪ REDIS ---
    initial_ctx = llm.ChatContext()
    saved_context = await redis_client.get(redis_key)

    if saved_context:
        # User RECONNECT: Phục hồi trí nhớ
        print("[Redis] Khôi phục lịch sử chat cho reconnect!")
        messages = json.loads(saved_context)
        for msg in messages:
            initial_ctx.messages.append(
                llm.ChatMessage(role=msg["role"], content=msg["text"])
            )
    else:
        # NEW SESSION: Bắt đầu mới
        initial_ctx.append(role="system", text="Bạn là trợ lý TRIAM...")

    # Start Session với initial_ctx
    session = AgentSession(...)
    await session.start(room=ctx.room, initial_ctx=initial_ctx, ...)

    # --- LUỒNG 2: SAVE CONTEXT LIÊN TỤC VÀ GIA HẠN TTL ---
    async def backup_to_redis():
        # Trích xuất lịch sử hiện tại của session
        msgs_to_save = [{"role": m.role, "text": m.content} for m in session.chat_ctx.messages]
        # Lưu vào Redis và set lại TTL 40s
        await redis_client.setex(redis_key, TTL_SECONDS, json.dumps(msgs_to_save))

    @session.on("user_speech_committed")
    async def on_user_speech(msg: llm.ChatMessage):
        await backup_to_redis()

    @session.on("agent_speech_committed")
    async def on_agent_speech(msg: llm.ChatMessage):
        await backup_to_redis()

    # Text Input qua Data Channel cũng gọi backup_to_redis() sau khi user nạp text!
```

## 5. Tại sao kiến trúc này lại hoàn hảo ("Match 100%")?

1. **Khắc phục lỗi "Câm/Điếc":** Tiến trình Python lúc nào cũng MỚI. STT (Deepgram) và VAD (Silero) không còn nguy cơ bị "kẹt buffer" hay timeout rớt mạng vì tàn dư của kết nối cũ nữa. Mọi thứ đều fresh và nhạy bén.
2. **Luôn nối tiếp câu chuyện:** Dù server thay người xử lý bên dưới, trí nhớ LLM được bưng nguyên vẹn sang, user không hề có cảm giác bị "mất kết nối".
3. **An toàn tài nguyên:** Việc tự động xoá Session Data sau 40s (qua TTL) là hoàn toàn native trên RAM. Không cần viết script dọn dẹp rác, không tạo gánh nặng lưu trữ I/O cho ổ cứng (như PostgreSQL).
4. **Mở rộng dễ dàng (Scalability):** Sang năm nếu App có 100,000 users, bạn scale Backend lên 10 Server Python chạy song song. Bất kể user Reconnect và bị bắn ngẫu nhiên vào Server số 2 hay Server số 9, Server đó đều trỏ về Redis tập trung và bốc đúng cái Ngữ cảnh đang nói dở lên. Đây chính là Distributed System (Hệ thống phân tán) đích thực!
