from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.services.tts_service import stream_text_to_speech, stream_text_to_speech_edge
from app.api.v1.endpoints import upload  # Import router upload

app = FastAPI(title="TRIAM Assistant API")

# Include Router
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])

@app.get("/")
async def root():
    return {"message": "TRIAM Backend is running fast with uv!"}

@app.get("/test-voice-stream")
async def test_voice_stream(text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM."):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(
        stream_text_to_speech(text),
        media_type="audio/mpeg"
    )

@app.get("/test-voice-stream-edge")
async def test_voice_stream_edge(text: str = "Xin chào, đây là thử nghiệm tốc độ đọc của TRIAM."):
    """
    Endpoint này demo khả năng stream audio ngay lập tức.
    """
    # Trả về StreamingResponse để Client nghe được ngay khi có byte đầu tiên
    return StreamingResponse(
        stream_text_to_speech_edge(text),
        media_type="audio/mpeg"
    )

if __name__ == "__main__":
    import uvicorn
    # Reload=True để code tới đâu server cập nhật tới đó
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
