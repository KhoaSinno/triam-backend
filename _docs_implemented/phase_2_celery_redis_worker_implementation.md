# Phase 2 Implementation Guide - Celery + Redis Worker Queue

Muc tieu Phase 2: chuyen `generate-plan` va `switch-mode` tu `FastAPI BackgroundTasks` sang **Celery + Redis**, nhung van giu **DB progress + polling endpoint** cua Phase 1 lam source of truth.

Sau Phase 2:

```text
FE POST /generate-plan
-> BE tao ReadingPlan + ProcessingJob
-> BE enqueue Celery task vao Redis
-> BE tra response ngay cho FE
-> Celery worker lay task va xu ly book
-> Worker update processing_jobs trong Postgres
-> FE poll /jobs/{job_id}
```

## 1. Tai Sao Can Phase 2?

`FastAPI BackgroundTasks` chi song chung voi request/app process. Neu server restart, deploy lai, worker bi kill, task dang chay co the mat.

Celery + Redis giai quyet:

- API tra response nhanh hon, khong om workflow nang trong web process.
- Worker co process rieng de xu ly LLM/TTS/RAG.
- Co queue rieng cho document/LLM/TTS/notification sau nay.
- Co nen tang de them retry, rate limit, Celery Beat reminder.
- Worker down thi job van co the nam trong queue, cho worker len lai xu ly.

Trade-off:

- Them Redis dependency.
- Local dev phai chay them Redis + Celery worker.
- Deploy HuggingFace can external Redis hoac chay them process worker trong container.
- Retry toan bo book chua nen bat manh neu idempotency segment/audio chua that tot.

## 2. Kien Truc Phase 2

```text
FastAPI process
  - validate request
  - create DB rows
  - enqueue Celery task
  - return job_id

Redis
  - broker queue
  - short-lived task metadata

Celery worker process
  - run_background_processing(book_id, mode, job_id)
  - run_switch_mode_processing(book_id, mode, job_id)
  - update DB progress

Postgres/Supabase DB
  - source of truth: books, chapters, processing_jobs
```

Rule quan trong:

- Khong dua SQLModel object vao Celery task.
- Chi dua primitive JSON: string UUID, mode string.
- Worker tu mo DB session qua code pipeline hien tai.
- FE khong doc Celery result backend. FE chi doc `processing_jobs`.

## 3. Install Dependencies

Chay:

```powershell
uv add "celery[redis]>=5.5.0" "redis>=5.2.0"
```

Sau lenh nay, `pyproject.toml` se co them:

```toml
dependencies = [
    ...
    "celery[redis]>=5.5.0",
    "redis>=5.2.0",
]
```

Tai sao can ca `celery[redis]` va `redis`?

- `celery[redis]` keo dependency Redis transport cho Celery/Kombu.
- `redis` client huu ich cho healthcheck/manual ping neu can.

Trade-off:

- Tang dependency va thoi gian build.
- Doi lai co hang doi task dung nghia.

## 4. Redis Cloud Setup - Recommended

Anh recommend dung **Redis Cloud/external Redis** cho Phase 2, dac biet vi BE cua em dang deploy tren HuggingFace Space. HuggingFace khong phai moi truong ly tuong de tu host Redis ben trong container, vi Redis se mat du lieu khi container restart va kho scale/debug hon.

### 4.1 Goi Free 30MB Co Du Khong?

Voi cach minh thiet ke Phase 2, **30MB RAM Redis Cloud la du cho capstone/dev demo**, neu thoa cac dieu kien:

- Redis chi lam **Celery broker**.
- Celery task args chi la string nho: `book_id`, `mode`, `job_id`.
- Khong dua text chapter, PDF bytes, audio bytes, LLM response vao Redis.
- Khong dung Redis result backend cho book jobs.
- FE doc progress tu Postgres `processing_jobs`, khong doc Celery result.
- Worker concurrency thap: 1-2 worker cho queue `document`.

Uoc tinh:

```text
1 Celery message voi payload UUID/mode/job_id thuong chi vai KB.
30MB co the chua hang nghin message nho neu khong luu results.
```

Nhung **30MB se khong du** neu:

- Bat Celery result backend va khong expire ket qua.
- Gui raw text chapter/PDF/audio vao task payload.
- Queue ton hang nghin job lon.
- Chay nhieu queue reminder/notification tan suat cao.
- De task bi ket lau, worker down nhung user tiep tuc enqueue rat nhieu.

