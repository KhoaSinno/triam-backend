from sqlmodel import Session, select
from app.db.database import engine
from app.models.db_models import Book

with Session(engine) as session:
    books = session.exec(select(Book)).all()
    print("📚 Books in Database:")
    for b in books:
        print(f"ID: {b.id} | Title: {b.title} | Document Type: {b.document_type}")
