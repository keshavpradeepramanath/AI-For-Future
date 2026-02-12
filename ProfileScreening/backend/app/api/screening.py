from fastapi import APIRouter, UploadFile, File
from app.core.parsing.file_parser import parse_file
from app.core.screening.screening_engine import screen_candidate

router = APIRouter()

@router.post("/evaluate")
async def evaluate_candidate(
    jd_file: UploadFile = File(...),
    resume_file: UploadFile = File(...)
):
    job_description = parse_file(jd_file)
    candidate_profile = parse_file(resume_file)

    result = await screen_candidate(
        job_description=job_description,
        candidate_profile=candidate_profile
    )

    return result
