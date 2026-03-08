from fastapi import APIRouter
from pydantic import BaseModel
from app.services.candidate_store import get_candidates

router = APIRouter()


class CompareRequest(BaseModel):
    candidates: list[str]


@router.post("/compare")
async def compare_candidates(data: CompareRequest):

    candidates = get_candidates()

    selected = [
        c for c in candidates
        if c["candidate_name"] in data.candidates
    ]

    all_skills = set()

    for c in selected:
        all_skills.update(c.get("skills", []))

    comparison = []

    for skill in sorted(all_skills):

        row = {"skill": skill}

        for c in selected:

            row[c["candidate_name"]] = (
                "✔" if skill in c.get("skills", []) else ""
            )

        comparison.append(row)

    return {
        "skills": list(all_skills),
        "comparison": comparison,
        "candidates": data.candidates
    }