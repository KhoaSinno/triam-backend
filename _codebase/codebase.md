# Project Export

## Project Statistics

- Total files: 15

## Folder Structure

```
app
  api
    v1
      endpoints
        chat.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    config.py
    __init__.py
  main.py
  schemas
    __init__.py
  services
    embed.py
    llm_service.py
    pdf_service.py
    tts_service.py
    __init__.py
  __init__.py

```

### app\api\v1\endpoints\chat.py

```py
# Chat endpoint for Q&A
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(question: str):
    """
    Handle Q&A chat requests
    """
    # TODO: Implement chat logic with RAG
    return {"question": question, "answer": "Coming soon..."}

```

### app\api\v1\endpoints\upload.py

```py
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.services.pdf_service import extract_text_from_pdf, extract_chapters_smart
from app.services.llm_service import normalize_text_for_speech
from app.services.tts_service import stream_text_to_speech_edge, generate_audio_file_edge
from app.services.embed import embed_text_to_pinecone
import os
import uuid

router = APIRouter()
sem = asyncio.Semaphore(3)

async def process_single_chapter(book_id: str, chapter_data: dict, index: int):
    """
    Worker xử lý toàn diện: Rewrite -> TTS -> Save DB -> Embed Pinecone
    """
    async with sem: # <--- Kiểm soát luồng vào
        try:
            print(f"--- Đang xử lý chương {index+1}... ---")

            # 1. REWRITE (Gemini)
            rewritten_text = await normalize_text_for_speech(chapter_data["text"])
            
            # 2. TTS (EdgeTTS)
            # Lưu ý: Đặt tên file theo book_id để quản lý
            # audio_filename = f"uploads/{book_id}_chap_{index + 1}.mp3"
            # await generate_audio_file_edge(rewritten_text, audio_filename)
            
            # 3. RAG PREPARATION (Pinecone) - QUAN TRỌNG
            # Chúng ta embed text đã rewrite để AI trả lời câu hỏi user chính xác hơn
            await embed_text_to_pinecone(book_id, index, rewritten_text) 

            # 4. SAVE TO DB (Firebase/Mongo)
            # Cập nhật trạng thái chương này là "DONE" và lưu URL audio
            # await db.update_chapter_status(book_id, index, status="ready", audio_url=audio_filename)

            print(f"--- Xong chương {index+1} ---")
            
        except Exception as e:
            print(f"Lỗi chương {index + 1}: {e}")
            # await db.update_chapter_status(book_id, index, status="error", error=str(e))

@router.post("/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks, # <--- Vũ khí bí mật
    file: UploadFile = File(...)
):
    # 1. Tạo Book ID & Extract (Vẫn phải chờ bước này để có khung sườn)
    book_id = str(uuid.uuid4())
    chapters = await extract_chapters_smart(file.file)
    
    # 2. Lưu khung sườn (Skeleton) vào DB trước với status="pending"
    # await db.create_book_record(book_id, chapters)

    # 3. Đẩy việc nặng vào Background (User nhận phản hồi NGAY LẬP TỨC)
    # Lưu ý: BackgroundTasks trong FastAPI chạy tuần tự hoặc song song tùy cách gọi.
    # Để chạy song song trong background, ta wrap vào 1 hàm async lớn.
    
    background_tasks.add_task(run_background_processing, book_id, chapters)

    return {
        "message": "Upload thành công! Chúng tôi đang xử lý sách của bạn.",
        "book_id": book_id,
        "total_chapters": len(chapters)
    }

async def run_background_processing(book_id: str, chapters: list):
    """Hàm quản lý việc chạy song song trong background"""
    tasks = []
    for i, chapter in enumerate(chapters):
        tasks.append(process_single_chapter(book_id, chapter, i))
    
    # Chạy tất cả, nhưng bị kìm hãm bởi Semaphore(3)
    await asyncio.gather(*tasks)
    print(f"=== HOÀN TẤT XỬ LÝ SÁCH {book_id} ===")



# async def process_single_chapter_pipeline(chapter_data: dict, index: int, filename_prefix: str):
#     """
#     Hàm worker: Nhận nhiệm vụ xử lý trọn gói 1 chương từ A-Z.
#     Flow: Text gốc -> Rewrite -> TTS -> Done.
#     """
#     try:
#         # 1. REWRITE (Gọi Gemini - I/O Bound)
#         # Chạy độc lập, không cần chờ chương khác
#         rewritten_text = await normalize_text_for_speech(chapter_data["text"])
        
#         # Cập nhật lại text vào object (để trả về FE)
#         chapter_data["text"] = rewritten_text
        
#         # 2. TTS (Gọi EdgeTTS - I/O Bound)
#         # Tạo tên file output
#         output_path = f"uploads/{filename_prefix}_chapter_{index + 1}.mp3"
        
#         # Đảm bảo thư mục tồn tại
#         os.makedirs("uploads", exist_ok=True)
        
#         await generate_audio_file_edge(rewritten_text, output_path)
        
#         return chapter_data
#     except Exception as e:
#         print(f"Lỗi xử lý chương {index + 1}: {e}")
#         # Trả về data lỗi hoặc gốc để không làm crash cả hệ thống
#         chapter_data["error"] = str(e)
#         return chapter_data

# @router.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     """
#     Upload and process PDF file (High Performance Mode)
#     """
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

#     # 1. Extract Chapters (Nặng CPU - vẫn phải chờ)
#     chapters = await extract_chapters_smart(file.file)

#     # 2. CHUẨN BỊ TASK XỬ LÝ SONG SONG (Concurrent)
#     # Thay vì await từng dòng, ta gom việc lại thành danh sách tasks
#     tasks = []
    
#     # Chỉ lấy tối đa 3 chương đầu để test (tránh lỗi index nếu sách chỉ có 1 chương)
#     limit = min(len(chapters), 3) 
    
#     for i in range(limit):
#         # Tạo task nhưng CHƯA CHẠY NGAY, chỉ mới lên lịch
#         task = process_single_chapter_pipeline(
#             chapter_data=chapters[i],
#             index=i,
#             filename_prefix=file.filename
#         )
#         tasks.append(task)

#     # 3. KÍCH HOẠT ĐA LUỒNG ("FIRE" ALL TASKS)
#     # asyncio.gather sẽ chạy tất cả các task cùng lúc.
#     # Thời gian hoàn thành = Thời gian của task lâu nhất (thay vì tổng thời gian)
#     processed_chapters = await asyncio.gather(*tasks)

#     # Return kết quả
#     return {
#         "filename": file.filename, 
#         "chapters": processed_chapters, # Đã chứa text rewrite
#         "message": f"Đã xử lý xong {len(processed_chapters)} chương."
#     }

@router.post("/process-book-intro")
async def process_book_intro(file: UploadFile = File(...)):
    """
    Flow Demo:
    1. User upload PDF.
    2. Server đọc 1-2 trang đầu.
    3. LLM sửa lỗi chính tả/viết tắt (CNTT -> Công nghệ thông tin).
    4. TTS đọc stream về ngay lập tức.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    # 1. Extract Text (Lấy 2 trang đầu làm Intro)
    raw_text = await extract_text_from_pdf(file, max_pages=2)

    if not raw_text:
        raise HTTPException(status_code=400, detail="Không đọc được nội dung PDF")

    # 2. Normalize (Biên tập lại - Bước quan trọng nhất!)
    # Cắt ngắn bớt nếu quá dài để demo cho nhanh (lấy 1000 ký tự đầu)
    short_preview = raw_text[:1000]
    script_ready = await normalize_text_for_speech(short_preview)

    print(f"Original: {short_preview[:100]}...")
    print(f"Normalized: {script_ready[:100]}...")

    # 3. Stream Audio về App (Dùng Edge TTS miễn phí)
    return StreamingResponse(
        stream_text_to_speech_edge(script_ready),
        media_type="audio/mpeg"
    )

```

