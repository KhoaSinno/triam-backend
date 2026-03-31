# Project Export

## Project Statistics

- Total files: 22

## Folder Structure

```
app
  api
    v1
      endpoints
        chat.py
        live.py
        upload.py
        __init__.py
      __init__.py
    __init__.py
  core
    config.py
    supabase.py
    __init__.py
  main.py
  schemas
    __init__.py
  services
    embed.py
    llm_service.py
    pdf_service.py
    rag_service.py
    tts_service.py
    __init__.py
  __init__.py
.dockerignore
.python-version
Dockerfile
pyproject.toml

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

### app\api\v1\endpoints\live.py

```py
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types
from tavily import AsyncTavilyClient

from app.core.config import settings
from app.services.rag_service import search_book_knowledge

tavily_client = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
router = APIRouter()

client = genai.Client(api_key=settings.GEMINI_API_KEY, http_options={"api_version": "v1beta"})
# =======OLD SYSTEM INSTRUCTION=======
# SYSTEM_INSTRUCTION = """
# Bạn là Trợ lý TRIAM, một chuyên gia hỗ trợ học tập qua giọng nói.
# Nhiệm vụ của bạn:
# 1. Luôn ưu tiên sử dụng công cụ 'search_book_knowledge' để tìm câu trả lời trong sách của người dùng.
# 2. Nếu thông tin không có trong sách, hãy dùng kiến thức nền của bạn để trả lời.
# 3. Trả lời bằng giọng nói thân thiện, ngắn gọn, tập trung vào việc giúp người dùng hiểu bài.
# """
SYSTEM_INSTRUCTION = """
Bạn là Trợ lý TRIAM - Người hỗ trợ cho người dùng đọc sách qua giọng nói. Bạn có 2 công cụ hỗ trợ:
1. 'search_book_knowledge': Dùng để tìm trong sách của người dùng. Luôn ưu tiên cái này trước.
2. 'search_web': Dùng để tìm thông tin từ Internet nếu sách không có câu trả lời hoặc câu hỏi là về tin tức/kiến thức chung.
Hãy trả lời ngắn gọn, súc tích bằng giọng nói thân thiện.
"""

# Model hỗ trợ native audio output
MODEL_ID = "gemini-2.5-flash-native-audio-latest"

# Audio format constants (PCM 16-bit, mono)
SEND_SAMPLE_RATE = 16000  # Microphone input rate
RECEIVE_SAMPLE_RATE = 24000  # AI output rate

# NOTE: google_search grounding tool CANNOT be combined with function_declarations
# in the Gemini Live API — it causes a server-side 1008 error after tool responses.
tools_config = [
    types.Tool(
        function_declarations=[
            # Tool search book knowledge in supabase
            types.FunctionDeclaration(
                name="search_book_knowledge",
                description="Tra cứu kiến thức trong sách khi user hỏi về nội dung sách.",
                parameters={
                    "type": "OBJECT",
                    "properties": {"query": {"type": "STRING", "description": "Câu hỏi tra cứu"}},
                    "required": ["query"],
                },
            ),
            # Tool Tavily search web input for llm (rag)
            types.FunctionDeclaration(
                name="search_web",
                description="Tìm kiếm Internet bằng Tavily khi cần kiến thức cập nhật hoặc sách không có.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Câu hỏi tìm kiếm trên web",
                        }
                    },
                    "required": ["query"],
                },
            ),
        ]
    ),
]