Ket luan:

- **Capstone/dev:** Redis Cloud free 30MB du.
- **Neu gap memory eviction/queue day:** chuyen sang Docker local khi dev, hoac nang Redis Cloud.
- **Production that:** dung Redis Cloud paid nho hoac managed Redis co RAM cao hon.

### 4.2 Security Note

Em da paste Redis password vao chat. Credential nay nen xem nhu da lo.

Viec can lam:

1. Vao Redis Cloud rotate/regenerate password.
2. Khong commit password vao git.
3. Chi dat password trong `.env`, HuggingFace Secrets, hoac environment variables.
4. Trong markdown/code example chi dung placeholder `<redis-password>`.

### 4.3 Redis Cloud Connection URL

Redis Cloud info cua em:

```text
host = redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com
port = 19459
username = default
region = AWS Singapore
```

Celery broker URL dang:

```env
CELERY_BROKER_URL=redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
```

Neu password co ky tu dac biet nhu `@`, `/`, `:`, `#`, `?`, can URL encode password truoc khi dat vao URL.

Vi du Python encode:

```python
from urllib.parse import quote

password = "your-raw-password"
print(quote(password, safe=""))
```

### 4.4 Quick Healthcheck

Khong hardcode secret trong source. Test bang env:

```powershell
$env:CELERY_BROKER_URL = "redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0"
uv run python - <<'PY'
import os
from redis import Redis
from urllib.parse import urlparse

url = os.environ["CELERY_BROKER_URL"]
r = Redis.from_url(url, decode_responses=True)
print(r.ping())
PY
```

Expected:

```text
True
```

## 4B. Docker Redis Fallback For Local Dev

Chi dung Docker Redis neu:

- Redis Cloud bi day 30MB.
- Mang toi cloud cham/khong on dinh.
- Em muon dev offline.
- Em muon test nhieu job ma khong anh huong cloud free quota.

Neu co Docker:

```powershell
docker run --name triam-redis -p 6379:6379 -d redis:7-alpine
```

Check Redis:

```powershell
docker exec -it triam-redis redis-cli ping
```

Expected:

```text
PONG
```

Docker `.env`:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
```

## 5. Environment Variables

File: `.env`

Them:

```env
CELERY_BROKER_URL=redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
CELERY_RESULT_BACKEND=
CELERY_TASK_ALWAYS_EAGER=false
CELERY_TASK_EAGER_PROPAGATES=false
CELERY_WORKER_PREFETCH_MULTIPLIER=1
CELERY_DOCUMENT_CONCURRENCY=1
```

Production/HuggingFace:

```env
CELERY_BROKER_URL=redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
CELERY_RESULT_BACKEND=
ENABLE_CELERY_WORKER=true
```

Tai sao `CELERY_RESULT_BACKEND` de rong?

- FE khong can Celery result.
- Worker update tien do vao Postgres `processing_jobs`.
- Tat result backend giup tiet kiem RAM Redis Cloud 30MB.

Neu provider bat TLS, URL co the la `rediss://...`. Redis Cloud sample cua em dang dung plain `redis://` host/port. Neu Redis Cloud dashboard bat TLS-only thi phai doi sang `rediss://` va test lai.

## 6. Code Change: Config

File: `app/core/config.py`

Them vao `Settings`:

```python
    # Celery / Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str | None = None
    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_EAGER_PROPAGATES: bool = False
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
    CELERY_DOCUMENT_CONCURRENCY: int = 1
```

Tai sao `worker_prefetch_multiplier=1`?

- Document/LLM/TTS task rat nang.
- Neu worker prefetch nhieu task, mot worker co the giu task qua lau trong RAM/queue ownership.
- `1` giup fair hon, de debug hon.

Trade-off:

- Throughput co the thap hon.
- Nhung an toan hon cho capstone va task nang.

## 7. Code Change: Celery App

File moi: `app/core/celery_app.py`

```python
from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "triam",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND or None,
    include=["app.tasks.book_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_ignore_result=True,
    task_acks_late=True,
    result_expires=3600,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    broker_connection_retry_on_startup=True,
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_TASK_EAGER_PROPAGATES,
    broker_transport_options={
        "visibility_timeout": 3600,
        "socket_keepalive": True,
        "health_check_interval": 30,
    },
    task_routes={
        "triam.books.process": {"queue": "document"},
        "triam.books.switch_mode": {"queue": "document"},
    },
)
```

