# Phase 1 Implementation Guide - DB Progress + Polling Endpoint

Muc tieu Phase 1: cho FE hien thi thanh progress on dinh khi user `generate-plan` hoac `switch-mode`, nhung **chua bat buoc dua Celery/Redis vao ngay**.

Phase nay van co the giu `FastAPI BackgroundTasks` tam thoi, nhung them mot lop quan sat tien do bang DB:

```text
FE tao job
-> BE ghi processing_jobs
-> BE tra job_id
-> Worker update processing_jobs
-> FE poll status va ve progress bar
```

Ly do lam Phase 1 truoc:

- Giai quyet ngay bai toan UX: user thay tien do, khong bi "bam xong roi cho may".
- Chua bat fresher phai hoc Redis/Celery ngay lap tuc.
- Khi chuyen sang Celery o Phase 2, FE contract va DB job model gan nhu giu nguyen.

Trade-off:

- Van chua durable bang Celery. Neu server restart, `BackgroundTasks` co the mat.
- Nhung progress da nam trong DB, nen user reload app van thay trang thai cuoi cung.
- Day la buoc dem tot cho capstone, khong phai kien truc production cuoi cung.

## 1. FE Co Ve Progress Bar Duoc Khong?

Co.

FE chi can:

1. Goi `POST /api/v1/generate-plan`.
2. Lay `job_id` tu response.
3. Poll `GET /api/v1/jobs/{job_id}` moi 2-5 giay.
4. Ve progress bar bang `progress_percent`.
5. Khi `status = partial_ready`, unlock nut nghe neu product cho nghe som.
6. Khi `status = ready`, dung polling.
7. Khi `status = error`, hien thi loi.

Response mau:

```json
{
  "id": "f05b4d64-2f55-4e6a-9c9b-873b4f38a62f",
  "book_id": "94266dd3-ed47-4870-9efc-85d1634d8d9b",
  "job_type": "generate_plan",
  "status": "processing",
  "progress_percent": 42,
  "current_step": "Generating audio for chapter 4/10",
  "total_units": 10,
  "done_units": 4,
  "failed_units": 0,
  "error_message": null
}
```

## 2. Status Design

Them status rieng cho job. Khong nen chi dua vao `books.status`, vi mot book co the co nhieu job:

- Generate plan lan dau.
- Switch mode.
- Re-generate audio loi.
- Sau nay reminder/review jobs.

### Job Status

```text
queued -> processing -> partial_ready -> ready
                         |
                         -> error
                         -> cancelled
```

### Job Type

```text
upload
generate_plan
switch_mode
notification
review
```

Phase 1 can dung:

- `generate_plan`
- `switch_mode`

## 3. Code Change: Constants

File: `app/core/constant.py`

Them enum:

```python
class BookStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PARTIAL_READY = "partial_ready"
    READY = "ready"
    ERROR = "error"


class ProcessingJobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    PARTIAL_READY = "partial_ready"
    READY = "ready"
    ERROR = "error"
    CANCELLED = "cancelled"


class ProcessingJobType(str, Enum):
    UPLOAD = "upload"
    GENERATE_PLAN = "generate_plan"
    SWITCH_MODE = "switch_mode"
    NOTIFICATION = "notification"
    REVIEW = "review"
```

Tai sao:

- `BookStatus` la trang thai tong cua book.
- `ProcessingJobStatus` la trang thai cua mot lan xu ly.
- Tach rieng de sau nay mot book co nhieu job van debug duoc.

Trade-off:

- Them bang/trang thai lam code dai hon.
- Doi lai FE va BE co mot contract ro, khong phai suy luan tien do tu chapter/segment.

## 4. Code Change: DB Model

File: `app/models/db_models.py`

Them import:

```python
from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType
```

Them model sau `ReadingPlan` hoac sau `Book`:

