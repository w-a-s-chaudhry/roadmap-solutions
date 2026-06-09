# Author:      Wajid Ali Chaudhry
# Description: Shared fixtures for all tests.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.limiter import limiter

# Rate limiting is irrelevant in tests; disable it at import time
limiter.enabled = False

# In-memory SQLite — wiped fresh each test session
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the real get_db with a test version
def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Replace the dependency in the app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
