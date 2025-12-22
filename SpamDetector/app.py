import os
import streamlit as st
from google.oauth2.credentials import Credentials
from gmail_tools import get_gmail_service, fetch_emails, delete_email
from agent import classify_email
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

if "deleted_ids" not in st.session_state:
    st.session_state.deleted_ids = set()

st.title("📧 Gmail Spam & Promotions Cleanup Agent")

# OpenAI key
st.sidebar.subheader("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]



def get_gmail_credentials():
    creds = None

    # 1️⃣ Load existing token.json if it exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 2️⃣ If no valid creds, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 3️⃣ Save token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds



# Gmail OAuth (assumes credentials.json already exists)
creds = get_gmail_credentials()



service = get_gmail_service(creds)

st.subheader("🔍 Test with a few emails")
num_emails = st.slider("Number of emails to test", 1, 10, 5)

if st.button("Analyze Emails"):
    emails = fetch_emails(service, max_results=num_emails)

    for email in emails:
        if email["id"] in st.session_state.deleted_ids:
            continue
        label = classify_email(
            email["subject"],
            email["from"],
            email["subject"]  # body omitted for speed
        )

        st.markdown("---")
        st.write(f"**From:** {email['from']}")
        st.write(f"**Subject:** {email['subject']}")
        st.write(f"**Agent classification:** `{label}`")

        if label in ["SPAM", "PROMOTIONAL"]:
            if st.button(f"Delete this email", key=email["id"]):
                delete_email(service, email["id"])
                st.success("Email deleted")




