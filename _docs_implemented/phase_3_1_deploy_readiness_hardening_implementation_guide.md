# Phase 3.1 Implementation Guide - Deploy Readiness And Background Worker Hardening

Date: 2026-05-22

Status: **Plan/implementation instruction, not implemented yet**

## 1. Tóm Tắt Cho Em

Phase 3 hiện tại đã chạy được local:

```text
t1: FastAPI
t2: Celery document worker
t3: Realtime voice agent
```

Khi deploy HuggingFace Docker Space, `Dockerfile` hiện có:

```dockerfile
CMD ["./start.sh"]
```

Nghĩa là Space sẽ chạy `start.sh`. Nếu HuggingFace Secrets/Variables có đủ `.env`, `start.sh` có thể chạy:

```text
voice agent
Celery document worker
FastAPI
```

Tuy nhiên, trước khi deploy Phase 3 lên server, anh khuyên làm Phase 3.1 để **harden deploy**, không thêm feature mới.

Phase 4 là feature mới:

```text
Notification Outbox + Celery Beat + Spaced Review
```

Phase 3.1 chỉ là:

```text
Làm Phase 3 sạch hơn, dễ deploy hơn, ít lỗi vận hành hơn.
```

## 2. Phase 3 Hiện Đã Có Gì

Đã có:

- Redis Cloud + Celery queue `document`.
- `processing_jobs` để FE poll progress.
- `chapter_processing_states` để theo dõi từng chapter/mode.
- Estimate token/audio trước khi gọi LLM.
- Hard limit để reject chapter quá lớn.
- Chunking cho chapter lớn.
- First playable unlock: chapter đầu có audio thì `partial_ready`.
- TTS phải tạo ít nhất một playable segment, nếu không fail rõ.
- Không xóa `Chapter` khi processing lỗi.
- Log chi tiết hơn cho LLM/TTS/segment.

Local test thực tế đã chạy được:

```text
Book ready
Job ready
3/3 chapters ready
Segments created
```

## 3. Những Trade-off Còn Đáng Lo Trước Deploy

### 3.1 `start.sh` đang dùng `uvicorn --reload`

Hiện tại:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
```

`--reload` tốt cho local dev, nhưng không nên dùng production/deploy vì:

- Nó tạo reload supervisor process.
- Tốn tài nguyên hơn.
- Có thể làm log/process khó hiểu.
- Không cần trên HuggingFace deploy.

Phase 3.1 fix:

- Thêm env `UVICORN_RELOAD=false`.
- Chỉ bật `--reload` khi local dev cần.

### 3.2 Voice agent đang luôn chạy

Hiện tại `start.sh` luôn chạy:

```bash
uv run python -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" > worker.log 2>&1 &
```

Trade-off:

- Nếu deploy chỉ muốn API/upload/generate audio, voice agent vẫn chiếm RAM/CPU.
- Nếu thiếu LiveKit/OpenAI realtime env, voice agent có thể crash liên tục hoặc làm log khó đọc.

Phase 3.1 fix:

- Thêm `ENABLE_VOICE_AGENT=true/false`.
- Chỉ start voice agent nếu env bật.

### 3.3 Worker log bị ghi vào file, HuggingFace log khó thấy

Hiện tại:

```bash
> celery_document.log 2>&1 &
> worker.log 2>&1 &
```

Trade-off:

- Local đọc file thì được.
- Nhưng trên HuggingFace, em thường xem stdout/stderr của container.
- Nếu log nằm trong file, debug deploy khó hơn.

Phase 3.1 fix:

- Với deploy, dùng `tee` để vừa ghi file vừa hiện stdout.
- Hoặc không redirect, để HuggingFace capture trực tiếp.

Recommendation:

```bash
2>&1 | tee celery_document.log &
```

### 3.4 Redis reconnect warning sau task dài

Em đã thấy log:

```text
Task succeeded
Connection to broker lost
Connected lại Redis
```

Hiện tại không làm hỏng job, vì task đã succeeded và DB đã `ready`.

Nhưng trade-off với long-running Celery task:

- Nếu Redis connection mất giữa task, task có thể bị redeliver tùy `acks_late`, visibility timeout và worker behavior.
- Phase 3 đã có idempotency theo chapter/mode, nhưng vẫn nên harden book-level skip.

Phase 3.1 fix:

- Explicit config `worker_cancel_long_running_tasks_on_connection_loss=False` để tránh Celery 6 đổi default bất ngờ.
- Add book/job-level idempotency guard ở task/pipeline start: nếu job đã `ready`, task redeliver thì skip.

### 3.5 DB migration Phase 3 phải có trên server

Phase 3 có migration:

```text
d7a2f4c9b8e1_phase_3_generation_guardrails.py
```

Nếu deploy code mới nhưng DB chưa migrate:

```text
worker/API sẽ lỗi vì thiếu columns/tables mới
```

Phase 3.1 decision:

- Capstone/dev: có thể add `RUN_MIGRATIONS_ON_START=true`.
- Production thật: nên migrate thủ công hoặc CI/CD trước khi start app.

### 3.6 Một HuggingFace Space chạy quá nhiều process

Một Space hiện có thể chạy:

```text
FastAPI
Voice agent
Celery document worker
```

Trade-off:

- Dễ deploy một nơi.
- Nhưng RAM/CPU bị chia sẻ.
- Khi gen audio dài, API/voice có thể chậm.

Phase 3.1 recommendation:

- Capstone/demo: một Space vẫn chấp nhận được.
- Nếu thấy lag/OOM: tách worker sang Space/server riêng.

## 4. Phase 3.1 Mục Tiêu

Sau Phase 3.1:

1. `start.sh` chạy ổn cả local Linux/HuggingFace.
2. Không dùng `--reload` khi deploy.
3. Có thể bật/tắt voice agent bằng env.
4. Celery worker reconnect behavior rõ ràng hơn.
5. Redelivered task không xử lý lại book đã `ready`.
6. Migration strategy rõ ràng trước deploy.
7. Log worker hiện ra được trên HuggingFace.
8. Có checklist deploy Phase 3 cho em làm theo.

Không làm trong Phase 3.1:

- Không thêm Notification Outbox.
- Không thêm Celery Beat.
- Không thêm FCM/push notification.
- Không thay mock user bằng auth thật.

## 5. Code Change 1 - Harden `start.sh`

File:

```text
start.sh
```

Replace current script shape bằng:

```bash
#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  echo "Đang tắt an toàn các tiến trình..."
  kill -TERM $(jobs -p) 2>/dev/null || true
  wait $(jobs -p) 2>/dev/null || true
  echo "Đã tắt xong."
}
trap cleanup INT TERM EXIT

