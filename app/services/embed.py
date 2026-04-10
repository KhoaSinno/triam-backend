import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI
from sqlmodel import Session

from app.core.config import settings
from app.crud.book_knowledge import bulk_create_knowledge
from app.models.db_models import BookKnowledge

aclient = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""],
)


async def embed_and_save_chapter(
    book_id: uuid.UUID,
    chapter_id: uuid.UUID,
    raw_text: str,
    session: Session,
) -> None:
    """
    Luồng 1 RAG:
    1. Cắt raw_text thành chunks bằng RecursiveCharacterTextSplitter.
    2. Gọi OpenAI Embedding API (batch).
    3. Lưu vào bảng book_knowledge qua SQLModel session.
    """
    chunks = _splitter.split_text(raw_text)
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
    print(f"✅ RAG: Saved {len(records)} vectors for chapter_id={chapter_id}")
