import argparse
import asyncio
import uuid

from sqlmodel import Session, select

from app.db.database import engine
from app.models.db_models import Book, BookSection
from app.services.book_section_knowledge_indexer import backfill_book_section_search_text, index_book_sections
from app.tasks.book_tasks import index_book_sections_task


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill canonical BookSection vector knowledge.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--book-id", help="Backfill one book id.")
    group.add_argument("--all", action="store_true", help="Backfill every book that has BookSection rows.")
    parser.add_argument("--run-now", action="store_true", help="Run in this process instead of enqueueing Celery tasks.")
    parser.add_argument(
        "--search-text-only",
        action="store_true",
        help="Backfill lexical search_text only. Requires --run-now and does not call embedding providers.",
    )
    return parser.parse_args()


def _book_ids_with_sections(session: Session) -> list[uuid.UUID]:
    rows = session.exec(
        select(Book.id)
        .join(BookSection, BookSection.book_id == Book.id)
        .where(BookSection.text_content.is_not(None), BookSection.text_char_count > 0)
        .distinct()
    ).all()
    return list(rows)


async def _run_now(book_ids: list[uuid.UUID]) -> None:
    for book_id in book_ids:
        with Session(engine) as session:
            result = await index_book_sections(session, book_id=book_id)
        print(
            "indexed",
            {
                "book_id": str(book_id),
                "sections": result.total_sections,
                "indexed": result.indexed_sections,
                "skipped": result.skipped_sections,
                "chunks": result.chunks_created,
            },
        )


def _run_search_text_now(book_ids: list[uuid.UUID]) -> None:
    for book_id in book_ids:
        with Session(engine) as session:
            result = backfill_book_section_search_text(session, book_id=book_id)
        print("search_text_backfilled", {"book_id": str(book_id), "updated_rows": result.updated_rows})


def _enqueue(book_ids: list[uuid.UUID]) -> None:
    for book_id in book_ids:
        index_book_sections_task.apply_async(args=[str(book_id)], queue="document")
        print("enqueued", {"book_id": str(book_id)})


def main() -> None:
    args = _parse_args()
    if args.search_text_only and not args.run_now:
        raise SystemExit("--search-text-only requires --run-now because it is a local DB-only maintenance operation.")

    if args.book_id:
        book_ids = [uuid.UUID(args.book_id)]
    else:
        with Session(engine) as session:
            book_ids = _book_ids_with_sections(session)

    if args.search_text_only:
        _run_search_text_now(book_ids)
    elif args.run_now:
        asyncio.run(_run_now(book_ids))
    else:
        _enqueue(book_ids)


if __name__ == "__main__":
    main()
