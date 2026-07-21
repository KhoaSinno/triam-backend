import json
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine

from app.core.constant import SummaryStatus
from app.core.exceptions import LLMResponseFormatError
from app.models.db_models import Book, BookSection, BookSectionKnowledge
from app.services.book_summary_service import BookSummarySchema, generate_ai_book_summary
from app.tasks.book_tasks import generate_book_summary_task


@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine("sqlite:///:memory:")
    target_tables = [Book.__table__, BookSection.__table__, BookSectionKnowledge.__table__]
    SQLModel.metadata.create_all(engine, tables=target_tables)
    with Session(engine) as session:
        yield session


def test_book_summary_schema_validation():
    """Kiểm tra Pydantic Schema khớp 1-1 với FE UI."""
    valid_payload = {
        "key_idea": "Ý tưởng chính của cuốn sách",
        "target_audience": "Đối tượng độc giả 16+",
        "estimated_read_minutes": 180,
        "key_takeaways": ["Bài học 1", "Bài học 2"],
        "summary": "Tóm tắt chi tiết cốt truyện",
        "main_characters": ["Nhân vật A", "Nhân vật B"]
    }
    schema = BookSummarySchema.model_validate(valid_payload)
    assert schema.key_idea == "Ý tưởng chính của cuốn sách"
    assert schema.estimated_read_minutes == 180
    assert len(schema.key_takeaways) == 2

    invalid_payload = valid_payload.copy()
    invalid_payload.pop("key_idea")
    with pytest.raises(ValidationError):
        BookSummarySchema.model_validate(invalid_payload)


@pytest.mark.asyncio
async def test_generate_ai_book_summary_service_success(db_session: Session):
    """Kiểm tra service gọi Gemini, parse JSON, validate Pydantic và cập nhật DB thành công."""
    user_id = uuid.uuid4()
    book = Book(
        title="Test Book",
        user_id=user_id,
        status="ready"
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    section = BookSection(
        book_id=book.id,
        section_index=0,
        title="Chương 1",
        level=1,
        path="1",
        text_content="Nội dung chương 1 ngắn gọn."
    )
    db_session.add(section)
    db_session.commit()

    llm_output_json = json.dumps({
        "key_idea": "Ý tưởng chính test",
        "target_audience": "Người đọc test",
        "estimated_read_minutes": 120,
        "key_takeaways": ["Bài học test 1"],
        "summary": "Tóm tắt test",
        "main_characters": ["Nhân vật 1"]
    })

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=llm_output_json))]

    with patch("app.services.book_summary_service.AsyncOpenAI") as mock_openai_cls:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_cls.return_value = mock_client

        result = await generate_ai_book_summary(db_session, book.id)

        assert result["key_idea"] == "Ý tưởng chính test"
        assert book.ai_summary_status == SummaryStatus.COMPLETED.value
        assert book.ai_summary["estimated_read_minutes"] == 120
        assert book.ai_summary_error is None


@pytest.mark.asyncio
async def test_generate_ai_book_summary_llm_format_error(db_session: Session):
    """Kiểm tra khi Gemini trả về không phải JSON hợp lệ, ném LLMResponseFormatError."""
    user_id = uuid.uuid4()
    book = Book(title="Bad Output Book", user_id=user_id, status="ready")
    db_session.add(book)
    db_session.commit()

    section = BookSection(
        book_id=book.id,
        section_index=0,
        title="Chương 1",
        level=1,
        path="1",
        text_content="Nội dung chương 1"
    )
    db_session.add(section)
    db_session.commit()

    # Trả về chuỗi không phải JSON
    bad_llm_json = "This is not valid JSON string at all!"
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=bad_llm_json))]

    with patch("app.services.book_summary_service.AsyncOpenAI") as mock_openai_cls:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_cls.return_value = mock_client

        with pytest.raises(LLMResponseFormatError):
            await generate_ai_book_summary(db_session, book.id)


def test_generate_book_summary_task_failure_and_retry_exhaustion():
    """Kiểm tra Celery task cập nhật FAILED khi retry 2 lần hết lượt."""
    book_id = uuid.uuid4()

    mock_task = MagicMock()
    mock_task.request.retries = 2
    mock_task.max_retries = 2

    with patch("app.tasks.book_tasks.Session") as mock_session_cls, \
         patch("app.tasks.book_tasks.generate_ai_book_summary", side_effect=Exception("API Timeout Connection Error")):

        mock_session = MagicMock()
        mock_book = Book(id=book_id, title="Failed Book", user_id=uuid.uuid4(), ai_summary_status="pending")
        mock_session.get.return_value = mock_book
        mock_session_cls.return_value.__enter__.return_value = mock_session

        func = generate_book_summary_task.__wrapped__
        if hasattr(func, "__func__"):
            func = func.__func__
        func(mock_task, str(book_id))

        assert mock_book.ai_summary_status == SummaryStatus.FAILED.value
        assert "API Timeout Connection Error" in mock_book.ai_summary_error
