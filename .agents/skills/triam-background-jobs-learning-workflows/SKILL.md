---
name: triam-background-jobs-learning-workflows
description: Project-specific rules for Triam background processing, Celery workers, Redis broker usage, DB progress polling, notification outbox, study reminders, spaced review, and long-running learning workflows. Use when adding, refactoring, reviewing, or debugging generate-plan, switch-mode, audio generation, reminders, notifications, progress endpoints, or worker queues.
---

# Triam Background Jobs And Learning Workflows

Use this skill when work touches long-running or scheduled behavior. Triam must treat book processing, audio generation, reminders, and spaced review as durable workflows, not request-time side effects.

## Core Rule

Use the database as the source of truth for user-visible state. Use Redis/Celery as execution infrastructure. If Redis is flushed, workers restart, or a task retries, FE-visible progress must still be recoverable from Postgres.

## Progress Pattern

For upload processing, generate-plan, switch-mode, TTS, reminders, and notification delivery:

- Create or update a `processing_jobs` row before enqueueing work.
- Return `job_id`, `book_id`, `status`, and `progress_percent` to FE.
- Expose a polling endpoint such as `GET /api/v1/jobs/{job_id}` or `GET /api/v1/books/{book_id}/processing-status`.
- Update progress at meaningful milestones, not every tiny loop iteration.
- Keep status values explicit: `queued`, `processing`, `partial_ready`, `ready`, `error`, `cancelled`.
- Store `current_step`, `total_units`, `done_units`, `failed_units`, and `error_message` for debugging.
- Treat polling as the source of truth; realtime/websocket updates are optional acceleration.

## Celery And Redis Rules

- Use Redis primarily as the Celery broker. Avoid Redis result backend for Triam book jobs because Postgres `processing_jobs` is the source of truth.
- If a result backend is temporarily enabled for debugging, keep `result_expires` short and never store large payloads.
- Do not store business truth only in Redis.
- Define queues by workload type: `document`, `llm`, `tts`, `embedding`, `notification`, `maintenance`.
- Route slow or rate-limited tasks to dedicated queues so TTS/LLM work cannot block reminders.
- Use Celery retries for transient external failures: provider rate limit, network timeout, storage temporary failure.
- Use idempotency keys for tasks that create files, segments, reminders, or notifications.
- Workers must create their own DB sessions. Never pass SQLModel objects or request sessions into Celery tasks.
- Celery task args should be JSON-serializable IDs and primitive values.
- When Celery runs inside Hugging Face Spaces through `start.sh`, use `uv run --no-sync` so runtime startup does not install dev dependencies or compete with worker boot.
- While FastAPI, Celery, and LiveKit are co-hosted on one free CPU Space, keep document worker concurrency conservative, usually `CELERY_DOCUMENT_CONCURRENCY=1`.
- For production scaling, prefer separating document workers into their own runtime before increasing concurrency aggressively.

## Scheduling Rule

Prefer database-driven schedules plus Celery Beat polling over creating many long-range ETA tasks.

Pattern:

```text
Celery Beat every minute
-> scan due reminders/reviews/outbox rows in Postgres
-> enqueue focused delivery tasks
-> mark rows sent/skipped/error with idempotency protection
```

This keeps reminder state visible, debuggable, and recoverable after deploys.

## Learning Workflow Rules

- A reading plan is not only audio generation; it includes progress tracking, reminder cadence, and review after completion.
- After a chapter becomes ready, create spaced-review items from `review_text` or selected knowledge atoms.
- Suggested review intervals for capstone: 1, 3, 7, 14, and 30 days.
- User timezone must be stored before scheduling wall-clock reminders.
- Notification copy should be short, specific, and tied to book/chapter progress.
- Do not spam: enforce per-user notification cooldown and daily caps.

## Audio Unlock Rule

Implement "listen early" as first playable content, not a brittle exact 50 percent rule.

- Mark `partial_ready` when the first useful chapter or configured threshold is ready.
- FE can unlock playback when at least one chapter/segment is ready.
- Continue processing the rest in the background.
- Keep segment/chapter ordering stable so the playlist can grow without reordering already visible audio.

## Implementation Order

1. Add `processing_jobs` and polling endpoint.
2. Add status transitions for book/chapter/segment progress.
3. Move generate-plan and switch-mode execution from FastAPI `BackgroundTasks` to Celery.
4. Add token estimation and hard/soft limits before LLM normalization.
5. Add partial-ready audio unlock.
6. Add notification outbox.
7. Add Celery Beat scanner for reminders and spaced review.

## Review Checklist

- Can FE show progress after page reload?
- Can a failed job be retried without duplicate DB rows or duplicate audio paths?
- Does a server restart lose the job, or can the worker resume/retry from DB state?
- Are rate-limited providers isolated by queue/concurrency?
- Is worker concurrency appropriate for the deployed runtime capacity?
- Are reminder schedules stored in Postgres with timezone-aware `due_at`?
- Are secrets and provider payloads excluded from logs?