@router.websocket("/ws/live-assistant/{book_id}")
async def live_assistant_endpoint(websocket: WebSocket, book_id: str):
    """
    WebSocket endpoint for real-time voice conversation via Gemini Live API.

    Protocol:
    - Client → Server: raw PCM audio bytes (16kHz, 16-bit, mono)
    - Server → Client: raw PCM audio bytes (24kHz, 16-bit, mono) — AI voice response
    """
    await websocket.accept()

    config = types.LiveConnectConfig(
        tools=tools_config,
        system_instruction=types.Content(parts=[types.Part(text=SYSTEM_INSTRUCTION)]),
        generation_config=types.GenerationConfig(response_modalities=["AUDIO"]),
    )

    try:
        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            print("✅ Đã kết nối Gemini Live")

            async def send_to_gemini():
                """
                Reads PCM audio bytes from the WebSocket and streams them
                to Gemini using send_realtime_input — the correct Live API method.
                """
                try:
                    while True:
                        data = await websocket.receive_bytes()
                        await session.send_realtime_input(audio={"data": data, "mime_type": "audio/pcm"})
                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (send loop)")
                except Exception as e:
                    print(f"❌ Lỗi gửi audio: {e}")

            async def receive_from_gemini():
                """
                Receives responses from Gemini using the async-for pattern shown
                in the reference code. Sends audio chunks to the client immediately.
                Handles tool calls (RAG search) inline.
                """
                result_text = ""
                try:
                    # Single async-for loop — the correct pattern from the reference code
                    async for response in session.receive():
                        server_content = response.server_content

                        # ── Audio response ──────────────────────────────────
                        if server_content and server_content.model_turn:
                            for part in server_content.model_turn.parts:
                                if part.inline_data and isinstance(part.inline_data.data, bytes):
                                    # Send audio chunk directly to client (no large buffer)
                                    await websocket.send_bytes(part.inline_data.data)

                        # ── Turn complete — AI finished speaking ─────────────
                        if server_content and server_content.turn_complete:
                            print("🔔 Gemini turn complete")

                        # ── Tool call: RAG search ────────────────────────────
                        if response.tool_call:
                            for call in response.tool_call.function_calls:
                                tool_name = call.name
                                if tool_name == "search_book_knowledge":
                                    query = call.args.get("query", "")
                                    print(f"🔍 RAG search: {query} (call.id={call.id})")
                                    if not call.id:
                                        print("⚠️ Bỏ qua tool call vì call.id là None")
                                        continue
                                    try:
                                        context = await search_book_knowledge(query, book_id)
                                        result_text = context
                                    except Exception as rag_err:
                                        print(f"❌ Lỗi RAG search: {rag_err}")
                                        result_text = "Không thể tra cứu thông tin lúc này."
                                elif tool_name == "search_web":
                                    # Gọi Tavily Search
                                    print("🌐 Đang search Tavily...")
                                    query = call.args.get("query", "")
                                    try:
                                        search_result = await tavily_client.search(
                                            query=query,
                                            search_depth="basic",  # "advanced" cho chất lượng cao nhất
                                            max_results=3,
                                        )
                                    except Exception as tavily_err:
                                        print(f"❌ Lỗi Tavily search: {tavily_err}")
                                        result_text = "Không thể tra cứu thông tin lúc này."
                                    # Tóm tắt kết quả cho Gemini đọc
                                    result_text = "\n".join([f"- {r['content']}" for r in search_result["results"]])
                                try:
                                    await session.send_tool_response(
                                        function_responses=[
                                            types.FunctionResponse(
                                                name=tool_name,
                                                id=call.id,
                                                response={"result": result_text},
                                            )
                                        ]
                                    )
                                    print(f"✅ Đã gửi {tool_name} response cho call.id={call.id}")
                                except Exception as send_err:
                                    print(f"❌ Lỗi gửi tool response: {send_err}")
                except WebSocketDisconnect:
                    print("📴 Client ngắt kết nối (receive loop)")
                except Exception as e:
                    print(f"❌ Lỗi nhận audio: {e}")

            # Run both tasks concurrently; cancel the other when one finishes
            await asyncio.gather(send_to_gemini(), receive_from_gemini())

    except WebSocketDisconnect:
        print("📴 Client ngắt kết nối trước khi kết nối Gemini")
    except Exception as e:
        print(f"❌ Lỗi kết nối Gemini Live: {e}")
        try:
            await websocket.send_text(f"Lỗi kết nối Gemini Live: {e}")
        except Exception:
            pass

```

### app\api\v1\endpoints\upload.py

```py
import asyncio
import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.core.supabase import supabase
from app.services.embed import embed_chunk_to_supbabase
from app.services.llm_service import normalize_text_for_speech
from app.services.pdf_service import extract_chapters_smart
from app.services.tts_service import (
    generate_audio_file_edge,
)

