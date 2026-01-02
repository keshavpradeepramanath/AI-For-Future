def search_gmail(service, keyword, max_results=20):
    query = f"{keyword} -in:trash"
    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    # messages[].id is MESSAGE ID (correct)
    return result.get("messages", [])


def fetch_metadata(service, msg_id):
    # msg_id MUST be messages[].id
    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["From", "Subject"]
    ).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

    return {
        "id": msg_id,   # MESSAGE ID ONLY
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", "")
    }