### app\api\v1\endpoints\__init__.py

```py
# API Endpoints module

```

### app\api\v1\__init__.py

```py
# API v1 module

```

### app\api\__init__.py

```py
# API v1 module

```

### app\core\config.py

```py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()

```

### app\core\__init__.py

```py
# Core module

```

### app\main.py

```py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.services.tts_service import stream_text_to_speech, stream_text_to_speech_edge
from app.api.v1.endpoints import upload  # Import router upload

app = FastAPI(title="TRIAM Assistant API")

# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])

@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}

@app.get("/test-voice-stream")
async def test_voice_stream(text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM."):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(
        stream_text_to_speech(text),
        media_type="audio/mpeg"
    )

@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM."):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(
        stream_text_to_speech_edge(text),
        media_type="audio/mpeg"
    )

if __name__ == "__main__":
    import uvicorn
    # Reload=True để code tới đâu server cập nhật tới đó
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

```

### app\schemas\__init__.py

```py
# Schemas module

```

### app\services\embed.py

```py
import os
from pinecone import Pinecone
from openai import AsyncOpenAI
import uuid

# Khởi tạo OpenAI
aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Khởi tạo Pinecone (Client v3+)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = "triam-knowledge-base"  # Tên Index bạn đã tạo trên Web Console
index = pc.Index(INDEX_NAME)



async def embed_text_to_pinecone(book_id: str, chapter_index: int, text: str):
    """
    Hàm xử lý RAG: Cắt nhỏ text -> Embed -> Lưu vào Pinecone.
    """
    try:
        # 1. CHUNKING (Cắt nhỏ văn bản)
        # Tại sao cần cắt? Vì Vector search hoạt động tốt nhất với các đoạn văn ngắn (context).
        # Cách đơn giản: Cắt theo đoạn văn (xuống dòng kép)
        chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 50]
        
        # Nếu text không có xuống dòng, cắt thô mỗi 1000 ký tự (Fallback)
        if not chunks:
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        print(f"-> Pinecone: Đang xử lý {len(chunks)} chunks cho chương {chapter_index + 1}...")

        vectors_to_upsert = []

        # 2. EMBEDDING (Tạo vector)
        # OpenAI hỗ trợ batch embedding, ta gửi cả list chunks đi 1 lần cho nhanh
        response = await aclient.embeddings.create(
            input=chunks,
            model="text-embedding-3-small" # Rẻ và nhanh, đủ dùng cho RAG
        )

        # 3. CHUẨN BỊ DATA (Format cho Pinecone)
        for i, embedding_data in enumerate(response.data):
            chunk_text = chunks[i]
            vector_id = f"{book_id}_chap{chapter_index}_{i}" # ID duy nhất
            
            # Vector Record
            vector_record = {
                "id": vector_id,
                "values": embedding_data.embedding,
                # Metadata cực quan trọng để AI biết đoạn này là chữ gì
                "metadata": {
                    "book_id": book_id,
                    "chapter_index": chapter_index,
                    "text": chunk_text, # Lưu text gốc để hồi đáp user
                    "source": "triam_app"
                }
            }
            vectors_to_upsert.append(vector_record)

        # 4. UPSERT (Đẩy lên Cloud)
        # Sử dụng namespace để tách biệt dữ liệu (optional, nhưng recommend)
        # Namespace giúp bạn xóa sách dễ dàng: index.delete(delete_all=True, namespace=book_id)
        index.upsert(vectors=vectors_to_upsert, namespace=book_id)
        
        print(f"-> Pinecone: Đã lưu {len(vectors_to_upsert)} vectors vào namespace '{book_id}'.")
        return True

    except Exception as e:
        print(f"Lỗi Embed Pinecone: {e}")
        return False
```

