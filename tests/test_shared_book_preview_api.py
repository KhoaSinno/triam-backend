import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import BookStatus, DocumentType, PlanMode, ProcessingJobStatus
from app.db.database import engine
from app.main import app
from app.models.db_models import Book, BookSection, LearningUnit, LearningUnitSegment


def test_shared_book_preview_returns_outline_and_one_audio_sample():
    owner_id = uuid.uuid4()
    with Session(engine) as session:
        book = Book(
            user_id=owner_id,
            title="Sách mẫu có preview",
            author="TRIAM",
            status=BookStatus.READY,
            document_type=DocumentType.PDF,
            is_shared=True,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        book_id = book.id

        chapter = BookSection(
            book_id=book_id,
            section_index=0,
            title="Chương 1",
            level=1,
            path="1",
            page_start=1,
            page_end=12,
        )
        section = BookSection(
            book_id=book_id,
            parent_id=chapter.id,
            section_index=1,
            title="Khái niệm nền tảng",
            level=2,
            path="1.1",
            page_start=2,
            page_end=6,
        )
        session.add(chapter)
        session.flush()
        section.parent_id = chapter.id
        session.add(section)

        full_unit = LearningUnit(
            user_id=owner_id,
            book_id=book.id,
            mode=PlanMode.FULL,
            unit_index=0,
            title="Toàn cảnh chương 1",
            unit_type="full_chapter",
            status=ProcessingJobStatus.READY,
            estimated_audio_seconds=240,
        )
        pareto_unit = LearningUnit(
            user_id=owner_id,
            book_id=book.id,
            mode=PlanMode.PARETO,
            unit_index=0,
            title="Ý chính chương 1",
            unit_type="pareto",
            status=ProcessingJobStatus.READY,
            planner_reason="Các ý trọng tâm",
        )
        session.add(full_unit)
        session.add(pareto_unit)
        session.flush()
        session.add(
            LearningUnitSegment(
                learning_unit_id=full_unit.id,
                segment_index=0,
                audio_url="https://audio.test/full-sample.mp3",
                text_content="Đây là đoạn nghe thử.",
                duration_ms=12000,
            )
        )
        session.commit()

    try:
        response = TestClient(app).get(f"/api/v1/books/library/{book_id}/preview?mode=full")

        assert response.status_code == 200
        body = response.json()
        assert body["book"]["id"] == str(book_id)
        assert body["book"]["is_shared"] is True
        assert body["available_modes"] == ["full", "pareto"]
        assert body["total_sections"] == 2
        assert body["outline_tree"][0]["title"] == "Chương 1"
        assert body["outline_tree"][0]["children"][0]["title"] == "Khái niệm nền tảng"
        assert body["total_units"] == 1
        assert body["learning_outline"][0]["has_audio_sample"] is True
        assert body["audio_sample"]["title"] == "Toàn cảnh chương 1"
        assert body["audio_sample"]["segments"] == [
            {
                "id": body["audio_sample"]["segments"][0]["id"],
                "segment_index": 0,
                "audio_url": "https://audio.test/full-sample.mp3",
                "text_content": "Đây là đoạn nghe thử.",
                "duration_ms": 12000,
            }
        ]

        pareto_response = TestClient(app).get(f"/api/v1/books/library/{book_id}/preview?mode=pareto")
        assert pareto_response.status_code == 200
        assert pareto_response.json()["audio_sample"] is None
        assert pareto_response.json()["learning_outline"][0]["title"] == "Ý chính chương 1"
    finally:
        with Session(engine) as session:
            persisted = session.get(Book, book_id)
            if persisted:
                session.delete(persisted)
                session.commit()


def test_shared_book_preview_hides_non_shared_books():
    with Session(engine) as session:
        book = Book(
            user_id=uuid.uuid4(),
            title="Không công khai",
            status=BookStatus.READY,
            document_type=DocumentType.PDF,
            is_shared=False,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        book_id = book.id

    try:
        response = TestClient(app).get(f"/api/v1/books/library/{book_id}/preview")
        assert response.status_code == 404
    finally:
        with Session(engine) as session:
            persisted = session.get(Book, book_id)
            if persisted:
                session.delete(persisted)
                session.commit()
