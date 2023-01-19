from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.app.database import SessionLocal


def get_db():
    db: Session = SessionLocal()

    try:
        yield db

    except:
        db.rollback()

    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(hashed_password, plain_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)