Tai sao `task_ignore_result=True`?

- Redis Cloud free chi 30MB.
- Celery results khong phai source of truth cua minh.
- Tat result giup Redis chi giu queue/control metadata ngan han.

Tai sao timezone UTC?

- DB timestamp nen luu UTC.
- Reminder Phase sau moi convert theo timezone user.
- Giam bug gio mua he/timezone.

Tai sao `task_acks_late=True`?

- Worker chi ack task sau khi task chay xong.
- Neu worker chet giua chung, broker co co hoi dua task lai cho worker khac.

Trade-off:

- Task co the bi chay lai neu worker chet sau khi da tao mot phan output.
- Vi vay idempotency la bat buoc o cac phase tiep theo.

## 8. Code Change: Tasks Package

Tao folder/file:

```text
app/tasks/__init__.py
app/tasks/book_tasks.py
```

File: `app/tasks/__init__.py`

```python
"""Celery task modules for Triam."""
```

File: `app/tasks/book_tasks.py`

```python
import asyncio
import uuid

from app.core.celery_app import celery_app
from app.core.logger import log
from app.services.workers.book_pipeline import run_background_processing, run_switch_mode_processing


@celery_app.task(name="triam.books.process")
def process_book_task(book_id: str, mode: str, job_id: str) -> None:
    """
    Celery wrapper for initial book processing.

    Args are strings to keep Celery JSON serialization simple.
    DB state is updated by the pipeline itself.
    """
    log.info(f"Celery process_book_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    asyncio.run(
        run_background_processing(
            uuid.UUID(book_id),
            mode,
            uuid.UUID(job_id),
        )
    )


@celery_app.task(name="triam.books.switch_mode")
def switch_mode_task(book_id: str, mode: str, job_id: str) -> None:
    """
    Celery wrapper for switch-mode audio generation.
    """
    log.info(f"Celery switch_mode_task started | book_id={book_id} | mode={mode} | job_id={job_id}")
    asyncio.run(
        run_switch_mode_processing(
            uuid.UUID(book_id),
            mode,
            uuid.UUID(job_id),
        )
    )
```

Tai sao wrapper sync goi `asyncio.run`?

- Celery task function mac dinh la sync.
- Pipeline hien tai la async vi goi LLM/TTS async.
- `asyncio.run(...)` la cach don gian nhat cho Phase 2.

Trade-off:

- Neu sau nay worker dung event loop phuc tap hon, co the tach pipeline thanh sync task orchestration hoac dung async worker strategy rieng.
- Phase 2 giu don gian de hoc va deploy duoc.

## 9. Code Change: Generate Plan Enqueue Celery

File: `app/services/upload_service.py`

Bo import:

```python
from fastapi import BackgroundTasks, UploadFile
from app.services.workers.book_pipeline import run_background_processing
```

Thanh:

```python
from fastapi import UploadFile
from app.tasks.book_tasks import process_book_task
```

Them import:

```python
from app.core.exceptions import ExternalServiceError
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
```

Sua signature:

```python
async def handle_generate_plan(session: Session, payload: PlanInput) -> dict:
```

Thay doan:

```python
background_tasks.add_task(run_background_processing, payload.book_id, payload.mode.value, job.id)
```

Bang:

```python
    try:
        process_book_task.apply_async(
            args=[str(payload.book_id), payload.mode.value, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step="Không thể đưa sách vào hàng đợi xử lý.",
            error_message=str(e),
        )
        update_book_status(session, payload.book_id, BookStatus.ERROR, "Không thể đưa sách vào hàng đợi xử lý.")
        raise ExternalServiceError("Không thể đưa sách vào hàng đợi xử lý. Vui lòng thử lại sau.") from e
```

Full function sau khi sua:

