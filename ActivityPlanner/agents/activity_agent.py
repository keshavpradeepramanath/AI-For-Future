from openai import OpenAI
from prompts.activity_prompt import get_activity_generation_prompt

def generate_activities(
    preferences: dict,
    llm_provider: str = "Mock",
    api_key: str | None = None
):
    # ---------------------------
    # MOCK MODE (only for demos)
    # ---------------------------
    if llm_provider == "Mock":
        return _mock_plan(preferences)

    # ---------------------------
    # OPENAI MODE (REAL CONTENT)
    # ---------------------------
    if llm_provider == "OpenAI":
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

    raise ValueError(f"Unsupported LLM provider: {llm_provider}")


def _parse_llm_output(text: str) -> dict:
    plan = {}
    current_day = None

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("Day"):
            current_day = line.replace(":", "")
            plan[current_day] = []
        elif line.startswith("-") and current_day:
            plan[current_day].append(line.replace("-", "").strip())

    return plan
