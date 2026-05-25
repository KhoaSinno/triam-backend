# Phase 4.1 Runtime Test Report - Celery Beat + Notification Worker

Date: 2026-05-24

Status: **PASSED**

## Why This Test Was Needed

The previous verification covered DB migration, API, repositories, task functions, and regression tests. It did **not** prove the real runtime chain:

```text
Celery Beat -> scan_due task -> notification worker -> deliver_due task -> user_notifications -> FE/API reads notifications
```

This report records the real local runtime test using a live Celery worker and a live Celery Beat process.

## Runtime Setup

Environment:

- Local Windows 11 workspace.
- Redis Cloud broker from current `.env`.
- Current DB migration head: `e4f7a9c2d1b0`.
- Worker queue: `notification,maintenance`.
- Worker pool: `solo`, concurrency `1`.
- Beat schedule: default `NOTIFICATION_SCAN_INTERVAL_SECONDS=60`.

Commands/processes used:

```powershell
uv run alembic current

uv run celery -A app.core.celery_app.celery_app worker `
  -Q notification,maintenance `
  -l info `
  --pool=solo `
  --concurrency 1 `
  --hostname triam-phase4-runtime-test@%h

uv run celery -A app.core.celery_app.celery_app beat `
  -l info `
  --schedule _docs_implemented/runtime_test_logs/celerybeat-schedule
```

Logs:

- `_docs_implemented/runtime_test_logs/phase4_worker.out.log`
- `_docs_implemented/runtime_test_logs/phase4_worker.err.log`
- `_docs_implemented/runtime_test_logs/phase4_beat.out.log`
- `_docs_implemented/runtime_test_logs/phase4_beat.err.log`
- `_docs_implemented/runtime_test_logs/phase4_runtime_seed.json`
- `_docs_implemented/runtime_test_logs/phase4_runtime_result.json`

## Seed Data

Run id:

```text
phase4-runtime-20260524100323
```

Seeded records:

- One READY book for mock user.
- One READY chapter.
- One active reading plan scheduled for current local weekday.
- One due `spaced_review_items` row.
- One already-pending `content_ready` outbox row.

Expected notification types:

```text
content_ready
spaced_review_due
plan_reminder
```

Note:

- The first seed attempt failed because test data inserted `spaced_review_items` in the same flush before the referenced chapter was visible to the FK check.
- This was a test-harness issue, not a Phase 4 runtime issue.
- Seed was fixed by committing `book/chapter/plan` first, then inserting due review/outbox rows.

## Observed Logs

Beat started:

```text
[2026-05-24 17:03:53,430: INFO/MainProcess] beat: Starting...
```

Beat emitted scanner task:

```text
[2026-05-24 17:04:53,695: INFO/MainProcess] Scheduler: Sending due task scan-due-notifications (triam.notifications.scan_due)
```

Worker registered queues and tasks:

```text
[queues]
  .> maintenance
  .> notification

[tasks]
  . triam.books.process
  . triam.books.switch_mode
  . triam.notifications.deliver_due
  . triam.notifications.scan_due
```

Scanner result:

```text
Notification scan done | created=2 | recovered=0 | should_deliver=True
```

Meaning:

- `created=2`: scanner created `plan_reminder` and `spaced_review_due`.
- The existing pending `content_ready` outbox was not newly created, but `has_due_outbox()` correctly made `should_deliver=True`.

Delivery result:

```text
Notification delivery batch done | delivered_attempts=3
```

Meaning:

- Delivery claimed and sent all 3 due outbox rows.

## Final DB/API Result

Final poll:

```json
{
  "outbox_count": 3,
  "sent_outbox_count": 3,
  "notification_count": 3,
  "api_items_for_run_count": 3,
  "review_status": "due",
  "api_status_code": 200
}
```

Final outbox statuses:

| Type | Status | Attempts |
| --- | --- | --- |
| `plan_reminder` | `sent` | 1 |
| `spaced_review_due` | `sent` | 1 |
| `content_ready` | `sent` | 1 |

Created user notifications:

| Type | Title |
| --- | --- |
| `plan_reminder` | `Đến giờ học rồi` |
| `spaced_review_due` | `Đến lúc ôn lại rồi` |
| `content_ready` | `Nội dung đã sẵn sàng` |

API verification:

- `GET /api/v1/notifications?limit=30` returned HTTP `200`.
- Response contained all 3 runtime-test notifications.

## Cleanup

Stopped local runtime test processes:

- Celery notification worker.
- Celery Beat.

Verification after stopping:

- No process remained with `triam-phase4-runtime-test`.
- No process remained using the runtime test Beat schedule path.

Restored mock user's notification settings after test:

```json
{
  "settings_restored": true,
  "user_id": "862d7c26-3160-4f76-9e77-07d91f7317cc"
}
```

Intentional leftover DB data:

- Runtime test book/chapter/plan.
- Runtime test outbox rows.
- Runtime test user notification rows.
- Runtime test spaced review item.

The user approved leaving DB test data because it can be cleaned manually later.

## Conclusion

Phase 4.1 runtime flow is now verified end-to-end:

```text
Beat emitted scan_due
-> worker consumed maintenance queue
-> scanner created due outbox rows
-> scanner detected existing pending outbox
-> worker consumed notification queue
-> delivery created user_notifications idempotently
-> API returned the created notifications
```

Deployment requirement:

For Phase 4.1 to run automatically in one current Hugging Face Space, set:

```env
ENABLE_NOTIFICATION_WORKER=true
ENABLE_CELERY_BEAT=true
```

If the app is split into multiple runtimes later:

- Multiple notification workers are allowed.
- Exactly one runtime should have `ENABLE_CELERY_BEAT=true`.
