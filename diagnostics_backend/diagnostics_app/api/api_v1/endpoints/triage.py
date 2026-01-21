from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional
from diagnostics_backend.diagnostics_app.api import deps
from diagnostics_backend.diagnostics_app.services.triage_orchestrator import TriageOrchestrator
from diagnostics_backend.diagnostics_app.models.schemas import TriageInputText, SessionResponse, TriageResponse, AnswerInput

router = APIRouter()

@router.post("/text", response_model=TriageResponse)
async def triage_text(
    input_data: TriageInputText,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Start a triage session with text symptoms.
    """
    orchestrator = TriageOrchestrator(db)
    session = await orchestrator.create_session()
    
    result = await orchestrator.process_text_triage(
        session.id, 
        input_data.symptoms, 
        severity=input_data.severity, 
        duration=input_data.duration
    )
    return result

@router.post("/image", response_model=TriageResponse)
async def triage_image(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Start or continue a triage session with an image.
    If session_id is provided, appends image to that session.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    orchestrator = TriageOrchestrator(db)
    # We do NOT create session manually here anymore if passing to orchestrator which handles it,
    # OR we keep logic consistent. Orchestrator process_image_triage now accepts session_id (opt).
    
    image_bytes = await file.read()
    result = await orchestrator.process_image_triage(session_id, image_bytes)
    return result

@router.post("/session/{session_id}/answer", response_model=TriageResponse)
async def triage_answer(
    session_id: str,
    answer_data: AnswerInput,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Answer a follow-up question to advance the session.
    """
    orchestrator = TriageOrchestrator(db)
    
    # Verify session exists
    session = await orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await orchestrator.process_answer(session_id, answer_data.answer)
    return result

@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get current state of a triage session.
    """
    orchestrator = TriageOrchestrator(db)
    session = await orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/session/{session_id}/text", response_model=TriageResponse)
async def triage_session_text(
    session_id: str,
    input_data: TriageInputText,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Add text symptoms to an existing session (multi-turn).
    """
    orchestrator = TriageOrchestrator(db)
    
    # Verify session exists
    session = await orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await orchestrator.process_session_text(
        session_id, 
        input_data.symptoms
    )
    return result
