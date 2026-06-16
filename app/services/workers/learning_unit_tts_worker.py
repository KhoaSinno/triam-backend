import os
import uuid
from dataclasses import dataclass

from sqlmodel import Session

from app.core.exceptions import NoPlayableAudioError
from app.core.logger import log as logger
from app.db.database import engine
from app.models.db_models import LearningUnitSegment
from app.repositories.learning_unit_repo import bulk_create_unit_segments, delete_unit_segments, update_learning_unit_review
from app.services.llm_service import normalize_text_for_speech
from app.services.storage_service import upload_file_to_supabase
from app.services.tts_service import generate_audio_and_get_duration


@dataclass(frozen=True)
class LearningUnitTTSResult:
    main_segment_count: int
    review_audio_created: bool
    review_text: str
    generated_audio_seconds: int = 0


async def _generate_unit_main_segments(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    unit_index: int,
    mode: str,
    main_scripts: list[str],
) -> list[LearningUnitSegment]:
    segments: list[LearningUnitSegment] = []
    total_scripts = len(main_scripts)
    logger.info(f"TTS main segments start | unit={unit_index + 1} | mode={mode} | total_scripts={total_scripts}")
    for i, script in enumerate(main_scripts):
        local_file = f"uploads/{uuid.uuid4()}.mp3"
        os.makedirs("uploads", exist_ok=True)
        try:
            logger.info(
                f"TTS segment start | unit={unit_index + 1} | mode={mode} | "
                f"segment={i + 1}/{total_scripts} | chars={len(script)}"
            )
            duration_ms = await generate_audio_and_get_duration(script, local_file)
            storage_path = f"{book_id}/unit_{unit_index + 1}/{mode}/part_{i + 1}.mp3"
            audio_url = await upload_file_to_supabase(local_file, storage_path, "audios", "audio/mpeg")
            segments.append(
                LearningUnitSegment(
                    learning_unit_id=learning_unit_id,
                    segment_index=i,
                    audio_url=audio_url,
                    duration_ms=duration_ms,
                    text_content=script,
                )
            )
            logger.info(
                f"TTS segment done | unit={unit_index + 1} | mode={mode} | "
                f"segment={i + 1}/{total_scripts} | duration_ms={duration_ms}"
            )
        except Exception as seg_err:
            logger.warning(f"Segment {i + 1} unit {unit_index + 1} TTS failed ({len(script)} chars): {seg_err}")
        finally:
            if os.path.exists(local_file):
                os.remove(local_file)
    logger.info(
        f"TTS main segments done | unit={unit_index + 1} | mode={mode} | "
        f"created_segments={len(segments)}/{total_scripts}"
    )
    return segments


async def _generate_unit_review_audio(
    book_id: uuid.UUID,
    unit_index: int,
    mode: str,
    review_text: str,
) -> str | None:
    if not review_text.strip():
        return None

    local_review = f"uploads/{uuid.uuid4()}.mp3"
    os.makedirs("uploads", exist_ok=True)
    try:
        logger.info(f"TTS review start | unit={unit_index + 1} | mode={mode} | chars={len(review_text)}")
        await generate_audio_and_get_duration(review_text, local_review)
        storage_path = f"{book_id}/unit_{unit_index + 1}/{mode}/review.mp3"
        review_url = await upload_file_to_supabase(local_review, storage_path, "audios", "audio/mpeg")
        logger.info(f"TTS review done | unit={unit_index + 1} | mode={mode}")
        return review_url
    except Exception as rev_err:
        logger.warning(f"Review audio unit {unit_index + 1} failed, skipped: {rev_err}")
        return None
    finally:
        if os.path.exists(local_review):
            os.remove(local_review)


def _store_unit_tts_result(
    learning_unit_id: uuid.UUID,
    mode: str,
    review_text: str,
    review_url: str | None,
    segments: list[LearningUnitSegment],
) -> None:
    logger.info(
        f"TTS DB store start | learning_unit_id={learning_unit_id} | mode={mode} | "
        f"segments={len(segments)} | review_audio={bool(review_url)}"
    )
    with Session(engine) as session:
        delete_unit_segments(session, learning_unit_id)
        bulk_create_unit_segments(session, segments)
        update_learning_unit_review(session, learning_unit_id, review_text=review_text, review_audio_url=review_url)
    logger.info(f"TTS DB store done | learning_unit_id={learning_unit_id} | mode={mode}")


async def run_learning_unit_tts_pipeline(
    book_id: uuid.UUID,
    learning_unit_id: uuid.UUID,
    unit_index: int,
    raw_text: str,
    mode: str,
    unit_title: str,
) -> LearningUnitTTSResult:
    logger.info(
        f"TTS pipeline start | unit={unit_index + 1} | mode={mode} | "
        f"title={unit_title} | raw_chars={len(raw_text)}"
    )
    obj_unit = await normalize_text_for_speech(raw_text, mode, unit_title=unit_title)
    main_scripts: list[str] = obj_unit.get("main_scripts", [])
    review_text: str = obj_unit.get("review_script", "")
    logger.info(
        f"TTS pipeline normalized | unit={unit_index + 1} | mode={mode} | "
        f"main_scripts={len(main_scripts)} | review_chars={len(review_text)}"
    )
    if not main_scripts:
        raise NoPlayableAudioError("LLM không tạo main_scripts để phát audio.")

    segments = await _generate_unit_main_segments(book_id, learning_unit_id, unit_index, mode, main_scripts)
    review_url = await _generate_unit_review_audio(book_id, unit_index, mode, review_text)

    if not segments:
        raise NoPlayableAudioError("Không tạo được segment audio nào.")

    _store_unit_tts_result(learning_unit_id, mode, review_text, review_url, segments)

    total_ms = sum(seg.duration_ms or 0 for seg in segments)
    generated_seconds = int(total_ms / 1000)

    return LearningUnitTTSResult(
        main_segment_count=len(segments),
        review_audio_created=bool(review_url),
        review_text=review_text,
        generated_audio_seconds=generated_seconds,
    )
