import asyncio
import logging
import os
import uuid

from sqlmodel import Session, select

from app.core.constant import BookStatus
from app.core.supabase import supabase
from app.crud.audiobook import update_book_status
from app.crud.book_knowledge import delete_knowledge_by_chapter
from app.crud.chapter import (
    Chapter,
    delete_chapter,
    get_draft_chapters_by_book,
    update_chapter_review_audio,
    update_chapter_review_text,
    update_chapter_status,
)
from app.crud.chapter_segment import bulk_create_segments, delete_segments_by_chapter_and_mode
from app.db import engine
from app.helper.upload2supabase import upload_file_to_supabase
from app.models.db_models import Book, ChapterSegment
from app.services.embed import embed_and_save_chapter
from app.services.llm_service import normalize_text_for_speech
from app.services.pdf_service import extract_chapters_smart
from app.services.tts_service import generate_audio_and_get_duration

logger = logging.getLogger("background")

# Chapter concurrency limiter (tối đa 3 chương xử lý song song)
sem = asyncio.Semaphore(5)


# -----------------------------------------------------------------------
# BACKGROUND: 2 luồng song song RAG + TTS cho từng chapter
# -----------------------------------------------------------------------
async def _thread_1_rag(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
) -> None:
    """Luồng 1: Cắt chunks → Embed → Lưu vào book_knowledge."""
    with Session(engine) as session:
        await embed_and_save_chapter(book_id, chapter_id, raw_text, session)


async def _thread_2_tts(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """Luồng 2: LLM rewrite → TTS → Upload Storage → Lưu chapter_segments."""
    # Step 1: LLM Rewrite
    obj_chapter = await normalize_text_for_speech(raw_text, mode)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # Lưu review_text vào chapter
    if review_text:
        with Session(engine) as session:
            update_chapter_review_text(session, chapter_id, review_text, mode)

    # Step 2: TTS + Upload từng segment
    segments: list[ChapterSegment] = []
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/part_{i + 1}.mp3"
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            segments.append(
                ChapterSegment(
                    chapter_id=chapter_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                    mode=mode,
                )
            )
        except Exception as seg_err:
            # Một segment thất bại — log kèm nội dung text để debug
            text_preview = script[:80] if script else "(empty)"
            logger.warning(f"⚠️ Segment {i + 1} chương {chapter_index + 1} lỗi TTS ({len(script)} chars, text='{text_preview}...'): {seg_err}")
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)

    # Step 3: Bulk save segments
    if segments:
        with Session(engine) as session:
            bulk_create_segments(session, segments)

    # Step 4 (optional): Sinh audio review
    if review_text and review_text.strip():
        local_review = f"uploads/{uuid.uuid4()}.mp3"
        try:
            await generate_audio_and_get_duration(review_text, local_review)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/review.mp3"
            review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
            with Session(engine) as session:
                update_chapter_review_audio(session, chapter_id, review_url, mode)
        except Exception as rev_err:
            logger.warning(f"⚠️ Review audio chương {chapter_index + 1} lỗi, bỏ qua: {rev_err}")
        finally:
            if os.path.exists(local_review):
                os.remove(local_review)


async def _process_single_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """Xử lý 1 chương: chạy 2 luồng song song, bị giới hạn bởi Semaphore."""
    async with sem:
        try:
            await asyncio.gather(
                _thread_1_rag(book_id, chapter_id, raw_text),
                _thread_2_tts(book_id, chapter_id, chapter_index, raw_text, mode),
            )
            with Session(engine) as session:
                update_chapter_status(session, chapter_id, BookStatus.READY)
            logger.info(f"✅ Chapter {chapter_index + 1} READY")
        except Exception as e:
            logger.error(f"❌ Error processing chapter {chapter_index + 1}: {e}")
            # [FIX BUG 2] Rollback đúng thứ tự:
            # Phải xóa book_knowledge (có FK trỏ vào chapter) TRƯỚC khi xóa chapter
            try:
                with Session(engine) as session:
                    delete_knowledge_by_chapter(session, chapter_id)
                    delete_chapter(session, chapter_id)
                logger.info(f"🗑️ Rollback chapter {chapter_index + 1} thành công.")
            except Exception as del_err:
                logger.error(f"Failed to rollback chapter {chapter_index + 1}: {del_err}")
            raise


