# Flow Live Assistant Gemini (Voice-to-Voice Realtime Q&A)

---

## 1. Khởi tạo kết nối WebSocket và Gemini Live Session

- **Aim:** Thiết lập kênh giao tiếp theo thời gian thực (real-time) với độ trễ thấp nhất giữa Client và mô hình AI.

- **Logic flow:**
  - **Flutter:**
    - Gửi request kết nối WebSocket tới endpoint `/ws/live-assistant/{book_id}`.
    - Setup AudioRecorder (PCM 16-bit, 16kHz, mono) và AudioPlayer engine (sẵn sàng nhận PCM 24kHz).
  - **Backend:**
    - Chấp nhận kết nối WebSocket.
    - Khởi tạo `genai.Client.aio.live.connect` với model `gemini-2.5-flash-native-audio-latest`.
    - Nạp `SYSTEM_INSTRUCTION` (định hình nhân vật Trợ lý TRIAM) và đăng ký 2 tools: `search_book_knowledge` và `search_web`.

## 2. Giao tiếp song công (Full-Duplex Streaming)

- **Aim:** Lắng nghe người dùng nói và phản hồi âm thanh đồng thời (hoạt động giống như đang gọi điện thoại).

- **Logic flow:**
  - **Backend chạy 2 tiến trình ngầm song song (`asyncio.gather`):**
    - **Tiến trình 1 (`send_to_gemini`):**
      - Lắng nghe luồng byte âm thanh thô (raw PCM bytes) từ WebSocket (Flutter gửi lên).
      - Đẩy trực tiếp các chunk âm thanh này vào Gemini thông qua hàm `send_realtime_input`.
    - **Tiến trình 2 (`receive_from_gemini`):**
      - Liên tục nhận tín hiệu trả về từ Gemini thông qua vòng lặp `async for response in session.receive()`.
      - Nếu response chứa audio data (`inline_data`), Backend gửi thẳng cục byte này (24kHz PCM) qua WebSocket về lại cho Flutter để phát ngay lập tức (không đợi AI nói xong nguyên câu).

## 3. Kích hoạt Tool Calling (RAG & Web Search)

- **Aim:** Cung cấp thông tin chính xác từ sách hoặc internet khi người dùng hỏi các câu hỏi cụ thể, thay vì để AI tự "bịa" câu trả lời (hallucination).

- **Logic flow:**
  - Trong quá trình nhận luồng (`receive_from_gemini`), nếu phát hiện AI kích hoạt `tool_call`, Backend sẽ tạm dừng phát âm thanh và rẽ nhánh xử lý:
    - **Trường hợp 1: `search_book_knowledge` (Ưu tiên)**
      - Lấy câu hỏi từ AI (ví dụ: "Tác giả định nghĩa thế nào về tư duy?").
      - Dùng thư viện `AsyncOpenAI` (`text-embedding-3-small`) để biến câu hỏi thành Vector (Embedding).
      - Gọi RPC `match_book_knowledge` xuống Supabase để query vector similarity, quét các chunk text trong `book_id` hiện tại.
    - **Trường hợp 2: `search_web`**
      - Gọi API của Tavily (`AsyncTavilyClient`) để search thông tin thực tế/cập nhật trên mạng.
  - **Phản hồi lại AI:** 
    - Tổng hợp các text content tìm được.
    - Gửi kết quả ngược lại cho Gemini thông qua `session.send_tool_response`.
    - Gemini đọc context này, hiểu vấn đề và tiếp tục sinh ra luồng âm thanh trả lời cho người dùng (quay lại bước 2).

## 4. Đóng kết nối (Graceful Disconnect)

- **Aim:** Giải phóng tài nguyên phần cứng và mạng khi kết thúc phiên hỏi đáp.
- **Logic flow:**
  - **Flutter:** Người dùng bấm nút tắt trợ lý -> Hủy ghi âm -> Close Web Socket sink.
  - **Backend:** 
    - Bắt Exception `WebSocketDisconnect`.
    - Dừng các vòng lặp asyncio, tự động ngắt kết nối với Gemini Live Session để tránh rò rỉ bộ nhớ (memory leak).
