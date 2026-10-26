import json
from datetime import datetime

class Logger:
    def __init__(self, log_file: str = "sentinel_logs.jsonl"):
        self.log_file = log_file
    
    def log(self, event: dict):
        event["logged_at"] = datetime.utcnow().isoformat()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + "\n")
        return event

logger = Logger()
