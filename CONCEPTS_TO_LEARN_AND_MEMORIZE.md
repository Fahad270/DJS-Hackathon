# CONCEPTS TO LEARN AND MEMORIZE

This file is made specifically for **Team Loosers** to revise before judging, viva, or just to lock these concepts in long-term.

## 1) AI Agent Security Basics

| Concept | Explanation | Memory Tip |
|---|---|---|
| **Tool-Using Agents** | Agents that can call external tools (APIs, files, emails) to take actions. | *"Chatbot talks, Agent acts"* |
| **RBAC (Role-Based Access Control)** | Give tools based on role. e.g. Research agent shouldn't send emails. | *"Right tool to right role"* |
| **Least Privilege** | Give minimum permissions needed, nothing extra. | *"Only what is strictly necessary"* |
| **Zero Trust** | Never trust by default. Continuously verify every action. | *"Never trust, always verify"* |
| **Valid Token != Safe** | Having OAuth token doesn't mean agent isn't hijacked. | *"Identity is not intent"* |

## 2) Prompt Injections

| Concept | Explanation | Memory Tip |
|---|---|---|
| **Direct Prompt Injection** | Malicious instruction in user's prompt to override system prompt. | *"Injected via user"* |
| **Indirect Prompt Injection (IPI)** | Hidden malicious instructions inside external data (email, PDF, website, RAG docs). Agent reads it and follows. | *"Injected via data"* |
| **Prompt Injection vs Jailbreak** | Injection = hijack instructions. Jailbreak = bypass safety filters. Often overlap. | *"Hijack vs bypass"* |
| **Data Exfiltration** | Stealing sensitive data and sending it outside (email/upload). | *"Data leaving where it shouldn't"* |

## 3) Behavioral Monitoring & Drift

| Concept | Explanation | Memory Tip |
|---|---|---|
| **Behavioral Drift** | Agent slowly deviates from its original purpose/role over time or after injection. | *"From helper to intruder"* |
| **Execution Trajectory** | The full sequence/path of actions taken by agent (tool call order). | *"Footprint of actions"* |
| **Baseline Behavior** | Expected normal pattern for a given role/goal. Anything away from it is suspicious. | *"Know normal to spot abnormal"* |
| **Anomaly Detection** | Finding patterns that don't match expected/normal behavior. | *"Outlier = suspicious"* |

## 4) Call-Tree, Entropy & Metrics

| Concept | Explanation | Memory Tip |
|---|---|---|
| **Call-Tree** | Tree/graph of tool calls showing parent-child relationships. Helps see chaining. | *"Family tree of actions"* |
| **Tool Chaining** | Using multiple tools in sequence to achieve something. Can be benign or malicious. | *"Chain reaction"* |
| **Shannon Entropy (Info Theory)** | Measures uncertainty/randomness. High entropy = more diverse/unpredictable tool usage. Low entropy = repetitive/predictable. | *"Chaos meter"* |
| **Embedding** | Numeric vector representation of text (captures meaning). Used to compare semantic similarity. | *"Meaning as numbers"* |
| **Embedding-Space Distance** | How far apart meanings are. Large distance = agent's actions semantically drift from declared goal. | *"Far from goal = drift"* |
| **Feature Engineering** | Converting raw data (calls, order, freq) into numbers ML can use. | *"Turning behavior into math"* |

## 5) ML Concepts Used/Related

| Concept | Explanation | Memory Tip |
|---|---|---|
| **IsolationForest** | Unsupervised ML that isolates anomalies. Anomalies need fewer splits to be isolated -> flagged. Great when you don't have labeled attacks. | *"Weird things stand out faster"* |
| **Unsupervised Learning** | Learn patterns from unlabeled data (just normal logs). Find outliers. | *"No attack labels needed"* |
| **Supervised Learning** | Train on labeled "normal" vs "malicious". Needs datasets. | *"Teach with examples"* |
| **Thresholding** | Decide ALLOW/DOWNGRADE/BLOCK based on risk score (e.g. >=50, >=80). | *"Cutoff point"* |
| **False Positive vs False Negative** | FP = Block legit (annoying). FN = Miss attack (dangerous). For security, better slightly strict. | *"Safety vs UX"* |

## 6) Proxy, Mitigation & Systems

| Concept | Explanation | Memory Tip |
|---|---|---|
| **Reverse Proxy / Middleware** | Intercepts requests between client and server. Can inspect, allow, block, modify. | *"Gatekeeper in the middle"* |
| **API Gateway** | Central point to route, auth, rate-limit, monitor APIs. Similar idea. | *"Single entry point"* |
| **Containment** | Isolate/restrict threat without destroying everything. | *"Quarantine, don't nuke"* |
| **Privilege Downgrade** | Reduce permissions (high->med->low/restricted) on detecting drift. | *"Handcuff the agent"* |
| **Token Revocation** | Invalidate credentials. Effective but disruptive. SentinelAgent avoids this. | *"Pulling the plug"* |
| **Session-based Tracking** | Track per session_id to see full trajectory. | *"Follow the trail"* |
| **Explainability** | Show *"WHY"* blocked (reasons list). Critical for trust/demo. | *"Show your work"* |

## 7) Key Ideas To Explain In Viva

1. **Why not just filter prompts?** - Indirect prompt injections come via external data. Input/output filters miss them. We need *behavioral* detection.
2. **Why proxy?** - We need visibility over *actions* (tool calls). Can't just look at text.
3. **Why no token revocation?** - Business continuity. Contain the compromised agent without breaking legit workflows.
4. **Why entropy?** - Legitimate agents tend to follow predictable patterns. Hijacked ones go off-script with weird tool mixes.
5. **Why call-tree?** | Malicious chains often follow a pattern (read -> collect -> exfiltrate). Alone tools might seem okay, chain is suspicious.
6. **Zero Trust for Agents** - Every tool call must earn trust based on role + behavior.

## 8) Quick Revision Questions

- **Q:** What problem does SentinelAgent solve?  
  **A:** Detects agent behavior drift from declared role via proxy + trajectory analysis and contains without revoking tokens.

- **Q:** Difference between direct and indirect prompt injection?  
  **A:** Direct = in user prompt. Indirect = in external data read by agent.

- **Q:** What is call-tree entropy?  
  **A:** Measure of randomness/diversity in tool usage sequence for a session.

- **Q:** Why use IsolationForest later?  
  **A:** Unsupervised, learns normal from data, flags outliers without needing huge labeled attack sets.

- **Q:** ALLOW/DOWNGRADE/BLOCK logic?  
  **A:** Based on weighted risk score from RBAC + history + entropy + chains.

## 9) Flashcard Style One-Liners
- **Proxy** = Gatekeeper
- **Entropy** = Chaos
- **Drift** = Going off-track
- **Containment** = Restrict not destroy
- **Trajectory** = Path taken
- **IPI** = Trojan via data
- **Zero Trust** = Verify always

## Pro Tip
Don't just memorize definitions. Understand **"WHY"**. For every concept, ask yourself - *"How does this help catch a hijacked agent?"* If you can answer that, you're solid.
