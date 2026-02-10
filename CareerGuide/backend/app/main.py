from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Career AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.career import router as career_router
from app.api.resume import router as resume_router
from app.api.roadmap import router as roadmap_router

app.include_router(career_router, prefix="/api/career")
app.include_router(resume_router, prefix="/api/resume")
app.include_router(roadmap_router, prefix="/api/roadmap")
