from app.agents.skill_agent import score_skills
from app.agents.innovation_agent import score_innovation
from app.agents.experience_agent import score_experience

def rank_resumes(resumes: list):

    ranked = []

    for resume in resumes:
        text = resume["text"]

        skill = score_skills(text)
        innovation = score_innovation(text)
        experience = score_experience(text)

        final_score = (
            skill["skill_score"] * 0.5 +
            innovation["innovation_score"] * 0.2 +
            experience["experience_score"] * 0.3
        )

        ranked.append({
            "name": resume["name"],
            "final_score": round(final_score, 2),
            "skills": skill["matched_skills"],
            "innovation": innovation["innovation_signals"],
            "experience_years": experience["experience_years"]
        })

    ranked_sorted = sorted(ranked, key=lambda x: x["final_score"], reverse=True)
    return ranked_sorted
