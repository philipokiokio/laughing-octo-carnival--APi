from celery import Celery
from celery.schedules import crontab
from src.projects.project_service import project_service


job = Celery("mixer", broker="redis://localhost:6379/0")
job.conf.enable_utc = True


@job.task
def add(x, y):
    return x + y


@job.task
def update_throttle_job():
    return project_service.job_pjs_rate_limit()


job.add_periodic_task(
    crontab(minute=0, hour="*"),
    update_throttle_job.s(),
    name="Project Rate Limit Count to 0",
)
