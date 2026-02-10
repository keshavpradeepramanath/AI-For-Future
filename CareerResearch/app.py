import asyncio
import streamlit as st

from agents.council.orchestrator import run_multi_llm_council
from agents.resume.resume_gap_chair import generate_resume_improvements
from agents.resume.resume_analyzer import analyze_resume_against_plan
from agents.resume.resume_parser import parse_resume
from agents.roadmap.roadmap_generator import generate_60_day_roadmap
from agents.roadmap.roadmap_to_excel import roadmap_to_excel

from utils.clipboard import copy_button
from utils.formatting import format_final_plan

# -------------------------------------------------
# Session State Initialization (CRITICAL)
# -------------------------------------------------
for key in [
    "career_plan",
    "content_plan",
    "gap_analysis",
    "resume_improvements",
    "roadmap_text",
]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="LLM Council Career Planner",
    layout="wide"
)

st.title("🚀 LLM Council Career Planner")
st.caption(
    "GPT + Grok + Gemini debate, agree, and help you execute your next career move."
)

# -------------------------------------------------
# Career Plan Form
# -------------------------------------------------
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

    # ✅ NO key here
    submit = st.form_submit_button("Generate Career Plan")

# -------------------------------------------------
# Generate Career Plan
# -------------------------------------------------
if submit:
    if not current_role or not target_role:
        st.warning("Please enter both current role and target role.")
        st.stop()

    with st.spinner("🧠 LLM Council is debating your career roadmap..."):
        career_raw, content_raw = run_multi_llm_council(
            current_role=current_role,
            target_role=target_role,
            years_exp=years_exp
        )

    st.session_state.career_plan = format_final_plan(career_raw)
    st.session_state.content_plan = content_raw.strip()

# -------------------------------------------------
# Display Career Plan (if exists)
# -------------------------------------------------
if st.session_state.career_plan:
    st.subheader("📌 Final Agreed Career Roadmap")
    st.write(st.session_state.career_plan)

    st.subheader("🎓 Best Learning Resources (Top Rated & Popular)")
    st.write(st.session_state.content_plan)

# -------------------------------------------------
# Resume Gap Analysis
# -------------------------------------------------
if st.session_state.career_plan:
    st.subheader("📄 Resume Gap Analysis")

    uploaded_resume = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

    run_comparison = st.button(
        "🔍 Compare Resume with Target Role",
        key="btn_compare_resume",
        disabled=not uploaded_resume
    )

    if run_comparison:
        with st.spinner("Analyzing resume against target role..."):
            resume_text = parse_resume(uploaded_resume)

            st.session_state.gap_analysis = asyncio.run(
                analyze_resume_against_plan(
                    resume_text=resume_text,
                    career_plan=st.session_state.career_plan
                )
            )

            st.session_state.resume_improvements = asyncio.run(
                generate_resume_improvements(
                    st.session_state.gap_analysis
                )
            )

    if st.session_state.gap_analysis:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Target Role Expectations")
            st.write(st.session_state.career_plan)

        with col2:
            st.subheader("📄 Resume Gap Analysis")
            st.write(st.session_state.gap_analysis)

        st.subheader("✍️ Resume Improvement Suggestions")
        st.write(st.session_state.resume_improvements)

# -------------------------------------------------
# 60-Day Roadmap
# -------------------------------------------------
if (
    st.session_state.career_plan
    and st.session_state.gap_analysis
    and st.session_state.resume_improvements
):
    st.subheader("🗓️ 60-Day Execution Roadmap")

    generate_roadmap_btn = st.button(
        "📅 Generate 60-Day Roadmap",
        key="btn_generate_roadmap"
    )

    if generate_roadmap_btn:
        with st.spinner("Building a 60-day execution roadmap..."):
            st.session_state.roadmap_text = asyncio.run(
                generate_60_day_roadmap(
                    career_plan=st.session_state.career_plan,
                    gap_analysis=st.session_state.gap_analysis,
                    resume_improvements=st.session_state.resume_improvements
                )
            )

    if st.session_state.roadmap_text:
        st.subheader("📍 Your 60-Day Roadmap")
        st.write(st.session_state.roadmap_text)

        excel_file = roadmap_to_excel(st.session_state.roadmap_text)

        st.download_button(
            label="⬇️ Download 60-Day Roadmap (Excel)",
            data=excel_file,
            file_name="60_day_career_roadmap.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn_download_roadmap_excel"
        )

# -------------------------------------------------
# Copy Everything (Single Button)
# -------------------------------------------------
if st.session_state.career_plan:
    combined_output = f"""
CAREER ROADMAP
==============
{st.session_state.career_plan}

LEARNING CONTENT
================
{st.session_state.content_plan}

RESUME GAP ANALYSIS
===================
{st.session_state.gap_analysis or "Not generated"}

RESUME IMPROVEMENTS
===================
{st.session_state.resume_improvements or "Not generated"}

60-DAY ROADMAP
==============
{st.session_state.roadmap_text or "Not generated"}
"""

    st.divider()
    copy_button(combined_output)