```python
class ProcessingJob(SQLModel, table=True):
    __tablename__ = "processing_jobs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(sa_column=Column(UUID(as_uuid=True), index=True, nullable=False))
    book_id: uuid.UUID | None = Field(
        default=None,
        sa_column=Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), index=True),
    )
    job_type: ProcessingJobType = Field(sa_column=Column(SAEnum(ProcessingJobType), nullable=False, index=True))
    status: ProcessingJobStatus = Field(
        default=ProcessingJobStatus.QUEUED,
        sa_column=Column(SAEnum(ProcessingJobStatus), nullable=False, index=True),
    )
    mode: PlanMode | None = Field(default=None, sa_column=Column(SAEnum(PlanMode)))
    progress_percent: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    current_step: str | None = Field(default=None, sa_column=Column(Text))
    total_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    done_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    failed_units: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    error_message: str | None = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    started_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    finished_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
```

Tai sao khong them progress vao `books` thoi?

- `books.status` chi nen noi book dang draft/processing/ready/error.
- `processing_jobs` noi job nao dang lam, lam toi dau, loi gi.
- Khi switch-mode va generate-plan cung ton tai, job table debug tot hon nhieu.

Trade-off:

- Phai them migration va repository.
- Doi lai sau nay chuyen Celery rat de, vi Celery task chi can update job row.

## 5. Code Change: Alembic Migration

Chay:

```powershell
uv run alembic revision -m "add processing jobs"
```

Sau do sua file migration thanh dang nay. Thay `revision` va `down_revision` theo file Alembic generate.

File: `app/db/migrations/versions/<revision>_add_processing_jobs.py`

```python
"""add processing jobs

Revision ID: <revision>
Revises: <down_revision>
Create Date: 2026-05-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "<revision>"
down_revision: Union[str, None] = "<down_revision>"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


processing_job_type = postgresql.ENUM(
    "upload",
    "generate_plan",
    "switch_mode",
    "notification",
    "review",
    name="processingjobtype",
)

processing_job_status = postgresql.ENUM(
    "queued",
    "processing",
    "partial_ready",
    "ready",
    "error",
    "cancelled",
    name="processingjobstatus",
)


def upgrade() -> None:
    processing_job_type.create(op.get_bind(), checkfirst=True)
    processing_job_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "processing_jobs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("book_id", sa.UUID(), nullable=True),
        sa.Column("job_type", processing_job_type, nullable=False),
        sa.Column("status", processing_job_status, nullable=False),
        sa.Column("mode", sa.Enum("FULL", "PARETO", name="planmode"), nullable=True),
        sa.Column("progress_percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_step", sa.Text(), nullable=True),
        sa.Column("total_units", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("done_units", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_units", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_processing_jobs_user_id", "processing_jobs", ["user_id"])
    op.create_index("ix_processing_jobs_book_id", "processing_jobs", ["book_id"])
    op.create_index("ix_processing_jobs_job_type", "processing_jobs", ["job_type"])
    op.create_index("ix_processing_jobs_status", "processing_jobs", ["status"])

    op.execute("ALTER TABLE books ADD CONSTRAINT ck_books_status_known CHECK (status IN ('draft', 'processing', 'partial_ready', 'ready', 'error') OR status IS NULL)")


def downgrade() -> None:
    op.execute("ALTER TABLE books DROP CONSTRAINT IF EXISTS ck_books_status_known")
    op.drop_index("ix_processing_jobs_status", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_job_type", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_book_id", table_name="processing_jobs")
    op.drop_index("ix_processing_jobs_user_id", table_name="processing_jobs")
    op.drop_table("processing_jobs")
    processing_job_status.drop(op.get_bind(), checkfirst=True)
    processing_job_type.drop(op.get_bind(), checkfirst=True)
```

Quan trong:

- Neu Alembic project dang co enum `planmode` dang luu lower-case hay upper-case, kiem tra migration cu truoc khi copy doan `sa.Enum("FULL", "PARETO", name="planmode")`.
- Neu model hien tai map `PlanMode.FULL = "full"` nhung PostgreSQL enum da tao gia tri `"FULL"`, dung theo DB hien co, khong doan.

Lenh apply:

```powershell
uv run alembic upgrade head
```

## 6. Code Change: Response Schema

File moi: `app/schemas/processing_job.py`

```python
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType


class ProcessingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ProcessingJobSummaryResponse(BaseModel):
    id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    error_message: str | None = None
```

