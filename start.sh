#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  echo "Đang tắt an toàn các tiến trình..."
  local pids
  pids="$(jobs -p)" || true
  if [ -n "$pids" ]; then
    kill -TERM $pids 2>/dev/null || true
    wait $pids 2>/dev/null || true
  fi
  echo "Đã tắt xong."
}
trap cleanup INT TERM EXIT

export PYTHONUNBUFFERED=1
export UV_NO_SYNC="${UV_NO_SYNC:-1}"

UV_RUN=(uv run --no-sync)

if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
  echo "Running Alembic migrations..."
  "${UV_RUN[@]}" alembic upgrade head
fi

if [ "${ENABLE_VOICE_AGENT:-true}" = "true" ]; then
  AGENT_MODE="${AGENT_MODE:-start}"
  echo "Starting realtime voice agent..."
  "${UV_RUN[@]}" python -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" 2>&1 | tee worker.log &
else
  echo "Skipping realtime voice agent because ENABLE_VOICE_AGENT=false"
fi

if [ "${ENABLE_CELERY_WORKER:-false}" = "true" ]; then
  echo "Starting Celery document worker..."
  "${UV_RUN[@]}" celery -A app.core.celery_app.celery_app worker \
    -Q document \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_DOCUMENT_CONCURRENCY:-1}" \
    2>&1 | tee celery_document.log &
else
  echo "Skipping Celery document worker because ENABLE_CELERY_WORKER=false"
fi

BACKEND_PORT="${BACKEND_PORT:-8000}"
UVICORN_RELOAD="${UVICORN_RELOAD:-false}"

if [ "$UVICORN_RELOAD" = "true" ]; then
  echo "Starting FastAPI with reload on port ${BACKEND_PORT}..."
  "${UV_RUN[@]}" uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
else
  echo "Starting FastAPI on port ${BACKEND_PORT}..."
  "${UV_RUN[@]}" uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT"
fi
