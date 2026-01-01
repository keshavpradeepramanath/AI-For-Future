import streamlit as st

from auth import get_credentials
from gmail_service import get_gmail_service
from gmail_tools import search_gmail, fetch_metadata
from agent import agent_decide
from executor import move_to_trash

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Gmail Cleanup Agent",
    layout="centered"
)

st.title("🤖 Gmail Cleanup Agent")
st.caption("Agent-assisted Gmail bulk cleanup with confirmation")

# --------------------------------------------------
# OpenAI API Key Input
# --------------------------------------------------
api_key = st.text_input(
    "Enter OpenAI API Key",
    type="password",
    help="Stored only for this session"
)

if api_key:
    st.session_state["api_key"] = api_key

if "api_key" not in st.session_state:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# --------------------------------------------------
# Gmail OAuth
# --------------------------------------------------
try:
    creds = get_credentials()
    service = get_gmail_service(creds)
except Exception as e:
    st.error("Failed to authenticate Gmail.")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# Keyword Selection UI
# --------------------------------------------------
st.subheader("Search Emails")

company_keywords = [
    "Tata",
    "Infosys",
    "Amazon",
    "Google",
    "Microsoft"
]

selected_company = st.selectbox(
    "Select a company keyword",
    options=["-- Select --"] + company_keywords
)

custom_keyword = st.text_input(
    "Or enter a custom keyword"
)

# --------------------------------------------------
# Decide final keyword
# --------------------------------------------------
final_keyword = None

col1, col2 = st.columns(2)

with col1:
    search_company_btn = st.button("Search Company Emails")

with col2:
    search_custom_btn = st.button("Search Custom Keyword")

if search_company_btn:
    if selected_company == "-- Select --":
        st.warning("Please select a company keyword.")
        st.stop()
    final_keyword = selected_company

if search_custom_btn:
    if not custom_keyword.strip():
        st.warning("Please enter a custom keyword.")
        st.stop()
    final_keyword = custom_keyword

# --------------------------------------------------
# Analyze Inbox (Agent Step)
# --------------------------------------------------
if final_keyword:

    with st.spinner(f"Fetching emails for '{final_keyword}'..."):
        messages = search_gmail(service, final_keyword)

    if not messages:
        st.info("No matching emails found.")
        st.stop()

    emails = [fetch_metadata(service, msg["id"]) for msg in messages]

    with st.spinner("Agent is reviewing emails..."):
        recommended_ids = agent_decide(
            api_key=st.session_state["api_key"],
            keyword=final_keyword,
            emails=emails
        )

    st.session_state["emails"] = emails
    st.session_state["recommended"] = recommended_ids

# --------------------------------------------------
# Display Results
# --------------------------------------------------
if "emails" in st.session_state:

    st.subheader("Agent-reviewed emails (max 20)")

    for email in st.session_state["emails"]:
        is_selected = email["id"] in st.session_state["recommended"]
        icon = "✅" if is_selected else "❌"

        st.markdown(
            f"{icon} **{email['subject']}**  \n"
            f"{email['from']}"
        )

    st.divider()

    st.info(
        f"Agent recommends moving "
        f"{len(st.session_state['recommended'])} email(s) to Trash."
    )

    confirm = st.checkbox(
        "I confirm that ONLY the agent-recommended emails should be moved to Trash"
    )

    if confirm and st.button("Execute Bulk Move to Trash"):
        with st.spinner("Moving emails to Trash..."):
            move_to_trash(
                service,
                st.session_state["recommended"]
            )

        st.success("Selected emails moved to Trash successfully.")
        st.session_state.clear()
