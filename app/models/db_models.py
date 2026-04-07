import uuid
from datetime import datetime, timezone
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Integer, Text
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    title: str = Field(sa_column=Column(Text, nullable=False))
    author: Optional[str] = Field(default=None, sa_column=Column(Text))
    gcs_pdf_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_chapters: Optional[int] = Field(default=None, sa_column=Column(Integer))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))
    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))



class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    chapter_index: int = Field(sa_column=Column(Integer, nullable=False))
    title: str = Field(sa_column=Column(Text, nullable=False))
    review_audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    review_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: Optional[str] = Field(default=None, sa_column=Column(Text))


class ChapterSegment(SQLModel, table=True):
    __tablename__ = "chapter_segments"

    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: uuid.UUID = Field(foreign_key="chapters.id")
    segment_index: int = Field(sa_column=Column(Integer, nullable=False))
    audio_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))


class BookKnowledge(SQLModel, table=True):
    __tablename__ = "book_knowledge"

    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="books.id")
    chapter_index: int = Field(sa_column=Column(Integer, nullable=False))
    chunk_index: int = Field(sa_column=Column(Integer, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    # Giả định vector có độ dài 1536 (OpenAI text-embedding-3-small)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))
