def move_to_trash(service, message_ids):
    """
    Move Gmail messages to Trash safely.
    """
    for msg_id in message_ids:
        if not isinstance(msg_id, str) or not msg_id.strip():
            continue  # skip invalid IDs

        try:
            service.users().messages().trash(
                userId="me",
                id=msg_id.strip()
            ).execute()
        except Exception as e:
            print(f"Failed to trash ID {msg_id}: {e}")
