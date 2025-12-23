import os
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI

# -------------------------------
# CONFIG
# -------------------------------
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

st.set_page_config(page_title="Gmail Spam Deletion Agent", layout="wide")
st.title("📧 Gmail Spam & Promotion Cleanup Agent")

# -------------------------------
# SESSION STATE INIT (CRITICAL)
# -------------------------------
if "emails" not in st.session_state:
    st.session_state.emails = []

if "deleted_ids" not in st.session_state:
    st.session_state.deleted_ids = set()

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# -------------------------------
# API KEY INPUT
# -------------------------------
st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# -------------------------------
# GMAIL AUTH
# -------------------------------
def get_gmail_credentials():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


creds = get_gmail_credentials()
service = build("gmail", "v1", credentials=creds)

# -------------------------------
# GMAIL HELPERS
# -------------------------------
def fetch_emails(max_results=5):
    results = service.users().messages().list(
        userId="me",
        q="in:inbox",
        maxResults=max_results
    ).execute()

    emails = []
    for msg in results.get("messages", []):
        data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()

        headers = {h["name"]: h["value"] for h in data["payload"]["headers"]}

        emails.append({
            "id": msg["id"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", "")
        })

    return emails


def delete_email(msg_id):
    service.users().messages().trash(
        userId="me",
        id=msg_id
    ).execute()

# -------------------------------
# LLM CLASSIFIER
# -------------------------------
def classify_email(subject, sender):
    client = OpenAI()

    prompt = f"""
Classify the email into one category:
- SPAM
- PROMOTIONAL
- IMPORTANT

Respond ONLY with one label.

Subject: {subject}
From: {sender}
"""

    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt
    )

    return response.output_text.strip()

# -------------------------------
# UI CONTROLS
# -------------------------------
st.sidebar.subheader("🔍 Test Settings")
num_emails = st.sidebar.slider("Emails to analyze", 1, 10, 5)

if st.sidebar.button("Analyze Emails"):
    st.session_state.emails = fetch_emails(num_emails)
    st.session_state.analyzed = True
    st.session_state.deleted_ids.clear()

# -------------------------------
# DISPLAY EMAILS
# -------------------------------
if st.session_state.analyzed:

    st.subheader("📬 Inbox Emails")

    if not st.session_state.emails:
        st.info("No emails found.")
    else:
        for email in st.session_state.emails:

            # Skip deleted ones
            if email["id"] in st.session_state.deleted_ids:
                continue

            label = classify_email(email["subject"], email["from"])

            st.markdown("---")
            st.write(f"**From:** {email['from']}")
            st.write(f"**Subject:** {email['subject']}")
            st.write(f"**Agent Decision:** `{label}`")

            if label in ["SPAM", "PROMOTIONAL"]:
                if st.button("🗑 Move to Bin", key=email["id"]):
                    delete_email(email["id"])
                    st.session_state.deleted_ids.add(email["id"])
                    st.success("Email moved to Bin")

# -------------------------------
# DEBUG (OPTIONAL)
# -------------------------------
# st.write("Deleted IDs:", st.session_state.deleted_ids)
