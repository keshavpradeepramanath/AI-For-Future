def move_to_trash(service, message_ids):
    for msg_id in message_ids:
        service.users().messages().trash(
            userId="me",
            id=msg_id
        ).execute()
