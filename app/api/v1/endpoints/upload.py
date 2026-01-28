from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.pdf_service import extract_text_from_pdf, extract_chapters_smart
from app.services.llm_service import normalize_text_for_speech
from app.services.tts_service import stream_text_to_speech_edge

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process PDF file
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    # return {"filename": file.filename, "status": "uploaded"}

    chapters = await extract_chapters_smart(file.file)
    return {"filename": file.filename, "chapters": chapters}


@router.post("/process-book-intro")
async def process_book_intro(file: UploadFile = File(...)):
    """
    Flow Demo:
    1. User upload PDF.
    2. Server đọc 1-2 trang đầu.
    3. LLM sửa lỗi chính tả/viết tắt (CNTT -> Công nghệ thông tin).
    4. TTS đọc stream về ngay lập tức.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    # 1. Extract Text (Lấy 2 trang đầu làm Intro)
    raw_text = await extract_text_from_pdf(file, max_pages=2)

    if not raw_text:
        raise HTTPException(status_code=400, detail="Không đọc được nội dung PDF")

    # 2. Normalize (Biên tập lại - Bước quan trọng nhất!)
    # Cắt ngắn bớt nếu quá dài để demo cho nhanh (lấy 1000 ký tự đầu)
    short_preview = raw_text[:1000]
    script_ready = await normalize_text_for_speech(short_preview)

    print(f"Original: {short_preview[:100]}...")
    print(f"Normalized: {script_ready[:100]}...")

    # 3. Stream Audio về App (Dùng Edge TTS miễn phí)
    return StreamingResponse(
        stream_text_to_speech_edge(script_ready),
        media_type="audio/mpeg"
    )
