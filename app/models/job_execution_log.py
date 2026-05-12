from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from app.db.database import Base

from datetime import datetime


class JobExecutionLog(Base):

    __tablename__ = "job_execution_logs"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer)

    execution_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(String(50))

    error_message = Column(
        String(1000),
        nullable=True
    )

    retry_attempt = Column(
        Integer,
        default=0
    )

    execution_output = Column(
        String(1000),
        nullable=True
    )