import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="SentinelAgent Dashboard", layout="wide")

st.title("🛡️ SentinelAgent - Behavior Drift Monitor")
st.caption("Real-time monitoring of AI Agent behavior against declared RBAC")

PROXY = "http://127.0.0.1:8000"

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Active Sessions")
    try:
        resp = requests.get(f"{PROXY}/sessions")
        sessions = resp.json()
        if sessions:
            df = pd.DataFrame(sessions)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No active sessions yet. Run the mock agent.")
    except Exception as e:
        st.error(f"Cannot connect to proxy: {e}")
        st.stop()
    
    st.subheader("Session Trace")
    if sessions:
        sid = st.selectbox("Select Session", [s["session_id"] for s in sessions])
        if st.button("Refresh Trace"):
            try:
                tr = requests.get(f"{PROXY}/sessions/{sid}/trace")
                trace = tr.json()
                st.write(f"**Entropy:** {trace['entropy']}")
                st.write("**Call History:**")
                for i, call in enumerate(trace['calls']):
                    st.text(f"{i+1}. {call['tool']} | args={call['args']}")
            except Exception as e:
                st.error(str(e))

with col2:
    st.subheader("Live Risk Analysis")
    st.markdown("""
    **Legend:**
    - 🟢 ALLOW - Within expected behavior
    - 🟡 DOWNGRADE - Drift detected, privileges reduced
    - 🔴 BLOCK - High risk, call blocked (No token revocation)
    """)
    
    st.info("Run `python agent_mock/test_agent.py` in another terminal to see live data populate.")
    
    st.subheader("How it works")
    st.markdown("""
    1. **Proxy Interception** - All tool calls routed through SentinelAgent
    2. **RBAC Check** - Compare against declared role & allowed tools
    3. **Trajectory Analysis** - Track call-tree & compute entropy
    4. **Anomaly Detection** - Rule-based risk scoring (MVP)
    5. **Automated Mitigation** - Downgrade or block without revoking OAuth tokens
    """)
    
    st.caption("Team Loosers | Faahd Syed • Hamzah Shaikh • Alston Miranda • Ashutosh Sononey")
