import os
import uuid
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import Book, ReadingPlan, ReadingPlanScheduleSlot
from app.services.audiobook_service import update_reading_plan

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

user_id = uuid.UUID("ca7c241b-169b-4300-9747-16da743ffef0")
book_id = uuid.UUID("4e8d605a-5e19-4f47-a59e-e5bab8efa6f1")

with Session(engine) as session:
    print(f"Testing update_reading_plan on Book {book_id} (active)...")
    try:
        # Try to change it to Mon at 21:00
        res = update_reading_plan(
            session,
            book_id=book_id,
            user_id=user_id,
            schedule_config=["Mon"],
            reminder_time="21:00"
        )
        print("Success:", res)
        session.rollback()
    except Exception as e:
        print("Failed:", type(e).__name__, str(e))
        session.rollback()
