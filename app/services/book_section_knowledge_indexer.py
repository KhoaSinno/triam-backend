import uuid
from dataclasses import dataclass
from typing import Protocol

from openai import AsyncOpenAI
from sqlmodel import Session, col, select

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import Book, BookSection, BookSectionKnowledge
from app.repositories.book_section_knowledge_repo import (
    bulk_create_section_knowledge,
    delete_section_knowledge,
    list_section_hashes,
)
from app.services.book_section_chunker import SectionChunk, build_section_chunks


class SectionEmbeddingProvider(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...


class OpenAISectionEmbeddingProvider:
    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = await self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]


@dataclass(frozen=True)
class BookSectionIndexResult:
    book_id: uuid.UUID
    total_sections: int
    indexed_sections: int
    skipped_sections: int
    chunks_created: int


def _build_records(
    *,
    book_id: uuid.UUID,
    chunks: list[SectionChunk],
    embeddings: list[list[float]],
) -> list[BookSectionKnowledge]:
    return [
        BookSectionKnowledge(
            book_id=book_id,
            section_id=chunk.section_id,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            content_hash=chunk.content_hash,
            embedding_model=settings.BOOK_SECTION_EMBEDDING_MODEL,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
            char_count=chunk.char_count,
            embedding=embeddings[index],
        )
        for index, chunk in enumerate(chunks)
    ]


def _section_chunks(book: Book, section: BookSection) -> list[SectionChunk]:
    return build_section_chunks(
        book_title=book.title,
        author=book.author,
        section_id=section.id,
        section_title=section.title,
        section_path=section.path,
        text=section.text_content,
        chunk_size_chars=settings.BOOK_SECTION_CHUNK_SIZE_CHARS,
        chunk_overlap_chars=settings.BOOK_SECTION_CHUNK_OVERLAP_CHARS,
        embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
    )


async def index_book_sections(
    session: Session,
    *,
    book_id: uuid.UUID,
    embedder: SectionEmbeddingProvider | None = None,
) -> BookSectionIndexResult:
    book = session.get(Book, book_id)
    if not book:
        raise ValueError(f"Book not found: {book_id}")

    sections = list(
        session.exec(
            select(BookSection)
            .where(
                BookSection.book_id == book_id,
                BookSection.text_content.is_not(None),
                BookSection.text_char_count > 0,
            )
            .order_by(col(BookSection.section_index))
        ).all()
    )
    if not sections:
        return BookSectionIndexResult(book_id=book_id, total_sections=0, indexed_sections=0, skipped_sections=0, chunks_created=0)

    provider = embedder or OpenAISectionEmbeddingProvider(
        api_key=settings.OPENAI_API_KEY,
        model=settings.BOOK_SECTION_EMBEDDING_MODEL,
    )

    indexed_sections = 0
    skipped_sections = 0
    chunks_created = 0
    batch_size = max(1, settings.BOOK_SECTION_EMBEDDING_BATCH_SIZE)

    for section in sections:
        chunks = _section_chunks(book, section)
        if not chunks:
            skipped_sections += 1
            continue

        current_hashes = list_section_hashes(
            session,
            section_id=section.id,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
        )
        next_hashes = [chunk.content_hash for chunk in chunks]
        if current_hashes == next_hashes:
            skipped_sections += 1
            continue

        delete_section_knowledge(
            session,
            section_id=section.id,
            embedding_version=settings.BOOK_SECTION_EMBEDDING_VERSION,
        )
        for start in range(0, len(chunks), batch_size):
            chunk_batch = chunks[start:start + batch_size]
            embeddings = await provider.embed_texts([chunk.embedding_text for chunk in chunk_batch])
            records = _build_records(book_id=book_id, chunks=chunk_batch, embeddings=embeddings)
            bulk_create_section_knowledge(session, records)
            chunks_created += len(records)

        session.commit()
        indexed_sections += 1

    log.info(
        "BookSectionKnowledge index done | "
        f"book_id={book_id} | sections={len(sections)} | indexed={indexed_sections} | "
        f"skipped={skipped_sections} | chunks_created={chunks_created} | "
        f"version={settings.BOOK_SECTION_EMBEDDING_VERSION}"
    )
    return BookSectionIndexResult(
        book_id=book_id,
        total_sections=len(sections),
        indexed_sections=indexed_sections,
        skipped_sections=skipped_sections,
        chunks_created=chunks_created,
    )
