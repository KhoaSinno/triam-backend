from datetime import datetime, timezone
import uuid

from app.models.db_models import UserSyncEvent
from app.services.sync_event_service import serialize_event


def test_sync_event_wire_payload_is_small_and_cursor_addressable():
    event = UserSyncEvent(
        event_id=42,
        user_id=uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc"),
        domain="progress",
        entity_id="unit-1",
        operation="update",
        updated_at=datetime(2026, 8, 14, tzinfo=timezone.utc),
    )

    assert serialize_event(event) == {
        "event_id": 42,
        "domain": "progress",
        "entity_id": "unit-1",
        "operation": "update",
        "updated_at": "2026-08-14T00:00:00+00:00",
    }
