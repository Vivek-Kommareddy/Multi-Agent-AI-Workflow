import time

import requests
import streamlit as st

st.title("Multi-Agent Research Demo")
api_base = st.sidebar.text_input("API Base URL", "http://localhost:8000")
workflow = st.selectbox("Workflow", ["research_report", "competitive_analysis", "literature_review"])
topic = st.text_input("Topic", "AI impact on healthcare")

if st.button("Start Research"):
    response = requests.post(f"{api_base}/research", json={"topic": topic, "workflow": workflow}, timeout=20)
    response.raise_for_status()
    st.session_state["job_id"] = response.json()["job_id"]

job_id = st.session_state.get("job_id")
if job_id:
    status_slot = st.empty()
    log_slot = st.empty()
    for _ in range(60):
        status = requests.get(f"{api_base}/status/{job_id}", timeout=20).json()
        status_slot.info(f"Status: {status['status']} | {status['progress']}%")
        log_slot.json(status.get("log", [])[-5:])
        if status["status"] == "completed":
            break
        time.sleep(0.5)
    result = requests.get(f"{api_base}/results/{job_id}", timeout=20).json()
    report = result.get("report", "")
    st.markdown(report)
    st.download_button("Download report", data=report, file_name="report.md")
    with st.expander("Artifacts"):
        st.json(result.get("artifacts", {}))
