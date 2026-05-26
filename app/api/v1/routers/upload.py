from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, UploadFile
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
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
    current_user: CurrentUser,
):
    """
    Bước 1: Nhận file, extract outline, upload tài liệu lên Supabase Storage,
    lưu Book + Chapter (DRAFT), trả về outline cho Flutter.
    """
    return await handle_upload_document(session, file, current_user.sub)


# -----------------------------------------------------------------------
# ENDPOINT 2: POST /generate-plan
# -----------------------------------------------------------------------
@router.post("/generate-plan")
async def generate_plan(
    session: Annotated[Session, Depends(get_session)],
    payload: Annotated[PlanInput, Body(...)],
    current_user: CurrentUser,
):
    """
    Bước 2: Nhận cấu hình kế hoạch học từ Flutter, lưu ReadingPlan,
    kick-off background processing.
    """
    return await handle_generate_plan(session, payload, current_user.sub)
