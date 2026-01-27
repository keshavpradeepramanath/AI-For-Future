# agents/activity_agent.py

from prompts.activity_prompt import get_activity_generation_prompt

def generate_activities(
    preferences: dict,
    llm_provider: str = "Mock",
    api_key: str | None = None
):
    prompt = get_activity_generation_prompt(preferences)

    # ---------------------------
    # MOCK MODE
    # ---------------------------
    if llm_provider == "Mock":
        return _mock_plan(preferences)

    # ---------------------------
    # OPENAI / OTHER PROVIDERS (TEMP FALLBACK)
    # ---------------------------
    if llm_provider in ["OpenAI", "Azure OpenAI", "Local LLM"]:
        # TEMP: Until real LLM integration is added
        # We still return a valid plan
        return _mock_plan(preferences)

    # ---------------------------
    # UNKNOWN PROVIDER
    # ---------------------------
    raise ValueError(f"Unsupported LLM provider: {llm_provider}")


def _mock_plan(preferences: dict):
    plan = {}

    for day in range(1, preferences["days"] + 1):
        activities = [
            f"Relaxed exploration of {preferences['destination']}",
            "Local food experience"
        ]

        if preferences["kids"] != "Adults only":
            activities.append("Park or family-friendly attraction")

        plan[f"Day {day}"] = activities

    return plan
