from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class JobCreate(BaseModel):

    job_name: str

    job_type: str

    payload: dict

    schedule_type: str

    scheduled_time: Optional[datetime] = None

    cron_expression: Optional[str] = None

    max_retries: int = 3


class RescheduleJob(BaseModel):

    scheduled_time: datetime