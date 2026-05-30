import uuid

from pydantic import BaseModel

from app.core.constant import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]
    reminder_time: str | None = None  # VD: "20:00", nếu None sẽ lấy từ user settings


class SwitchModeRequest(BaseModel):
    mode: PlanMode


class PlanUpdateRequest(BaseModel):
    pace: int | None = None
    schedule_config: list[str] | None = None
    reminder_time: str | None = None  # HH:MM format
