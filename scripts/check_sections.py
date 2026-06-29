from sqlmodel import Session, select
from app.db.database import engine
from app.models.db_models import Book, BookSection

with Session(engine) as session:
    # Query distinct book titles that have sections
    books = session.exec(select(Book).join(BookSection, BookSection.book_id == Book.id).distinct()).all()
    print("📚 Books with Sections in DB:")
    for b in books:
        count = session.exec(select(BookSection).where(BookSection.book_id == b.id)).all()
        print(f"ID: {b.id} | Title: {b.title} | Sections: {len(count)}")
