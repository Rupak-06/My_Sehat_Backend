from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from diagnostics_backend.diagnostics_app.core.config import settings

# SQLite for dev, standard URL for prod
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
