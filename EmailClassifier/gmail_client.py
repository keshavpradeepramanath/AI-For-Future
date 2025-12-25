import base64

def fetch_emails(service, sender_filter=None, max_results=200):
    """
    Fetch emails from Gmail.
    Optionally filter by sender using Gmail search syntax.
    """

    # Build Gmail search query
    query = f"from:{sender_filter}" if sender_filter else ""

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    emails = []

    for msg in results.get("messages", []):
        data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = {
            h["name"]: h["value"]
            for h in data["payload"]["headers"]
        }

        body = ""

        # Extract text/plain body safely
        parts = data["payload"].get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain" and "data" in part["body"]:
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
                break

        emails.append({
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "body": body
        })

    return emails
