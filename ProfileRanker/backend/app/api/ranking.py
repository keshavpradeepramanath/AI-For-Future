from fastapi import APIRouter, UploadFile, File
from app.core.parsing import extract_text_from_file
from app.agents.ranking_agent import rank_resumes

router = APIRouter()

@router.post("/bulk-rank")
async def bulk_rank(files: list[UploadFile] = File(...)):

    resumes = []

    for file in files:
        text = extract_text_from_file(file)
        resumes.append({
            "name": file.filename,
            "text": text
        })

    ranked = rank_resumes(resumes)
    return {"ranking": ranked}
