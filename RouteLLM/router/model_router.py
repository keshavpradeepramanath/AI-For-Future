def route_model(intent: str) -> str:
    mapping = {
        "general": "gpt-3.5",
        "design": "gpt-4o",
        "math": "gemini",
        "coding": "claude"
    }
    return mapping.get(intent, "gpt-3.5")
