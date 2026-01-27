import streamlit as st

from agents.preference_agent import interpret_preferences
from agents.activity_agent import generate_activities
from agents.evaluator_agent import evaluate_plan
from agents.refinement_agent import refine_plan
from agents.day_regeneration_agent import regenerate_day
from agents.sustainability_agent import score_day_sustainability
from agents.transport_agent import recommend_transport

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Agentic Sustainable Travel Planner",
    layout="wide"
)

st.title("🧭 Agentic Sustainable Travel Planner")
st.caption(
    "Stateful planning • Day-level regeneration • Sustainability-aware transport"
)

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "final_plan" not in st.session_state:
    st.session_state.final_plan = None

if "preferences" not in st.session_state:
    st.session_state.preferences = None

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# -------------------------------------------------
# Sidebar – Model Configuration
# -------------------------------------------------
st.sidebar.header("🤖 Model Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Stored only for this session"
)

st.session_state.api_key = api_key

st.sidebar.divider()

# -------------------------------------------------
# Sidebar – Travel Preferences
# -------------------------------------------------
st.sidebar.header("✈️ Travel Preferences")

destinations_input = st.sidebar.text_area(
    "Destinations (one per line)",
    value="Split\nDubrovnik",
    help="Enter one city or place per line"
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
    if not api_key:
        st.warning("Please provide your OpenAI API key.")
    elif not destinations:
        st.warning("Please enter at least one destination.")
    else:
        with st.spinner("Agents are planning your trip..."):
            preferences = interpret_preferences(
                destinations=destinations,
                days=days,
                pace=travel_pace,
                kids=kids,
                food=food_interest,
                budget=budget
            )

            draft_plan = generate_activities(
                preferences=preferences,
                api_key=api_key
            )

            evaluation = evaluate_plan(draft_plan, preferences)
            final_plan = refine_plan(draft_plan, evaluation)

            if isinstance(final_plan, dict) and final_plan:
                st.session_state.final_plan = final_plan
                st.session_state.preferences = preferences
                st.success("Your personalized itinerary is ready!")
            else:
                st.session_state.final_plan = None
                st.error("Failed to generate a valid plan. Please try again.")

# -------------------------------------------------
# Display Itinerary
# -------------------------------------------------
if isinstance(st.session_state.final_plan, dict) and st.session_state.final_plan:
    st.header("📅 Your Itinerary")

    destinations = st.session_state.preferences["destinations"]
    day_keys = list(st.session_state.final_plan.keys())

    for i, day in enumerate(day_keys):
        activities = st.session_state.final_plan[day]

        st.subheader(day)

        for act in activities:
            st.write(f"• {act}")

        # 🌱 Sustainability (PER DAY)
        sustainability = score_day_sustainability(
            day_name=day,
            activities=activities,
            destination=destinations[min(i, len(destinations) - 1)],
            api_key=st.session_state.api_key
        )

        st.markdown(
            f"🌱 **Sustainability Score:** `{sustainability['score']} / 5`"
        )
        st.caption(sustainability["summary"])

        # 🚆 Transport between destinations
        if i < len(destinations) - 1:
            origin = destinations[i]
            next_city = destinations[i + 1]

            transport = recommend_transport(
                origin=origin,
                destination=next_city,
                preferences=st.session_state.preferences,
                api_key=st.session_state.api_key
            )

            st.markdown("🚦 **Travel to Next Destination**")
            st.write(
                f"**Recommended Mode:** {transport['mode']}  \n"
                f"🌱 Sustainability: {transport['sustainability_score']} / 5  \n"
                f"{transport['summary']}"
            )

        st.divider()

    # -------------------------------------------------
    # Day-Level Regeneration
    # -------------------------------------------------
    st.sidebar.header("🔁 Regenerate a Day")

    day_to_regenerate = st.sidebar.selectbox(
        "Select Day",
        day_keys
    )

    if st.sidebar.button("Regenerate Selected Day"):
        if not api_key:
            st.warning("Please provide your OpenAI API key.")
        else:
            with st.spinner(f"Regenerating {day_to_regenerate}..."):
                updated_activities = regenerate_day(
                    day_key=day_to_regenerate,
                    full_plan=st.session_state.final_plan,
                    preferences=st.session_state.preferences,
                    api_key=api_key
                )

                st.session_state.final_plan[day_to_regenerate] = updated_activities

            st.success(f"{day_to_regenerate} updated successfully!")