### app\services\llm_service.py

```py
from openai import AsyncOpenAI
from app.core.config import settings

# client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Prompt "thần thánh" để định hình phong cách đọc
SYSTEM_PROMPT_REWRITE = """
Bạn là một biên tập viên phát thanh chuyên nghiệp (Script Editor).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (Spoken Script) để AI TTS đọc tự nhiên nhất.

QUY TẮC BẮT BUỘC:
1. Mở rộng từ viết tắt: Dựa vào ngữ cảnh, hãy viết đầy đủ các từ viết tắt.
   - Ví dụ: "CNTT" -> "Công nghệ thông tin", "DN" -> "Doanh nghiệp", "NS" -> "Nhân sự".
2. Xử lý Tiếng Anh/Thuật ngữ:
   - Các từ tiếng Anh phổ biến (AI, CEO, Marketing) -> Giữ nguyên (nếu bộ đọc tốt) hoặc chú thích phiên âm nếu cần.
   - Ví dụ đặc biệt: "AI" -> "Ây Ai", "Agile" -> "A-chao".
3. Số liệu & Ký hiệu:
   - "5%" -> "Năm phần trăm".
   - "Tp.HCM" -> "Thành phố Hồ Chí Minh".
4. Xử lý lỗi PDF & Format (Quan trọng nhất):
   - Nối các dòng bị ngắt quãng giữa chừng do lỗi PDF (line break).
   - Loại bỏ số trang (ví dụ số "10", "11" nằm trơ trọi cuối đoạn).
   - Xóa các ký tự rác do lỗi font (ví dụ: "J", "", các dấu gạch ngang vô nghĩa).
   - Tự động sửa lỗi chính tả hiển nhiên (ví dụ: "Qcmenia" -> "Armenia").
5. Tự nhiên hóa số liệu & Thời gian (Văn nói người Việt):
   - "1,5 giờ" -> Chuyển thành "một tiếng rưỡi" (KHÔNG dùng "một phẩy năm giờ").
   - "0.5" -> "nửa" hoặc "không phẩy năm" tùy ngữ cảnh.
   - "30km" -> "ba mươi ki-lô-mét".
   - "1990" -> "năm một ngàn chín trăm chín mươi".
   - Danh sách "1. 2. 3." -> Chuyển thành "Điều thứ nhất: ... Điều thứ hai: ... Điều thứ ba: ..." (để tạo nhịp điệu).

6. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

Input: Văn bản gốc từ sách.
Output: Chỉ trả về văn bản đã biên tập, không thêm lời chào hay giải thích gì khác.
"""

async def normalize_text_for_speech(raw_text: str) -> str:
    """
    Gửi text thô cho GPT-4o-mini biên tập lại trước khi đọc.
    Dùng model 'gpt-4o-mini' cho rẻ và nhanh (Latency thấp).
    """
    try:
        response = await client.chat.completions.create(
            # model="gpt-4o-mini",
            model="gemini-2.5-flash-lite",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_REWRITE},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3,  # Giữ cho AI tập trung, ít sáng tạo lung tung
            # max_tokens=2000   # Giới hạn output
        )
        normalized_text = response.choices[0].message.content
        return normalized_text
    except Exception as e:
        print(f"Lỗi Normalization: {e}")
        return raw_text  # Fallback: Nếu lỗi thì trả về text gốc đọc tạm

```