Tai sao response co `user_id`?

- Trong dev co the giu de debug.
- Neu muon an voi FE production, bo `user_id` khoi response public.

Trade-off:

- Response day du giup debug tot.
- Nhung public DTO nen can than khong lo thong tin noi bo. Production co the dung `SummaryResponse`.

## 7. Code Change: Repository

File moi: `app/repositories/processing_job_repo.py`

```python
import uuid
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.constant import ProcessingJobStatus
from app.models.db_models import ProcessingJob


def create_processing_job(session: Session, job: ProcessingJob) -> ProcessingJob:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def get_processing_job_by_id(session: Session, job_id: uuid.UUID) -> ProcessingJob | None:
    return session.get(ProcessingJob, job_id)


def get_processing_job_by_id_and_user(session: Session, job_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(
        select(ProcessingJob).where(
            ProcessingJob.id == job_id,
            ProcessingJob.user_id == user_id,
        )
    ).first()


def get_latest_processing_job_for_book(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> ProcessingJob | None:
    return session.exec(
        select(ProcessingJob)
        .where(
            ProcessingJob.book_id == book_id,
            ProcessingJob.user_id == user_id,
        )
        .order_by(ProcessingJob.created_at.desc())
    ).first()


def update_processing_job(
    session: Session,
    job_id: uuid.UUID,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> ProcessingJob | None:
    job = session.get(ProcessingJob, job_id)
    if not job:
        return None

    if status is not None:
        job.status = status
    if progress_percent is not None:
        job.progress_percent = max(0, min(100, progress_percent))
    if current_step is not None:
        job.current_step = current_step
    if total_units is not None:
        job.total_units = total_units
    if done_units is not None:
        job.done_units = done_units
    if failed_units is not None:
        job.failed_units = failed_units
    if error_message is not None:
        job.error_message = error_message
    if started_at is not None:
        job.started_at = started_at
    if finished_at is not None:
        job.finished_at = finished_at

    job.updated_at = datetime.now(timezone.utc)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job
```

Tai sao repository khong tinh business progress?

- Repository chi DB CRUD.
- Service/worker moi biet job nay co bao nhieu chapter, partial ready luc nao.

## 8. Code Change: Service

File moi: `app/services/processing_job_service.py`

```python
import uuid

from sqlmodel import Session

from app.core.exceptions import AppException
from app.repositories.processing_job_repo import (
    get_latest_processing_job_for_book,
    get_processing_job_by_id_and_user,
)


class ProcessingJobNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy tiến trình xử lý."


def get_job_status(session: Session, user_id: uuid.UUID, job_id: uuid.UUID):
    job = get_processing_job_by_id_and_user(session, job_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job


def get_book_processing_status(session: Session, user_id: uuid.UUID, book_id: uuid.UUID):
    job = get_latest_processing_job_for_book(session, book_id, user_id)
    if not job:
        raise ProcessingJobNotFoundError()
    return job
```

Ghi chu clean code:

- Co the dua `ProcessingJobNotFoundError` vao `app/core/exceptions.py` thay vi khai bao trong service.
- Anh khuyen dua vao `exceptions.py` neu minh implement that.

Ban production nen them vao `app/core/exceptions.py`:

```python
class ProcessingJobNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy tiến trình xử lý."
```

Va service import tu `app.core.exceptions`.

## 9. Code Change: Router

File moi: `app/api/v1/routers/jobs.py`

```python
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.processing_job import ProcessingJobSummaryResponse
from app.services.processing_job_service import get_book_processing_status, get_job_status

router = APIRouter()

# TODO: Replace with JWT user later.
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


@router.get("/jobs/{job_id}", response_model=ProcessingJobSummaryResponse)
def read_job_status(job_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_job_status(session, MOCK_USER_ID, job_id)


@router.get("/books/{book_id}/processing-status", response_model=ProcessingJobSummaryResponse)
def read_book_processing_status(book_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    return get_book_processing_status(session, MOCK_USER_ID, book_id)
```

Tai sao co 2 endpoint?

