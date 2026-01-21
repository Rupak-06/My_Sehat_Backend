from fastapi import FastAPI, HTTPException
from datetime import datetime, date
import os
from typing import List

# Import local modules
from models import (
    ChatRequest, ChatResponse, 
    CheckinQuestionsResponse, CheckinSubmitRequest, CheckinSubmitResponse
)
import db
from services import ai_agent, risk_engine

app = FastAPI(
    title="Mental Health Agentic AI Backend",
    description="Backend for mental health screening and crisis detection",
    version="0.2.1"
)

# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
def on_startup():
    db.init_db()

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat/message", response_model=ChatResponse)
def chat_message(request: ChatRequest):
    # 1. Save User Message
    user_msg_id = db.save_message(request.user_id, "user", request.message)

    # 2. Get LLM Analysis
    llm_result = ai_agent.analyze_message_llm(request.message)
    
    # 3. Deterministic Risk Assessment
    # 3. Deterministic Risk Assessment
    kw_score, reasons = risk_engine.calculate_risk_score(request.message)
    
    # Check if deterministic engine caught self-harm (score >= 20 from our new logic)
    deterministic_sh = (kw_score >= 20)

    final_risk_level = risk_engine.determinize_risk_level(
        llm_result.get("risk_level", "medium"),
        kw_score,
        llm_result.get("self_harm_detected", False)
    )
    
    # Unified self-harm flag
    final_sh_detected = llm_result.get("self_harm_detected", False) or deterministic_sh

    # 4. Determine Actions
    actions = risk_engine.get_actions(final_risk_level)
    
    # Add keyword reasons to internal tracking (optional, merging with LLM if needed)
    # For now we rely on the risk event log

    # 5. Save Risk Event & Assistant Message
    # We save the risk event first to capture the moment analysis
    db.save_risk_event(
        user_id=request.user_id,
        message_id=user_msg_id,
        risk_level=final_risk_level,
        self_harm_detected=final_sh_detected,
        keyword_score=kw_score,
        reasons=reasons  # could also add reasons from LLM if we extracted them
    )
    
    reply_text = llm_result.get("reply", "I am here for you.")
    
    # SAFETY OVERRIDE: If LLM failed (fallback used) AND risk is high, provide safe crisis message
    if reply_text == ai_agent.FALLBACK_ERROR_MESSAGE and final_risk_level in ["high", "critical"]:
        reply_text = "I hear that you are in pain. Please reach out for help immediately – you are not alone. I’ve listed some resources below."

    db.save_message(request.user_id, "assistant", reply_text)

    return {
        "reply": reply_text,
        "risk_level": final_risk_level,
        "self_harm_detected": final_sh_detected,
        "advice": llm_result.get("advice", []),
        "actions": actions,
        "timestamp": datetime.utcnow().isoformat()
    }

# -----------------------------
# Daily Check-in Endpoints
# -----------------------------
@app.get("/checkin/today", response_model=CheckinQuestionsResponse)
def get_checkin_questions(user_id: str):
    # In a real app we might check if they already submitted today
    return {
        "date": date.today().isoformat(),
        "questions": [
            "How are you feeling right now (1–10)?",
            "What was the strongest emotion you felt today?",
            "What triggered stress or anxiety today?",
            "Did you sleep well last night?",
            "Name one thing that helped you get through today.",
            "Have you had any thoughts of hurting yourself?"
        ]
    }

@app.post("/checkin/submit", response_model=CheckinSubmitResponse)
def submit_checkin(request: CheckinSubmitRequest):
    # 1. Summarize with LLM
    summary_result = ai_agent.summarize_day_llm(request.answers)
    
    # 2. Save Daily Summary
    db.save_daily_summary(
        user_id=request.user_id,
        date=date.today().isoformat(),
        summary_text=summary_result.get("daily_summary", "Summary unavailable."),
        risk_level=summary_result.get("risk_level", "low")
    )
    
    # 3. Determine Actions based on summary risk
    actions = risk_engine.get_actions(summary_result.get("risk_level", "low"))

    return {
        "daily_summary": summary_result.get("daily_summary", ""),
        "risk_level": summary_result.get("risk_level", "low"),
        "self_harm_detected": summary_result.get("self_harm_detected", False),
        "advice": summary_result.get("advice", []),
        "actions": actions
    }
