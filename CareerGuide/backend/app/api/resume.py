from fastapi import APIRouter, UploadFile, File, Form
from app.core.resume.resume_parser import parse_resume
from app.core.resume.resume_analyzer import analyze_resume_against_plan
from app.core.resume.resume_gap_chair import generate_resume_improvements

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    career_plan: str = Form(...),
    file: UploadFile = File(...)
):
    resume_text = parse_resume(file.file)

    gap = await analyze_resume_against_plan(resume_text, career_plan)
    improvements = await generate_resume_improvements(gap)

    return {
        "gap_analysis": gap,
        "resume_improvements": improvements
    }
