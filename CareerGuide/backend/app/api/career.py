from fastapi import APIRouter
from pydantic import BaseModel
from app.core.council.orchestrator import run_multi_llm_council

router = APIRouter()

class CareerRequest(BaseModel):
    current_role: str
    target_role: str
    years_exp: int

@router.post("/generate")
def generate_career(req: CareerRequest):
    career_plan, learning_content = run_multi_llm_council(
        req.current_role,
        req.target_role,
        req.years_exp
    )

    return {
        "career_plan": career_plan,
        "learning_content": learning_content
    }
