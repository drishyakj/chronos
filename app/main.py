from fastapi import FastAPI

from app.db.database import Base
from app.db.database import engine

from app.api.jobs import router as jobs_router
from app.api.auth import router as auth_router

from app.scheduler.scheduler import start_scheduler

from app.models import user
from app.models import job
from app.models import job_execution_log

app = FastAPI(
    title="Chronos"
)

Base.metadata.create_all(bind=engine)

app.include_router(jobs_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.get("/")
def root():
    return {
        "message": "Chronos Running"
    }