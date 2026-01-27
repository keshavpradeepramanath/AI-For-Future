import streamlit as st

from agents.preference_agent import interpret_preferences
from agents.activity_agent import generate_activities
from agents.evaluator_agent import evaluate_plan
from agents.refinement_agent import refine_plan
from agents.day_regeneration_agent import regenerate_day
from agents.sustainability_agent import score_day_sustainability

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Agentic Activity Planner",
    layout="wide"
)

st.title("🧭 Agentic Travel Activity Planner")
st.caption("Stateful, controllable, day-by-day intelligent planning")

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

if "preferences" not in st.session_state:
    st.session_state.preferences = None

if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "Mock"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# -------------------------------------------------
# Sidebar – Model Configuration
# -------------------------------------------------
st.sidebar.header("🤖 Model Configuration")

provider = st.sidebar.selectbox(
    "LLM Provider",
    ["Mock", "OpenAI"]
)

api_key = ""
if provider != "Mock":
    api_key = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Stored only for this session"
    )

st.session_state.llm_provider = provider
st.session_state.api_key = api_key

st.sidebar.divider()

# -------------------------------------------------
# Sidebar – Travel Preferences
# -------------------------------------------------
st.sidebar.header("✈️ Travel Preferences")

destinations_input = st.sidebar.text_area(
    "Destinations (one per line)",
    value="Split\nDubrovnik",
    help="Enter one city/place per line"
)

destinations = [
    d.strip() for d in destinations_input.split("\n") if d.strip()
]

days = st.sidebar.slider("Total Trip Duration (Days)", 1, 14, 6)

travel_pace = st.sidebar.selectbox(
    "Travel Pace",
    ["Slow", "Medium", "Fast"]
)

kids = st.sidebar.selectbox(
    "Traveling With",
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

# -------------------------------------------------
# Generate Full Plan
# -------------------------------------------------
if st.button("✨ Generate Travel Plan"):
    if provider != "Mock" and not api_key:
        st.warning("Please provide an API key or switch to Mock mode.")
    elif not destinations:
        st.warning("Please enter at least one destination.")
    else:
        with st.spinner("Agents are planning your trip..."):
            preferences = interpret_preferences(
                destinations,
                days,
                travel_pace,
                kids,
                food_interest,
                budget
            )

            draft_plan = generate_activities(
                preferences,
                llm_provider=provider,
                api_key=api_key
            )

            evaluation = evaluate_plan(draft_plan, preferences)
            final_plan = refine_plan(draft_plan, evaluation)

            st.session_state.final_plan = final_plan
            st.session_state.preferences = preferences

        st.success("Your personalized itinerary is ready!")

# -------------------------------------------------
# Display Plan
# -------------------------------------------------
if isinstance(st.session_state.final_plan, dict) and st.session_state.final_plan:
    for day, activities in st.session_state.final_plan.items():
        with st.container():
            st.subheader(day)

            for act in activities:
                st.write(f"• {act}")

            sustainability = score_day_sustainability(
                day_name=day,
                activities=activities,
                destination=st.session_state.preferences["destinations"][0],
                llm_provider=st.session_state.llm_provider,
                api_key=st.session_state.api_key
            )

            st.markdown(
                f"🌱 **Sustainability Score:** `{sustainability['score']} / 5`"
            )
            st.caption(sustainability["summary"])

            st.divider()

    # -------------------------------------------------
    # Day-Level Regeneration
    # -------------------------------------------------
    st.sidebar.header("🔁 Regenerate a Day")

    day_to_regenerate = st.sidebar.selectbox(
        "Select Day",
        list(st.session_state.final_plan.keys())
    )

    if st.sidebar.button("Regenerate Selected Day"):
        if provider == "Mock":
            st.info("Day regeneration requires an LLM provider.")
        else:
            with st.spinner(f"Regenerating {day_to_regenerate}..."):
                updated_activities = regenerate_day(
                    day_key=day_to_regenerate,
                    full_plan=st.session_state.final_plan,
                    preferences=st.session_state.preferences,
                    llm_provider=provider,
                    api_key=api_key
                )

                st.session_state.final_plan[day_to_regenerate] = updated_activities

            st.success(f"{day_to_regenerate} updated successfully!")

