from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from medicine_backend.medicine_app.core.config import settings
from medicine_backend.medicine_app.core.db import engine, Base
from medicine_backend.medicine_app.routes import medications, reminders, prescriptions

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Mount uploads directory for static access (optional but helpful for checking uploaded files)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(medications.router)
app.include_router(reminders.router)
app.include_router(prescriptions.router)

@app.get("/health")
def health():
    return {"status": "ok"}
