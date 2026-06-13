import uuid

from sqlmodel import Session, col, select

from app.core.constant import PlanMode, PlanStatus
from app.models.db_models import Book, ReadingPlan


def get_current_plan_for_owned_book(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
) -> ReadingPlan | None:
    return session.exec(
        select(ReadingPlan)
        .join(Book, Book.id == ReadingPlan.book_id)
        .where(
            Book.id == book_id,
            Book.user_id == user_id,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()


def get_plan_for_book_mode(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> ReadingPlan | None:
    return session.exec(
        select(ReadingPlan)
        .where(
            ReadingPlan.book_id == book_id,
            ReadingPlan.mode == mode,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()


def list_plans_for_book_mode(
    session: Session,
    *,
    book_id: uuid.UUID,
    mode: PlanMode,
) -> list[ReadingPlan]:
    return list(
        session.exec(
            select(ReadingPlan)
            .where(
                ReadingPlan.book_id == book_id,
                ReadingPlan.mode == mode,
                ReadingPlan.status != PlanStatus.ERROR.value,
            )
            .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
        ).all()
    )
