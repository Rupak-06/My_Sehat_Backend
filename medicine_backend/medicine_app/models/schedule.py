from sqlalchemy import Column, Integer, String, ForeignKey
from medicine_backend.medicine_app.core.db import Base

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    schedule_type = Column(String, nullable=False)  # DAILY, WEEKLY, INTERVAL
    times_json = Column(String, nullable=False)  # JSON list ["08:00", "20:00"]
    days_json = Column(String, nullable=True)  # JSON list [1, 3, 5] (Mon, Wed, Fri)
    interval_hours = Column(Integer, nullable=True)
    timezone = Column(String, default="Asia/Kolkata")