```python
async def handle_generate_plan(session: Session, payload: PlanInput) -> dict:
    """
    Validate trạng thái sách, tạo ReadingPlan, tạo progress job,
    enqueue Celery processing task.
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
        logger.info(f"ReadingPlan created for book {payload.book_id} | mode={payload.mode.value} | job={job.id}")
    except Exception as e:
        logger.error(f"Failed to create reading plan: {e}")
        raise DatabaseError(f"Lỗi lưu ReadingPlan: {str(e)}") from e

    try:
        process_book_task.apply_async(
            args=[str(payload.book_id), payload.mode.value, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step="Không thể đưa sách vào hàng đợi xử lý.",
            error_message=str(e),
        )
        update_book_status(session, payload.book_id, BookStatus.ERROR, "Không thể đưa sách vào hàng đợi xử lý.")
        raise ExternalServiceError("Không thể đưa sách vào hàng đợi xử lý. Vui lòng thử lại sau.") from e

    return {
        "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
        "book_id": str(payload.book_id),
        "job_id": str(job.id),
        "mode": payload.mode.value,
        "status": job.status,
        "progress_percent": job.progress_percent,
    }
```

Tai sao enqueue sau khi commit DB?

- Worker can tim thay `Book`, `Chapter`, `ProcessingJob` trong DB.
- Neu enqueue truoc commit, worker co the chay nhanh va khong thay row.

Trade-off:

- Neu DB commit xong nhung Redis enqueue fail, job se bi mark error.
- Day la dung: FE thay loi ro thay vi job ket `queued` vo han.

## 10. Code Change: Upload Router

File: `app/api/v1/routers/upload.py`

Bo `BackgroundTasks` import va parameter.

Before:

```python
from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile
...
async def generate_plan(
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
):
    return await handle_generate_plan(session, background_tasks, payload)
```

After:

```python
from fastapi import APIRouter, Body, Depends, File, UploadFile
...
async def generate_plan(
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
):
    return await handle_generate_plan(session, payload)
```

## 11. Code Change: Switch Mode Enqueue Celery

File: `app/services/audiobook_service.py`

Bo:

```python
from fastapi import BackgroundTasks
from app.services.workers.book_pipeline import run_switch_mode_processing
```

Them:

```python
from app.core.exceptions import ExternalServiceError
from app.repositories.processing_job_repo import create_processing_job, update_processing_job
from app.tasks.book_tasks import switch_mode_task
```

Sua signature:

```python
def switch_book_mode(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    payload_mode: str,
) -> dict:
```

Them helper:

```python
def _enqueue_switch_mode_job(session: Session, book_id: uuid.UUID, mode: str, job: ProcessingJob) -> None:
    try:
        switch_mode_task.apply_async(
            args=[str(book_id), mode, str(job.id)],
            queue="document",
        )
    except Exception as e:
        update_processing_job(
            session,
            job.id,
            status=ProcessingJobStatus.ERROR,
            current_step=f"Không thể đưa tác vụ switch mode {mode} vào hàng đợi.",
            error_message=str(e),
        )
        raise ExternalServiceError("Không thể đưa tác vụ đổi mode vào hàng đợi xử lý. Vui lòng thử lại sau.") from e
```

Thay cac doan:

```python
background_tasks.add_task(run_switch_mode_processing, book_id, requested_mode_value, job.id)
```

Bang:

```python
_enqueue_switch_mode_job(session, book_id, requested_mode_value, job)
```

## 12. Code Change: Audiobooks Router

File: `app/api/v1/routers/audiobooks.py`

Bo import:

```python
from fastapi import APIRouter, BackgroundTasks, Depends
```

Thanh:

```python
from fastapi import APIRouter, Depends
```

Sua endpoint:

```python
@router.post("/books/{book_id}/switch-mode", response_model=SwitchModeResponse)
def switch_book_mode_endpoint(
    book_id: uuid.UUID,
    payload: SwitchModeRequest,
    session: Annotated[Session, Depends(get_session)],
):
    """Đổi mode đang active và sinh audio mới nếu mode này chưa từng được gen."""
    return switch_book_mode(session, book_id, MOCK_USER_ID, payload.mode)
```

## 13. Run Commands Local

Terminal 1 - Redis:

Voi Redis Cloud, khong can chay Redis local. Chi can set env:

```powershell
$env:CELERY_BROKER_URL = "redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0"
```

Terminal 2 - FastAPI:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 3 - Celery worker tren Windows:

```powershell
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo
```

Terminal 3 - Celery worker tren Linux/Docker:

```bash
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --concurrency="${CELERY_DOCUMENT_CONCURRENCY:-1}"
```

