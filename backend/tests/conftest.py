# conftest.py
import pytest
from fastapi.testclient import TestClient 
from app.main import app
from app.db.deps import override_get_db
from app.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_TEST_DATABASE_URL = os.getenv("DATABASE_URL_TEST")

engine_test = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[override_get_db] = get_test_db

@pytest.fixture(scope="module")
async def client(): 
    with TestClient(app) as c:
        yield c