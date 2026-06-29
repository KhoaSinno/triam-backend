import hashlib
import re
import uuid
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.agent_grounding.query_normalizer import normalized_key

_WHITESPACE_RE = re.compile(r"[ \t\r\f\v]+")


@dataclass(frozen=True)
class SectionChunk:
    section_id: uuid.UUID
    section_title: str
    section_path: str
    chunk_index: int
    content: str
    embedding_text: str
    content_hash: str
    char_count: int



def normalize_section_text(text: str | None) -> str:
    """
    Bộ chuẩn hóa nâng cấp đa ngôn ngữ (Xử lý tối ưu lỗi PDF tiếng Việt và sở hữu cách tiếng Anh)
    """
    if not text:
        return ""

    # 1. Đồng nhất xuống dòng
    text = text.replace("\r\n", "\n")

    # 2. Xóa ký tự rác (cid:xxx)
    text = re.sub(r"\(cid:\d+\)", "•", text)

    # 3. SỬA LỖI ĐẶC THÙ TIẾNG ANH: Vá các khoảng trắng bị lỗi bẻ đôi do sở hữu cách hoặc viết tắt
    # Đổi "george s " -> "george's ", "tha s " -> "that's " (hoặc tha's theo ngôn ngữ gốc của truyện)
    text = re.sub(r"\b(\w+)\s+s\b", r"\1's", text)   # Sửa george s -> george's, curley s -> curley's
    text = re.sub(r"\b(\w+)\s+ll\b", r"\1'll", text)  # Sửa you ll -> you'll
    text = re.sub(r"\b(\w+)\s+d\b", r"\1'd", text)    # Sửa you d -> you'd
    text = re.sub(r"\b(\w+)\s+t\b", r"\1't", text)    # Sửa didn t -> didn't, don t -> don't
    text = re.sub(r"\b(\w+)\s+re\b", r"\1're", text)  # Sửa you re -> you're
    text = re.sub(r"\b(\w+)\s+ve\b", r"\1've", text)  # Sửa you ve -> you've

    # 4. Tách Paragraph bằng dấu xuống dòng kép
    paragraphs = text.split("\n\n")
    normalized_paragraphs = []

    for paragraph in paragraphs:
        p_clean = paragraph.strip()
        if not p_clean:
            continue

        # 5. Xóa bỏ toàn bộ dấu xuống dòng đơn lẻ nằm giữa các câu liền mạch
        p_sub = re.sub(r"(?<![•\-\*\d\.])\n(?!\s*[•\-\*\d\.])", " ", p_clean)

        # 6. Gom khoảng trắng thừa
        p_sub = re.sub(r"[ \t]+", " ", p_sub)

        normalized_paragraphs.append(p_sub.strip())

    return "\n\n".join(normalized_paragraphs)


def build_section_search_text(*, section_path: str, section_title: str, content: str) -> str:
    return normalized_key(f"{section_path} {section_title} {content}")


def build_section_chunks(
    *,
    book_title: str,
    author: str | None,
    section_id: uuid.UUID,
    section_title: str,
    section_path: str,
    text: str | None,
    chunk_size_chars: int,
    chunk_overlap_chars: int,
    embedding_version: str,
) -> list[SectionChunk]:
    normalized_text = normalize_section_text(text)
    if not normalized_text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max(1, chunk_size_chars),
        chunk_overlap=max(0, min(chunk_overlap_chars, chunk_size_chars - 1)),
        separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""],
    )
    raw_chunks = [chunk.strip() for chunk in splitter.split_text(normalized_text) if chunk.strip()]

    chunks: list[SectionChunk] = []
    for index, chunk in enumerate(raw_chunks):
        content = f"[{section_path}]\n{chunk}"
        embedding_parts = [
            f"Book: {book_title}",
            f"Section path: {section_path}",
            f"Section title: {section_title}",
        ]
        if author:
            embedding_parts.insert(1, f"Author: {author}")
        embedding_text = "\n".join(embedding_parts) + f"\nContent:\n{chunk}"
        content_hash = hashlib.sha256(
            f"{embedding_version}\0{section_id}\0{index}\0{content}".encode("utf-8")
        ).hexdigest()
        chunks.append(
            SectionChunk(
                section_id=section_id,
                section_title=section_title,
                section_path=section_path,
                chunk_index=index,
                content=content,
                embedding_text=embedding_text,
                content_hash=content_hash,
                char_count=len(content),
            )
        )
    return chunks
