FROM python:3.12-slim

# Copy uv from Astral's official image (best way to install uv in Docker)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create non-root user (required on Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    UV_NO_SYNC=1

# Set working directory
WORKDIR $HOME/app

# Copy uv's dependency management files to cache
COPY --chown=user pyproject.toml uv.lock ./

# Install dependencies (using uv sync)
RUN uv sync --frozen --no-dev

# Copy all project source code into container
COPY --chown=user . .

# Run FastAPI application using uvicorn via uv, change port to 7860
# CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

# Provide access to execute and run start.sh
RUN chmod +x ./start.sh
ENV BACKEND_PORT=7860
ENV AGENT_MODE=start
CMD ["./start.sh"]
