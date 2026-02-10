from fastapi import APIRouter
from pydantic import BaseModel
from app.core.roadmap.roadmap_generator import generate_60_day_roadmap
from app.core.roadmap.roadmap_to_excel import roadmap_to_excel
from fastapi.responses import StreamingResponse

router = APIRouter()

class RoadmapRequest(BaseModel):
    career_plan: str
    gap_analysis: str
    resume_improvements: str

@router.post("/generate")
async def generate_roadmap(req: RoadmapRequest):
    roadmap = await generate_60_day_roadmap(
        req.career_plan,
        req.gap_analysis,
        req.resume_improvements
    )
    return {"roadmap": roadmap}

@router.post("/download")
async def download_excel(req: RoadmapRequest):
    roadmap = await generate_60_day_roadmap(
        req.career_plan,
        req.gap_analysis,
        req.resume_improvements
    )
    excel = roadmap_to_excel(roadmap)

    return StreamingResponse(
        excel,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=60_day_roadmap.xlsx"}
    )
