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
from dataclasses import dataclass

from sqlmodel import Session

from app.core.exceptions import NoPlayableAudioError
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import ChapterSegment
from app.repositories.chapter_repo import update_chapter_review_audio, update_chapter_review_text
from app.repositories.chapter_segment_repo import bulk_create_segments, delete_segments_by_chapter_and_mode
from app.services.llm_service import normalize_text_for_speech
from app.services.storage_service import upload_file_to_supabase
from app.services.tts_service import generate_audio_and_get_duration


@dataclass(frozen=True)
class TTSChapterResult:
    main_segment_count: int
    review_audio_created: bool


async def _generate_main_segments(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    mode: str,
    main_scripts: list[str],
) -> list[ChapterSegment]:
    segments: list[ChapterSegment] = []
    total_scripts = len(main_scripts)
    logger.info(f"TTS main segments start | chapter={chapter_index + 1} | mode={mode} | total_scripts={total_scripts}")
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            logger.info(
                f"TTS segment start | chapter={chapter_index + 1} | mode={mode} | "
                f"segment={i + 1}/{total_scripts} | chars={len(script)}"
            )
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
            logger.info(
                f"TTS segment done | chapter={chapter_index + 1} | mode={mode} | "
                f"segment={i + 1}/{total_scripts} | duration_ms={duration_ms}"
            )
        except Exception as seg_err:
            logger.warning(
                f"⚠️ Segment {i + 1} chương {chapter_index + 1} lỗi TTS "
                f"({len(script)} chars): {seg_err}"
            )
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)
    logger.info(
        f"TTS main segments done | chapter={chapter_index + 1} | mode={mode} | "
        f"created_segments={len(segments)}/{total_scripts}"
    )
    return segments


async def _generate_review_audio(
    book_id: uuid.UUID,
    chapter_index: int,
    mode: str,
    review_text: str,
) -> str | None:
    if not review_text.strip():
        return None

    local_review = f"uploads/{uuid.uuid4()}.mp3"
    os.makedirs("uploads", exist_ok=True)
    try:
        logger.info(f"TTS review start | chapter={chapter_index + 1} | mode={mode} | chars={len(review_text)}")
        await generate_audio_and_get_duration(review_text, local_review)
        storage_path = f"{book_id}/chap_{chapter_index + 1}/{mode}/review.mp3"
        review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
        logger.info(f"TTS review done | chapter={chapter_index + 1} | mode={mode}")
        return review_url
    except Exception as rev_err:
        logger.warning(f"⚠️ Review audio chương {chapter_index + 1} lỗi, bỏ qua: {rev_err}")
        return None
    finally:
        if os.path.exists(local_review):
            os.remove(local_review)


def _store_tts_result(
    chapter_id: uuid.UUID,
    mode: str,
    review_text: str,
    review_url: str | None,
    segments: list[ChapterSegment],
) -> None:
    logger.info(
        f"TTS DB store start | chapter_id={chapter_id} | mode={mode} | "
        f"segments={len(segments)} | review_audio={bool(review_url)}"
    )
    with Session(engine) as session:
        delete_segments_by_chapter_and_mode(session, chapter_id, mode)
        if review_text:
            update_chapter_review_text(session, chapter_id, review_text, mode)
        bulk_create_segments(session, segments)
        if review_url:
            update_chapter_review_audio(session, chapter_id, review_url, mode)
    logger.info(f"TTS DB store done | chapter_id={chapter_id} | mode={mode}")


async def run_tts_pipeline(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    chapter_index: int,
    raw_text: str,
    mode: str,
    chapter_title: str | None = None,
) -> TTSChapterResult:
    """
    Pipeline TTS đầy đủ cho 1 chapter:
      LLM rewrite → TTS segments → upload → review audio → lưu DB (1 session).

    Ghi chú về Session:
        Tất cả DB writes (review_text, segments, review_audio) được gom vào
        **1 Session duy nhất** ở cuối pipeline, tránh mở-đóng nhiều connections.
    """
    # ── Step 1: LLM Rewrite ──────────────────────────────────────────────────
    logger.info(
        f"TTS pipeline start | chapter={chapter_index + 1} | mode={mode} | "
        f"title={chapter_title or '(unknown)'} | raw_chars={len(raw_text)}"
    )
    obj_chapter = await normalize_text_for_speech(raw_text, mode, chapter_title=chapter_title)
    main_scripts: list[str] = obj_chapter.get("main_scripts", [])
    review_text: str = obj_chapter.get("review_script", "")
    logger.info(
        f"TTS pipeline normalized | chapter={chapter_index + 1} | mode={mode} | "
        f"main_scripts={len(main_scripts)} | review_chars={len(review_text)}"
    )
    if not main_scripts:
        raise NoPlayableAudioError("LLM không tạo main_scripts để phát audio.")

    # ── Step 2: TTS + Upload segments ────────────────────────────────────────
    segments = await _generate_main_segments(book_id, chapter_id, chapter_index, mode, main_scripts)

    # ── Step 3: TTS Review audio ─────────────────────────────────────────────
    review_url = await _generate_review_audio(book_id, chapter_index, mode, review_text)

    # ── Step 4: Lưu tất cả vào DB — 1 Session duy nhất ──────────────────────
    if not segments:
        raise NoPlayableAudioError("Không tạo được segment audio nào.")

    _store_tts_result(chapter_id, mode, review_text, review_url, segments)

    return TTSChapterResult(
        main_segment_count=len(segments),
        review_audio_created=bool(review_url),
    )
