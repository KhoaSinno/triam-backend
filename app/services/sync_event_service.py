import asyncio
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Iterable

from sqlmodel import Session, select

from app.models.db_models import UserSyncEvent

RETENTION = timedelta(days=7)
POLL_INTERVAL_SECONDS = 1.0


def record_event(
    session: Session,
    *,
    user_id: uuid.UUID,
    domain: str,
    entity_id: str | uuid.UUID,
    operation: str,
    updated_at: datetime | None = None,
) -> UserSyncEvent:
    """Persist an invalidation event in the caller's transaction."""
    event = UserSyncEvent(
        user_id=user_id,
        domain=domain,
        entity_id=str(entity_id),
        operation=operation,
        updated_at=updated_at or datetime.now(timezone.utc),
    )
    session.add(event)
    session.flush()
    return event


def list_events(
    session: Session,
    *,
    user_id: uuid.UUID,
    after: int | None,
    limit: int = 100,
) -> tuple[list[UserSyncEvent], bool]:
    oldest = session.exec(
        select(UserSyncEvent.event_id)
        .where(UserSyncEvent.user_id == user_id)
        .order_by(UserSyncEvent.event_id)
        .limit(1)
    ).first()
    reset_required = after is not None and oldest is not None and after < oldest - 1
    if reset_required:
        return [], True
    statement = (
        select(UserSyncEvent)
        .where(UserSyncEvent.user_id == user_id)
        .order_by(UserSyncEvent.event_id)
        .limit(limit)
    )
    if after is not None:
        statement = statement.where(UserSyncEvent.event_id > after)
    return list(session.exec(statement).all()), False


def serialize_event(event: UserSyncEvent) -> dict[str, str | int]:
    return {
        "event_id": event.event_id or 0,
        "domain": event.domain,
        "entity_id": event.entity_id,
        "operation": event.operation,
        "updated_at": event.updated_at.isoformat(),
    }


async def stream_events(session_factory, *, user_id: uuid.UUID, after: int | None):
    """Database-polled SSE for the single EC2 deployment.

    The durable log makes reconnects safe; deployment can later replace the
    wait loop with a broker without changing the wire contract.
    """
    cursor = after
    while True:
        with session_factory() as session:
            events, reset_required = list_events(
                session, user_id=user_id, after=cursor,
            )
        if reset_required:
            yield "event: reset_required\ndata: {}\n\n"
            return
        for event in events:
            payload = serialize_event(event)
            cursor = int(payload["event_id"])
            yield f"id: {cursor}\nevent: sync\ndata: {json.dumps(payload)}\n\n"
        if not events:
            yield ": keep-alive\n\n"
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


def prune_expired_events(session: Session, *, now: datetime | None = None) -> int:
    cutoff = (now or datetime.now(timezone.utc)) - RETENTION
    events = list(session.exec(select(UserSyncEvent).where(UserSyncEvent.created_at < cutoff)).all())
    for event in events:
        session.delete(event)
    return len(events)
