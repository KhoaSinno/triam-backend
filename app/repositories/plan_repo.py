import uuid

from sqlmodel import Session, select

from app.core.constant import PlanStatus
from app.models.db_models import ReadingPlan


def check_plan_exist(session: Session, book_id: uuid.UUID) -> bool:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first() is not None


def get_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id)).first()


def get_active_plan_by_book_id(session: Session, book_id: uuid.UUID) -> ReadingPlan:
    return session.exec(select(ReadingPlan).where(ReadingPlan.book_id == book_id).where(ReadingPlan.status == PlanStatus.ACTIVE)).first()


def get_all_plan_by_user_id(session: Session, user_id: uuid.UUID) -> list[ReadingPlan]:
    return session.exec(select(ReadingPlan).where(ReadingPlan.user_id == user_id)).all()


def create_reading_plan(session: Session, plan: ReadingPlan) -> ReadingPlan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
