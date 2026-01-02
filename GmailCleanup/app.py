import streamlit as st
from collections import defaultdict

from auth import get_credentials
from gmail_service import get_gmail_service
from gmail_tools import search_gmail, fetch_metadata
from agent import agent_decide
from executor import move_to_trash


# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Gmail Cleanup – Company-wise",
    layout="centered"
)

st.title("📧 Gmail Cleanup – Company-wise View")
st.caption("Search → Agent selects → Review → Confirm → Trash")


# --------------------------------------------------
# Helper: Extract company from sender
# --------------------------------------------------
def extract_company(from_field: str) -> str:
    known_companies = [
        "Tata",
        "Amazon",
        "Google",
        "Microsoft",
        "Infosys",
        "Flipkart",
        "Wipro",
        "Accenture"
    ]

    if not from_field:
        return "Others"

    from_lower = from_field.lower()
    for company in known_companies:
        if company.lower() in from_lower:
            return company

    return "Others"


# --------------------------------------------------
# Gemini API Key (UI input)
# --------------------------------------------------
api_key = st.text_input(
    "Enter Gemini API Key",
    type="password",
    help="Free key from Google AI Studio. Stored only for this session."
)

if api_key:
    st.session_state["api_key"] = api_key

if "api_key" not in st.session_state:
    st.warning("Please enter your Gemini API key to continue.")
    st.stop()


# --------------------------------------------------
# Gmail OAuth
# --------------------------------------------------
try:
    creds = get_credentials()
    service = get_gmail_service(creds)
except Exception as e:
    st.error("Gmail authentication failed.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# Search UI
# --------------------------------------------------
st.subheader("Search Emails")

company_keywords = ["Tata", "Amazon", "Google", "Microsoft", "Infosys"]

selected_company = st.selectbox(
    "Select a company",
    options=["-- Select --"] + company_keywords
)

custom_keyword = st.text_input("Or enter a custom keyword")

col1, col2 = st.columns(2)
final_keyword = None

with col1:
    if st.button("Search Company Emails"):
        if selected_company == "-- Select --":
            st.warning("Please select a company.")
            st.stop()
        final_keyword = selected_company

with col2:
    if st.button("Search Custom Keyword"):
        if not custom_keyword.strip():
            st.warning("Please enter a keyword.")
            st.stop()
        final_keyword = custom_keyword.strip()


# --------------------------------------------------
# Fetch emails + Agent selection
# --------------------------------------------------
if final_keyword:

    with st.spinner(f"Fetching emails for '{final_keyword}'..."):
        messages = search_gmail(service, final_keyword)

    if not messages:
        st.info("No matching emails found.")
        st.stop()

    # Fetch metadata (MESSAGE IDs only)
    emails = [fetch_metadata(service, msg["id"]) for msg in messages]

    # Attach company labels
    for email in emails:
        email["company"] = extract_company(email.get("from", ""))

    # Agent selects IDs (may be empty)
    agent_ids = agent_decide(
        api_key=st.session_state["api_key"],
        keyword=final_keyword,
        emails=emails
    )

    # -------------------------------
    # HARD SAFETY: sanitize IDs
    # -------------------------------
    valid_message_ids = {
        e["id"] for e in emails
        if isinstance(e.get("id"), str) and e["id"].strip()
    }

    recommended_ids = {
        i.strip()
        for i in agent_ids
        if isinstance(i, str) and i.strip() and i.strip() in valid_message_ids
    }

    # Fallback if agent returns nothing usable
    if not recommended_ids:
        st.warning(
            "Agent could not confidently select emails. "
            "Defaulting to ALL displayed emails."
        )
        recommended_ids = valid_message_ids.copy()

    st.session_state["emails"] = emails
    st.session_state["recommended"] = recommended_ids


# --------------------------------------------------
# Company-wise UI display (NO IDs SHOWN)
# --------------------------------------------------
if "emails" in st.session_state:

    st.subheader("Company-wise Emails")

    company_map = defaultdict(list)
    for email in st.session_state["emails"]:
        company_map[email["company"]].append(email)

    recommended_set = set(st.session_state["recommended"])

    for company, mails in company_map.items():

        st.markdown(f"### 📌 {company}")

        for mail in mails:
            selected = mail["id"] in recommended_set
            icon = "✅" if selected else "❌"

            st.markdown(
                f"{icon} **{mail['subject']}**  \n"
                f"<small>{mail['from']}</small>",
                unsafe_allow_html=True
            )

    st.divider()

    confirm = st.checkbox(
        "I confirm that ONLY the selected emails should be moved to Trash"
    )

    if confirm:
        if st.button("Execute Bulk Move to Trash"):
            with st.spinner("Moving emails to Trash..."):
                move_to_trash(
                    service,
                    list(recommended_set)
                )

            st.success("Emails moved to Trash successfully.")
            st.session_state.clear()