- `GET /jobs/{job_id}`: chinh xac nhat khi FE vua tao job.
- `GET /books/{book_id}/processing-status`: huu ich khi FE reload app, chi con book_id.

Trade-off:

- Latest job theo book co the gay nham neu mot book co nhieu job song song.
- Phase 1 chap nhan vi moi book thuong chi co 1 job active. Phase 2 nen chan job song song hoac them query `job_type`.

## 10. Code Change: Include Router

File: `app/main.py`

Sua import:

```python
from app.api.v1.routers import audiobooks, jobs, live, study_context, threads, upload
```

Them include:

```python
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
```

Nen dat sau `audiobooks` hoac truoc deu duoc. FastAPI route `/books/{book_id}/processing-status` se khong conflict voi `/books/{book_id}` vi path cu the hon van match dung.

## 11. Code Change: Generate Plan Tao Job

File: `app/services/upload_service.py`

Them import:

```python
from app.core.constant import BookStatus, DocumentType, PlanStatus, ProcessingJobStatus, ProcessingJobType
from app.models.db_models import Book, Chapter, ProcessingJob, ReadingPlan
from app.repositories.processing_job_repo import create_processing_job
```

Sua `handle_generate_plan`:

```python
async def handle_generate_plan(session: Session, background_tasks: BackgroundTasks, payload: PlanInput) -> dict:
    """
    Bước 2: Validate trạng thái sách, tạo ReadingPlan, tạo processing job,
    kick-off background processing.
    """
    book = session.get(Book, payload.book_id)
    if not book:
        raise BookNotFoundError()
    if book.status not in (BookStatus.DRAFT,):
        raise BookStatusConflictError(f"Sách đang ở trạng thái '{book.status}', không thể tạo plan mới.")

    try:
        plan = ReadingPlan(
            book_id=payload.book_id,
            mode=payload.mode,
            pace=payload.pace,
            schedule_config=payload.schedule_config,
            status=PlanStatus.ACTIVE,
        )
        create_reading_plan(session, plan)

        job = ProcessingJob(
            user_id=MOCK_USER_ID,
            book_id=payload.book_id,
            job_type=ProcessingJobType.GENERATE_PLAN,
            status=ProcessingJobStatus.QUEUED,
            mode=payload.mode,
            total_units=book.total_chapters or 0,
            done_units=0,
            progress_percent=0,
            current_step="Đang chờ xử lý sách.",
        )
        create_processing_job(session, job)

        update_book_status(session, payload.book_id, BookStatus.PROCESSING)

        logger.info(f"ReadingPlan created for book {payload.book_id} | mode={payload.mode} | job={job.id}")
    except Exception as e:
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    background_tasks.add_task(run_background_processing, payload.book_id, payload.mode, job.id)

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "job_id": str(job.id),
        "mode": payload.mode,
        "status": job.status,
        "progress_percent": job.progress_percent,
    }
```

Tai sao tao job truoc khi add background task?

- Neu worker chay nhanh, no co row de update.
- Neu response ve FE, FE co `job_id` poll ngay.

Trade-off:

- Neu background task khong bao gio chay do server crash, job se dung o `queued`.
- Phase 2 voi Celery se giai quyet bang retry/queue durable hon.

## 12. Code Change: Worker Update Progress

File: `app/services/workers/book_pipeline.py`

Them import:

```python
import math
from datetime import datetime, timezone

from app.core.constant import BookStatus, ProcessingJobStatus
from app.repositories.processing_job_repo import update_processing_job
```

Sua signature:

```python
async def run_background_processing(book_id: uuid.UUID, mode: str, job_id: uuid.UUID | None = None) -> None:
```

Them helper trong file:

```python
def _update_job(
    job_id: uuid.UUID | None,
    *,
    status: ProcessingJobStatus | None = None,
    progress_percent: int | None = None,
    current_step: str | None = None,
    total_units: int | None = None,
    done_units: int | None = None,
    failed_units: int | None = None,
    error_message: str | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
) -> None:
    if not job_id:
        return
    with Session(engine) as session:
        update_processing_job(
            session,
            job_id,
            status=status,
            progress_percent=progress_percent,
            current_step=current_step,
            total_units=total_units,
            done_units=done_units,
            failed_units=failed_units,
            error_message=error_message,
            started_at=started_at,
            finished_at=finished_at,
        )
```

