import argparse
import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlmodel import Session, select  # noqa: E402

from app.core.constant import PlanMode, PlanStatus  # noqa: E402
from app.db.database import engine  # noqa: E402
from app.models.db_models import Book, ReadingPlan  # noqa: E402
from app.services.learning_progress_service import sync_book_learning_state  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill cached book learning states for existing books.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--book-id", help="Backfill one book id.")
    group.add_argument("--all", action="store_true", help="Backfill every book with a non-error reading plan.")
    parser.add_argument("--dry-run", action="store_true", help="Print target rows without writing state.")
    return parser.parse_args()


def _target_plans(session: Session, book_id: uuid.UUID | None) -> list[tuple[uuid.UUID, uuid.UUID, object]]:
    statement = (
        select(Book.user_id, ReadingPlan.book_id, ReadingPlan.mode)
        .join(Book, Book.id == ReadingPlan.book_id)
        .where(ReadingPlan.status != PlanStatus.ERROR.value)
        .distinct()
    )
    if book_id:
        statement = statement.where(ReadingPlan.book_id == book_id)
    return list(session.exec(statement).all())


def main() -> None:
    args = _parse_args()
    book_id = uuid.UUID(args.book_id) if args.book_id else None
    with Session(engine) as session:
        targets = _target_plans(session, book_id)

    print("book_learning_state_backfill_targets", {"count": len(targets), "dry_run": args.dry_run})
    if args.dry_run:
        for user_id, target_book_id, mode in targets:
            print("target", {"user_id": str(user_id), "book_id": str(target_book_id), "mode": PlanMode(mode).value})
        return

    for user_id, target_book_id, mode in targets:
        mode_value = PlanMode(mode)
        with Session(engine) as session:
            state = sync_book_learning_state(session, user_id=user_id, book_id=target_book_id, mode=mode_value)
            print(
                "backfilled",
                {
                    "user_id": str(user_id),
                    "book_id": str(target_book_id),
                    "mode": mode_value.value,
                    "status": state.status,
                    "progress": state.book_progress_percent,
                },
            )


if __name__ == "__main__":
    main()
