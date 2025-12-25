import base64

def fetch_emails(service, max_results=200):
    results = service.users().messages().list(
        userId="me",
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
        parts = data["payload"].get("parts", [])
        for part in parts:
            if part["mimeType"] == "text/plain":
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
