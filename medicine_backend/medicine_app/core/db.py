from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from medicine_backend.medicine_app.core.config import settings

# SQLite checks same thread by default, we need to disable it for FastAPI
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
