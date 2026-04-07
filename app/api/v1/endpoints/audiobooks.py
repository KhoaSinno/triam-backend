from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.crud import audiobook as crud_book
from app.models.db_models import Book

router = APIRouter()


@router.get("/books", response_model=list[Book])
def read_all_books(session: Session = Depends(get_session)):
    return crud_book.get_audiobooks(session)


@router.post("/books", response_model=Book)
def add_new_book(book: Book, session: Session = Depends(get_session)):
    return crud_book.create_audiobook(session, book)