Tai sao Windows dung `--pool=solo`?

- Celery prefork khong than thien tren Windows.
- `solo` cham hon nhung de debug local.

Trade-off:

- Windows local chi xu ly 1 task/worker.
- Production Linux co the dung concurrency > 1.

## 14. HuggingFace Deployment Note

HuggingFace Space hien tai dang chay `start.sh` gom FastAPI va LiveKit voice worker. Phase 2 can them Celery worker process.

Option A - Cung container, external Redis:

File: `start.sh`

Them truoc uvicorn:

```bash
if [ "${ENABLE_CELERY_WORKER:-true}" = "true" ]; then
  uv run celery -A app.core.celery_app.celery_app worker \
    -Q document \
    -l info \
    --concurrency "${CELERY_DOCUMENT_CONCURRENCY:-1}" \
    > celery_document.log 2>&1 &
fi
```

Can set env tren HuggingFace:

```env
CELERY_BROKER_URL=<external redis url>
CELERY_RESULT_BACKEND=
ENABLE_CELERY_WORKER=true
```

Option B - Tach worker ra service rieng:

- FastAPI Space chi serve API.
- Worker chay o VM/Render/Railway/Fly.io.
- Redis external dung chung.

Anh khuyen:

- Capstone nhanh: Option A.
- Production that: Option B.

Trade-off Option A:

- De deploy mot noi.
- Nhung CPU/RAM Space bi chia cho API, voice agent, Celery worker.
- Neu job nang, API co the cham.

Trade-off Option B:

- Sach kien truc hon.
- Nhung tang do phuc tap deployment.

## 15. Testing Strategy

### 15.1 Unit/API Test Khong Can Redis That

Mock `process_book_task.apply_async` de check API co enqueue dung.

File: `tests/test_generate_plan_enqueue.py`

```python
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.constant import BookStatus, DocumentType
from app.db.database import engine
from app.main import app
from app.models.db_models import Book, Chapter


MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")


def test_generate_plan_enqueues_celery(monkeypatch):
    calls = []

    def fake_apply_async(*, args, queue):
        calls.append({"args": args, "queue": queue})

    monkeypatch.setattr("app.services.upload_service.process_book_task.apply_async", fake_apply_async)

    with Session(engine) as session:
        book = Book(
            user_id=MOCK_USER_ID,
            title="Celery Test Book",
            total_chapters=1,
            status=BookStatus.DRAFT,
            document_type=DocumentType.PDF,
            file_url="https://example.test/raw_books/book/original.pdf",
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        chapter = Chapter(book_id=book.id, chapter_index=0, title="Chapter 1", status=BookStatus.DRAFT)
        session.add(chapter)
        session.commit()
        book_id = book.id

    client = TestClient(app)
    response = client.post(
        "/api/v1/generate-plan",
        json={"book_id": str(book_id), "mode": "full", "pace": 1, "schedule_config": ["Mon"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["job_id"]
    assert body["status"] == "queued"
    assert calls
    assert calls[0]["queue"] == "document"
    assert calls[0]["args"][0] == str(book_id)
    assert calls[0]["args"][1] == "full"

    with Session(engine) as session:
        saved = session.get(Book, book_id)
        if saved:
            session.delete(saved)
            session.commit()
```

### 15.2 Manual Test Co Redis + Worker

1. Start Redis.
2. Start Celery worker.
3. Start FastAPI.
4. Upload `Chương 4_ Phương pháp luận nghiên cứu.pdf`.
5. POST `/generate-plan`.
6. Poll `/jobs/{job_id}`.
7. Confirm worker terminal co log task.
8. Confirm progress chuyen:

```text
queued -> processing -> partial_ready -> ready
```

Neu khong muon dot LLM/TTS:

- Mock LLM/TTS trong test script nhu Phase 1.
- Hoac dung file rat nho va test 1 chapter.

## 16. Monitoring Va Debug

Lenh xem Redis Cloud co connect duoc:

```powershell
uv run python - <<'PY'
import os
from redis import Redis

r = Redis.from_url(os.environ["CELERY_BROKER_URL"], decode_responses=True)
print(r.ping())
PY
```

Lenh inspect Celery:

```powershell
uv run celery -A app.core.celery_app.celery_app inspect active
uv run celery -A app.core.celery_app.celery_app inspect reserved
uv run celery -A app.core.celery_app.celery_app inspect scheduled
```

