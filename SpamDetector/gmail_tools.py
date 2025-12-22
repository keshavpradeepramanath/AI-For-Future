from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]

def get_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)

def fetch_emails(service, max_results=5):
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = []
    for msg in results.get("messages", []):
        data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()

        headers = {h["name"]: h["value"] for h in data["payload"]["headers"]}
        messages.append({
            "id": msg["id"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", "")
        })

    return messages

def delete_email(service, msg_id):
    """
    Moves the email to Gmail Bin (Trash).
    This is the correct and only supported way.
    """
    service.users().messages().trash(
        userId="me",
        id=msg_id
    ).execute()