logger = logging.getLogger("upload")

router = APIRouter()
sem = asyncio.Semaphore(3)

async def upload_to_supabase(local_path: str, storage_path: str, max_retries: int = 3):
    """Hàm hỗ trợ upload file và trả về public URL"""
    # Validate file
    file_size = os.path.getsize(local_path)
    max_size = 20 * 1024 * 1024 # 20MB
    if file_size > max_size:
        raise HTTPException(status_code=400, detail=f"File size exceeds maximum limit of {max_size} bytes")
    # Upload file
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, 'rb') as f:
                file_bytes = await f.read()

                supabase.storage.from_("audios").upload(
                    path=storage_path,
                    file=file_bytes,
                    file_options={"content-type": "audio/mpeg"}
                )
            # Lấy URL công khai
            return supabase.storage.from_("audios").get_public_url(storage_path)

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Upload failed, retrying... ({attempt + 1}/{max_retries})")
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise


async def process_single_chapter(book_id: str, chapter_data: dict, index: int):
    async with sem:
        chapter_id = None  # Initialize to prevent UnboundLocalError
        try:
            # 1. REWRITE
            obj_chapter = await normalize_text_for_speech(chapter_data["text"])
            main_chunks: list[str] = obj_chapter.get("main_scripts", [])
            review_text: str = obj_chapter.get("sub_scripts", "")

            # Insert tbl "chappters"
            chapter_id = supabase.table("chapters").insert({
                "book_id": book_id,
                "chapter_index": index,
                "title": chapter_data.get("title", f"Chương {index+1}"),
                "review_text": review_text
            }).execute().data[0]['id']

            segments_to_insert = []
            # 2. TTS AND STORAGE TO CLOUD
            for i, chunk in enumerate(main_chunks):
                local_filename = f"{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(chunk, local_filename)
                logger.info(f"Generated audio file: {local_filename}")
                storage_path = f"{book_id}/chap_{index + 1}/part_{i + 1}.mp3"
                # Upload to Supabase Storage
                public_url = await upload_to_supabase(local_filename, storage_path)
                logger.info(f"Uploaded audio file: {public_url}")

                # Delete local file
                if os.path.exists(local_filename):
                    os.remove(local_filename)

                segments_to_insert.append({
                    "chapter_id": chapter_id,
                    "segment_index": i,
                    "audio_url": public_url,
                    "text_content": chunk,
                })

            # 3. SAVE PLAYLIST TO DB
            if segments_to_insert:
                supabase.table("chapter_segments").insert(segments_to_insert).execute()

            # 4. HANDLE REVIEW SCRIPT
            if review_text:
                local_filename = f"{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(review_text, local_filename)
                # logger.info(f"Generated review audio file: {local_filename}")
                storage_path = f"{book_id}/chap_{index + 1}/review.mp3"
                public_url = await upload_to_supabase(local_filename, storage_path)
                # logger.info(f"Uploaded review audio file: {public_url}")

                if os.path.exists(local_filename):
                    os.remove(local_filename)

                supabase.table("chapters").update({ "review_audio_url": public_url }).eq("id", chapter_id).execute()

            # 5. EMBEDDING TO SUPABASE
            await embed_chunk_to_supbabase(book_id, index, main_chunks)

            # 6. UPDATE STATUS TO READY
            supabase.table("chapters").update({
                "status": "ready"
            }).eq("id", chapter_id).execute()

        except Exception as e:
            # Rollback: Delete chapter and segments if chapter was created
            if chapter_id:
                try:
                    supabase.table("chapters").delete().eq("id", chapter_id).execute()
                except Exception as delete_error:
                    logger.error(f"Failed to rollback chapter {index + 1}: {delete_error}")
            logger.error(f"Error processing chapter {index + 1}: {e}")
            raise


