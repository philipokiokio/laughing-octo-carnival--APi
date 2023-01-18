from celery import Celery
from src.app.database import SessionLocal
from src.projects.models import ProjectRateLimit
from sqlalchemy.orm import scoped_session
from celery.schedules import crontab

job = Celery("mixer", broker="redis://localhost:6379/0")
job.conf.enable_utc = True


# Setting up the SQLAlchemy
db = scoped_session(SessionLocal)


class SQLAlchemyTask(job.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db.remove()


@job.task
def add(x, y):
    return x + y


@job.task(base=SQLAlchemyTask)
def update_throttle_job():
    pj_rates = db.query(ProjectRateLimit).all()

    if not pj_rates:
        return "No Projects to Revert base count"
    for pj_rate in pj_rates:
        pj_rate.count = 0
        db.commit()
        db.refresh(pj_rate)
    return "Project Rates for all project count is reverted to 0"


job.add_periodic_task(
    crontab(minute=0, hour="*"),
    update_throttle_job.s(),
    name="Project Rate Limit Count to 0",
)