Flower optional:

```powershell
uv add flower
uv run celery -A app.core.celery_app.celery_app flower --port=5555
```

Trade-off:

- Flower de nhin task truc quan.
- Nhung them dependency, co the de sau.

## 17. Retry Policy Trong Phase 2

Khong nen bat retry toan bo book qua manh ngay.

Ly do:

- Pipeline hien co co the da tao mot phan audio/segments.
- Retry toan bo book khi idempotency chua hoan hao co the tao duplicate storage/object hoac conflict DB.
- Phase 1 da co unique constraints, nhung storage/audio path va rollback van can review them.

Phase 2 recommended:

- Celery de tach worker va queue durable hon.
- Chua autoretry toan bo book.
- Neu task loi, pipeline mark `processing_jobs.status = error`.
- FE hien retry button sau.

Phase 3 moi them:

- Retry tung chapter.
- Idempotency per chapter/mode.
- Resume job tu chapter chua ready.
- External provider retry voi backoff o LLM/TTS/storage layer.

## 18. Common Errors

### Redis connection refused

Symptom:

```text
Error 10061 connecting to localhost:6379
```

Fix:

Neu dung Redis Cloud, loi nay thuong la app van dang doc default `redis://localhost:6379/0`.

Check `.env`/HuggingFace Secrets:

```env
CELERY_BROKER_URL=redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
```

Neu dung Docker fallback thi moi can:

```powershell
docker start triam-redis
```

### Redis maxmemory / OOM

Neu Redis Cloud 30MB bi day:

- Dam bao `task_ignore_result=True`.
- Dam bao `CELERY_RESULT_BACKEND=` rong.
- Khong day raw document/text/audio vao Celery args.
- Giam enqueue job dong thoi.
- Xoa queue test cu neu can.
- Hoac chuyen sang Docker local/upgrade Redis Cloud.

### Worker khong nhan task

Check worker co dung queue khong:

```powershell
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo
```

Neu task route vao queue `document` ma worker khong listen `document`, task se nam im trong Redis.

### Task import error

Check:

```powershell
uv run python -c "from app.tasks.book_tasks import process_book_task; print(process_book_task.name)"
```

Expected:

```text
triam.books.process
```

### Job queued forever

Nguyen nhan:

- Worker chua chay.
- Worker nghe sai queue.
- Redis URL sai.
- Task import fail.

Fix:

- Check Celery worker log.
- Poll `/api/v1/jobs/{job_id}`.
- Inspect Redis/Celery active/reserved.

## 19. Checklist Implement Phase 2

- Add dependencies Celery/Redis.
- Add `.env` Celery variables.
- Add `app/core/celery_app.py`.
- Add `app/tasks/book_tasks.py`.
- Remove `BackgroundTasks` from generate-plan flow.
- Remove `BackgroundTasks` from switch-mode flow.
- Enqueue Celery tasks with string UUID args.
- Keep `processing_jobs` progress contract unchanged.
- Run Redis + Celery worker local.
- Test generate-plan returns `job_id`.
- Test Celery worker receives task.
- Poll `/jobs/{job_id}` and confirm progress changes.

## 20. Trade-off Summary

| Decision | Loi ich | Trade-off |
| --- | --- | --- |
| Celery + Redis Cloud | Tach task nang khoi web process, deploy HF de hon | Phu thuoc network/cloud quota |
| Tat Celery result backend | Tiet kiem RAM Redis 30MB | Khong xem task result tu Redis, dung DB progress thay the |
| DB progress source of truth | FE reload van biet progress | Phai update DB milestone |
| Queue `document` rieng | Worker xu ly sach khong chan API | Can command worker dung queue |
| `acks_late=True` | Worker chet co the re-deliver task | Task phai idempotent hon |
| Chua autoretry book | Giam duplicate/side effect | Loi transient co the can user retry |
| Windows `--pool=solo` | De dev local | Cham, 1 task/luc |

## 21. Next Phase Sau Phase 2

Phase 3 nen lam:

1. Token estimation + soft/hard chapter limit.
2. Idempotency/resume per chapter/mode.
3. Retry tung external call voi backoff.
4. Notification outbox.
5. Celery Beat scan reminders/spaced review.
