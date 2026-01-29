import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.pdf_service import extract_text_from_pdf, extract_chapters_smart
from app.services.llm_service import normalize_text_for_speech
from app.services.tts_service import stream_text_to_speech_edge, generate_audio_file_edge
import os

router = APIRouter()


async def process_single_chapter_pipeline(chapter_data: dict, index: int, filename_prefix: str):
    """
    Hàm worker: Nhận nhiệm vụ xử lý trọn gói 1 chương từ A-Z.
    Flow: Text gốc -> Rewrite -> TTS -> Done.
    """
    try:
        # 1. REWRITE (Gọi Gemini - I/O Bound)
        # Chạy độc lập, không cần chờ chương khác
        rewritten_text = await normalize_text_for_speech(chapter_data["text"])
        
        # Cập nhật lại text vào object (để trả về FE)
        chapter_data["text"] = rewritten_text
        
        # 2. TTS (Gọi EdgeTTS - I/O Bound)
        # Tạo tên file output
        output_path = f"uploads/{filename_prefix}_chapter_{index + 1}.mp3"
        
        # Đảm bảo thư mục tồn tại
        os.makedirs("uploads", exist_ok=True)
        
        await generate_audio_file_edge(rewritten_text, output_path)
        
        return chapter_data
    except Exception as e:
        print(f"Lỗi xử lý chương {index + 1}: {e}")
        # Trả về data lỗi hoặc gốc để không làm crash cả hệ thống
        chapter_data["error"] = str(e)
        return chapter_data

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process PDF file (High Performance Mode)
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    # 1. Extract Chapters (Nặng CPU - vẫn phải chờ)
    chapters = await extract_chapters_smart(file.file)

    # 2. CHUẨN BỊ TASK XỬ LÝ SONG SONG (Concurrent)
    # Thay vì await từng dòng, ta gom việc lại thành danh sách tasks
    tasks = []
    
    # Chỉ lấy tối đa 3 chương đầu để test (tránh lỗi index nếu sách chỉ có 1 chương)
    limit = min(len(chapters), 3) 
    
    for i in range(limit):
        # Tạo task nhưng CHƯA CHẠY NGAY, chỉ mới lên lịch
        task = process_single_chapter_pipeline(
            chapter_data=chapters[i],
            index=i,
            filename_prefix=file.filename
        )
        tasks.append(task)

    # 3. KÍCH HOẠT ĐA LUỒNG ("FIRE" ALL TASKS)
    # asyncio.gather sẽ chạy tất cả các task cùng lúc.
    # Thời gian hoàn thành = Thời gian của task lâu nhất (thay vì tổng thời gian)
    processed_chapters = await asyncio.gather(*tasks)

    # Return kết quả
    return {
        "filename": file.filename, 
        "chapters": processed_chapters, # Đã chứa text rewrite
        "message": f"Đã xử lý xong {len(processed_chapters)} chương."
    }

# @router.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     """
#     Upload and process PDF file
#     """
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

#     # return {"filename": file.filename, "status": "uploaded"}

#     chapters = await extract_chapters_smart(file.file)

#     # Test rewrite chap 1
#     chapters[0]["text"] = await normalize_text_for_speech(chapters[0]["text"])
#     chapters[1]["text"] = await normalize_text_for_speech(chapters[1]["text"])
#     chapters[2]["text"] = await normalize_text_for_speech(chapters[2]["text"])

#     # Test generate audio 1 chapter file
#     await generate_audio_file_edge(chapters[0]["text"], "uploads/" + file.filename + "_chapter_1.mp3")
#     await generate_audio_file_edge(chapters[1]["text"], "uploads/" + file.filename + "_chapter_2.mp3")
#     await generate_audio_file_edge(chapters[2]["text"], "uploads/" + file.filename + "_chapter_3.mp3")

#     # Return 3 first chapter and filename
#     return {"filename": file.filename, "chapters": chapters[:3]}


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
