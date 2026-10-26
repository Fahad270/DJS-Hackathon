from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time
import uuid

from app.core.tracker import tracker
from app.core.rbac import rbac
from app.core.risk_engine import risk_engine
from app.core.mitigator import mitigator

app = FastAPI(title="SentinelAgent - Dynamic Identity & Behavior Drift Monitor", version="0.1.0")

# in-memory session state
SESSIONS = {}

class InvokeRequest(BaseModel):
    session_id: Optional[str] = None
    agent_role: str
    tool: str
    args: Optional[Dict[str, Any]] = {}
    declared_goal: Optional[str] = ""
    tier: Optional[str] = "low"

class RegisterRequest(BaseModel):
    agent_role: str
    declared_goal: Optional[str] = ""
    tier: Optional[str] = "low"

@app.get("/")
def root():
    return {"status": "ok", "service": "SentinelAgent Proxy", "msg": "Send POST /invoke to proxy agent tool calls"}

@app.post("/register")
def register(req: RegisterRequest):
    sid = str(uuid.uuid4())[:8]
    tracker.start_session(sid, req.agent_role, req.declared_goal)
    SESSIONS[sid] = {"agent_role": req.agent_role, "declared_goal": req.declared_goal, "tier": req.tier}
    return {"session_id": sid, "status": "registered", "role": req.agent_role, "tier": req.tier}

@app.post("/invoke")
def invoke(req: InvokeRequest):
    sid = req.session_id or str(uuid.uuid4())[:8]
    if sid not in tracker.sessions:
        tracker.start_session(sid, req.agent_role, req.declared_goal)
        SESSIONS[sid] = {"agent_role": req.agent_role, "declared_goal": req.declared_goal, "tier": req.tier or "low"}
    
    # log call first for chain analysis
    tracker.log_call(sid, req.tool, req.args)
    current_tier = SESSIONS.get(sid, {}).get("tier", req.tier or "low")
    
    # assess risk
    assessment = risk_engine.assess(sid, req.agent_role, req.tool, req.args, current_tier)
    risk_score = assessment["risk_score"]
    reasons = assessment["reasons"]
    entropy = assessment["entropy"]
    
    # decide action
    action = risk_engine.action_for(risk_score)
    mitigation = mitigator.mitigate(action, current_tier)
    
    # update tier if downgraded
    if mitigation["action"] == "DOWNGRADE":
        SESSIONS[sid]["tier"] = mitigation["new_tier"]
    elif mitigation["action"] == "BLOCK":
        # don't actually execute - blocked
        pass
    
    result = {
        "session_id": sid,
        "agent_role": req.agent_role,
        "tool": req.tool,
        "tier_before": current_tier,
        "tier_after": mitigation["new_tier"],
        "risk_score": risk_score,
        "entropy": entropy,
        "reasons": reasons,
        "action": mitigation["action"],
        "mitigation": mitigation["mitigation"],
        "allowed": mitigation["action"] != "BLOCK",
        "timestamp": time.time()
    }
    
    if mitigation["action"] == "BLOCK":
        raise HTTPException(status_code=403, detail=result)
    
    # Simulate successful tool execution
    result["execution"] = {"status": "executed", "output": f"[SIMULATED] {req.tool} executed with args {req.args}"}
    return result

@app.get("/sessions")
def sessions():
    out = []
    for sid, sess in SESSIONS.items():
        out.append({
            "session_id": sid,
            "agent_role": sess.get("agent_role"),
            "declared_goal": sess.get("declared_goal"),
            "tier": sess.get("tier"),
            "call_count": len(tracker.get_calls(sid)),
            "entropy": tracker.entropy(sid)
        })
    return out

@app.get("/sessions/{session_id}/trace")
def trace(session_id: str):
    if session_id not in tracker.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "calls": tracker.get_calls(session_id),
        "entropy": tracker.entropy(session_id)
    }
