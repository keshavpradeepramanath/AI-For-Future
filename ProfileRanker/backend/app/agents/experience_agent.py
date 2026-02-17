import re

def score_experience(text: str):
    text = text.lower()
    match = re.search(r"(\d+)\s+years", text)

    if match:
        years = int(match.group(1))
        score = min(years * 5, 40)
    else:
        years = 0
        score = 0

    return {"experience_years": years, "experience_score": score}