Sau khi lay `draft_chapters`, update started:

```python
total_units = len(draft_chapters)
partial_threshold = max(1, math.ceil(total_units * 0.5))

_update_job(
    job_id,
    status=ProcessingJobStatus.PROCESSING,
    progress_percent=0,
    current_step="Đang tải và phân tích tài liệu.",
    total_units=total_units,
    done_units=0,
    started_at=datetime.now(timezone.utc),
)
```

Cho doan dispatch tasks, thay `await asyncio.gather(*tasks)` bang:

```python
tasks = []
for draft_chap in draft_chapters:
    raw_text = chapters_map.get(draft_chap.chapter_index, "")
    if not raw_text.strip():
        logger.warning(f"Chapter {draft_chap.chapter_index + 1} '{draft_chap.title}' không có text — bỏ qua.")
        continue
    tasks.append(
        asyncio.create_task(
            process_chapter(
                book_id,
                book.title,
                draft_chap.title,
                draft_chap.id,
                draft_chap.chapter_index,
                raw_text,
                mode,
            )
        )
    )

completed = 0
for task in asyncio.as_completed(tasks):
    await task
    completed += 1
    progress = int(completed * 100 / total_units) if total_units else 100
    job_status = ProcessingJobStatus.PARTIAL_READY if completed >= partial_threshold and completed < total_units else ProcessingJobStatus.PROCESSING

    with Session(engine) as session:
        if completed >= partial_threshold:
            update_book_status(session, book_id, BookStatus.PARTIAL_READY)

    _update_job(
        job_id,
        status=job_status,
        progress_percent=progress,
        current_step=f"Đã xử lý {completed}/{total_units} chương.",
        done_units=completed,
    )
```

Sau khi xong het:

```python
with Session(engine) as session:
    update_book_status(session, book_id, BookStatus.READY)

_update_job(
    job_id,
    status=ProcessingJobStatus.READY,
    progress_percent=100,
    current_step="Sách đã xử lý xong.",
    done_units=total_units,
    finished_at=datetime.now(timezone.utc),
)
```

Trong `except`:

```python
except Exception as e:
    with Session(engine) as session:
        update_book_status(session, book_id, BookStatus.ERROR, str(e))
    _update_job(
        job_id,
        status=ProcessingJobStatus.ERROR,
        current_step="Xử lý sách thất bại.",
        error_message=str(e),
        finished_at=datetime.now(timezone.utc),
    )
    logger.error(f"LỖI XỬ LÝ SÁCH {book_id}: {e}")
```

Tai sao dung `asyncio.as_completed` thay vi `gather`?

- `gather` chi biet khi tat ca xong hoac loi.
- `as_completed` cho phep update progress moi khi 1 chapter xong.

Trade-off:

- Code dai hon.
- Neu mot chapter fail, job co the chuyen error ngay. Phase sau co the them partial failure/retry tung chapter.

## 13. Code Change: Switch Mode Tao Job

File: `app/schemas/responses/audiobook_res.py`

Sua `SwitchModeResponse`:

```python
class SwitchModeResponse(BaseModel):
    """DTO cho response của POST /books/{id}/switch-mode."""

    message: str
    needs_generation: bool
    job_id: uuid.UUID | None = None
    status: str | None = None
    progress_percent: int | None = None
```

File: `app/services/audiobook_service.py`

Them import:

```python
from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType
from app.models.db_models import Book, Chapter, ChapterSegment, ProcessingJob, ReadingPlan
from app.repositories.processing_job_repo import create_processing_job
```

Khi `needs_generation`, tao job:

