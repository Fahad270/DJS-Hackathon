import requests
import time

PROXY = "http://127.0.0.1:8000"

def test_normal():
    print("[TEST] Normal behavior - research_assistant")
    r = requests.post(f"{PROXY}/register", json={"agent_role": "research_assistant", "declared_goal": "Summarize papers"})
    sid = r.json()["session_id"]
    print(f"Session: {sid}")
    
    # normal calls
    for tool in ["web_search", "summarize_text", "read_file"]:
        try:
            resp = requests.post(f"{PROXY}/invoke", json={"session_id": sid, "agent_role": "research_assistant", "tool": tool, "args": {"q": "test"}})
            print(f"  {tool} -> {resp.json()['action']} (risk={resp.json()['risk_score']})")
        except Exception as e:
            print(f"  {tool} -> ERROR")
        time.sleep(0.5)
    
    print()

def test_malicious():
    print("[TEST] Malicious drift - research_assistant trying to exfiltrate")
    r = requests.post(f"{PROXY}/register", json={"agent_role": "research_assistant", "declared_goal": "Summarize papers"})
    sid = r.json()["session_id"]
    print(f"Session: {sid}")
    
    # start normal
    for tool in ["web_search", "read_file"]:
        try:
            resp = requests.post(f"{PROXY}/invoke", json={"session_id": sid, "agent_role": "research_assistant", "tool": tool, "args": {}})
            print(f"  {tool} -> {resp.json()['action']} (risk={resp.json()['risk_score']})")
        except Exception as e:
            print(f"  {tool} -> ERROR")
        time.sleep(0.3)
    
    # drift to malicious
    malicious = ["read_secrets", "email_data", "exfiltrate"]
    for tool in malicious:
        try:
            resp = requests.post(f"{PROXY}/invoke", json={"session_id": sid, "agent_role": "research_assistant", "tool": tool, "args": {"target": "internal"}})
            print(f"  {tool} -> {resp.json()['action']} (risk={resp.json()['risk_score']})")
        except Exception as e:
            try:
                print(f"  {tool} -> BLOCKED (risk={e.response.json()['detail']['risk_score']})")
            except:
                print(f"  {tool} -> BLOCKED")
        time.sleep(0.3)
    
    print()

if __name__ == "__main__":
    print("="*50)
    print("SentinelAgent Mock Agent Demo")
    print("="*50)
    test_normal()
    test_malicious()
    print("="*50)
    print("Demo complete. Check dashboard at http://localhost:8501")
    print("="*50)
