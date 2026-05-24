---
name: triam-deploy-realtime-ops
description: Project-specific deployment and realtime operations rules for Triam Backend. Use when deploying, debugging, reviewing, or hardening Hugging Face Spaces, Dockerfile, start.sh, runtime env vars, uv runtime behavior, LiveKit realtime voice agent, production logs, capacity settings, health checks, or production smoke tests.
---

# Triam Deploy And Realtime Ops

Use this skill when work touches production startup, Hugging Face Spaces, Docker, `start.sh`, LiveKit voice agent runtime, or server logs.

## 1. Production Runtime Rules

- Docker build may install dependencies with `uv sync --frozen --no-dev`; runtime must not install or sync dependencies again.
- In `start.sh`, run Python tools through `uv run --no-sync` and set `UV_NO_SYNC=1` by default.
- Do not use `uvicorn --reload` in deployed environments. Gate reload behind `UVICORN_RELOAD=false`.
- Keep runtime process toggles explicit: `ENABLE_VOICE_AGENT`, `ENABLE_CELERY_WORKER`, `RUN_MIGRATIONS_ON_START`, `BACKEND_PORT`.
- Keep `start.sh` POSIX-compatible and verify with `bash -n start.sh`.
- Ensure shell files use LF line endings. Keep `.gitattributes` rules for `*.sh text eol=lf`.

## 2. Hugging Face Free Capacity Profile

Current free CPU Space expectations:

- Treat CPU Basic as small shared capacity: 2 vCPU, 16 GB RAM, temporary local disk.
- Triam currently co-hosts FastAPI, Celery document worker, and LiveKit voice agent in one Space. Tune for stability before concurrency.
- Default production profile while co-hosted:
  - `CELERY_DOCUMENT_CONCURRENCY=1`
  - `LIVEKIT_AGENT_JOB_EXECUTOR_TYPE=thread`
  - `LIVEKIT_AGENT_NUM_IDLE_PROCESSES=1`
  - `LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=1` for stable demo, `2` only when intentionally testing concurrent voice users
  - `LIVEKIT_AGENT_INITIALIZE_PROCESS_TIMEOUT=60`
- If realtime concurrency becomes a product requirement, prefer splitting API/Celery/Voice into separate runtimes before raising all concurrency knobs.

## 3. LiveKit Agent Rules

- Do not set LiveKit `load_fnc=lambda: 0.0` in production; that makes the worker report unlimited capacity.
- Use a load function based on active jobs and `LIVEKIT_AGENT_MAX_CONCURRENT_JOBS`.
- On HF free, prefer thread executor to avoid expensive child process startup. Use process executor only on a dedicated, stronger runtime.
- `unexpected message type` plus immediate `failed to connect ... retrying` and then `registered worker` is a transient reconnect, not a fatal outage.
- Escalate LiveKit reconnects only when they loop repeatedly, prevent registration, or coincide with failed room joins.

## 4. Secret-Safe Logging

- Production loggers must not leak `Authorization`, `apikey`, `api_key`, `api_secret`, service-role keys, JWTs, access tokens, or refresh tokens.
- Disable Loguru `diagnose` and `backtrace` in production sinks so tracebacks do not dump local variables.
- When adding log redaction, add regression tests with realistic snippets from third-party stack traces.
- Never paste raw production logs containing secrets into docs, issues, or chat.

## 5. Verification Checklist

Before deploy-related changes are considered done:

```powershell
bash -n start.sh
uv run ruff check <changed python files>
uv run python -m py_compile <changed python files>
uv run pytest tests/test_health_api.py tests/test_celery_enqueue.py tests/test_processing_jobs_api.py -q
```

For log/security changes, also run:

```powershell
uv run pytest tests/test_document_parsers.py -q
```

After deployment, check logs for:

- no runtime dependency downloads such as `Downloading ruff`
- FastAPI startup complete
- Celery connected and ready when enabled
- LiveKit worker registered when enabled
- no visible API keys or bearer tokens in tracebacks
