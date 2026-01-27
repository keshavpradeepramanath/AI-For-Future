import streamlit as st
from agents.preference_agent import interpret_preferences
from agents.activity_agent import generate_activities
from agents.evaluator_agent import evaluate_plan
from agents.refinement_agent import refine_plan

st.set_page_config(page_title="Agentic Activity Planner", layout="wide")

st.title("🧭 Agentic Travel Activity Planner")
st.caption("Smart, pace-aware, family-friendly travel planning")

# ---------------- Session State ----------------
if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "Mock"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ---------------- Sidebar: Model Config ----------------
st.sidebar.header("🤖 Model Configuration")

provider = st.sidebar.selectbox(
    "Select Model Provider",
    ["Mock", "OpenAI", "Azure OpenAI", "Local LLM"]
)

api_key = ""
if provider != "Mock":
    api_key = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Your API key is stored only for this session"
    )

st.session_state.llm_provider = provider
st.session_state.api_key = api_key

st.sidebar.divider()

# ---------------- Sidebar: Travel Preferences ----------------
st.sidebar.header("✈️ Travel Preferences")

destination = st.sidebar.text_input("Destination", "Rome")
days = st.sidebar.slider("Trip Duration (Days)", 1, 10, 4)

travel_pace = st.sidebar.selectbox(
    "Travel Pace",
    ["Slow", "Medium", "Fast"]
)

kids = st.sidebar.selectbox(
    "Traveling with",
    ["Adults only", "Kids (5+ years)", "Infants / Toddlers"]
)

food_interest = st.sidebar.selectbox(
    "Food Exploration Level",
    ["Low", "Medium", "High"]
)

budget = st.sidebar.selectbox(
    "Budget Comfort",
    ["Low", "Medium", "High"]
)

# ---------------- Run Agentic Flow ----------------
if st.button("✨ Generate My Plan"):
    if provider != "Mock" and not api_key:
        st.warning("Please provide an API key or switch to Mock mode.")
    else:
        with st.spinner("Agents are planning your trip..."):
            preferences = interpret_preferences(
                destination, days, travel_pace, kids, food_interest, budget
            )

            draft_plan = generate_activities(
                preferences,
                llm_provider=st.session_state.llm_provider,
                api_key=st.session_state.api_key
            )

            evaluation = evaluate_plan(draft_plan, preferences)
            final_plan = refine_plan(draft_plan, evaluation)

        st.success("Your personalized activity plan is ready!")

        for day, activities in final_plan.items():
            st.subheader(day)
            for act in activities:
                st.write(f"• {act}")
