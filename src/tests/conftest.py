from src.app.database import SQLALCHEMY_DATABASE_URL, create_engine, sessionmaker, Base
from fastapi.testclient import TestClient
from src.auth.oauth import create_access_token, create_refresh_token
import pytest

TestSQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL + "_test"

engine = create_engine(TestSQLALCHEMY_DATABASE_URL)
TestSessLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    db = TestSessLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    pass
