import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.crud import audiobook as crud_book
from app.db import get_session
from app.models.db_models import Book, Chapter, ChapterSegment

router = APIRouter()


@router.get("/books", response_model=list[Book])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return crud_book.get_audiobooks(session)


@router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return crud_book.get_book_by_id(session, book_id)


@router.post("/books", response_model=Book)
def add_new_book(book: Book, session: Annotated[Session, Depends(get_session)]):
    return crud_book.create_book(session, book)


@router.get("/books/{book_id}/details")
def get_book_details(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    chapters = session.exec(select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_index)).all()

    result = []
    for chap in chapters:
        segments = session.exec(select(ChapterSegment).where(ChapterSegment.chapter_id == chap.id).order_by(ChapterSegment.segment_index)).all()
        result.append({"id": str(chap.id), "title": chap.title, "status": chap.status, "chapter_index": chap.chapter_index, "chapter_segments": [s.model_dump() for s in segments]})

    return {"book_status": book.status, "total_chapters": book.total_chapters, "chapters": result}
