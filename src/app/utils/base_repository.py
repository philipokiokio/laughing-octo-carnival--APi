from sqlalchemy.orm import Session

from src.app.utils.db_utils import SessionLocal


class BaseRepo:
    def __init__(self):
        self.db: Session = SessionLocal()
