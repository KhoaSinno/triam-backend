import pytest
from app.services.agent_grounding.contracts import GroundingIntent
from app.services.agent_grounding.intent_router import classify_intent
from app.services.agent_grounding.query_normalizer import normalize_query

@pytest.mark.asyncio
async def test_detects_bilingual_metadata_intents():
    assert await classify_intent(normalize_query("Tác giả của sách là ai?")) == GroundingIntent.BOOK_METADATA_AUTHOR
    assert await classify_intent(normalize_query("Who wrote this book?")) == GroundingIntent.BOOK_METADATA_AUTHOR
    assert await classify_intent(normalize_query("Tên của quyển sách này là gì?")) == GroundingIntent.BOOK_METADATA_TITLE
    assert await classify_intent(normalize_query("Sách có bao nhiêu phần chính?")) == GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT
    assert await classify_intent(normalize_query("Sách có bao nhiêu đề mục?")) == GroundingIntent.BOOK_METADATA_SECTION_COUNT

@pytest.mark.asyncio
async def test_does_not_misroute_author_content_question_as_metadata():
    query = normalize_query("Tác giả giải thích khái niệm này như thế nào?")
    assert await classify_intent(query) == GroundingIntent.BOOK_SEMANTIC_QUESTION

@pytest.mark.asyncio
async def test_detects_section_summary_and_missing_reference():
    clear = normalize_query("Tóm tắt chương 4.")
    main_idea = normalize_query("Ý chương bốn là gì?")
    
    assert await classify_intent(clear) == GroundingIntent.BOOK_SECTION_SUMMARY
    assert await classify_intent(main_idea) == GroundingIntent.BOOK_SECTION_SUMMARY
