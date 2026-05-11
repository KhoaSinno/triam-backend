# Hướng dẫn Tích hợp Chat Text và Voice cho Flutter (LiveKit Multimodal)

Tài liệu này dành cho team Frontend (Flutter) để thực hiện chức năng cho phép User gõ chữ (Text) vào phòng thoại và nhận câu trả lời (bằng Voice + Text) từ Agent. Tính năng này được hỗ trợ mặc định qua hệ thống **Data Channels** của LiveKit.

---

## 1. Cơ Chế Hoạt Động

Backend (Python LiveKit Agent) đã bật `TextInputOptions` và `TextOutputOptions`.
- **User gửi tin nhắn:** Thay vì gửi API POST truyền thống, App Flutter sẽ bọc nội dung văn bản thành mảng Byte và bắn trực tiếp vào phòng (Room) qua kênh Data Channel với tên topic cố định là `lk.chat`.
- **Agent nhận diện:** Agent nhận luồng byte, giải mã thành Text, và coi nó như việc người dùng vừa NÓI câu đó. Nó sẽ đưa vào não (LLM) chung với các dữ kiện âm thanh.
- **Agent trả lời:**
  - **Chat text (rẻ):** Backend bắn câu trả lời dạng chat text qua Data Channel topic `lk.chat` để Frontend hiển thị.
  - **Transcript (tuỳ chọn):** Backend bắn transcript (text chạy theo voice) qua Data Channel topic `lk.transcript` nếu FE muốn hiển thị realtime transcript.

### Payload format (plain text vs JSON)
- Mặc định backend gửi **plain UTF-8 text**.
- Nếu backend bật `TRIAM_DC_PAYLOAD=json`, payload sẽ là JSON có key `text` (và có thể có thêm `type`, `role`, `ts`, `id`...).
- FE nên parse: thử JSON trước, nếu fail thì fallback sang plain text.

---

## 2. Cách Gửi Tin Nhắn Text (Flutter)

Bạn sử dụng hàm `localParticipant.publishData` có sẵn trong SDK `livekit_client`.

```dart
import 'dart:convert';
import 'dart:typed_data';
import 'package:livekit_client/livekit_client.dart';

// room là đối tượng Room mà bạn đã connect.
Future<void> sendChatMessage(Room room, String message) async {
  if (room.localParticipant == null || message.trim().isEmpty) return;

  try {
    // Biến đổi string thành uint8 list
    final data = utf8.encode(message);

    // Bắn thẳng lên Data Channel với topic là 'lk.chat'
    // Bắt buộc phải là 'lk.chat' thì Agent bên backend mới bắt được.
    await room.localParticipant!.publishData(
      data,
      topic: 'lk.chat', 
      reliability: Reliability.reliable, // Đảm bảo tin nhắn không bị rớt mạng
    );
    
    print('Gửi tin nhắn thành công: $message');
    // Mẹo: Tự add tin nhắn này vào danh sách chat trên màn hình ở phía mình
  } catch (e) {
    print('Lỗi gửi tin nhắn: $e');
  }
}
```

---

## 3. Cách Lắng Nghe Agent Trả Lời Text (Flutter)

Khi Agent đang suy nghĩ và nói, nó cũng bắn Text về phía client. Bạn cần lắng nghe Event `DataReceivedEvent` trên đối tượng Room.

```dart
import 'dart:convert';
import 'package:livekit_client/livekit_client.dart';

// Trong file Stateful Widget hoặc Controller quản lý Room của bạn
late EventsListener<RoomEvent> _listener;

void _setUpRoomListener(Room room) {
  _listener = room.createListener();

  // Lắng nghe sự kiện Data Channel
  _listener.on<DataReceivedEvent>((event) {
    String? _decodeText(Uint8List data) {
      try {
        final s = utf8.decode(data);
        // Try JSON first
        try {
          final obj = jsonDecode(s);
          if (obj is Map && obj['text'] is String) {
            return obj['text'] as String;
          }
        } catch (_) {
          // Not JSON
        }
        return s;
      } catch (_) {
        return null;
      }
    }

    // 1) Chat replies
    if (event.topic == 'lk.chat') {
      final decodedMessage = _decodeText(event.data);
      if (decodedMessage == null || decodedMessage.trim().isEmpty) return;
      final String senderIdentity = event.participant?.identity ?? 'Unknown';
      print('Nhận được tin nhắn từ $senderIdentity: $decodedMessage');
      // TODO: Update state UI hiển thị chat
    }

    // 2) Transcript stream (optional UI)
    if (event.topic == 'lk.transcript') {
      final decodedTranscript = _decodeText(event.data);
      if (decodedTranscript == null || decodedTranscript.trim().isEmpty) return;
      final String senderIdentity = event.participant?.identity ?? 'Unknown';
      print('Transcript từ $senderIdentity: $decodedTranscript');
      // TODO: Update UI nếu muốn hiển thị chữ chạy theo voice
    }
  });
}

@override
void dispose() {
  _listener.dispose(); // Nhớ dispose khi rời phòng
  super.dispose();
}
```

### 💡 Lưu ý quan trọng cho FE:
1. **Liên kết hội thoại:** Lịch sử chat được LiveKit Backend gom chung với Voice. Do đó nếu user nói "A", xong gõ chữ "B", Agent sẽ hiểu cả câu "A và B" một cách bình thường.
2. **UX Hiển thị:** Text của Agent có thể được bắn về dạng streaming (từng đoạn nhỏ ghép lại) hoặc từng câu hoàn chỉnh (phụ thuộc vào tuỳ chọn `TextOutputOptions` ở BE). Hãy print log biến `decodedMessage` ra để xem LiveKit hiện đang gom cục hay stream từng chữ, từ đó bạn có logic append chữ cho mượt mà (giống ChatGPT).
3. **Mute Micro:** Khi user đang gõ chat, bạn không cần phải tắt Micro của họ, nhưng nếu họ muốn vừa gõ vừa tắt mic để đỡ ồn, chỉ cần gọi hàm tắt `room.localParticipant.setMicrophoneEnabled(false);`