export PYTHONUNBUFFERED=1

if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
  echo "Running Alembic migrations..."
  uv run alembic upgrade head
fi

if [ "${ENABLE_VOICE_AGENT:-true}" = "true" ]; then
  AGENT_MODE="${AGENT_MODE:-start}"
  echo "Starting realtime voice agent..."
  uv run python -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" 2>&1 | tee worker.log &
fi

if [ "${ENABLE_CELERY_WORKER:-false}" = "true" ]; then
  echo "Starting Celery document worker..."
  uv run celery -A app.core.celery_app.celery_app worker \
    -Q document \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_DOCUMENT_CONCURRENCY:-1}" \
    2>&1 | tee celery_document.log &
fi

BACKEND_PORT="${BACKEND_PORT:-8000}"
UVICORN_RELOAD="${UVICORN_RELOAD:-false}"

if [ "$UVICORN_RELOAD" = "true" ]; then
  echo "Starting FastAPI with reload..."
  uv run uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
else
  echo "Starting FastAPI..."
  uv run uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT"
fi
```

Why:

- `set -euo pipefail`: fail rõ khi biến/command lỗi.
- `RUN_MIGRATIONS_ON_START`: tránh quên migration trong capstone.
- `ENABLE_VOICE_AGENT`: deploy API-only dễ hơn.
- `tee`: log hiện trên HuggingFace và vẫn ghi file.
- `UVICORN_RELOAD=false`: production/deploy gọn hơn.

Trade-off:

- `tee` ghi thêm file log, nhưng dễ debug.
- Auto migration tiện cho capstone, nhưng production thật nên dùng CI/CD migration riêng.

## 6. Code Change 2 - Add Config Env

File:

```text
app/core/config.py
```

Add:

```python
    # Runtime process toggles
    ENABLE_VOICE_AGENT: bool = True
    RUN_MIGRATIONS_ON_START: bool = False
    UVICORN_RELOAD: bool = False
    CELERY_LOG_LEVEL: str = "info"

    # Celery durability / reconnect behavior
    CELERY_VISIBILITY_TIMEOUT_SECONDS: int = 3600
    CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS: bool = False
```

File:

```text
.env.example
```

Add:

```env
# Runtime process toggles
ENABLE_VOICE_AGENT=true
RUN_MIGRATIONS_ON_START=false
UVICORN_RELOAD=false
CELERY_LOG_LEVEL=info

