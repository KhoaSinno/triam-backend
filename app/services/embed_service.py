import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
from sqlmodel import Session

from app.core.config import settings
from app.core.logger import log
from app.models.db_models import BookKnowledge
from app.repositories.book_knowledge_repo import bulk_create_knowledge

aclient = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""],
)


def process_book_to_enriched_chunks(book_title: str, chapter_title: str, raw_text: str):
    raw_chunks = _splitter.split_text(raw_text)
    enriched_chunks = []

    for index, chunk in enumerate(raw_chunks):
        # BƠM NGỮ CẢNH: Giúp Vector nắm bắt được bối cảnh toàn cục
        header = f"[Tác phẩm: {book_title} | Chương: {chapter_title}]\n"
        enriched_content = header + chunk

        enriched_chunks.append(enriched_content)

    return enriched_chunks


async def embed_and_save_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    book_title: str,
    chapter_title: str,
    raw_text: str,
    session: Session,
) -> None:
    """
    Luồng 1 RAG:
    1. Cắt raw_text thành chunks bằng RecursiveCharacterTextSplitter.
    2. Gọi OpenAI Embedding API (batch).
    3. Lưu vào bảng book_knowledge qua SQLModel session.
    """
    chunks: list[str] = process_book_to_enriched_chunks(
        book_title=book_title,
        chapter_title=chapter_title,
        raw_text=raw_text,
    )

    if not chunks:
        return

    response = await aclient.embeddings.create(
        input=chunks,
        model="text-embedding-3-small",
    )

    records = [
        BookKnowledge(
            book_id=book_id,
            chapter_id=chapter_id,
            chunk_index=i,
            content=chunks[i],
            embedding=embedding_data.embedding,
        )
        for i, embedding_data in enumerate(response.data)
    ]

    bulk_create_knowledge(session, records)
    log.info(f"RAG: Saved {len(records)} vectors for chapter_id={chapter_id}")
