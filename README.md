# **TÀI LIỆU ĐẶC TẢ KỸ THUẬT (TECHNICAL SPECIFICATION) \- PROJECT TRIAM**

## **1\. Tổng quan dự án (Project Overview)**

- **Tên sản phẩm:** TRIAM Assistant
- **Mục tiêu:** Ứng dụng AI Assistant tương tác Voice-to-Voice tập trung vào giáo dục, hỗ trợ người dùng "ngại đọc" có thể nghe và học từ sách/tài liệu nhanh chóng.

- **Điểm khác biệt:** Không chỉ là sách nói (Audiobook), mà là một "Active Learning Partner" (Đối tác học tập chủ động) có khả năng thảo luận, tóm tắt 80/20 và lên lộ trình học.

## ---

**2\. Yêu cầu Chức năng (Functional Requirements)**

### **2.1. Quản lý Tài liệu & Onboarding**

- **Upload tài liệu:** Người dùng upload file (PDF, EPUB, Docx).
- **Phân tích ban đầu:** Ngay khi upload, AI sẽ quét nội dung và thực hiện một cuộc hội thoại ngắn để giới thiệu sơ lược về cuốn sách.

### **2.2. Lộ trình học cá nhân hóa (Personalized Roadmap)**

- **Đề xuất lộ trình:** AI phân tích độ dài sách và thói quen người dùng để đề xuất (ví dụ: 1 chương/ngày hoặc 15 phút/ngày).

- **Chế độ học:**
  - _Full Mode:_ Đọc toàn bộ nội dung.
  - _Smart Mode (80/20):_ AI tóm lọc 20% nội dung cốt lõi chứa đựng 80% giá trị kiến thức để đọc cho user.

- **Nhắc nhở (Notification):** Push notification đúng giờ đã hẹn để user vào học ngay.

### **2.3. Tương tác Voice-to-Voice (Core Feature)**

- **Listening:** Ứng dụng đọc nội dung sách bằng giọng đọc AI tự nhiên.
- **Interruption & Q\&A:**
  - User có thể ngắt lời (hoặc bấm nút) để hỏi khi không hiểu.

  - Cơ chế trả lời: Ưu tiên tìm trong sách \-\> Nếu không có, sử dụng kiến thức nền của AI hoặc search web (Google Search/Bing) để giải thích.

  - Sau khi trả lời xong, AI hỏi user có muốn tiếp tục nghe không.

### **2.4. Xử lý ngôn ngữ tự nhiên (NLP Requirements) \- Rất quan trọng**

- **Text Normalization (Chuẩn hóa văn bản trước khi đọc):**
  - Phải xử lý từ viết tắt tiếng Việt: "CNTT" $\\rightarrow$ đọc là "Công nghệ thông tin".

  - Phải xử lý từ chuyên ngành/Tiếng Anh: "AI" $\\rightarrow$ đọc là "Ây-Ai" (đánh vần) hoặc giữ nguyên tiếng Anh, không được dịch sai ngữ cảnh.

## ---

**3\. Kiến trúc Công nghệ & Tech Stack (Architecture & Stack)**

Dựa trên nguyên tắc "không code thuần nếu có thư viện", đây là đề xuất Stack tốt nhất hiện nay:

### **3.1. Mobile App (Frontend)**

- **Công nghệ:** **Flutter** (Google).
- **Lý do:** Cross-platform (iOS/Android) mượt mà, hỗ trợ tốt các thư viện âm thanh và xử lý background service cho việc nghe sách.

### **3.2. Backend & AI Core**

- **Ngôn ngữ:** **Python** (Framework: **FastAPI**).
- **Lý do:** Python là vua của AI, FastAPI nhanh và hỗ trợ xử lý bất đồng bộ (async) tốt cho voice streaming.

### **3.3. Các module AI (Sử dụng API Service)**

Đây là phần "trí tuệ" của ứng dụng, chúng ta sẽ ghép nối các dịch vụ hàng đầu:

1. **LLM (Bộ não \- Xử lý logic & Tóm tắt):**
   - **Dịch vụ:** **OpenAI GPT-4o** hoặc **Anthropic Claude 3.5 Sonnet**.
   - _Nhiệm vụ:_ Đọc hiểu PDF, tạo lộ trình 80/20, trả lời câu hỏi user, và **quan trọng nhất là Pre-processing Text** (viết lại văn bản thô thành văn bản nói để xử lý vụ "CNTT" hay "AI").

