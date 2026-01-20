import os
import streamlit as st

from src.core.config_loader import ConfigLoader
from src.core.logger import setup_logger
from src.agents.planner_agent import PlannerAgent
from src.agents.executor_agent import ExecutorAgent
from src.agents.critic_agent import CriticAgent
from src.agents.travel_agent import TravelAgent
from src.tools.tavily_search import TavilySearch

from langchain_google_genai import ChatGoogleGenerativeAI


# ----------------------------
# App & Config Initialization
# ----------------------------
config = ConfigLoader.load()
logger = setup_logger()

st.set_page_config(
    page_title=config["app"]["title"],
    layout="wide"
)
st.title(config["app"]["title"])


# ----------------------------
# Sidebar: API Configuration
# ----------------------------
st.sidebar.header("🔐 Model Configuration")

gemini_api_key = st.sidebar.text_input(
    "Enter your Google Gemini API Key",
    type="password",
    help="Your Gemini API key is used only for this session and never stored."
)

tavily_api_key = st.sidebar.text_input(
    "Enter your Tavily Search API Key",
    type="password",
    help="Required for real-time web search."
)

model_name = st.sidebar.selectbox(
    "Select Gemini Model",
    options=[
        "gemini-3-pro-preview"
    ],
    index=0
)


# ----------------------------
# Session State
# ----------------------------
if "agent" not in st.session_state:
    st.session_state.agent = None


def initialize_agent():
    """
    Initialize Gemini LLM and Planner–Executor–Critic agent
    """
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.3
    )

    search_tool = TavilySearch(api_key=tavily_api_key)

    planner = PlannerAgent(llm, logger)
    executor = ExecutorAgent(llm, search_tool, logger)
    critic = CriticAgent(llm, logger)

    return TravelAgent(planner, executor, critic, logger)


# ----------------------------
# Main Input UI
# ----------------------------
st.subheader("✈️ Travel Preferences")

user_input = st.text_area(
    "Describe your trip (destination, days, budget, travel style, etc.)",
    height=220
)

generate_clicked = st.button("🚀 Generate Itinerary")


# ----------------------------
# Validation & Execution
# ----------------------------
if generate_clicked:

    if not gemini_api_key:
        st.error("❌ Please enter your Google Gemini API key.")
        st.stop()

    if not tavily_api_key:
        st.error("❌ Please enter your Tavily Search API key.")
        st.stop()

    if not user_input.strip():
        st.error("❌ Please enter travel details.")
        st.stop()

    # Securely inject Gemini API key
    os.environ["GOOGLE_API_KEY"] = gemini_api_key

    models = client.models.list()
    for model in models:
        print(model.name)

    # Initialize agent once per session
    if st.session_state.agent is None:
        with st.spinner("Initializing Gemini agent..."):
            st.session_state.agent = initialize_agent()

    with st.spinner("🧠 Gemini is planning your trip..."):
        try:
            result = st.session_state.agent.run(user_input)
            st.success("✅ Itinerary Generated")
            st.markdown(result)

        except Exception as e:
            logger.exception("Itinerary generation failed")
            st.error(f"❌ Error: {str(e)}")