# Celery reconnect / long-task behavior
CELERY_VISIBILITY_TIMEOUT_SECONDS=3600
CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS=false
```

For HuggingFace Phase 3 deploy:

```env
BACKEND_PORT=7860
ENABLE_VOICE_AGENT=true
ENABLE_CELERY_WORKER=true
RUN_MIGRATIONS_ON_START=false
UVICORN_RELOAD=false
CELERY_DOCUMENT_CONCURRENCY=1
CELERY_WORKER_PREFETCH_MULTIPLIER=1
CELERY_RESULT_BACKEND=
```

If DB chưa migrate:

```env
RUN_MIGRATIONS_ON_START=true
```

Sau khi migrate xong, nên set lại:

```env
RUN_MIGRATIONS_ON_START=false
```

## 7. Code Change 3 - Harden Celery Config

File:

```text
app/core/celery_app.py
```

Current:

```python
task_acks_late=True
broker_transport_options={
    "visibility_timeout": 3600,
    "socket_keepalive": True,
    "health_check_interval": 30,
}
```

Change to:

```python
celery_app.conf.update(
    ...
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_ignore_result=True,
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    worker_cancel_long_running_tasks_on_connection_loss=(
        settings.CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS
    ),
    broker_connection_retry_on_startup=True,
    broker_transport_options={
        "visibility_timeout": settings.CELERY_VISIBILITY_TIMEOUT_SECONDS,
        "socket_keepalive": True,
        "health_check_interval": 30,
    },
)
```

Why:

- `visibility_timeout` lấy từ config, dễ tune.
- Explicit `worker_cancel_long_running_tasks_on_connection_loss=False` để Celery version mới không đổi behavior bất ngờ.
- `task_reject_on_worker_lost=True` giúp task không bị ack nhầm nếu worker process chết cứng.

Trade-off:

- Nếu worker chết giữa task, task có thể chạy lại.
- Vì vậy phải có idempotency guard ở task/pipeline.

## 8. Code Change 4 - Book/Job-Level Idempotency Guard

Hiện Phase 3 đã có per-chapter/per-mode idempotency. Phase 3.1 nên thêm guard ở đầu task/pipeline.

File:

```text
app/tasks/book_tasks.py
```

Add helper:

```python
def _should_skip_finished_job(job_id: uuid.UUID) -> bool:
    with Session(engine) as session:
        job = session.get(ProcessingJob, job_id)
        return bool(job and job.status == ProcessingJobStatus.READY)
```

In task:

```python
@celery_app.task(name="triam.books.process")
def process_book_task(book_id: str, mode: str, job_id: str) -> None:
    parsed_job_id = uuid.UUID(job_id)
    if _should_skip_finished_job(parsed_job_id):
        log.info(f"Skip process_book_task because job already READY | job_id={job_id}")
        return

    asyncio.run(run_background_processing(...))
```

Same for `switch_mode_task`.

Why:

- Nếu Redis/Celery redeliver task sau reconnect, task đã `ready` sẽ không làm lại.
- Bảo vệ chi phí LLM/TTS.

Alternative:

- Put guard in `run_background_processing()`.
- Anh khuyên làm cả task-level guard và pipeline-level guard nếu muốn chắc nhất.

## 9. Code Change 5 - Pipeline-Level Idempotency Guard

File:

```text
app/services/workers/book_pipeline.py
```

At beginning of `run_background_processing()`:

```python
with Session(engine) as session:
    job = session.get(ProcessingJob, job_id) if job_id else None
    book = session.get(Book, book_id)
    if job and job.status == ProcessingJobStatus.READY:
        logger.info(f"Skip book processing because job already READY | book_id={book_id} | job_id={job_id}")
        return
    if book and book.status == BookStatus.READY:
        logger.info(f"Book already READY at pipeline start | book_id={book_id}")
```

Important:

- Nếu `book.status == READY` nhưng job chưa `READY`, cần cẩn thận. Có thể do status lệch.
- Phase 3.1 nên only hard-skip when `job.status == READY`.

For switch mode:

- Skip only if `job.status == READY`.
- Do not skip only because book is `READY`, because switch mode may legitimately generate new mode for a ready book.

## 10. Code Change 6 - Deploy Health Checks

Optional but recommended before deploy.

Add endpoint:

```text
GET /api/v1/health
```

Response:

```json
{
  "status": "ok",
  "service": "triam-backend"
}
```

Add background readiness endpoint:

```text
GET /api/v1/health/background
```

Response shape:

```json
{
  "redis": "ok",
  "document_queue_length": 0,
  "database": "ok"
}
```

Do not expose secrets.

Trade-off:

- Adds a small router/service.
- Makes deploy debugging much easier.

For HuggingFace, even plain `/api/v1/health` is useful to verify container is alive.

## 11. Code Change 7 - Documentation For Local vs Deploy Commands

Add/update doc:

```text
_docs_implemented/phase_3_fresher_explained_celery_redis_worker.md
```

Include this table:

| Environment | How to run |
| --- | --- |
| Windows local | Run 3 terminals manually |
| Git Bash/WSL local | Can run `./start.sh` |
| HuggingFace Docker Space | Dockerfile runs `./start.sh` |
| Production split services | API process + worker process separately |

Local Windows commands:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo --concurrency 1
uv run python -m app.services.agent_voice_gpt_realtime start
```

