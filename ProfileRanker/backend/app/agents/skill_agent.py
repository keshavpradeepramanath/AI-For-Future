import re

AI_SKILLS = [
    "machine learning", "deep learning", "nlp",
    "computer vision", "pytorch", "tensorflow",
    "llm", "genai", "mlops", "aws", "python"
]

def score_skills(text: str):
    text = text.lower()
    score = 0
    matched = []

    for skill in AI_SKILLS:
        if re.search(rf"\b{skill}\b", text):
            score += 10
            matched.append(skill)

    return {"skill_score": score, "matched_skills": matched}
