import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.schemas.plan import (
    ReadingPlanSessionActionResponse,
    ReadingPlanSessionRangeResponse,
    ReadingPlanSessionRescheduleRequest,
    ReadingPlanSessionSkipRequest,
)
from app.services.reading_plan_session_service import (
    list_reading_plan_sessions_range,
    reschedule_reading_plan_session,
    skip_reading_plan_session,
)
from app.services.sync_event_service import record_event

router = APIRouter()


@router.get("/reading-plan/sessions", response_model=ReadingPlanSessionRangeResponse)
def get_reading_plan_sessions(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    from_date: date | None = None,
    to_date: date | None = None,
    book_id: uuid.UUID | None = None,
    mode: str | None = None,
    status: str | None = None,
):
    """Lấy lịch học theo khoảng ngày để FE vẽ calendar tuần/tháng."""
    return list_reading_plan_sessions_range(
        session,
        user_id=current_user.sub,
        from_date=from_date,
        to_date=to_date,
        book_id=book_id,
        mode=mode,
        status=status,
    )


@router.post("/reading-plan/sessions/{session_id}/skip", response_model=ReadingPlanSessionActionResponse)
def skip_plan_session(
    session_id: uuid.UUID,
    payload: ReadingPlanSessionSkipRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Bỏ qua một buổi học mà không đánh dấu learning progress là completed."""
    response = skip_reading_plan_session(
        session,
        user_id=current_user.sub,
        session_id=session_id,
        reason=payload.reason,
    )
    record_event(session, user_id=current_user.sub, domain="reading_plan_session", entity_id=session_id, operation="update")
    session.commit()
    return response


@router.put("/reading-plan/sessions/{session_id}/schedule", response_model=ReadingPlanSessionActionResponse)
def reschedule_plan_session(
    session_id: uuid.UUID,
    payload: ReadingPlanSessionRescheduleRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
):
    """Dời lịch một buổi học cụ thể, giữ nguyên các learning units trong buổi đó."""
    response = reschedule_reading_plan_session(
        session,
        user_id=current_user.sub,
        session_id=session_id,
        local_date=payload.local_date,
        reminder_time=payload.reminder_time,
        timezone_name=payload.timezone,
    )
    record_event(session, user_id=current_user.sub, domain="reading_plan_session", entity_id=session_id, operation="update")
    session.commit()
    return response
