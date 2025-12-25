import streamlit as st
import os
from googleapiclient.discovery import build

from gmail_auth import get_gmail_credentials
from gmail_client import fetch_emails
from sender_agent import normalize_sender
from summary_agent import summarize_email
from intent_agent import classify_intent
from aggregation import aggregate_by_company

# -------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------
st.set_page_config(
    page_title="Email Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Email Categorization & Trend Intelligence")

st.markdown(
    """
This app:
- Reads emails from Gmail
- Understands **email content** (not sender assumptions)
- Classifies emails into intent labels
- Aggregates counts per **company & category**
"""
)

# -------------------------------------------------
# Sidebar Inputs
# -------------------------------------------------
st.sidebar.header("🔐 Configuration")

openai_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

max_emails = st.sidebar.slider(
    "Number of emails to analyze",
    min_value=50,
    max_value=500,
    value=200,
    step=50
)

# -------------------------------------------------
# Main Action Button (ALWAYS visible)
# -------------------------------------------------
analyze_clicked = st.button("🚀 Analyze Emails")

# -------------------------------------------------
# Processing Logic (runs ONLY after click)
# -------------------------------------------------
if analyze_clicked:

    # -------- Validate OpenAI Key --------
    if not openai_key:
        st.error("Please enter your OpenAI API key to continue.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_key

    # -------- Gmail Authentication --------
    try:
        creds = get_gmail_credentials()
        service = build("gmail", "v1", credentials=creds)
    except Exception as e:
        st.error(f"Gmail authentication failed: {e}")
        st.stop()

    # -------- Fetch Emails --------
    
        # -------- Fetch Emails --------
    with st.spinner("📥 Fetching emails from Gmail..."):
        emails = fetch_emails(service, max_results=max_emails)

    st.write("📬 Emails fetched:", len(emails))

    if not emails:
        st.warning("No emails found. Try increasing max emails.")
        st.stop()

    enriched_emails = []
    failed = 0

    # -------- Content Understanding --------
    with st.spinner("🧠 Understanding email content..."):
        for idx, email in enumerate(emails, start=1):
            try:
                if not email.get("subject") and not email.get("body"):
                    failed += 1
                    continue

                company = normalize_sender(email["from"])
                summary = summarize_email(
                    email.get("subject", ""),
                    email.get("body", "")
                )
                label = classify_intent(summary)

                enriched_emails.append({
                    "company": company,
                    "label": label
                })

            except Exception as e:
                failed += 1
                st.warning(f"⚠️ Failed to process email #{idx}: {e}")

    st.write("✅ Emails processed:", len(enriched_emails))
    st.write("❌ Emails skipped:", failed)

    if not enriched_emails:
        st.error("No emails could be processed. Check logs above.")
        st.stop()


    # -------- Content Understanding --------
    enriched_emails = []

    with st.spinner("🧠 Understanding email content..."):
        for email in emails:
            try:
                company = normalize_sender(email["from"])
                summary = summarize_email(
                    email["subject"],
                    email["body"]
                )
                label = classify_intent(summary)

                enriched_emails.append({
                    "company": company,
                    "label": label
                })

            except Exception:
                # Skip problematic emails safely
                continue

    # -------- Aggregation --------
    stats = aggregate_by_company(enriched_emails)

    if not stats:
        st.error("Aggregation returned no results.")
        st.stop()

    st.subheader("📌 Company-wise Email Classification")

    for company, labels in stats.items():
        st.markdown(f"### 🏢 {company}")
        for label, count in labels.items():
            st.write(f"{label} → {count}")

    # -------- Display Results --------
    st.subheader("📌 Company-wise Email Classification")

    for company, labels in stats.items():
        with st.expander(f"🏢 {company}", expanded=True):
            for label, count in sorted(
                labels.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                st.write(f"**{label}** → {count}")

    st.success("Analysis complete ✅")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Agentic Email Intelligence | Content-driven classification | No sender assumptions"
)
