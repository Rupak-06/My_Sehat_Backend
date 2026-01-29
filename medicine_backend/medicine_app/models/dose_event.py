from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from medicine_backend.medicine_app.core.db import Base

class DoseEvent(Base):
    __tablename__ = "dose_events"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, TAKEN, SKIPPED, MISSED
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    taken_at = Column(DateTime, nullable=True)
    note = Column(String, nullable=True)

    medication = relationship("Medication")

    @property
    def medication_name(self):
        return self.medication.name if self.medication else "Unknown Medicine"

    @property
    def strength(self):
        return self.medication.strength if self.medication else None
