# LiveKit Deepdive: Thoại (Voice), Data Channel và Text Stream

Tài liệu này giải thích chi tiết về các khái niệm giao tiếp trong LiveKit, tại sao chúng tồn tại, và cách chúng được áp dụng trong dự án.

## 1. Voice Stream vs Text Stream

### Voice Stream (Track Audio)

- **Là gì**: Luồng dữ liệu WebRTC thuần túy chuyên chở âm thanh được mã hóa (Opus).
- **Mục đích**: Dùng để giao tiếp âm thanh realtime (độ trễ siêu thấp) giữa người-người hoặc người-máy.
- **Áp dụng**: FE của ta publish Mic Track lên. BE Subcribe Track đó, nạp vào STT. BE generate sinh Audio Track qua TTS, publish lại để FE phát.

### Text Stream và `handle_text_input`

- **Là gì**: Một cơ chế chuyên dụng của LiveKit (mới xuất hiện khi có hệ sinh thái Agent) để truyền văn bản hiển thị theo thời gian thực — stream từng chữ (chunk).
- **Tại sao cần**: Khi LLM sinh văn bản, trải nghiệm tốt nhất là thấy text hiện ra từ từ như ChatGPT. Text Stream được thiết kế chuyên biệt cho việc đó.
- **Đóng vai trò thế nào trong Backend SDK (`handle_text_input`)**:
  - LiveKit Python Agent SDK cung cấp sẵn callback `handle_text_input` (cấu hình qua `TextInputOptions`) để tự động lắng nghe Text Stream từ phía người dùng. Khi có dữ liệu đến, nó sẽ ngắt lời Agent đang nói (`sess.interrupt()`) và đẩy text ngay vào cho AI xử lý.
- **Lý do không sử dụng trong nền tảng hiện tại (Đã xóa)**:
  - Client Flutter gửi tin nhắn dạng một cục (nguyên đoạn chat) dưới dạng byte thông qua **Data Channel** (dùng `publishData`), chứ KHÔNG gửi dạng Text Stream.
  - Do đó, việc cấu hình lắng nghe `handle_text_input` ở Backend trở nên dư thừa (dead code) vì không bao giờ được gọi tới. Ta đã xóa bỏ thiết lập này trong `agent_voice.py` để kiến trúc trong sạch và tập trung hoàn toàn vào việc bắt sự kiện Data Channel thực tế.

## 2. Data Channel (publishData & data_received)

- **Là gì**: Data Channel là thành phần cốt lõi của WebRTC (được hỗ trợ bởi SCTP protocol), cho phép truyền dữ liệu dạng nhị phân/Text realtime (Peer-to-Peer hoặc Peer-to-SFU).
- **Tại sao sử dụng ở đây thay cho Text Stream**: Data Channel cực kỳ ổn định, mọi LiveKit SDK từ nền tảng nào (Flutter, JS, Swift...) cũng đều support API `publishData()` (gửi) và `onDataReceived` (nhận) ngay từ phiên bản đầu.
- **Cách hoạt động trong App**:
  - FE gọi `publishData(utf8.encode(text), topic: "lk.chat")`.
  - BE lắng nghe event `data_received`, kiểm tra `packet.topic == "lk.chat"`, rồi xử lý message.
  - Ngược lại, BE tạo class `ChatTextOutput` gom text từ LLM sinh ra, gọi `room.local_participant.publish_data(..., topic="lk.chat")` để FE nhận nó như một Data Packet bình thường.

## 3. Word Timestamps là gì?

- Bạn thấy log cảnh báo: `unexpected message {'type': 'output_timestamps'...}`.
- **Nguồn gốc**: Các hệ thống TTS cao cấp hiện nay (như ElevenLabs, Deepgram) không chỉ trả về cục Audio nhị phân, chúng trả về thêm Metadata báo rõ _từ nào_ (Word) được phát âm trong _khoảng thời gian nào_ (Ví dụ: `word: 'Xin', start: 0.1s, end: 0.3s`).
- **Nhiệm vụ**: Sinh ra để Frontend có thể làm hiệu ứng Karaoke (chữ tô sáng đậm lên khớp từng miliseconds với giọng phát ra loa).
- **Tại sao lại thành warning**: Core của SDK LiveKit Agent phiên bản 1.5.x đôi khi nhận trực tiếp message này từ TTS engine nhưng mặc định chưa định tuyến nó vào UI hoặc đang bị bọc sai định dạng sự kiện, dẫn tới log WARNING cảnh báo chưa có handler mặc định cho `output_timestamps`. Nó hoàn toàn vô hại và không làm hỏng luồng stream audio/text chính.

## 4. Tóm tắt

- **Audio Track**: Giao tiếp Giọng nói.
- **Data Channel (publishData/data_received)**: Giao tiếp Text dạng tin nhắn toàn vẹn, tương thích tuyệt đối cho Chat.
- **Text Stream**: Giao tiếp Text dạng chunking (từng mẩu nhỏ), hiện đại cho AI nhưng mỏng về tương thích ở một số client sdk nhất định.
- **Word Timestamps**: Timestamp để đồng bộ phụ đề (subtitle/karaoke) với âm thanh.
