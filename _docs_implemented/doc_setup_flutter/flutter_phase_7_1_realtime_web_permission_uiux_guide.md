# TRIAM Flutter Phase 7.1 Realtime Web Permission UI/UX Guide

Ngày cập nhật: 2026-05-31  
Audience: Flutter team, backend maintainer  
Backend scope: Phase 7.1 realtime voice/text web-search permission guardrail  
Đọc sau file:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md
```

---

## 1. Kết Luận Nhanh Cho FE

Phase 7.1 **không thêm REST API mới**.

FE vẫn dùng các API và DataChannel đã có:

```http
GET /api/v1/threads/for-book/{book_id}
GET /api/v1/live-token/thread/{thread_id}
```

Realtime topics vẫn là:

| Topic | Direction | Payload |
| --- | --- | --- |
| `lk.chat` | FE -> BE, BE -> FE | plain UTF-8 text |
| `lk.transcript` | BE -> FE only | transcript JSON |
| `lk.control` | FE -> BE | JSON control message |

FE cần update chủ yếu ở **UI/UX web-search permission**:

- Voice mode: user không cần bấm nút xác nhận; user trả lời bằng giọng nói tự nhiên.
- Text chat mode: FE nên render action chips/nút nhanh `Cho phép tìm web` và `Không cần`.
- FE phải gửi toggle web search qua `lk.control` nếu màn chat/voice có chức năng cho phép tìm internet.
- FE không tự gọi API tìm web. BE realtime agent tự xử lý RAG, xin phép, search web và trả lời.

---

## 2. Vì Sao Có Phase 7.1?

Trước Phase 7.1, voice agent có thể gặp các lỗi UX:

```text
AI hỏi xin phép tìm internet -> user nói "Có" / "Ok baby" / "Yup làm đi"
-> agent vẫn hỏi xác nhận lại hoặc trả lời lặp.
```

Backend đã cải thiện:

- Nhận diện câu đồng ý/từ chối bằng ngôn ngữ tự nhiên, không hard-code vài từ cố định.
- Hỗ trợ câu trả lời voice như `Yup`, `Ok baby`, `Có, làm đi`, `Ừ tìm đi`.
- Giảm nguy cơ trả lời lặp trong voice flow.
- Thêm guardrail để web search chỉ chạy khi user đã cho phép.

FE không cần implement classifier. FE chỉ cần thiết kế UI đúng để user hiểu trạng thái.

---

## 3. Web Search Toggle Contract

Khi user bật/tắt tính năng tìm kiếm internet trong màn Ask AI hoặc Voice Agent, FE publish lên `lk.control`.

```json
{
  "type": "toggle_web_search",
  "enabled": true
}
```

Khi tắt:

```json
{
  "type": "toggle_web_search",
  "enabled": false
}
```

Rule:

- Publish reliable.
- Gửi lại toggle sau khi join room thành công.
- Nếu UI có switch, state mặc định nên lấy từ local/session preference của FE.
- Nếu chưa gửi toggle, backend dùng default server config; FE không nên phụ thuộc default này.

Flutter pseudo-code:

```dart
Future<void> publishWebSearchToggle(bool enabled) async {
  final payload = jsonEncode({
    'type': 'toggle_web_search',
    'enabled': enabled,
  });

  await room.localParticipant?.publishData(
    utf8.encode(payload),
    reliable: true,
    topic: 'lk.control',
  );
}
```

---

## 4. Text Chat UX

### 4.1 Khi User Gõ Câu Hỏi

FE gửi plain text qua `lk.chat`.

```dart
Future<void> sendTextChat(String text) async {
  await room.localParticipant?.publishData(
    utf8.encode(text),
    reliable: true,
    topic: 'lk.chat',
  );
}
```

### 4.2 Khi Assistant Xin Phép Tìm Internet

Backend hiện trả lời bằng text tự nhiên, ví dụ:

```text
Thông tin về '...' không có trong sách. Bạn có muốn tôi tìm kiếm thêm trên internet không?
```

FE nên render trong bubble assistant kèm quick actions:

```text
[Cho phép tìm web] [Không cần]
```

Khi user bấm:

| User action | FE gửi vào `lk.chat` |
| --- | --- |
| Cho phép tìm web | `Có, tìm kiếm trên internet.` |
| Không cần | `Không cần.` |

Không cần endpoint mới.

### 4.3 Tránh UI Gây Hiểu Lầm

Không nên dùng modal blocking toàn màn hình cho text chat. Nên dùng action chips ngay dưới bubble permission.

Gợi ý states:

```text
Assistant bubble: câu xin phép
Quick actions: Cho phép tìm web / Không cần
Sau khi bấm: disable chips, show "Đang tìm kiếm..."
Khi assistant trả lời: render bubble mới từ lk.transcript/lk.chat
```

---

## 5. Voice UX

### 5.1 Voice Không Bắt Buộc Bấm Nút Xác Nhận

Trong voice mode, user có thể đang đeo tai nghe hoặc không cầm điện thoại. Vì vậy FE **không được bắt buộc user phải bấm nút** để cho phép tìm web.

Flow đúng:

```text
User hỏi bằng giọng nói
AI không thấy đủ thông tin trong sách
AI hỏi: "Bạn có muốn tôi tìm kiếm thêm trên internet không?"
User nói: "Có", "Ok baby", "Yup làm đi", "Ừ tìm đi", ...
Backend tự hiểu và search
AI trả lời bằng giọng nói
```

### 5.2 UI Nên Hiển Thị Gì?

FE nên hiển thị nhẹ, không blocking:

```text
AI cần tìm thêm trên internet
Bạn có thể nói "Có" hoặc "Không cần"
```

Có thể thêm 2 nút phụ để tiện nếu user đang cầm máy:

```text
[Cho phép] [Không cần]
```

Nhưng đây chỉ là optional shortcut. Voice answer vẫn phải hoạt động.

Nếu user bấm nút trong voice screen:

| Button | FE gửi vào `lk.chat` |
| --- | --- |
| Cho phép | `Có, tìm kiếm trên internet.` |
| Không cần | `Không cần.` |

### 5.3 Mic State

Khi AI đang nói câu xin phép, FE không nên tự tắt mic. Nếu tắt mic thì user không thể trả lời bằng giọng nói.

Nếu FE có push-to-talk:

- Sau câu xin phép, giữ trạng thái sẵn sàng nghe.
- Không mở modal làm mất focus mic.

Nếu FE dùng open mic:

- Giữ mic hoạt động.
- UI chỉ hiển thị trạng thái đang nghe.

---

## 6. Transcript Rendering

FE vẫn lấy timeline chính từ `lk.transcript`.

Schema không đổi:

```json
{
  "v": 1,
  "type": "transcript",
  "role": "assistant",
  "text": "...",
  "id": "uuid",
  "ts": "2026-05-31T10:00:00.000+00:00"
}
```

Rules:

- Dedupe bằng `id`.
- Không publish lên `lk.transcript`.
- `lk.chat` có thể dùng để hiển thị nhanh, nhưng timeline chính nên dùng transcript/history.
- Nếu cùng nội dung xuất hiện ở `lk.chat` và `lk.transcript`, FE không render trùng bubble.

Gợi ý:

```dart
final seenTranscriptIds = <String>{};

