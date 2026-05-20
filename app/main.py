from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.v1.routers import audiobooks, jobs, live, study_context, threads, upload
from app.core.exceptions import AppException
from app.core.logger import log
from app.services.tts_service import stream_text_to_speech_edge


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Chạy khi STARTUP ---
    log.info("Khởi động hệ thống... (TRIAM)")
    # Schema được quản lý bởi Alembic. Chạy: alembic upgrade head
    # Sau từ khóa yield là lúc ứng dụng đang chạy (đang phục vụ người dùng)
    yield
    # --- Chạy khi SHUTDOWN ---
    log.info("Đang dọn dẹp tài nguyên...")


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Global Exception Handler — bắt tất cả AppException và subclass của nó
# ---------------------------------------------------------------------------
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    message = f"AppException: {exc.detail} - Status Code: {exc.status_code}"
    if exc.status_code >= 500:
        log.error(message)
    else:
        log.warning(message)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.exception("Unhandled Exception:")
    return JSONResponse(status_code=500, content={"detail": "Lỗi hệ thống nội bộ."})


# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(study_context.router, prefix="/api/v1", tags=["Study Context"])

app.include_router(threads.router, prefix="/api/v1", tags=["Threads Chat"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(
    text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM.",
):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(stream_text_to_speech_edge(text), media_type="audio/mpeg")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
