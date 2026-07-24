import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.config import settings
from app.core.constant import BookStatus, DocumentType, PlanMode
from app.core.exceptions import AudioLimitExceededError
from app.models.db_models import Book, BookSection, LearningUnit, ReadingPlanScheduleSlot
from app.schemas.plan import PlanInput
from app.services.document_structure_types import ParsedDocument, ParsedSection
from app.services.learning_unit_planner_service import PlannedLearningUnit
from app.services.token_budget_service import check_book_preflight_limits
from app.services.upload_service import _enqueue_book_summary, handle_generate_plan, handle_upload_document


class FakeSession:
    def __init__(self):
        self.added = []
        self.commits = 0
        self.rollbacks = 0
        self.store = {}

    def add(self, obj):
        self.added.append(obj)
        if hasattr(obj, "id") and getattr(obj, "id", None):
            self.store[obj.id] = obj

    def add_all(self, objs):
        for o in objs:
            self.add(o)

    def commit(self):
        self.commits += 1

    def flush(self):
        pass

    def refresh(self, obj):
        pass

    def rollback(self):
        self.rollbacks += 1

    def get(self, model, key):
        return self.store.get(key)

    def exec(self, query):
        class Results:
            def __init__(self, items):
                self._items = items

            def all(self):
                return self._items

            def first(self):
                return self._items[0] if self._items else None

        q_str = str(query).lower()
        if "slot" in q_str:
            items = [o for o in self.added if isinstance(o, ReadingPlanScheduleSlot)]
        elif "learning" in q_str or "learningunit" in q_str or "learning_unit" in q_str:
            items = [o for o in self.added if isinstance(o, LearningUnit)]
        else:
            items = [o for o in self.added if isinstance(o, Book)]
        return Results(items)


def _create_mock_section_node(order_index: int, word_count: int) -> ParsedSection:
    text = " ".join(["từ"] * word_count)
    return ParsedSection(
        title=f"Chương {order_index}",
        level=1,
        order_index=order_index,
        path=str(order_index),
        text=text,
    )


def test_check_book_preflight_limits_valid():
    sections = [_create_mock_section_node(1, 2600)]
    is_valid, est_seconds, err_msg = check_book_preflight_limits(sections)
    assert is_valid is True
    assert est_seconds > 0
    assert err_msg is None


def test_check_book_preflight_limits_exceeded():
    sections = [_create_mock_section_node(1, 35000)]
    is_valid, est_seconds, err_msg = check_book_preflight_limits(sections)
    assert is_valid is False
    assert est_seconds > settings.MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK
    assert "Tài liệu quá lớn" in err_msg


@pytest.mark.asyncio
async def test_upload_document_preflight_audio_limit_rejection():
    session = FakeSession()
    user_id = uuid.uuid4()
    mock_file = MagicMock()
    mock_file.filename = "large_book.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"mock pdf bytes")

    large_sections = [_create_mock_section_node(i, 10000) for i in range(1, 5)]
    mock_parsed_doc = ParsedDocument(document_type="pdf", sections=large_sections)

    mock_file_handle = AsyncMock()
    mock_file_handle.write = AsyncMock()
    mock_aio = MagicMock()
    mock_aio.__aenter__ = AsyncMock(return_value=mock_file_handle)
    mock_aio.__aexit__ = AsyncMock(return_value=None)

    with patch("app.services.upload_service.aiofiles.open", return_value=mock_aio), \
         patch("app.services.upload_service._extract_structure_by_type", return_value=mock_parsed_doc), \
         patch("app.services.upload_service.upload_file_to_supabase") as mock_supabase_upload:
        with pytest.raises(AudioLimitExceededError) as exc_info:
            await handle_upload_document(session, mock_file, user_id)

        assert "Tài liệu quá lớn" in str(exc_info.value.detail)
        mock_supabase_upload.assert_not_called()
        assert len(session.added) == 0


