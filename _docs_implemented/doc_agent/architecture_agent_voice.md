# Kiến trúc giao tiếp: Backend, Frontend và LiveKit Cloud

Tài liệu này mô tả chi tiết luồng hoạt động của agent voice trong tệp `agent_voice.py`, cách các thành phần tương tác với nhau và lý do đằng sau các thiết kế này.

## 1. Cấu trúc các thành phần

Hệ thống giao tiếp thông qua 3 thành tố chính:
- **Frontend (Flutter)**: Ứng dụng người dùng, nơi thu âm/phát âm thanh và nhận/gửi văn bản qua LiveKit client SDK.
- **LiveKit Cloud / Server**: Dịch vụ trung gian (SFU/WebRTC Server) quản lý Room, điều phối luồng Media (Audio/Video) và Data Channels giữa các Participant (Client và Agent).
- **Backend (Python Agent)**: Chạy dưới dạng một `Worker` ứng dụng Agent SDK của LiveKit. Kết nối vào Room như một Participant đặc biệt, dùng AI để xử lý ngôn ngữ và giọng nói.

## 2. Luồng giao tiếp (Flow)

### Bước 1: Khởi tạo và Kết nối
1. Từ FE, người dùng yêu cầu join room. Backend trả về một Token.
2. FE dùng token đó để kết nối vào LiveKit Cloud Room.
3. Khi Room được tạo/hoạt động, Backend (Worker) bắt được tín hiệu điều phối và chạy `entrypoint()`.
4. Agent gọi `ctx.connect()` để chính thức gia nhập Room. 

### Bước 2: Khởi tạo Pipeline AI (AgentSession)
- Agent khởi tạo `AgentSession` đóng vai trò điều phối pipeline xử lý giọng nói, bao gồm:
  - **VAD (Voice Activity Detection)**: Dùng Silero để phát hiện người dùng bắt đầu nói hay dừng nói.
  - **STT (Speech-to-Text)**: Dùng Deepgram để chuyển giọng nói người dùng thành văn bản (tiếng Việt).
  - **LLM**: Dùng GPT để phân tích văn bản, gọi Tools (RAG qua Supabase, Search Web qua Tavily), sinh câu trả lời.
  - **TTS (Text-to-Speech)**: Dùng ElevenLabs để chuyển text ngược lại thành giọng nói tiếng Việt mượt mà. Đẩy Audio Track ngược lên LiveKit.

### Bước 3: Giao tiếp Văn bản & Giọng nói (Đồng thời)
- **Luồng Voice**: FE gửi Audio Track -> LiveKit Cloud -> Backend VAD & STT -> LLM xử lý -> TTS -> Backend gửi sinh Audio Track mới -> LiveKit Cloud -> FE phát ra loa.
- **Luồng Text (Chat)**:
  - **Hướng FE -> BE**: FE gửi tin nhắn dạng `DataChannel` (qua hàm `publishData` trong SDK). Backend lắng nghe qua sự kiện `ctx.room.on("data_received")`. Khi nhận data thuộc topic `lk.chat`, Backend ngắt hành động hiện tại (`session.interrupt()`) và đẩy text vào LLM để tạo câu trả lời.
  - **Hướng BE -> FE**: Backend chặn luồng text đầu ra từ LLM trước khi nó biến thành giọng nói, hoặc song song với nó, gom (flush) lại và đẩy ngược DataChannel qua lớp `ChatTextOutput` tự định nghĩa bằng hàm `room.local_participant.publish_data(...)`. FE nhận sự kiện Data trên topic `lk.chat` và in ra màn hình.

## 3. Ý nghĩa các thành phần Code chính

- `ChatTextOutput`: Kế thừa `voice_io.TextOutput`. Mặc định LiveKit Agent đẩy text về dạng `TextStream` (một cơ chế stream mới do LK định nghĩa). Tuy nhiên FE Flutter hiện đang lắng nghe DataChannel. Do đó chúng ta tạo class này để hứng text từ LLM, gom lại thành block, rồi publish qua `publish_data` để FE có thể hiển thị như chat message thường.
- `TriamAssistant(Agent)`: Định nghĩa system prompt của LLM và đăng ký các @function_tool (Kỹ năng của Agent như tra cứu DB, tìm kiếm web).
- Xóa `room_io.TextInputOptions`: Phiên bản cơ bản của Agent lắng nghe chuỗi text stream chuẩn của LiveKit, nhưng do ta tự handle `publishData` từ FE (data channel), ta không cần `handle_text_input` mặc định của LK nữa để tránh dư thừa.