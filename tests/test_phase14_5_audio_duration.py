import uuid
import pytest
from sqlmodel import Session

from app.core.constant import ProcessingJobStatus, PlanMode, BookStatus
from app.db.database import engine
from app.models.db_models import Book, LearningUnit
from app.services.audiobook_service import _unit_to_dict
from app.services.workers.learning_unit_worker import process_learning_unit
from app.services.workers.learning_unit_tts_worker import LearningUnitTTSResult


def test_unit_to_dict_returns_db_estimated_audio_seconds():
    unit = LearningUnit(
        id=uuid.uuid4(),
        title="Test Unit Raw",
        status=ProcessingJobStatus.PROCESSING,
        unit_index=0,
        unit_type="full_group",
        source_text_char_count=5000,
        estimated_audio_seconds=420,
    )
    
    result = _unit_to_dict(unit, segments=[])
    assert result["estimated_audio_seconds"] == 420
    assert result["status"] == ProcessingJobStatus.PROCESSING
    assert len(result["segments"]) == 0


@pytest.mark.asyncio
async def test_process_learning_unit_updates_estimated_audio_seconds_in_db(monkeypatch):
    user_id = uuid.uuid4()
    book_id: uuid.UUID | None = None
    unit_id: uuid.UUID | None = None
    
    async def fake_tts(*args, **kwargs):
        return LearningUnitTTSResult(
            main_segment_count=2,
            review_audio_created=False,
            review_text="Test review",
            generated_audio_seconds=123,
        )
        
    monkeypatch.setattr("app.services.workers.learning_unit_worker.run_learning_unit_tts_pipeline", fake_tts)
    
    try:
        with Session(engine) as session:
            book = Book(
                user_id=user_id,
                title="Phase 14.5 Integration Book",
                status=BookStatus.PROCESSING.value,
            )
            session.add(book)
            session.flush()
            book_id = book.id
            
            unit = LearningUnit(
                user_id=user_id,
                book_id=book.id,
                mode=PlanMode.FULL,
                unit_index=0,
                title="Integration Unit",
                unit_type="full",
                status=ProcessingJobStatus.QUEUED,
                source_text_char_count=1000,
                estimated_tokens=250,
                estimated_audio_seconds=420, # initial source estimate
            )
            session.add(unit)
            session.commit()
            session.refresh(unit)
            unit_id = unit.id
            
        await process_learning_unit(
            user_id,
            book_id,
            "Phase 14.5 Integration Book",
            unit,
            "raw text content",
            None,
            raw_text_char_count=1000,
            estimated_tokens=250,
            estimated_audio_seconds=420,
        )
        
        with Session(engine) as session:
            db_unit = session.get(LearningUnit, unit_id)
            assert db_unit is not None
            assert db_unit.status == ProcessingJobStatus.READY
            # Verify the database column is updated to 123 (actual generated seconds)!
            assert db_unit.estimated_audio_seconds == 123
            
    finally:
        with Session(engine) as session:
            if book_id:
                book = session.get(Book, book_id)
                if book:
                    session.delete(book)
                    session.commit()