void onTranscript(Map<String, dynamic> payload) {
  final id = payload['id']?.toString();
  if (id == null || seenTranscriptIds.contains(id)) return;
  seenTranscriptIds.add(id);
  // append bubble
}
```

---

## 7. Recommended UI Components

### 7.1 Ask AI / Chat Screen

Nên có:

- Toggle tìm internet.
- Text composer.
- Chat bubbles.
- Permission quick actions dưới bubble assistant khi phát hiện câu xin phép.
- Loading state nhỏ: `Đang tìm kiếm...`.

Không nên:

- Tự gọi web search từ FE.
- Tự trả lời câu hỏi ngoài sách.
- Ép user xác nhận nhiều lần.

### 7.2 Voice Agent Screen

Nên có:

- Mic button hoặc open mic indicator.
- Web search toggle.
- Transcript live/timeline.
- Permission hint nhẹ khi AI hỏi xin phép.
- Optional buttons `Cho phép` / `Không cần`.

Không nên:

- Modal blocking khi AI hỏi xin phép.
- Tắt mic sau khi AI hỏi xin phép.
- Render nhiều bubble trùng từ `lk.chat` và `lk.transcript`.

---

## 8. Detect Permission Bubble Như Thế Nào?

Backend hiện chưa gửi event JSON riêng kiểu `web_permission_requested`.

Bản Phase 7.1 hiện tại FE có thể detect mềm bằng text assistant:

```text
có muốn tôi tìm kiếm thêm trên internet không
tìm kiếm thêm trên internet
tìm trên internet
```

Ví dụ:

```dart
bool looksLikeWebPermissionQuestion(String text) {
  final normalized = text.toLowerCase();
  return normalized.contains('tìm kiếm thêm trên internet') ||
      normalized.contains('tìm trên internet') ||
      normalized.contains('tìm kiếm trên internet');
}
```

Trade-off:

- Cách này đủ dùng cho capstone/demo.
- Production tốt hơn nên có event riêng từ BE để FE không phải detect bằng text.

Future BE improvement nếu cần:

```json
{
  "type": "web_permission_requested",
  "query": "...",
  "request_id": "uuid"
}
```

Hiện tại event này **chưa có**, FE không được phụ thuộc vào nó.

---

## 9. Error/Edge Cases FE Cần Xử Lý

### 9.1 Web Search Disabled

Nếu user tắt toggle, assistant có thể nói:

```text
Tính năng tìm kiếm internet hiện đang tắt.
```

FE nên hiển thị gợi ý:

```text
Bật tìm internet để AI có thể tra cứu thông tin ngoài sách.
```

### 9.2 User Từ Chối

Nếu user nói/gõ:

```text
Không cần.
```

Assistant sẽ không search web. FE chỉ render bình thường.

### 9.3 User Hỏi Câu Mới Thay Vì Xác Nhận

Nếu AI vừa xin phép nhưng user hỏi câu khác, backend có thể xem đó là câu hỏi mới và clear pending permission.

FE không cần xử lý đặc biệt, chỉ tiếp tục timeline.

### 9.4 Network/Rejoin Room

Khi reconnect room:

- Lấy lại LiveKit token nếu token cũ hết hạn.
- Rejoin room.
- Publish lại `toggle_web_search`.
- Dedupe transcript bằng `id`.
- Có thể load message history bằng API thread messages nếu screen cần khôi phục timeline.

---

## 10. Test Checklist Cho FE

### 10.1 Text Chat

```text
1. Join thread có sách.
2. Bật web search toggle.
3. Gõ câu trong sách -> AI trả lời từ sách.
4. Gõ câu ngoài sách -> AI xin phép tìm internet.
5. Bấm "Cho phép tìm web" -> FE gửi "Có, tìm kiếm trên internet." qua lk.chat.
6. AI trả lời kết quả web.
7. Gõ câu ngoài sách khác, bấm "Không cần" -> AI không search.
8. Tắt web search toggle -> câu ngoài sách phải báo tìm internet đang tắt hoặc chỉ dùng sách.
```

### 10.2 Voice

```text
1. Join thread có sách.
2. Bật web search toggle.
3. Nói câu trong sách -> AI trả lời từ sách.
4. Nói câu ngoài sách -> AI xin phép tìm internet.
5. Nói "Có", "Ok baby", "Yup làm đi" -> AI search và trả lời.
6. Lặp lại với "Không cần" -> AI không search.
7. Test bằng tai nghe.
8. Test bằng loa ngoài, kiểm tra AI không bị ngắt/lặp bất thường.
```

### 10.3 Regression Cần Chú Ý

Không được xảy ra:

```text
AI hỏi xác nhận liên tục dù user đã nói có.
AI nói "đang tìm" mãi dù search đã xong.
AI trả lời cùng một kết quả nhiều lần.
Text bubble bị render trùng.
Voice permission bắt buộc user phải bấm màn hình.
```

---

## 11. Production Test Vẫn Cần

Phase 7.1 đã cải thiện backend, nhưng realtime voice cần test production thật vì phụ thuộc:

- microphone/loa/tai nghe;
- echo cancellation trên thiết bị;
- LiveKit room thật;
- latency OpenAI realtime;
- latency web search;
- network mobile.

Trước khi xem là ổn định production, FE và BE nên test:

```text
Mobile thật + tai nghe
Mobile thật + loa ngoài
Text chat qua lk.chat
Voice qua microphone
Reconnect room
Web search on/off
Permission grant/deny/new question
```

---

## 12. FE Implementation Priority

Ưu tiên theo thứ tự:

1. Đảm bảo `lk.control` toggle web search chạy đúng.
2. Text chat render permission quick actions.
3. Voice screen không block user bằng modal khi cần xác nhận.
4. Dedupe `lk.chat` và `lk.transcript`.
5. QA trên mobile thật với tai nghe và loa ngoài.

---

## 13. Một Câu Định Hướng Cho FE

```text
FE chỉ điều khiển trải nghiệm xác nhận và hiển thị trạng thái.
Quyết định RAG, xin phép, search web và trả lời thuộc về backend realtime agent.
```
