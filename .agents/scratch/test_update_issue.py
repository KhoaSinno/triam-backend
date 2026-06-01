import os
import uuid
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import Book, ReadingPlan, ReadingPlanScheduleSlot
from app.services.audiobook_service import update_reading_plan, resume_reading_plan

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

user_id = uuid.UUID("ca7c241b-169b-4300-9747-16da743ffef0")
# Let's find one active book for this user
with Session(engine) as session:
    active_plans = session.exec(select(ReadingPlan).where(ReadingPlan.status == "active")).all()
    print("Active plans in DB:")
    for p in active_plans:
        print(f"Plan ID: {p.id} | Book ID: {p.book_id} | Schedule: {p.schedule_config} | Time: {p.reminder_time}")

    if active_plans:
        target_plan = active_plans[0]
        print(f"\nTesting update_reading_plan on Plan {target_plan.id} (Book {target_plan.book_id})...")
        try:
            # Let's try to update schedule to Tue at 21:00 (which is free)
            res = update_reading_plan(
                session,
                book_id=target_plan.book_id,
                user_id=user_id,
                pace=target_plan.pace,
                schedule_config=["Tue"],
                reminder_time="21:00"
            )
            print("Update Success:", res)
            # rollback to avoid messing up DB
            session.rollback()
        except Exception as e:
            print("Update Failed:", type(e).__name__, str(e))
            session.rollback()
