from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from medicine_backend.medicine_app.core.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    extraction_status = Column(String, default="UPLOADED")  # UPLOADED, CONFIRMED
    extracted_json = Column(String, nullable=True)  # Store JSON as string if needed, or structured data
