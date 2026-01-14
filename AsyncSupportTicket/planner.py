def plan_ticket(ticket: str) -> dict:
    ticket_lower = ticket.lower()

    if "refund" in ticket_lower or "payment" in ticket_lower:
        intent = "billing"
    elif "error" in ticket_lower or "not working" in ticket_lower:
        intent = "tech"
    else:
        intent = "general"

    urgency = "high" if "urgent" in ticket_lower else "normal"

    return {
        "intent": intent,
        "urgency": urgency,
        "ticket": ticket
    }
