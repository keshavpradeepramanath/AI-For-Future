from openai import OpenAI

def recommend_transport(
    origin: str,
    destination: str,
    preferences: dict,
    api_key: str
):
    """
    Returns:
    {
      "mode": str,
      "sustainability_score": int (0–5),
      "summary": str
    }
    """

    if not api_key:
        raise ValueError("OpenAI API key is required")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a sustainable transport planner.

Route: {origin} to {destination}
Travel pace: {preferences["pace"]}
Traveling with: {preferences["kids"]}

Choose ONE best transport mode that balances:
- Sustainability (lower emissions)
- Total travel time
- Comfort and fatigue

Return ONLY:

Mode: <Train / Bus / Car / Flight / Ferry>
Score: <0-5>
Summary: <1-2 sentences>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You recommend balanced, sustainable transport."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return _parse_transport(response.choices[0].message.content)


def _parse_transport(text: str):
    mode = ""
    score = 0
    summary = ""

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Mode:"):
            mode = line.replace("Mode:", "").strip()
        elif line.startswith("Score:"):
            score = int(line.replace("Score:", "").strip())
        elif line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()

    if not summary:
        summary = "Balanced choice considering sustainability and practicality."

    return {
        "mode": mode,
        "sustainability_score": score,
        "summary": summary
    }
