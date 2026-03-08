from fastapi import APIRouter, UploadFile, File
import asyncio

from app.core.parser import extract_text
from app.services.candidate_store import store_candidates
from app.agents.llm_screening_agent import evaluate_candidate

router = APIRouter()


@router.post("/screen")
async def screen_candidates(
    jd_file: UploadFile = File(...),
    resumes: list[UploadFile] = File(...)
):

    jd_text = await extract_text(jd_file)

    tasks = []

    for resume in resumes:

        resume_text = await extract_text(resume)

        tasks.append(
            evaluate_candidate(jd_text, resume_text)
        )

    results = await asyncio.gather(*tasks)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(results):
        r["rank"] = i + 1

    store_candidates(results)

    return {"results": results}