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


class ReadingPlanSessionUnitResponse(BaseModel):
    id: uuid.UUID
    learning_unit_id: uuid.UUID
    unit_title: str = ""
    unit_order: int
    status: str
    completed_at: datetime | None = None


class ReadingPlanSessionResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    book_id: uuid.UUID
    mode: PlanMode
    session_index: int
    scheduled_at: datetime
    local_date: str
    reminder_time: str
    timezone: str
    status: str
    completed_units: int
    total_units: int
    is_overdue: bool
    started_at: datetime | None = None
    completed_at: datetime | None = None
    missed_at: datetime | None = None
    skipped_at: datetime | None = None
    units: list[ReadingPlanSessionUnitResponse] = Field(default_factory=list)


class ReadingPlanSessionListResponse(BaseModel):
    book_id: uuid.UUID | None = None
    local_date: str | None = None
    timezone: str | None = None
    total: int
    items: list[ReadingPlanSessionResponse] = Field(default_factory=list)


class ReadingPlanSessionSummaryResponse(BaseModel):
    total_sessions: int = 0
    completed_sessions: int = 0
    missed_sessions: int = 0
    next_session: ReadingPlanSessionResponse | None = None


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
    started_at: datetime | None = None
    paused_at: datetime | None = None
    completed_at: datetime | None = None
    session_summary: ReadingPlanSessionSummaryResponse | None = None


class ReadingPlanUpdateResponse(ReadingPlanResponse):
    message: str
