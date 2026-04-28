# Báo Cáo So Sánh: VoicePipelineAgent vs RealtimeModel (AgentSession)

Dựa trên code hiện tại của bạn (`agent_voice.py`), bạn đang sử dụng `google.realtime.RealtimeModel` chạy bọc trong `AgentSession`. Đây là kiến trúc **Realtime/Multimodal Native**, hoàn toàn khác với kiến trúc **VoicePipelineAgent** (STT -> LLM -> TTS rời rạc) mà các tutorial cũ của LiveKit thường hướng dẫn.

Dưới đây là báo cáo trả lời 2 câu hỏi lớn của bạn.

---

## 1. Giải pháp ở report trước có áp dụng được cho RealtimeModel không?

**Câu trả lời là: CÓ, nhưng cần tinh chỉnh một chút về mặt sự kiện (Events).**

Cả 2 mô hình đều dùng chung hệ sinh thái LiveKit Room, nên Data Channel (`lk.chat`) hoạt động hoàn toàn giống nhau. Tuy nhiên, cách chúng xử lý văn bản (Text) bên dưới có sự khác biệt:

- **Tích hợp Text Chat:** Hoạt động **CỰC KỲ TỐT** trên RealtimeModel. Bản thân Gemini Realtime (hay OpenAI Realtime) sinh ra đã là mô hình Đa phương thức (Multimodal). Nó nhận Audio và Text cùng lúc vào cùng một cổng. Khi user gõ text, `AgentSession` tự động đẩy text đó vào Gemini, và Gemini có thể trả lời bằng giọng nói ngay lập tức mà không cần qua bước chuyển đổi nào.
- **Lưu Lịch Sử (History):** Hoạt động tốt, nhưng có lưu ý nhỏ. Đối với Pipeline rời rạc, bạn có STT (Speech-to-Text) chạy riêng nên text có ngay lập tức. Đối với RealtimeModel, việc bóc băng (Transcription) phụ thuộc vào chính model Gemini trả về. Sự kiện `user_speech_committed` hoặc `conversation_item_added` vẫn được bắn ra, nhưng độ trễ text hiển thị có thể chậm hơn 1-2 giây (dù giọng nói đã được phản hồi ngay lập tức). Bạn vẫn có thể dùng các hook này để lưu vào Database.

---

## 2. Phân Tích So Sánh Chi Tiết: VoicePipelineAgent vs RealtimeModel

### A. Kiến trúc hoạt động

| Tiêu chí               | VoicePipelineAgent (Kiến trúc rời)                                                                                               | RealtimeModel / AgentSession (Kiến trúc Native)                                                                         |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **Bản chất**           | Lắp ghép 3 model riêng biệt: STT (nhận diện giọng nói) $\rightarrow$ LLM (nghĩ câu trả lời) $\rightarrow$ TTS (đọc thành tiếng). | Dùng 1 model duy nhất (Gemini Live / GPT-4o Realtime). Model nghe trực tiếp audio, suy nghĩ, và trả trực tiếp audio ra. |
| **Thành phần cấu tạo** | Vd: Deepgram (STT) + OpenAI GPT-4o (LLM) + ElevenLabs (TTS).                                                                     | Vd: Google Gemini Realtime Audio.                                                                                       |
| **Trung gian Text**    | Mọi thứ bắt buộc phải chuyển qua Text (Văn bản).                                                                                 | Không cần Text làm trung gian. (Voice-in $\rightarrow$ Voice-out).                                                      |

### B. Ưu điểm & Nhược điểm

#### 1. RealtimeModel (Đang dùng hiện tại)

- **Ưu điểm:**
  - **Độ trễ cực thấp (Ultra-low latency):** Vì không qua bước dịch ra text rồi mới xử lý, agent có thể phản hồi gần như ngay lập tức giống người thật.
  - **Hiểu được sắc thái giọng nói:** Model nghe được giọng bạn đang buồn, vui, hay ngập ngừng để đưa ra phản hồi phù hợp (điều mà text không làm được).
  - **Cắt lời (Interruption) mượt mà:** Xử lý người dùng ngắt lời cực kỳ tự nhiên và nhạy bén.
