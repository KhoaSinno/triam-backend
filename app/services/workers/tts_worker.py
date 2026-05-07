"""
app/services/workers/tts_worker.py
====================================
Worker xử lý TTS (Text-to-Speech) cho 1 chapter.

Trách nhiệm:
    1. Gọi LLM rewrite text → main_scripts + review_script
    2. TTS từng segment → upload audio lên Storage
    3. Lưu tất cả kết quả vào DB trong **1 session duy nhất**
       (thay vì 3 sessions riêng biệt như trước → giảm connection overhead)
"""

import os
import uuid

from sqlmodel import Session

from app.db.database import engine
from app.models.db_models import ChapterSegment
from app.repositories.chapter_repo import update_chapter_review_audio, update_chapter_review_text
from app.repositories.chapter_segment_repo import bulk_create_segments
from app.services.llm_service import normalize_text_for_speech
from app.services.storage_service import upload_file_to_supabase
from app.services.tts_service import generate_audio_and_get_duration

from app.core.logger import log as logger


async def run_tts_pipeline(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
) -> None:
    """
    Pipeline TTS đầy đủ cho 1 chapter:
      LLM rewrite → TTS segments → upload → review audio → lưu DB (1 session).

    Ghi chú về Session:
        Tất cả DB writes (review_text, segments, review_audio) được gom vào
        **1 Session duy nhất** ở cuối pipeline, tránh mở-đóng nhiều connections.
    """
    # ── Step 1: LLM Rewrite ──────────────────────────────────────────────────
    obj_chapter = await normalize_text_for_speech(raw_text, mode)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")

    # ── Step 2: TTS + Upload segments ────────────────────────────────────────
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
            text_preview = script[:80] if script else "(empty)"
            logger.warning(
                f"⚠️ Segment {i + 1} chương {chapter_index + 1} lỗi TTS "
                f"({len(script)} chars, text='{text_preview}...'): {seg_err}"
            )
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)

    # ── Step 3: TTS Review audio ─────────────────────────────────────────────
    review_url: str | None = None
    if review_text and review_text.strip():
        local_review = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            await generate_audio_and_get_duration(review_text, local_review)
            storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/review.mp3"
            review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
        except Exception as rev_err:
            logger.warning(f"⚠️ Review audio chương {chapter_index + 1} lỗi, bỏ qua: {rev_err}")
        finally:
            if os.path.exists(local_review):
                os.remove(local_review)

    # ── Step 4: Lưu tất cả vào DB — 1 Session duy nhất ──────────────────────
    with Session(engine) as session:
        if review_text:
            update_chapter_review_text(session, chapter_id, review_text, mode)
        if segments:
            bulk_create_segments(session, segments)
        if review_url:
            update_chapter_review_audio(session, chapter_id, review_url, mode)
