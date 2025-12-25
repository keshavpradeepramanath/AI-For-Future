import streamlit as st
import os
import pandas as pd
from datetime import datetime
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
**What this app does**
- Reads emails from your Gmail account (OAuth-based)
- Understands **email content** (not sender assumptions)
- Classifies intent (Promotional, Bank Statement, Due Payment, etc.)
- Aggregates counts per **company & category**
- Allows CSV export for future reference
"""
)

# -------------------------------------------------
# Session State Initialization (CRITICAL)
# -------------------------------------------------
if "enriched_emails" not in st.session_state:
    st.session_state.enriched_emails = []

# -------------------------------------------------
# Sidebar Inputs
# -------------------------------------------------
st.sidebar.header("🔐 Configuration")

openai_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

sender_filter = st.sidebar.text_input(
    "Filter by sender (optional)",
    placeholder="hdfc / icici / makemytrip"
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
# Processing Logic
# -------------------------------------------------
if analyze_clicked:

    # -------- Validate API Key --------
    if not openai_key:
        st.error("Please enter your OpenAI API key.")
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
    with st.spinner("📥 Fetching emails from Gmail..."):
        emails = fetch_emails(
            service,
            sender_filter=sender_filter,
            max_results=max_emails
        )

    st.write("📬 Emails fetched:", len(emails))

    if not emails:
        st.warning("No emails found. Try adjusting the sender filter or email count.")
        st.stop()

    # Reset previous results
    st.session_state.enriched_emails = []
    failed = 0

    # -------- Processing Loop --------
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

                try:
                    month = datetime.strptime(
                        email["date"][:16], "%a, %d %b %Y"
                    ).strftime("%Y-%m")
                except:
                    month = "Unknown"

                st.session_state.enriched_emails.append({
                    "company": company,
                    "label": label,
                    "summary": summary,
                    "month": month
                })

            except Exception as e:
                failed += 1
                st.warning(f"⚠️ Failed to process email #{idx}: {e}")

    st.write("✅ Emails processed:", len(st.session_state.enriched_emails))
    st.write("❌ Emails skipped:", failed)

    if not st.session_state.enriched_emails:
        st.error("No emails could be processed. Check warnings above.")
        st.stop()

# -------------------------------------------------
# Display Results (if available)
# -------------------------------------------------
if st.session_state.enriched_emails:

    stats = aggregate_by_company(st.session_state.enriched_emails)

    if not stats:
        st.error("Aggregation returned no results.")
        st.stop()

    st.subheader("📌 Company-wise Email Classification")

    for company, labels in stats.items():
        with st.expander(f"🏢 {company}", expanded=True):
            for label, count in sorted(
                labels.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                st.write(f"**{label}** → {count}")

    # -------------------------------------------------
    # CSV Export
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("⬇️ Export Report")

    df = pd.DataFrame(st.session_state.enriched_emails)

    st.download_button(
        label="📥 Download CSV Report",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="email_classification_report.csv",
        mime="text/csv"
    )

    st.success("Analysis complete ✅")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Agentic Email Intelligence | Content-driven classification | Streamlit + Gmail + LLMs"
)
