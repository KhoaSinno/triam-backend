import uuid

from pydantic import BaseModel


class PlanInput(BaseModel):
    book_id: uuid.UUID
    mode: str  # "FULL_MODE" | "PARETO_MODE"
    pace: int  # số chương/ngày
    schedule_config: list[str]  # VD: ["Mon", "Wed", "Fri"]
