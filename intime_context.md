Kết luận: nên nâng cấp từ “Context selector chọn một thread trước khi mở room” thành “Context runtime” gồm:

1. Flutter quan sát context hiện tại.
2. Resolver xếp hạng các context phù hợp.
3. Backend giữ `active_context` có thể thay đổi trong cùng LiveKit room.
4. Agent dùng function calling/RPC để đọc hoặc yêu cầu chuyển context.

Hiện tại Tri Âm đã có nền tảng nhưng context còn bị “đóng băng” khi room khởi tạo.

- `AgentContextResolver` hiện chỉ ưu tiên sách đang nghe, sau đó đến sách gần đây nhất.
- `BookDetail` chưa phải nguồn context ưu tiên cấp một xuyên suốt navigation.
- `startBookSession()` gọi `threads/for-book`, lấy `contextId + threadId`, rồi nếu khác context hiện tại thì disconnect room.
- Backend tạo LiveKit metadata cố định với `thread_id`, `context_id`, `document_ids`. `entrypoint()` đọc các giá trị này một lần và `TriamAssistant` giữ `document_ids` cố định trong suốt session.
- Vì vậy, dù room còn sống, “ngữ nghĩa agent đang hiểu” vẫn chỉ thuộc về một context.

Tham chiếu chính: [agent_context_resolver.dart](D:/tri-am/lib/features/agent/presentation/providers/agent_context_resolver.dart), [agent_provider.dart](D:/tri-am/lib/features/agent/presentation/providers/agent_provider.dart), [live_service.py](D:/triam-backend/app/services/live_service.py), [agent_voice_gpt_realtime.py](D:/triam-backend/app/services/agent_voice_gpt_realtime.py).

**1. Context nên được hiểu như một snapshot**

Flutter nên duy trì một `AgentAppContextSnapshot`, cập nhật khi người dùng:

- mở `BookDetail(bookId)`;
- bắt đầu hoặc đổi audiobook;
- mở một reading-plan session;
- mở Knowledge Context;
- chọn thread cụ thể;
- chuyển sang màn hình tổng quan hoặc không còn context rõ ràng.

Ví dụ:

```json
{
  "route": "book_detail",
  "book_id": "book-123",
  "book_title": "Atomic Habits",
  "learning_unit_id": "unit-7",
  "selected_context_id": "context-abc",
  "selected_thread_id": "thread-xyz",
  "is_playing": true,
  "source": "book_detail",
  "updated_at": "..."
}
```

Snapshot này không nên gửi liên tục. Chỉ gửi khi route, sách, thread hoặc trạng thái nghe thay đổi.

