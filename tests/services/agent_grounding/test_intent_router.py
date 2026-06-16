from app.services.agent_grounding.contracts import GroundingIntent
from app.services.agent_grounding.intent_router import (
    detect_external_current_info,
    detect_metadata_intent,
    detect_section_intent,
)
from app.services.agent_grounding.query_normalizer import normalize_query
from app.services.agent_grounding.section_reference_parser import parse_section_reference


def test_detects_bilingual_metadata_intents():
    assert detect_metadata_intent(normalize_query("Tác giả của sách là ai?")) == GroundingIntent.BOOK_METADATA_AUTHOR
    assert detect_metadata_intent(normalize_query("Who wrote this book?")) == GroundingIntent.BOOK_METADATA_AUTHOR
    assert detect_metadata_intent(normalize_query("Tên của quyển sách này là gì?")) == GroundingIntent.BOOK_METADATA_TITLE
    assert detect_metadata_intent(normalize_query("Sách có bao nhiêu phần chính?")) == GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT
    assert detect_metadata_intent(normalize_query("Sách có bao nhiêu đề mục?")) == GroundingIntent.BOOK_METADATA_SECTION_COUNT


def test_does_not_misroute_author_content_question_as_metadata():
    query = normalize_query("Tác giả giải thích khái niệm này như thế nào?")

    assert detect_metadata_intent(query) is None


def test_detects_section_summary_and_missing_reference():
    clear = normalize_query("Tóm tắt chương 4.")
    main_idea = normalize_query("Ý chương bốn là gì?")
    missing = normalize_query("Tóm tắt chương.")

    assert detect_section_intent(clear, parse_section_reference(clear)) == GroundingIntent.BOOK_SECTION_SUMMARY
    assert detect_section_intent(main_idea, parse_section_reference(main_idea)) == GroundingIntent.BOOK_SECTION_SUMMARY
    assert detect_section_intent(missing, parse_section_reference(missing)) is None


def test_external_current_info_detection_is_conservative():
    assert detect_external_current_info(normalize_query("Giá Bitcoin hôm nay là bao nhiêu?")) is True
    assert detect_external_current_info(normalize_query("Hôm nay tôi nên học chương nào?")) is False
