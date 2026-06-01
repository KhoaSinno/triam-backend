import os
import uuid
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import Book, ReadingPlan, ReadingPlanScheduleSlot

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to Database at: {db_url}")
engine = create_engine(db_url)

with Session(engine) as session:
    print("\n--- BOOKS ---")
    books = session.exec(select(Book)).all()
    for b in books:
        print(f"Book ID: {b.id} | Title: {b.title} | Status: {b.status}")

    print("\n--- READING PLANS ---")
    plans = session.exec(select(ReadingPlan)).all()
    for p in plans:
        print(f"Plan ID: {p.id} | Book ID: {p.book_id} | Status: {p.status} | Schedule: {p.schedule_config} | Time: {p.reminder_time}")

    print("\n--- ACTIVE SCHEDULE SLOTS ---")
    slots = session.exec(select(ReadingPlanScheduleSlot).where(ReadingPlanScheduleSlot.is_active == True)).all()
    for s in slots:
        print(f"Slot ID: {s.id} | Plan ID: {s.plan_id} | Book ID: {s.book_id} | Weekday: {s.weekday} | Time: {s.reminder_time} | Active: {s.is_active}")
