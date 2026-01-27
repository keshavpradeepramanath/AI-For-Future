from openai import OpenAI

def score_day_sustainability(
    day_name: str,
    activities: list[str],
    destination: str,
    llm_provider: str,
    api_key: str
):
    """
    Returns:
    {
      "score": int (0–5),
      "summary": str
    }
    """

    if llm_provider != "OpenAI":
        return {
            "score": 3,
            "summary": "Moderate impact day with a mix of walking and tourist activities."
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a sustainable tourism expert.

Destination: {destination}
Day: {day_name}

Activities:
{chr(10).join(f"- {a}" for a in activities)}

Evaluate the overall sustainability of THIS DAY.

Consider:
- Walkability / transport usage
- Crowd intensity
- Support for local economy
- Environmental footprint

Return ONLY:

Score: <0-5>
Summary: <one or two sentences explaining the score>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You score travel days for sustainability."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return _parse_day_score(response.choices[0].message.content)


def _parse_day_score(text: str):
    score = 0
    summary = ""

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Score:"):
            score = int(line.replace("Score:", "").strip())
        elif line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()

    return {
        "score": score,
        "summary": summary
    }
