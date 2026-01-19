def route_query(user_input: str):
    user_input = user_input.lower()

    if "add" in user_input:
        return {
            "tool": "add",
            "args": {"a": 5, "b": 3}
        }

    if "weather" in user_input:
        return {
            "tool": "get_weather",
            "args": {"city": "Bangalore"}
        }

    return {
        "tool": None,
        "response": "I can chat but no tool is needed."
    }
