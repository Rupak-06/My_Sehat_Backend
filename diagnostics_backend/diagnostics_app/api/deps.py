from typing import Generator
from diagnostics_backend.diagnostics_app.db.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
