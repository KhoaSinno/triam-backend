import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.constant import PlanMode, ProcessingJobStatus, ProcessingJobType


class ProcessingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ProcessingJobSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    book_id: uuid.UUID | None = None
    job_type: ProcessingJobType
    status: ProcessingJobStatus
    mode: PlanMode | None = None
    progress_percent: int
    current_step: str | None = None
    total_units: int
    done_units: int
    failed_units: int
    error_message: str | None = None
