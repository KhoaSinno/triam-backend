---
name: fastapi-sqlmodel-clean-architecture
description: Project-specific backend engineering rules for Triam Backend. Use when adding, refactoring, reviewing, or debugging FastAPI routers, services, repositories, SQLModel models, Alembic migrations, Supabase/Postgres access, background workers, upload/document parsing, logging, exceptions, or tests in this codebase.
---

# Triam Backend Engineering Rules

Use this skill to keep backend changes consistent with the current Triam architecture. The project is a layered FastAPI backend using SQLModel, Alembic, Supabase/Postgres, service/repository separation, and background AI/TTS workers.

## 1. Current Architecture

Triam is not pure MVC, but it maps closely:

| MVC idea | Triam layer | Rule |
| --- | --- | --- |
| Controller | `app/api/v1/routers/` | Thin FastAPI routes only. Parse input, inject dependencies, call services, return response. |
| Model | `app/models/db_models.py` | SQLModel table definitions only. Keep schema truth here. |
| View/DTO | `app/schemas/` | Request/response DTOs. Do not expose DB models blindly for complex endpoints. |
| Service | `app/services/` | Business logic, external APIs, parsing, orchestration. Raise domain exceptions. |
| Repository | `app/repositories/` | Database reads/writes only. No HTTP, no LLM, no Supabase Storage side effects. |
| Worker | `app/services/workers/` | Long-running chapter/book/TTS/RAG processing. Create its own DB session. |
| Core | `app/core/` | Config, logging, exceptions, Supabase client, constants. |
| DB runtime | `app/db/` | Engine/session dependency and Alembic migrations. |

Prefer existing folders and naming. Do not introduce new architectural styles unless the existing layer cannot express the feature cleanly.

## 2. Request Flow

Use this flow for API features:

```text
router -> service -> repository -> model/database
       -> external integrations when needed
       -> domain exception -> global exception handler
```

Rules:

- Routers must stay thin; no parsing PDFs, no LLM prompts, no multi-step DB orchestration in routes.
- Services own business decisions and may call several repositories or external services.
- Repositories accept `session: Session` as their first argument and never create sessions internally.
- Services should raise `AppException` subclasses from `app/core/exceptions.py`; avoid `HTTPException` outside routers.
- Avoid catching broad `Exception` unless converting to a domain exception with useful context.

## 3. FastAPI Rules

- Inject DB sessions with `Depends(get_session)` in routers.
- Use `Annotated[..., Depends(...)]`, `Annotated[..., Body(...)]`, and `Annotated[..., File(...)]` where the file already follows that style.
- Return explicit response dictionaries or schema instances; keep response shape stable for FE.
- Admin routes must live under `/api/v1/admin`, require the admin dependency, and return curated DTOs instead of raw DB models.
- Admin mutations must create an audit log row. Do not expose raw server logs, provider secrets, Supabase keys, full document text, embeddings, or request headers to the admin frontend.
- Use `BackgroundTasks` only for tasks that can safely run in-process and can tolerate app restart loss.
- For durable/long-running production jobs, prefer a worker/queue design; do not hide a multi-minute critical workflow inside a request handler.
- Keep upload endpoints fail-fast: validate type/size/structure before Storage and DB writes.
- Do not log request headers, tokens, raw file bytes, or full external API payloads.

## 4. SQLModel and Repository Rules

- Define tables in `app/models/db_models.py` with explicit `__tablename__`.
- Use `uuid.UUID` primary keys with `default_factory=uuid.uuid4` unless there is a strong reason not to.
- Use explicit foreign keys and indexes for lookup paths used by endpoints/workers.
- Keep relationships in models when they clarify ownership/cascade behavior.
- Use repository functions for reusable queries and mutations:

```python
def get_book_by_id(session: Session, book_id: uuid.UUID) -> Book | None:
    return session.get(Book, book_id)
```

- Do not commit in both service and repository for the same transaction. Pick one ownership model per flow. Existing simple create repositories may commit; for multi-step workflows prefer the service controls final commit.
- Avoid N+1 query patterns. If a service loops and queries per item, consider one repository query that fetches all needed rows.

## 5. Alembic Rules

Schema changes require Alembic. Do not rely on `SQLModel.metadata.create_all()` to evolve existing tables.

Workflow:

```powershell
uv run alembic revision --autogenerate -m "short descriptive message"
uv run alembic upgrade head
```

After autogenerate:

- Read the generated migration before running it.
- Check for accidental `drop_table`, `drop_column`, enum rewrites, or destructive operations.
- Add data backfill steps manually when adding non-null columns to tables with existing rows.
- Keep downgrade reasonable for simple schema changes.
- Make sure `app/db/migrations/env.py` imports all models before `target_metadata = SQLModel.metadata`.
- For Supabase/Postgres, be careful with locks on large tables; add indexes and constraints deliberately.

## 6. Background Worker Rules

