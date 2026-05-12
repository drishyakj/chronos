import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.job import Job
from app.models.job_execution_log import JobExecutionLog

from app.services.job_executor import JobExecutor

scheduler = BackgroundScheduler()


async def process_job(job_id: int):

    db: Session = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        db.close()
        return

    if job.status == "CANCELLED":
        db.close()
        return

    try:

        job.status = "RUNNING"
        db.commit()

        result = await JobExecutor.execute(job)

        job.status = "SUCCESS"

        log = JobExecutionLog(
            job_id=job.id,
            status="SUCCESS",
            execution_output=str(result)
        )

        db.add(log)

        job.last_run_time = job.next_run_time

        db.commit()

    except Exception as e:

        job.retry_count += 1

        if job.retry_count >= job.max_retries:
            job.status = "FAILED"
        else:
            job.status = "RETRYING"

        log = JobExecutionLog(
            job_id=job.id,
            status="FAILED",
            error_message=str(e),
            retry_attempt=job.retry_count
        )

        db.add(log)

        db.commit()

    finally:
        db.close()


def execute_job(job_id: int):
    asyncio.run(process_job(job_id))


def start_scheduler():
    scheduler.start()