```python
job = ProcessingJob(
    user_id=user_id,
    book_id=book_id,
    job_type=ProcessingJobType.SWITCH_MODE,
    status=ProcessingJobStatus.QUEUED,
    mode=PlanMode(payload_mode),
    total_units=book.total_chapters or 0,
    done_units=0,
    progress_percent=0,
    current_step=f"Đang chờ sinh audio mode {payload_mode}.",
)
create_processing_job(session, job)
background_tasks.add_task(run_switch_mode_processing, book_id, payload_mode, job.id)

return {
    "message": f"Đã chuyển sang mode {payload_mode}. Hệ thống đang sinh audio trong background.",
    "needs_generation": True,
    "job_id": job.id,
    "status": job.status,
    "progress_percent": job.progress_percent,
}
```

Voi case da co audio:

```python
return {
    "message": f"Đã chuyển sang mode {payload_mode}. Audio đã có sẵn.",
    "needs_generation": False,
    "job_id": None,
    "status": None,
    "progress_percent": None,
}
```

## 14. Code Change: Switch Mode Worker Progress

File: `app/services/workers/book_pipeline.py`

Sua signature:

```python
async def run_switch_mode_processing(book_id: uuid.UUID, new_mode: str, job_id: uuid.UUID | None = None) -> None:
```

Trong function, sau khi lay `chapters`:

```python
total_units = len(chapters)
partial_threshold = max(1, math.ceil(total_units * 0.5))
_update_job(
    job_id,
    status=ProcessingJobStatus.PROCESSING,
    progress_percent=0,
    current_step=f"Đang sinh audio mode {new_mode}.",
    total_units=total_units,
    done_units=0,
    started_at=datetime.now(timezone.utc),
)
```

Thay `await asyncio.gather(*tasks)` bang:

```python
completed = 0
for task in asyncio.as_completed(tasks):
    await task
    completed += 1
    progress = int(completed * 100 / total_units) if total_units else 100
    job_status = ProcessingJobStatus.PARTIAL_READY if completed >= partial_threshold and completed < total_units else ProcessingJobStatus.PROCESSING

    _update_job(
        job_id,
        status=job_status,
        progress_percent=progress,
        current_step=f"Đã sinh audio mode {new_mode} cho {completed}/{total_units} chương.",
        done_units=completed,
    )
```

Sau khi xong:

```python
_update_job(
    job_id,
    status=ProcessingJobStatus.READY,
    progress_percent=100,
    current_step=f"Đã sinh xong audio mode {new_mode}.",
    done_units=total_units,
    finished_at=datetime.now(timezone.utc),
)
```

Trong `except`:

```python
_update_job(
    job_id,
    status=ProcessingJobStatus.ERROR,
    current_step=f"Sinh audio mode {new_mode} thất bại.",
    error_message=str(e),
    finished_at=datetime.now(timezone.utc),
)
```

## 15. Important Bug Risk: `total_units` Va Skipped Chapter

Trong worker hien tai, neu chapter khong co text thi code skip. Neu `total_units = len(draft_chapters)` nhung skip 1 chapter, progress co the khong dat 100.

Fix tot hon:

```python
processable_chapters = []
for draft_chap in draft_chapters:
    raw_text = chapters_map.get(draft_chap.chapter_index, "")
    if raw_text.strip():
        processable_chapters.append((draft_chap, raw_text))
    else:
        logger.warning(f"Chapter {draft_chap.chapter_index + 1} không có text — bỏ qua.")

total_units = len(processable_chapters)
```

Neu `total_units == 0`, mark error:

```python
if total_units == 0:
    with Session(engine) as session:
        update_book_status(session, book_id, BookStatus.ERROR, "Không có chương nào có nội dung để xử lý.")
    _update_job(
        job_id,
        status=ProcessingJobStatus.ERROR,
        progress_percent=0,
        current_step="Không có chương nào có nội dung để xử lý.",
        error_message="Không có chương nào có nội dung để xử lý.",
        finished_at=datetime.now(timezone.utc),
    )
    return
```

Tai sao can:

- Progress phai len 100 khi cac unit xu ly duoc da xong.
- Neu khong, FE se bi ket o 80-90%.

## 16. Tests Nen Them

File moi: `tests/test_processing_jobs_api.py`

