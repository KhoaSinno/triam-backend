# Flutter Spec: LiveKit Realtime Voice/Text + Transcript UI (Triam)

Tài liệu này hướng dẫn FE Flutter implement (Bạn có thể bỏ qua các phần đã implement đúng và clean code) **từng bước** luồng chat voice/text với LiveKit realtime agent theo đúng backend hiện tại.

Phạm vi backend tương ứng: (Đạt có thể xem cụ thể code BE implement)

- LiveKit worker realtime: `app/services/agent_voice_gpt_realtime.py`
- Token API: `app/api/v1/routers/live.py` + `app/services/live_service.py`
- Study context + thread API: `app/api/v1/routers/study_context.py`

---

## 1) Mục tiêu UX cần đạt

1. User có thể **join 1 LiveKit Room** gắn với `thread_id`.
2. User có thể **nói** (micro) và nghe assistant trả lời (audio).
3. User có thể **gõ text** (kèm payload `toggle_web_search` true/false để bật/tắt web search cho LLM) gửi vào room.
4. UI hiển thị được:
   - Tin nhắn assistant (text)
   - Transcript của user (từ voice hoặc từ text)
   - Transcript của assistant (text)
5. UI không phụ thuộc vào STT client-side: **backend sẽ publish transcript** (JSON) trên DataChannel.

---

## 2) DataChannel contract (BẮT BUỘC đúng topic)

Backend realtime worker dùng 2 topic chính:

### 2.1 Topic `lk.chat` (UTF-8 text thuần)

- **Client → Server**: user gửi câu hỏi dạng text
- **Server → Client**: assistant gửi greeting/answer dạng text

Payload:

- bytes UTF-8 của string

Reliability:

- publish reliable

### 2.2 Topic `lk.transcript` (JSON)

Backend publish transcript đã “committed” cho **cả user và assistant**.

Schema (đúng theo backend hiện tại):

```json
{
  "v": 1,
  "type": "transcript",
  "role": "user" | "assistant",
  "text": "...",
  "id": "<uuid>",
  "ts": "2026-05-12T09:29:28.738+00:00"
}
```

Quy ước xử lý UI:

- `id`: dùng để **dedupe** (tránh render trùng nếu reconnect)
- `ts`: dùng để **sort** nếu cần
- `role=user|assistant`: quyết định bubble bên trái/bên phải

Lưu ý:

- `lk.chat` là text thuần; UI có thể dùng để hiển thị nhanh.
- `lk.transcript` là JSON ổn định nhất để hiển thị “câu user nói” (voice transcript) và normalize cho UI.

### 2.3 Topic `lk.control` (JSON)

- **Client → Server**: user gửi các lệnh điều khiển cấu hình session realtime.

**Tính năng: Toggle Web Search**
Khi chat UI client sẽ có toggle search web, nếu user chat và bật lên thì AI có quyền tự động search web khi sách không đủ thông tin, ngược lại thì không (luồng hiện tại RAG naive).

Payload (UTF-8 encoded JSON):

```json
{
  "type": "toggle_web_search",
  "enabled": true
}
```

Reliability:

- publish reliable

---

## 3) REST API flow để có LiveKit token (Study Context → Thread) => Xem đầy đủ docs api ở file `fe_imp_study_context.md` đính kèm

Backend hiện tại chưa bật JWT thực, đang dùng user mock trong router study context, nên FE **chưa cần auth header** (sau này sẽ thay đổi).

### 3.1 Tạo Study Context

`POST {BASE_URL}/study-contexts`

Request:

```json
{
  "title": "Tên ngữ cảnh"
}
```

Response: `StudyContextResponse` (có `id`).

### 3.2 Gắn sách/tài liệu vào context

`POST {BASE_URL}/study-contexts/{context_id}/documents`

Request:

```json
{
  "book_id": "<uuid>"
}
```

Ghi chú:

- Có thể gọi nhiều lần để add nhiều sách.

### 3.3 Tạo thread trong context

`POST {BASE_URL}/study-contexts/{context_id}/threads`

Request:

```json
{
  "title": "Tên thread"
}
```

Response: `ChatThreadResponse` (có `id` = `thread_id`).

### 3.4 Lấy LiveKit token theo thread

`GET {BASE_URL}/live-token/thread/{thread_id}`

Response:

```json
{
  "token": "<livekit_jwt>",
  "room_name": "triam_<threadPrefix>_<rand>"
}
```

Ghi chú quan trọng:

- Token hiện tại được backend tạo với identity dạng `user_<random>`.
- `room_name` chủ yếu để debug/log; client vẫn connect bằng `LIVEKIT_URL` + `token`.

### 3.5 (Tuỳ chọn) Load lịch sử chat để render trước khi join

`GET {BASE_URL}/threads/{thread_id}/messages`

Response: list message persisted (source `livekit`).

Khuyến nghị UI:

- Render history trước (bubble list)
- Sau đó join room để tiếp tục realtime

---

## 4) LiveKit connect + subscribe (gợi ý code Flutter)

### 4.1 Dependencies gợi ý

- `livekit_client`
<!-- - `http` hoặc `dio` -->

### 4.2 Connect room

Pseudo-code:

