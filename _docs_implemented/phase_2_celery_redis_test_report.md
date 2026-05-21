# Phase 2 Celery + Redis Test Report

Date: 2026-05-21

## Scope

Implemented Phase 2 code path:

- FastAPI no longer executes `generate-plan` and `switch-mode` through `BackgroundTasks`.
- API creates DB `processing_jobs` rows as in Phase 1.
- API enqueues Celery tasks:
  - `triam.books.process`
  - `triam.books.switch_mode`
- Redis/Celery is execution infrastructure only.
- FE progress remains sourced from Postgres via:
  - `GET /api/v1/jobs/{job_id}`
  - `GET /api/v1/books/{book_id}/processing-status`

## Security Note

Redis Cloud credentials were not committed to source and were not written to this report.

The Redis password was pasted into chat during implementation. Treat it as exposed and rotate it before deploy or sharing logs.

Local code reads Redis from `CELERY_BROKER_URL`. Do not hard-code this value in source, tests, docs, or shell scripts. Put it in local `.env` or HuggingFace Secrets.

Local `.env` has been updated for development, but `.env` is git-ignored and will not be deployed through source control. HuggingFace Spaces must receive the same variables through Space Secrets/Variables.

Expected deployment shape:

```text
CELERY_BROKER_URL=redis://default:<redis-password>@<redis-host>:<redis-port>/0
CELERY_RESULT_BACKEND=
```

`CELERY_RESULT_BACKEND` should stay empty for this phase because Postgres `processing_jobs` is the source of truth.

## Static Verification

Celery app import/config check:

```text
celery_app.main = triam
task_ignore_result = True
task_routes = {
  "triam.books.process": {"queue": "document"},
  "triam.books.switch_mode": {"queue": "document"}
}
```

Task import check:

```text
triam.books.process
triam.books.switch_mode
```

Alembic DB state:

```text
c4f0a9d8e2b1 (head)
```

## Automated Tests

Command:

```powershell
uv run pytest tests\test_celery_enqueue.py tests\test_processing_jobs_api.py tests\test_document_parsers.py tests\test_api_study_context.py -q
```

Result:

```text
13 passed in 21.10s
```

Ruff focused check:

```powershell
uv run ruff check app\core\config.py app\core\celery_app.py app\tasks\__init__.py app\tasks\book_tasks.py app\services\upload_service.py app\api\v1\routers\upload.py app\services\audiobook_service.py app\api\v1\routers\audiobooks.py tests\test_celery_enqueue.py
```

Result:

```text
All checks passed!
```

## Runtime Integration Test With Real PDF

File:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

To avoid burning LLM/TTS quota and writing test files to Supabase Storage, this test used:

- Real PDF file.
- Real parser.
- Real FastAPI routes.
- Real DB writes.
- Mocked Supabase Storage upload.
- Mocked Celery `apply_async`, capturing task name, queue, and args.
- Cleanup of the created book after test.

### Log Summary

```text
STEP 1 | PDF_FOUND | Chương 4_ Phương pháp luận nghiên cứu.pdf
STEP 2 | STORAGE_UPLOAD_MOCK | raw_books <book_id>/original.pdf application/pdf
INFO | PDF uploaded to Storage: <book_id>/original.pdf
INFO | Created DRAFT book <book_id> | 3 chapters | file_url saved
STEP 3 | UPLOAD_RESPONSE | 200
```

Upload response:

```json
{
  "total_chapters": 3,
  "document_type": "pdf",
  "outline": [
    {"title": "Chương 4: Phương pháp luận nghiên cứu", "page_start": 1},
    {"title": "Chương 5: Kết quả phân tích và so sánh", "page_start": 2},
    {"title": "Chương 6: Bàn luận và Khuyến nghị", "page_start": 6}
  ]
}
```

Generate plan:

```text
INFO | ReadingPlan created for book <book_id> | mode=full | job=<job_id>
STEP 5 | CELERY_ENQUEUE_GENERATE_PLAN | queue=document args=[<book_id>, full, <job_id>]
STEP 4 | GENERATE_PLAN_RESPONSE | 200
```

