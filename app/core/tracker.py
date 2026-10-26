import math
from collections import defaultdict, Counter
from typing import Dict, Any

class CallTracker:
    def __init__(self):
        # session_id -> {tree: list of calls, parents: ...}
        self.sessions = {}
    
    def start_session(self, session_id: str, agent_role: str, declared_goal: str = ""):
        self.sessions[session_id] = {
            "agent_role": agent_role,
            "declared_goal": declared_goal,
            "calls": [],
            "call_tree": [],
            "current_parent": None
        }
        return self.sessions[session_id]
    
    def log_call(self, session_id: str, tool: str, args: Dict[str, Any] = None, parent_id: str = None):
        if session_id not in self.sessions:
            self.start_session(session_id, "unknown")
        call = {
            "tool": tool,
            "args": args or {},
            "parent_id": parent_id,
            "risk_contribution": 0
        }
        self.sessions[session_id]["calls"].append(call)
        self.sessions[session_id]["call_tree"].append(call)
        return call
    
    def get_calls(self, session_id: str):
        if session_id not in self.sessions:
            return []
        return self.sessions[session_id]["calls"]
    
    def entropy(self, session_id: str):
        calls = self.get_calls(session_id)
        if not calls:
            return 0.0
        # frequency distribution of tools
        cnt = Counter(c["tool"] for c in calls)
        n = len(calls)
        ent = 0.0
        for _, c in cnt.items():
            p = c / n
            if p > 0:
                ent -= p * math.log2(p)
        return round(ent, 4)

tracker = CallTracker()
