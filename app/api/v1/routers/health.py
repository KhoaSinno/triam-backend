from typing import Any

from fastapi import APIRouter

from app.services.health_service import get_background_health

router = APIRouter()


@router.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok", "service": "triam-backend"}


@router.get("/health/background")
def read_background_health() -> dict[str, Any]:
    return get_background_health()