```dart
import 'package:livekit_client/livekit_client.dart';

Future<Room> connectRoom({
  required String livekitUrl,
  required String token,
}) async {
  final room = Room();

  await room.connect(
    livekitUrl,
    token,
    const RoomOptions(
      adaptiveStream: true,
      dynacast: true,
    ),
  );

  return room;
}
```

### 4.3 Subscribe DataChannel messages

Bạn cần listen `DataReceivedEvent` và dispatch theo `topic`:

```dart
import 'dart:convert';
import 'package:livekit_client/livekit_client.dart';

late final EventsListener<RoomEvent> listener;

void setupRoomListeners(Room room) {
  listener = room.createListener();

  listener.on<DataReceivedEvent>((event) {
    final topic = event.topic;

    // 1) lk.chat: UTF-8 plain text
    if (topic == 'lk.chat') {
      final text = utf8.decode(event.data);
      final sender = event.participant?.identity ?? 'unknown';

      // Gợi ý: chỉ render nếu sender là agent
      // (identity agent thường có chữ "agent" theo quan sát test)
      // Nhưng đừng hardcode quá chặt; tốt nhất dựa vào lk.transcript để render.
      onChatText(sender: sender, text: text);
      return;
    }

    // 2) lk.transcript: JSON
    if (topic == 'lk.transcript') {
      final raw = utf8.decode(event.data);
      final obj = jsonDecode(raw);
      if (obj is! Map) return;

      final type = obj['type'];
      if (type != 'transcript') return;

      final id = obj['id']?.toString() ?? '';
      final role = obj['role']?.toString() ?? '';
      final text = obj['text']?.toString() ?? '';
      final ts = obj['ts']?.toString();

      if (text.isEmpty) return;
      onTranscript(id: id, role: role, text: text, ts: ts);
      return;
    }
  });
}

void disposeRoomListeners() {
  listener.dispose();
}
```

### 4.4 Send text message (publish to `lk.chat`)

```dart
Future<void> sendText(Room room, String message) async {
  final text = message.trim();
  if (text.isEmpty) return;

  final data = utf8.encode(text);
  await room.localParticipant?.publishData(
    data,
    topic: 'lk.chat',
    reliability: Reliability.reliable,
  );

  // UX: optimistic render bubble (role=user) ngay lập tức
  // Sau đó khi nhận lk.transcript role=user thì reconcile/dedupe.
}
```

### 4.5 Send control message (publish to `lk.control`)

Dùng để gửi các tín hiệu cấu hình. Hiện tại hỗ trợ bật/tắt tính năng **Web Search**:

```dart
Future<void> sendWebSearchToggle(Room room, bool enabled) async {
  final payload = jsonEncode({
    "type": "toggle_web_search",
    "enabled": enabled,
  });

  final data = utf8.encode(payload);
  await room.localParticipant?.publishData(
    data,
    topic: 'lk.control',
    reliability: Reliability.reliable,
  );
}
```

---

<!-- ## 5) UI state model khuyến nghị (để scale và tránh bug)

### 5.1 Message model (unified)

Khuyến nghị map cả `lk.chat` và `lk.transcript` về 1 model:

- `id` (từ transcript id, hoặc local generated)
- `role` = `user|assistant`
- `text`
- `ts`
- `source` = `transcript|chat|history`

### 5.2 Dedupe rule

- Nếu nhận `lk.transcript` có `id` đã tồn tại → bỏ qua.
- Nếu bạn optimistic-render user bubble khi gửi text:
  - Khi nhận transcript `role=user` với cùng text trong một khoảng thời gian ngắn → có thể “merge” hoặc bỏ transcript đó.

### 5.3 Ordering rule

- Ưu tiên order theo `ts` nếu có.
- Nếu `ts` parse fail, fallback theo “arrival order”.

--- -->

## 5) Reconnect & token refresh

Tình huống:

- Mạng rớt → room disconnect.

Khuyến nghị:

1. UI chuyển trạng thái “Reconnecting…”
2. Disconnect room cũ (nếu cần)
3. Call lại `GET /live-token/thread/{thread_id}` để lấy token mới
4. Connect lại room

Lưu ý:

- Token identity hiện random; reconnect sẽ tạo identity mới → đừng phụ thuộc identity cho persistence UI.

---

## 6) Checklist test cho Flutter

1. Join room thành công (không crash, có remote audio).
2. Nhận greeting trên `lk.chat`.
3. Nhận transcript greeting trên `lk.transcript` (role=assistant).
4. Gửi text lên `lk.chat`.
5. Nhận transcript user trên `lk.transcript` (role=user).
6. Nhận answer text trên `lk.chat`.
7. Nhận transcript answer trên `lk.transcript` (role=assistant).
8. Kill mạng / bật lại → reconnect ok, không render trùng transcript (dedupe theo `id`).

---

## 7) Notes / Known constraints (đúng theo backend hiện tại)

- Study context API đang dùng `MOCK_USER_ID` (chưa có auth). Khi backend bật JWT, Flutter sẽ phải gửi access token.
- Backend dùng RealtimeModel cho audio voice; text chat tay qua `lk.chat` được xử lý bằng LLM text riêng và không phát audio. Assistant voice vẫn publish text transcript qua `lk.chat`/`lk.transcript` để UI hiển thị.
- Topic names là contract cứng: `lk.chat`, `lk.transcript`, `lk.control`.
