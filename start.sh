#!/usr/bin/env bash
set -e

export PYTHONUNBUFFERED=1
export UV_NO_SYNC="${UV_NO_SYNC:-1}"

# Giới hạn luồng tính toán cho PyTorch/MKL/OpenMP trên CPU basic HF Spaces.
# Mặc định PyTorch sẽ cố dùng hết tất cả cores vật lý của máy chủ ảo hóa,
# gây thrashing trên container 2 vCPU và làm container treo khi khởi động.
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export TORCH_NUM_THREADS=1

# Gọi binary trực tiếp từ .venv (nhanh hơn uv run, tránh lock contention khi
# nhiều tiến trình khởi động đồng thời). .venv được tạo bởi Dockerfile (uv sync).
PYTHON_BIN="./.venv/bin/python"
CELERY_BIN="./.venv/bin/celery"
ALEMBIC_BIN="./.venv/bin/alembic"
UVICORN_BIN="./.venv/bin/uvicorn"

if [ "${RUN_MIGRATIONS_ON_START:-false}" = "true" ]; then
  echo "Running Alembic migrations..."
  "$ALEMBIC_BIN" upgrade head
fi

if [ "${ENABLE_VOICE_AGENT:-true}" = "true" ]; then
  AGENT_MODE="${AGENT_MODE:-start}"
  echo "Starting realtime voice agent (mode=$AGENT_MODE)..."
  "$PYTHON_BIN" -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" 2>&1 | tee worker.log &
else
  echo "Skipping realtime voice agent (ENABLE_VOICE_AGENT=false)"
fi

if [ "${ENABLE_CELERY_WORKER:-false}" = "true" ]; then
  echo "Starting Celery document worker..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app worker \
    -Q document \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_DOCUMENT_CONCURRENCY:-1}" \
    2>&1 | tee celery_document.log &
else
  echo "Skipping Celery document worker (ENABLE_CELERY_WORKER=false)"
fi

if [ "${ENABLE_NOTIFICATION_WORKER:-false}" = "true" ]; then
  echo "Starting Celery notification worker..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app worker \
    -Q notification,maintenance \
    -l "${CELERY_LOG_LEVEL:-info}" \
    --concurrency "${CELERY_NOTIFICATION_CONCURRENCY:-1}" \
    2>&1 | tee celery_notification.log &
else
  echo "Skipping Celery notification worker (ENABLE_NOTIFICATION_WORKER=false)"
fi

if [ "${ENABLE_CELERY_BEAT:-false}" = "true" ]; then
  echo "Starting Celery Beat..."
  "$CELERY_BIN" -A app.core.celery_app.celery_app beat \
    -l "${CELERY_LOG_LEVEL:-info}" \
    2>&1 | tee celery_beat.log &
else
  echo "Skipping Celery Beat (ENABLE_CELERY_BEAT=false)"
fi

BACKEND_PORT="${BACKEND_PORT:-7860}"
UVICORN_RELOAD="${UVICORN_RELOAD:-false}"

if [ "$UVICORN_RELOAD" = "true" ]; then
  echo "Starting FastAPI with reload on port ${BACKEND_PORT}..."
  exec "$UVICORN_BIN" app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
else
  echo "Starting FastAPI on port ${BACKEND_PORT}..."
  exec "$UVICORN_BIN" app.main:app --host 0.0.0.0 --port "$BACKEND_PORT"
fi
