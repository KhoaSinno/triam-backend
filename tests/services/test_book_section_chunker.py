import uuid

from app.services.book_section_chunker import (
    build_section_chunks,
    build_section_search_text,
    normalize_section_text,
)


def test_normalize_section_text_removes_empty_lines_and_extra_spaces():
    text = "  Dòng   một. \n\n\tDòng hai   \r\n"

    assert normalize_section_text(text) == "Dòng một.\nDòng hai"


def test_build_section_chunks_adds_stable_section_metadata_and_hashes():
    section_id = uuid.UUID("11111111-1111-1111-1111-111111111111")

    chunks = build_section_chunks(
        book_title="Sách thử nghiệm",
        author="Tác giả A",
        section_id=section_id,
        section_title="Mục 1",
        section_path="Chương 1 > Mục 1",
        text="Đây là nội dung đủ dài để tạo chunk. " * 30,
        chunk_size_chars=160,
        chunk_overlap_chars=20,
        embedding_version="section-v1",
    )

    assert chunks
    assert chunks[0].section_id == section_id
    assert chunks[0].section_title == "Mục 1"
    assert chunks[0].section_path == "Chương 1 > Mục 1"
    assert chunks[0].content.startswith("[Chương 1 > Mục 1]")
    assert "Book: Sách thử nghiệm" in chunks[0].embedding_text
    assert "Author: Tác giả A" in chunks[0].embedding_text
    assert "Section path: Chương 1 > Mục 1" in chunks[0].embedding_text
    assert len(chunks[0].content_hash) == 64

    same_chunks = build_section_chunks(
        book_title="Sách thử nghiệm",
        author="Tác giả A",
        section_id=section_id,
        section_title="Mục 1",
        section_path="Chương 1 > Mục 1",
        text="Đây là nội dung đủ dài để tạo chunk. " * 30,
        chunk_size_chars=160,
        chunk_overlap_chars=20,
        embedding_version="section-v1",
    )
    assert [chunk.content_hash for chunk in chunks] == [chunk.content_hash for chunk in same_chunks]


def test_build_section_search_text_normalizes_accents_and_metadata():
    search_text = build_section_search_text(
        section_path="Chương 4 > Mục 4.1",
        section_title="Khái niệm SLR",
        content="Systematic Literature Review là phương pháp tổng hợp tài liệu.",
    )

    assert "chuong 4 muc 4.1" in search_text
    assert "khai niem slr" in search_text
    assert "systematic literature review" in search_text


def test_build_section_chunks_skips_empty_text():
    chunks = build_section_chunks(
        book_title="Sách thử nghiệm",
        author=None,
        section_id=uuid.uuid4(),
        section_title="Mục rỗng",
        section_path="Mục rỗng",
        text="   \n\n",
        chunk_size_chars=100,
        chunk_overlap_chars=10,
        embedding_version="section-v1",
    )

    assert chunks == []
