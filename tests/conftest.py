import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, LocalSession
from app.auth import verify_jwt_token
from main import app

db_path = "test.db"

temp_db = create_engine(f"sqlite:///{db_path}", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=temp_db)

# Create tables before any tests run
Base.metadata.create_all(bind=temp_db)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override dependencies
app.dependency_overrides[verify_jwt_token] = lambda: "test@email.com"
app.dependency_overrides[LocalSession] = override_get_db


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    # Drop all tables and recreate for each test
    Base.metadata.drop_all(bind=temp_db)
    Base.metadata.create_all(bind=temp_db)
    yield
