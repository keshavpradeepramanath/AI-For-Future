import streamlit as st
from agents.council.orchestrator import run_multi_llm_council
from utils.clipboard import copy_button

st.set_page_config(page_title="LLM Council Career Planner", layout="wide")

st.title("🚀 LLM Council Career Planner")
st.caption("Multiple top LLMs debate and agree on your career roadmap")

with st.form("career_form"):
    current_role = st.text_input("Current Role", placeholder="Software Engineer")
    years_exp = st.number_input("Years of Experience", min_value=0, max_value=40, step=1)
    target_role = st.text_input("Target Role", placeholder="Senior / Staff / AI Engineer")

    submit = st.form_submit_button("Generate Career Roadmap")

from utils.formatting import format_final_plan

if submit:
    with st.spinner("LLM Council is debating your career..."):
        raw_plan = run_multi_llm_council(current_role, target_role, years_exp)
        st.write("DEBUG RAW PLAN:", raw_plan)

    final_plan = format_final_plan(raw_plan)

    st.subheader("📌 Final Agreed Career Plan")
    st.write(final_plan)

    st.divider()
    copy_button(final_plan)
