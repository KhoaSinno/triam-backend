# Sử dụng Python 3.10 slim
FROM python:3.12-slim

# Copy uv từ image chính thức của Astral (cách cài uv tốt nhất trong Docker)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Tạo user không phải root (Bắt buộc trên Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Thiết lập thư mục làm việc
WORKDIR $HOME/app

# Copy các file quản lý thư viện của uv vào trước để cache
COPY --chown=user pyproject.toml uv.lock ./

# Cài đặt dependencies (sử dụng uv sync)
RUN uv sync --frozen --no-dev

# Copy toàn bộ mã nguồn dự án vào container
COPY --chown=user . .

# Chạy ứng dụng FastAPI bằng uvicorn thông qua uv, đổi port sang 7860
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]