- **Nhược điểm:**
  - **Giọng đọc (TTS) bị giới hạn:** Bạn bị khóa chặt vào các giọng đọc mặc định của Google Gemini (ví dụ giọng "Puck" bạn đang cài). Bạn không thể lấy giọng nói truyền cảm của ElevenLabs hay OpenAI TTS để ghép vào.
  - **Đắt đỏ:** Chi phí tính theo giây audio stream trực tiếp, thường đắt hơn nhiều so với việc tính theo token text.
  - **Tiếng Việt:** Các model realtime của Google và OpenAI hiện tại hỗ trợ Tiếng Việt chưa thật sự hoàn hảo (đôi khi bị lơ lớ hoặc dính âm Mỹ).

#### 2. VoicePipelineAgent (LiveKit khuyên dùng cho đa số dự án)

- **Ưu điểm:**
  - **Tùy biến tối đa:** Bạn có thể chọn model tốt nhất cho từng khâu. STT nhận diện Tiếng Việt dùng Deepgram (siêu chuẩn), LLM dùng GPT-4o-mini (rẻ, thông minh), TTS dùng ElevenLabs hoặc OpenAI Alloy (đọc siêu hay, truyền cảm).
  - **Dễ kiểm soát luồng:** Bạn có thể can thiệp vào câu text trước khi nó được đọc lên (ví dụ chặn từ bậy bạ, thêm hiệu ứng).
  - **Rẻ hơn:** Tối ưu hóa chi phí cực tốt vì chỉ trả tiền LLM theo token text.
- **Nhược điểm:**
  - **Độ trễ cao hơn (Latency):** Mất thời gian chờ STT dịch xong $\rightarrow$ gửi LLM $\rightarrow$ chờ LLM nhả text $\rightarrow$ gửi TTS đọc. Thường trễ từ 1-3 giây so với RealtimeModel.
  - **Mất sắc thái:** STT chỉ dịch ra chữ, LLM không biết bạn vừa quát tháo hay nói nhỏ nhẹ.

---

## 3. KẾT LUẬN & KHUYẾN NGHỊ CHO DỰ ÁN TRIAM

Dự án Triam là **Nền tảng đọc sách (Audiobook / RAG Book)**. Dưới đây là phân tích mức độ phù hợp:

1.  **Chất lượng Giọng Đọc (TTS) là sinh mệnh:** Người dùng dùng app của bạn để nghe sách hoặc thảo luận về sách. Giọng đọc phải thực sự truyền cảm, rõ chữ, chuẩn Tiếng Việt, giống người kể chuyện. Giọng mặc định của Gemini Realtime (Puck, Aoede...) hiện tại đọc Tiếng Việt còn khá "máy móc" và lơ lớ.
2.  **Khả năng RAG (Trích xuất kiến thức sách):** Việc agent cần gọi tool để lấy thông tin từ sách đòi hỏi suy luận logic tốt. Pipeline cho phép bạn dùng các model LLM chuyên biệt cho RAG (như Claude 3.5 Sonnet hoặc GPT-4o) cực kỳ ổn định.

### KHUYẾN NGHỊ CỦA TÔI:

**Nên CHUYỂN SANG sử dụng kiến trúc `VoicePipelineAgent` thay vì `RealtimeModel` hiện tại.**

**Tech Stack đề xuất cho Triam Agent:**

- **VAD:** `silero.VAD` (Giữ nguyên, phát hiện giọng nói rất tốt)
- **STT (Nghe):** Sử dụng plugin Google STT hoặc Deepgram STT (Deepgram nhận diện Tiếng Việt cực đỉnh và nhanh).
- **LLM (Nghĩ):** Sử dụng Google Gemini (gemini-1.5-flash hoặc pro) thông qua plugin LLM thông thường.
- **TTS (Nói):** Sử dụng ElevenLabs (Nếu có budget) hoặc Google TTS / OpenAI TTS để có giọng Tiếng Việt tự nhiên nhất.

**Lợi ích lớn nhất nếu bạn chuyển đổi:**

1. Khắc phục ngay nhược điểm giọng đọc dở/lơ lớ của model Realtime.
2. Áp dụng hoàn hảo các giải pháp lưu lịch sử (Vấn đề 1) và Chat Text song song (Vấn đề 2) một cách cực kỳ ổn định, vì mọi thứ đi qua Text, ta nắm toàn quyền kiểm soát log.

Nếu bạn đồng ý chuyển đổi kiến trúc sang `VoicePipelineAgent` để tối ưu cho dự án, tôi sẽ bắt tay vào refactor lại file `agent_voice.py` cho bạn!
