# Báo cáo: Vấn đề thiết kế Room Name = book_id và đề xuất giải pháp

## Tóm tắt

Câu hỏi của bạn: **"Việc đặt Room Name = book_id có phải là nguyên nhân gây ra vấn đề không?"**

**Câu trả lời: CÓ — đây đúng là nguyên nhân gốc rễ.** Nhưng vấn đề chính không phải là RAG bị sai, mà là **Agent nhận được request từ một session cũ còn sót lại trong phòng**, dẫn đến context bị trộn lẫn và hành vi không xác định.

---

## Phân tích nguyên nhân chi tiết

### 1. Thiết kế hiện tại (đang gây lỗi)

```
User mở sách A  →  FE gọi GET /live-token/{book_id_A}
                →  BE tạo token với room=book_id_A
                →  FE kết nối vào room "book_id_A"
                →  LiveKit dispatch Agent vào room "book_id_A"
                →  Agent đọc book_id từ ctx.room.name ← đây là "book_id_A"
```

**Vấn đề xuất hiện khi:**

```
[Session 1 - 9:00] User A mở sách A → room "book_id_A" được tạo, Agent A chạy
[Session 1 - 9:05] User A đóng app → room "book_id_A" đóng, Agent A giải phóng

[Session 2 - 9:10] User A (hoặc B) mở sách A lần 2 → room "book_id_A" được tạo LẠI
                   → Agent MỚI được dispatch vào room "book_id_A"
                   → Agent đọc ctx.room.name = "book_id_A" ✅ (đúng)
                   → NHƯNG: Session 1 vẫn còn context "lk.chat" tồn đọng trong room buffer
                   → Agent mới nhận message cũ từ session 1 → trả lời lạc đề
```

Bạn thấy trên **LiveKit Cloud Dashboard**:

- `RM_WpR7MdzST8ao` → room name = `140376bf-3e5f-491d-95fc-dd82d33fd64d`
- `RM_Jg5QswwZxQ2P` → room name = `140376bf-3e5f-491d-95fc-dd82d33fd64d` (cùng tên!)
- `RM_jjpn4Bj8PWTm` → room name = `140376bf-3e5f-491d-95fc-dd82d33fd64d` (cùng tên!)

→ **Tất cả đều là cùng 1 cuốn sách, nhưng nhiều phiên khác nhau.** Mỗi Room ID khác nhau (RM_xxx) nhưng Room Name giống nhau. Đây là thiết kế của LiveKit: Room Name = định danh logic, Room ID = định danh vật lý từng instance.

### 2. Tại sao Agent đôi khi bị "lú" (confused context)?

Trường hợp nguy hiểm: **User ngắt kết nối nhưng Agent chưa kịp tắt hoàn toàn**, rồi ngay lập tức một session mới bắt đầu vào cùng room name. LiveKit có thể reuse room đó trước khi nó đóng hoàn toàn.

Trong test của bạn, Agent trả lời:

> _"Chào bạn 👋 Bạn muốn mình đọc hay tóm tắt cuốn sách nào?"_

Thay vì tìm trong sách. Điều này xảy ra vì **Agent này thuộc về một session cũ đang còn sống trong room** và nhận được câu hỏi của bạn. Agent cũ đó không biết `book_id` nào đang được hỏi vì nó được init bằng một `ChatContext` trắng mới.

---

## So sánh: Thiết kế hiện tại vs. Đề xuất

|                                      | Hiện tại (Room = book_id)              | Đề xuất (Room = session_id)        |
| ------------------------------------ | -------------------------------------- | ---------------------------------- |
| **Room name**                        | `140376bf-3e5f-491d-95fc-dd82d33fd64d` | `sess_140376bf_a3f9c1` (uuid ngắn) |
| **book_id truyền cho Agent**         | Đọc từ `ctx.room.name`                 | Đọc từ `ctx.job.metadata` (JSON)   |
| **Tách biệt session**                | ❌ Các phiên chia sẻ room name         | ✅ Mỗi phiên có room riêng         |
| **Session cũ ảnh hưởng session mới** | ✅ Có thể                              | ❌ Không thể                       |
| **Nhiều user cùng mở 1 sách**        | ❌ Vào chung 1 phòng                   | ✅ Mỗi user phòng riêng            |

