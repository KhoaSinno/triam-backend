# ruff: noqa: E402

import asyncio
import os
import sys
import uuid
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ebooklib import epub
from sqlmodel import Session, select

from app.core.constant import PlanMode
from app.db.database import engine
from app.models.db_models import Book, LearningUnit, LearningUnitSegment, ProcessingJob
from app.schemas.plan import PlanInput
from app.services import upload_service
from app.services.upload_service import handle_generate_plan, handle_upload_document
from app.services.workers.book_pipeline import run_background_processing


class LocalUploadFile:
    def __init__(self, path: Path, content_type: str):
        self.path = path
        self.filename = path.name
        self.content_type = content_type

    async def read(self) -> bytes:
        return self.path.read_bytes()


def build_epub_sample(path: Path) -> None:
    book = epub.EpubBook()
    book.set_identifier("phase5-sample")
    book.set_title("Phase 5 EPUB Sample")
    book.set_language("vi")
    book.add_author("TRIAM")

    chapter_1 = epub.EpubHtml(title="Chương 1: Khởi động", file_name="chap_1.xhtml", lang="vi")
    chapter_1.content = """
    <h1>Chương 1: Khởi động</h1>
    <p>Đây là nội dung mẫu để kiểm tra EPUB. Người học cần nắm ý chính và ví dụ minh họa.</p>
    """
    chapter_2 = epub.EpubHtml(title="Chương 2: Ôn tập", file_name="chap_2.xhtml", lang="vi")
    chapter_2.content = """
    <h1>Chương 2: Ôn tập</h1>
    <p>Nội dung ôn tập giúp kiểm tra khả năng tạo learning unit và audio.</p>
    """
    book.add_item(chapter_1)
    book.add_item(chapter_2)
    book.toc = (epub.Link("chap_1.xhtml", "Chương 1: Khởi động", "c1"), epub.Link("chap_2.xhtml", "Chương 2: Ôn tập", "c2"))
    book.spine = ["nav", chapter_1, chapter_2]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(str(path), book)


async def run_case(path: Path, content_type: str, mode: PlanMode) -> None:
    user_id = uuid.uuid4()
    print(f"\n=== CASE {path.name} | mode={mode.value} | user={user_id} ===", flush=True)

    with Session(engine) as session:
        upload_result = await handle_upload_document(session, LocalUploadFile(path, content_type), user_id)
        book_id = uuid.UUID(upload_result["book_id"])
        print(
            f"UPLOAD OK | book_id={book_id} | sections={upload_result['total_sections']} | "
            f"depth={upload_result['max_depth']} | warnings={upload_result['warnings']}",
            flush=True,
        )

    with Session(engine) as session:
        plan_result = await handle_generate_plan(
            session,
            PlanInput(book_id=book_id, mode=mode, pace=1, schedule_config=["Mon"]),
            user_id,
        )
        job_id = uuid.UUID(plan_result["job_id"])
        print(
            f"PLAN OK | book_id={book_id} | job_id={job_id} | planned_units={len(plan_result['planned_units'])}",
            flush=True,
        )

    await run_background_processing(book_id, mode.value, job_id)

    with Session(engine) as session:
        book = session.get(Book, book_id)
        job = session.get(ProcessingJob, job_id)
        units = session.exec(
            select(LearningUnit).where(LearningUnit.book_id == book_id, LearningUnit.mode == mode).order_by(LearningUnit.unit_index)
        ).all()
        unit_ids = [unit.id for unit in units]
        segments = session.exec(select(LearningUnitSegment).where(LearningUnitSegment.learning_unit_id.in_(unit_ids))).all() if unit_ids else []
        print(
            f"WORKER DONE | book_status={book.status if book else None} | "
            f"job_status={job.status if job else None} | progress={job.progress_percent if job else None} | "
            f"units={len(units)} | segments={len(segments)}",
            flush=True,
        )
        for unit in units:
            print(
                f"UNIT | index={unit.unit_index} | title={unit.title} | status={unit.status} | "
                f"segments={unit.main_segment_count} | review={bool(unit.review_text)}",
                flush=True,
            )


async def main() -> None:
    os.makedirs("uploads", exist_ok=True)
    upload_service.process_book_task.apply_async = lambda *, args, queue: print(f"QUEUE STUB | queue={queue} | args={args}", flush=True)

    epub_path = Path("uploads/phase5_sample.epub")
    build_epub_sample(epub_path)

    cases = [
        (Path("Chương 4_ Phương pháp luận nghiên cứu.pdf"), "application/pdf", PlanMode.FULL),
        (Path("trr.docx"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document", PlanMode.PARETO),
        (epub_path, "application/epub+zip", PlanMode.FULL),
    ]
    for path, content_type, mode in cases:
        await run_case(path, content_type, mode)


if __name__ == "__main__":
    asyncio.run(main())
