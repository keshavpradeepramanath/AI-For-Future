# agents/day_regeneration_agent.py

from openai import OpenAI
from prompts.activity_prompt import get_activity_generation_prompt

def regenerate_day(
    day_key: str,
    full_plan: dict,
    preferences: dict,
    llm_provider: str,
    api_key: str
):
    if llm_provider != "OpenAI":
        return full_plan[day_key]

    client = OpenAI(api_key=api_key)

    context = f"""
You are regenerating ONLY {day_key}.

Other days are FIXED and must not be changed.

Existing plan:
{full_plan}

Regenerate ONLY {day_key}.

Rules:
1. Return ONLY activities for this day
2. Each activity must be a concrete, real place or experience
3. Use bullet points (- or •)
4. Do NOT include explanations
5. Do NOT repeat activities from other days
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a careful travel planner."},
            {"role": "user", "content": context}
        ],
        temperature=0.6
    )

    return _parse_single_day(response.choices[0].message.content)


def _parse_single_day(text: str):
    activities = []
    current = None

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("- Activity:"):
            current = {
                "title": line.replace("- Activity:", "").strip(),
                "why": ""
            }
            activities.append(current)
            continue

        if line.startswith("Why:") and current:
            current["why"] = line.replace("Why:", "").strip()

    if not activities:
        raise ValueError("Regeneration returned no activities")

    return activities