@router.post("/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks, # <--- Vũ khí bí mật
    file: UploadFile = File(...)
):
    # 1. Tạo Book ID & Extract (Vẫn phải chờ bước này để có khung sườn)
    book_id = str(uuid.uuid4())
    chapters = await extract_chapters_smart(file.file)

    # 2. Lưu khung sườn (Skeleton) vào DB trước với status="pending"
    try:
        supabase.table("books").insert({
            "id": book_id,
            "title": file.filename.replace(".pdf", ""),
            "total_chapters": len(chapters),
            "status": "processing",
            "created_at": "now()"
        }).execute()
        logger.info(f"Created book record: {book_id} with {len(chapters)} chapters")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create book record: {str(e)}")

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
    try:
        tasks = []
        for i, chapter in enumerate(chapters):
            tasks.append(process_single_chapter(book_id, chapter, i))

        # Chạy tất cả, nhưng bị kìm hãm bởi Semaphore(3)
        await asyncio.gather(*tasks)

        # Update book status to completed
        supabase.table("books").update({
            "status": "completed"
        }).eq("id", book_id).execute()

        logger.info(f"✅ HOÀN TẤT XỬ LÝ SÁCH {book_id}")
    except Exception as e:
        # Update book status to error if processing fails
        supabase.table("books").update({
            "status": "error",
            "error_message": str(e)
        }).eq("id", book_id).execute()
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


# @router.post("/process-book-intro")
# async def process_book_intro(file: UploadFile = File(...)):
#     """
#     Flow Demo:
#     1. User upload PDF.
#     2. Server đọc 1-2 trang đầu.
#     3. LLM sửa lỗi chính tả/viết tắt (CNTT -> Công nghệ thông tin).
#     4. TTS đọc stream về ngay lập tức.
#     """
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

#     # 1. Extract Text (Lấy 2 trang đầu làm Intro)
#     raw_text = await extract_text_from_pdf(file, max_pages=2)

#     if not raw_text:
#         raise HTTPException(status_code=400, detail="Không đọc được nội dung PDF")

#     # 2. Normalize (Biên tập lại - Bước quan trọng nhất!)
#     # Cắt ngắn bớt nếu quá dài để demo cho nhanh (lấy 1000 ký tự đầu)
#     short_preview = raw_text[:1000]
#     script_ready = await normalize_text_for_speech(short_preview)

#     print(f"Original: {short_preview[:100]}...")
#     print(f"Normalized: {script_ready[:100]}...")

#     # 3. Stream Audio về App (Dùng Edge TTS miễn phí)
#     return StreamingResponse(
#         stream_text_to_speech_edge(script_ready),
#         media_type="audio/mpeg"
#     )

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
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

settings = Settings()

```

### app\core\supabase.py

```py
from dotenv import load_dotenv
from supabase import Client, create_client

from app.core.config import settings

load_dotenv()

url: str = settings.SUPABASE_URL
# Use service role key for backend operations (bypasses RLS)
# Fall back to anon key if service role key is not set
key: str = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

```

### app\core\__init__.py

```py
# Core module

```

### app\main.py

```py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.api.v1.endpoints import live, upload
from app.services.tts_service import stream_text_to_speech, stream_text_to_speech_edge

app = FastAPI(title="TRIAM Assistant API")

# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


@app.get("/test-voice-stream")
async def test_voice_stream(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech(text), media_type="audio/mpeg")


@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech_edge(text), media_type="audio/mpeg")


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

from openai import AsyncOpenAI
from pinecone import Pinecone

from app.core.supabase import supabase

# Khởi tạo OpenAI
aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Khởi tạo Pinecone (Client v3+)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = "triam-knowledge-base"  # Tên Index bạn đã tạo trên Web Console
index = pc.Index(INDEX_NAME)


async def embed_chunk_to_supbabase(book_id: str, chapter_index: int, chunks: list[str]):
    try:
        response = await aclient.embeddings.create(
            input=chunks,
            model="text-embedding-3-small"
        )

        data_to_insert = []
        for i, embedding_data in enumerate(response.data):
            data_to_insert.append({
                "book_id": book_id,
                "chapter_index": chapter_index,
                "chunk_index": i,
                "content": chunks[i],
                "embedding": embedding_data.embedding
            })

        # Insert vào Supabase
        if data_to_insert:
            supabase.table("book_knowledge").insert(data_to_insert).execute()
            print(f"✅ Saved {len(data_to_insert)} vectors into Supabase.")
            return True

    except Exception as e:
        print(f"Error Embed Supabase: {e}")
        return False



