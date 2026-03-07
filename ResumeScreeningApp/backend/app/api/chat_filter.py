from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.candidate_store import get_candidates

router = APIRouter()


class Query(BaseModel):
    query: str


SIMILARITY_THRESHOLD = 0.72


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/filter")
async def filter_candidates(data: Query):

    candidates = get_candidates()

    if not candidates:
        return {"results": [], "message": "No candidates available"}

    query_embedding = await generate_embedding(data.query)

    filtered = []

    for c in candidates:

        emb = c.get("embedding")

        if emb is None:
            continue

        similarity = cosine_similarity(query_embedding, emb)

        if similarity >= SIMILARITY_THRESHOLD:
            filtered.append((similarity, c))

    if not filtered:
        return {"results": [], "message": "No candidates matched your query"}

    filtered.sort(key=lambda x: x[0], reverse=True)

    results = [x[1] for x in filtered]

    return {"results": results}