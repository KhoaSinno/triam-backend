from app.services.tts_script_quality_service import (
    find_unexplained_acronyms,
    has_markdown_artifacts,
    sanitize_tts_script_text,
)


def test_sanitize_tts_script_text_removes_visual_markdown_artifacts():
    text = """
    ## Tiêu đề
    - Trục đầu tiên là **kiến trúc mô hình**, xem thêm [1].
    Xem [nguồn](https://example.com) và `thuật ngữ`.
    """

    cleaned = sanitize_tts_script_text(text)

    assert cleaned == "Tiêu đề Trục đầu tiên là kiến trúc mô hình, xem thêm. Xem nguồn và thuật ngữ."
    assert not has_markdown_artifacts(cleaned)


def test_find_unexplained_acronyms_uses_general_first_use_rule():
    warnings = find_unexplained_acronyms(
        ["Bài học nhắc tới ABC và XYZ-Bench như hai tiêu chí đánh giá quan trọng."]
    )

    assert warnings == ("ABC", "XYZ-Bench")


def test_find_unexplained_acronyms_accepts_source_style_explanation():
    warnings = find_unexplained_acronyms(
        ["Phương pháp phân tích tổng hợp, gọi tắt là ABC, được dùng trong nghiên cứu này."]
    )

    assert warnings == ()
