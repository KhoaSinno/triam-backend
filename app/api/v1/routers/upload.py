from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.plan import PlanInput
from app.services.upload_service import handle_generate_plan, handle_upload_document

router = APIRouter()


# -----------------------------------------------------------------------
# ENDPOINT 1: POST /upload
# -----------------------------------------------------------------------
@router.post("/upload")
async def upload_document(
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile, File(...)],
):
    """
    Bước 1: Nhận file, extract outline, upload PDF lên Supabase Storage,
    lưu Book + Chapter (DRAFT), trả về outline cho Flutter.
    """
    return await handle_upload_document(session, file)


# -----------------------------------------------------------------------
# ENDPOINT 2: POST /generate-plan
# -----------------------------------------------------------------------
@router.post("/generate-plan")
async def generate_plan(
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
):
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    return await handle_generate_plan(session, background_tasks, payload)
