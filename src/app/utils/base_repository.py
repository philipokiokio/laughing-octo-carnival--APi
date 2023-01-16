from src.app.utils.db_utils import SessionLocal
from sqlalchemy.orm import Session


class BaseRepo:
    def __init__(self):
        self.db: Session = SessionLocal()
