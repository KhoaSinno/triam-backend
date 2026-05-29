import uuid

import pytest
from sqlmodel import Session, select

from app.core.constant import BookStatus, DocumentType, PlanMode, ProcessingJobStatus, ProcessingJobType
from app.core.exceptions import ChapterTooLargeError, LLMResponseFormatError, NoPlayableAudioError
from app.db.database import engine
from app.models.db_models import Book, BookSection, Chapter, LearningUnit, LearningUnitSource, ProcessingJob
from app.services.token_budget_service import estimate_text_budget

MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def test_token_budget_estimates_vietnamese_text():
    budget = estimate_text_budget("Đây là một đoạn văn bản tiếng Việt để kiểm tra ước lượng token.")

    assert budget.char_count > 0
    assert budget.estimated_tokens > 0
    assert budget.estimated_audio_seconds >= 0


def test_llm_hard_limit_blocks_provider_call(monkeypatch):
    from app.core.config import settings
    from app.services import llm_service

    async def fail_if_called(*args, **kwargs):
        raise AssertionError("LLM should not be called when hard limit is exceeded")

    monkeypatch.setattr(settings, "LLM_INPUT_HARD_TOKEN_LIMIT", 1)
    monkeypatch.setattr(llm_service, "_call_normalize_llm", fail_if_called)

    with pytest.raises(ChapterTooLargeError):
        import asyncio

        asyncio.run(llm_service.normalize_text_for_speech("nội dung đủ dài để vượt một token", "full"))


def test_llm_response_validation_rejects_bad_payload():
    from app.services.llm_service import _validate_normalized_payload

    with pytest.raises(LLMResponseFormatError):
        _validate_normalized_payload({"review_script": "missing scripts"})


def test_chunking_splits_long_text(monkeypatch):
    from app.core.config import settings
    from app.services.chapter_chunking_service import split_text_for_llm

    monkeypatch.setattr(settings, "LLM_CHUNK_TARGET_TOKENS", 30)
    monkeypatch.setattr(settings, "LLM_CHUNK_OVERLAP_TOKENS", 5)

    chunks = split_text_for_llm(" ".join(["tri âm học tập"] * 120))

    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
    assert chunks[0].index == 0


@pytest.mark.asyncio
async def test_tts_pipeline_fails_when_llm_returns_no_playable_scripts(monkeypatch):
    async def fake_normalize(*args, **kwargs):
        return {"main_scripts": [], "review_script": "review"}

    monkeypatch.setattr("app.services.workers.tts_worker.normalize_text_for_speech", fake_normalize)

    from app.services.workers.tts_worker import run_tts_pipeline

    with pytest.raises(NoPlayableAudioError):
        await run_tts_pipeline(uuid.uuid4(), uuid.uuid4(), 0, "raw text", "full")


@pytest.mark.asyncio
async def test_chapter_failure_keeps_chapter_and_marks_state(monkeypatch):
    async def fake_rag(*args, **kwargs):
        return None

    async def fake_tts(*args, **kwargs):
        raise NoPlayableAudioError("no audio")

    monkeypatch.setattr("app.services.workers.chapter_worker._run_rag_pipeline", fake_rag)
    monkeypatch.setattr("app.services.workers.chapter_worker.run_tts_pipeline", fake_tts)

    from app.models.db_models import ChapterProcessingState
    from app.services.workers.chapter_worker import process_chapter

    with Session(engine) as session:
        book = Book(
            user_id=MOCK_USER_ID,
            title="Phase 3 Failure Test",
            total_chapters=1,
            status=BookStatus.PROCESSING,
            document_type=DocumentType.PDF,
            file_url="https://example.test/storage/v1/object/public/raw_books/test/original.pdf",
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        chapter = Chapter(book_id=book.id, chapter_index=0, title="Chapter 1", status=BookStatus.PROCESSING)
        session.add(chapter)
        session.commit()
        session.refresh(chapter)
        book_id = book.id
        chapter_id = chapter.id

    with pytest.raises(NoPlayableAudioError):
        await process_chapter(
            MOCK_USER_ID,
            book_id,
            "Phase 3 Failure Test",
            "Chapter 1",
            chapter_id,
            0,
            "raw text",
            PlanMode.FULL.value,
            raw_text_char_count=8,
            estimated_tokens=2,
            estimated_audio_seconds=1,
        )

    with Session(engine) as session:
        chapter = session.get(Chapter, chapter_id)
        state = session.exec(
            select(ChapterProcessingState).where(
                ChapterProcessingState.chapter_id == chapter_id,
                ChapterProcessingState.mode == PlanMode.FULL,
            )
        ).first()
        assert chapter is not None
        assert chapter.status == BookStatus.ERROR
        assert state is not None
        assert state.status == ProcessingJobStatus.ERROR

        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()


@pytest.mark.asyncio
async def test_book_pipeline_sets_partial_ready_after_first_playable(monkeypatch):
    from app.services.workers import book_pipeline

    calls = []

    async def fake_process_learning_unit(user_id, book_id, book_title, unit, raw_text, job_id, *args, **kwargs):
        calls.append(unit.unit_index)
        if unit.unit_index == 1:
            with Session(engine) as session:
                book = session.get(Book, book_id)
                job = session.get(ProcessingJob, job_id)
                assert book.status == BookStatus.PARTIAL_READY
                assert job.status == ProcessingJobStatus.PARTIAL_READY

    monkeypatch.setattr(book_pipeline, "process_learning_unit", fake_process_learning_unit)

    with Session(engine) as session:
        book = Book(
            user_id=MOCK_USER_ID,
            title="Phase 3 Partial Test",
            total_sections=2,
            total_units=2,
            status=BookStatus.PROCESSING,
            document_type=DocumentType.PDF,
            file_url="https://example.test/storage/v1/object/public/raw_books/test/original.pdf",
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        for index in range(2):
            section = BookSection(
                book_id=book.id,
                section_index=index,
                title=f"Section {index + 1}",
                level=1,
                path=str(index + 1),
                text_content=f"source text {index + 1}",
                text_char_count=13,
            )
            session.add(section)
            session.flush()
            unit = LearningUnit(
                user_id=MOCK_USER_ID,
                book_id=book.id,
                mode=PlanMode.FULL,
                unit_index=index,
                title=f"Unit {index + 1}",
                unit_type="full",
                status=ProcessingJobStatus.QUEUED,
                source_text_char_count=13,
                estimated_tokens=3,
                estimated_audio_seconds=1,
            )
            session.add(unit)
            session.flush()
            session.add(LearningUnitSource(learning_unit_id=unit.id, section_id=section.id, source_order=0))
        job = ProcessingJob(
            user_id=MOCK_USER_ID,
            book_id=book.id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.QUEUED,
            mode=PlanMode.FULL,
            total_units=2,
        )
        session.add(job)
        session.commit()
        session.refresh(book)
        session.refresh(job)
        book_id = book.id
        job_id = job.id

    await book_pipeline.run_background_processing(book_id, PlanMode.FULL.value, job_id)

    assert calls == [0, 1]
    with Session(engine) as session:
        book = session.get(Book, book_id)
        job = session.get(ProcessingJob, job_id)
        assert book.status == BookStatus.READY
        assert job.status == ProcessingJobStatus.READY
        assert job.estimated_input_tokens is not None
        assert job.estimated_audio_seconds is not None
        if book:
            session.delete(book)
            session.commit()
