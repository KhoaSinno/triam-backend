import asyncio
import logging
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from sqlmodel import Session

from app.core.supabase import supabase
from app.crud.audiobook import (
    bulk_create_segments,
    create_book,
    create_chapter,
    delete_chapter,
    update_book_status,
    update_chapter_review_audio,
    update_chapter_status,
)
from app.db import engine
from app.models.db_models import Book, Chapter, ChapterSegment
from app.services.embed import embed_chunk_to_supbabase
from app.services.llm_service import normalize_text_for_speech
from app.services.pdf_service import extract_chapters_smart
from app.services.tts_service import generate_audio_file_edge

logger = logging.getLogger("upload")

router = APIRouter()
sem = asyncio.Semaphore(3)


async def upload_to_supabase(local_path: str, storage_path: str, max_retries: int = 3) -> str:
    """Upload file lên Supabase Storage và trả về public URL."""
    file_size = os.path.getsize(local_path)
    max_size = 20 * 1024 * 1024  # 20 MB
    if file_size > max_size:
        raise HTTPException(status_code=400, detail=f"File size exceeds maximum limit of {max_size} bytes")

    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_("audios").upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": "audio/mpeg"},
            )
            return supabase.storage.from_("audios").get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Upload failed, retrying... ({attempt + 1}/{max_retries})")
                await asyncio.sleep(2**attempt)  # Exponential backoff
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise


async def process_single_chapter(book_id: uuid.UUID, chapter_data: dict, index: int) -> None:
    """Xử lý một chương: TTS → upload → lưu DB."""
    async with sem:
        chapter_id: uuid.UUID | None = None
        try:
            # 1. REWRITE TEXT
            obj_chapter = await normalize_text_for_speech(chapter_data["text"])
            main_chunks: list[str] = obj_chapter.get("main_scripts", [])
            review_text: str = obj_chapter.get("sub_scripts", "")

            # 2. INSERT CHAPTER
            with Session(engine) as session:
                chapter = Chapter(
                    book_id=book_id,
                    chapter_index=index,
                    title=chapter_data.get("title", f"Chương {index + 1}"),
                    review_text=review_text,
                )
                created_chapter = create_chapter(session, chapter)
                chapter_id = created_chapter.id

            # 3. TTS + UPLOAD FROM SUPABASE STORAGE
            segments: list[ChapterSegment] = []
            for i, chunk in enumerate(main_chunks):
                local_filename = f"{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(chunk, local_filename)
                logger.info(f"Generated audio: {local_filename}")

                storage_path = f"{book_id}/chap_{index + 1}/part_{i + 1}.mp3"
                public_url = await upload_to_supabase(local_filename, storage_path)
                logger.info(f"Uploaded audio: {public_url}")

                if os.path.exists(local_filename):
                    os.remove(local_filename)

                segments.append(
                    ChapterSegment(
                        chapter_id=chapter_id,
                        segment_index=i,
                        audio_url=public_url,
                        text_content=chunk,
                    )
                )

            # 4. BULK SAVE SEGMENTS
            if segments:
                with Session(engine) as session:
                    bulk_create_segments(session, segments)

            # 5. REVIEW AUDIO
            if review_text:
                local_filename = f"{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(review_text, local_filename)
                storage_path = f"{book_id}/chap_{index + 1}/review.mp3"
                public_url = await upload_to_supabase(local_filename, storage_path)

                if os.path.exists(local_filename):
                    os.remove(local_filename)

                with Session(engine) as session:
                    update_chapter_review_audio(session, chapter_id, public_url)

            # 6. EMBEDDING
            await embed_chunk_to_supbabase(book_id, index, main_chunks)

            # 7. MARK CHAPTER READY
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, "ready")

        except Exception as e:
            # Rollback: xoá chapter nếu đã tạo
            if chapter_id:
                try:
                    with Session(engine) as session:
                        delete_chapter(session, chapter_id)
                except Exception as delete_error:
                    logger.error(f"Failed to rollback chapter {index + 1}: {delete_error}")
            logger.error(f"Error processing chapter {index + 1}: {e}")
            raise


@router.post("/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    # 1. Extract chapters from PDF
    book_id = uuid.uuid4()
    chapters = await extract_chapters_smart(file.file)

    # 2. Lưu skeleton Book vào DB với status="processing"
    try:
        book = Book(
            id=book_id,
            title=file.filename.replace(".pdf", ""),
            total_chapters=len(chapters),
            status="processing",
        )
        with Session(engine) as session:
            create_book(session, book)
        logger.info(f"Created book record: {book_id} with {len(chapters)} chapters")
    except Exception as e:
        logger.error(f"Failed to create book record: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create book record: {str(e)}")

    # 3. Đẩy việc nặng vào Background → trả phản hồi ngay
    background_tasks.add_task(run_background_processing, book_id, chapters)

    return {
        "message": "Upload thành công! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(book_id),
        "total_chapters": len(chapters),
    }


async def run_background_processing(book_id: uuid.UUID, chapters: list) -> None:
    """Chạy song song tất cả chapters, bị kìm hãm bởi Semaphore."""
    try:
        tasks = [process_single_chapter(book_id, chapter, i) for i, chapter in enumerate(chapters)]
        await asyncio.gather(*tasks)

        with Session(engine) as session:
            update_book_status(session, book_id, "completed")

        logger.info(f"✅ HOÀN TẤT XỬ LÝ SÁCH {book_id}")
    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, "error", error_message=str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")