LiveKit participant attributes phù hợp cho trạng thái nhỏ và ít thay đổi; data packet phù hợp cho event tức thời; RPC phù hợp cho request-response như `get_current_context` hoặc `switch_context`. LiveKit cũng giới hạn attributes cho cập nhật không thường xuyên, còn RPC hỗ trợ payload tối đa 15 KiB và có timeout rõ ràng. [Participant attributes](https://docs.livekit.io/transport/data/state/participant-attributes/), [RPC](https://docs.livekit.io/transport/data/rpc/), [Data overview](https://docs.livekit.io/transport/data/)

**2. Resolver nên ưu tiên context theo thứ tự**

Đề xuất thứ tự:

| Ưu tiên | Nguồn | Hành vi |
|---|---|---|
| 1 | Thread người dùng vừa chọn | Giữ nguyên, không tự đổi |
| 2 | BookDetail đang mở | Context của sách hiện tại |
| 3 | Sách đang nghe | Chọn sách/audio hiện tại |
| 4 | Reading-plan session đang mở | Chọn book + learning unit |
| 5 | Knowledge Context đang xem | Chọn context/thread tương ứng |
| 6 | Context gần đây | Chỉ dùng khi không có context màn hình |
| 7 | Không xác định | Hiển thị picker hoặc hỏi người dùng |

Điểm quan trọng: `BookDetail` và audiobook phải trở thành nguồn sự thật về “người dùng đang quan tâm gì”, không chỉ là fallback trong `AgentContextResolver`.

Không nên để LLM tự đoán từ tên màn hình. Flutter biết chính xác `bookId`; agent chỉ nên nhận snapshot đã chuẩn hóa.

Nên thêm điểm tin cậy:

```text
explicit_thread       = 1.00
book_detail           = 0.95
active_audio          = 0.90
reading_plan_session  = 0.85
knowledge_context     = 0.80
recent_context        = 0.50
```

Nếu context mới có điểm thấp hơn context đang hoạt động, không tự chuyển giữa chừng. Chỉ chuyển khi người dùng nói rõ như “chuyển sang sách này”, chọn picker, hoặc agent hỏi xác nhận.

**3. Context selector nên trở thành “context switcher”**

UI không nên chỉ hiển thị danh sách context. Nó nên có:

- Context hiện tại: “Đang nói về …”
- Nguồn hiện tại: “Màn hình đang mở”, “Sách đang nghe”, “Thread đã chọn”
- 2-3 context đề xuất
- Recent contexts
- Nút chuyển nhanh
- Preview trước khi voice bắt đầu

Ví dụ khi ở Book Detail:

```text
Ngữ cảnh hiện tại
Atomic Habits
Chương 3 · Thread chính

Đề xuất
• Sách đang nghe: Atomic Habits
• Thread gần đây: Ôn tập chương 2
• Ngữ cảnh: Tâm lý học hành vi
```

Start Live nên dùng chính danh sách này. Không cần mở picker đầy đủ nếu resolver có context chắc chắn; chỉ cần cho người dùng thấy “context mình sắp bắt đầu là gì”.

**4. Không nên dùng function calling để tự lấy context từ Flutter trước tiên**

Backend hiện đã có function calling cho RAG và web search. Phần còn thiếu không phải là cơ chế function calling, mà là bộ tool thuộc nhóm “context control”.

Nên chia thành hai loại:

Các tool chạy trực tiếp ở backend:

```text
get_active_context()
list_available_contexts(query?)
resolve_context_for_book(book_id)
switch_active_context(context_handle)
```

Các tool cần frontend thông qua LiveKit RPC:

```text
get_app_context()
get_visible_screen()
open_context_picker()
navigate_to_context(context_handle)
```

Agent không nên truyền raw UUID tùy ý. Backend nên trả về các `context_handle` ngắn hạn, có quyền truy cập và phiên bản:

```json
{
  "handle": "candidate_1",
  "thread_id": "...",
  "context_id": "...",
  "title": "Atomic Habits",
  "reason": "book_detail",
  "confidence": 0.95,
  "version": 4
}
```

Sau đó agent gọi:

```text
switch_active_context(handle="candidate_1")
```

Backend kiểm tra ownership, resolve lại context, rồi mới chuyển.

**5. Giải pháp tối ưu: giữ nguyên room, thay đổi active context**

Không nên reconnect LiveKit khi đổi context. Cần tách:

```text
LiveKit room/session
    giữ nguyên

Active agent context
    thay đổi được

Transcript persistence target
    thay đổi theo thread

RAG scope
    reload hoặc lazy-load theo context
```

Backend nên có state dạng:

```python
@dataclass
class ActiveContext:
    context_id: UUID
    thread_id: UUID
    document_ids: set[UUID]
    version: int
    switching: bool = False
```

Hiện tại `document_ids`, `thread_uuid`, `grounding_router` và `VoiceTranscriptStore` được tạo theo context ban đầu. Cần refactor để chúng đọc `session_state.active_context` thay vì đóng cứng giá trị lúc `entrypoint()` chạy.

Khi chuyển context:

1. Agent phát âm ngắn: “Được, tôi chuyển sang Atomic Habits.”
2. Đánh dấu session là `SWITCHING`.
3. Hủy hoặc chờ turn hiện tại.
4. Backend xác thực context/thread mới.
5. Load hoặc prewarm RAG scope mới.
6. Đổi transcript target sang thread mới.
7. Gửi `context.changed`.
8. Agent tiếp tục trong cùng room.

LiveKit Agents hỗ trợ cập nhật instructions/tools trong lúc session đang chạy, nên cách này phù hợp với mô hình active context mutable. [Agent session](https://docs.livekit.io/agents/logic/sessions/), [Function tools](https://docs.livekit.io/agents/logic/tools/definition/)

Điều cần tránh là trộn lịch sử hai thread vào cùng một conversation history. Room có thể liên tục, nhưng lịch sử nghiệp vụ vẫn phải tách theo `threadId`.

**6. Contract backend nên bổ sung**

Có thể thiết kế ba nhóm API/control:

```text
GET  /api/v1/agent/context-candidates
POST /api/v1/agent/context/resolve
POST /api/v1/agent/context/switch
```

Trong đó `context-candidates` nên trả một lần:

- context hiện tại;
- thread hiện tại;
- book đang mở;
- book đang nghe;
- các context gần đây;
- canonical thread cho mỗi book.

Như vậy Flutter không phải gọi nhiều endpoint tuần tự mỗi lần mở Agent.

Trong room, dùng event:

```json
{
  "type": "context.snapshot",
  "route": "book_detail",
  "book_id": "...",
  "thread_id": "..."
}
```

và:

```json
{
  "type": "context.switch.request",
  "handle": "candidate_1",
  "request_id": "..."
}
```

Phản hồi:

```json
{
  "type": "context.switch.ack",
  "request_id": "...",
  "context_id": "...",
  "thread_id": "...",
  "version": 5
}
```

Nếu agent tự gọi function `switch_active_context`, backend có thể phát event `context.changed` xuống Flutter để UI cập nhật đồng bộ.

**7. Tối ưu tốc độ/kết nối**

Ưu tiên triển khai theo thứ tự này:

1. Resolve context local từ route, playback và state Riverpod.
2. Prefetch `threads/for-book` ngay khi mở Book Detail hoặc bắt đầu nghe.
3. Cache mapping `bookId -> contextId/threadId`.
4. Kết nối room một lần và giữ warm room khi chuyển text/background.
5. Load thread history bất đồng bộ sau khi room sẵn sàng.
6. Khi đổi context, chỉ đổi backend session state, không đổi room.
7. Prewarm RAG scope cho 1-2 context đề xuất.
8. Chỉ reconnect khi token hết hạn, room hỏng hoặc session không thể migrate.

Hiện tại app đã có warm room cho soft-stop, nhưng `startBookSession()` vẫn hard-disconnect khi context/thread thay đổi. Đây là điểm có khả năng giảm độ trễ lớn nhất.

**8. Lộ trình khả thi**

P0, chỉ Flutter:

- Chuẩn hóa `AgentAppContextSnapshot`.
- Gắn Book Detail vào snapshot.
- Gắn audiobook playback vào snapshot.
- Resolver theo ranking.
- Hiển thị context preview trước Start Live.
- Cache `bookId -> AgentBookThread`.

P1, backend không cần LLM tool:

- Thêm `context.snapshot` và `context.switch` qua `lk.control`.
- Backend có `ActiveContextState`.
- Chuyển transcript/RAG scope theo active context.
- Giữ nguyên room khi switch.
- Thêm version và request id để chống race condition.

P2, agentic context:

- Thêm `list_context_candidates`.
- Thêm `switch_active_context`.
- Thêm frontend RPC `get_app_context`.
- Cho agent yêu cầu mở picker khi confidence thấp.

P3, tối ưu nâng cao:

- Prefetch context candidates.
- Prewarm RAG scope.
- Context summary khi rời thread.
- Metrics:
  - `context_resolve_ms`
  - `context_switch_ack_ms`
  - `room_reconnect_count`
  - `time_to_first_audio_after_switch`
  - `switch_failure_rate`
  - `wrong_context_rate`

Định hướng nên chọn là: “một room, nhiều active context tuần tự”, không phải “một room chứa nhiều context đồng thời”. Nhiều context đồng thời sẽ làm RAG, transcript và quyền truy cập khó kiểm soát hơn; còn context tuần tự vẫn giữ được cảm giác agent liên tục nhưng bảo toàn ranh giới thread.

Phân tích này tự động sinh trước commit 8edb6cc0cf94b4d1a19a233521fc884c62ccc2c2 của FE nên xem xét ngữ cảnh trước khi triển khai vì fe đã có tương thích tạm thời