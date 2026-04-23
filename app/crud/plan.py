from sqlmodel import Session

from app.models.db_models import ReadingPlan


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
