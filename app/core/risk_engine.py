from typing import Dict, Any
from app.core.tracker import tracker
from app.core.rbac import rbac

SUSPICIOUS_CHAINS = [
    {"read_secrets", "email_data", "exfiltrate"},
    {"read_file", "send_email"},
    {"read_logs", "external_upload"},
]

class RiskEngine:
    def __init__(self):
        self.threshold_block = 80
        self.threshold_downgrade = 50
    
    def assess(self, session_id: str, agent_role: str, tool: str, args: Dict[str, Any] = None, tier: str = "low") -> Dict[str, Any]:
        args = args or {}
        score = 0
        reasons = []
        
        # unknown role
        if not rbac.get_role(agent_role):
            score += 25
            reasons.append("Unknown agent role")
        
        # out of role
        if not rbac.is_allowed(agent_role, tool, tier):
            score += 30
            reasons.append(f"Tool '{tool}' not in allowlist for role '{agent_role}'")
        
        # suspicious tools
        high_risk_tools = {"read_secrets", "exfiltrate", "external_upload", "delete_backup"}
        if tool in high_risk_tools:
            score += 15
            reasons.append(f"High-risk tool attempted: {tool}")
        
        # call tree entropy
        ent = tracker.entropy(session_id)
        if ent > 1.2:  # more diverse than normal
            score += 10
            reasons.append(f"Call-tree entropy spike ({ent})")
        if ent > 1.8:
            score += 10
            reasons.append(f"Unusually chaotic call pattern ({ent})")
        
        # check recent chain
        calls = tracker.get_calls(session_id)
        recent = [c["tool"] for c in calls[-5:]]
        recent_set = set(recent)
        for chain in SUSPICIOUS_CHAINS:
            if chain.issubset(recent_set):
                score += 25
                reasons.append(f"Suspicious tool-chain detected: {chain}")
                break
        
        # rapid fire
        if len(calls) >= 6 and ent > 1.0:
            score += 5
            reasons.append("Rapid tool chaining observed")
        
        score = min(score, 100)
        return {"risk_score": score, "reasons": reasons, "entropy": ent}
    
    def action_for(self, score: int) -> str:
        if score >= self.threshold_block:
            return "BLOCK"
        if score >= self.threshold_downgrade:
            return "DOWNGRADE"
        return "ALLOW"

risk_engine = RiskEngine()