async def run_background_processing(book_id: uuid.UUID, mode: str) -> None:
    """
    Điều phối xử lý tất cả chapters song song.
    1. Fetch draft chapters từ DB.
    2. Download PDF từ Supabase Storage (file_url đã lưu lúc /upload).
    3. Re-extract text per-chapter, ghép với draft chapters theo chapter_index.
    4. Chạy 2 luồng song song: RAG + TTS cho từng chapter.
    """
    import io

    try:
        # 1. Fetch book + draft chapters từ DB
        with Session(engine) as session:
            book = session.get(Book, book_id)
            draft_chapters = get_draft_chapters_by_book(session, book_id)

        if not book:
            logger.error(f"Book {book_id} not found")
            return

        if not draft_chapters:
            with Session(engine) as session:
                update_book_status(session, book_id, BookStatus.ERROR, "Không có chapter nào để xử lý.")
            return

        if not book.file_url:
            with Session(engine) as session:
                update_book_status(session, book_id, BookStatus.ERROR, "file_url chưa được lưu — PDF chưa upload lên Storage.")
            logger.error(f"book.file_url is missing for book {book_id}")
            return

        # 2. Download PDF từ Supabase Storage
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF from Storage: {storage_path}")
        pdf_bytes: bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)

        # 3. Re-extract chapters (giữ text thật theo từng chapter)
        chapters_data = await extract_chapters_smart(pdf_file)

        # Ghép chapters_data với draft_chapters theo chapter_index
        # (draft_chapters đã sort theo chapter_index từ get_draft_chapters_by_book)
        chapters_map: dict[int, str] = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # 4. Tạo tasks song song cho từng chapter
        tasks = []
        for draft_chap in draft_chapters:
            raw_text = chapters_map.get(draft_chap.chapter_index, "")
            if not raw_text.strip():
                logger.warning(f"⚠️ Chapter {draft_chap.chapter_index + 1} '{draft_chap.title}' không có text — bỏ qua.")
                continue
            tasks.append(
                _process_single_chapter(
                    book_id,
                    draft_chap.id,
                    draft_chap.chapter_index,
                    raw_text,
                    mode,
                )
            )

        await asyncio.gather(*tasks)

        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.READY)
        logger.info(f"🎉 Book {book_id} READY — tất cả chapters đã xử lý xong.")

    except Exception as e:
        with Session(engine) as session:
            update_book_status(session, book_id, BookStatus.ERROR, str(e))
        logger.error(f"❌ LỖI XỬ LÝ SÁCH {book_id}: {e}")


async def _process_switch_mode_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    new_mode: str,
) -> None:
    """Xử lý switch mode 1 chương: chỉ chạy TTS, xóa segments cũ của mode này trước khi tạo."""
    async with sem:
        try:
            # 1. Xoá audio cũ của mode chuẩn bị gen (để ko bị trùng)
            with Session(engine) as session:
                delete_segments_by_chapter_and_mode(session, chapter_id, new_mode)

            # 2. Sinh Audio TTS mới
            await _thread_2_tts(book_id, chapter_id, chapter_index, raw_text, new_mode)

            logger.info(f"✅ Chapter {chapter_index + 1} SWITCH MODE {new_mode} READY")
        except Exception as e:
            logger.error(f"❌ Error switching mode chapter {chapter_index + 1}: {e}")
            raise


async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str) -> None:
    """
    Luồng sinh audio riêng khi User switch mode:
    Bỏ qua RAG, lấy lại text từ PDF, gen audio TTS.
    """
    import io

    try:
        with Session(engine) as session:
            book = session.get(Book, book_id)
            chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id)).all()

        if not book or not book.file_url:
            logger.error(f"Cannot switch mode for book {book_id}: Invalid book or file_url")
            return

        # Tải PDF và lấy text gốc
        storage_path = f"{book_id}/original.pdf"
        logger.info(f"⬇️  Downloading PDF for Switch Mode: {storage_path}")
        pdf_bytes = supabase.storage.from_("raw_books").download(storage_path)
        pdf_file = io.BytesIO(pdf_bytes)
        chapters_data = await extract_chapters_smart(pdf_file)
        chapters_map = {i: chap.get("text", "") for i, chap in enumerate(chapters_data)}

        # Chạy task song song cho các chapter
        tasks = []
        for chap in chapters:
            raw_text = chapters_map.get(chap.chapter_index, "")
            if raw_text.strip():
                tasks.append(_process_switch_mode_chapter(book_id, chap.id, chap.chapter_index, raw_text, new_mode))

        await asyncio.gather(*tasks)
        logger.info(f"🎉 Sách {book_id} đã gen xong audio cho mode: {new_mode}.")

    except Exception as e:
        logger.error(f"❌ LỖI SWITCH MODE SÁCH {book_id}: {e}")
