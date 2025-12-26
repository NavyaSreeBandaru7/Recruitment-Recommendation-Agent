import os
import streamlit as st
import pandas as pd

from rragent.orchestrator import run_pipeline

st.set_page_config(page_title="Recruitment Recommendation Agent", layout="wide")
st.title("🧑‍💼 Recruitment Recommendation Agent (Multi-Agent)")
st.caption("Shortlists candidates with evidence + fairness checks. Human-in-the-loop only (no auto-reject).")

with st.sidebar:
    st.header("Scoring Weights")
    w_skill = st.slider("Skills match", 0, 100, 55, key="w_skill")
    w_resp  = st.slider("Responsibilities match", 0, 100, 25, key="w_resp")
    w_exp   = st.slider("Experience signals", 0, 100, 15, key="w_exp")
    w_other = st.slider("Other keywords", 0, 100, 5, key="w_other")

    top_k = st.slider("Show top K", 1, 20, 5, key="topk")

st.subheader("1) Paste Job Description (JD)")
jd_text = st.text_area("Job Description", height=220, key="jd_text")

st.subheader("2) Upload Candidate Resumes (.txt)")
files = st.file_uploader(
    "Upload one or more .txt resumes",
    type=["txt"],
    accept_multiple_files=True,
    key="resume_upload"
)

run_btn = st.button("Run Shortlisting", type="primary", use_container_width=True, key="run_btn")

if run_btn:
    if not jd_text.strip():
        st.error("Please paste a job description.")
        st.stop()
    if not files:
        st.error("Please upload at least one resume (.txt).")
        st.stop()

    candidates = []
    for f in files:
        text = f.read().decode("utf-8", errors="ignore")
        candidates.append({"candidate_id": f.name, "raw_text": text})

    weights = {"skill": w_skill, "resp": w_resp, "exp": w_exp, "other": w_other}

    with st.spinner("Running agents (Parser → Matcher → Evidence → Fairness → Narrator)..."):
        result = run_pipeline(jd_text=jd_text, candidates=candidates, weights=weights)

    st.success("Done ✅")

    # Ranking table
    st.subheader("Shortlist (ranked)")
    df = pd.DataFrame(result["ranked"])
    if not df.empty:
        show_cols = ["rank", "candidate_id", "score_total", "score_skill", "score_resp", "score_exp", "flags_count"]
        st.dataframe(df[show_cols].head(top_k), use_container_width=True)

    # Candidate drill-down
    st.subheader("Candidate Details")
    pick = st.selectbox("Select candidate", [r["candidate_id"] for r in result["ranked"]], key="candidate_pick")
    detail = next(x for x in result["ranked"] if x["candidate_id"] == pick)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Narrative Summary")
        st.write(detail["narrative"])

        st.markdown("### Fairness / Compliance Flags")
        if detail["flags"]:
            for fl in detail["flags"]:
                st.warning(fl)
        else:
            st.success("No fairness/compliance flags detected.")

    with c2:
        st.markdown("### Evidence (resume snippets supporting matches)")
        for ev in detail["evidence"][:12]:
            st.markdown(f"**{ev['jd_item']}**")
            st.code(ev["resume_snippet"])

    st.subheader("Trace Timeline (What each agent did)")
    for e in result["trace"]:
        with st.expander(f"{e['step']} — {e['agent']} — {e['status']}"):
            st.write(e["summary"])
            if e.get("details"):
                st.code(e["details"])
