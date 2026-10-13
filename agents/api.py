"""
FastAPI REST API Server for Hereditary Cancer Syndrome Agent.
"""
import os
import secrets
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Hereditary Cancer Syndrome Agent API",
    description="Illustrative numeric rule engine for synthetic inputs; not a clinical decision-support tool.",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "hereditary-cancer-syndrome-agent", "domain": "Clinical & Biomedical AI", "standard": "Illustrative rules (not validated clinical criteria)", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "DEMONSTRATION_RUNNING"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException:
        raise HTTPException(status_code=422, detail="Identifier pattern rejected in request") from None
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except (ValueError, SecurityException):
        raise HTTPException(status_code=400, detail="Invalid chat request")


@app.get("/api/audit/logs")
def api_audit_logs(x_audit_token: Optional[str] = Header(default=None)):
    configured = os.environ.get("AUDIT_API_TOKEN")
    if not configured or not x_audit_token or not secrets.compare_digest(x_audit_token, configured):
        raise HTTPException(status_code=403, detail="Audit log access disabled or unauthorized")
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
