from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from app.db.database import Base

from datetime import datetime


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    job_name = Column(String(255), nullable=False)

    job_type = Column(String(100), nullable=False)

    payload = Column(JSON, nullable=False)

    status = Column(String(50), default="PENDING")

    schedule_type = Column(String(50))

    scheduled_time = Column(DateTime, nullable=True)

    cron_expression = Column(String(100), nullable=True)

    retry_count = Column(Integer, default=0)

    max_retries = Column(Integer, default=3)

    next_run_time = Column(DateTime, nullable=True)

    last_run_time = Column(DateTime, nullable=True)

    is_recurring = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )