import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the application uses the test database during pytest collection.
# Some modules (e.g. src.api.main) import DB/session objects at import time,
# so we must set DB_URL before those modules are imported by test modules.
# The Makefile sets DATABASE_URL for the test run; mirror it into DB_URL.
from src.api.db.db import Base

DATABASE_URL = os.environ["DATABASE_URL"]
# Make app code that reads DB_URL (via os.getenv) use the test database
os.environ["DB_URL"] = DATABASE_URL

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