Generate plan response:

```json
{
  "mode": "full",
  "status": "queued",
  "progress_percent": 0
}
```

Job status:

```text
STEP 6 | JOB_STATUS_RESPONSE | 200
```

Job status response:

```json
{
  "job_type": "generate_plan",
  "status": "queued",
  "mode": "full",
  "progress_percent": 0,
  "current_step": "Đang chờ xử lý sách.",
  "total_units": 3,
  "done_units": 0,
  "failed_units": 0,
  "error_message": null
}
```

Switch mode:

```text
STEP 8 | CELERY_ENQUEUE_SWITCH_MODE | queue=document args=[<book_id>, pareto, <switch_job_id>]
STEP 7 | SWITCH_MODE_RESPONSE | 200
```

Switch response:

```json
{
  "message": "Đã chuyển sang mode pareto. Hệ thống đang sinh audio trong background.",
  "needs_generation": true,
  "status": "queued",
  "progress_percent": 0
}
```

Latest processing job:

```text
STEP 9 | LATEST_JOB_RESPONSE | 200
```

Latest job response:

```json
{
  "job_type": "switch_mode",
  "status": "queued",
  "mode": "pareto",
  "progress_percent": 0,
  "current_step": "Đang chờ sinh audio mode pareto.",
  "total_units": 3,
  "done_units": 0,
  "failed_units": 0,
  "error_message": null
}
```

Captured Celery calls:

```text
triam.books.process -> queue=document -> args=[<book_id>, full, <job_id>]
triam.books.switch_mode -> queue=document -> args=[<book_id>, pareto, <switch_job_id>]
```

Cleanup:

```text
STEP 11 | CLEANUP_BOOK | <book_id>
```

## Live Redis Cloud Verification

Redis Cloud connectivity was checked with the real free Redis instance. The secret value was injected only through the shell environment and was not committed.

Initial mistake caught during verification:

```text
TRIAM_REDIS_TEST_URL was set, but app.core.celery_app reads CELERY_BROKER_URL.
Celery therefore tried redis://localhost:6379/0 and failed with connection refused.
```

Corrected verification:

```text
REDIS_PING True
CELERY_PROBE_TASK_SENT True
PROBE_QUEUE_LENGTH_AFTER_SEND 1
PROBE_QUEUE_LENGTH_AFTER_CLEANUP 0
```

Meaning:

- Redis Cloud is reachable from the local backend environment.
- Celery can publish a task message to Redis Cloud.
- Probe cleanup worked; the temporary probe queue was removed.
- The real `document` queue was not polluted by the probe.

Worker probe:

```text
transport: redis://default:**@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
results: disabled://
queues: document
tasks:
  . triam.books.process
  . triam.books.switch_mode
phase2probe2@KhoaSinoo ready.
```

Celery control ping:

```text
->  phase2probe@KhoaSinoo: OK
        pong

1 node online.
```

This confirms a real Celery worker can connect to Redis Cloud and receive control messages through the broker. The probe worker was stopped after verification.

## Worker Startup

Local worker command for Windows development:

```powershell
$env:CELERY_BROKER_URL="redis://default:<redis-password>@<redis-host>:<redis-port>/0"
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo
```

Linux/HuggingFace startup:

```env
CELERY_BROKER_URL=redis://default:<redis-password>@redis-19459.crce302.ap-seast-1-3.ec2.cloud.redislabs.com:19459/0
CELERY_RESULT_BACKEND=
ENABLE_CELERY_WORKER=true
```

`start.sh` starts the document worker only when `ENABLE_CELERY_WORKER=true`. This keeps local API-only development simple and allows deployment to choose whether API and worker live in the same Space or separate runtimes.

## Result

Phase 2 is functionally wired:

- `generate-plan` creates a DB job and enqueues `triam.books.process`.
- `switch-mode` creates a DB job and enqueues `triam.books.switch_mode`.
- FE can poll job progress immediately after the API response.
- Redis Cloud publish path works.
- Worker execution still uses the existing Phase 1 processing functions, so progress/status semantics remain consistent.