# ====== OLD CODE ======
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
import json

from openai import AsyncOpenAI

from app.core.config import settings

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Prompt được nâng cấp để trả về JSON và xử lý logic chia đoạn thông minh
SYSTEM_PROMPT_REWRITE = """
Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Nội dung tóm tắt để ôn tập..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""

async def normalize_text_for_speech(raw_text: str) -> dict:
    """
    Gửi text thô cho Gemini/GPT để biên tập và cấu trúc lại dữ liệu.
    Trả về Dictionary: {"main_scripts": [], "review_script": ""}
    """
    # Fallback structure nếu AI lỗi
    fallback_result = {
        "main_scripts": [raw_text],
        "review_script": "Không thể tạo tóm tắt cho đoạn này."
    }

    try:
        response = await client.chat.completions.create(
            # model="gpt-4o-mini",
            model="gemini-2.5-flash-lite", # Model này input token lớn, rẻ
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_REWRITE},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3, # Giảm sáng tạo để format JSON chuẩn
            response_format={"type": "json_object"}

        )

        content = response.choices[0].message.content.strip()

        # Xử lý trường hợp AI trả về markdown ```json ... ```
      #   if content.startswith("```json"):
      #       content = content.replace("```json", "").replace("```", "")
      #   elif content.startswith("```"):
      #       content = content.replace("```", "")

        # Parse JSON
        parsed_data = json.loads(content)

        # Validate sơ bộ
      #   if "main_scripts" not in parsed_data or not isinstance(parsed_data["main_scripts"], list):
      #       print("Cảnh báo: Output thiếu main_scripts hoặc sai định dạng.")
      #       return fallback_result

        return parsed_data

    except json.JSONDecodeError:
        print(f"Lỗi Parse JSON từ LLM. Raw content: {content[:100]}...")
        # Trường hợp này có thể fallback bằng cách trả về raw text vào main_scripts
        return {
            "main_scripts": [content], # Cố gắng lấy nội dung dù không đúng format
            "review_script": "Lỗi định dạng tóm tắt."
        }
    except Exception as e:
        print(f"Lỗi LLM Service: {e}")
        return fallback_result

# /////////////// code V1 ///////////////

# from openai import AsyncOpenAI
# from app.core.config import settings

# # client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
# client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# # Prompt "thần thánh" để định hình phong cách đọc
# SYSTEM_PROMPT_REWRITE = """
# Bạn là một biên tập viên phát thanh chuyên nghiệp (Script Editor).
# Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (Spoken Script) để AI TTS đọc tự nhiên nhất.

# QUY TẮC BẮT BUỘC:
# 1. Mở rộng từ viết tắt: Dựa vào ngữ cảnh, hãy viết đầy đủ các từ viết tắt.
#    - Ví dụ: "CNTT" -> "Công nghệ thông tin", "DN" -> "Doanh nghiệp", "NS" -> "Nhân sự".
# 2. Xử lý Tiếng Anh/Thuật ngữ:
#    - Các từ tiếng Anh phổ biến (AI, CEO, Marketing) -> Giữ nguyên (nếu bộ đọc tốt) hoặc chú thích phiên âm nếu cần.
#    - Ví dụ đặc biệt: "AI" -> "Ây Ai", "Agile" -> "A-chao".
# 3. Số liệu & Ký hiệu:
#    - "5%" -> "Năm phần trăm".
#    - "Tp.HCM" -> "Thành phố Hồ Chí Minh".
# 4. Xử lý lỗi PDF & Format (Quan trọng nhất):
#    - Nối các dòng bị ngắt quãng giữa chừng do lỗi PDF (line break).
#    - Loại bỏ số trang (ví dụ số "10", "11" nằm trơ trọi cuối đoạn).
#    - Xóa các ký tự rác do lỗi font (ví dụ: "J", "", các dấu gạch ngang vô nghĩa).
#    - Tự động sửa lỗi chính tả hiển nhiên (ví dụ: "Qcmenia" -> "Armenia").
# 5. Tự nhiên hóa số liệu & Thời gian (Văn nói người Việt):
#    - "1,5 giờ" -> Chuyển thành "một tiếng rưỡi" (KHÔNG dùng "một phẩy năm giờ").
#    - "0.5" -> "nửa" hoặc "không phẩy năm" tùy ngữ cảnh.
#    - "30km" -> "ba mươi ki-lô-mét".
#    - "1990" -> "năm một ngàn chín trăm chín mươi".
#    - Danh sách "1. 2. 3." -> Chuyển thành "Điều thứ nhất: ... Điều thứ hai: ... Điều thứ ba: ..." (để tạo nhịp điệu).

