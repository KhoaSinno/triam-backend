import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.services.pdf_service import extract_text_from_pdf, extract_chapters_smart
from app.services.llm_service import normalize_text_for_speech
from app.services.tts_service import stream_text_to_speech_edge, generate_audio_file_edge
from app.services.embed import embed_text_to_pinecone
import os
import uuid
import json

router = APIRouter()
sem = asyncio.Semaphore(3)

async def process_single_chapter(book_id: str, chapter_data: dict, index: int):
    """
    Worker xử lý toàn diện: Rewrite -> TTS -> Save DB -> Embed Pinecone
    """
    async with sem: ## 3 workers
        try:
            print(f"--- Đang xử lý chương {index+1}... ---")

            # 1. REWRITE (Gemini)
            obj_chapter = await normalize_text_for_speech(chapter_data["text"])

            # Print this json rewritten_text
            print(f"Rewritten text: {obj_chapter}")

            # save rewritten_text to json file
            # with open(f"_log_extracted_json/test_logs/{book_id}_chap_{index + 1}.json", "w", encoding="utf-8") as f:
            #     json.dump(obj_chapter, f, ensure_ascii=False)
            
            # 2. TTS (EdgeTTS)
            # Lưu ý: Đặt tên file theo book_id để quản lý
            main_chunks: list[str] = obj_chapter["main_scripts"]
            # sub_chunks: list[str] = obj_chapter["sub_scripts"]
            for i, chunk in enumerate(main_chunks):
                # audio_filename = f"uploads/{book_id}_chap_{index + 1}_main_{i + 1}.mp3"
                audio_filename = f"_log_extracted_json/test_audio_main/{book_id}_chap_{index + 1}_main_{i + 1}.mp3"
                await generate_audio_file_edge(chunk, audio_filename)
            # for i, chunk in enumerate(sub_chunks):
            #     # audio_filename = f"uploads/{book_id}_chap_{index + 1}_sub_{i + 1}.mp3"
            #     audio_filename = f"_log_extracted_json/test_audio_sub/{book_id}_chap_{index + 1}_sub_{i + 1}.mp3"
            #     await generate_audio_file_edge(chunk, audio_filename)
            
            # 3. RAG PREPARATION (Pinecone) - QUAN TRỌNG
            # Chúng ta embed text đã rewrite để AI trả lời câu hỏi user chính xác hơn
            # await embed_text_to_pinecone(book_id, index, rewritten_text) 

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