### app\services\pdf_service.py

```py
# app/services/pdf_service.py
import pdfplumber
from pypdf import PdfReader
import re

def get_pdf_outline_structure(file_obj):
    """
    Hàm này cố gắng đọc Mục lục (Bookmarks) từ metadata của PDF.
    Trả về: List [{"title": "Chapter 1", "page_start": 5}, ...] hoặc [] nếu không có.
    """
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        # reader.outline chứa cấu trúc mục lục
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    # Đệ quy nếu có mục lục con (Sub-chapter)
                    _parse_outline(item)
                else:
                    try:
                        # Lấy số trang (pypdf trả về page object, cần lấy index)
                        page_number = reader.get_destination_page_number(item)
                        # +1 vì pypdf đếm từ 0, còn ta hay tư duy từ 1
                        outline_data.append({
                            "title": item.title,
                            "page_start": page_number + 1 
                        })
                    except Exception:
                        pass # Bỏ qua nếu item bị lỗi link
        
        _parse_outline(reader.outline)
        
        # Sắp xếp lại theo số trang để chắc chắn thứ tự đúng
        outline_data.sort(key=lambda x: x["page_start"])
        return outline_data
    except Exception as e:
        print(f"Lỗi đọc Outline: {e}")
        return []

async def extract_chapters_smart(file_obj, pages_per_chunk=10):
    """
    Hàm xử lý thông minh 3 cấp độ:
    Level 1: Dùng Outline (Mục lục ẩn).
    Level 2: Dùng Regex quét text.
    Level 3: Cắt theo số trang cố định.
    """
    # --- LEVEL 1: Dùng Mục lục Metadata ---
    # Lưu ý: Phải reset pointer file về 0 trước khi đọc
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)
    
    chapters = []
    
    if outlines and len(outlines) > 1:
        print(">> Đã tìm thấy Mục lục Metadata (Outline). Sử dụng Level 1.")
        
        # Mở lại bằng pdfplumber để lấy text (pdfplumber extract text ngon hơn pypdf)
        file_obj.seek(0)
        with pdfplumber.open(file_obj) as pdf:
            total_pages = len(pdf.pages)
            
            for i in range(len(outlines)):
                current_chap = outlines[i]
                start_p = current_chap["page_start"] - 1 # index từ 0
                
                # Xác định trang kết thúc (là trang bắt đầu của chương sau - 1)
                if i < len(outlines) - 1:
                    end_p = outlines[i+1]["page_start"] - 1
                else:
                    end_p = total_pages # Chương cuối thì lấy hết
                
                # Đảm bảo không vượt quá file
                end_p = min(end_p, total_pages)
                
                # Gom text từ start_p đến end_p
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    text = pdf.pages[p_idx].extract_text()
                    if text:
                        chap_text += text + "\n"
                
                if chap_text.strip():
                    chapters.append({
                        "title": current_chap["title"],
                        "text": chap_text,
                        "page_start": start_p + 1,
                        "page_end": end_p
                    })
        return chapters

    # --- LEVEL 2: Dùng Regex (Nếu Level 1 thất bại) ---
    print(">> Không có Mục lục Metadata. Chuyển sang Level 2 (Regex Scan).")
    file_obj.seek(0)
    
    # Compile regex patterns cho tiêu đề chương
    chapter_patterns = [
        r'^\s*(?:Chương|CHƯƠNG|Chapter|CHAPTER)\s+(?:[IVX]+|\d+)',  # Chương 1, Chapter I, etc.
        r'^\s*(?:Phần|PHẦN|Part|PART)\s+(?:[IVX]+|\d+)',  # Phần 1, Part I, etc.
    ]
    combined_pattern = re.compile('|'.join(chapter_patterns), re.MULTILINE)
    
    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        chapter_markers = []  # List of {title, page_idx}
        
        # Quét từng trang tìm tiêu đề
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            
            # Tách thành từng dòng và kiểm tra
            lines = text.split('\n')
            for line in lines[:10]:  # Chỉ check 10 dòng đầu mỗi trang
                if combined_pattern.match(line.strip()):
                    chapter_markers.append({
                        'title': line.strip(),
                        'page_idx': page_idx
                    })
                    break  # Tìm được tiêu đề rồi thì next page
        
        # Nếu tìm được ít nhất 2 chương
        if len(chapter_markers) >= 2:
            print(f">> Tìm được {len(chapter_markers)} chương bằng Regex.")
            
            for i in range(len(chapter_markers)):
                start_p = chapter_markers[i]['page_idx']
                
                # Xác định trang kết thúc
                if i < len(chapter_markers) - 1:
                    end_p = chapter_markers[i+1]['page_idx']
                else:
                    end_p = total_pages
                
                # Extract text từ start đến end
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    chap_text += (pdf.pages[p_idx].extract_text() or "") + "\n"
                
                if chap_text.strip():
                    chapters.append({
                        "title": chapter_markers[i]['title'],
                        "text": chap_text,
                        "page_start": start_p + 1,
                        "page_end": end_p
                    })
            
            return chapters  # Return kết quả Level 2
    
    # --- LEVEL 3: Cắt Page cố định (Fallback cuối cùng) ---
    print(">> Không quét được tiêu đề. Chuyển sang Level 3 (Fixed Page Chunk).")
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        for i in range(0, total_pages, pages_per_chunk):
            chunk_text = ""
            end_page = min(i + pages_per_chunk, total_pages)
            for p_idx in range(i, end_page):
                chunk_text += (pdf.pages[p_idx].extract_text() or "") + "\n"
            
            chapters.append({
                "title": f"Phần {i//pages_per_chunk + 1} (Trang {i+1}-{end_page})",
                "text": chunk_text,
                "page_start": i + 1,
                "page_end": end_page
            })
            
    return chapters


async def extract_text_from_pdf(file_obj, max_pages=None):
    """
    Helper function: Extract raw text từ PDF (không chia chương).
    Dùng cho demo endpoints như /process-book-intro.
    
    Args:
        file_obj: File object của PDF
        max_pages: Số trang tối đa cần extract (None = all pages)
    
    Returns:
        str: Raw text từ PDF
    """
    file_obj.seek(0)
    extracted_text = ""
    
    with pdfplumber.open(file_obj) as pdf:
        pages_to_read = len(pdf.pages) if max_pages is None else min(max_pages, len(pdf.pages))
        
        for i in range(pages_to_read):
            text = pdf.pages[i].extract_text()
            if text:
                extracted_text += text + "\n"
    
    return extracted_text.strip()




def extract_text_by_page_range(pdf_obj, start_page: int, end_page: int):
    """
    Trích xuất text từ trang A đến trang B.
    - pdf_obj: Đối tượng pdfplumber đã mở.
    - start_page: Số trang thực tế (ví dụ: 5).
    - end_page: Số trang thực tế (ví dụ: 10).
    -> Trả về text của trang 5, 6, 7, 8, 9, 10.
    """
    extracted_text = ""
    
    # Validate: Đảm bảo trang kết thúc không vượt quá tổng số trang
    total_pages = len(pdf_obj.pages)
    if end_page > total_pages:
        end_page = total_pages
    
    # Vòng lặp lấy text
    # LƯU Ý: Python index bắt đầu từ 0. 
    # Nếu muốn lấy trang 5 (start_page), index phải là 4 (start_page - 1).
    # Hàm range(a, b) chạy đến b-1, nên tham số thứ 2 là end_page (tương ứng index end_page-1)
    
    # Ví dụ: Lấy trang 5 đến 7.
    # start_page=5 -> index=4
    # end_page=7
    # range(4, 7) sẽ chạy qua index: 4 (trang 5), 5 (trang 6), 6 (trang 7). CHUẨN.
    
    for i in range(start_page - 1, end_page):
        try:
            page = pdf_obj.pages[i]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception as e:
            print(f"Lỗi đọc trang {i+1}: {e}")
            
    return extracted_text




def extract_clean_text(page):
    """
    Chỉ lấy phần thân trang, bỏ Header (trên cùng) và Footer (số trang dưới cùng)
    """
    width = page.width
    height = page.height
    
    # Giả sử Header chiếm 50px trên cùng, Footer chiếm 50px dưới cùng
    # Tọa độ crop: (x0, top, x1, bottom)
    bounding_box = (0, 50, width, height - 50) 
    
    try:
        cropped_page = page.crop(bounding_box)
        return cropped_page.extract_text()
    except ValueError:
        # Fallback nếu trang không crop được (ví dụ trang trắng)
        return page.extract_text()
```