@pytest.mark.asyncio
async def test_upload_document_lazy_section_indexing():
    session = FakeSession()
    user_id = uuid.uuid4()
    mock_file = MagicMock()
    mock_file.filename = "valid_book.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"mock pdf bytes")

    valid_sections = [_create_mock_section_node(1, 1300)]
    mock_parsed_doc = ParsedDocument(document_type="pdf", sections=valid_sections)

    mock_file_handle = AsyncMock()
    mock_file_handle.write = AsyncMock()
    mock_aio = MagicMock()
    mock_aio.__aenter__ = AsyncMock(return_value=mock_file_handle)
    mock_aio.__aexit__ = AsyncMock(return_value=None)

    with patch("app.services.upload_service.aiofiles.open", return_value=mock_aio), \
         patch("app.services.upload_service._extract_structure_by_type", return_value=mock_parsed_doc), \
         patch("app.services.upload_service.upload_file_to_supabase", return_value="https://storage.mock/raw.pdf"), \
         patch("app.services.upload_service.index_book_sections_task.apply_async") as mock_index_task, \
         patch("app.services.upload_service._enqueue_book_summary") as mock_summary_task:

        res = await handle_upload_document(session, mock_file, user_id)

        assert res["total_sections"] == 1
        book_id = uuid.UUID(res["book_id"])

        book = session.get(Book, book_id)
        assert book is not None
        assert book.status == BookStatus.DRAFT

        mock_index_task.assert_not_called()
        mock_summary_task.assert_called_once_with(book_id)


def test_ai_summary_auto_enqueue_toggle():
    book_id = uuid.uuid4()
    with patch("app.services.upload_service.generate_book_summary_task.delay") as mock_delay:
        with patch.object(settings, "AI_SUMMARY_AUTO_ENQUEUE_ENABLED", False):
            _enqueue_book_summary(book_id)
            mock_delay.assert_not_called()

        with patch.object(settings, "AI_SUMMARY_AUTO_ENQUEUE_ENABLED", True):
            _enqueue_book_summary(book_id)
            mock_delay.assert_called_once_with(str(book_id))


@pytest.mark.asyncio
async def test_handle_generate_plan_triggers_deferred_section_indexing():
    session = FakeSession()
    user_id = uuid.uuid4()
    book_id = uuid.uuid4()

    book = Book(
        id=book_id,
        user_id=user_id,
        title="Test Book for Plan",
        total_sections=1,
        total_units=0,
        status=BookStatus.DRAFT,
        document_type=DocumentType.PDF.value,
    )
    session.add(book)
    section = BookSection(
        id=uuid.uuid4(),
        book_id=book_id,
        title="Chapter 1",
        level=1,
        ordinal=1,
        content="Nội dung bài học thử nghiệm.",
    )
    session.add(section)

    payload = PlanInput(
        book_id=book_id,
        mode=PlanMode.PARETO,
        pace=1,
        schedule_config=["Mon", "Wed", "Fri"],
        reminder_time="20:00",
    )

    mock_unit = PlannedLearningUnit(
        title="Unit 1",
        unit_type="chapter",
        source_section_ids=[section.id],
        source_text="Nội dung bài học thử nghiệm.",
        source_text_char_count=27,
        estimated_tokens=10,
        estimated_audio_seconds=5,
        planner_reason="Initial unit",
    )

    with patch("app.services.upload_service.index_book_sections_task.apply_async") as mock_index_task, \
         patch("app.services.upload_service.process_book_task.apply_async") as mock_process_task, \
         patch("app.services.upload_service.build_plan_session_summary", return_value={}), \
         patch("app.services.upload_service._planned_units_for_book", return_value=[mock_unit]):

        res = await handle_generate_plan(session, payload, user_id)

        assert res["book_id"] == str(book_id)
        assert res["mode"] == "pareto"

        mock_index_task.assert_called_once_with(args=[str(book_id)], queue="document")
        mock_process_task.assert_called_once()