---

## Giải pháp đề xuất: Dùng Job Metadata thay vì Room Name

### Bước 1: Sửa file `app/api/v1/endpoints/live.py`

Thay vì dùng `book_id` làm room name, tạo 1 session UUID ngắn làm room name. Truyền `book_id` qua `metadata` của `RoomAgentDispatch`.

```python
# TRƯỚC (đang gây lỗi):
agent_dispatch = api.RoomAgentDispatch(agent_name=settings.LIVEKIT_AGENT_NAME)
room_config = api.RoomConfiguration(name=book_id, agents=[agent_dispatch])
token = (
    api.AccessToken(...)
    .with_grants(api.VideoGrants(room_join=True, room=book_id))
    .with_room_config(room_config)
)
```

```python
# SAU (đề xuất - fix triệt để):
import json, uuid

# Tạo room name duy nhất cho mỗi session
session_room_name = f"triam_{book_id[:8]}_{uuid.uuid4().hex[:6]}"

# Truyền book_id qua metadata của Agent Dispatch (không phải room name)
agent_dispatch = api.RoomAgentDispatch(
    agent_name=settings.LIVEKIT_AGENT_NAME,
    metadata=json.dumps({"book_id": book_id})   # ← KEY FIX
)
room_config = api.RoomConfiguration(agents=[agent_dispatch])

token = (
    api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
    .with_identity(f"user_{uuid.uuid4().hex[:6]}")
    .with_grants(api.VideoGrants(room_join=True, room=session_room_name))  # ← room mới mỗi session
    .with_room_config(room_config)
)
return {"token": token.to_jwt(), "room_name": session_room_name}
```

### Bước 2: Sửa file `app/services/agent_voice.py`

Thay vì đọc `book_id` từ `ctx.room.name`, đọc từ `ctx.job.metadata`.

```python
# TRƯỚC (đang gây lỗi):
async def entrypoint(ctx: JobContext):
    await ctx.connect()
    book_id = ctx.room.name   # ← Đây là room name (session UUID mới), KHÔNG còn là book_id!
```

```python
# SAU (đề xuất - fix triệt để):
import json

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # Đọc book_id từ Job Metadata (được truyền từ token RoomAgentDispatch)
    try:
        job_meta = json.loads(ctx.job.metadata or "{}")
        book_id = job_meta.get("book_id", "")
    except (json.JSONDecodeError, AttributeError):
        book_id = ""

    if not book_id:
        print("[Agent] ❌ Không tìm thấy book_id trong metadata! Thoát.")
        return

    print(f"[Agent] ✅ Book ID từ metadata: {book_id}")
    print(f"[Agent] 🏠 Room Name (session): {ctx.room.name}")
```

---

## Kết luận

|                              | Vấn đề                                  | Mức độ                  |
| ---------------------------- | --------------------------------------- | ----------------------- |
| ❌ Room name = book_id       | Session cũ lẫn sang session mới         | **Nghiêm trọng**        |
| ❌ Nhiều user cùng mở 1 sách | Vào chung 1 phòng, nghe giọng nhau      | **Nghiêm trọng**        |
| ✅ Giải pháp đề xuất         | Room = UUID riêng, book_id qua metadata | **An toàn, đúng chuẩn** |

**Mức độ thay đổi code:** Nhỏ - chỉ 2 file (`live.py` và `agent_voice.py`), không ảnh hưởng logic RAG, TTS, hay STT.

> Nếu bạn approve, tôi sẽ fix trực tiếp 2 file này ngay bây giờ.
