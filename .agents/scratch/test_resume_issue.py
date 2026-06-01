import os
import uuid
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import Book, ReadingPlan
from app.services.audiobook_service import resume_reading_plan

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

user_id = uuid.UUID("ca7c241b-169b-4300-9747-16da743ffef0")
book_id = uuid.UUID("21f1b570-88c3-4a69-b6a7-80441ffa57a7")

with Session(engine) as session:
    print(f"Testing resume_reading_plan on Book {book_id}...")
    try:
        res = resume_reading_plan(session, book_id=book_id, user_id=user_id)
        print("Resume Success:", res)
        session.rollback()
    except Exception as e:
        print("Resume Failed:", type(e).__name__, str(e))
        session.rollback()