- Worker functions in `app/services/workers/` must open their own `Session(engine)`; never reuse the request session after the response.
- Update status fields (`PROCESSING`, `READY`, `ERROR`) so FE can poll.
- Limit concurrency with `asyncio.Semaphore` or bounded task lists for LLM/TTS/embedding calls.
- Log book/chapter ids and status, not secrets or large text.
- Make worker code resumable where practical: repeated calls should not corrupt storage or duplicate DB rows.
- If a worker supports multiple document types, use shared parser/dispatcher code, not hard-coded `.pdf` paths.
- For multi-minute, retryable, scheduled, or user-visible workflows, prefer Celery/RQ-style workers plus DB progress rows over FastAPI `BackgroundTasks`.
- Treat Postgres as the source of truth for job progress; Redis/Celery is execution infrastructure, not the only state store.
- For progress features, return `job_id` and expose a polling endpoint before adding realtime acceleration.
- For reminders and spaced review, store schedules/outbox rows in DB and let a scheduler enqueue due work.

## 7. Document Upload and Parsing Rules

- Supported upload types must be supported end-to-end: upload endpoint, parser, storage path, background worker.
- PDF requires hidden outline/bookmarks. No outline means `DocumentOutlineRequiredError` and HTTP 422.
- EPUB requires TOC/navigation. No TOC means HTTP 422.
- DOCX requires Heading/outline styles. No Heading means HTTP 422.
- Do not fallback to regex chapter detection, token-length splitting, or OCR unless the product explicitly adds that mode.
- EPUB/DOCX have no stable page numbers; return `page_start: None`.
- Validate before upload to Storage and DB whenever possible.

## 8. TTS Script and LLM Rewrite Rules

- Treat the LLM rewrite output as product content, not a temporary helper string. Anything stored in `LearningUnitSegment.text_content` may be spoken by TTS and shown by FE.
- Prompt rules must be general, not patched for one test book or one acronym. Do not hard-code fixes for current examples such as specific benchmark names unless they are part of a documented reusable glossary feature.
- For any acronym, initialism, symbol, benchmark, method name, or domain-specific abbreviation, the first occurrence in a learning unit must be briefly explained using the document's own expansion when available. Later occurrences in the same unit may use the short form for brevity.
- Review scripts can be played independently days later, so essential abbreviations should be explained again in `review_script`.
- The rewrite output must be plain spoken text: no Markdown, no heading markers, no bullet/table syntax, no inline code markers, no raw citation markers, and no visual emphasis symbols such as `**`.
- Add deterministic post-processing after LLM output and before DB/TTS storage for format artifacts that are never useful in speech. Use validators or tests to catch regressions.
- Do not rely on TTS providers to fix malformed content. Edge/Google/OpenAI TTS should receive already-clean, listener-friendly text.
- Prefer quality logs that report counts or terms, not full script text, because generated scripts may contain user document content.

## 9. Exceptions and Logging

- Add domain errors as `AppException` subclasses in `app/core/exceptions.py`.
- Use 400 for bad input type/size, 404 for missing resources, 409 for state conflicts, 422 for semantically invalid documents, 500 for real internal failures.
- Let `app/main.py` global handlers format responses.
- Log domain validation failures as warning/error only when operationally useful.
- Default app logs should be `INFO`; third-party HTTP libraries should stay `WARNING` or higher.
- Redact `Authorization`, `apikey`, `service_role`, JWTs, and user secrets before logs are written.
- Redact both header-style and Python local-variable-style secrets: `api_key`, `api_secret`, `access_token`, `refresh_token`.
- Disable verbose traceback local-variable dumping in production logging, such as Loguru `diagnose=True` or equivalent, because third-party stack traces can expose provider credentials.
- Add regression tests whenever a real leaked-log pattern is discovered.

## 10. Python Clean Code Rules

- Prefer small functions with one reason to change.
- Use type hints on service/repository boundaries.
- Use constants/enums from `app/core/constant.py` instead of repeated strings for statuses/modes.
- Avoid boolean flags that create two different workflows inside one function; split functions when behavior diverges.
- Avoid broad utility modules that become junk drawers.
- Keep comments for business rules or non-obvious constraints, not for line-by-line narration.
- Preserve existing Vietnamese user-facing messages when they are part of FE contract.

## 11. Testing Rules

Add tests proportional to risk:

- Parser/business rule changes: unit tests.
- Router contract changes: API tests with dependency overrides where possible.
- Worker changes: test pure helper logic and status transitions separately from external services.
- External services/Supabase: mock in unit tests; use manual integration tests only when needed.
- Add regression tests for every bug that reached manual testing.

Preferred checks:

```powershell
uv run ruff check <changed files>
uv run pytest <focused tests> -q
uv run python -m py_compile <changed python files>
```

## 12. Review Checklist

Before finalizing a backend change, verify:

- The route is thin and the service owns business logic.
- DB access is isolated in repositories unless the existing local pattern is service-owned and simple.
- All new schema changes have Alembic migrations.
- Background work does not reuse request sessions.
- Upload/storage paths match worker download paths.
- No secrets can appear in logs.
- Production tracebacks cannot dump local variables containing secrets.
- FE response contract is stable and documented when changed.
- Targeted tests and ruff pass, or any skipped check is explained.
