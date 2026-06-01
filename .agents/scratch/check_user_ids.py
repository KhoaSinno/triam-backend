import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import Book, ReadingPlan, ReadingPlanScheduleSlot

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

with Session(engine) as session:
    books = session.exec(select(Book)).all()
    print("--- BOOKS AND USER IDS ---")
    for b in books:
        print(f"Book: {b.title} | ID: {b.id} | UserID: {b.user_id}")