```python
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import ProcessingJobStatus, ProcessingJobType
from app.main import app
from app.models.db_models import ProcessingJob


def test_get_job_status_returns_job(session: Session):
    client = TestClient(app)
    user_id = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")
    job = ProcessingJob(
        user_id=user_id,
        book_id=None,
        job_type=ProcessingJobType.GENERATE_PLAN,
        status=ProcessingJobStatus.PROCESSING,
        progress_percent=25,
        current_step="Testing progress",
        total_units=4,
        done_units=1,
    )
    session.add(job)
    session.commit()
    session.refresh(job)

    response = client.get(f"/api/v1/jobs/{job.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == str(job.id)
    assert body["progress_percent"] == 25
    assert body["status"] == "processing"
```

Ghi chu:

- Test project hien tai co fixture DB rieng hay khong thi can align lai.
- Neu chua co fixture `session`, viet test theo pattern test hien tai trong repo.

Manual test:

```powershell
uv run ruff check app tests
uv run pytest tests/test_processing_jobs_api.py -q
uv run alembic upgrade head
```

## 17. FE Contract De Gui Cho Frontend

### POST `/api/v1/generate-plan`

Response moi:

```json
{
  "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
  "book_id": "uuid",
  "job_id": "uuid",
  "mode": "full",
  "status": "queued",
  "progress_percent": 0
}
```

### GET `/api/v1/jobs/{job_id}`

```json
{
  "id": "uuid",
  "book_id": "uuid",
  "job_type": "generate_plan",
  "status": "processing",
  "progress_percent": 35,
  "current_step": "Đã xử lý 3/10 chương.",
  "total_units": 10,
  "done_units": 3,
  "failed_units": 0,
  "error_message": null
}
```

### GET `/api/v1/books/{book_id}/processing-status`

Tra ve latest job cua book. Dung khi FE reload va khong con `job_id`.

## 18. FE Behavior

Mapping:

```text
queued        -> show 0%, "Dang cho xu ly"
processing    -> show progress bar
partial_ready -> unlock listen button, van show progress tiep
ready         -> hide loading/progress, show full audio
error         -> show error + retry option
cancelled     -> show cancelled
```

Polling interval:

- 2 giay khi dang o man hinh processing.
- 5-10 giay khi user da vao man nghe.
- Stop polling khi `ready/error/cancelled`.

## 19. Tai Sao Phase 1 Chua Dung Celery?

Vi em dang la fresher va project dang co nhieu thu can clean. Neu dua Celery ngay:

- Phai them Redis local/deploy.
- Phai them worker process.
- Phai sua deployment HuggingFace.
- Phai debug queue/task/import path.

Phase 1 cho minh hoc dung concept truoc:

- Job model.
- Progress state.
- Polling contract.
- Worker update milestone.

Sau do Phase 2 chi thay execution engine:

```text
BackgroundTasks.add_task(...)
```

thanh:

```text
celery_task.delay(...)
```

DB/FE contract van giu.

## 20. Trade-off Summary

| Decision | Loi ich | Trade-off |
| --- | --- | --- |
| DB progress table | Reload app van xem duoc progress, debug de | Them migration/table |
| Polling endpoint | De implement, on dinh voi mobile | Co request lap lai |
| `as_completed` | Update progress theo chapter xong | Code worker dai hon |
| `partial_ready` | User nghe som hon | Can FE handle playlist dang grow |
| Chua Celery o Phase 1 | Hoc tu tu, it rui ro deploy | Server restart van co the mat task dang chay |

## 21. Checklist Truoc Khi Implement

- Backup DB local neu can.
- Kiem tra enum `PlanMode` trong migration cu dang luu value nao.
- Tao migration bang Alembic, khong sua DB bang tay.
- Implement endpoint job truoc.
- Implement generate-plan progress truoc.
- Test FE progress bar.
- Sau do moi them switch-mode progress.

## 22. Checklist Sau Khi Implement

- `POST /generate-plan` tra `job_id`.
- `GET /jobs/{job_id}` tra 200.
- Progress tang khi tung chapter xong.
- Book chuyen `partial_ready` khi dat nguong.
- Book chuyen `ready` khi xong het.
- Neu worker loi, job chuyen `error`.
- FE reload app van lay duoc latest status bang `book_id`.
- Ruff va test pass.
