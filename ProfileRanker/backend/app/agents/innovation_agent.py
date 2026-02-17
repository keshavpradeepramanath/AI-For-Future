INNOVATION_KEYWORDS = [
    "innovation", "patent", "research", "published","defensive publication",
    "award", "prototype", "r&d"
]

def score_innovation(text: str):
    text = text.lower()
    score = 0
    matched = []

    for keyword in INNOVATION_KEYWORDS:
        if keyword in text:
            score += 8
            matched.append(keyword)

    return {"innovation_score": score, "innovation_signals": matched}
