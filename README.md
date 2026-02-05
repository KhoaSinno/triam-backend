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

======================

# 🚀 How to Run TRIAM Backend

## 📋 Project Overview

**TRIAM Assistant** is an AI-powered Voice-to-Voice educational assistant built with:

- **Backend Framework**: FastAPI (Python)
- **Package Manager**: uv (ultra-fast Rust-based package manager)
- **AI Services**: OpenAI (GPT-4, TTS), Pinecone (Vector DB), Tavily (Web Search)
- **Key Features**: PDF processing, text-to-speech streaming, voice interaction

---

## ✅ Prerequisites

Before running the project, ensure you have:

1. **Python 3.10+** installed (Currently using: Python 3.10.6 ✓)
2. **uv package manager** installed (Currently using: uv 0.9.26 ✓)
3. **API Keys** configured in [.env](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env) file (Already configured ✓)

---

## 🔧 Installation Steps

### 1. Navigate to Project Directory

```bash
cd W:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend
```

### 2. Sync Dependencies

The project uses `uv` for dependency management. All dependencies are defined in [pyproject.toml](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/pyproject.toml).

```bash
uv sync
```

This will:

- Install Python 3.14.2 (as specified in pyproject.toml)
- Install all 48 required packages including:
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `openai` - OpenAI API client
  - `pinecone-client` - Vector database
  - `pypdf` - PDF processing
  - `edge-tts` - Microsoft Edge TTS
  - `tiktoken` - Token counting
  - And more...

---

## 🏃 Running the Server

### Option 1: Using uv (Recommended)

```bash
uv run app/main.py
```

### Option 2: Using Python directly

```bash
python app/main.py
```

### Option 3: Using uvicorn

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on **http://localhost:8000** with auto-reload enabled.

---

## 🧪 Testing the API

### 1. Access Interactive API Documentation

Open your browser and navigate to:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Test Basic Endpoint

```bash
curl http://localhost:8000/
```

Expected response:

```json
{
  "message": "TRIAM Backend is running fast with uv!"
}
```

### 3. Test Voice Streaming (OpenAI TTS)

Open in browser:

```
http://localhost:8000/test-voice-stream?text=Xin chào, đây là thử nghiệm
```

Or use curl:

```bash
curl "http://localhost:8000/test-voice-stream?text=Công nghệ thông tin" --output test.mp3
```

### 4. Test Voice Streaming (Edge TTS - Free)

```
http://localhost:8000/test-voice-stream-edge?text=Xin chào TRIAM
```

### 5. Test PDF Upload

Using the Swagger UI at http://localhost:8000/docs:

1. Navigate to `/api/v1/upload-pdf` endpoint
2. Click "Try it out"
3. Upload a PDF file
4. Execute the request

---

## 📁 Project Structure

```
triam-backend/
├── .env                    # API keys and configuration
├── pyproject.toml          # Dependencies and project metadata
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── core/              # Configuration
│   │   └── config.py      # Settings and environment variables
│   ├── api/               # API routes
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── upload.py   # PDF upload endpoint
│   │           └── chat.py     # Chat endpoints
│   ├── services/          # Business logic
│   │   ├── tts_service.py      # Text-to-Speech streaming
│   │   ├── llm_service.py      # LLM processing
│   │   └── pdf_service.py      # PDF processing
│   └── schemas/           # Pydantic models
```

---

## 🔑 Environment Variables

The [.env](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env) file contains the following API keys (already configured):

```env
# OpenAI API
OPENAI_API_KEY=sk-proj-...

# Pinecone Vector Database
PINECONE_API_KEY=pcsk_...
PINECONE_ENV=us-east-1

# Tavily Search API
TAVILY_API_KEY=tvly-dev-...

# Google Gemini API
GEMINI_API_KEY=AIzaSy...
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

> ⚠️ **Security Note**: Never commit the [.env](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env) file to version control!

---

## 🎯 Available Endpoints

| Method | Endpoint                  | Description                    |
| ------ | ------------------------- | ------------------------------ |
| GET    | `/`                       | Health check                   |
| GET    | `/test-voice-stream`      | Test OpenAI TTS streaming      |
| GET    | `/test-voice-stream-edge` | Test Edge TTS streaming (free) |
| POST   | `/api/v1/upload-pdf`      | Upload and process PDF files   |

---

## 🐛 Troubleshooting

### Issue: Port 8000 already in use

**Solution**: Change the port in [app/main.py](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/main.py) or kill the process using port 8000:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue: Module not found errors

**Solution**: Re-sync dependencies:

```bash
uv sync --reinstall
```

### Issue: API key errors

**Solution**: Verify your [.env](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env) file has valid API keys and is in the project root directory.

### Issue: Python version mismatch

**Solution**: The project requires Python 3.14+ as specified in [pyproject.toml](file:///W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/pyproject.toml). uv will automatically download and use the correct version.

---

## 📚 Next Steps

1. **Test Voice Streaming**: Try the `/test-voice-stream` endpoint
2. **Upload a PDF**: Use the `/api/v1/upload-pdf` endpoint
3. **Explore the Code**: Check out the services in `app/services/`
4. **Read Documentation**: Review `README.md` and `setup.md` for more details

---

## 🛠️ Development Commands

```bash
# Sync dependencies
uv sync

# Run the server with auto-reload
uv run app/main.py

# Run with custom port
uv run uvicorn app.main:app --port 8080

# Add a new dependency
uv add <package-name>

# Remove a dependency
uv remove <package-name>

# Update all dependencies
uv sync --upgrade
```

---

## 📞 Support

For issues or questions:

1. Check the `setup.md` file for detailed setup instructions
2. Review the `README.md` for project specifications
3. Examine the code in `app/` directory

---

**Happy Coding! 🎉**