### app\services\tts_service.py

```py
from openai import AsyncOpenAI
from app.core.config import settings
import edge_tts
import asyncio # Need to install

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def stream_text_to_speech(text: str, voice: str = "alloy"):
    """
    Hàm này nhận text, gọi OpenAI TTS và trả về stream audio ngay lập tức.
    """
    try:
        # Gọi API OpenAI với response_format để stream
        async with client.audio.speech.with_streaming_response.create(
            model="tts-1",  # Model nhanh nhất, độ trễ thấp
            voice=voice,
            input=text
        ) as response:
            # Streaming response (Chunking 4096 bytes để gửi dần xuống client)
            async for chunk in response.iter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk

    except Exception as e:
        print(f"Error in TTS Stream: {e}")
        # Trong thực tế nên log vào file hoặc Sentry

async def stream_text_to_speech_edge(text: str, voice: str = "vi-VN-HoaiMyNeural"):
    """
    Sử dụng Edge TTS: Hoàn toàn MIỄN PHÍ và chất lượng Neural rất tốt.
    """
    communicate = edge_tts.Communicate(text, voice)
    
    # Streaming response
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


# Production ready
# async def generate_audio_file(text: str, file_path: str):
#     """
#     Tạo audio và lưu xuống ổ cứng (sau này là upload lên Firebase Storage).
#     """
#     try:
#         response = await client.audio.speech.create(
#             model="tts-1",
#             voice="alloy",
#             input=text
#         )
#         # Lưu file binary xuống đĩa
#         response.stream_to_file(file_path)
#         return True
#     except Exception as e:
#         print(f"Lỗi TTS: {e}")
#         return False


# Create audio file wiht edge tts


async def generate_audio_file_edge(text: str, filename: str, voice: str = "vi-VN-HoaiMyNeural"):
    """
    Tạo file audio từ text bằng Edge TTS và lưu vào file.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"✓ Audio saved to {filename}")
    except Exception as e:
        print(f"Error creating audio file: {e}")

# Example usage:
# asyncio.run(create_audio_file("Xin chào, đây là bài test giọng nói.", "test.mp3"))

```

### app\services\__init__.py

```py
# Services module

```

### app\__init__.py

```py
# TRIAM Backend Application

```
