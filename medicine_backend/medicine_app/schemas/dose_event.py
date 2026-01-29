from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DoseEventBase(BaseModel):
    status: str
    note: Optional[str] = None

class DoseEventUpdate(BaseModel):
    status: str
    note: Optional[str] = None

class DoseEvent(DoseEventBase):
    id: int
    medication_id: int
    scheduled_at: datetime
    updated_at: datetime
    taken_at: Optional[datetime] = None
    medication_name: Optional[str] = None
    strength: Optional[str] = None

    class Config:
        from_attributes = True
