from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import asyncio
import json

from app.core.parser import extract_text
from app.agents.llm_screening_agent import evaluate_candidate
from app.services.candidate_store import store_candidates

router = APIRouter()


async def stream_screening(jd_text, resumes):

    yield f"data: {json.dumps({'status':'Parsing resumes'})}\n\n"

    tasks = []
    resume_texts = []

    for resume in resumes:
        text = await extract_text(resume)
        resume_texts.append(text)

    for i, text in enumerate(resume_texts):

        yield f"data: {json.dumps({'status':f'Evaluating resume {i+1}/{len(resume_texts)}'})}\n\n"

        result = await evaluate_candidate(jd_text, text)

        tasks.append(result)

    yield f"data: {json.dumps({'status':'Ranking candidates'})}\n\n"

    results = sorted(tasks, key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(results):
        r["rank"] = i + 1

    store_candidates(results)

    yield f"data: {json.dumps({'status':'Completed','results':results})}\n\n"


@router.post("/screen-stream")
async def screen_stream(
    jd_file: UploadFile = File(...),
    resumes: list[UploadFile] = File(...)
):

    jd_text = await extract_text(jd_file)

    generator = stream_screening(jd_text, resumes)

    return StreamingResponse(generator, media_type="text/event-stream")