HuggingFace:

```text
No manual terminal.
Dockerfile -> CMD ["./start.sh"]
start.sh reads env/secrets and starts needed processes.
```

## 12. HuggingFace Secrets Checklist

Before deploy Phase 3, set at least:

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_ROLE_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
GEMINI_BASE_URL=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
ENABLE_CELERY_WORKER=true
ENABLE_VOICE_AGENT=true
BACKEND_PORT=7860
UVICORN_RELOAD=false
CELERY_DOCUMENT_CONCURRENCY=1
CELERY_WORKER_PREFETCH_MULTIPLIER=1
```

Voice agent also needs:

```env
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
LIVEKIT_AGENT_NAME=
DEEPGRAM_API_KEY=
OPENAI_STREAM_MODEL_NAME=
OPENAI_REALTIME_VOICE=
OPENAI_REALTIME_TRANSCRIPTION_MODEL=
OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE=vi
```

TTS/provider:

```env
EDGE_TTS_VOICE=
CARTESIA_API_KEY_TTS=
ELEVENLABS_API_KEY_TTS=
```

Generation guardrails:

```env
LLM_INPUT_SOFT_TOKEN_LIMIT=12000
LLM_INPUT_HARD_TOKEN_LIMIT=60000
LLM_CHUNK_TARGET_TOKENS=5000
LLM_CHUNK_OVERLAP_TOKENS=300
MAX_ESTIMATED_AUDIO_SECONDS_PER_BOOK=14400
FIRST_PLAYABLE_CHAPTERS=1
CHAPTER_PROCESSING_CONCURRENCY=2
LLM_NORMALIZE_CONCURRENCY=1
TTS_GENERATION_CONCURRENCY=2
EMBEDDING_BATCH_SIZE=64
```

Security:

- Rotate Redis password if it was pasted into chat/log.
- Do not commit `.env`.
- Keep HuggingFace Secrets private.

## 13. Deployment Test Plan

### 13.1 Pre-deploy local checks

```powershell
uv run ruff check app tests
uv run pytest tests\test_phase3_generation_guardrails.py tests\test_celery_enqueue.py tests\test_processing_jobs_api.py -q
uv run alembic current
```

Expected:

```text
DB head includes d7a2f4c9b8e1
```

### 13.2 Deploy smoke test

After HuggingFace starts:

1. Check `/api/v1/health`.
2. Check logs show:

```text
Starting Celery document worker...
Starting FastAPI...
triam-local-document or Celery worker ready
```

3. Upload real PDF:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

4. Generate plan.
5. Poll job:

```text
queued -> processing -> partial_ready -> ready
```

6. Confirm Redis `document` queue is not stuck.

### 13.3 Failure smoke test

Upload PDF without outline.

Expected:

```text
HTTP 422
No Celery task enqueued
No stuck processing job
```

## 14. What Is Safe To Deploy Now

Safe enough for capstone/demo if:

- DB migrated to Phase 3 head.
- HuggingFace secrets are complete.
- `ENABLE_CELERY_WORKER=true`.
- Redis Cloud is reachable.
- Only one replica/Space is running document worker for now.
- You accept single-Space resource sharing.

Not production-perfect yet:

- Auth still uses mock user in some routes.
- No user quota/upload limit per account yet.
- Notification/reminder is Phase 4.
- Worker and API share same Space resources.
- No deep monitoring dashboard yet.

## 15. Phase 4 Boundary

Phase 4 is a **new product feature**, not a required fix for Phase 3 deploy.

Phase 4 adds:

- `notification_outbox`.
- Celery Beat.
- Spaced review schedules.
- In-app notifications.
- Optional FCM push later.

Do not mix Phase 4 into Phase 3.1 deploy hardening.

Recommended order:

```text
Phase 3.1: deploy hardening
Deploy + test on HuggingFace
Then Phase 4: notification/reminder feature
```

## 16. Final Recommendation

Anh khuyên trước deploy làm Phase 3.1 theo priority:

1. Update `start.sh` to remove production `--reload`, add toggles, show logs.
2. Add Celery reconnect/long-task config explicitly.
3. Add task/job idempotency guard for already-ready jobs.
4. Add optional health endpoints.
5. Run Phase 3 tests and deploy smoke test.

Nếu em muốn tối thiểu nhất trước deploy:

```text
Must:
- Ensure DB migration is applied.
- Ensure HuggingFace Secrets complete.
- Ensure ENABLE_CELERY_WORKER=true.
- Ensure start.sh is actually used by Dockerfile.

Should:
- Remove --reload in deploy.
- Add idempotency guard for redelivered ready jobs.
- Make worker logs visible.
```

Phase 3.1 là bước "đóng nắp hộp máy" trước khi đưa lên server.

