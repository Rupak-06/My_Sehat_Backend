from pydantic import BaseModel
from typing import List, Optional, Dict

# Chat
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    risk_level: str
    self_harm_detected: bool
    advice: List[str]
    actions: List[str]
    timestamp: str

# Daily Check-in
class CheckinQuestionsResponse(BaseModel):
    date: str
    questions: List[str]

class CheckinSubmitRequest(BaseModel):
    user_id: str
    answers: Dict[str, str]

class CheckinSubmitResponse(BaseModel):
    daily_summary: str
    risk_level: str
    self_harm_detected: bool
    advice: List[str]
    actions: List[str]