# 6. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

# Input: Văn bản gốc từ sách.
# Output: Chỉ trả về văn bản đã biên tập, không thêm lời chào hay giải thích gì khác.
# """

# async def normalize_text_for_speech(raw_text: str) -> str:
#     """
#     Gửi text thô cho GPT-4o-mini biên tập lại trước khi đọc.
#     Dùng model 'gpt-4o-mini' cho rẻ và nhanh (Latency thấp).
#     """
#     try:
#         response = await client.chat.completions.create(
#             # model="gpt-4o-mini",
#             model="gemini-2.5-flash-lite",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT_REWRITE},
#                 {"role": "user", "content": raw_text}
#             ],
#             temperature=0.3,  # Giữ cho AI tập trung, ít sáng tạo lung tung
#             # max_tokens=2000   # Giới hạn output
#         )
#         normalized_text = response.choices[0].message.content
#         return normalized_text
#     except Exception as e:
#         print(f"Lỗi Normalization: {e}")
#         return raw_text  # Fallback: Nếu lỗi thì trả về text gốc đọc tạm

```

### app\services\pdf_service.py

```py
import re

import pdfplumber
from pypdf import PdfReader


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
                        # pypdf get đúng page number
                        outline_data.append({
                            "title": item.title,
                            "page_start": page_number
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

### app\services\rag_service.py

```py
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.supabase import supabase

ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def search_book_knowledge(query: str, book_id: str):
    # 1. Tạo embedding cho câu hỏi của user
    res = await ai_client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_vector = res.data[0].embedding

    # 2. Gọi hàm RPC match_book_knowledge đã tạo ở Supabase
    result = supabase.rpc("match_book_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.2,
        "match_count": 3,
        "filter_book_id": book_id
    }).execute()

    if not result.data:
        return "Không tìm thấy thông tin cụ thể trong sách."

    return "\n".join([item['content'] for item in result.data])

```

### app\services\tts_service.py

```py

import edge_tts
from openai import AsyncOpenAI

from app.core.config import settings

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

### .dockerignore

```gitignore
.git
.gitignore
.venv
.env
__pycache__
*.pyc
.DS_Store

# Bỏ qua các thư mục chứa dữ liệu tĩnh/log không cần thiết khi deploy
uploads/
_log_extracted_json/
script_ouputs/
_codebase/
_docs_implemented/
implement_docs/
scripts/
```

### .python-version

*(Unsupported file type)*

### Dockerfile

```dockerfile
# Sử dụng Python 3.10 slim
FROM python:3.12-slim

# Copy uv từ image chính thức của Astral (cách cài uv tốt nhất trong Docker)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Tạo user không phải root (Bắt buộc trên Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Thiết lập thư mục làm việc
WORKDIR $HOME/app

# Copy các file quản lý thư viện của uv vào trước để cache
COPY --chown=user pyproject.toml uv.lock ./

# Cài đặt dependencies (sử dụng uv sync)
RUN uv sync --frozen --no-dev

# Copy toàn bộ mã nguồn dự án vào container
COPY --chown=user . .

# Chạy ứng dụng FastAPI bằng uvicorn thông qua uv, đổi port sang 7860
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### pyproject.toml

*(Unsupported file type)*
