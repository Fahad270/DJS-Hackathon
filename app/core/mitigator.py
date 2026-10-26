from typing import Dict, Any

class Mitigator:
    def __init__(self):
        self.tier_order = ["low", "med", "high"]
    
    def downgrade(self, current_tier: str = "low") -> str:
        try:
            idx = self.tier_order.index(current_tier)
            if idx == 0:
                # already lowest, can be restricted further conceptually
                return "restricted"
            return self.tier_order[idx-1]
        except ValueError:
            return "restricted"
    
    def mitigate(self, action: str, current_tier: str = "low") -> Dict[str, Any]:
        if action == "BLOCK":
            return {"action": "BLOCK", "new_tier": current_tier, "mitigation": "Call blocked - high risk"}
        elif action == "DOWNGRADE":
            new_tier = self.downgrade(current_tier)
            return {"action": "DOWNGRADE", "new_tier": new_tier, "mitigation": f"Privileges downgraded {current_tier} -> {new_tier}"}
        else:
            return {"action": "ALLOW", "new_tier": current_tier, "mitigation": "Allowed"}

mitigator = Mitigator()
