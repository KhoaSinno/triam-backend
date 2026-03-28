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
