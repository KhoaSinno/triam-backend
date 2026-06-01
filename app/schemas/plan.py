import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constant import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]
    reminder_time: str | None = None  # VD: "20:00", nếu None sẽ lấy từ user settings
    activate: bool = False  # False: chỉ cấu hình/generate, True: active lịch ngay


class SwitchModeRequest(BaseModel):
    mode: PlanMode


class PlanUpdateRequest(BaseModel):
    pace: int | None = None
    schedule_config: list[str] | None = None
    reminder_time: str | None = None  # HH:MM format


class ReadingPlanSlotResponse(BaseModel):
    id: uuid.UUID
    weekday: int
    weekday_label: str
    reminder_time: str
    timezone: str
    is_active: bool


class ReadingPlanUserSlotResponse(ReadingPlanSlotResponse):
    plan_id: uuid.UUID
    book_id: uuid.UUID


class ReadingPlanResponse(BaseModel):
    plan_id: uuid.UUID
    book_id: uuid.UUID
    mode: PlanMode
    pace: int
    schedule_config: list[str] = Field(default_factory=list)
    reminder_time: str
    status: str
    plan_status: str
    active_slots: list[ReadingPlanSlotResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ReadingPlanUpdateResponse(ReadingPlanResponse):
    message: str
