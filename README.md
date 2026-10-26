# TEAM LOOSERS - Project Info

## Team Details
- **Team Name:** TEAM LOOSERS
- **Team Members:**
  1. Fahad Syed
  2. Hamzah Shaikh
  3. Alston Miranda
  4. Ashutosh Sononey

- **Project Title:** SentinelAgent – Dynamic Identity & Behavior Drift Monitor for Autonomous AI

## Problem Statement
In current AI agent ecosystems, once an agent is issued a valid OAuth token with a specific RBAC role, it is implicitly trusted to perform any action allowed by that role. However, this "trust by identity" model is fundamentally broken. 

Through **Indirect Prompt Injections**, malicious instructions hidden in data (emails, files, websites) can hijack a benign agent and force it to carry out malicious tasks like reading secrets, exfiltrating data, or calling sensitive APIs - all while still using its valid credentials.

Worse still, the conventional response is to **revoke tokens** which kills the entire session/workflow causing major disruption.

## Aim
To build a real-time behavioral monitoring proxy that cross-checks an autonomous agent's execution trajectory against its declared role and intent, and **automatically contains threats by dynamically downgrading privileges or blocking high-risk calls without revoking OAuth tokens.**

## What is SentinelAgent?
SentinelAgent acts as a **zero-trust behavioral firewall** for tool-using AI agents. It sits between the agent and its tool/APIs, inspects every tool call in real-time, builds a live call-tree, calculates risk based on role compliance, call entropy and suspicious chaining, and mitigates in under reasonable time without breaking authentication.

## Unique Selling Proposition (USP)
- **Containment without Revocation** - Downgrade privilege tiers or block specific calls instead of killing auth.
- **Trajectory-Based Detection** - Focuses on *"what is the agent doing?"* not just *"what did it say?"*. Catches indirect prompt injections missed by input filters.
- **Call-Tree Entropy Analysis** - Measures chaos/randomness in tool usage to detect drift.
- **Multi-Signal Risk Scoring** - Combines RBAC, tool risk, entropy, and suspicious chains.
- **Real-Time Automated Mitigation** - Instant response with clear reasoning shown on dashboard.
- **Demo-Friendly & Explainable** - Rule-based MVP that judges can easily understand.

## Key Features
- **Proxy Middleware** - Intercepts all agent-tool invocations
- **Role-Based Access Control (RBAC)** - Enforce per-role allowlists
- **Call-Tree Tracking** - Build live execution graph per session
- **Behavioral Drift Detection** - Detect deviation from declared goal/role
- **Risk Engine** - Weighted scoring with explainable reasons
- **Mitigator** - Dynamic privilege downgrade or hard block
- **Live Dashboard** - Visualize sessions, traces, entropy, risk & actions
- **Mock Agent** - Test normal vs malicious drift instantly

## Tech Stack
| Layer | Technology | Purpose |
|---|---|---|
| **Backend/Proxy** | FastAPI, Uvicorn, Pydantic | High-performance async proxy API |
| **RBAC & Config** | JSON | Role definitions & allowlists |
| **Tracking & Logic** | Python (collections, math) | Call-tree, entropy, risk scoring |
| **ML Ready (Stretch)** | scikit-learn, sentence-transformers | For future IsolationForest & embedding drift |
| **Frontend/Dashboard** | Streamlit, Pandas | Real-time visualization |
| **HTTP** | Requests | Mock agent <-> proxy communication |

## Architecture Overview
```
[AI Agent] -> [SentinelAgent Proxy :8000] -> [Tools/APIs]
                    |                        ^
                    v                        |
                [RBAC] [Tracker] [RiskEngine] [Mitigator]
                    \      |        |        /
                     \     |        |       /
                        [Live Dashboard :8501]
```

## How It Works (Step by Step)
1. **Register** - Agent registers with its `agent_role` and `declared_goal` via `/register`
2. **Intercept** - Every tool call goes to `POST /invoke`
3. **Log** - Call added to session's call-tree
4. **Verify** - RBAC checks if tool allowed for role/current tier
5. **Analyze** - Risk engine computes score using role, entropy, chains, history
6. **Decide** - ALLOW / DOWNGRADE / BLOCK based on thresholds
7. **Mitigate** - If downgrade/block, apply without token revocation
8. **Monitor** - Dashboard shows everything live

## Demo Flow
1. Start Proxy (`run_proxy.bat`)
2. Start Dashboard (`run_dashboard.bat`) 
3. Run Mock Agent (`run_test_agent.bat`)
   - First test: Normal behavior (web_search, summarize_text, read_file) -> mostly ALLOW
   - Second test: Drift to malicious (read_secrets, email_data, exfiltrate) -> RISK rises -> DOWNGRADE/BLOCK with reasons

## File Structure
```
DJ-HACK/
├── app/ (proxy core: config, core logic, main, utils)
├── agent_mock/ (test agent)
├── dashboard/ (streamlit UI)
├── run_*.bat (quick start scripts)
├── requirements.txt
├── .env.example
└── MD files (this one + concepts file)
```

## Future Scope
- Integrate **IsolationForest** for unsupervised anomaly detection
- Use **sentence-transformers** to compute embedding distance from declared goal
- Add **session replay & forensic logs**
- Support **OPA (Open Policy Agent)** style policies
- Add **JWT/OAuth introspection** for real agents
- Export alerts to SIEM
- Graph-based visualization of call-tree

## GitHub Push Checklist
- [ ] Remove `.env` if created, use `.env.example`
- [ ] Add `__pycache__/`, `*.pyc`, `venv/`, `.streamlit/` to `.gitignore`
- [ ] Write clear README with setup + demo
- [ ] Add screenshots/gif of dashboard
- [ ] Commit with meaningful messages
- [ ] Add MIT/appropriate license if desired

## Credits
**Team Loosers** - Built with a lot of late night chaos, caffeine and the goal to actually learn something new. 

*"Trust, but verify. Or better - never trust, continuously verify."*
