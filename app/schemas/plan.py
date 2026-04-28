import uuid
from typing import Optional

from pydantic import BaseModel, field_validator


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: str  # "full" | "pareto" (hoặc "FULL_MODE" | "PARETO_MODE" - đều được chấp nhận)
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]

    @field_validator("mode")
    @classmethod
    def normalize_mode(cls, v: str) -> str:
        """Normalize mode về lowercase, hỗ trợ cả FULL_MODE và full."""
        mode_map = {
            "full_mode": "full",
            "pareto_mode": "pareto",
        }
        normalized = v.lower().strip()
        return mode_map.get(normalized, normalized)


class SwitchModeRequest(BaseModel):
    mode: str
