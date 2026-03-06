from fastapi import APIRouter, UploadFile, File
from app.core.parser import extract_text
from app.agents.llm_screening_agent import screen_resume

router = APIRouter()


@router.post("/screen")

async def screen_candidates(
    jd_file: UploadFile = File(...),
    resumes: list[UploadFile] = File(...)
):

    jd_text = await extract_text(jd_file)

    results = []

    for resume in resumes:

        resume_text = await extract_text(resume)

        decision_data = await screen_resume(jd_text, resume_text)

        results.append({
            "candidate_name": decision_data["candidate_name"],
            "score": decision_data["score"],
            "decision": decision_data["decision"],
            "reason": decision_data["reason"]
        })

    return {"results": results}
