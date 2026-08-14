from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import engine, get_session
from app.services.sync_event_service import list_events, serialize_event, stream_events

router = APIRouter()


def _parse_cursor(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None
    try:
        return max(0, int(value))
    except ValueError:
        return None


@router.get("/sync/events")
def replay_events(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    after: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
):
    events, reset_required = list_events(
        session,
        user_id=current_user.sub,
        after=_parse_cursor(after),
        limit=limit,
    )
    return {
        "events": [serialize_event(event) for event in events],
        "cursor": str(events[-1].event_id) if events else after,
        "reset_required": reset_required,
    }


@router.get("/sync/events/stream")
async def event_stream(
    current_user: CurrentUser,
    last_event_id: Annotated[str | None, Header()] = None,
    after: str | None = None,
):
    cursor = _parse_cursor(last_event_id) or _parse_cursor(after)
    return StreamingResponse(
        stream_events(lambda: Session(engine), user_id=current_user.sub, after=cursor),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
