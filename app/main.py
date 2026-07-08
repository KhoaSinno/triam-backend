print("--- TRIAM FastAPI starting up... ---", flush=True)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.api.v1.routers import admin, audiobooks, health, jobs, learning_progress, live, notifications, reading_plan_sessions, reviews, study_context, threads, upload
from app.core.exceptions import AppException
from app.core.logger import log
from app.db.database import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Khởi động hệ thống... (TRIAM)")
    # Alembic owns schema migration; startup only manages runtime resources.
    yield
    log.info("Đang dọn dẹp tài nguyên...")
    dispose_engine()


app = FastAPI(title="TRIAM Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(live.router, prefix="/api/v1", tags=["Live"])
app.include_router(audiobooks.router, prefix="/api/v1", tags=["Audiobooks"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notifications"])
app.include_router(learning_progress.router, prefix="/api/v1", tags=["Learning Progress"])
app.include_router(reading_plan_sessions.router, prefix="/api/v1", tags=["Reading Plan Sessions"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
app.include_router(study_context.router, prefix="/api/v1", tags=["Study Context"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])

app.include_router(threads.router, prefix="/api/v1", tags=["Threads Chat"])


@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
