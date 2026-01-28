from openai import OpenAI
from prompts.activity_prompt import get_activity_generation_prompt

def generate_activities(preferences: dict, api_key: str):
    """
    Generates a full multi-day itinerary using OpenAI
    """

    if not api_key:
        raise ValueError("OpenAI API key is required")

    client = OpenAI(api_key=api_key)
    prompt = get_activity_generation_prompt(preferences)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert travel planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    raw_text = response.choices[0].message.content
    return _parse_llm_output(raw_text)


def _parse_llm_output(text: str) -> dict:
    plan = {}
    current_day = None
    current_activity = None

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("day"):
            current_day = line.replace(":", "")
            plan[current_day] = []
            continue

        if line.startswith("- Activity:") and current_day:
            current_activity = {
                "title": line.replace("- Activity:", "").strip(),
                "why": ""
            }
            plan[current_day].append(current_activity)
            continue

        if line.startswith("Why:") and current_activity:
            current_activity["why"] = line.replace("Why:", "").strip()

    if not plan:
        raise ValueError("LLM returned empty itinerary")

    return plan
