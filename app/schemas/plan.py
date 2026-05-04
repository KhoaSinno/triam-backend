import uuid

from pydantic import BaseModel

from app.models.db_models import PlanMode


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: PlanMode
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]


class SwitchModeRequest(BaseModel):
    mode: PlanMode
