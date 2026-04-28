# Báo Cáo Nghiên Cứu: Tối Ưu Hóa LiveKit Agent (Voice & Chat)

Dựa trên tài liệu mới nhất của LiveKit Agents Framework (2026) và kiến trúc dự án Triam Backend của bạn, dưới đây là phân tích chi tiết và đề xuất giải pháp cho 2 vấn đề bạn đang gặp phải.

---

## Vấn đề 1: Lưu Trữ Lịch Sử Hội Thoại (Conversation History Persistence)

### Hiện trạng

LiveKit Agent có một đối tượng `session.history` (hoặc `ChatContext`) lưu trữ toàn bộ bối cảnh cuộc gọi hiện tại. Tuy nhiên, khi ngắt kết nối (session kết thúc), context này bị hủy theo RAM của worker. Nếu user gọi lại, agent sẽ "mất trí nhớ".

### Giải pháp tối ưu

Để xử lý chuyên nghiệp, chúng ta không đợi session kết thúc mới lưu, mà sẽ **lưu theo thời gian thực (Real-time Streaming)** vào Database (PostgreSQL) thông qua các Event Hooks của LiveKit, và **khôi phục (Restore)** lại lịch sử khi user bắt đầu session mới.

#### Bước 1: Thiết kế Database (SQLModel)

Tạo thêm một bảng `AgentChatLog` để lưu từng câu thoại.

```python
# app/models/db_models.py
class AgentChatLog(SQLModel, table=True):
    __tablename__ = "agent_chat_logs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(index=True)
    role: str # "user" hoặc "agent"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Bước 2: Bắt sự kiện (Event Hook) để lưu lịch sử

Trong file `agent_voice.py`, bạn có thể lắng nghe các sự kiện khi user nói xong hoặc agent nói xong để ghi vào DB ngay lập tức.

```python
# Thêm vào trong hàm entrypoint của agent_voice.py
async def entrypoint(ctx: JobContext):
    # ... khởi tạo session ...

    # 1. BẮT SỰ KIỆN LƯU VÀO DB
    @session.on("user_speech_committed")
    def on_user_speech(msg: llm.ChatMessage):
        # Lưu câu nói của User vào DB (Chạy ngầm)
        save_chat_to_db(book_id, "user", msg.content)

    @session.on("agent_speech_committed")
    def on_agent_speech(msg: llm.ChatMessage):
        # Lưu câu trả lời của Agent vào DB
        save_chat_to_db(book_id, "agent", msg.content)

    # 2. KHÔI PHỤC LỊCH SỬ KHI BẮT ĐẦU
    # Lấy 10-20 câu thoại gần nhất từ DB để nạp vào Context
    past_history = get_chat_history_from_db(book_id, limit=20)

    # Khởi tạo context ban đầu
    initial_ctx = llm.ChatContext()
    for log in past_history:
        initial_ctx.append(role=log.role, text=log.content)

    # Kèm thêm System Prompt
    initial_ctx.append(role="system", text="Bạn là trợ lý TRIAM...")

    # Truyền context vào lúc start
    await session.start(
        room=ctx.room,
        agent=TriamAssistant(book_id=book_id),
        initial_ctx=initial_ctx, # Nạp trí nhớ cho Agent ở đây!
        # ...
    )
```

> **Lợi ích:** Dù user văng app, rớt mạng, hay chủ động tắt đi gọi lại 1 tháng sau, Agent vẫn nhớ rõ đang nói chuyện tới đâu.

---

## Vấn đề 2: Tích Hợp Chat Text + Voice Trong Cùng 1 Session

Bạn tư duy hoàn toàn chính xác! LiveKit Agent (đặc biệt là `VoicePipelineAgent` hoặc kiến trúc Multimodal mới) được thiết kế mặc định để xử lý song song cả Text và Audio thông qua Data Channels.

User đang nghe voice nhưng không tiện nói (đang ở chỗ ồn), user gõ chữ vào ô Chat -> Agent vẫn hiểu và có thể trả lời bằng Voice (hoặc cả Voice + Text).

### Cách hoạt động trong LiveKit

LiveKit có một Data Channel mặc định tên là `lk.chat`. Agent tự động lắng nghe topic này.

#### 1. Cấu hình Backend (Python)

Trong `agent_voice.py`, bạn cần cấu hình để agent chấp nhận cả text và trả lời bằng text nếu cần:

```python
    await session.start(
        room=ctx.room,
        agent=TriamAssistant(book_id=book_id),
        room_options=room_io.RoomOptions(
            # Chấp nhận user gửi Text chat lên
            text_input=room_io.TextInputOptions(enabled=True),
            # Agent có thể đồng thời trả về text transcript xuống màn hình chat
            text_output=room_io.TextOutputOptions(enabled=True)
        )
    )
```

Khi user gõ text, sự kiện Text sẽ được nạp thẳng vào LLM giống hệt như khi user nói. LLM xử lý xong, câu trả lời sẽ được chuyển qua TTS đọc lên, **đồng thời** đoạn text đó sẽ được bắn ngược lại Room qua Data Channel để hiển thị lên màn hình chat của app Flutter.

#### 2. Phía Client (App Flutter)

Bạn không cần viết API backend riêng cho tính năng chat này. App Flutter sử dụng trực tiếp SDK LiveKit để gửi tin nhắn vào phòng:

```dart
// Ví dụ logic trên Flutter
import 'package:livekit_client/livekit_client.dart';

// Khi user bấm nút gửi tin nhắn text:
Future<void> sendChatMessage(Room room, String message) async {
  // Gửi data qua Data Channel mặc định cho Chat
  await room.localParticipant?.publishData(
    utf8.encode(message),
    topic: 'lk.chat', // Bắt buộc dùng topic này để Agent nhận diện
  );
}
```

### Cách Agent Xử lý "Multimodal" (Đa phương thức)

Với LiveKit:

1. **User NÓI:** `Audio -> STT (Chuyển thành chữ) -> Context LLM -> LLM sinh câu trả lời -> TTS đọc lên + Bắn text xuống`
2. **User GÕ CHỮ:** `Data Channel -> Context LLM -> LLM sinh câu trả lời -> TTS đọc lên + Bắn text xuống`

Cả 2 hành động đều đi chung vào 1 bộ não (LLM ChatContext), nên lịch sử hội thoại sẽ xen kẽ tự nhiên (Vd: User nói -> Agent nói -> User gõ chữ -> Agent nói...). Bạn vẫn dùng Hook ở **Vấn đề 1** để lưu lịch sử bình thường.

---

## 🎯 Đề xuất Kế Hoạch Triển Khai (Action Plan)

Nếu bạn đồng ý với hướng giải quyết trên, chúng ta có thể thực hiện theo các bước sau:

1. **Database:** Tạo model `AgentChatLog`, migrate DB.
2. **CRUD:** Tạo 2 hàm `save_chat_to_db` và `get_chat_history_from_db`.
3. **Agent Backend:** Update file `app/services/agent_voice.py`:
   - Lắng nghe event để lưu log.
   - Nạp `initial_ctx` lúc khởi động.
   - Bật `TextInputOptions` và `TextOutputOptions`.
4. **App Flutter:** Tích hợp ô nhập text gọi lệnh `publishData(topic: 'lk.chat')` khi đang ở trong phòng thoại.
