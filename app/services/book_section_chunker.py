import hashlib
import re
import uuid
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

_WHITESPACE_RE = re.compile(r"[ \t\r\f\v]+")


@dataclass(frozen=True)
class SectionChunk:
    section_id: uuid.UUID
    chunk_index: int
    content: str
    embedding_text: str
    content_hash: str
    char_count: int


def normalize_section_text(text: str | None) -> str:
    if not text:
        return ""
    lines = [_WHITESPACE_RE.sub(" ", line).strip() for line in text.splitlines()]
    compact_lines = [line for line in lines if line]
    return "\n".join(compact_lines).strip()


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
                chunk_index=index,
                content=content,
                embedding_text=embedding_text,
                content_hash=content_hash,
                char_count=len(content),
            )
        )
    return chunks
