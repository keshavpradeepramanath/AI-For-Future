from fastapi import APIRouter, UploadFile, File
import numpy as np

from app.core.parser import extract_text
from app.services.embedding_service import generate_embedding
from app.services.candidate_store import store_candidates

from app.agents.llm_screening_agent import screen_resume
from app.agents.risk_analysis_agent import analyze_risk
from app.agents.interview_agent import generate_interview_insights

router = APIRouter()


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/screen")
async def screen_candidates(
    jd_file: UploadFile = File(...),
    resumes: list[UploadFile] = File(...)
):

    jd_text = await extract_text(jd_file)

    jd_embedding = await generate_embedding(jd_text)

    results = []

    for resume in resumes:

        resume_text = await extract_text(resume)

        resume_embedding = await generate_embedding(resume_text)

        similarity = cosine_similarity(jd_embedding, resume_embedding)

        score = int(similarity * 100)

        screening = await screen_resume(jd_text, resume_text)

        risk = await analyze_risk(jd_text, resume_text)

        insights = await generate_interview_insights(jd_text, resume_text)

        candidate = {
            "candidate_name": screening["candidate_name"],
            "score": score,
            "decision": screening["decision"],
            "reason": screening["reason"],
            "risk_level": risk["risk_level"],
            "strength": insights["strength"],
            "skill_gap": insights["skill_gap"],
            "interview_question": insights["interview_question"],
            "embedding": resume_embedding
        }

        results.append(candidate)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    for idx, r in enumerate(results):
        r["rank"] = idx + 1

    store_candidates(results)

    return {"results": results}