import streamlit as st
from agents.research_agent import research_role
from agents.skill_agent import extract_skills
from agents.course_agent import recommend_courses
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Career Agent", layout="wide")

st.title("🚀 AI Career Preparation Agent")
st.caption("Built like a real product, not a demo")

with st.form("career_form"):
    current_role = st.text_input("Current Role", placeholder="Software Engineer")
    years_exp = st.number_input("Years of Experience", min_value=0, max_value=40, step=1)
    target_role = st.text_input("Target Role", placeholder="Senior Software Engineer / Staff Engineer / AI Engineer")

    submit = st.form_submit_button("Generate Career Plan")

if submit:
    with st.spinner("Researching industry expectations..."):
        research = research_role(current_role, target_role, years_exp)

    with st.spinner("Identifying required skillsets..."):
        skills = extract_skills(research)

    with st.spinner("Curating best learning resources..."):
        courses = recommend_courses(skills, target_role)

    st.subheader("📌 Role Expectations")
    st.write(research)

    st.subheader("🧠 Required Skillsets")
    st.write(skills)

    st.subheader("🎓 Recommended Courses")
    st.write(courses)

    full_output = f"""
    AI CAREER PREPARATION PLAN
    =========================

    ROLE EXPECTATIONS
    -----------------
    {research}

    REQUIRED SKILLSETS
    ------------------
    {skills}

    RECOMMENDED COURSES
    -------------------
    {courses}
    """



    st.divider()

    

    components.html(
    f"""
    <textarea id="careerOutput" style="display:none;">
    {full_output}
    </textarea>

    <button
        onclick="
            const text = document.getElementById('careerOutput').value;
            navigator.clipboard.writeText(text);
            this.innerText='✅ Copied!';
            setTimeout(() => this.innerText='📋 Copy Full Answer', 2000);
        "
        style="
            padding:10px 16px;
            font-size:14px;
            border-radius:6px;
            border:none;
            background-color:#4CAF50;
            color:white;
            cursor:pointer;
        "
    >
        📋 Copy Full Answer
    </button>
    """,
    height=80,
    )