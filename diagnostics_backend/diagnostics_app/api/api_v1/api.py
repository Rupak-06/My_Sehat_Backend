from fastapi import APIRouter
from diagnostics_backend.diagnostics_app.api.api_v1.endpoints import triage

api_router = APIRouter()
api_router.include_router(triage.router, prefix="/triage", tags=["triage"])