2. **STT (Speech-to-Text \- Tai nghe):**
   - **Dịch vụ:** **OpenAI Whisper (qua API Groq để siêu nhanh)** hoặc **Deepgram Nova 2**.
   - _Nhiệm vụ:_ Chuyển giọng nói user thành text cực nhanh, hỗ trợ tiếng Việt tốt.
3. **TTS (Text-to-Speech \- Miệng nói):**
   - **Dịch vụ:** **ElevenLabs** (Chất lượng tốt nhất hiện nay) hoặc **OpenAI TTS HD**.
   - _Nhiệm vụ:_ Đọc văn bản với cảm xúc. ElevenLabs hỗ trợ tiếng Việt rất tự nhiên, không bị "máy móc".
4. **Vector Database (Bộ nhớ sách):**
   - **Dịch vụ:** **Pinecone** hoặc **Qdrant**.
   - _Nhiệm vụ:_ Lưu trữ nội dung sách đã được phân mảnh (chunking). Giúp AI tìm kiếm chính xác đoạn văn trong sách để trả lời câu hỏi (kỹ thuật RAG \- Retrieval Augmented Generation).
5. **Search Tool:**
   - **Dịch vụ:** **Tavily API** hoặc **Google Serper**.
   - _Nhiệm vụ:_ Để AI search web khi kiến thức không có trong sách.

---

4\. Luồng xử lý dữ liệu (Technical Data Flow)

### **Luồng 1: Upload & Xử lý sách**

1. User upload PDF $\\rightarrow$ Backend dùng thư viện PyMuPDF hoặc LlamaParse để trích xuất text.
2. Chia nhỏ text (Chunking) $\\rightarrow$ Lưu vào Vector DB (Pinecone).
3. LLM phân tích mục lục $\\rightarrow$ Tạo file JSON chứa lộ trình học (Chapter list).

### **Luồng 2: Quy trình đọc & Xử lý chuẩn hóa (Normalization Logic)**

Để giải quyết bài toán "CNTT" và "AI", ta thêm một bước đệm **Text-to-SSML** (Speech Synthesis Markup Language) bằng LLM:

1. Lấy đoạn text gốc từ sách.
2. **Prompt gửi LLM:** _"Hãy chuyển đoạn văn sau thành kịch bản nói. Mở rộng các từ viết tắt tiếng Việt (VD: CNTT \-\> Công nghệ thông tin), giữ nguyên thuật ngữ tiếng Anh thông dụng. Văn phong tự nhiên."_
3. Kết quả từ LLM $\\rightarrow$ Gửi sang API ElevenLabs (TTS) $\\rightarrow$ Stream âm thanh về App.

### **Luồng 3: Hỏi đáp (Interactive Mode)**

1. User bấm nút "Hỏi" (Voice) $\\rightarrow$ Deepgram STT chuyển thành text.
2. Backend search trong Vector DB (nội dung sách).
   - _Nếu độ khớp cao:_ Gửi context sách \+ câu hỏi $\\rightarrow$ LLM trả lời.
   - _Nếu độ khớp thấp:_ Kích hoạt Tavily API search Web $\\rightarrow$ LLM tổng hợp $\\rightarrow$ Trả lời.

3. LLM output text $\\rightarrow$ TTS $\\rightarrow$ App phát loa.

---

5\. Hướng dẫn thực hiện (Implementation Steps)

1. **Phase 1: The Core (2 tuần)**
   - Dựng FastAPI backend.
   - Tích hợp OpenAI API (LLM), Pinecone (DB).
   - Viết hàm xử lý PDF upload và RAG cơ bản.
2. **Phase 2: The Voice (2 tuần)**
   - Tích hợp Deepgram (nghe) và ElevenLabs (nói).
   - Xử lý logic "Pre-processing" để chuẩn hóa từ ngữ viết tắt (CNTT/AI) đảm bảo trải nghiệm nghe mượt mà.

   - Dựng App Flutter cơ bản: Upload file, nút Play/Pause/Talk.

3. **Phase 3: The Features (2 tuần)**
   - Logic lộ trình học & nhắc nhở (Notification).
   - Chế độ tóm tắt 80/20 (Dùng LLM tóm tắt từng chương trước khi đưa vào luồng đọc).

### **Lời khuyên từ Tech Lead:**

Bạn nên bắt đầu với **OpenAI Assistant API** trước. Nó đã tích hợp sẵn: RAG (File Search), Code Interpreter và quản lý hội thoại. Điều này giúp bạn giảm 50% lượng code backend cần viết, đúng tiêu chí "không thiết kế lại bánh xe". Chỉ cần tập trung tối ưu phần Voice và Prompt Engineering để xử lý việc đọc từ viết tắt cho chuẩn.
