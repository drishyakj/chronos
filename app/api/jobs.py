from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.job import Job
from app.models.job_execution_log import JobExecutionLog

from app.schemas.job import JobCreate
from app.schemas.job import RescheduleJob

from app.scheduler.scheduler import scheduler
from app.scheduler.scheduler import execute_job

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/")
def create_job(
    payload: JobCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    is_recurring = payload.schedule_type == "CRON"

    job = Job(
        job_name=payload.job_name,
        job_type=payload.job_type,
        payload=payload.payload,
        schedule_type=payload.schedule_type,
        scheduled_time=payload.scheduled_time,
        cron_expression=payload.cron_expression,
        max_retries=payload.max_retries,
        status="SCHEDULED",
        is_recurring=is_recurring
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    # One-time jobs
    if payload.schedule_type == "ONCE":

        scheduler.add_job(
            execute_job,
            "date",
            run_date=payload.scheduled_time,
            args=[job.id],
            id=str(job.id)
        )

    # Recurring cron jobs
    elif payload.schedule_type == "CRON":

        cron_parts = payload.cron_expression.split()

        scheduler.add_job(
            execute_job,
            "cron",
            minute=cron_parts[0],
            hour=cron_parts[1],
            day=cron_parts[2],
            month=cron_parts[3],
            day_of_week=cron_parts[4],
            args=[job.id],
            id=str(job.id)
        )

    return {
        "message": "Job created successfully",
        "job_id": job.id
    }


@router.get("/")
def get_jobs(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Job).all()


@router.get("/{job_id}")
def get_job(
    job_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )


@router.delete("/{job_id}")
def cancel_job(
    job_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        return {
            "message": "Job not found"
        }

    job.status = "CANCELLED"

    try:
        scheduler.remove_job(str(job.id))
    except:
        pass

    db.commit()

    return {
        "message": "Job cancelled"
    }


@router.put("/{job_id}/reschedule")
def reschedule_job(
    job_id: int,
    payload: RescheduleJob,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        return {
            "message": "Job not found"
        }

    job.scheduled_time = payload.scheduled_time

    job.status = "SCHEDULED"

    try:
        scheduler.remove_job(str(job.id))
    except:
        pass

    scheduler.add_job(
        execute_job,
        "date",
        run_date=payload.scheduled_time,
        args=[job.id],
        id=str(job.id)
    )

    db.commit()

    return {
        "message": "Job rescheduled"
    }


@router.get("/logs/all")
def get_logs(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(JobExecutionLog).all()


@router.get("/health/check")
def health_check(
    current_user=Depends(get_current_user)
):

    return {
        "status": "healthy"
    }


@router.get("/stats/summary")
def stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    total_jobs = db.query(Job).count()

    success_jobs = (
        db.query(Job)
        .filter(Job.status == "SUCCESS")
        .count()
    )

    failed_jobs = (
        db.query(Job)
        .filter(Job.status == "FAILED")
        .count()
    )

    pending_jobs = (
        db.query(Job)
        .filter(Job.status == "PENDING")
        .count()
    )

    recurring_jobs = (
        db.query(Job)
        .filter(Job.is_recurring == True)
        .count()
    )

    return {
        "total_jobs": total_jobs,
        "success_jobs": success_jobs,
        "failed_jobs": failed_jobs,
        "pending_jobs": pending_jobs,
        "recurring_jobs": recurring_jobs
    }