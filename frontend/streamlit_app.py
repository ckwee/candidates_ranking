import streamlit as st
import requests
import json

# ============================
# CONFIG
# ============================
BACKEND_URL = "http://localhost:8000"   # Change if backend is remote

st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide"
)

st.title("⚙️ AI Recruitment Screener")
st.write("Upload a Job Description and candidate resumes to evaluate them using the backend pipeline.")


# ============================
# SIDEBAR SETTINGS
# ============================
with st.sidebar:
    st.header("🔧 Backend Settings")
    backend_url = st.text_input("Backend URL", BACKEND_URL)
    st.markdown("---")
    st.caption("Ensure your FastAPI backend is running before using the app.")


# ============================
# FILE UPLOADS
# ============================
st.subheader("📄 Upload Job Description")
jd_file = st.file_uploader("Upload JD (.pdf or .docx)", type=["pdf", "docx"])

st.subheader("👥 Upload Candidate Resumes")
resume_files = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

run_button = st.button("🚀 Run Screening", type="primary")


# ============================
# PIPELINE EXECUTION
# ============================
if run_button:
    if not jd_file:
        st.error("Please upload a Job Description file.")
        st.stop()

    if not resume_files:
        st.error("Please upload at least one resume.")
        st.stop()

    # --------------------------
    # 1. Analyze JD
    # --------------------------
    with st.spinner("Analyzing Job Description..."):
        jd_resp = requests.post(
            f"{backend_url}/analyze_jd_file",
            files={"jd_file": (jd_file.name, jd_file.getvalue())}
        )

        if jd_resp.status_code != 200:
            st.error(f"JD analysis failed: {jd_resp.text}")
            st.stop()

        criteria = jd_resp.json()

    st.success("JD analyzed successfully!")

    # Display criteria
    with st.expander("📋 Extracted Job Criteria", expanded=True):
        st.json(criteria)

    # --------------------------
    # 2. Evaluate Resumes
    # --------------------------
    with st.spinner("Evaluating candidates..."):

        # IMPORTANT FIX:
        # criteria must be sent as a string, not JSON object
        data_payload = {
            "criteria": json.dumps(criteria)
        }

        files_payload = [
            ("resumes", (f.name, f.getvalue()))
            for f in resume_files
        ]

        eval_resp = requests.post(
            f"{backend_url}/evaluate_files",
            data=data_payload,
            files=files_payload
        )

        if eval_resp.status_code != 200:
            st.error(f"Candidate evaluation failed: {eval_resp.text}")
            st.stop()

        evaluations = eval_resp.json()

    st.success("Candidate evaluations completed!")

    # --------------------------
    # 3. Ranking
    # --------------------------
    with st.spinner("Ranking candidates..."):
        rank_resp = requests.post(
            f"{backend_url}/rank",
            json=evaluations
        )

        if rank_resp.status_code != 200:
            st.error(f"Ranking failed: {rank_resp.text}")
            st.stop()

        ranking = rank_resp.json()

    st.success("Ranking complete!")

    # ============================
    # DISPLAY RESULTS
    # ============================
    st.subheader("🏆 Final Candidate Rankings")

    for i, cand in enumerate(ranking, start=1):
        with st.expander(f"#{i} — {cand['candidate_name']} (Score: {cand['overall_score']})", expanded=(i == 1)):
            st.progress(cand["overall_score"] / 100)

            st.markdown(f"**Confidence:** {cand['confidence']}%")
            st.markdown(f"**Justification:** {cand['justification']}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🟢 Strengths")
                for s in cand["strengths"]:
                    st.markdown(f"- {s}")

            with col2:
                st.markdown("### 🔴 Weaknesses")
                for w in cand["weaknesses"]:
                    st.markdown(f"- {w}")

            st.markdown("### 📊 Category Scores")
            st.json(cand["category_scores"])
