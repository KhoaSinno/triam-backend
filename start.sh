#!/usr/bin/env bash
set -e

# Bắt tín hiệu Ctrl+C để gửi lệnh tắt (TERM) cho worker, sau đó ĐỨNG CHỜ (wait) nó dọn dẹp an toàn
trap 'echo "Đang tắt an toàn các tiến trình..."; kill -TERM $(jobs -p) 2>/dev/null; wait $(jobs -p) 2>/dev/null; echo "Đã tắt xong."; exit' INT TERM EXIT

# Chạy Agent ngầm qua module path để tránh lỗi import package `app`.
# Dùng mode `start` cho server; có thể đổi qua `dev` khi local debug.
AGENT_MODE="${AGENT_MODE:-start}"
export PYTHONUNBUFFERED=1
# uv run python -m app.services.agent_voice_service "$AGENT_MODE" > worker.log 2>&1 &
uv run python -m app.services.agent_voice_gpt_realtime "$AGENT_MODE" > worker.log 2>&1 &
# uv run python -m app.services.agent_voice_test_gemini "$AGENT_MODE" > worker.log 2>&1 &


# Chạy FastAPI chính
BACKEND_PORT="${BACKEND_PORT:-8000}"
uv run uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
