import streamlit as st
import asyncio

from agents.council.orchestrator import run_multi_llm_council
from utils.clipboard import copy_button
from utils.formatting import format_final_plan
from agents.council.orchestrator import run_resume_gap_analysis_async

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="LLM Council Career Planner",
    layout="wide"
)

if "career_plan" not in st.session_state:
    st.session_state.career_plan = None

if "content_plan" not in st.session_state:
    st.session_state.content_plan = None


st.title("🚀 LLM Council Career Planner")
st.caption(
    "Top LLMs (GPT, Grok, Gemini) debate, agree, and recommend the best roadmap and learning content for your next role."
)

# ----------------------------
# Input Form
# ----------------------------
with st.form("career_form"):
    current_role = st.text_input(
        "Current Role",
        placeholder="Software Engineer"
    )

    years_exp = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=40,
        step=1
    )

    target_role = st.text_input(
        "Target Role",
        placeholder="Senior / Staff / AI Engineer"
    )

    submit = st.form_submit_button("Generate Career Plan")

# ----------------------------
# Execution
# ----------------------------
if submit:
    if not current_role or not target_role:
        st.warning("Please provide both current role and target role.")
        st.stop()

    with st.spinner("🧠 LLM Council is debating your career roadmap..."):
        career_plan_raw, content_plan_raw = run_multi_llm_council(
            current_role=current_role,
            target_role=target_role,
            years_exp=years_exp
        )

    # ---- FORMAT & STORE ----
    st.session_state.career_plan = format_final_plan(career_plan_raw)
    st.session_state.content_plan = content_plan_raw.strip()



    # ---- DISPLAY ----
    st.subheader("📌 Final Agreed Career Roadmap")
    st.write(st.session_state.career_plan)


    st.subheader("🎓 Best Learning Resources (Top Rated & Popular)")
    st.write(st.session_state.content_plan)

    # =============================
    # Resume Gap Analysis (SAFE)
    # =============================
    # =============================
st.subheader("📄 Resume Gap Analysis")

uploaded_resume = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

run_comparison = st.button(
    "🔍 Compare Resume with Target Role",
    disabled=not uploaded_resume or not st.session_state.career_plan
)

if run_comparison:
    with st.spinner("Comparing resume against target role..."):
        gap_analysis, resume_improvements = asyncio.run(
            run_resume_gap_analysis_async(
                uploaded_file=uploaded_resume,
                career_plan=st.session_state.career_plan
            )
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Target Role Expectations")
        st.write(st.session_state.career_plan)

    with col2:
        st.subheader("📄 Resume Gap Analysis")
        st.write(gap_analysis)

    st.subheader("✍️ Resume Improvement Suggestions")
    st.write(resume_improvements)
