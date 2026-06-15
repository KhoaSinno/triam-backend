import uuid
from dataclasses import dataclass

from sqlmodel import Session, col, select

from app.core.constant import PlanStatus
from app.models.db_models import Book, BookLearningState, ReadingPlan


@dataclass(frozen=True)
class BookListProjection:
    book: Book
    current_plan: ReadingPlan | None
    learning_state: BookLearningState | None


def _latest_plan_by_book(plans: list[ReadingPlan]) -> dict[uuid.UUID, ReadingPlan]:
    result: dict[uuid.UUID, ReadingPlan] = {}
    for plan in plans:
        result.setdefault(plan.book_id, plan)
    return result


def _mode_key(mode: object) -> str:
    return str(mode.value if hasattr(mode, "value") else mode)


def _learning_state_by_book_mode(states: list[BookLearningState]) -> dict[tuple[uuid.UUID, str], BookLearningState]:
    return {(state.book_id, _mode_key(state.mode)): state for state in states}


def list_book_library_projections(session: Session, *, user_id: uuid.UUID) -> list[BookListProjection]:
    books = list(
        session.exec(
            select(Book)
            .where(Book.user_id == user_id)
            .order_by(col(Book.created_at).desc(), col(Book.id).desc())
        ).all()
    )
    if not books:
        return []

    book_ids = [book.id for book in books]
    plans = list(
        session.exec(
            select(ReadingPlan)
            .where(
                col(ReadingPlan.book_id).in_(book_ids),
                ReadingPlan.status != PlanStatus.ERROR.value,
            )
            .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
        ).all()
    )
    states = list(
        session.exec(
            select(BookLearningState).where(
                BookLearningState.user_id == user_id,
                col(BookLearningState.book_id).in_(book_ids),
            )
        ).all()
    )

    plan_by_book = _latest_plan_by_book(plans)
    state_by_book_mode = _learning_state_by_book_mode(states)
    return [
        BookListProjection(
            book=book,
            current_plan=plan_by_book.get(book.id),
            learning_state=state_by_book_mode.get(
                (book.id, _mode_key(plan_by_book[book.id].mode))
            )
            if book.id in plan_by_book
            else None,
        )
        for book in books
    ]


def get_book_library_projection(
    session: Session,
    *,
    user_id: uuid.UUID,
    book_id: uuid.UUID,
) -> BookListProjection | None:
    book = session.exec(select(Book).where(Book.id == book_id, Book.user_id == user_id)).first()
    if not book:
        return None

    plan = session.exec(
        select(ReadingPlan)
        .where(
            ReadingPlan.book_id == book_id,
            ReadingPlan.status != PlanStatus.ERROR.value,
        )
        .order_by(col(ReadingPlan.updated_at).desc(), col(ReadingPlan.created_at).desc())
    ).first()
    state = None
    if plan:
        state = session.exec(
            select(BookLearningState).where(
                BookLearningState.user_id == user_id,
                BookLearningState.book_id == book_id,
                BookLearningState.mode == plan.mode,
            )
        ).first()

    return BookListProjection(book=book, current_plan=plan, learning_state=state)
