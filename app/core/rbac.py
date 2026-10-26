import json
import os
from typing import Dict, Any

class RBAC:
    def __init__(self, config_path: str = "app/config/roles.json"):
        self.config_path = config_path
        self.roles = self.load()
    
    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # map by role name
        out = {}
        for r in data:
            out[r['role']] = r
        return out
    
    def get_role(self, role_name: str):
        return self.roles.get(role_name)
    
    def is_allowed(self, role_name: str, tool: str, tier: str = None):
        role = self.get_role(role_name)
        if not role:
            return False
        tier = tier or role.get('default_tier', 'low')
        if tool in role.get('allowed_tools', []):
            return True
        return False
    
    def allowed_tools(self, role_name: str):
        role = self.get_role(role_name)
        if not role:
            return []
        return role.get('allowed_tools', [])

rbac = RBAC()
