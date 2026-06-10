import base64
import json

from app.core.config import settings
from app.services.live_service import _build_livekit_token


def _decode_jwt_payload(token: str) -> dict:
    payload = token.split(".")[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)
    return json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))


def test_livekit_token_includes_room_lifecycle_config():
    token_data = _build_livekit_token("room-test", {"thread_id": "thread-1"})

    payload = _decode_jwt_payload(token_data["token"])
    room_config = payload["roomConfig"]

    assert room_config["emptyTimeout"] == settings.LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS
    assert room_config["departureTimeout"] == settings.LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS
    assert room_config["agents"][0]["agentName"] == settings.LIVEKIT_AGENT_NAME
    assert json.loads(room_config["agents"][0]["metadata"]) == {"thread_id": "thread-1"}
