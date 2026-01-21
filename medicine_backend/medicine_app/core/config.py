import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "Medicine & Reminder Backend"
    
    # Use absolute path for database to work from any working directory
    @property
    def DATABASE_URL(self) -> str:
        backend_dir = Path(__file__).resolve().parent.parent.parent
        db_file = backend_dir / "medicine.db"
        return f"sqlite:///{db_file}"
    
    TIMEZONE: str = "Asia/Kolkata"
    
    # Upload directory: use absolute path
    @property
    def UPLOAD_DIR(self) -> str:
        backend_dir = Path(__file__).resolve().parent.parent.parent
        upload_dir = backend_dir / "uploads"
        return str(upload_dir)
    
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
