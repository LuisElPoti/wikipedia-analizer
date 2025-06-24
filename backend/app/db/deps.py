from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.models import Base
from dotenv import load_dotenv
from typing import Generator
import os

load_dotenv()

# Base de datos para entorno normal

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
Base.metadata.create_all(bind=engine)

# Base de datos para pruebas
SQLALCHEMY_TEST_DATABASE_URL = os.getenv("DATABASE_URL_TEST")
engine_test = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tablas para test 
Base.metadata.create_all(bind=engine_test)
